from __future__ import annotations

from types import SimpleNamespace
from typing import Dict, Iterable, List
from urllib.parse import quote


def _encode(value) -> str:
  if isinstance(value, str) and value in {"+", "-"}:
    return quote(f'"{value}"', safe="")
  return quote(str(value), safe="")


def eq(field_name: str, value) -> str:
  return f"eq({field_name},{_encode(value)})"


def gt(field_name: str, value) -> str:
  return f"gt({field_name},{_encode(value)})"


def lt(field_name: str, value) -> str:
  return f"lt({field_name},{_encode(value)})"


def and_filters(*parts: str) -> str:
  cleaned = [p for p in parts if p]
  return f"and({','.join(cleaned)})" if cleaned else ""


def or_filters(*parts: str) -> str:
  cleaned = [p for p in parts if p]
  return f"or({','.join(cleaned)})" if cleaned else ""


def in_filters(field_name: str, values: Iterable) -> str:
  values_list = list(values)
  return f"in({field_name},{','.join(_encode(v) for v in values_list)})" if values_list else ""


def select(fields: List[str]) -> str:
  return f"select({','.join(fields)})" if fields else ""


def sort(sort_expr: str) -> str:
  return f"sort({sort_expr})" if sort_expr else ""


def limit(limit_value: int) -> str:
  return f"limit({int(limit_value)})" if isinstance(limit_value, int) else ""


def http_download(enable: bool = False) -> str:
  return "http_download=true" if enable else ""


def obj_to_eq(filters: Dict[str, object] | None = None):
  filters = filters or {}
  return [eq(k, v) for k, v in filters.items()]


def build_and_from(filters: Dict[str, object] | None = None) -> str:
  return and_filters(*obj_to_eq(filters))


qb = SimpleNamespace(
  eq=eq,
  gt=gt,
  lt=lt,
  and_=and_filters,
  or_=or_filters,
  in_=in_filters,
  select=select,
  sort=sort,
  limit=limit,
  http_download=http_download,
  obj_to_eq=obj_to_eq,
  build_and_from=build_and_from,
)


__all__ = [
  "qb",
  "eq",
  "gt",
  "lt",
  "and_filters",
  "or_filters",
  "in_filters",
  "select",
  "sort",
  "limit",
  "http_download",
  "obj_to_eq",
  "build_and_from",
]


