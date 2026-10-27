"""The tool list and the dispatcher.

``TOOLS`` describes every tool (name, description, JSON schema, whether it
changes anything). ``dispatch(name, arguments, ctx)`` runs one: it rejects
unknown tools and unparseable arguments, applies the tool's timeout, and turns
exceptions into structured error dicts, so a caller always gets a dict back.

It knows nothing about who is calling or whether they may: approval, plan
modes and result sizing belong to the caller.
"""

from __future__ import annotations

import asyncio
import traceback
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, List, Optional

from bvbrc_mcp.context import ToolContext
from bvbrc_mcp.tools.analysis import _get_expected_outputs_async as get_expected_outputs
from bvbrc_mcp.tools.analysis import get_job_details
from bvbrc_mcp.tools.batch import prepare_batch
from bvbrc_mcp.tools.collections import get_collection_fields, list_collections
from bvbrc_mcp.tools.data import facet_query, probe_data, search_data
from bvbrc_mcp.tools.file_search import search_file
from bvbrc_mcp.tools.file_summary import summarize_file
from bvbrc_mcp.tools.gowe import get_workflow_inputs, list_gowe_workflows, submit_gowe_job
from bvbrc_mcp.tools.groups import create_group, edit_group, get_group_ids, list_groups
from bvbrc_mcp.tools.helpdesk import get_service_schema, list_services, query_helpdesk
from bvbrc_mcp.tools.jobs import list_jobs
from bvbrc_mcp.tools.literature import search_literature
from bvbrc_mcp.tools.rerun import rerun_jobs
from bvbrc_mcp.tools.samples import list_samples
from bvbrc_mcp.tools.schemas import ALL_TOOL_SCHEMAS
from bvbrc_mcp.tools.similar_genome import find_similar_genomes
from bvbrc_mcp.tools.sra import get_sra_metadata
from bvbrc_mcp.tools.workspace import get_file_metadata, read_file_preview, workspace_browse

TOOL_DISPATCH: Dict[str, Callable[..., Awaitable[Dict[str, Any]]]] = {
    "search_data": search_data,
    "facet_query": facet_query,
    "probe_data": probe_data,
    "list_collections": list_collections,
    "get_collection_fields": get_collection_fields,
    "workspace_browse": workspace_browse,
    "get_file_metadata": get_file_metadata,
    "read_file_preview": read_file_preview,
    "search_file": search_file,
    "summarize_file": summarize_file,
    "list_samples": list_samples,
    "list_gowe_workflows": list_gowe_workflows,
    "get_workflow_inputs": get_workflow_inputs,
    "submit_gowe_job": submit_gowe_job,
    "rerun_jobs": rerun_jobs,
    "prepare_batch": prepare_batch,
    "create_group": create_group,
    "edit_group": edit_group,
    "list_groups": list_groups,
    "get_group_ids": get_group_ids,
    "get_sra_metadata": get_sra_metadata,
    "find_similar_genomes": find_similar_genomes,
    "search_literature": search_literature,
    "query_helpdesk": query_helpdesk,
    "list_services": list_services,
    "get_service_schema": get_service_schema,
    "get_expected_outputs": get_expected_outputs,
    "get_job_details": get_job_details,
    "list_jobs": list_jobs,
}

# Tools that change something in the user's account.
SIDE_EFFECT_TOOLS: frozenset[str] = frozenset({"submit_gowe_job", "create_group", "edit_group"})

# Tools that legitimately run longer than the default tool timeout.
TOOL_TIMEOUT_OVERRIDES: Dict[str, float] = {
    "find_similar_genomes": 120.0,
    "search_file": 90.0,  # streams up to 25 MB from the workspace
    "summarize_file": 90.0,  # same scan
    "rerun_jobs": 90.0,  # recursive listing + query_tasks + workflow catalog
    "list_samples": 60.0,  # one folder listing of up to 500 items
    "prepare_batch": 90.0,  # workflow inputs + up to 10 GoWe dry runs
    "workspace_browse": 90.0,  # one search over every shared workspace: ~30 s for 1,264 job results
}


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable[..., Awaitable[Dict[str, Any]]]
    side_effect: bool = False
    timeout_seconds: Optional[float] = None


def _build_tools() -> List[Tool]:
    tools = []
    for schema in ALL_TOOL_SCHEMAS:
        fn = schema["function"]
        name = fn["name"]
        tools.append(Tool(
            name=name,
            description=fn["description"],
            parameters=fn["parameters"],
            handler=TOOL_DISPATCH[name],
            side_effect=name in SIDE_EFFECT_TOOLS,
            timeout_seconds=TOOL_TIMEOUT_OVERRIDES.get(name),
        ))
    return tools


TOOLS: List[Tool] = _build_tools()
TOOLS_BY_NAME: Dict[str, Tool] = {t.name: t for t in TOOLS}


def _safe_args(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Arguments without config/headers, for error reports."""
    return {k: v for k, v in arguments.items() if k not in ("config", "headers")}


def unparseable_arguments_result(tool_name: str, raw: Any) -> Dict[str, Any]:
    return {
        "error": (
            f"The arguments for '{tool_name}' were not valid JSON, so the "
            f"tool was not called. Nothing was submitted or changed. Send "
            f"the arguments again as a single JSON object."
        ),
        "invalid_arguments": True,
        "tool": tool_name,
        "received": (raw[:400] if isinstance(raw, str) else str(raw)[:400]),
    }


async def dispatch(
    tool_name: str,
    arguments: Dict[str, Any],
    ctx: Any,
    *,
    headers: Optional[Dict[str, str]] = None,
    timeout_seconds: Optional[float] = None,
    dispatch_table: Optional[Dict[str, Callable[..., Awaitable[Dict[str, Any]]]]] = None,
    inject_config: bool = True,
    inject_headers: bool = True,
) -> Dict[str, Any]:
    """Run one tool and return its result dict (errors included, never raised).

    Args:
        tool_name: A name from ``TOOLS``.
        arguments: The tool's arguments. ``_unparseable_arguments`` marks a
            call whose JSON could not be parsed; such a call is refused.
        ctx: A ``ToolContext`` (or an object with the same attributes).
        headers: Auth headers; default ``{"Authorization": ctx.bvbrc_auth_token}``.
        timeout_seconds: The caller's timeout; a tool's own longer timeout wins.
        dispatch_table: Another name -> function table (a caller that adds tools).
        inject_config: Pass ``ctx`` to the tool as ``config`` (when ctx is not None).
        inject_headers: Pass headers to the tool; when False, none are derived
            from the token either.
    """
    table = TOOL_DISPATCH if dispatch_table is None else dispatch_table
    func = table.get(tool_name)
    if func is None:
        return {"error": f"Unknown tool: '{tool_name}'", "available_tools": sorted(table)}

    arguments = dict(arguments or {})
    if "_unparseable_arguments" in arguments:
        return unparseable_arguments_result(tool_name, arguments.get("_unparseable_arguments"))

    if headers is None and inject_headers:
        token = getattr(ctx, "bvbrc_auth_token", None)
        headers = {"Authorization": token} if token else None
    base = timeout_seconds if timeout_seconds is not None else getattr(ctx, "tool_timeout_seconds", 30.0)
    timeout = max(base if base else 30.0, TOOL_TIMEOUT_OVERRIDES.get(tool_name, 0.0))

    if inject_config and ctx is not None:
        arguments.setdefault("config", ctx)
    if inject_headers and headers is not None:
        arguments.setdefault("headers", headers)

    try:
        return await asyncio.wait_for(func(**arguments), timeout=timeout)
    except asyncio.TimeoutError:
        return {
            "error": f"Tool '{tool_name}' timed out after {timeout}s",
            "tool": tool_name,
            "arguments": _safe_args(arguments),
        }
    except TypeError as e:
        return {
            "error": f"Invalid arguments for tool '{tool_name}': {e}",
            "tool": tool_name,
            "arguments": _safe_args(arguments),
        }
    except Exception as e:
        return {
            "error": f"Tool '{tool_name}' failed: {type(e).__name__}: {e}",
            "tool": tool_name,
            "arguments": _safe_args(arguments),
            "traceback": traceback.format_exc(),
        }


__all__ = [
    "SIDE_EFFECT_TOOLS",
    "TOOLS",
    "TOOLS_BY_NAME",
    "TOOL_DISPATCH",
    "TOOL_TIMEOUT_OVERRIDES",
    "Tool",
    "ToolContext",
    "dispatch",
]
