from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Tuple

import httpx


# Default Solr base URL; should point at the Solr root, not the generic API root
DEFAULT_SOLR_BASE_URL = "https://www.bv-brc.org/api-bulk/"
logger = logging.getLogger(__name__)
DEFAULT_SOLR_REQUEST_FORMAT = "form"

# Accept multiple aliases so callers can pass whichever naming style they use.
REQUEST_FORMAT_PARAM_KEYS = (
  "request_format",
  "requestFormat",
  "solr_request_format",
  "solrRequestFormat",
  "solr_format",
)


def create_solr_context(overrides: Dict[str, Any] | None = None) -> Dict[str, Any]:
  overrides = overrides or {}
  base_url = overrides.get("solr_base_url") or overrides.get("solrBaseUrl") or DEFAULT_SOLR_BASE_URL
  headers = dict(overrides.get("headers") or {})
  auth = overrides.get("auth")
  timeout = overrides.get("timeout", 60.0)
  request_format = _normalize_request_format(
    overrides.get("request_format")
    or overrides.get("requestFormat")
    or overrides.get("solr_request_format")
    or overrides.get("solrRequestFormat")
    or overrides.get("solr_format")
  )
  headers.setdefault("X-Solr-Request-Format", request_format)
  return {
    "solr_base_url": base_url.rstrip("/"),
    "headers": headers,
    "auth": auth,
    "timeout": timeout,
    "request_format": request_format,
  }


def _normalize_request_format(value: Any) -> str:
  normalized = str(value or "").strip().lower()
  if normalized in {"", "default", "auto"}:
    return DEFAULT_SOLR_REQUEST_FORMAT
  if normalized in {"form", "urlencoded", "form-urlencoded", "x-www-form-urlencoded", "legacy"}:
    return "form"
  if normalized in {"json", "solr-json", "solr_json"}:
    return "json"
  raise ValueError(
    f"Invalid Solr request format '{value}'. Supported values: form, json."
  )


def _extract_param_request_format(params: Dict[str, Any]) -> Any:
  for key in REQUEST_FORMAT_PARAM_KEYS:
    if key in params:
      return params.pop(key)
  return None


def resolve_request_format(
  explicit_request_format: Any = None,
  params: Optional[Dict[str, Any]] = None,
  headers: Optional[Dict[str, str]] = None,
) -> str:
  """Resolve request format from explicit arg, params aliases, then header override."""
  if explicit_request_format is not None:
    return _normalize_request_format(explicit_request_format)

  mutable_params = params if params is not None else {}
  param_value = _extract_param_request_format(mutable_params)
  if param_value is not None:
    return _normalize_request_format(param_value)

  header_value = None
  if headers:
    header_value = headers.get("X-Solr-Request-Format")
  return _normalize_request_format(header_value)


def _prepare_request(
  collection: str,
  params: Dict[str, Any],
  base_url: Optional[str],
  headers: Optional[Dict[str, str]],
  request_format: Optional[str] = None,
) -> Tuple[str, Dict[str, Any], Dict[str, str], bool]:
  # Solr select endpoint
  # Direct collection access like the working curl example
  solr_base = (base_url or DEFAULT_SOLR_BASE_URL).rstrip("/")
  url = f"{solr_base}/{collection}/"
  req_params = dict(params or {})
  final_headers = dict(headers or {})

  resolved_format = resolve_request_format(request_format, req_params, final_headers)

  # Ensure JSON response like legacy clients did (wt=json)
  if "wt" not in req_params:
    req_params["wt"] = "json"

  # Add BV-BRC specific headers for Solr queries.
  final_headers["Accept"] = "application/solr+json"
  if resolved_format == "json":
    final_headers["Content-Type"] = "application/json"
    return url, {"params": req_params}, final_headers, True

  final_headers["Content-Type"] = "application/solrquery+x-www-form-urlencoded"
  return url, req_params, final_headers, False


def select(
  collection: str,
  params: Dict[str, Any],
  base_url: Optional[str] = None,
  headers: Optional[Dict[str, str]] = None,
  auth: Any = None,
  timeout: float = 60.0,
  request_format: Optional[str] = None,
) -> Dict[str, Any]:
  """Synchronous Solr select helper kept for backward compatibility."""
  url, req_payload, final_headers, send_json = _prepare_request(collection, params, base_url, headers, request_format)
  logger.info("Executing Solr query: collection=%s url=%s payload=%s", collection, url, req_payload)

  with httpx.Client() as client:
    response = client.post(
      url,
      json=req_payload if send_json else None,
      data=None if send_json else req_payload,
      headers=final_headers,
      auth=auth,
      timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


async def async_select(
  collection: str,
  params: Dict[str, Any],
  *,
  client: Optional[httpx.AsyncClient] = None,
  base_url: Optional[str] = None,
  headers: Optional[Dict[str, str]] = None,
  auth: Any = None,
  timeout: float = 60.0,
  request_format: Optional[str] = None,
) -> Dict[str, Any]:
  """Async Solr select helper supporting optional shared AsyncClient."""
  url, req_payload, final_headers, send_json = _prepare_request(collection, params, base_url, headers, request_format)
  logger.info("Executing Solr query: collection=%s url=%s payload=%s", collection, url, req_payload)

  if client is not None:
    response = await client.post(
      url,
      json=req_payload if send_json else None,
      data=None if send_json else req_payload,
      headers=final_headers,
      auth=auth,
      timeout=timeout,
    )
    response.raise_for_status()
    return response.json()

  async with httpx.AsyncClient() as local_client:
    response = await local_client.post(
      url,
      json=req_payload if send_json else None,
      data=None if send_json else req_payload,
      headers=final_headers,
      auth=auth,
      timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


__all__ = [
  "create_solr_context",
  "resolve_request_format",
  "async_select",
  "select",
]


