"""Turn a tool result into JSON text of bounded size.

``truncate_result`` keeps the whole result when it fits; otherwise it samples
list items representatively (by type and folder), adds an aggregate summary,
keeps facet bucket counts and whole catalogs, and binary-searches the largest
sample that fits. Used by the MCP servers (``Settings.max_result_chars``) and
by LLM harnesses with smaller caps.
"""

from __future__ import annotations

import json
import math
import os
from collections import Counter, defaultdict
from typing import Any, Dict, Optional

# ---------------------------------------------------------------------------
# Smart truncation with representative sampling
# ---------------------------------------------------------------------------


def _build_items_summary(items: list) -> Dict[str, Any]:
    """Build an aggregate summary of items for the LLM.

    Returns counts by type, folder distribution, size stats, date range, etc.
    so the LLM can answer aggregation questions even when items are truncated.
    """
    type_counts: Counter = Counter()
    folder_counts: Counter = Counter()
    total_size = 0
    dates: list[str] = []

    for item in items:
        if isinstance(item, dict):
            item_type = item.get("type", "unknown")
            item_path = item.get("path", "")
            item_size = item.get("size", 0)
            item_date = item.get("creation_time", "")
        elif isinstance(item, list) and len(item) >= 4:
            item_type = item[1] if len(item) > 1 else "unknown"
            item_path = item[2] if len(item) > 2 else ""
            item_size = item[6] if len(item) > 6 else 0
            item_date = item[3] if len(item) > 3 else ""
        else:
            continue

        type_counts[item_type] += 1

        parent = os.path.dirname(item_path.rstrip("/")) if item_path else ""
        if parent:
            folder_counts[parent] += 1

        if isinstance(item_size, (int, float)):
            total_size += item_size
        if item_date:
            dates.append(str(item_date))

    summary: Dict[str, Any] = {
        "total_items": len(items),
        "counts_by_type": dict(type_counts.most_common()),
        "unique_types": sorted(type_counts.keys()),
    }

    if folder_counts:
        summary["top_folders"] = dict(folder_counts.most_common(10))
    if total_size > 0:
        summary["total_size_bytes"] = total_size
    if dates:
        sorted_dates = sorted(dates)
        summary["date_range"] = {
            "earliest": sorted_dates[0],
            "latest": sorted_dates[-1],
        }

    return summary


def _slim_item(item: Any) -> Any:
    """Strip verbose metadata fields from a workspace item dict."""
    if not isinstance(item, dict):
        return item
    drop_keys = {
        "userMeta",
        "autoMeta",
        "link_reference",
        "user_permissions",
        "global_permission",
    }
    return {k: v for k, v in item.items() if k not in drop_keys}


def _sample_representative(items: list, budget: int) -> list:
    """Pick a representative sample of items, ensuring each type is included."""
    if len(items) <= budget:
        return [_slim_item(i) for i in items]

    by_type: dict[str, list] = defaultdict(list)
    for item in items:
        if isinstance(item, dict):
            t = item.get("type", "unknown")
        elif isinstance(item, list) and len(item) > 1:
            t = item[1]
        else:
            t = "unknown"
        by_type[t].append(item)

    sampled: list = []
    remaining_budget = budget

    # Phase 1: one item per type
    for t, group in by_type.items():
        if remaining_budget <= 0:
            break
        sampled.append(_slim_item(group[0]))
        remaining_budget -= 1

    # Phase 2: fill proportionally from each type
    if remaining_budget > 0:
        for t, group in by_type.items():
            share = max(0, math.floor((len(group) / len(items)) * remaining_budget))
            for item in group[1 : 1 + share]:
                sampled.append(_slim_item(item))

    # Fill remaining budget
    if len(sampled) < budget:
        seen = {id(s) for s in sampled}
        for item in items:
            if len(sampled) >= budget:
                break
            if id(item) not in seen:
                sampled.append(_slim_item(item))
                seen.add(id(item))

    return sampled[:budget]


def truncate_result(result: Dict[str, Any], max_chars: int = 8000) -> str:
    """Serialize a tool result to JSON, truncating if too large.

    Smart truncation strategy:
      1. Catalog lists (``workflows``) are never sampled -- every entry is
         kept and descriptions are shortened instead, so the LLM always
         sees the full set of available workflows.
      2. Adds aggregate summary (type counts, folder distribution, etc.).
      3. Samples items representatively across types (not just first N).
      4. Strips verbose metadata from sampled items.
      5. Uses binary search to find the largest sample that fits.
      6. Falls back to hard truncation if nothing else works.

    Args:
        result: The tool result dict.
        max_chars: Maximum characters for the serialized output.

    Returns:
        JSON string of the result, possibly truncated.
    """
    serialized = json.dumps(result, indent=2, default=str)

    if len(serialized) <= max_chars:
        return serialized

    # Catalog lists must stay complete: dropping entries hides options from
    # the LLM (e.g. the BLAST workflow silently vanishing from discovery).
    catalog = _fit_catalog(result, "workflows", "description", max_chars)
    if catalog is not None:
        return catalog

    # Facet results: sample the bucket lists but always keep the per-field
    # bucket / distinct counts.  Hard-cutting the JSON mid-bucket left the
    # LLM with no total and thousands of ids to "count" (see the
    # penicillin-resistant S. pneumoniae 5-minute timeout).
    faceted = _fit_facets(result, max_chars)
    if faceted is not None:
        return faceted

    # Find the list-valued key to truncate (check nested "result" envelope too)
    for list_key in ("items", "results", "records", "files", "ids"):
        target = result
        if "result" in result and isinstance(result["result"], dict):
            target = result["result"]

        if list_key in target and isinstance(target[list_key], list):
            all_items = target[list_key]
            num_items = len(all_items)
            summary = _build_items_summary(all_items)

            truncated = dict(result)
            if "result" in truncated and isinstance(truncated["result"], dict):
                truncated["result"] = dict(truncated["result"])
                inner = truncated["result"]
            else:
                inner = truncated

            inner["_summary"] = summary

            # Binary search for the largest representative sample that fits
            lo, hi = 1, num_items
            best_n = 1
            while lo <= hi:
                mid = (lo + hi) // 2
                inner[list_key] = _sample_representative(all_items, mid)
                inner["_truncated"] = {
                    "total": num_items,
                    "shown": mid,
                    "note": (
                        f"Showing {mid} of {num_items} items "
                        f"(representative sample across types)."
                    ),
                }
                candidate = json.dumps(truncated, indent=2, default=str)
                if len(candidate) <= max_chars:
                    best_n = mid
                    serialized = candidate
                    lo = mid + 1
                else:
                    hi = mid - 1

            inner[list_key] = _sample_representative(all_items, best_n)
            inner["_truncated"] = {
                "total": num_items,
                "shown": best_n,
                "note": (
                    f"Showing {best_n} of {num_items} items "
                    f"(representative sample across types)."
                ),
            }
            return json.dumps(truncated, indent=2, default=str)

    # Fallback: hard truncate
    return serialized[:max_chars] + f"\n... [TRUNCATED at {max_chars} chars]"


def _fit_facets(result: Dict[str, Any], max_chars: int) -> Optional[str]:
    """Serialize a ``facet_query`` result within *max_chars*.

    Keeps ``numFound``, ``bucket_counts`` / ``distinct_counts`` and every
    other scalar key intact, then binary-searches the number of buckets
    kept per field.  Returns ``None`` when *result* has no ``facets`` dict.
    """
    facets = result.get("facets")
    if not isinstance(facets, dict) or not facets:
        return None
    lists = {f: v for f, v in facets.items() if isinstance(v, list)}
    if not lists:
        return None

    total = {f: len(v) for f, v in lists.items()}
    max_len = max(total.values())

    def render(n: int) -> str:
        trimmed = dict(result)
        trimmed["facets"] = {
            f: (v[:n] if isinstance(v, list) else v) for f, v in facets.items()
        }
        trimmed.setdefault("bucket_counts", total)
        trimmed["_truncated"] = {
            "buckets_total": total,
            "buckets_shown": {f: min(n, len(v)) for f, v in lists.items()},
            "note": (
                f"Showing the top {n} buckets per field. bucket_counts / "
                "distinct_counts give the full number of distinct values — "
                "do not count the buckets."
            ),
        }
        return json.dumps(trimmed, indent=2, default=str)

    lo, hi, best = 0, max_len, None
    while lo <= hi:
        mid = (lo + hi) // 2
        candidate = render(mid)
        if len(candidate) <= max_chars:
            best = candidate
            lo = mid + 1
        else:
            hi = mid - 1
    # Even zero buckets did not fit (huge scalar payload) — let the generic
    # fallback handle it.
    return best


def _fit_catalog(
    result: Dict[str, Any],
    list_key: str,
    text_key: str,
    max_chars: int,
) -> Optional[str]:
    """Serialize ``result`` keeping every entry of ``result[list_key]``.

    Tries compact (no-indent) JSON first, then shrinks the ``text_key``
    field of each entry (binary search on its length) until the JSON fits
    ``max_chars``.  Returns ``None`` when ``list_key`` is absent or the
    entries cannot fit even with the text removed.
    """
    entries = result.get(list_key)
    if not isinstance(entries, list) or not entries:
        return None

    longest = max(
        (len(e.get(text_key, "")) for e in entries if isinstance(e, dict)),
        default=0,
    )

    def shrink_entry(e: Any, cap: int) -> Any:
        if not isinstance(e, dict) or not isinstance(e.get(text_key), str):
            return e
        if cap <= 0:
            return {k: v for k, v in e.items() if k != text_key}
        text = e[text_key]
        return {**e, text_key: text[:cap].rstrip() + ("..." if len(text) > cap else "")}

    def render(cap: int, indent: Optional[int] = 2) -> str:
        shrunk = dict(result)
        shrunk[list_key] = [shrink_entry(e, cap) for e in entries]
        if cap < longest:
            shrunk["_truncated"] = {
                "total": len(entries),
                "shown": len(entries),
                "note": (
                    f"All {len(entries)} entries kept; {text_key} fields "
                    + (f"shortened to {cap} chars to fit." if cap > 0
                       else "omitted to fit.")
                ),
            }
        return json.dumps(shrunk, indent=indent, default=str)

    # Indentation is the cheapest thing to give up -- keep full text if
    # compact JSON fits.
    compact = render(longest, indent=None)
    if len(compact) <= max_chars:
        return compact

    # Binary search for the longest text cap that fits (compact JSON).
    lo, hi = 0, longest
    best: Optional[str] = None
    while lo <= hi:
        mid = (lo + hi) // 2
        candidate = render(mid, indent=None)
        if len(candidate) <= max_chars:
            best = candidate
            lo = mid + 1
        else:
            hi = mid - 1
    return best


# ---------------------------------------------------------------------------
# Result shapes callers check for
# ---------------------------------------------------------------------------


def is_invalid_arguments_result(result: Any) -> bool:
    """True when the call was refused because its arguments were not JSON.

    The tool never ran and nothing changed; a caller counting failures should
    skip it.
    """
    return isinstance(result, dict) and bool(result.get("invalid_arguments"))


def is_needs_user_input_result(result: Any) -> bool:
    """True when submit_gowe_job stopped before submitting to ask the user something."""
    return isinstance(result, dict) and bool(result.get("needs_user_input"))


def is_already_submitted_result(result: Any) -> bool:
    """True when submit_gowe_job refused a repeat of a recent submission."""
    return isinstance(result, dict) and bool(result.get("already_submitted"))
