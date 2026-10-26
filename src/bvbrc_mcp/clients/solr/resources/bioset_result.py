from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class BiosetResult:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, id: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("id", id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_bioset_id(self, bioset_id: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("bioset_id", bioset_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_bioset_name(self, bioset_name: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("bioset_name", bioset_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_bioset_description(self, bioset_description: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("bioset_description", bioset_description), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_bioset_type(self, bioset_type: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("bioset_type", bioset_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_entity_id(self, entity_id: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("entity_id", entity_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_entity_name(self, entity_name: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("entity_name", entity_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_entity_type(self, entity_type: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("entity_type", entity_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_exp_id(self, exp_id: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("exp_id", exp_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_exp_name(self, exp_name: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("exp_name", exp_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_exp_title(self, exp_title: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("exp_title", exp_title), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_exp_type(self, exp_type: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("exp_type", exp_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_feature_id(self, feature_id: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("feature_id", feature_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gene(self, gene: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("gene", gene), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gene_id(self, gene_id: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("gene_id", gene_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_id(self, genome_id: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("genome_id", genome_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_locus_tag(self, locus_tag: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("locus_tag", locus_tag), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_organism(self, organism: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("organism", organism), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_patric_id(self, patric_id: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("patric_id", patric_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_product(self, product: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("product", product), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_protein_id(self, protein_id: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("protein_id", protein_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_result_type(self, result_type: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("result_type", result_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_strain(self, strain: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("strain", strain), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_uniprot_id(self, uniprot_id: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("uniprot_id", uniprot_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_other_id(self, other_id: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("other_ids", other_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_treatment_name(self, treatment_name: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("treatment_name", treatment_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_treatment_type(self, treatment_type: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("treatment_type", treatment_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_treatment_amount(self, treatment_amount: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("treatment_amount", treatment_amount), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_treatment_duration(self, treatment_duration: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("treatment_duration", treatment_duration), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_counts_range(self, min_counts: float, max_counts: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("counts", min_counts), qb.lt("counts", max_counts)]
    return run("bioset_result", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_fpkm_range(self, min_fpkm: float, max_fpkm: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("fpkm", min_fpkm), qb.lt("fpkm", max_fpkm)]
    return run("bioset_result", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_log2_fc_range(self, min_log2_fc: float, max_log2_fc: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("log2_fc", min_log2_fc), qb.lt("log2_fc", max_log2_fc)]
    return run("bioset_result", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_p_value_range(self, min_p_value: float, max_p_value: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("p_value", min_p_value), qb.lt("p_value", max_p_value)]
    return run("bioset_result", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_tpm_range(self, min_tpm: float, max_tpm: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("tpm", min_tpm), qb.lt("tpm", max_tpm)]
    return run("bioset_result", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_other_value_range(self, min_value: float, max_value: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("other_value", min_value), qb.lt("other_value", max_value)]
    return run("bioset_result", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_z_score_range(self, min_z_score: float, max_z_score: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("z_score", min_z_score), qb.lt("z_score", max_z_score)]
    return run("bioset_result", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_version(self, version: int, options: Dict[str, Any] | None = None):
    return run("bioset_result", qb.eq("_version_", version), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("bioset_result", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("bioset_result", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("bioset_result", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("bioset_result", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

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
      collection="bioset_result",
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


__all__ = ["BiosetResult"]
