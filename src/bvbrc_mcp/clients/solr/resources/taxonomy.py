from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class Taxonomy:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, taxon_id: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_cds_mean(self, cds_mean: float, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("cds_mean", cds_mean), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_cds_sd(self, cds_sd: float, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("cds_sd", cds_sd), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_core_families(self, core_families: int, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("core_families", core_families), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_core_family_ids(self, core_family_ids: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("core_family_ids", core_family_ids), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_description(self, description: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("description", description), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_division(self, division: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("division", division), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genetic_code(self, genetic_code: int, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("genetic_code", genetic_code), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_count(self, genome_count: int, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("genome_count", genome_count), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_length_mean(self, genome_length_mean: float, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("genome_length_mean", genome_length_mean), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_length_sd(self, genome_length_sd: float, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("genome_length_sd", genome_length_sd), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genomes(self, genomes: int, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("genomes", genomes), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genomes_f(self, genomes_f: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("genomes_f", genomes_f), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_hypothetical_cds_ratio_mean(self, hypothetical_cds_ratio_mean: float, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("hypothetical_cds_ratio_mean", hypothetical_cds_ratio_mean), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_hypothetical_cds_ratio_sd(self, hypothetical_cds_ratio_sd: float, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("hypothetical_cds_ratio_sd", hypothetical_cds_ratio_sd), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_lineage(self, lineage: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("lineage", lineage), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_lineage_ids(self, lineage_ids: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("lineage_ids", lineage_ids), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_lineage_names(self, lineage_names: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("lineage_names", lineage_names), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_lineage_ranks(self, lineage_ranks: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("lineage_ranks", lineage_ranks), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_other_names(self, other_names: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("other_names", other_names), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_parent_id(self, parent_id: int, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("parent_id", parent_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_plfam_cds_ratio_mean(self, plfam_cds_ratio_mean: float, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("plfam_cds_ratio_mean", plfam_cds_ratio_mean), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_plfam_cds_ratio_sd(self, plfam_cds_ratio_sd: float, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("plfam_cds_ratio_sd", plfam_cds_ratio_sd), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id_i(self, taxon_id_i: int, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("taxon_id_i", taxon_id_i), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_name(self, taxon_name: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("taxon_name", taxon_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_rank(self, taxon_rank: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", qb.eq("taxon_rank", taxon_rank), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_cds_mean_range(self, min_cds_mean: float, max_cds_mean: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("cds_mean", min_cds_mean), qb.lt("cds_mean", max_cds_mean)]
    return run("taxonomy", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_core_families_range(self, min_core_families: int, max_core_families: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("core_families", min_core_families), qb.lt("core_families", max_core_families)]
    return run("taxonomy", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genetic_code_range(self, min_genetic_code: int, max_genetic_code: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("genetic_code", min_genetic_code), qb.lt("genetic_code", max_genetic_code)]
    return run("taxonomy", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_count_range(self, min_genome_count: int, max_genome_count: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("genome_count", min_genome_count), qb.lt("genome_count", max_genome_count)]
    return run("taxonomy", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_length_mean_range(self, min_genome_length_mean: float, max_genome_length_mean: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("genome_length_mean", min_genome_length_mean), qb.lt("genome_length_mean", max_genome_length_mean)]
    return run("taxonomy", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genomes_range(self, min_genomes: int, max_genomes: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("genomes", min_genomes), qb.lt("genomes", max_genomes)]
    return run("taxonomy", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_hypothetical_cds_ratio_mean_range(self, min_hypothetical_cds_ratio_mean: float, max_hypothetical_cds_ratio_mean: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("hypothetical_cds_ratio_mean", min_hypothetical_cds_ratio_mean), qb.lt("hypothetical_cds_ratio_mean", max_hypothetical_cds_ratio_mean)]
    return run("taxonomy", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_parent_id_range(self, min_parent_id: int, max_parent_id: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("parent_id", min_parent_id), qb.lt("parent_id", max_parent_id)]
    return run("taxonomy", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_plfam_cds_ratio_mean_range(self, min_plfam_cds_ratio_mean: float, max_plfam_cds_ratio_mean: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("plfam_cds_ratio_mean", min_plfam_cds_ratio_mean), qb.lt("plfam_cds_ratio_mean", max_plfam_cds_ratio_mean)]
    return run("taxonomy", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id_i_range(self, min_taxon_id_i: int, max_taxon_id_i: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("taxon_id_i", min_taxon_id_i), qb.lt("taxon_id_i", max_taxon_id_i)]
    return run("taxonomy", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("taxonomy", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("taxonomy", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Solr cursor-based streaming (Option B implementation)
  def stream_all_solr(
    self,
    *,
    rows: int = 1000,
    sort: str | None = None,
    unique_key: str | None = "taxon_id",
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
      collection="taxonomy",
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


__all__ = ["Taxonomy"]
