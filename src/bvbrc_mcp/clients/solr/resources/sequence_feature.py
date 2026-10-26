from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class SequenceFeature:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, id: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("id", id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_feature_id(self, feature_id: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("feature_id", feature_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_id(self, genome_id: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("genome_id", genome_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_name(self, genome_name: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("genome_name", genome_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gene(self, gene: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("gene", gene), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_product(self, product: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("product", product), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_patric_id(self, patric_id: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("patric_id", patric_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genbank_accession(self, genbank_accession: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("genbank_accession", genbank_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_refseq_locus_tag(self, refseq_locus_tag: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("refseq_locus_tag", refseq_locus_tag), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sf_category(self, sf_category: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("sf_category", sf_category), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sf_id(self, sf_id: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("sf_id", sf_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sf_name(self, sf_name: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("sf_name", sf_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_source(self, source: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("source", source), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_source_id(self, source_id: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("source_id", source_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_source_strain(self, source_strain: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("source_strain", source_strain), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_segment(self, segment: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("segment", segment), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_subtype(self, subtype: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("subtype", subtype), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_evidence_code(self, evidence_code: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("evidence_code", evidence_code), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_aa_sequence_md5(self, aa_sequence_md5: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("aa_sequence_md5", aa_sequence_md5), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_aa_variant(self, aa_variant: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("aa_variant", aa_variant), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sf_sequence_md5(self, sf_sequence_md5: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("sf_sequence_md5", sf_sequence_md5), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_source_aa_sequence(self, source_aa_sequence: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("source_aa_sequence", source_aa_sequence), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_source_sf_location(self, source_sf_location: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("source_sf_location", source_sf_location), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_variant_types(self, variant_types: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("variant_types", variant_types), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_start(self, start: int, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("start", start), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_end(self, end: int, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("end", end), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_length(self, length: int, options: Dict[str, Any] | None = None):
    return run("sequence_feature", qb.eq("length", length), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_position_range(self, start: int, end: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("start", start), qb.lt("end", end)]
    return run("sequence_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_length_range(self, min_length: int, max_length: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("length", min_length), qb.lt("length", max_length)]
    return run("sequence_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("sequence_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_modified_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("sequence_feature", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("sequence_feature", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("sequence_feature", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

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
      collection="sequence_feature",
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


__all__ = ["SequenceFeature"]
