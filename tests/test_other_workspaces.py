"""Other users' workspaces: discovering them and reading their groups.

2026-10-26: shared and public folders could be browsed by full path, but
nothing listed them (``workspace_browse`` with no path is the user's home),
and ``get_group_ids`` only looked in the user's own Genome Groups folder.
"""
import json

import pytest

from bvbrc_mcp.clients import group_functions as gf
from bvbrc_mcp.tools import workspace as ws

ME = "me@patricbrc.org"
HEADERS = {"Authorization": f"un={ME}|tokenid=x|sig=y"}


def _top(name, owner, user_perm, global_perm, ctime="2024-01-01T00:00:00Z"):
    return [name, "folder", "/", ctime, "id-" + name, owner, 0, {}, {}, user_perm, global_perm, ""]


class FakeApi:
    def __init__(self, ls=None, objects=None):
        self.ls, self.objects, self.calls = ls or [], objects or {}, []

    async def acall(self, method, params, request_id=1, token=None):
        self.calls.append((method, params))
        if method == "Workspace.ls":
            return [{"/": self.ls}]
        if method == "Workspace.list_permissions":
            return [{o: [["someone@patricbrc.org", "r"]] + ([] if "carol" in o else [[ME, "w" if "bob" in o else "r"]])
                     for o in params["objects"]}]
        if method == "Workspace.get":
            path = params["objects"][0]
            if path not in self.objects:
                raise RuntimeError("_ERROR_Object not found_ERROR_")
            typ, data = self.objects[path]
            parent, name = path.rsplit("/", 1)
            return [[[[name, typ, parent + "/", "t", "id", "allan@patricbrc.org", 1, {}, {}], json.dumps(data)]]]
        raise AssertionError(method)


ROOT = [
    _top("home", ME, "o", "n"),
    _top("AllanShare", "allan@patricbrc.org", "r", "n"),
    _top("TeamData", "bob@patricbrc.org", "w", "n"),
    _top("Scratch", "carol@patricbrc.org", "w", "w"),
    _top("2023-NVDDTHD", "ntvy@patricbrc.org", "r", "r"),
    _top("BV-BRC Workshop", "ARWattam@patricbrc.org", "r", "r"),
    _top("MyPublic", ME, "o", "r"),
]


@pytest.fixture
def api(monkeypatch):
    fake = FakeApi(ls=ROOT)
    monkeypatch.setattr(ws, "_get_api", lambda config=None: fake)
    return fake


async def test_shared_lists_other_users_private_workspaces(api):
    r = await ws.workspace_browse(scope="shared", headers=HEADERS)
    assert [w["path"] for w in r["items"]] == [
        "/allan@patricbrc.org/AllanShare", "/carol@patricbrc.org/Scratch", "/bob@patricbrc.org/TeamData"]
    # From list_permissions: the ls tuple's own field says "n" for a share.
    # A workspace open to every user (global "w") is not shared by name.
    assert [w["your_permission"] for w in r["items"]] == ["read", "write", "write"]
    assert r["items"][1]["open_to_all_users"] is True and "_global" not in r["items"][0]
    assert r["items"][0]["workspace_browser_url"].endswith("/workspace/allan@patricbrc.org/AllanShare")
    assert [m for m, _ in api.calls] == ["Workspace.ls", "Workspace.list_permissions"]


async def test_public_excludes_own_and_filters_by_name_or_owner(api):
    r = await ws.workspace_browse(scope="public", headers=HEADERS)
    assert {w["name"] for w in r["items"]} == {"2023-NVDDTHD", "BV-BRC Workshop"}
    r = await ws.workspace_browse(scope="public", name_contains=["ntvy"], headers=HEADERS)
    assert [w["name"] for w in r["items"]] == ["2023-NVDDTHD"]
    r = await ws.workspace_browse(scope="public", name_contains=["workshop"], headers=HEADERS)
    assert [w["owner"] for w in r["items"]] == ["ARWattam@patricbrc.org"]


async def test_cap_says_how_to_narrow(api):
    r = await ws.workspace_browse(scope="public", num_results=1, headers=HEADERS)
    assert r["count"] == 1 and r["matched"] == 2 and r["truncated"] is True
    assert "name_contains" in r["hint"]


async def test_bad_scope_is_refused(api):
    r = await ws.workspace_browse(scope="everything", headers=HEADERS)
    assert r["errorType"] == "INVALID_PARAMETERS" and api.calls == []


GROUP = "/allan@patricbrc.org/AllanShare/Streptococcus public"
OBJECTS = {
    GROUP: ("genome_group", {"id_list": {"genome_id": ["1313.1", "1313.2"]}}),
    "/allan@patricbrc.org/AllanShare/notes.txt": ("txt", {}),
}


@pytest.mark.parametrize("ref", [GROUP, "/public" + GROUP, GROUP + "/"])
async def test_group_by_full_path_is_read_directly(ref):
    api = FakeApi(objects=OBJECTS)
    r = await gf.get_group_ids(api, ref, "genome_group", "un=me@patricbrc.org|sig=x")
    assert r["genome_ids"] == ["1313.1", "1313.2"] and r["count"] == 2
    assert r["path"] == GROUP and r["name"] == "Streptococcus public" and r["match_type"] == "path"
    assert [m for m, _ in api.calls] == ["Workspace.get"]


async def test_group_path_missing_or_not_a_group():
    api = FakeApi(objects=OBJECTS)
    r = await gf.get_group_ids(api, "/allan@patricbrc.org/AllanShare/nope", "genome_group", "t")
    assert r["errorType"] == "NOT_FOUND" and "nope" in r["error"]
    r = await gf.get_group_ids(api, "/allan@patricbrc.org/AllanShare/notes.txt", "genome_group", "t")
    assert r["errorType"] == "WRONG_TYPE"
    r = await gf.get_group_ids(api, GROUP, "feature_group", "t")
    assert r["errorType"] == "WRONG_TYPE"
