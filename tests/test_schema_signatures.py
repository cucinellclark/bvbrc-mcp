"""Every tool schema matches its function's parameters.

2026-10-27: removing two workspace_browse parameters from the schema also cut
``file_extensions`` and ``workspace_types``, which sat between them. The
prompts still told the model to use both, so it did; with no declared type
the tool-call parser passed ``["fastq", "fq"]`` through as the text
``"[\\"fastq\\", \\"fq\\"]"``, the tool read it a character at a time, and the
answer said "1 FASTQ file" (there are 53).
"""
import inspect

import pytest

from bvbrc_mcp.registry import TOOL_DISPATCH
from bvbrc_mcp.tools.schemas import ALL_TOOL_SCHEMAS

# Injected by the dispatcher, never sent by a model.
_INJECTED = {"config", "headers"}
# Function parameters deliberately not offered to the model.
_INTERNAL_ONLY = {
    "search_data": {"base_url"},
    "facet_query": {"base_url"},
    "probe_data": {"base_url"},
    "read_file_preview": {"allow_binary"},
    "summarize_file": {"delimiter"},
}


def _function_params(fn):
    return {name for name, p in inspect.signature(fn).parameters.items()
            if p.kind not in (p.VAR_KEYWORD, p.VAR_POSITIONAL) and name not in _INJECTED}


@pytest.mark.parametrize("schema", ALL_TOOL_SCHEMAS, ids=lambda s: s["function"]["name"])
def test_schema_and_function_agree(schema):
    name = schema["function"]["name"]
    declared = set(schema["function"]["parameters"].get("properties") or {})
    accepted = _function_params(TOOL_DISPATCH[name])
    assert declared - accepted == set(), f"{name}: schema offers parameters the function does not take"
    assert accepted - declared == _INTERNAL_ONLY.get(name, set()), (
        f"{name}: the function takes parameters the schema does not declare "
        "(add them to the schema, or to _INTERNAL_ONLY if the model must not see them)"
    )
