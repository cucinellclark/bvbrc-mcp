from bvbrc_mcp.clients.json_rpc import JsonRpcCaller
from typing import List, Any
import asyncio
import httpx
import requests
import os
import json
import sys
import base64
import re

import os

def _flatten_ls_result(result) -> list:
    result_list = result if isinstance(result, list) else [result]
    flat: list = []

    for entry in result_list:
        if isinstance(entry, dict):
            for val in entry.values():
                if isinstance(val, list):
                    flat.extend(val)
                else:
                    flat.append(val)
        else:
            flat.append(entry)

    # filter out items whose name (first element) starts with '.'
    return [
        item for item in flat
        if isinstance(item, list)
        and item
        and not str(item[0]).startswith(".")
    ]


def _fix_duplicated_user_id_in_path(path: str, user_id: str) -> str:
    """
    Detect and fix paths with duplicated user_id (e.g., /user@domain.com/user@domain.com/home -> /user@domain.com/home).
    
    Args:
        path: Path that may have duplicated user_id
        user_id: User ID to check for duplication
    
    Returns:
        Path with duplicated user_id removed
    """
    if not path or not user_id:
        return path
    
    # Check if path starts with /{user_id}/{user_id}/ (duplicated user_id)
    duplicated_prefix = f"/{user_id}/{user_id}/"
    if path.startswith(duplicated_prefix):
        # Remove the duplicate user_id segment
        fixed_path = f"/{user_id}/" + path[len(duplicated_prefix):]
        print(f"Fixed duplicated user_id in path: {path} -> {fixed_path}", file=sys.stderr)
        return fixed_path
    
    return path

def _fix_duplicated_user_id_in_paths(paths: List[str], user_id: str) -> List[str]:
    """
    Fix duplicated user_id in a list of paths.
    
    Args:
        paths: List of paths that may have duplicated user_id
        user_id: User ID to check for duplication
    
    Returns:
        List of paths with duplicated user_id removed
    """
    if not paths or not user_id:
        return paths
    
    return [_fix_duplicated_user_id_in_path(path, user_id) for path in paths]

async def workspace_ls(
    api: JsonRpcCaller,
    paths: List[str],
    token: str,
    file_types: List[str] = None,
    sort_by: str = None,
    sort_order: str = None,
    limit: int = None
) -> dict:
    """
    List the contents of a specific workspace directory using the JSON-RPC API.
    This is NOT a generic search function, use `workspace_search` for search functionality.

    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        paths: List of paths to list
        token: Authentication token for API calls
        file_types: Optional list of file types to filter by (e.g., ['contigs', 'folder', 'unspecified']).
                    If provided, only files/objects with these types will be returned.
        sort_by: Optional sort field. Valid options: creation_time, name, size, type.
        sort_order: Optional sort direction. Valid options: asc, desc.
        limit: Passed to the service, which ignores it (callers must cap the result).
    Returns:
        List of workspace items
    """
    try:
        # Fix any duplicated user_id in paths (defensive measure)
        user_id = _get_user_id_from_token(token)
        if user_id:
            paths = _fix_duplicated_user_id_in_paths(paths, user_id)
        
        # Build API call parameters
        # Enable recursive search when file_types is provided to search subdirectories
        if file_types:
            # file_types is already a list
            file_types_list = file_types if file_types else ['unspecified']

            # Use recursive search format matching workspace_search when filtering by type
            # Pass type as array directly (API expects array format for type filtering)
            api_params = {
                "recursive": True,
                "includeSubDirs": True,
                "excludeDirectories": False,
                "excludeObjects": False,
                "paths": paths,
                "query": {
                    "type": file_types_list
                }
            }
        else:
            # Non-recursive listing when no file_type filter.
            # Workspace.ls expects lowercase "recursive".
            api_params = {
                "recursive": False,
                "includeSubDirs": False,
                "paths": paths
            }
        # Pass backend-supported sort options through directly when provided
        if sort_by:
            api_params["sort_by"] = sort_by
        if sort_order:
            api_params["sort_order"] = sort_order
        if limit is not None:
            api_params["limit"] = limit

        # Only include file_types_list in print if it was defined
        print_msg = f"workspace_ls file_types: {file_types}, Query params: {json.dumps(api_params, indent=2)}"
        if file_types:
            print_msg = f"workspace_ls file_types: {file_types}, file_types_list: {file_types_list}, Query params: {json.dumps(api_params, indent=2)}"
        print(print_msg, file=sys.stderr)
        result = await api.acall("Workspace.ls", api_params, 1, token)

        # Standardize response structure
        # Workspace.ls returns [{path: [item1, item2, ...]}] — unwrap the inner items
        flat_items = _flatten_ls_result(result)
        return {
            "items": flat_items,
            "count": len(flat_items),
            "path": paths[0] if paths else "/",
            "source": "bvbrc-workspace"
        }
    except Exception as e:
        if "Object not found" in str(e):
            return {
                "error": "Object not found",
                "errorType": "NOT_FOUND",
                "source": "bvbrc-workspace"
            }
        return {
            "error": f"Error listing workspace: {str(e)}",
            "errorType": "API_ERROR",
            "source": "bvbrc-workspace"
        }

NAME_MATCH_MODES = ("all", "any", "word")


def name_regex(terms: List[str] = None, extensions: List[str] = None, mode: str = "all") -> str:
    """One case-insensitive regex for name terms and extensions.

    Used as the ``Workspace.ls`` query (Mongo/PCRE) and, with Python's ``re``,
    on our side, so both match the same names. Terms are literal text
    (escaped: ``TanA+`` or ``sample (1)`` used to be sent as regex). *mode*:
    ``all`` = every term, ``any`` = at least one, ``word`` = every term as a
    whole word, where only letters count as word characters, so
    ``Bacillus_group_1`` matches "bacillus" and ``Lactobacillus`` does not.
    Extensions: the name ends with any of them. Returns "" for no filter.
    """
    terms = [re.escape(str(t)) for t in (terms or []) if str(t or "").strip()]
    exts = [re.escape(str(e).lstrip(".")) for e in (extensions or []) if str(e or "").strip(".").strip()]
    if mode == "word":
        terms = [f"(?<![a-z]){t}(?![a-z])" for t in terms]
    if not terms:
        lookaheads = ""
    elif mode == "any":
        lookaheads = "(?=.*(?:" + "|".join(terms) + "))"
    else:
        lookaheads = "".join(f"(?=.*{t})" for t in terms)
    if exts:
        return lookaheads + r".*\.(?:" + "|".join(exts) + ")$"
    return lookaheads


async def workspace_search(
    api: JsonRpcCaller,
    paths: List[str] = None,
    filename_search_terms: List[str] = None,
    file_extension: List[str] = None,
    file_types: List[str] = None,
    token: str = None,
    sort_by: str = None,
    sort_order: str = None,
    limit: int = None,
    name_match: str = "all"
) -> dict:
    """
    Search the entire workspace for a given term and/or file extension and/or file type.

    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        paths: List of paths to search
        filename_search_terms: Optional list of terms to search for within file/object names. All terms must appear in the name (AND logic).
                               Example: ["genome", "bacteria"] will match files containing both words in their name.
        file_extension: Optional list of file extensions to filter by (e.g., ['py', 'txt', 'json']).
                       Can include or exclude the leading dot. Multiple extensions use OR logic.
        file_types: Optional list of file types to filter by (e.g., ['contigs', 'folder', 'unspecified']).
                   If provided, only files/objects with these types will be returned. This filters by the workspace object type,
                   not by file extension, so it can match files with different extensions that share the same type.
        token: Authentication token for API calls
        sort_by: Optional sort field. Valid options: creation_time, name, size, type.
        sort_order: Optional sort direction. Valid options: asc, desc.
        limit: Passed to the service, which ignores it (callers must cap the result).
        name_match: How the search terms combine: "all", "any", or "word" (all, whole words); see ``name_regex``.
    Returns:
        List of matching workspace items
    """
    if not paths:
        user_id = _get_user_id_from_token(token)
        if not user_id:
            return {
                "error": "Unable to derive user id from token",
                "errorType": "INVALID_PARAMETERS",
                "source": "bvbrc-workspace"
            }
        paths = [f"/{user_id}/home"]
    else:
        # Fix any duplicated user_id in paths (defensive measure)
        user_id = _get_user_id_from_token(token)
        if user_id:
            paths = _fix_duplicated_user_id_in_paths(paths, user_id)

    name_pattern = name_regex(filename_search_terms, file_extension, name_match)
    query_conditions = {}
    if name_pattern:
        query_conditions["name"] = {"$regex": name_pattern, "$options": "i"}
    if file_types:
        # Pass type as array directly (API expects array format for type filtering).
        query_conditions["type"] = file_types
    if not query_conditions:
        # No explicit filters: perform recursive search under provided paths
        query_conditions = None

    try:
        api_params = {
            "recursive": True,
            "excludeDirectories": False,
            "excludeObjects": False,
            "includeSubDirs": True,
            "paths": paths
        }
        if query_conditions is not None:
            api_params["query"] = query_conditions
        if sort_by:
            api_params["sort_by"] = sort_by
        if sort_order:
            api_params["sort_order"] = sort_order
        if limit is not None:
            api_params["limit"] = limit

        result = await api.acall("Workspace.ls", api_params, 1, token)

        # Standardize response structure
        # Workspace.ls returns [{path: [item1, item2, ...]}] — unwrap the inner items
        flat_items = _flatten_ls_result(result)
        return {
            "items": flat_items,
            "count": len(flat_items),
            "filename_search_terms": filename_search_terms,
            "paths": paths,
            "source": "bvbrc-workspace"
        }
    except Exception as e:
        if "Object not found" in str(e):
            return {
                "error": "Object not found",
                "errorType": "NOT_FOUND",
                "source": "bvbrc-workspace"
            }
        return {
            "error": f"Error searching workspace: {str(e)}",
            "errorType": "API_ERROR",
            "source": "bvbrc-workspace"
        }

# Workspace.ls tuple: [name, type, parent_path, creation_time, id, owner, size, ...]
_SORT_INDEX = {"name": 0, "type": 1, "creation_time": 3, "size": 6}
_SUMMARY_TOP = 15
_MAX_PARALLEL_ROOTS = 8


def _sort_pairs(pairs: list, sort_by: str = None, sort_order: str = None, search: bool = False) -> list:
    """Sort ``(root, tuple)`` pairs by the tuple's field, on our side.

    Done here so that "the first N" after the cap means the requested order.
    Without *sort_by*: a search shows the newest first, a folder listing
    shows folders first and then names (as the website does). The service's
    own order is unspecified.
    """
    idx = _SORT_INDEX.get(sort_by)
    if idx is None:
        if search:
            return sorted(pairs, key=lambda p: str(p[1][3] if len(p[1]) > 3 else "") or "", reverse=True)
        return sorted(pairs, key=lambda p: (p[1][1] != "folder" if len(p[1]) > 1 else True,
                                            str(p[1][0] or "").lower()))

    def key(pair):
        item = pair[1]
        value = item[idx] if len(item) > idx else None
        if idx == 6:
            try:
                return (0, float(value))
            except (TypeError, ValueError):
                return (1, 0.0)
        return (0, str(value or "").lower())

    return sorted(pairs, key=key, reverse=(sort_order == "desc"))


def _rel_segments(item: list, root: str) -> List[str]:
    """Folder names between *root* and the item (empty for a direct child)."""
    parent = str(item[2] or "") if len(item) > 2 else ""
    root = root.rstrip("/")
    rel = parent[len(root):] if parent.startswith(root) else parent
    return [seg for seg in rel.split("/") if seg]


def _in_hidden_folder(item: list, root: str) -> bool:
    """True when the item lies inside a dot-folder below *root*.

    Dot-folders are job output folders (``.<job name>/``) and ``.chats/``.
    Only the part below the search root counts, so browsing inside a job
    output folder on purpose still finds its files.
    """
    return any(seg.startswith(".") for seg in _rel_segments(item, root))


def _matches_filters(item: list, name_pattern: Any = None, types: List[str] = None) -> bool:
    """The search filters, applied on our side to a one-folder listing.

    *name_pattern* is the compiled ``name_regex`` the service gets for a
    search, so both match the same names; any type.
    """
    if name_pattern is not None and not name_pattern.search(str(item[0] or "")):
        return False
    if types and (len(item) < 2 or item[1] not in types):
        return False
    return True


_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?Z?)?$")


def valid_date(value: Any) -> bool:
    """``YYYY-MM-DD`` or ``YYYY-MM-DDTHH:MM[:SS][Z]`` (compared as text with the
    ISO creation times ``Workspace.ls`` returns)."""
    return bool(_DATE.match(str(value or "")))


def _in_date_range(item: list, created_after: str = None, created_before: str = None) -> bool:
    """Created on/after *created_after* and before *created_before* (ISO text)."""
    ctime = str(item[3] or "") if len(item) > 3 else ""
    if created_after and not (ctime and ctime >= created_after):
        return False
    if created_before and not (ctime and ctime < created_before):
        return False
    return True


def _top_counts(counts: dict) -> dict:
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0])))
    out = dict(ranked[:_SUMMARY_TOP])
    if len(ranked) > _SUMMARY_TOP:
        out["(others)"] = sum(n for _, n in ranked[_SUMMARY_TOP:])
    return out


def _summarize_items(pairs: list, by_folder: bool, by_root: bool) -> dict:
    """Counts by type, total size, oldest/newest; by subfolder (one-root
    search) or by root (several roots)."""
    by_type: dict = {}
    folders: dict = {}
    roots: dict = {}
    size = 0
    times = []
    for root, item in pairs:
        typ = item[1] if len(item) > 1 else None
        by_type[typ] = by_type.get(typ, 0) + 1
        try:
            size += int(item[6] or 0)
        except (TypeError, ValueError, IndexError):
            pass
        if len(item) > 3 and item[3]:
            times.append(str(item[3]))
        if by_root:
            roots[root] = roots.get(root, 0) + 1
        elif by_folder:
            segs = _rel_segments(item, root)
            top = segs[0] if segs else "(this folder)"
            folders[top] = folders.get(top, 0) + 1

    summary = {"by_type": _top_counts(by_type), "total_size": size}
    if times:
        summary["oldest"], summary["newest"] = min(times), max(times)
    if by_root:
        summary["by_root"] = _top_counts(roots)
    elif by_folder:
        summary["by_folder"] = _top_counts(folders)
    return summary


async def workspace_browse(
    api: JsonRpcCaller,
    token: str,
    path: str = None,
    search: bool = False,
    filename_search_terms: List[str] = None,
    file_extension: List[str] = None,
    file_types: List[str] = None,
    sort_by: str = None,
    sort_order: str = None,
    num_results: int = 50,
    offset: int = 0,
    recursive: bool = None,
    max_depth: int = None,
    include_job_outputs: bool = False,
    paths: List[str] = None,
    name_match: str = "all",
    created_after: str = None,
    created_before: str = None,
    tool_name: str = "workspace_browse_tool"
) -> dict:
    """
    Unified workspace browser entrypoint.

    - recursive=True: search everything under path (or user home by default).
    - recursive=False: inspect path and return its folder listing or the
      file/object metadata. Filters apply to that one folder.
    - recursive=None (not given): recursive when *search* or any filter is set
      (the behaviour before ``recursive`` existed).
    - *paths* (two or more): list or search each of them (in parallel, one
      ``Workspace.ls`` per root, so an unreadable root does not sink the
      others); every result item keeps its full path, the summary counts by
      root, and roots that failed are listed in ``unreadable``.

    ``Workspace.ls`` ignores ``limit`` and ``offset`` and always returns
    everything, so results are filtered, sorted and paged here.

    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        token: Authentication token for API calls
        path: Path to inspect/search. Defaults to user home if not provided.
        search: Old switch for recursive search; used only when *recursive* is None.
        filename_search_terms: Terms that must all appear in the name (case-insensitive).
        file_extension: Extension filters (OR logic).
        file_types: Workspace type filters (OR logic).
        sort_by: Optional sort field. Valid options: creation_time, name, size, type.
        sort_order: Optional sort direction. Valid options: asc, desc.
        num_results: Page size. Defaults to 50.
        offset: Index of the first item to return (from a previous ``next_offset``).
        recursive: Search under path instead of listing it.
        max_depth: With recursive, how many folder levels below path to search
                   (0 = path itself only, 1 = its subfolders too, ...).
        include_job_outputs: Search inside hidden folders (job outputs, ``.chats``) too.
        paths: Several folders at once (overrides *path* when it has 2+ entries).
        name_match: How name terms combine: "all", "any", or "word" (see ``name_regex``).
        created_after / created_before: ISO date range (after inclusive, before exclusive).
        tool_name: Name of the calling tool (for response envelope).

    Returns a consistent response envelope with all data nested under "result":
      {
        "result": {
          "items": <array> | "metadata": <dict>,  // items for search/list, metadata for file/object
          "tool_name": <tool name>,
          "result_type": "search_result" | "list_result" | "metadata_result",
          "count": <number>,      // items returned (search/list)
          "total": <number>,      // items matched (search/list)
          "truncated": <bool>,    // more matched than returned (search/list)
          "offset", "next_offset": paging (next_offset only when more remain)
          "summary": {by_type, total_size, oldest, newest, by_folder | by_root}
          "hidden_in_job_outputs": <number>,  // search only, when > 0
          "path": <workspace path> | "paths": [<roots>], "unreadable": [...]
          "source": "bvbrc-workspace"
        }
      }
    """
    if not token:
        return {
            "error": "Authentication token not provided",
            "errorType": "INVALID_PARAMETERS",
            "source": "bvbrc-workspace"
        }

    roots = list(dict.fromkeys(p for p in (paths or []) if p))
    if len(roots) == 1:
        path, roots = roots[0], []

    if not roots and (not path or path == '/'):
        user_id = _get_user_id_from_token(token)
        if not user_id:
            return {
                "error": "Unable to derive user id from token",
                "errorType": "INVALID_PARAMETERS",
                "source": "bvbrc-workspace"
            }
        path = f"/{user_id}/home"

    offset = max(0, int(offset or 0))

    def _items_response(pairs: list, result_type: str, hidden: int = 0, unreadable: list = None) -> dict:
        pairs = _sort_pairs(pairs, sort_by, sort_order, search=(result_type == "search_result"))
        total = len(pairs)
        page = [item for _, item in pairs[offset:offset + num_results]]
        end = offset + len(page)
        result = {
            "items": page,
            "tool_name": tool_name,
            "result_type": result_type,
            "count": len(page),
            "total": total,
            "truncated": total > len(page),
            "offset": offset,
        }
        if roots:
            result["paths"] = roots
        else:
            result["path"] = path
        result["summary"] = _summarize_items(pairs, by_folder=(result_type == "search_result"), by_root=bool(roots))
        result["source"] = "bvbrc-workspace"
        hints = []
        if end < total:
            result["next_offset"] = end
        if result["truncated"]:
            shown = f"items {offset + 1}-{end}" if page else "no items"
            hints.append(
                f"Showing {shown} of {total}. The others exist but are not in this result: "
                "describe them from summary, say the list is partial, narrow it (filters, a "
                "subfolder) or fetch the next page with offset=next_offset if the user needs it."
            )
        if hidden:
            result["hidden_in_job_outputs"] = hidden
            hints.append(
                f"{hidden} more match{'es' if hidden != 1 else ''} inside job output folders "
                "(left out; pass include_job_outputs=true to include them)."
            )
        if unreadable:
            result["unreadable"] = unreadable
            hints.append(f"{len(unreadable)} folder(s) could not be read; see unreadable.")
        if hints:
            result["hint"] = " ".join(hints)
        return {"result": result}

    def _keep(pairs: list) -> tuple:
        """Apply the date range, max_depth and the job-output rule;
        returns (pairs, hidden), so ``hidden`` counts only full matches."""
        pairs = [(r, i) for r, i in pairs if _passes(i)]
        if max_depth is not None:
            pairs = [(r, i) for r, i in pairs if len(_rel_segments(i, r)) <= max(0, int(max_depth))]
        if include_job_outputs:
            return pairs, 0
        kept = [(r, i) for r, i in pairs if not _in_hidden_folder(i, r)]
        return kept, len(pairs) - len(kept)

    has_filters = bool(filename_search_terms) or bool(file_extension) or bool(file_types)
    pattern = name_regex(filename_search_terms, file_extension, name_match)
    name_pattern = re.compile(pattern, re.IGNORECASE) if pattern else None
    if recursive is None:
        recursive = bool(search or has_filters)
        if has_filters:
            print(f"workspace_browse: filters without recursive -> recursive search of {roots or path}", file=sys.stderr)

    async def _search(root: str) -> dict:
        return await workspace_search(
            api=api,
            paths=[root],
            filename_search_terms=filename_search_terms,
            file_extension=file_extension,
            file_types=file_types,
            token=token,
            sort_by=sort_by,
            sort_order=sort_order,
            name_match=name_match,
        )

    async def _list(root: str) -> dict:
        return await workspace_ls(api=api, paths=[root], token=token, sort_by=sort_by, sort_order=sort_order)

    def _passes(item: list) -> bool:
        return _in_date_range(item, created_after, created_before)

    def _listing(list_result: dict) -> List[list]:
        items = [i for i in list_result.get("items", []) if _passes(i)]
        if has_filters:
            items = [i for i in items if _matches_filters(i, name_pattern, file_types)]
        return items

    if roots:
        gate = asyncio.Semaphore(_MAX_PARALLEL_ROOTS)

        async def one(root: str) -> tuple:
            async with gate:
                return root, await (_search(root) if recursive else _list(root))

        pairs, unreadable = [], []
        for root, res in await asyncio.gather(*(one(r) for r in roots)):
            if "error" in res:
                unreadable.append({"path": root, "error": res.get("error")})
                continue
            items = res.get("items", []) if recursive else _listing(res)
            pairs.extend((root, i) for i in items)
        if len(unreadable) == len(roots):
            return {
                "error": f"None of the {len(roots)} folders could be read.",
                "errorType": "API_ERROR",
                "unreadable": unreadable,
                "source": "bvbrc-workspace",
            }
        hidden = 0
        if recursive:
            pairs, hidden = _keep(pairs)
        return _items_response(pairs, "search_result" if recursive else "list_result", hidden, unreadable)

    if recursive:
        search_result = await _search(path)
        if "error" in search_result:
            return search_result
        pairs, hidden = _keep([(path, i) for i in search_result.get("items", [])])
        return _items_response(pairs, "search_result", hidden)

    # Handle all public browsing in one branch. Workspace.get can fail for valid
    # public directories, so prefer Workspace.ls here.
    if path.startswith("/public"):
        # Keep /public as-is; requesting "/" can trigger permission errors.
        list_result = await _list(path)
        if "error" in list_result:
            # Do not fall through to Workspace.get on public listing failures.
            # Returning the original listing error preserves the real failure cause.
            return list_result
        return _items_response([(path, i) for i in _listing(list_result)], "list_result")

    metadata_result = await workspace_get_object(api, path, metadata_only=True, token=token)
    if "error" in metadata_result:
        return metadata_result

    metadata = metadata_result.get("metadata")
    if not metadata or not isinstance(metadata, dict):
        return {
            "error": "Invalid metadata response",
            "errorType": "INVALID_RESPONSE",
            "source": "bvbrc-workspace"
        }

    auto_meta = metadata.get("autoMeta") if isinstance(metadata.get("autoMeta"), dict) else {}
    is_folder = metadata.get("type") == "folder" or auto_meta.get("is_folder") == 1

    if is_folder:
        list_result = await _list(path)
        if "error" in list_result:
            return list_result
        return _items_response([(path, i) for i in _listing(list_result)], "list_result")

    return {
        "result": {
            "metadata": metadata,
            "tool_name": tool_name,
            "result_type": "metadata_result",
            "path": path,
            "source": "bvbrc-workspace",
        }
    }


async def workspace_get_file_metadata(api: JsonRpcCaller, path: str, token: str) -> dict:
    """
    Get the metadata of a file from the workspace using the JSON-RPC API.

    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        path: Path to the file to get the metadata of
        token: Authentication token for API calls
    Returns:
        String representation of the file metadata
    """
    try:
        result = await api.acall("Workspace.get", {
            "objects": [path],
            "metadata_only": True
        },1, token)

        # Add source field to response
        if isinstance(result, dict):
            result["source"] = "bvbrc-workspace"
            return result
        else:
            return {
                "data": result,
                "source": "bvbrc-workspace"
            }
    except Exception as e:
        if "Object not found" in str(e):
            return {
                "error": "Object not found",
                "errorType": "NOT_FOUND",
                "source": "bvbrc-workspace"
            }
        return {
            "error": f"Error getting file metadata: {str(e)}",
            "errorType": "API_ERROR",
            "source": "bvbrc-workspace"
        }


async def workspace_download_file(api: JsonRpcCaller, path: str, token: str, output_file: str = None, return_data: bool = False) -> dict:
    """
    Download a file from the workspace using the JSON-RPC API.

    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        path: Path to the file to download
        token: Authentication token for API calls
        output_file: Optional name and path of the file to save the downloaded content to.
        return_data: If True, return the file data directly (base64 encoded for binary files, text for text files).
                    If False and output_file is provided, only write to file. If False and output_file is None,
                    returns file data (default behavior for backward compatibility).
    Returns:
        If return_data is True or output_file is None: Returns file data (base64 encoded for binary, text for text files).
        If output_file is provided and return_data is False: Returns success message.
        If both output_file and return_data are True: Returns file data along with success message.
    """
    try:
        download_url_obj = await _get_download_url(api, path, token)
        download_url = download_url_obj[0][0]

        headers = {
            "Authorization": token
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(download_url, headers=headers)
            response.raise_for_status()
            content = response.content

            result_parts = []

            # Write to file if output_file is provided
            if output_file:
                with open(output_file, 'wb') as file:
                    file.write(content)
                result_parts.append(f"File downloaded and saved to {output_file}")

            # Return data if return_data is True, or if output_file is None (backward compatibility)
            if return_data or output_file is None:
                # Try to decode as text first
                try:
                    text_content = content.decode('utf-8')
                    result_parts.append(text_content)
                except UnicodeDecodeError:
                    # If it's binary, encode as base64
                    base64_content = base64.b64encode(content).decode('utf-8')
                    result_parts.append(f"<base64_encoded_data>{base64_content}</base64_encoded_data>")

            # Return appropriate result
            if len(result_parts) == 1:
                return {
                    "data": result_parts[0],
                    "source": "bvbrc-workspace"
                }
            elif len(result_parts) == 2:
                # Both file write and data return
                return {
                    "message": result_parts[0],
                    "data": result_parts[1],
                    "source": "bvbrc-workspace"
                }
            else:
                return {
                    "data": content,
                    "source": "bvbrc-workspace"
                }
    except Exception as e:
        return {
            "error": f"Error downloading file: {str(e)}",
            "errorType": "API_ERROR",
            "source": "bvbrc-workspace"
        }

async def workspace_preview_file(api: JsonRpcCaller, path: str, token: str) -> dict:
    """
    Preview a file from the workspace by downloading only the first portion using byte ranges.
    This function uses HTTP Range headers internally to download only a portion of the file.

    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        path: Path to the file to preview
        token: Authentication token for API calls
    Returns:
        Dictionary containing the preview data (text for text files, base64 for binary files)
    """
    # Keep preview as a compatibility wrapper around ranged reads.
    PREVIEW_BYTE_RANGE = 8192
    result = await workspace_read_range(
        api=api,
        path=path,
        token=token,
        start_byte=0,
        max_bytes=PREVIEW_BYTE_RANGE
    )
    if isinstance(result, dict) and not result.get("error"):
        result["preview_size"] = result.get("bytes_read", 0)
        result["is_preview"] = True
    return result

async def workspace_read_range(api: JsonRpcCaller, path: str, token: str, start_byte: int = 0, max_bytes: int = 8192) -> dict:
    """
    Read a specific byte range from a workspace file using HTTP Range headers.

    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        path: Path to the file
        token: Authentication token for API calls
        start_byte: Zero-based byte offset to start reading from
        max_bytes: Maximum number of bytes to read (capped at 1 MiB)

    Returns:
        Dictionary containing ranged file data (text for text files, base64 for binary files)
    """
    if start_byte < 0:
        return {
            "error": "start_byte must be >= 0",
            "errorType": "INVALID_PARAMETERS",
            "source": "bvbrc-workspace"
        }

    if max_bytes <= 0:
        return {
            "error": "max_bytes must be > 0",
            "errorType": "INVALID_PARAMETERS",
            "source": "bvbrc-workspace"
        }

    max_bytes = min(max_bytes, 1024 * 1024)
    end_byte = start_byte + max_bytes - 1

    try:
        download_url_obj = await _get_download_url(api, path, token)
        download_url = download_url_obj[0][0]

        headers = {
            "Authorization": token,
            "Range": f"bytes={start_byte}-{end_byte}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(download_url, headers=headers)
            if response.status_code not in (200, 206):
                response.raise_for_status()
            content = response.content

            # Detect genuinely binary content (null bytes in first 8 KB
            # or known magic bytes like PNG/JPG/ZIP/PDF) before decoding.
            # Text chunks that start mid-codepoint (e.g. from a Range
            # request on a UTF-8 file) are decoded with errors='replace'
            # instead of being base64-encoded, which would make the
            # content opaque to the LLM.
            _first = content[:8192]
            is_binary = b"\x00" in _first
            if not is_binary:
                _magic_sigs = [
                    b"\x89PNG", b"\xff\xd8\xff", b"GIF8",
                    b"PK\x03\x04", b"PK\x05\x06", b"%PDF",
                    b"\x1f\x8b", b"\x42\x5a\x68",
                    b"\xfd\x37\x7a\x58\x5a\x00", b"Rar!", b"\x7fELF",
                ]
                for sig in _magic_sigs:
                    if content[:len(sig)] == sig:
                        is_binary = True
                        break

            if is_binary:
                base64_content = base64.b64encode(content).decode("utf-8")
                data = f"<base64_encoded_data>{base64_content}</base64_encoded_data>"
            else:
                data = content.decode("utf-8", errors="replace")

            bytes_read = len(content)
            next_start = start_byte + bytes_read

            # Try to determine total file size from response headers
            total_size = None
            content_range = response.headers.get("content-range", "")
            if "/" in content_range:
                # Format: "bytes 0-8191/12345"
                try:
                    total_size = int(content_range.split("/")[-1])
                except (ValueError, IndexError):
                    pass
            if total_size is None and response.status_code == 200:
                # Full response (no range), total size is content length
                total_size = bytes_read

            is_complete = (
                total_size is not None and next_start >= total_size
            ) or bytes_read < max_bytes

            return {
                "data": data,
                "start_byte": start_byte,
                "bytes_read": bytes_read,
                "total_size": total_size,
                "is_complete": is_complete,
                "is_binary": is_binary,
                "requested_max_bytes": max_bytes,
                "next_start_byte": next_start if not is_complete else None,
                "source": "bvbrc-workspace"
            }
    except Exception as e:
        return {
            "error": f"Error reading byte range: {str(e)}",
            "errorType": "API_ERROR",
            "source": "bvbrc-workspace"
        }

async def _get_download_url(api: JsonRpcCaller, path: str, token: str) -> str:
    """
    Get the download URL of a file from the workspace using the JSON-RPC API.

    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        path: Path to the file to get the download URL of
        token: Authentication token for API calls
    Returns:
        String representation of the download URL
    """
    try:
        result = await api.acall("Workspace.get_download_url", {
            "objects": [path],
        },1, token)
        return result
    except Exception as e:
        return [f"Error getting download URL: {str(e)}"]

def _get_user_id_from_token(token: str) -> str:
    """
    Extract user ID from a BV-BRC/KBase style auth token.
    Returns None if token is None or invalid.
    """
    if not token:
        return None
    try:
        # Token format example: "un=username|..."; take first segment and strip prefix
        return token.split('|')[0].replace('un=','')
    except Exception as e:
        print(f"Error extracting user ID from token: {e}")
        return None

async def workspace_upload(api: JsonRpcCaller, filename: str, upload_dir: str = None, token: str = None) -> dict:
    """
    Create an upload URL for a file in the workspace using the JSON-RPC API.

    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        filename: Name of the file to create upload URL for
        upload_dir: Directory to upload the file to (defaults to /<user_id>/home)
        token: Authentication token for API calls (required)
    Returns:
        String representation of the upload URL response with parsed metadata
    """
    try:

        if not token:
            return {
                "error": "Authentication token not provided",
                "errorType": "INVALID_PARAMETERS",
                "source": "bvbrc-workspace"
            }

        if not upload_dir:
            user_id = _get_user_id_from_token(token)
            if not user_id:
                return {
                    "error": "Unable to derive user id from token",
                    "errorType": "INVALID_PARAMETERS",
                    "source": "bvbrc-workspace"
                }
            upload_dir = '/' + user_id + '/home'
        download_url_path = os.path.join(upload_dir,os.path.basename(filename))
        # call format: workspace file location, file type, object metadata, object content
        result = await _workspace_create(
            api,
            [[download_url_path, 'unspecified', {}, '']],
            token,
            create_upload_nodes=True,
            overwrite=None
        )

        # Parse the result if successful
        if result and len(result) > 0 and len(result[0]) > 0:
            # Extract the metadata array from result[0][0]
            meta_list = result[0][0]

            # Convert the array to a structured object
            meta_obj = {
                "id": meta_list[4],
                "path": meta_list[2] + meta_list[0],
                "name": meta_list[0],
                "type": meta_list[1],
                "creation_time": meta_list[3],
                "link_reference": meta_list[11],
                "owner_id": meta_list[5],
                "size": meta_list[6],
                "userMeta": meta_list[7],
                "autoMeta": meta_list[8],
                "user_permission": meta_list[9],
                "global_permission": meta_list[10],
                "timestamp": meta_list[3]  # Keep as string for now, could parse to timestamp if needed
            }

            upload_url = meta_obj["link_reference"]

            msg = {
                "file": os.path.basename(filename),
                "uploadDirectory": upload_dir,
                "url": upload_url,
                "source": "bvbrc-workspace"
            }

            # Upload the file to the upload URL
            print(f"Uploading file to {upload_url}")
            # Use the same timeout as the API client for consistency
            upload_timeout = getattr(api, 'timeout', 120.0)
            upload_result = _upload_file_to_url(filename, upload_url, token, timeout=upload_timeout)
            print(f"Upload result: {upload_result}")
            if upload_result.get("success"):
                msg["upload_status"] = "success"
                msg["upload_message"] = upload_result.get("message", "File uploaded successfully")
            else:
                msg["upload_status"] = "failed"
                msg["upload_error"] = upload_result.get("error", "Upload failed")

            return msg
        else:
            return {
                "error": "No valid result returned from workspace API",
                "errorType": "API_ERROR",
                "source": "bvbrc-workspace"
            }

    except Exception as e:
        return {
            "error": f"Error creating upload URL: {str(e)}",
            "errorType": "API_ERROR",
            "source": "bvbrc-workspace"
        }

async def _workspace_create(api: JsonRpcCaller, objects: list, token: str, create_upload_nodes: bool = True, overwrite: Any = None):
    """
    Helper to invoke Workspace.create via JSON-RPC.
    """
    try:
        return await api.acall(
            "Workspace.create",
            {
                "objects": objects,
                "createUploadNodes": create_upload_nodes,
                "overwrite": overwrite
            },
            1,
            token
        )
    except Exception as e:
        return [f"Error creating workspace object: {str(e)}"]

def _upload_file_to_url(filename: str, upload_url: str, token: str, timeout: float = 120.0) -> dict:
    """
    Upload a file to the specified Shock API URL using binary data.

    Args:
        filename: Path to the file to upload
        upload_url: The upload URL from workspace API
        token: Authentication token for API calls
        timeout: Request timeout in seconds (default: 120.0)
    Returns:
        Dictionary with upload result status and message
    """
    try:
        # Check if file exists
        if not os.path.exists(filename):
            return {"success": False, "error": f"File {filename} does not exist"}

        # Read the file content
        with open(filename, 'rb') as file:
            file_content = file.read()

        # Set up headers for the Shock API request
        headers = {
            'Authorization': 'OAuth ' + token
        }

        # Prepare the file for multipart form data upload
        with open(filename, 'rb') as file:
            files = {
                'upload': (os.path.basename(filename), file, 'application/octet-stream')
            }

            # Make the POST request with multipart form data
            response = requests.put(upload_url, files=files, headers=headers, timeout=timeout)

        if response.status_code == 200:
            return {
                "success": True,
                "message": f"File {filename} uploaded successfully",
                "status_code": response.status_code
            }
        else:
            return {
                "success": False,
                "error": f"Upload failed with status code {response.status_code}: {response.text}",
                "status_code": response.status_code
            }

    except Exception as e:
        return {"success": False, "error": f"Upload failed: {str(e)}"}

# ──────────────────────────────────────────────────────────────────
# Group creation/retrieval functions have been moved to
# functions/group_functions.py (create_group, get_group_ids, etc.)
# ──────────────────────────────────────────────────────────────────

async def workspace_get_object(api: JsonRpcCaller, path: str, metadata_only: bool = False, token: str = None) -> dict:
    """
    Get an object from the workspace using the JSON-RPC API.

    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        path: Path to the object to retrieve
        metadata_only: If True, only return metadata without the actual data
        token: Authentication token for API calls
    Returns:
        Dictionary containing metadata and optionally data
    """
    if not path:
        return {
            "error": "Invalid Path(s) to retrieve",
            "errorType": "INVALID_PARAMETERS",
            "source": "bvbrc-workspace"
        }

    try:
        # Decode URL-encoded path
        path = requests.utils.unquote(path)

        # Call Workspace.get API
        result = await api.acall("Workspace.get", {
            "objects": [path],
            "metadata_only": metadata_only
        }, 1, token)

        # Validate response structure
        if not result or not result[0] or not result[0][0] or not result[0][0][0] or not result[0][0][0][4]:
            return {
                "error": "Object not found",
                "errorType": "NOT_FOUND",
                "source": "bvbrc-workspace"
            }

        # Extract metadata from nested array structure
        meta_array = result[0][0][0]
        metadata = {
            "name": meta_array[0],
            "type": meta_array[1],
            "path": meta_array[2],
            "creation_time": meta_array[3],
            "id": meta_array[4],
            "owner_id": meta_array[5],
            "size": meta_array[6],
            "userMeta": meta_array[7],
            "autoMeta": meta_array[8],
            "user_permissions": meta_array[9],
            "global_permission": meta_array[10],
            "link_reference": meta_array[11]
        }

        # If metadata only, return just the metadata
        if metadata_only:
            return {
                "metadata": metadata,
                "source": "bvbrc-workspace"
            }

        # Get the actual data
        data = result[0][0][1]

        return {
            "metadata": metadata,
            "data": data,
            "source": "bvbrc-workspace"
        }

    except Exception as e:
        if "Object not found" in str(e):
            return {
                "error": "Object not found",
                "errorType": "NOT_FOUND",
                "source": "bvbrc-workspace"
            }
        return {
            "error": f"Error getting workspace object: {str(e)}",
            "errorType": "API_ERROR",
            "source": "bvbrc-workspace"
        }

