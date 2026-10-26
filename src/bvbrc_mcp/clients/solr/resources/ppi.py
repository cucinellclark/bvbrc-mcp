from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class Ppi:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, id: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("id", id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("ppi", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_category(self, category: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("category", category), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_detection_method(self, detection_method: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("detection_method", detection_method), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_domain_a(self, domain_a: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("domain_a", domain_a), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_domain_b(self, domain_b: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("domain_b", domain_b), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_evidence(self, evidence: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("evidence", evidence), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_feature_id_a(self, feature_id_a: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("feature_id_a", feature_id_a), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_feature_id_b(self, feature_id_b: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("feature_id_b", feature_id_b), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gene_a(self, gene_a: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("gene_a", gene_a), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gene_b(self, gene_b: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("gene_b", gene_b), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_id_a(self, genome_id_a: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("genome_id_a", genome_id_a), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_id_b(self, genome_id_b: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("genome_id_b", genome_id_b), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_name_a(self, genome_name_a: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("genome_name_a", genome_name_a), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_name_b(self, genome_name_b: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("genome_name_b", genome_name_b), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_interaction_type(self, interaction_type: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("interaction_type", interaction_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_interactor_a(self, interactor_a: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("interactor_a", interactor_a), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_interactor_b(self, interactor_b: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("interactor_b", interactor_b), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_interactor_desc_a(self, interactor_desc_a: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("interactor_desc_a", interactor_desc_a), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_interactor_desc_b(self, interactor_desc_b: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("interactor_desc_b", interactor_desc_b), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_interactor_type_a(self, interactor_type_a: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("interactor_type_a", interactor_type_a), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_interactor_type_b(self, interactor_type_b: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("interactor_type_b", interactor_type_b), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pmid(self, pmid: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("pmid", pmid), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_refseq_locus_tag_a(self, refseq_locus_tag_a: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("refseq_locus_tag_a", refseq_locus_tag_a), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_refseq_locus_tag_b(self, refseq_locus_tag_b: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("refseq_locus_tag_b", refseq_locus_tag_b), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_score(self, score: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("score", score), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_source_db(self, source_db: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("source_db", source_db), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_source_id(self, source_id: str, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("source_id", source_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id_a(self, taxon_id_a: int, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("taxon_id_a", taxon_id_a), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id_b(self, taxon_id_b: int, options: Dict[str, Any] | None = None):
    return run("ppi", qb.eq("taxon_id_b", taxon_id_b), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("ppi", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("ppi", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("ppi", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("ppi", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

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
      collection="ppi",
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


__all__ = ["Ppi"]
