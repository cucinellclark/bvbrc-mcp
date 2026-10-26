from __future__ import annotations

from typing import Any, Dict, Iterable

import httpx


DEFAULT_BASE_URL = "https://www.bv-brc.org/api-bulk"
DEFAULT_HEADERS = {
  "Accept": "application/json",
  "Content-Type": "application/rqlquery+x-www-form-urlencoded",
}


def create_context(overrides: Dict[str, Any] | None = None) -> Dict[str, Any]:
  overrides = overrides or {}
  base_url = overrides.get("base_url") or overrides.get("baseUrl") or DEFAULT_BASE_URL
  headers = dict(DEFAULT_HEADERS)
  headers.update(overrides.get("headers") or {})
  return {
    "base_url": base_url,
    "headers": headers,
  }


def _build_body(filter: str, options: Dict[str, Any]) -> str:
  from .query_builder import select as qb_select, sort as qb_sort, limit as qb_limit, http_download as qb_http_download

  select_fields: Iterable[str] | None = options.get("select")
  sort_expr: str | None = options.get("sort")
  limit_value: int | None = options.get("limit")
  http_download: bool = bool(options.get("http_download", False))

  if http_download and not sort_expr:
    raise ValueError("sort parameter is required when http_download is true")

  final_limit = limit_value if isinstance(limit_value, int) else 1000

  params: list[str] = []
  if filter:
    params.append(filter)
  if select_fields:
    params.append(qb_select(list(select_fields)))
  if sort_expr:
    params.append(qb_sort(sort_expr))
  if isinstance(final_limit, int):
    params.append(qb_limit(final_limit))
  if http_download:
    params.append(qb_http_download(True))

  return "&".join([p for p in params if p])

def run(core_name: str, filter: str, options: Dict[str, Any] | None, base_url: str | None, headers: Dict[str, str] | None):
  options = options or {}
  url = f"{(base_url or DEFAULT_BASE_URL).rstrip('/')}/{core_name}/"
  body = _build_body(filter, options)
  final_headers = headers or DEFAULT_HEADERS

  with httpx.Client() as client:
    response = client.post(url, content=body, headers=final_headers, timeout=60.0)
    response.raise_for_status()
    return response.json()


__all__ = [
  "create_context",
  "run",
]


