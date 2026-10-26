from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class Pathway:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, id: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("id", id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("pathway", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_accession(self, accession: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("accession", accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_alt_locus_tag(self, alt_locus_tag: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("alt_locus_tag", alt_locus_tag), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_annotation(self, annotation: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("annotation", annotation), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_ec_description(self, ec_description: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("ec_description", ec_description), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_ec_number(self, ec_number: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("ec_number", ec_number), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_feature_id(self, feature_id: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("feature_id", feature_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gene(self, gene: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("gene", gene), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_ec(self, genome_ec: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("genome_ec", genome_ec), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_id(self, genome_id: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("genome_id", genome_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_name(self, genome_name: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("genome_name", genome_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_owner(self, owner: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("owner", owner), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pathway_class(self, pathway_class: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("pathway_class", pathway_class), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pathway_ec(self, pathway_ec: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("pathway_ec", pathway_ec), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pathway_id(self, pathway_id: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("pathway_id", pathway_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pathway_name(self, pathway_name: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("pathway_name", pathway_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_patric_id(self, patric_id: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("patric_id", patric_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_product(self, product: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("product", product), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_public_status(self, is_public: bool, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("public", is_public), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_refseq_locus_tag(self, refseq_locus_tag: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("refseq_locus_tag", refseq_locus_tag), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sequence_id(self, sequence_id: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("sequence_id", sequence_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_user_read(self, user_read: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("user_read", user_read), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_user_write(self, user_write: str, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("user_write", user_write), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_version(self, version: int, options: Dict[str, Any] | None = None):
    return run("pathway", qb.eq("_version_", version), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("pathway", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("pathway", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("pathway", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("pathway", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

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
      collection="pathway",
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


__all__ = ["Pathway"]
