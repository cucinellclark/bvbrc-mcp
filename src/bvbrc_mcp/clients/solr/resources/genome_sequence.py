from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class GenomeSequence:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, sequence_id: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("sequence_id", sequence_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_accession(self, accession: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("accession", accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_chromosome(self, chromosome: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("chromosome", chromosome), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_description(self, description: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("description", description), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gc_content(self, gc_content: float, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("gc_content", gc_content), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_id(self, genome_id: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("genome_id", genome_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_name(self, genome_name: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("genome_name", genome_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gi(self, gi: int, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("gi", gi), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_length(self, length: int, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("length", length), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_mol_type(self, mol_type: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("mol_type", mol_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_owner(self, owner: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("owner", owner), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_p2_sequence_id(self, p2_sequence_id: int, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("p2_sequence_id", p2_sequence_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_plasmid(self, plasmid: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("plasmid", plasmid), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_public_status(self, is_public: bool, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("public", is_public), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_segment(self, segment: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("segment", segment), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sequence_md5(self, sequence_md5: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("sequence_md5", sequence_md5), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sequence_status(self, sequence_status: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("sequence_status", sequence_status), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sequence_type(self, sequence_type: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("sequence_type", sequence_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_topology(self, topology: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("topology", topology), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_version(self, version: int, options: Dict[str, Any] | None = None):
    return run("genome_sequence", qb.eq("version", version), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_length_range(self, min_length: int, max_length: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("length", min_length), qb.lt("length", max_length)]
    return run("genome_sequence", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gc_content_range(self, min_gc_content: float, max_gc_content: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("gc_content", min_gc_content), qb.lt("gc_content", max_gc_content)]
    return run("genome_sequence", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("genome_sequence", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("genome_sequence", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_release_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("release_date", start_date), qb.lt("release_date", end_date)]
    return run("genome_sequence", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("genome_sequence", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("genome_sequence", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Solr cursor-based streaming (Option B implementation)
  def stream_all_solr(
    self,
    *,
    rows: int = 1000,
    sort: str | None = None,
    unique_key: str | None = "sequence_id",
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
      collection="genome_sequence",
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


__all__ = ["GenomeSequence"]
