"""The real ``workspace_browse`` output, fed to the tools that read it.

2026-10-27: the result was flattened (no ``{"result": ...}`` envelope).
``list_samples`` and ``rerun_jobs`` read it with ``.get("result") or {}``,
which on a flat result means "no items": no samples, no job results, no
error. Their own tests mock ``workspace_browse``, so a fake in the old shape
would have kept them green. These tests run the real tool against a fake
Workspace service instead.
"""
from bvbrc_mcp.tools import rerun, samples
from bvbrc_mcp.tools import workspace as ws

ME = "me@patricbrc.org"
HEADERS = {"Authorization": f"un={ME}|tokenid=x|sig=y"}
READS = f"/{ME}/home/reads"
JOBS = f"/{ME}/home/jobs"


def _item(name, parent, typ="reads"):
    return [name, typ, parent, "2026-01-01T00:00:00Z", "id-" + name, ME, 1, {}, {}, "o", "n", ""]


class FakeWorkspace:
    def __init__(self, folders):
        self.folders = folders

    async def acall(self, method, params, request_id=1, token=None):
        if method == "Workspace.get":
            path = params["objects"][0]
            parent, name = path.rsplit("/", 1)
            return [[[[name, "folder", parent + "/", "t", "id", ME, 0, {}, {"is_folder": 1}, "o", "n", ""], ""]]]
        if method == "Workspace.ls":
            root = params["paths"][0]
            items = self.folders.get(root, [])
            types = (params.get("query") or {}).get("type")
            return [{root: [i for i in items if not types or i[1] in types]}]
        raise AssertionError(method)


def _install(monkeypatch, folders):
    monkeypatch.setattr(ws, "_get_api", lambda config=None: FakeWorkspace(folders))


async def test_list_samples_reads_the_real_listing(monkeypatch):
    _install(monkeypatch, {READS: [_item("s1_R1.fastq", READS + "/"), _item("s1_R2.fastq", READS + "/"),
                                   _item("s2.fastq", READS + "/")]})
    r = await samples.list_samples(path=READS, headers=HEADERS)
    assert r["sample_count"] == 2 and len(r["paired"]) == 1 and len(r["single"]) == 1
    assert r["folder"] == READS


async def test_rerun_reads_the_real_search(monkeypatch):
    _install(monkeypatch, {JOBS: [_item("asm1", JOBS + "/", "job_result"), _item("tree", JOBS + "/sub/", "job_result")]})
    r = await rerun._job_results(JOBS, None, HEADERS)
    assert sorted(i["name"] for i in r["items"]) == ["asm1", "tree"] and r["folder"] == JOBS
