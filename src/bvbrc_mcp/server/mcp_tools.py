"""Register bvbrc_mcp.TOOLS on a FastMCP server as ``agent_<name>`` tools.

Each tool takes its own parameters plus an optional ``bvbrc_token``; over
HTTP the OAuth bearer token takes priority (TokenProvider). The client's own
approval is the confirmation for side-effecting tools, so they run when
called. Results are JSON, bounded by ``Settings.max_result_chars``.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

import pydantic_core
from fastmcp import FastMCP
from fastmcp.tools.tool import Tool as MCPTool, ToolResult
from mcp.types import TextContent

from bvbrc_mcp.registry import TOOLS, dispatch
from bvbrc_mcp.results import truncate_result
from bvbrc_mcp.settings import Settings, get_settings

logger = logging.getLogger(__name__)

PREFIX = "agent_"

# What happens over MCP, where the client (not a chat card) asks the user.
MCP_NOTES: Dict[str, str] = {
    "rerun_jobs": (
        "Nothing is submitted. To run the prepared jobs, call "
        "agent_submit_gowe_job with each prepared action's arguments after "
        "the user agrees."
    ),
    "prepare_batch": (
        "Nothing is submitted. To run the prepared jobs, call "
        "agent_submit_gowe_job with each prepared action's arguments after "
        "the user agrees."
    ),
    "edit_group": "The edit runs as soon as this tool is called; confirm the exact change with the user first.",
    "submit_gowe_job": "The job is submitted as soon as this tool is called.",
    "create_group": "The group is created as soon as this tool is called.",
}

TOKEN_PARAM = {
    "type": "string",
    "description": "BV-BRC auth token. Not needed when the client is signed in (OAuth).",
}


def mcp_tool_specs() -> list[dict]:
    """``{name, tool, description, parameters}`` for every tool to register."""
    specs = []
    for tool in TOOLS:
        parameters = json.loads(json.dumps(tool.parameters))
        parameters.setdefault("type", "object")
        parameters.setdefault("properties", {})["bvbrc_token"] = TOKEN_PARAM
        description = tool.description
        if tool.name in MCP_NOTES:
            description = f"{description}\n\n{MCP_NOTES[tool.name]}"
        specs.append({
            "name": PREFIX + tool.name,
            "tool": tool.name,
            "description": description,
            "parameters": parameters,
        })
    return specs


def _public_result(result: Any) -> Any:
    """Drop server internals (tracebacks) from an error before it leaves."""
    if isinstance(result, dict) and "traceback" in result:
        result = {k: v for k, v in result.items() if k != "traceback"}
    return result


class BvbrcTool(MCPTool):
    """An MCP tool that runs one bvbrc_mcp tool through ``dispatch``."""

    tool_name: str
    token_provider: Any = None
    settings: Any = None

    async def run(self, arguments: Dict[str, Any]) -> ToolResult:
        arguments = dict(arguments or {})
        explicit = arguments.pop("bvbrc_token", None)
        token = explicit
        if self.token_provider is not None:
            try:
                token = self.token_provider.get_token(explicit)
            except Exception:
                token = explicit
        settings: Settings = self.settings or get_settings()
        ctx = settings.tool_context(token)

        result = await dispatch(self.tool_name, arguments, ctx)
        result = _public_result(pydantic_core.to_jsonable_python(result, fallback=str))
        text = truncate_result(result, max_chars=settings.max_result_chars)
        try:
            structured = json.loads(text)
        except ValueError:
            structured = None
        return ToolResult(
            content=[TextContent(type="text", text=text)],
            structured_content=structured if isinstance(structured, dict) else None,
        )


def register_tools(mcp: FastMCP, token_provider: Any = None, settings: Optional[Settings] = None) -> int:
    """Register every tool on *mcp*; returns how many."""
    specs = mcp_tool_specs()
    for spec in specs:
        mcp.add_tool(BvbrcTool(
            name=spec["name"],
            description=spec["description"],
            parameters=spec["parameters"],
            tool_name=spec["tool"],
            token_provider=token_provider,
            settings=settings,
        ))
    logger.info("Registered %d BV-BRC tools (%s prefix)", len(specs), PREFIX)
    return len(specs)
