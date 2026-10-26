from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class Serology:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, id: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("id", id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("serology", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_additional_metadata(self, additional_metadata: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("additional_metadata", additional_metadata), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_city(self, collection_city: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("collection_city", collection_city), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_country(self, collection_country: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("collection_country", collection_country), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_state(self, collection_state: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("collection_state", collection_state), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_year(self, collection_year: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("collection_year", collection_year), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_comments(self, comments: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("comments", comments), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_contributing_institution(self, contributing_institution: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("contributing_institution", contributing_institution), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genbank_accession(self, genbank_accession: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("genbank_accession", genbank_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_geographic_group(self, geographic_group: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("geographic_group", geographic_group), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_age(self, host_age: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("host_age", host_age), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_age_group(self, host_age_group: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("host_age_group", host_age_group), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_common_name(self, host_common_name: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("host_common_name", host_common_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_health(self, host_health: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("host_health", host_health), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_identifier(self, host_identifier: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("host_identifier", host_identifier), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_sex(self, host_sex: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("host_sex", host_sex), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_species(self, host_species: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("host_species", host_species), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_type(self, host_type: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("host_type", host_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_positive_definition(self, positive_definition: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("positive_definition", positive_definition), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_project_identifier(self, project_identifier: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("project_identifier", project_identifier), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sample_accession(self, sample_accession: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("sample_accession", sample_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sample_identifier(self, sample_identifier: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("sample_identifier", sample_identifier), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_serotype(self, serotype: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("serotype", serotype), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_strain(self, strain: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("strain", strain), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_lineage_id(self, taxon_lineage_id: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("taxon_lineage_ids", taxon_lineage_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_test_antigen(self, test_antigen: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("test_antigen", test_antigen), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_test_interpretation(self, test_interpretation: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("test_interpretation", test_interpretation), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_test_pathogen(self, test_pathogen: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("test_pathogen", test_pathogen), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_test_result(self, test_result: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("test_result", test_result), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_test_type(self, test_type: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("test_type", test_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_virus_identifier(self, virus_identifier: str, options: Dict[str, Any] | None = None):
    return run("serology", qb.eq("virus_identifier", virus_identifier), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("collection_date", start_date), qb.lt("collection_date", end_date)]
    return run("serology", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("serology", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("serology", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("serology", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("serology", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

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
      collection="serology",
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


__all__ = ["Serology"]
