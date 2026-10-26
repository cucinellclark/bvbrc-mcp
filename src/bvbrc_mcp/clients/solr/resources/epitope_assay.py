from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class EpitopeAssay:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, assay_id: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("assay_id", assay_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_assay_group(self, assay_group: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("assay_group", assay_group), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_assay_measurement(self, assay_measurement: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("assay_measurement", assay_measurement), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_assay_measurement_unit(self, assay_measurement_unit: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("assay_measurement_unit", assay_measurement_unit), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_assay_method(self, assay_method: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("assay_method", assay_method), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_assay_result(self, assay_result: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("assay_result", assay_result), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_assay_type(self, assay_type: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("assay_type", assay_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_authors(self, authors: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("authors", authors), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_epitope_id(self, epitope_id: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("epitope_id", epitope_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_epitope_sequence(self, epitope_sequence: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("epitope_sequence", epitope_sequence), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_epitope_type(self, epitope_type: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("epitope_type", epitope_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_name(self, host_name: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("host_name", host_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_taxon_id(self, host_taxon_id: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("host_taxon_id", host_taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_mhc_allele(self, mhc_allele: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("mhc_allele", mhc_allele), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_mhc_allele_class(self, mhc_allele_class: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("mhc_allele_class", mhc_allele_class), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_organism(self, organism: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("organism", organism), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pdb_id(self, pdb_id: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("pdb_id", pdb_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pmid(self, pmid: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("pmid", pmid), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_protein_accession(self, protein_accession: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("protein_accession", protein_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_protein_id(self, protein_id: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("protein_id", protein_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_protein_name(self, protein_name: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("protein_name", protein_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_start(self, start: int, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("start", start), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_end(self, end: int, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("end", end), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_lineage_id(self, taxon_lineage_id: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("taxon_lineage_ids", taxon_lineage_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_lineage_name(self, taxon_lineage_name: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("taxon_lineage_names", taxon_lineage_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_title(self, title: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", qb.eq("title", title), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_position_range(self, min_start: int, max_end: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("start", min_start), qb.lt("end", max_end)]
    return run("epitope_assay", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("epitope_assay", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("epitope_assay", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("epitope_assay", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("epitope_assay", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Solr cursor-based streaming (Option B implementation)
  def stream_all_solr(
    self,
    *,
    rows: int = 1000,
    sort: str | None = None,
    unique_key: str | None = "assay_id",
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
      collection="epitope_assay",
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


__all__ = ["EpitopeAssay"]
