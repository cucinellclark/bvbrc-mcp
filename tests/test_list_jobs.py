"""``list_jobs``: service names, compact jobs with their result location.

2026-10-27: AppService filters on the exact app id, and the schema's own
examples ('genome_assembly', 'rnaseq') returned 0 jobs with no error. The
chat agent answered "where are my assembly results" by browsing folders
named like "assembly" and found ~10 of 33; ``list_jobs`` with the app id has
all 88 jobs and each one's output path.
"""
from bvbrc_mcp.clients import service_functions
from bvbrc_mcp.tools import jobs

HEADERS = {"Authorization": "un=me@patricbrc.org|tokenid=x|sig=y"}


def _task(i, app, status="completed", **params):
    p = {"output_path": "/me@patricbrc.org/home/chats/s1", "output_file": f"run{i}",
         "_preflight": {"cpu": 12}, **params}
    return {"id": i, "app": app, "application_name": app, "status": status, "submit_time": "2026-10-01T00:00:00Z",
            "parameters": p, "user_id": "me@patricbrc.org", "workspace": None, "storage_location": ""}


class FakeAppService:
    def __init__(self, tasks):
        self.tasks, self.filters = tasks, []

    async def acall(self, method, params, request_id=None, token=None):
        assert method == "AppService.enumerate_tasks_filtered"
        offset, limit, flt = params
        self.filters.append(flt)
        hits = [t for t in self.tasks if not flt.get("app") or t["app"] == flt["app"]]
        return [hits[offset:offset + limit], len(hits)]


def _install(monkeypatch, tasks):
    fake = FakeAppService(tasks)
    monkeypatch.setattr(service_functions, "_api", fake, raising=False)
    return fake


def test_common_names_and_partial_names_resolve_to_app_ids():
    assert jobs.resolve_service("genome_assembly") == ["GenomeAssembly2"]
    assert jobs.resolve_service("Genome Assembly") == ["GenomeAssembly2"]
    assert jobs.resolve_service("rnaseq") == ["RNASeq"]
    assert jobs.resolve_service("blast") == ["Homology"]
    assert jobs.resolve_service("TreeSort") == ["TreeSort"]  # not in service_mapping.json
    assert jobs.resolve_service("influenza_ha_subtype_conversion") == ["HASubtypeNumberingConversion"]
    assert jobs.resolve_service("assembly") == ["GenomeAssembly2", "SARS2Assembly", "ViralAssembly"]
    assert jobs.resolve_service("no such thing") == []


async def test_a_common_name_finds_the_jobs(monkeypatch):
    fake = _install(monkeypatch, [_task(1, "GenomeAssembly2"), _task(2, "CodonTree")])
    r = await jobs.list_jobs(service="genome_assembly", headers=HEADERS)
    assert fake.filters[-1]["app"] == "GenomeAssembly2"
    assert r["total"] == 1 and r["service"] == "GenomeAssembly2" and r["service_requested"] == "genome_assembly"


async def test_a_partial_name_merges_the_services_it_fits(monkeypatch):
    # "tree" fits CodonTree, GeneTree and TreeSort: one page, newest first,
    # exactly what one combined query would return.
    tasks = []
    for i, (app, day) in enumerate([("CodonTree", 9), ("TreeSort", 8), ("GeneTree", 7), ("CodonTree", 6),
                                    ("TreeSort", 5), ("CodonTree", 4), ("GenomeAssembly2", 10)]):
        t = _task(i, app)
        t["submit_time"] = f"2026-10-{day:02d}T00:00:00Z"
        tasks.append(t)
    fake = _install(monkeypatch, tasks)
    r = await jobs.list_jobs(service="tree", limit=2, headers=HEADERS)
    assert sorted(f["app"] for f in fake.filters) == ["CodonTree", "GeneTree", "TreeSort"]
    assert [j["app"] for j in r["items"]] == ["CodonTree", "TreeSort"]
    assert r["total"] == 6 and r["total_by_service"] == {"CodonTree": 3, "GeneTree": 1, "TreeSort": 2}
    assert "3 services" in r["note"]
    page2 = await jobs.list_jobs(service="tree", limit=2, offset=2, headers=HEADERS)
    assert [j["submit_time"][8:10] for j in page2["items"]] == ["07", "06"]


async def test_a_name_that_fits_too_many_services_asks(monkeypatch):
    fake = _install(monkeypatch, [])
    monkeypatch.setattr(jobs, "MAX_MERGED_SERVICES", 2)
    r = await jobs.list_jobs(service="tree", headers=HEADERS)
    assert r["errorType"] == "AMBIGUOUS_SERVICE" and "TreeSort" in r["candidates"]
    assert fake.filters == []


async def test_an_unknown_name_with_no_jobs_says_so(monkeypatch):
    _install(monkeypatch, [_task(1, "GenomeAssembly2")])
    r = await jobs.list_jobs(service="Frobnicate", headers=HEADERS)
    assert r["total"] == 0 and "not a known service name" in r["note"] and "GenomeAssembly2" in r["note"]


async def test_jobs_are_compact_and_say_where_their_results_are(monkeypatch):
    _install(monkeypatch, [_task(7, "RNASeq", "failed", srr_ids=[f"SRR{i}" for i in range(9)], recipe="HTSeq-DESeq")])
    r = await jobs.list_jobs(headers=HEADERS)
    job = r["items"][0]
    assert job["result_path"] == "/me@patricbrc.org/home/chats/s1/run7"
    assert job["output_folder"] == "/me@patricbrc.org/home/chats/s1/.run7"
    assert job["inputs"]["srr_ids"][-1] == "… 4 more" and job["inputs"]["recipe"] == "HTSeq-DESeq"
    assert "_preflight" not in str(job) and "user_id" not in job and "parameters" not in job
    assert "ui_grid" not in r and "call" not in r
