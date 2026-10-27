"""
Shared job listing tool.

Wraps the MCP server's ``service_functions.list_jobs`` to enumerate
user jobs with optional filtering, sorting, and pagination.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from bvbrc_mcp.tools._clients import get_service_functions

# App ids seen in job histories that service_mapping.json does not list, and
# a few common names for them. AppService filters on the exact app id: the
# schema's own examples ('genome_assembly', 'rnaseq') returned 0 jobs.
_EXTRA_APP_IDS = (
    "TreeSort", "HASubtypeNumberingConversion", "ComprehensiveSARS2Analysis",
    "DifferentialExpression", "MobileElementDetection", "SARS2Wastewater",
    "ProteinStructurePrediction",
)
_EXTRA_NAMES = {
    "codon_tree": "CodonTree",
    "phylogenetic_tree": "CodonTree",
    "ha_subtype_numbering": "HASubtypeNumberingConversion",
    "influenza_ha_subtype_conversion": "HASubtypeNumberingConversion",  # mapping file says InfluenzaHASubtypeConversion
    "sars2_wastewater": "SARS2Wastewater",
    "differential_expression": "DifferentialExpression",
    "mobile_element_detection": "MobileElementDetection",
    "msa": "MSA",
    "similar_genome_finder": "SimilarGenomeFinder",
}


def _norm(text: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(text or "").lower())


def _service_names() -> Dict[str, str]:
    """``{normalized name: app id}`` for app ids and common names."""
    from bvbrc_mcp.clients.service_validation_functions import _get_service_mapping

    names: Dict[str, str] = {}
    mapping = dict(_get_service_mapping())
    mapping.update(_EXTRA_NAMES)  # also corrects the mapping's influenza app id
    for app_id in list(mapping.values()) + list(_EXTRA_APP_IDS):
        names[_norm(app_id)] = app_id
    for friendly, app_id in mapping.items():
        names.setdefault(_norm(friendly), app_id)
    return names


def resolve_service(service: str) -> List[str]:
    """App ids *service* may mean: an exact app id or common name gives one;
    a partial name gives every app id it is part of; unknown text gives []."""
    q = _norm(service)
    if not q:
        return []
    names = _service_names()
    if q in names:
        return [names[q]]
    return sorted({app_id for name, app_id in names.items() if q in name})


def _extract_token(
    config: Any = None,
    headers: Optional[Dict[str, str]] = None,
) -> Optional[str]:
    """Extract BV-BRC auth token from config or headers."""
    token = getattr(config, "bvbrc_auth_token", None)
    if token:
        return token
    if headers:
        return headers.get("Authorization")
    return None


def _extract_user_id(token: str) -> Optional[str]:
    """Extract user ID from a BV-BRC auth token."""
    if not token:
        return None
    try:
        return token.split("|")[0].replace("un=", "")
    except Exception:
        return None


MAX_MERGED_SERVICES = 4

# list_jobs sort_by -> the compact job's field (service_functions.compact_job).
_MERGE_SORT_KEYS = {
    "submit_time": "submit_time", "creation_time": "submit_time",
    "start_time": "start_time", "completed_time": "completed_time", "finish_time": "completed_time",
    "app": "app", "application_name": "app", "status": "status", "id": "id",
}


async def _merged(query: Any, service: str, apps: List[str], limit: int, offset: int,
                  sort_by: str, sort_dir: str) -> Dict[str, Any]:
    """One page over several services: a partial name like "tree" fits
    CodonTree, GeneTree and TreeSort, and the model used to query each.

    Each service is asked for its first ``offset + limit`` jobs in the same
    order (in parallel); the union is merged in that order and sliced, which
    gives exactly the page a single combined query would.
    """
    import asyncio

    results = await asyncio.gather(*(query(app, 0, offset + limit) for app in apps))
    errors = [r for r in results if not isinstance(r, dict) or r.get("error")]
    if len(errors) == len(results):
        return errors[0] if isinstance(errors[0], dict) else {"error": "list_jobs failed", "source": "shared-tools"}
    items, by_service = [], {}
    for app, r in zip(apps, results):
        if isinstance(r, dict) and not r.get("error"):
            items.extend(r.get("items") or [])
            by_service[app] = r.get("total") or 0
    key = _MERGE_SORT_KEYS.get(sort_by, "submit_time")
    dated = sorted((j for j in items if j.get(key) is not None), key=lambda j: str(j[key]),
                   reverse=(sort_dir != "asc"))
    items = dated + [j for j in items if j.get(key) is None]  # missing values last either way
    page = items[offset:offset + limit]
    total = sum(by_service.values())
    result: Dict[str, Any] = {
        "items": page,
        "total": total,
        "count": len(page),
        "offset": offset,
        "limit": limit,
        "service_requested": service,
        "services": apps,
        "total_by_service": by_service,
        "jobs_page_url": "https://www.bv-brc.org/job/",
        "source": "bvbrc-service",
    }
    note = f"'{service}' fits {len(apps)} services ({', '.join(apps)}); their jobs are merged, newest first."
    if sort_dir == "asc" or key != "submit_time":
        note = note.replace(", newest first", f", by {sort_by} {sort_dir}")
    failed = [app for app, r in zip(apps, results) if not isinstance(r, dict) or r.get("error")]
    if failed:
        note += f" Could not list {', '.join(failed)}."
    result["note"] = note
    return result


async def list_jobs(
    limit: int = 20,
    offset: int = 0,
    sort_by: str = "submit_time",
    sort_dir: str = "desc",
    status: Optional[str] = None,
    service: Optional[str] = None,
    search: Optional[str] = None,
    include_archived: bool = False,
    config: Any = None,
    headers: Optional[Dict[str, str]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """List user jobs with optional filtering and sorting.

    Args:
        limit: Maximum jobs to return (default 20).
        offset: Number of jobs to skip for pagination.
        sort_by: Field to sort by (default ``submit_time``).
        sort_dir: Sort direction (``asc`` or ``desc``).
        status: Filter by job status (e.g. ``completed``, ``failed``).
        service: App id (``GenomeAssembly2``), common name (``genome_assembly``,
            ``rnaseq``) or a part of one; a part that fits up to
            ``MAX_MERGED_SERVICES`` services lists their jobs merged.
        search: Free-text search filter.
        include_archived: Include archived jobs.
        config: Agent configuration (provides auth token, MCP path).
        headers: HTTP headers (auth fallback).

    Returns:
        Dict with ``items`` (compact jobs: app, status, times, ``result_path``,
        ``output_folder``, ``inputs``), ``total``, ``count``, pagination.
    """
    token = _extract_token(config, headers)
    if not token:
        return {
            "error": "No authentication token available.",
            "source": "shared-tools",
        }

    user_id = _extract_user_id(token)

    app_id = None
    candidates: List[str] = []
    if service:
        candidates = resolve_service(service)
        if len(candidates) > MAX_MERGED_SERVICES:
            return {
                "error": f"'{service}' matches {len(candidates)} services: {', '.join(candidates)}. Pass one of them.",
                "errorType": "AMBIGUOUS_SERVICE",
                "candidates": candidates,
                "source": "shared-tools",
            }
        app_id = candidates[0] if candidates else service

    svc_fn = get_service_functions(getattr(config, "mcp_server_path", None))

    # The MCP server's JsonRpcCaller is stored on the service_functions module
    # as ``_api``.  It is set during MCP server startup by
    # ``register_service_tools()``.  For the shared-tools path we need the
    # ``list_jobs`` async function which requires an ``api`` argument.
    # The lazy-import bridge gives us the module; ``list_jobs`` is a
    # module-level async function that accepts ``api`` as the first arg.
    api = getattr(svc_fn, "_api", None)
    if api is None:
        # Fallback: import the JsonRpcCaller from the MCP common layer.
        from bvbrc_mcp.tools._clients import get_json_rpc
        json_rpc = get_json_rpc(getattr(config, "mcp_server_path", None))
        # Build a caller pointed at the BV-BRC app service endpoint
        bvbrc_url = getattr(config, "bvbrc_workspace_url", "https://p3.theseed.org/services/app_service")
        # Replace workspace_service path with app_service if needed
        if "workspace_service" in bvbrc_url:
            bvbrc_url = bvbrc_url.replace("workspace_service", "app_service")
        elif not bvbrc_url.endswith("app_service"):
            bvbrc_url = "https://p3.theseed.org/services/app_service"
        api = json_rpc.JsonRpcCaller(bvbrc_url)

    async def query(app: Optional[str], first: int, count: int) -> Dict[str, Any]:
        return await svc_fn.list_jobs(
            api=api,
            token=token,
            user_id=user_id,
            limit=count,
            offset=first,
            sort_by=sort_by,
            sort_dir=sort_dir,
            status=status,
            service=app,
            search=search,
            include_archived=include_archived,
        )

    try:
        if len(candidates) > 1:
            return await _merged(query, service, candidates, limit, offset, sort_by, sort_dir)
        result = await query(app_id, offset, limit)

        # Attach a link to the BV-BRC jobs page so the LLM can include
        # a clickable markdown link in its response.
        if isinstance(result, dict) and not result.get("error"):
            result["jobs_page_url"] = "https://www.bv-brc.org/job/"
            if service:
                result["service"] = app_id
                if app_id != service:
                    result["service_requested"] = service
                if not result.get("total") and app_id == service:
                    result["note"] = (
                        f"No jobs for app id '{service}', which is not a known service name. "
                        f"Known app ids: {', '.join(sorted(set(_service_names().values())))}."
                    )

        return result

    except Exception as e:
        return {
            "error": f"list_jobs failed: {type(e).__name__}: {str(e)}",
            "source": "shared-tools",
        }
