"""query_helpdesk searches RAGStack (the only backend since 2026-10-26).

No network: ``requests.post`` is patched.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


from bvbrc_mcp.clients import rag_database_functions as rdf  # noqa: E402

RAGSTACK_CFG = {
    "ragstack_base_url": "https://example.org/ragstack/clark/api/",
    "ragstack_collection": "bvbrc_helpdesk",
}


def _response(payload: dict) -> MagicMock:
    resp = MagicMock()
    resp.json.return_value = payload
    resp.raise_for_status.return_value = None
    return resp


RAGSTACK_HIT = {
    "sources": [
        {
            "content": "Use the Genome Assembly service...",
            "score": 0.93,
            "metadata": {"filename": "quick_references__services__genome_assembly_service.md",
                         "chunk_index": 2, "tenant_id": "bvbrc:someone"},
        }
    ]
}


def test_ragstack_request_shape():
    with patch.object(rdf.requests, "post", return_value=_response(RAGSTACK_HIT)) as post:
        rdf.query_rag_helpdesk_func("assemble reads", top_k=3, config=RAGSTACK_CFG, auth_token="un=u|tokenid=x")
    url = post.call_args.args[0]
    kwargs = post.call_args.kwargs
    assert url == "https://example.org/ragstack/clark/api/v1/retrieve"
    # Defaults chosen in step 4: vector retrieval, reranker off.
    assert kwargs["json"] == {"query": "assemble reads", "collection": "bvbrc_helpdesk",
                              "top_k": 3, "retrieval_mode": "vector", "rerank": False}
    assert kwargs["headers"]["Authorization"] == "Bearer un=u|tokenid=x"
    # Cloudflare 403s the default Python-urllib agent; we always name ourselves.
    assert kwargs["headers"]["User-Agent"].startswith("bvbrc-copilot-helpdesk")


def test_existing_bearer_prefix_not_doubled():
    with patch.object(rdf.requests, "post", return_value=_response({"sources": []})) as post:
        rdf.query_rag_helpdesk_func("q", config=RAGSTACK_CFG,
                                    auth_token="Bearer abc")
    assert post.call_args.kwargs["headers"]["Authorization"] == "Bearer abc"


def test_ragstack_results_carry_doc_path_and_url():
    with patch.object(rdf.requests, "post", return_value=_response(RAGSTACK_HIT)):
        out = rdf.query_rag_helpdesk_func("q", config=RAGSTACK_CFG, auth_token="t")
    assert out["count"] == 1
    assert out["source"] == "bvbrc-ragstack"
    assert out["index"] == "bvbrc_helpdesk"
    md = out["results"][0]["metadata"]
    assert md["doc_path"] == "quick_references/services/genome_assembly_service"
    assert md["docs_url"] == ("https://www.bv-brc.org/docs/quick_references/services/"
                              "genome_assembly_service.html")
    assert "tenant_id" not in md  # internal RAGStack fields are not passed to the LLM


def test_ragstack_without_token_is_an_error_not_a_request():
    with patch.object(rdf.requests, "post") as post:
        out = rdf.query_rag_helpdesk_func("q", config=RAGSTACK_CFG, auth_token=None)
    post.assert_not_called()
    assert out["count"] == 0
    assert out["errorType"] == "API_ERROR"
    assert "token" in out["error"]


def test_ragstack_http_error_shape():
    resp = MagicMock()
    resp.raise_for_status.side_effect = rdf.requests.HTTPError("403 Forbidden")
    with patch.object(rdf.requests, "post", return_value=resp):
        out = rdf.query_rag_helpdesk_func("q", config=RAGSTACK_CFG, auth_token="t")
    assert out["errorType"] == "RAG_API_REQUEST_ERROR"
    assert out["results"] == []




def test_outbreak_pages_link_to_the_website_not_docs():
    assert rdf._ragstack_doc_url("outbreaks/Measles/resources") == (
        "https://www.bv-brc.org/outbreaks/Measles/#view_tab=resources")
    assert rdf._ragstack_doc_url(rdf._ragstack_doc_path("outbreaks__H5N1__clt.md")) == (
        "https://www.bv-brc.org/outbreaks/H5N1/#view_tab=clt")
    assert rdf._ragstack_doc_url("outbreaks/SARSCoV2/overview-p3") == (
        "https://www.bv-brc.org/outbreaks/SARSCoV2/#view_tab=overview")
    assert rdf._ragstack_doc_url("outbreaks/SARSCoV2/overview-3") == (
        "https://www.bv-brc.org/outbreaks/SARSCoV2/#view_tab=overview")
    assert rdf._ragstack_doc_url("outbreaks/index") is None
    assert rdf._ragstack_doc_url("about") == "https://www.bv-brc.org/docs/about.html"
    assert rdf._ragstack_doc_url(None) is None


def test_doc_path_mapping():
    assert rdf._ragstack_doc_path("about.md") == "about"
    assert rdf._ragstack_doc_path("cli_tutorial__cli_installation.md") == "cli_tutorial/cli_installation"
    assert rdf._ragstack_doc_path(None) is None




async def test_query_helpdesk_searches_as_the_user_with_its_settings():
    """The tool passes the caller's token and the context's RAGStack settings."""
    from bvbrc_mcp import ToolContext
    from bvbrc_mcp.tools import helpdesk

    ctx = ToolContext(bvbrc_auth_token="un=u|tokenid=x", helpdesk_config={"ragstack_collection": "c"})
    with patch.object(rdf, "query_rag_helpdesk_func", return_value={"results": [], "count": 0}) as q:
        await helpdesk.query_helpdesk("q", top_k=5, config=ctx)
    assert q.call_args.kwargs == {"query": "q", "top_k": 5, "config": {"ragstack_collection": "c"},
                                  "auth_token": "un=u|tokenid=x"}


async def test_query_helpdesk_falls_back_to_server_settings():
    """A config without helpdesk_config (the harness's agent config) uses Settings.helpdesk."""
    from types import SimpleNamespace

    from bvbrc_mcp.settings import get_settings
    from bvbrc_mcp.tools import helpdesk

    with patch.object(rdf, "query_rag_helpdesk_func", return_value={"results": [], "count": 0}) as q:
        await helpdesk.query_helpdesk("q", config=SimpleNamespace(bvbrc_auth_token="t"))
    assert q.call_args.kwargs["config"] == get_settings().helpdesk
    assert q.call_args.kwargs["config"]["ragstack_collection"] == "bvbrc_helpdesk"
