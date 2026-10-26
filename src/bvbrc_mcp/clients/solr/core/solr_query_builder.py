from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Dict, Iterable, List, Sequence


def _escape_term(value: str) -> str:
  # Escape Solr special characters inside a quoted string
  # Reference: + - && || ! ( ) { } [ ] ^ " ~ * ? : \
  specials = set("+ - && || ! ( ) { } [ ] ^ \" ~ * ? : \\".split())
  escaped = []
  for ch in value:
    if ch in {"+", "-", "&&", "||", "!", "(", ")", "{", "}", "[", "]", "^", "\"", "~", "*", "?", ":", "\\"}:
      escaped.append(f"\\{ch}")
    else:
      escaped.append(ch)
  return "".join(escaped)


def _quote_if_needed(value: Any) -> str:
  if isinstance(value, (int, float)):
    return str(value)
  if isinstance(value, bool):
    return "true" if value else "false"
  if value is None:
    return "\"\""
  text = str(value)
  # Check if value looks like a numeric ID (e.g., "208964.12")
  # Don't quote numeric-looking values to match BV-BRC Solr expectations
  if text.replace('.', '', 1).replace('-', '', 1).isdigit():
    return text
  return f'"{_escape_term(text)}"'


def q(expr: str) -> str:
  return expr or "*:*"


def eq(field_name: str, value: Any) -> str:
  return f"{field_name}:{_quote_if_needed(value)}"


def gt(field_name: str, value: Any, inclusive: bool = False) -> str:
  boundary = "[" if inclusive else "{"
  return f"{field_name}:{boundary}{_quote_if_needed(value)} TO *]"


def lt(field_name: str, value: Any, inclusive: bool = False) -> str:
  boundary = "]" if inclusive else "}"
  return f"{field_name}:[* TO {_quote_if_needed(value)}{boundary}"


def between(field_name: str, start: Any, end: Any, include_start: bool = True, include_end: bool = True) -> str:
  left = "[" if include_start else "{"
  right = "]" if include_end else "}"
  return f"{field_name}:{left}{_quote_if_needed(start)} TO {_quote_if_needed(end)}{right}"


def in_filters(field_name: str, values: Iterable[Any]) -> str:
  vals = [ _quote_if_needed(v) for v in list(values) ]
  if not vals:
    return "*:*"  # empty means match all; caller can AND with others
  return f"{field_name}:(" + " OR ".join(vals) + ")"


def and_filters(*parts: str) -> str:
  cleaned = [p for p in parts if p]
  if not cleaned:
    return ""
  if len(cleaned) == 1:
    return cleaned[0]
  return "(" + " AND ".join(cleaned) + ")"


def or_filters(*parts: str) -> str:
  cleaned = [p for p in parts if p]
  if not cleaned:
    return ""
  if len(cleaned) == 1:
    return cleaned[0]
  return "(" + " OR ".join(cleaned) + ")"


def fl(fields: Sequence[str] | None) -> str:
  return ",".join(fields) if fields else ""


def build_params(
  *,
  q_expr: str | None = None,
  fq_list: List[str] | None = None,
  fields: Sequence[str] | None = None,
  sort: str | None = None,
  rows: int | None = None,
  cursor_mark: str | None = None,
  def_type: str | None = None,
  extra: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
  #params: Dict[str, Any] = {"wt": "json"}
  params: Dict[str, Any] = {}
  if q_expr:
    params["q"] = q(q_expr)
  else:
    params["q"] = "*:*"
  if fq_list:
    # multiple fq supported by Solr; pass as list so httpx encodes repeats
    params["fq"] = list(fq_list)
  if fields:
    params["fl"] = fl(fields)
  if sort:
    params["sort"] = sort
  if isinstance(rows, int):
    params["rows"] = rows
  if cursor_mark is not None:
    params["cursorMark"] = cursor_mark
  if def_type:
    params["defType"] = def_type
  if extra:
    params.update(extra)
  return params


qb = SimpleNamespace(
  q=q,
  eq=eq,
  gt=gt,
  lt=lt,
  between=between,
  in_=in_filters,
  and_=and_filters,
  or_=or_filters,
  fl=fl,
  build_params=build_params,
)


__all__ = [
  "qb",
  "q",
  "eq",
  "gt",
  "lt",
  "between",
  "in_filters",
  "and_filters",
  "or_filters",
  "fl",
  "build_params",
]


