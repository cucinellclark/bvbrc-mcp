from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class StructuredAssertion:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, id: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("id", id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_comment(self, comment: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("comment", comment), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_evidence_code(self, evidence_code: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("evidence_code", evidence_code), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_feature_id(self, feature_id: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("feature_id", feature_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_owner(self, owner: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("owner", owner), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_patric_id(self, patric_id: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("patric_id", patric_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pmid(self, pmid: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("pmid", pmid), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_property(self, property: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("property", property), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_public_status(self, is_public: bool, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("public", is_public), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_refseq_locus_tag(self, refseq_locus_tag: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("refseq_locus_tag", refseq_locus_tag), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_score(self, score: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("score", score), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_source(self, source: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("source", source), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_value(self, value: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("value", value), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_user_read(self, user_read: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("user_read", user_read), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_user_write(self, user_write: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("user_write", user_write), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_version(self, version: int, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.eq("_version_", version), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.and_(qb.gte("date_inserted", start_date), qb.lte("date_inserted", end_date)), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", qb.and_(qb.gte("date_modified", start_date), qb.lte("date_modified", end_date)), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("structured_assertion", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("structured_assertion", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Solr cursor-based streaming (Option B implementation)
  def stream_all_solr(
    self,
    *,
    rows: int = 1000,
    sort: str | None = None,
    unique_key: str | None = "id",
    fields: list[str] | None = None,
    q_expr: str | None = None,
    fq: list[str] | None = None,
    start_cursor: str = "*",
    context_overrides: Dict[str, Any] | None = None,
  ) -> CursorPager:
    # Combine base context with optional overrides to build Solr context
    merged_ctx: Dict[str, Any] = {}
    merged_ctx.update(self._ctx)
    if context_overrides:
      merged_ctx.update(context_overrides)
    solr_ctx = create_solr_context(merged_ctx)

    base_params = solrqb.build_params(
      q_expr=q_expr or "*:*",
      fq_list=fq or None,
      fields=fields or None,
      # sort, rows, cursorMark handled by CursorPager for iteration
    )

    return CursorPager(
      collection="structured_assertion",
      base_params=base_params,
      base_url=solr_ctx["solr_base_url"],
      headers=solr_ctx.get("headers"),
      auth=solr_ctx.get("auth"),
      rows=rows,
      sort=sort,
      unique_key=unique_key,
      start_cursor=start_cursor,
      timeout=solr_ctx.get("timeout", 60.0),
    )


__all__ = ["StructuredAssertion"]


