"""Helpdesk tools: search the BV-BRC documentation, list services, read a
service's parameter schema.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional


def _helpdesk_config(config: Any) -> Dict[str, Any]:
    """RAGStack settings: from the context, else this server's settings."""
    cfg = getattr(config, "helpdesk_config", None)
    if cfg:
        return dict(cfg)
    from bvbrc_mcp.settings import get_settings

    return dict(get_settings().helpdesk)


async def query_helpdesk(
    query: str,
    top_k: int = 5,
    config: Optional[Any] = None,
    **kwargs,
) -> Dict[str, Any]:
    """Search the BV-BRC helpdesk knowledge base (raw passages, no summary).

    Returns ``{results: [{content, score, metadata: {doc_path, docs_url}}],
    count, query, index}``.
    """
    from bvbrc_mcp.clients import rag_database_functions as rag

    # RAGStack searches as the user; the call is blocking (requests).
    return await asyncio.to_thread(
        rag.query_rag_helpdesk_func,
        query=query,
        top_k=top_k,
        config=_helpdesk_config(config),
        auth_token=getattr(config, "bvbrc_auth_token", None),
    )


async def list_services(config: Optional[Any] = None, **kwargs) -> Dict[str, Any]:
    """List all available BV-BRC services with descriptions."""
    from bvbrc_mcp.clients import service_validation_functions as vf

    return vf.list_services_fn()


async def get_service_schema(
    service_name: str,
    config: Optional[Any] = None,
    **kwargs,
) -> Dict[str, Any]:
    """Get the full parameter schema for a specific service."""
    from bvbrc_mcp.clients import service_validation_functions as vf

    return vf.get_service_schema_fn(service_name)
