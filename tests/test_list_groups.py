"""``list_groups``: names once, a total, job-output groups left out.

2026-10-27: 162 genome groups were listed three times (items, group_names,
message) plus a ``ui_grid`` copy, the loop cut the result, and the model
said "at least 158 groups (and there are more)".
"""
from bvbrc_mcp.tools import groups

ME = "me@patricbrc.org"
HEADERS = {"Authorization": f"un={ME}|tokenid=x|sig=y"}
HOME = f"/{ME}/home"


def _group(name, parent):
    return [name, "genome_group", parent, "2025-01-01T00:00:00Z", "id", ME, 1, {}, {}, "o", "n", ""]


class FakeApi:
    def __init__(self, items):
        self.items = items

    async def acall(self, method, params, request_id=1, token=None):
        assert method == "Workspace.ls" and params["query"] == {"type": ["genome_group"]}
        return [{params["paths"][0]: self.items}]


async def test_names_once_sorted_with_total_and_hidden(monkeypatch):
    items = [_group(f"g{i:03d}", f"{HOME}/Genome Groups/") for i in range(160)][::-1]
    items += [_group("elsewhere", f"{HOME}/Project/"), _group("in_job", f"{HOME}/Project/.tree_job/")]
    monkeypatch.setattr(groups, "_get_api", lambda config=None: FakeApi(items))
    r = await groups.list_groups("genome_group", headers=HEADERS)
    assert r["total"] == 161 and r["count"] == 161 and r["truncated"] is False
    # Default folder: the name; elsewhere: the full path (get_group_ids takes both).
    assert r["groups"][:3] == [f"{HOME}/Project/elsewhere", "g000", "g001"]  # sorted by name
    assert r["hidden_in_job_outputs"] == 1
    assert r["message"].startswith("161 genome groups.") and "g000" not in r["message"]
    assert "ui_grid" not in str(r)


async def test_long_lists_are_capped_and_say_so(monkeypatch):
    items = [_group(f"g{i:04d}", f"{HOME}/Genome Groups/") for i in range(groups.MAX_LISTED_GROUPS + 20)]
    monkeypatch.setattr(groups, "_get_api", lambda config=None: FakeApi(items))
    r = await groups.list_groups("genome_group", headers=HEADERS)
    assert r["count"] == groups.MAX_LISTED_GROUPS and r["total"] == groups.MAX_LISTED_GROUPS + 20
    assert r["truncated"] is True and "showing the first" in r["message"]


def test_the_chat_loop_keeps_a_full_list():
    import json
    payload = {"groups": [f"genome_group_name_{i:04d}" for i in range(groups.MAX_LISTED_GROUPS)],
               "count": groups.MAX_LISTED_GROUPS, "total": 999, "message": "x" * 200}
    assert len(json.dumps(payload, indent=2)) < 12_000
