"""Helpdesk search: BV-BRC documentation passages from a RAGStack collection.

The legacy helpdesk RAG API (port 8001) was retired on 2026-10-26; RAGStack is
the only backend.
"""

from typing import Dict, Any, Optional, List
import re
import requests


#: Docs site the helpdesk corpus is scraped from (BV-BRC-Docs ``docroot``).
BVBRC_DOCS_BASE_URL = "https://www.bv-brc.org/docs"

#: The website itself, for corpus pages that are not docs (the outbreak pages).
BVBRC_SITE_URL = "https://www.bv-brc.org"

#: Argonne's Cloudflare in front of www.bv-brc.org answers 403 to some default
#: client user agents (``Python-urllib``), so name ourselves.
_USER_AGENT = "bvbrc-copilot-helpdesk/1.0"


def _ragstack_doc_path(filename: Optional[str]) -> Optional[str]:
    """Map an uploaded RAGStack filename back to its docs path.

    The helpdesk corpus is uploaded one file per doc, named from the doc's path
    under BV-BRC-Docs ``docroot`` with ``/`` -> ``__`` and the extension -> ``.md``
    (``quick_references__services__blast.md`` -> ``quick_references/services/blast``).
    """
    if not filename:
        return None
    stem = filename[:-3] if filename.endswith(".md") else filename
    return stem.replace("__", "/")


def _ragstack_doc_url(doc_path: Optional[str]) -> Optional[str]:
    """The public page for a corpus doc path.

    Docs pages live under ``/docs/<path>.html``.  The outbreak pages
    (``outbreaks/<Name>/<tab>``, uploaded from
    ``Agents/scripts/helpdesk_extra_docs``) are website pages,
    ``/outbreaks/<Name>/#view_tab=<tab>``; their index has no page of its
    own; a long page uploaded in parts is ``<tab>-p<n>`` (``-3`` from one
    superseded split).  Before 2026-10-20 every path got a ``/docs/`` link.
    """
    if not doc_path:
        return None
    parts = doc_path.split("/")
    if parts[0] == "outbreaks":
        if len(parts) == 3:
            tab = re.sub(r"-p?\d+$", "", parts[2])
            return f"{BVBRC_SITE_URL}/outbreaks/{parts[1]}/#view_tab={tab}"
        return None
    return f"{BVBRC_DOCS_BASE_URL}/{doc_path}.html"


def _query_ragstack(
    query: str, top_k: Optional[int], config: dict, auth_token: Optional[str]
) -> List[Dict[str, Any]]:
    """Retrieve helpdesk passages from a RAGStack collection (``POST /v1/retrieve``).

    ``retrieval_mode`` and ``rerank`` default to ``vector`` / off: on the helpdesk
    question set the deployment's cross-encoder reranker lowered hit@1 from 1.00
    to 0.80 (Agents/current_plans/ragstack_helpdesk_reingest.md, step 4).
    """
    if not auth_token:
        raise PermissionError(
            "RAGStack helpdesk search needs the caller's BV-BRC token, and none was provided"
        )
    base_url = config.get("ragstack_base_url", "https://www.bv-brc.org/ragstack/clark/api")
    token = auth_token.strip()
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    payload: Dict[str, Any] = {
        "query": query,
        "collection": config.get("ragstack_collection", "bvbrc_helpdesk"),
        "top_k": top_k or 5,
        "retrieval_mode": config.get("ragstack_retrieval_mode", "vector"),
        "rerank": config.get("ragstack_rerank", False),
    }
    response = requests.post(
        f"{base_url.rstrip('/')}/v1/retrieve",
        json=payload,
        headers={"Authorization": token, "User-Agent": _USER_AGENT},
        timeout=config.get("ragstack_timeout_seconds", 45),
    )
    response.raise_for_status()

    results = []
    for src in response.json().get("sources", []):
        md = src.get("metadata") or {}
        doc_path = _ragstack_doc_path(md.get("filename"))
        results.append(
            {
                "content": src.get("content", ""),
                "score": src.get("score", 0.0),
                "metadata": {
                    "doc_path": doc_path,
                    "docs_url": _ragstack_doc_url(doc_path),
                    "chunk_index": md.get("chunk_index"),
                },
            }
        )
    return results


def query_rag_helpdesk_func(
    query: str,
    top_k: Optional[int] = 5,
    config: Optional[dict] = None,
    auth_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve helpdesk passages for *query* (raw documents, no summary).

    Args:
        query: The question, typically how to do something on BV-BRC.
        top_k: Number of passages to return.
        config: RAGStack settings: ``ragstack_base_url``, ``ragstack_collection``,
            ``ragstack_retrieval_mode``, ``ragstack_rerank``, ``ragstack_timeout_seconds``.
        auth_token: The caller's BV-BRC token; RAGStack searches as the user.

    Returns:
        ``{results, count, query, index, source}``; each result carries
        ``metadata.doc_path`` and ``metadata.docs_url``. On failure the same
        shape with ``error`` and ``errorType``.
    """
    config = config or {}
    database_name = config.get("ragstack_collection", "bvbrc_helpdesk")
    source = "bvbrc-ragstack"
    try:
        results = _query_ragstack(query, top_k, config, auth_token)
        return {
            "results": results,
            "count": len(results),
            "query": query,
            "index": database_name,
            "source": source,
        }
    except requests.RequestException as e:
        error, error_type = f"Helpdesk search request failed: {e}", "RAG_API_REQUEST_ERROR"
    except Exception as e:
        error, error_type = str(e), "API_ERROR"
    return {
        "results": [],
        "count": 0,
        "query": query,
        "index": database_name,
        "error": error,
        "errorType": error_type,
        "source": source,
    }
