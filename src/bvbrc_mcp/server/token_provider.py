"""Which BV-BRC token a tool call runs as.

HTTP: the request's ``Authorization`` bearer token (an access token this
server issued, mapped back to the user's BV-BRC token by the OAuth provider),
else a ``bvbrc_token`` argument. stdio: a ``bvbrc_token`` argument, else the
``KB_AUTH_TOKEN`` environment variable.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Optional

try:
    from fastmcp.server.dependencies import get_http_headers
except ImportError:  # pragma: no cover
    def get_http_headers():
        return {}


class TokenProvider:
    def __init__(self, mode: str = "stdio", oauth_provider: Any = None):
        if mode not in ("stdio", "http"):
            raise ValueError(f"mode must be 'stdio' or 'http', not {mode!r}")
        self.mode = mode
        self._oauth_provider = oauth_provider

    def _resolve(self, token: Optional[str]) -> Optional[str]:
        """Map an MCP bearer token to the BV-BRC token used by BV-BRC APIs."""
        if not token:
            return token
        resolver = getattr(self._oauth_provider, "resolve_patric_token", None)
        if resolver:
            resolved = resolver(token)
            if resolved:
                return resolved
        return token

    def get_token(self, provided_token: Optional[str] = None) -> Optional[str]:
        if self.mode == "http":
            header_token = self._token_from_request_headers()
            if header_token:
                return self._resolve(header_token)
        if provided_token:
            return self._resolve(provided_token)
        if self.mode == "stdio":
            return os.getenv("KB_AUTH_TOKEN") or None
        return None

    def _token_from_request_headers(self) -> Optional[str]:
        try:
            headers = get_http_headers()
        except Exception as e:  # pragma: no cover
            print(f"Warning: could not read HTTP headers: {e}", file=sys.stderr)
            return None
        auth = (headers.get("authorization") or headers.get("Authorization") or "").strip()
        if not auth:
            return None
        return auth[7:].strip() if auth.lower().startswith("bearer ") else auth
