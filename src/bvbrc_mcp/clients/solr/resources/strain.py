from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class Strain:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, id: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("id", id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("strain", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_1_pb2(self, pb2: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("1_pb2", pb2), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_2_pb1(self, pb1: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("2_pb1", pb1), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_3_pa(self, pa: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("3_pa", pa), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_4_ha(self, ha: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("4_ha", ha), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_5_np(self, np: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("5_np", np), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_6_na(self, na: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("6_na", na), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_7_mp(self, mp: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("7_mp", mp), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_8_ns(self, ns: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("8_ns", ns), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_date(self, collection_date: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("collection_date", collection_date), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_year(self, collection_year: int, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("collection_year", collection_year), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_family(self, family: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("family", family), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genbank_accessions(self, genbank_accessions: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("genbank_accessions", genbank_accessions), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_ids(self, genome_ids: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("genome_ids", genome_ids), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genus(self, genus: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("genus", genus), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_geographic_group(self, geographic_group: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("geographic_group", geographic_group), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_h_type(self, h_type: int, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("h_type", h_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_common_name(self, host_common_name: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("host_common_name", host_common_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_group(self, host_group: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("host_group", host_group), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_name(self, host_name: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("host_name", host_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_isolation_country(self, isolation_country: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("isolation_country", isolation_country), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_l(self, l: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("l", l), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_lab_host(self, lab_host: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("lab_host", lab_host), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_m(self, m: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("m", m), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_n_type(self, n_type: int, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("n_type", n_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_other_segments(self, other_segments: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("other_segments", other_segments), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_owner(self, owner: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("owner", owner), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_passage(self, passage: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("passage", passage), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_public(self, is_public: bool, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("public", is_public), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_s(self, s: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("s", s), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_season(self, season: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("season", season), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_segment_count(self, segment_count: int, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("segment_count", segment_count), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_species(self, species: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("species", species), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_status(self, status: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("status", status), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_strain(self, strain: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("strain", strain), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_subtype(self, subtype: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("subtype", subtype), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_lineage_ids(self, taxon_lineage_ids: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("taxon_lineage_ids", taxon_lineage_ids), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_lineage_names(self, taxon_lineage_names: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("taxon_lineage_names", taxon_lineage_names), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_user_read(self, user_read: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("user_read", user_read), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_user_write(self, user_write: str, options: Dict[str, Any] | None = None):
    return run("strain", qb.eq("user_write", user_write), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_year_range(self, start_year: int, end_year: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("collection_year", start_year), qb.lt("collection_year", end_year)]
    return run("strain", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("strain", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("strain", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_h_type_range(self, min_h_type: int, max_h_type: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("h_type", min_h_type), qb.lt("h_type", max_h_type)]
    return run("strain", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_n_type_range(self, min_n_type: int, max_n_type: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("n_type", min_n_type), qb.lt("n_type", max_n_type)]
    return run("strain", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_segment_count_range(self, min_segment_count: int, max_segment_count: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("segment_count", min_segment_count), qb.lt("segment_count", max_segment_count)]
    return run("strain", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id_range(self, min_taxon_id: int, max_taxon_id: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("taxon_id", min_taxon_id), qb.lt("taxon_id", max_taxon_id)]
    return run("strain", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("strain", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("strain", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

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
      collection="strain",
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


__all__ = ["Strain"]
