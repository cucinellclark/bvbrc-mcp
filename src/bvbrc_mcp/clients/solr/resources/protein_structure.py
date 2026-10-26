from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class ProteinStructure:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, pdb_id: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("pdb_id", pdb_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_feature_id(self, feature_id: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("feature_id", feature_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_id(self, genome_id: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("genome_id", genome_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_patric_id(self, patric_id: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("patric_id", patric_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_organism_name(self, organism_name: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("organism_name", organism_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_title(self, title: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("title", title), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_resolution(self, resolution: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("resolution", resolution), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_institution(self, institution: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("institution", institution), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_file_path(self, file_path: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("file_path", file_path), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_author(self, author: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("authors", author), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_method(self, method: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("method", method), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gene(self, gene: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("gene", gene), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_product(self, product: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("product", product), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sequence(self, sequence: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("sequence", sequence), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sequence_md5(self, sequence_md5: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("sequence_md5", sequence_md5), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_uniprotkb_accession(self, uniprotkb_accession: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("uniprotkb_accession", uniprotkb_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pmid(self, pmid: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("pmid", pmid), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_lineage_id(self, taxon_lineage_id: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("taxon_lineage_ids", taxon_lineage_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_lineage_name(self, taxon_lineage_name: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("taxon_lineage_names", taxon_lineage_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_alignment(self, alignment: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", qb.eq("alignments", alignment), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_release_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("release_date", start_date), qb.lt("release_date", end_date)]
    return run("protein_structure", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("protein_structure", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("protein_structure", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("protein_structure", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("protein_structure", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Solr cursor-based streaming (Option B implementation)
  def stream_all_solr(
    self,
    *,
    rows: int = 1000,
    sort: str | None = None,
    unique_key: str | None = "pdb_id",
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
      collection="protein_structure",
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


__all__ = ["ProteinStructure"]
