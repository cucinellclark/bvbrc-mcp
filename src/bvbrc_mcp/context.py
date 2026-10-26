"""ToolContext: what a tool call needs to know besides its arguments.

Every tool function takes ``config`` (a ToolContext, or any object with the
same attributes) and ``headers`` (``{"Authorization": <token>}``). The
attribute names are the ones the tools have always read, so the
bvbrc-agents harness can pass its own agent config unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ToolContext:
    # The caller's BV-BRC token, raw (no "OAuth " prefix).
    bvbrc_auth_token: Optional[str] = None

    # Services
    bvbrc_api_url: str = "https://www.bv-brc.org/api-bulk"
    bvbrc_workspace_url: str = "https://p3.theseed.org/services/Workspace"
    # The GoWe workflow engine: required by the GoWe tools (list, inputs,
    # submit, rerun, batch); there is no public default.
    gowe_url: Optional[str] = None
    similar_genome_finder_url: str = "https://p3.theseed.org/services/minhash_service"
    literature_rag_url: str = "https://www.bv-brc.org/ragstack/asm-next/api"
    literature_rag_timeout_seconds: int = 45
    literature_rag_collections: List[str] = field(default_factory=lambda: ["asm-tok256", "open-access"])
    # Helpdesk search (RAGStack): ragstack_base_url, ragstack_collection,
    # ragstack_retrieval_mode, ragstack_rerank, ragstack_timeout_seconds.
    helpdesk_config: Dict[str, Any] = field(default_factory=dict)
    # SRA metadata lookups run sra-tools from this container when present.
    singularity_container_path: Optional[str] = None

    tool_timeout_seconds: float = 30.0

    # Optional: put submitted jobs' outputs under
    # <workspace_path>/chats/<session_id>/ and label GoWe submissions with the
    # session. Unset for a plain MCP call.
    session_id: Optional[str] = None
    workspace_path: Optional[str] = None

    def auth_headers(self) -> Optional[Dict[str, str]]:
        return {"Authorization": self.bvbrc_auth_token} if self.bvbrc_auth_token else None
