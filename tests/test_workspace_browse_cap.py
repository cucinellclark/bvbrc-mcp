"""``workspace_browse`` results: cap, paging, summary, explicit recursive.

2026-10-27: ``Workspace.ls`` ignores ``limit`` and ``offset``, so
``num_results`` capped nothing (5 asked, 109 returned; one listing returned
11,215 items). Every result also carried a ``ui_grid`` copy of the raw
tuples (82 % of the bytes, read by nothing), and recursive searches were
mostly files inside hidden job output folders (770 of 879).

Part 2 (same day): whether a call listed one folder or searched everything
under it depended on whether a filter was present, a capped result did not
say it was capped, and there was no page 2.
"""
import json

import pytest

from bvbrc_mcp.tools import workspace as ws

ME = "me@patricbrc.org"
HEADERS = {"Authorization": f"un={ME}|tokenid=x|sig=y"}
HOME = f"/{ME}/home"


def _item(name, parent, typ="reads", ctime="2024-01-01T00:00:00Z", size=1):
    return [name, typ, parent, ctime, "id-" + name, ME, size, {}, {}, "o", "n", ""]


class FakeApi:
    """``Workspace.ls`` returns everything (as the real service does).

    *listing* (optional) is what a non-recursive ``ls`` returns; without it
    both kinds of call return *items*.
    """

    def __init__(self, items, listing=None):
        self.items, self.listing, self.calls = items, listing, []

    async def acall(self, method, params, request_id=1, token=None):
        self.calls.append((method, params))
        if method == "Workspace.get":
            path = params["objects"][0]
            parent, name = path.rstrip("/").rsplit("/", 1)
            return [[[[name, "folder", parent + "/", "t", "id", ME, 0, {}, {"is_folder": 1}, "o", "n", ""], ""]]]
        if method == "Workspace.ls":
            flat = self.listing is not None and not params.get("recursive")
            return [{params["paths"][0]: self.listing if flat else self.items}]
        raise AssertionError(method)


@pytest.fixture
def use_api(monkeypatch):
    def install(items, listing=None):
        fake = FakeApi(items, listing)
        monkeypatch.setattr(ws, "_get_api", lambda config=None: fake)
        return fake
    return install


async def test_listing_is_capped_and_says_total(use_api):
    use_api([_item(f"f{i:03d}.fastq", HOME + "/") for i in range(300)])
    r = await ws.workspace_browse(num_results=50, headers=HEADERS)
    assert r["count"] == 50 and len(r["items"]) == 50
    assert r["total"] == 300 and r["truncated"] is True
    assert "1-50 of 300" in r["hint"] and r["next_offset"] == 50


async def test_small_listing_is_not_truncated(use_api):
    use_api([_item("a.fastq", HOME + "/"), _item("b.fastq", HOME + "/")])
    r = await ws.workspace_browse(headers=HEADERS)
    assert r["count"] == r["total"] == 2 and r["truncated"] is False
    assert "hint" not in r


async def test_cap_applies_after_sorting(use_api):
    use_api([
        _item("old", HOME + "/", ctime="2020-01-01T00:00:00Z"),
        _item("new", HOME + "/", ctime="2026-01-01T00:00:00Z"),
        _item("mid", HOME + "/", ctime="2023-01-01T00:00:00Z"),
    ])
    r = (await ws.workspace_browse(sort_by="creation_time", sort_order="desc",
                                   num_results=2, headers=HEADERS))
    assert [i["name"] for i in r["items"]] == ["new", "mid"]
    r = await ws.workspace_browse(sort_by="size", num_results=3, headers=HEADERS)
    assert r["total"] == 3


async def test_no_ui_grid_or_call_envelope(use_api):
    use_api([_item(f"f{i}.fastq", HOME + "/") for i in range(5)])
    for kwargs in ({}, {"file_extensions": ["fastq"]}):
        r = await ws.workspace_browse(headers=HEADERS, **kwargs)
        text = json.dumps(r)
        assert "ui_grid" not in text and "call" not in r


SEARCH_TREE = [
    _item("a.fastq", HOME + "/reads/"),
    _item("b.fastq", HOME + "/.job1/"),
    _item("c.fastq", HOME + "/Assembly/.MyAsm/sub/"),
    _item("d.fastq", HOME + "/.chats/abc/uploaded_files/"),
]


async def test_search_leaves_out_job_outputs_and_counts_them(use_api):
    use_api(SEARCH_TREE)
    r = await ws.workspace_browse(file_extensions=["fastq"], headers=HEADERS)
    assert [i["name"] for i in r["items"]] == ["a.fastq"]
    assert r["total"] == 1 and r["hidden_in_job_outputs"] == 3
    assert "include_job_outputs" in r["hint"]


async def test_include_job_outputs_finds_everything(use_api):
    use_api(SEARCH_TREE)
    r = (await ws.workspace_browse(file_extensions=["fastq"], include_job_outputs=True,
                                   headers=HEADERS))
    assert len(r["items"]) == 4 and "hidden_in_job_outputs" not in r


async def test_searching_inside_a_job_output_folder_keeps_its_files(use_api):
    # The user asked for this folder, so its own dot-name does not hide it;
    # only dot-folders below the search root do.
    root = HOME + "/Assembly/.MyAsm"
    use_api([_item("contigs.fasta", root + "/"), _item("x.fasta", root + "/.tmp/")])
    r = await ws.workspace_browse(path=root, file_extensions=["fasta"], headers=HEADERS)
    assert [i["name"] for i in r["items"]] == ["contigs.fasta"]
    assert r["hidden_in_job_outputs"] == 1


async def test_service_is_not_asked_for_a_limit(use_api):
    fake = use_api([_item("a.fastq", HOME + "/")])
    await ws.workspace_browse(file_extensions=["fastq"], num_results=5, headers=HEADERS)
    ls = [p for m, p in fake.calls if m == "Workspace.ls"]
    assert ls and all("limit" not in p for p in ls)


FOLDER = [_item("a.fastq", HOME + "/"), _item("b.fasta", HOME + "/", typ="contigs"),
          _item("reads", HOME + "/", typ="folder")]
UNDER = FOLDER + [_item("deep.fastq", HOME + "/reads/"), _item("deeper.fastq", HOME + "/reads/x/")]


async def test_filters_on_a_plain_listing_stay_in_that_folder(use_api):
    fake = use_api(UNDER, listing=FOLDER)
    r = await ws.workspace_browse(file_extensions=["fastq"], recursive=False, headers=HEADERS)
    assert [i["name"] for i in r["items"]] == ["a.fastq"] and r["result_type"] == "list_result"
    ls = [p for m, p in fake.calls if m == "Workspace.ls"]
    assert len(ls) == 1 and ls[0]["recursive"] is False and "query" not in ls[0]
    r = await ws.workspace_browse(workspace_types=["contigs"], recursive=False, headers=HEADERS)
    assert [i["name"] for i in r["items"]] == ["b.fasta"]
    r = await ws.workspace_browse(name_contains=["A."], recursive=False, headers=HEADERS)
    assert [i["name"] for i in r["items"]] == ["a.fastq"]


async def test_filters_without_recursive_still_search_for_now(use_api):
    use_api(UNDER, listing=FOLDER)
    r = await ws.workspace_browse(file_extensions=["fastq"], headers=HEADERS)
    assert r["result_type"] == "search_result" and r["total"] == len(UNDER)


async def test_recursive_without_filters_searches_everything(use_api):
    use_api(UNDER, listing=FOLDER)
    r = await ws.workspace_browse(recursive=True, headers=HEADERS)
    assert r["result_type"] == "search_result" and r["total"] == 5


async def test_max_depth_limits_the_search(use_api):
    use_api(UNDER)
    names = lambda r: sorted(i["name"] for i in r["items"])
    assert names(await ws.workspace_browse(recursive=True, max_depth=0, headers=HEADERS)) == ["a.fastq", "b.fasta", "reads"]
    assert "deep.fastq" in names(await ws.workspace_browse(recursive=True, max_depth=1, headers=HEADERS))
    assert "deeper.fastq" not in names(await ws.workspace_browse(recursive=True, max_depth=1, headers=HEADERS))


async def test_pages_follow_next_offset_to_the_end(use_api):
    use_api([_item(f"f{i:03d}.fastq", HOME + "/") for i in range(120)])
    seen, offset = [], 0
    while offset is not None:
        r = await ws.workspace_browse(num_results=50, offset=offset, sort_by="name", headers=HEADERS)
        assert r["offset"] == offset and r["total"] == 120
        seen += [i["name"] for i in r["items"]]
        offset = r.get("next_offset")
    assert seen == [f"f{i:03d}.fastq" for i in range(120)]
    assert r["count"] == 20 and "next_offset" not in r


async def test_summary_counts_everything_matched_not_just_the_page(use_api):
    items = ([_item(f"r{i}.fastq", HOME + "/Assembly/", size=10, ctime=f"2024-01-{i + 1:02d}T00:00:00Z") for i in range(8)]
             + [_item("t.txt", HOME + "/", typ="txt", size=5, ctime="2020-05-05T00:00:00Z")])
    use_api(items)
    r = await ws.workspace_browse(recursive=True, num_results=2, headers=HEADERS)
    s = r["summary"]
    assert s["by_type"] == {"reads": 8, "txt": 1} and s["total_size"] == 85
    assert s["oldest"].startswith("2020") and s["newest"].startswith("2024-01-08")
    assert s["by_folder"] == {"Assembly": 8, "(this folder)": 1}
    use_api(items, listing=items[-1:])
    r = await ws.workspace_browse(headers=HEADERS)
    assert "by_folder" not in r["summary"] and r["truncated"] is False


# ── Filter / sort review (2026-10-27) ─────────────────────────────────────
from bvbrc_mcp.clients import workspace_functions as wf  # noqa: E402


def test_name_terms_are_literal_and_combine_three_ways():
    import re
    def match(terms, mode, names):
        p = re.compile(wf.name_regex(terms, None, mode), re.I)
        return [n for n in names if p.search(n)]
    # Terms used to go to the service as regex: "+" and "(" broke them.
    assert match(["TanA+"], "all", ["TanA+ genomes", "TanAAA"]) == ["TanA+ genomes"]
    assert match(["sample (1)"], "all", ["sample (1).fa", "sample 1.fa"]) == ["sample (1).fa"]
    names = ["Avian_influenza_ref", "FLU-IRMA.sh", "H5N1_cattle", "ecoli"]
    assert match(["influenza", "flu", "h5n1"], "any", names) == names[:3]
    assert match(["influenza", "ref"], "all", names) == ["Avian_influenza_ref"]
    bac = ["Bacillus_group_1", "A Bacillus velezensis", "Lactobacillus iners", "Lactiplantibacillus"]
    assert match(["bacillus"], "word", bac) == bac[:2]
    assert wf.name_regex(None, ["fastq", ".fq"]) == r".*\.(?:fastq|fq)$"
    assert wf.name_regex(None, None) == ""


async def test_any_word_and_escaping_reach_the_service_query(use_api):
    fake = use_api([_item("a.fastq", HOME + "/")])
    await ws.workspace_browse(name_contains=["flu", "influenza"], name_match="any", recursive=True, headers=HEADERS)
    q = [p for m, p in fake.calls if m == "Workspace.ls"][-1]["query"]
    assert q == {"name": {"$regex": "(?=.*(?:flu|influenza))", "$options": "i"}}


async def test_name_match_applies_to_a_plain_listing_and_to_scope(use_api):
    use_api([], listing=[_item("Bacillus_group_1", HOME + "/"), _item("Lactobacillus", HOME + "/")])
    r = await ws.workspace_browse(name_contains=["bacillus"], name_match="word", recursive=False, headers=HEADERS)
    assert [i["name"] for i in r["items"]] == ["Bacillus_group_1"]


async def test_date_range_on_our_side(use_api):
    use_api([], listing=[_item("old", HOME + "/", ctime="2025-12-31T23:00:00Z"),
                         _item("oct", HOME + "/", ctime="2026-10-01T00:00:00Z"),
                         _item("new", HOME + "/", ctime="2026-10-27T10:00:00Z")])
    names = lambda r: sorted(i["name"] for i in r["items"])
    assert names(await ws.workspace_browse(created_after="2026-10-01", headers=HEADERS)) == ["new", "oct"]
    assert names(await ws.workspace_browse(created_after="2026-01-01", created_before="2026-10-27",
                                           headers=HEADERS)) == ["oct"]
    bad = await ws.workspace_browse(created_after="last week", headers=HEADERS)
    assert bad["errorType"] == "INVALID_PARAMETERS" and "YYYY" not in bad["error"] and "2026-10-01" in bad["error"]


async def test_default_order_folders_then_names_or_newest_first(use_api):
    items = [_item("b.txt", HOME + "/", ctime="2020-01-01T00:00:00Z"),
             _item("Zeta", HOME + "/", typ="folder", ctime="2021-01-01T00:00:00Z"),
             _item("a.txt", HOME + "/", ctime="2026-01-01T00:00:00Z"),
             _item("alpha", HOME + "/", typ="folder", ctime="2019-01-01T00:00:00Z")]
    use_api(items, listing=items)
    listed = (await ws.workspace_browse(headers=HEADERS))["items"]
    assert [i["name"] for i in listed] == ["alpha", "Zeta", "a.txt", "b.txt"]
    found = (await ws.workspace_browse(recursive=True, headers=HEADERS))["items"]
    assert [i["name"] for i in found] == ["a.txt", "Zeta", "b.txt", "alpha"]
