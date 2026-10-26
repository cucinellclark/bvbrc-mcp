"""The MCP servers: tool list, calls through dispatch, OAuth audience."""

import json
from urllib.parse import urlparse

import pytest
from fastmcp import Client, FastMCP
from starlette.testclient import TestClient

from bvbrc_mcp import TOOLS
from bvbrc_mcp.registry import TOOL_DISPATCH
from bvbrc_mcp.server.mcp_tools import MCP_NOTES, PREFIX, register_tools
from bvbrc_mcp.settings import Settings, get_settings


def _server(settings=None):
    mcp = FastMCP("test")
    register_tools(mcp, token_provider=None, settings=settings or Settings(gowe_url="http://gowe.test"))
    return mcp


@pytest.fixture
def recorded(monkeypatch):
    calls = []

    def recorder(name):
        async def fn(config=None, headers=None, **kwargs):
            calls.append({"tool": name, "args": kwargs, "config": config, "headers": headers})
            return {"ok": True, "tool": name}
        return fn

    for name in list(TOOL_DISPATCH):
        monkeypatch.setitem(TOOL_DISPATCH, name, recorder(name))
    return calls


async def test_every_tool_is_listed_with_its_schema():
    async with Client(_server()) as client:
        listed = {t.name: t for t in await client.list_tools()}
    assert set(listed) == {PREFIX + t.name for t in TOOLS}
    for t in TOOLS:
        mt = listed[PREFIX + t.name]
        props = dict(mt.inputSchema["properties"])
        assert props.pop("bvbrc_token")["type"] == "string"
        assert props == t.parameters.get("properties", {})
        assert mt.inputSchema.get("required", []) == t.parameters.get("required", [])
        assert mt.description.startswith(t.description)
        if t.name in MCP_NOTES:
            assert mt.description.endswith(MCP_NOTES[t.name])


async def test_a_call_runs_with_the_token_and_server_settings(recorded):
    async with Client(_server()) as client:
        r = await client.call_tool("agent_search_data",
                                   {"collection": "genome", "query": "*", "bvbrc_token": "un=x|sig=y"})
    assert r.structured_content == {"ok": True, "tool": "search_data"}
    assert json.loads(r.content[0].text) == {"ok": True, "tool": "search_data"}
    (call,) = recorded
    assert call["args"] == {"collection": "genome", "query": "*"}
    assert call["config"].bvbrc_auth_token == "un=x|sig=y"
    assert call["config"].gowe_url == "http://gowe.test"
    assert call["headers"] == {"Authorization": "un=x|sig=y"}


@pytest.mark.parametrize("tool", ["submit_gowe_job", "create_group", "edit_group"])
async def test_side_effecting_tools_run_when_called(recorded, tool):
    async with Client(_server()) as client:
        r = await client.call_tool(PREFIX + tool, {})
    assert r.structured_content == {"ok": True, "tool": tool}


async def test_tracebacks_never_reach_the_client(monkeypatch):
    async def boom(**kwargs):
        raise RuntimeError("secret internals")

    monkeypatch.setitem(TOOL_DISPATCH, "probe_data", boom)
    async with Client(_server()) as client:
        r = await client.call_tool("agent_probe_data", {"collection": "genome", "keywords": "x"},
                                   raise_on_error=False)
    assert r.structured_content["error"] == "Tool 'probe_data' failed: RuntimeError: secret internals"
    assert "traceback" not in r.structured_content


@pytest.mark.parametrize("public_url", ["https://www.bv-brc.org/mcp", "https://dev-9.bv-brc.org"])
def test_token_audience_equals_the_advertised_resource(monkeypatch, public_url):
    from bvbrc_mcp.server.http import create_server

    settings = Settings(public_url=public_url, jwt_signing_key="k" * 32)
    mcp = create_server(settings)
    app = mcp.http_app(path=settings.mcp_path)
    prefix = urlparse(public_url).path.rstrip("/")
    with TestClient(app) as c:
        meta = c.get(f"/.well-known/oauth-protected-resource{prefix}/").json()
        unauthenticated = c.post(settings.mcp_path, json={})
    assert meta["resource"] == mcp.auth._audience == public_url.rstrip("/") + "/"
    assert unauthenticated.status_code == 401


def test_settings_file_and_environment(tmp_path, monkeypatch):
    cfg = tmp_path / "c.json"
    cfg.write_text(json.dumps({"gowe_url": "http://localhost:7000", "port": 9000,
                               "helpdesk": {"ragstack_collection": "other"}}))
    monkeypatch.setenv("BVBRC_MCP_CONFIG", str(cfg))
    monkeypatch.setenv("BVBRC_MCP_PORT", "9100")
    get_settings.cache_clear()
    try:
        s = get_settings()
        assert (s.gowe_url, s.port) == ("http://localhost:7000", 9100)
        assert s.helpdesk["ragstack_collection"] == "other"
        assert s.helpdesk["ragstack_retrieval_mode"] == "vector"   # default kept
        assert s.tool_context("t").gowe_url == "http://localhost:7000"
        cfg.write_text(json.dumps({"gowe": {"url": "x"}}))
        get_settings.cache_clear()
        with pytest.raises(ValueError, match="unknown settings"):
            get_settings()
    finally:
        get_settings.cache_clear()
