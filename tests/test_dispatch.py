"""bvbrc_mcp.dispatch: refusals, error wrapping, context and headers."""

import asyncio

from bvbrc_mcp import TOOLS, TOOLS_BY_NAME, SIDE_EFFECT_TOOLS, ToolContext, dispatch
from bvbrc_mcp.results import is_invalid_arguments_result
from bvbrc_mcp.tools.schemas import ALL_TOOL_SCHEMAS


def _recorder(calls, result=None):
    async def tool(**kwargs):
        calls.append(kwargs)
        return result or {"ok": True}
    return tool


async def test_unparseable_arguments_are_refused_without_calling():
    calls = []
    r = await dispatch("probe_data", {"_unparseable_arguments": "{bad"}, ToolContext(),
                       dispatch_table={"probe_data": _recorder(calls)})
    assert calls == []
    assert is_invalid_arguments_result(r)
    assert r["received"] == "{bad"
    assert "Nothing was submitted or changed" in r["error"]


async def test_a_normal_call_passes_context_and_token_headers():
    calls = []
    ctx = ToolContext(bvbrc_auth_token="un=x|sig=y")
    r = await dispatch("probe_data", {"x": 1}, ctx, dispatch_table={"probe_data": _recorder(calls)})
    assert r == {"ok": True}
    assert calls == [{"x": 1, "config": ctx, "headers": {"Authorization": "un=x|sig=y"}}]
    assert not is_invalid_arguments_result(r)


async def test_no_token_means_no_headers():
    calls = []
    await dispatch("probe_data", {}, ToolContext(), dispatch_table={"probe_data": _recorder(calls)})
    assert "headers" not in calls[0]


async def test_unknown_tool():
    r = await dispatch("nope", {}, ToolContext())
    assert r["error"] == "Unknown tool: 'nope'"
    assert "search_data" in r["available_tools"]


async def test_exceptions_and_bad_arguments_become_error_dicts():
    async def boom(**kwargs):
        raise RuntimeError("down")

    async def strict(*, collection, config=None, headers=None):
        return {}

    r = await dispatch("probe_data", {}, ToolContext(), dispatch_table={"probe_data": boom})
    assert r["error"] == "Tool 'probe_data' failed: RuntimeError: down"
    r = await dispatch("probe_data", {"nope": 1}, ToolContext(), dispatch_table={"probe_data": strict})
    assert r["error"].startswith("Invalid arguments for tool 'probe_data'")
    assert r["arguments"] == {"nope": 1}


async def test_timeout_is_reported():
    async def slow(**kwargs):
        await asyncio.sleep(1)

    r = await dispatch("probe_data", {}, ToolContext(), timeout_seconds=0.01,
                       dispatch_table={"probe_data": slow})
    assert r["error"].startswith("Tool 'probe_data' timed out")


def test_tool_list_matches_the_schemas():
    names = [s["function"]["name"] for s in ALL_TOOL_SCHEMAS]
    assert [t.name for t in TOOLS] == names
    assert len(names) == len(set(names)) == 29
    assert set(TOOLS_BY_NAME) == set(names)
    assert {t.name for t in TOOLS if t.side_effect} == SIDE_EFFECT_TOOLS == {
        "submit_gowe_job", "create_group", "edit_group"}
    for t in TOOLS:
        assert t.parameters.get("type") == "object"
        assert t.description
