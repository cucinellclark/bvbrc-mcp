from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class Epitope:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, epitope_id: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("epitope_id", epitope_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("epitope", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_epitope_sequence(self, epitope_sequence: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("epitope_sequence", epitope_sequence), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_epitope_type(self, epitope_type: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("epitope_type", epitope_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_name(self, host_name: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("host_name", host_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_organism(self, organism: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("organism", organism), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_protein_accession(self, protein_accession: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("protein_accession", protein_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_protein_id(self, protein_id: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("protein_id", protein_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_protein_name(self, protein_name: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("protein_name", protein_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_start(self, start: int, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("start", start), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_end(self, end: int, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("end", end), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_bcell_assays(self, bcell_assays: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("bcell_assays", bcell_assays), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_mhc_assays(self, mhc_assays: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("mhc_assays", mhc_assays), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_tcell_assays(self, tcell_assays: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("tcell_assays", tcell_assays), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_total_assays(self, total_assays: int, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("total_assays", total_assays), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_comment(self, comment: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("comments", comment), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_assay_result(self, assay_result: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("assay_results", assay_result), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_lineage_id(self, taxon_lineage_id: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("taxon_lineage_ids", taxon_lineage_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_lineage_name(self, taxon_lineage_name: str, options: Dict[str, Any] | None = None):
    return run("epitope", qb.eq("taxon_lineage_names", taxon_lineage_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_position_range(self, min_start: int, max_end: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("start", min_start), qb.lt("end", max_end)]
    return run("epitope", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_total_assays_range(self, min_assays: int, max_assays: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("total_assays", min_assays), qb.lt("total_assays", max_assays)]
    return run("epitope", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("epitope", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("epitope", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("epitope", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("epitope", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Solr cursor-based streaming (Option B implementation)
  def stream_all_solr(
    self,
    *,
    rows: int = 1000,
    sort: str | None = None,
    unique_key: str | None = "epitope_id",
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
      collection="epitope",
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


__all__ = ["Epitope"]
