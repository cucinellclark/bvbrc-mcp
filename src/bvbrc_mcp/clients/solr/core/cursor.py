from __future__ import annotations

from typing import Any, Dict, Generator, Iterable, List, Optional

from .solr_http_client import select


class CursorPager:
  def __init__(
    self,
    *,
    collection: str,
    base_params: Dict[str, Any],
    base_url: str,
    headers: Dict[str, str] | None = None,
    auth: Any = None,
    rows: int = 1000,
    sort: str | None = None,
    unique_key: str | None = "id",
    start_cursor: str = "*",
    timeout: float = 60.0,
  ) -> None:
    self.collection = collection
    self.base_params = dict(base_params)
    self.base_url = base_url
    self.headers = headers or {}
    self.auth = auth
    self.rows = int(rows)
    self.sort = sort
    self.unique_key = unique_key
    self.cursor = start_cursor
    self.timeout = timeout

    if not self.sort:
      if not self.unique_key:
        raise ValueError("CursorPager requires either sort or unique_key for deterministic ordering")
      self.sort = f"{self.unique_key} asc"
    elif self.unique_key and self.unique_key not in self.sort:
      # Ensure stable tie-breaker
      self.sort = f"{self.sort}, {self.unique_key} asc"

  def __iter__(self):
    return self.iter_docs()

  def iter_docs(self) -> Generator[Dict[str, Any], None, None]:
    last_mark = None
    while True:
      params = dict(self.base_params)
      params["rows"] = self.rows
      params["sort"] = self.sort
      params["cursorMark"] = self.cursor

      result = select(
        self.collection,
        params,
        base_url=self.base_url,
        headers=self.headers,
        auth=self.auth,
        timeout=self.timeout,
      )

      response = result.get("response", {})
      docs: List[Dict[str, Any]] = response.get("docs", [])
      next_cursor = result.get("nextCursorMark")

      if not docs:
        return

      for doc in docs:
        yield doc

      if next_cursor is None or next_cursor == self.cursor or next_cursor == last_mark:
        return
      last_mark = self.cursor
      self.cursor = next_cursor


__all__ = ["CursorPager"]


