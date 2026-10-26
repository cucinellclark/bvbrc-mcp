from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class SpikeLineage:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, id: str, options: Dict[str, Any] | None = None):
    return run("spike_lineage", qb.eq("id", id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("spike_lineage", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_country(self, country: str, options: Dict[str, Any] | None = None):
    return run("spike_lineage", qb.eq("country", country), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_growth_rate(self, growth_rate: float, options: Dict[str, Any] | None = None):
    return run("spike_lineage", qb.eq("growth_rate", growth_rate), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_lineage(self, lineage: str, options: Dict[str, Any] | None = None):
    return run("spike_lineage", qb.eq("lineage", lineage), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_lineage_count(self, lineage_count: int, options: Dict[str, Any] | None = None):
    return run("spike_lineage", qb.eq("lineage_count", lineage_count), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_lineage_of_concern(self, lineage_of_concern: str, options: Dict[str, Any] | None = None):
    return run("spike_lineage", qb.eq("lineage_of_concern", lineage_of_concern), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_month(self, month: str, options: Dict[str, Any] | None = None):
    return run("spike_lineage", qb.eq("month", month), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_prevalence(self, prevalence: float, options: Dict[str, Any] | None = None):
    return run("spike_lineage", qb.eq("prevalence", prevalence), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_region(self, region: str, options: Dict[str, Any] | None = None):
    return run("spike_lineage", qb.eq("region", region), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sequence_features(self, sequence_features: str, options: Dict[str, Any] | None = None):
    return run("spike_lineage", qb.eq("sequence_features", sequence_features), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_total_isolates(self, total_isolates: int, options: Dict[str, Any] | None = None):
    return run("spike_lineage", qb.eq("total_isolates", total_isolates), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_growth_rate_range(self, min_growth_rate: float, max_growth_rate: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("growth_rate", min_growth_rate), qb.lt("growth_rate", max_growth_rate)]
    return run("spike_lineage", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_lineage_count_range(self, min_lineage_count: int, max_lineage_count: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("lineage_count", min_lineage_count), qb.lt("lineage_count", max_lineage_count)]
    return run("spike_lineage", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_prevalence_range(self, min_prevalence: float, max_prevalence: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("prevalence", min_prevalence), qb.lt("prevalence", max_prevalence)]
    return run("spike_lineage", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_total_isolates_range(self, min_total_isolates: int, max_total_isolates: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("total_isolates", min_total_isolates), qb.lt("total_isolates", max_total_isolates)]
    return run("spike_lineage", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("spike_lineage", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("spike_lineage", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("spike_lineage", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("spike_lineage", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

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
      collection="spike_lineage",
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


__all__ = ["SpikeLineage"]
