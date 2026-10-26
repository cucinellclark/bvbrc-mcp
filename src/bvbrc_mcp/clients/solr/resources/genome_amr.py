from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class GenomeAmr:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, id: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("id", id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_antibiotic(self, antibiotic: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("antibiotic", antibiotic), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_computational_method(self, computational_method: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("computational_method", computational_method), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_computational_method_version(self, computational_method_version: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("computational_method_version", computational_method_version), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_evidence(self, evidence: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("evidence", evidence), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_id(self, genome_id: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("genome_id", genome_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_name(self, genome_name: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("genome_name", genome_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_laboratory_typing_method(self, laboratory_typing_method: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("laboratory_typing_method", laboratory_typing_method), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_laboratory_typing_method_version(self, laboratory_typing_method_version: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("laboratory_typing_method_version", laboratory_typing_method_version), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_laboratory_typing_platform(self, laboratory_typing_platform: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("laboratory_typing_platform", laboratory_typing_platform), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_measurement(self, measurement: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("measurement", measurement), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_measurement_sign(self, measurement_sign: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("measurement_sign", measurement_sign), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_measurement_unit(self, measurement_unit: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("measurement_unit", measurement_unit), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_measurement_value(self, measurement_value: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("measurement_value", measurement_value), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_owner(self, owner: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("owner", owner), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pmid(self, pmid: int, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("pmid", pmid), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_public_status(self, is_public: bool, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("public", is_public), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_resistant_phenotype(self, resistant_phenotype: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("resistant_phenotype", resistant_phenotype), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_source(self, source: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("source", source), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_testing_standard(self, testing_standard: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("testing_standard", testing_standard), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_testing_standard_year(self, testing_standard_year: int, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("testing_standard_year", testing_standard_year), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_vendor(self, vendor: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", qb.eq("vendor", vendor), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("genome_amr", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_modified_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("genome_amr", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("genome_amr", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("genome_amr", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

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
      collection="genome_amr",
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


__all__ = ["GenomeAmr"]
