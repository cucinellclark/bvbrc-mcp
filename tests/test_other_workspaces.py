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
    assert r["count"] == 1 and r["total"] == 2 and r["truncated"] is True
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


# ── Part 3 (2026-10-27): searching inside shared workspaces, cache ────────
# "Do any shared workspaces have Streptococcus data?" took 20 calls and 33 s:
# one recursive search per shared workspace, and the top-level listing was
# fetched again on every scope call.

class SearchingApi(FakeApi):
    """Top-level listing from ROOT; a recursive ls of a root returns its files."""

    def __init__(self, trees, broken=()):
        super().__init__(ls=ROOT)
        self.trees, self.broken = trees, set(broken)

    async def acall(self, method, params, request_id=1, token=None):
        if method == "Workspace.ls" and params["paths"] != ["/"]:
            self.calls.append((method, params))
            root = params["paths"][0]
            if root in self.broken:
                raise RuntimeError("_ERROR_User lacks permission to " + root)
            types = (params.get("query") or {}).get("type")
            return [{root: [i for i in self.trees.get(root, []) if not types or i[1] in types]}]
        return await super().acall(method, params, request_id, token)


def _file(name, parent, typ="genome_group"):
    return [name, typ, parent, "2025-02-01T00:00:00Z", "id-" + name, "x", 1, {}, {}, "r", "n", ""]


TREES = {
    "/allan@patricbrc.org/AllanShare": [_file("Streptococcus public", "/allan@patricbrc.org/AllanShare/")],
    "/bob@patricbrc.org/TeamData": [_file("strep.fasta", "/bob@patricbrc.org/TeamData/seqs/", "contigs"),
                                    _file("strep_contigs.fa", "/bob@patricbrc.org/TeamData/.asm1/", "contigs")],
}


async def test_shared_search_looks_inside_every_shared_workspace(monkeypatch):
    fake = SearchingApi(TREES)
    monkeypatch.setattr(ws, "_get_api", lambda config=None: fake)
    r = await ws.workspace_browse(scope="shared", name_contains=["strep"], recursive=True, headers=HEADERS)
    inner = r
    assert sorted(i["name"] for i in inner["items"]) == ["Streptococcus public", "strep.fasta"]
    assert inner["summary"]["by_root"] == {"/allan@patricbrc.org/AllanShare": 1, "/bob@patricbrc.org/TeamData": 1}
    assert inner["hidden_in_job_outputs"] == 1 and inner["scope"] == "shared"
    assert "3 workspaces shared with you" in inner["note"]
    searched = sorted(p["paths"][0] for m, p in fake.calls if m == "Workspace.ls" and p["paths"] != ["/"])
    assert searched == ["/allan@patricbrc.org/AllanShare", "/bob@patricbrc.org/TeamData", "/carol@patricbrc.org/Scratch"]
    assert "workspace_browser_url" not in r


async def test_one_unreadable_workspace_does_not_sink_the_search(monkeypatch):
    fake = SearchingApi(TREES, broken={"/carol@patricbrc.org/Scratch"})
    monkeypatch.setattr(ws, "_get_api", lambda config=None: fake)
    inner = await ws.workspace_browse(scope="shared", workspace_types=["genome_group"], headers=HEADERS)
    assert [i["name"] for i in inner["items"]] == ["Streptococcus public"]
    assert inner["unreadable"][0]["path"] == "/carol@patricbrc.org/Scratch"


async def test_shared_without_recursive_still_lists_workspaces_by_name(monkeypatch):
    fake = SearchingApi(TREES)
    monkeypatch.setattr(ws, "_get_api", lambda config=None: fake)
    r = await ws.workspace_browse(scope="shared", name_contains=["team"], headers=HEADERS)
    assert [w["name"] for w in r["items"]] == ["TeamData"]


async def test_public_contents_are_never_searched(api):
    r = await ws.workspace_browse(scope="public", recursive=True, name_contains=["flu"], headers=HEADERS)
    assert r["errorType"] == "INVALID_PARAMETERS" and "by name" in r["error"] and api.calls == []


async def test_several_paths_in_one_call(monkeypatch):
    fake = SearchingApi(TREES)
    monkeypatch.setattr(ws, "_get_api", lambda config=None: fake)
    inner = await ws.workspace_browse(paths=list(TREES), recursive=True, headers=HEADERS)
    assert inner["paths"] == list(TREES) and inner["total"] == 2
    assert {i["path"] for i in inner["items"]} == {"/allan@patricbrc.org/AllanShare/Streptococcus public",
                                                  "/bob@patricbrc.org/TeamData/seqs/strep.fasta"}


async def test_top_level_listing_and_permissions_are_cached(api):
    await ws.workspace_browse(scope="shared", headers=HEADERS)
    await ws.workspace_browse(scope="public", name_contains=["work"], headers=HEADERS)
    await ws.workspace_browse(scope="shared", headers=HEADERS)
    assert [m for m, _ in api.calls] == ["Workspace.ls", "Workspace.list_permissions"]
    ws.clear_workspace_caches()
    await ws.workspace_browse(scope="public", headers=HEADERS)
    assert [m for m, _ in api.calls].count("Workspace.ls") == 2


async def test_scope_names_take_name_match_and_dates(api):
    r = await ws.workspace_browse(scope="public", name_contains=["workshop", "nvddthd"], name_match="any", headers=HEADERS)
    assert {w["name"] for w in r["items"]} == {"2023-NVDDTHD", "BV-BRC Workshop"}
    r = await ws.workspace_browse(scope="public", created_after="2025-01-01", headers=HEADERS)
    assert r["items"] == []
