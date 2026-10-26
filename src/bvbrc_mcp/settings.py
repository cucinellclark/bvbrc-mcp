"""Settings for the MCP servers and for tool calls made through them.

Read once, in this order (later wins):

1. Defaults: public BV-BRC endpoints; no GoWe.
2. The JSON file named by ``BVBRC_MCP_CONFIG`` (see ``config.example.json``).
3. Environment variables ``BVBRC_MCP_<NAME>`` for the flat keys below, e.g.
   ``BVBRC_MCP_GOWE_URL``, ``BVBRC_MCP_PORT``, ``BVBRC_MCP_PUBLIC_URL``.

A library caller that builds its own ``ToolContext`` never needs this module.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, fields
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from bvbrc_mcp.context import ToolContext


@dataclass
class Settings:
    # Services (ToolContext fields)
    api_url: str = "https://www.bv-brc.org/api-bulk"
    workspace_url: str = "https://p3.theseed.org/services/Workspace"
    app_service_url: str = "https://p3.theseed.org/services/app_service"
    gowe_url: Optional[str] = None
    minhash_url: str = "https://p3.theseed.org/services/minhash_service"
    literature_url: str = "https://www.bv-brc.org/ragstack/asm-next/api"
    literature_collections: List[str] = field(default_factory=lambda: ["asm-tok256", "open-access"])
    helpdesk: Dict[str, Any] = field(default_factory=lambda: {
        "ragstack_base_url": "https://www.bv-brc.org/ragstack/clark/api",
        "ragstack_collection": "bvbrc_helpdesk",
        "ragstack_retrieval_mode": "vector",
        "ragstack_rerank": False,
        "ragstack_timeout_seconds": 45,
    })
    sra_container_path: Optional[str] = None
    tool_timeout_seconds: float = 30.0

    # HTTP server
    host: str = "127.0.0.1"
    port: int = 12010
    # The public URL clients connect to, e.g. https://www.bv-brc.org/mcp.
    # Every OAuth address the server advertises is built from it.
    public_url: str = "http://127.0.0.1:12010"
    # Path the MCP endpoint is served at on this process ("/" behind a
    # prefix-stripping proxy; see DEPLOYMENT.md).
    mcp_path: str = "/"
    authentication_url: str = "https://user.patricbrc.org/authenticate"
    oauth: Dict[str, Any] = field(default_factory=dict)
    # Signs the access tokens issued to clients. Unset = a random key per
    # start, which signs every client out on restart.
    jwt_signing_key: Optional[str] = None
    # Largest tool result returned to a client, in characters.
    max_result_chars: int = 60_000

    def tool_context(self, token: Optional[str]) -> ToolContext:
        return ToolContext(
            bvbrc_auth_token=token,
            bvbrc_api_url=self.api_url,
            bvbrc_workspace_url=self.workspace_url,
            gowe_url=self.gowe_url,
            similar_genome_finder_url=self.minhash_url,
            literature_rag_url=self.literature_url,
            literature_rag_collections=list(self.literature_collections),
            helpdesk_config=dict(self.helpdesk),
            singularity_container_path=self.sra_container_path,
            tool_timeout_seconds=self.tool_timeout_seconds,
        )


_FLAT_TYPES = {"str", "int", "float", "Optional[str]"}


def _from_env(values: Dict[str, Any]) -> None:
    for f in fields(Settings):
        raw = os.environ.get(f"BVBRC_MCP_{f.name.upper()}")
        if raw is None:
            continue
        if f.type == "int":
            values[f.name] = int(raw)
        elif f.type == "float":
            values[f.name] = float(raw)
        elif f.type in _FLAT_TYPES:
            values[f.name] = raw
        else:
            values[f.name] = json.loads(raw)
    # The name the server used before the package existed.
    if "jwt_signing_key" not in values and os.environ.get("MCP_JWT_SIGNING_KEY"):
        values["jwt_signing_key"] = os.environ["MCP_JWT_SIGNING_KEY"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    values: Dict[str, Any] = {}
    path = os.environ.get("BVBRC_MCP_CONFIG")
    if path:
        data = json.loads(Path(path).expanduser().read_text())
        known = {f.name for f in fields(Settings)}
        unknown = sorted(set(data) - known)
        if unknown:
            raise ValueError(f"{path}: unknown settings {unknown}")
        values.update(data)
    _from_env(values)
    defaults = Settings()
    if "helpdesk" in values:
        values["helpdesk"] = {**defaults.helpdesk, **values["helpdesk"]}
    return Settings(**values)
