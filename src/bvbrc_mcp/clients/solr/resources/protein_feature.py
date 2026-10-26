from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class ProteinFeature:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, id: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("id", id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_aa_sequence_md5(self, aa_sequence_md5: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("aa_sequence_md5", aa_sequence_md5), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_classification(self, classification: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("classification", classification), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_comment(self, comment: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("comments", comment), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_description(self, description: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("description", description), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_e_value(self, e_value: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("e_value", e_value), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_end(self, end: int, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("end", end), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_evidence(self, evidence: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("evidence", evidence), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_feature_id(self, feature_id: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("feature_id", feature_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_feature_type(self, feature_type: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("feature_type", feature_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gene(self, gene: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("gene", gene), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_id(self, genome_id: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("genome_id", genome_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_name(self, genome_name: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("genome_name", genome_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_interpro_description(self, interpro_description: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("interpro_description", interpro_description), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_interpro_id(self, interpro_id: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("interpro_id", interpro_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_length(self, length: int, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("length", length), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_patric_id(self, patric_id: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("patric_id", patric_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_product(self, product: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("product", product), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_publication(self, publication: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("publication", publication), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_refseq_locus_tag(self, refseq_locus_tag: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("refseq_locus_tag", refseq_locus_tag), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_score(self, score: float, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("score", score), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_segment(self, segment: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("segments", segment), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sequence(self, sequence: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("sequence", sequence), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_source(self, source: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("source", source), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_source_id(self, source_id: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("source_id", source_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_start(self, start: int, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("start", start), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("protein_feature", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_score_range(self, min_score: float, max_score: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("score", min_score), qb.lt("score", max_score)]
    return run("protein_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_length_range(self, min_length: int, max_length: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("length", min_length), qb.lt("length", max_length)]
    return run("protein_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_position_range(self, min_start: int, max_end: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("start", min_start), qb.lt("end", max_end)]
    return run("protein_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("protein_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("protein_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("protein_feature", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("protein_feature", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

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
      collection="protein_feature",
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


__all__ = ["ProteinFeature"]
