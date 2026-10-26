from __future__ import annotations

from typing import Any, Dict

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class GenomeFeature:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, feature_id: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("feature_id", feature_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_id(self, genome_id: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("genome_id", genome_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_name(self, genome_name: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("genome_name", genome_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gene(self, gene_name: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("gene", gene_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_product(self, product_name: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("product", product_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_feature_type(self, feature_type: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("feature_type", feature_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_annotation(self, annotation_type: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("annotation", annotation_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_patric_id(self, patric_id: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("patric_id", patric_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_protein_id(self, protein_id: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("protein_id", protein_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_accession(self, accession: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("accession", accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_uniprot_accession(self, uniprot_accession: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("uniprotkb_accession", uniprot_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_figfam_id(self, figfam_id: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("figfam_id", figfam_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pgfam_id(self, pgfam_id: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("pgfam_id", pgfam_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_plfam_id(self, plfam_id: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("plfam_id", plfam_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_go_term(self, go_term: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("go", go_term), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_strand(self, strand: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("strand", strand), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_location_range(self, start: int, end: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("start", start), qb.lt("end", end)]
    return run("genome_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sequence_length_range(self, min_length: int, max_length: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("na_length", min_length), qb.lt("na_length", max_length)]
    return run("genome_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_protein_length_range(self, min_length: int, max_length: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("aa_length", min_length), qb.lt("aa_length", max_length)]
    return run("genome_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_classifier_score_range(self, min_score: float, max_score: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("classifier_score", min_score), qb.lt("classifier_score", max_score)]
    return run("genome_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("genome_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_public_status(self, is_public: bool, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("public", is_public), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sequence_id(self, sequence_id: str, options: Dict[str, Any] | None = None):
    return run("genome_feature", qb.eq("sequence_id", sequence_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("genome_feature", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Solr cursor-based streaming (Option B implementation)
  def stream_all_solr(
    self,
    *,
    rows: int = 1000,
    sort: str | None = None,
    unique_key: str | None = "feature_id",
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
      collection="genome_feature",
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


__all__ = ["GenomeFeature"]


