from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class Experiment:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, exp_id: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("exp_id", exp_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("experiment", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_additional_data(self, additional_data: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("additional_data", additional_data), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_additional_metadata(self, additional_metadata: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("additional_metadata", additional_metadata), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_biosets(self, biosets: int, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("biosets", biosets), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_detection_instrument(self, detection_instrument: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("detection_instrument", detection_instrument), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_doi(self, doi: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("doi", doi), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_exp_description(self, exp_description: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("exp_description", exp_description), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_exp_name(self, exp_name: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("exp_name", exp_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_exp_poc(self, exp_poc: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("exp_poc", exp_poc), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_exp_protocol(self, exp_protocol: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("exp_protocol", exp_protocol), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_exp_title(self, exp_title: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("exp_title", exp_title), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_exp_type(self, exp_type: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("exp_type", exp_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_experimenters(self, experimenters: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("experimenters", experimenters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_id(self, genome_id: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("genome_id", genome_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_measurement_technique(self, measurement_technique: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("measurement_technique", measurement_technique), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_organism(self, organism: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("organism", organism), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pmid(self, pmid: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("pmid", pmid), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_public_identifier(self, public_identifier: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("public_identifier", public_identifier), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_public_repository(self, public_repository: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("public_repository", public_repository), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_samples(self, samples: int, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("samples", samples), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_strain(self, strain: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("strain", strain), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_study_description(self, study_description: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("study_description", study_description), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_study_institution(self, study_institution: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("study_institution", study_institution), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_study_name(self, study_name: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("study_name", study_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_study_pi(self, study_pi: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("study_pi", study_pi), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_study_title(self, study_title: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("study_title", study_title), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_lineage_ids(self, taxon_lineage_ids: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("taxon_lineage_ids", taxon_lineage_ids), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_treatment_amount(self, treatment_amount: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("treatment_amount", treatment_amount), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_treatment_duration(self, treatment_duration: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("treatment_duration", treatment_duration), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_treatment_name(self, treatment_name: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("treatment_name", treatment_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_treatment_type(self, treatment_type: str, options: Dict[str, Any] | None = None):
    return run("experiment", qb.eq("treatment_type", treatment_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("experiment", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("experiment", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_biosets_range(self, min_biosets: int, max_biosets: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("biosets", min_biosets), qb.lt("biosets", max_biosets)]
    return run("experiment", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_samples_range(self, min_samples: int, max_samples: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("samples", min_samples), qb.lt("samples", max_samples)]
    return run("experiment", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("experiment", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("experiment", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Solr cursor-based streaming (Option B implementation)
  def stream_all_solr(
    self,
    *,
    rows: int = 1000,
    sort: str | None = None,
    unique_key: str | None = "exp_id",
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
      collection="experiment",
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


__all__ = ["Experiment"]
