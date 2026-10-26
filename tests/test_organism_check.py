"""CGA and Genome Annotation need a real organism and its NCBI taxonomy_id.

taxonomy_id is optional in the specs, but the website never submits without
it and the app does not cope: mshukla's CGA (scientific_name "metagenome", no
taxonomy_id) failed on "Cannot parse 'taxon_id:'"; marcnguy's CGA was sent
scientific_name "bau_sim" (a read-file prefix). See service_status.md.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest


from bvbrc_mcp.tools import gowe
from bvbrc_mcp.results import is_needs_user_input_result  # noqa: E402
from bvbrc_mcp.tools.gowe import _check_organism  # noqa: E402

CGA = "ComprehensiveGenomeAnalysis"


@pytest.mark.parametrize("inputs", [
    {"scientific_name": "Staphylococcus aureus", "taxonomy_id": 1280},
    {"scientific_name": "Streptococcus pneumoniae", "taxonomy_id": "1313"},
])
def test_real_organism_passes(inputs):
    assert _check_organism(CGA, inputs) is None
    assert _check_organism("GenomeAnnotation", inputs) is None


@pytest.mark.parametrize("inputs", [
    {},                                                          # nothing
    {"scientific_name": "bau_sim"},                              # marcnguy: no taxonomy_id
    {"scientific_name": "bau_sim.fastq", "taxonomy_id": 1280},   # filename
    {"scientific_name": "/u/home/reads/x", "taxonomy_id": 1280}, # path
    {"scientific_name": "SRR19542959", "taxonomy_id": 1280},     # accession
    {"scientific_name": "unknown", "taxonomy_id": 1280},
    {"scientific_name": "Escherichia coli", "taxonomy_id": 0},
    {"scientific_name": "Escherichia coli", "taxonomy_id": True},
    {"scientific_name": "Escherichia coli", "taxonomy_id": "562a"},
])
def test_unusable_organism_is_missing_organism(inputs):
    kind, reason = _check_organism(CGA, inputs)
    assert kind == "missing_organism"
    assert 'collection=\\"taxonomy\\"' in reason or 'collection="taxonomy"' in reason
    assert "taxon_rank:species" in reason


def test_metagenome_is_the_wrong_workflow():
    kind, reason = _check_organism(CGA, {"scientific_name": "metagenome"})
    assert kind == "wrong_workflow"
    assert "Metagenomic Binning" in reason


def test_other_workflows_are_not_checked():
    assert _check_organism("Variation", {}) is None
    assert _check_organism("Taxonomic Classification", {"scientific_name": "metagenome"}) is None


# --- submit_gowe_job ---------------------------------------------------------

@pytest.fixture
def client(monkeypatch):
    gowe._recent_submissions.clear()
    c = SimpleNamespace(create_submission=AsyncMock(return_value={"id": "sub_1", "state": "PENDING"}))
    monkeypatch.setattr(gowe, "_get_client", lambda config=None: c)
    yield c
    gowe._recent_submissions.clear()


def _cfg():
    return SimpleNamespace(bvbrc_auth_token="un=u@patricbrc.org|t", session_id="s1", workspace_path="/u@patricbrc.org/home")


@pytest.mark.asyncio
async def test_submit_blocks_cga_without_taxonomy_id(client, monkeypatch):
    monkeypatch.setattr(gowe, "_resolve_workflow_ref", AsyncMock(return_value=("wf_cga", None)))
    r = await gowe.submit_gowe_job(CGA, {"scientific_name": "metagenome", "output_path": "x"}, config=_cfg())
    client.create_submission.assert_not_awaited()
    assert is_needs_user_input_result(r) and r.get("wrong_workflow")


@pytest.mark.asyncio
async def test_submit_resolves_uuid_to_name_for_the_check(client, monkeypatch):
    """The model may pass wf_<uuid>; the name comes from the catalog lookup."""
    class _Catalog:
        async def list_workflows(self, **kw):
            return [{"id": "wf_b7f11701", "name": CGA}], None
        create_submission = client.create_submission
    monkeypatch.setattr(gowe, "_get_client", lambda config=None: _Catalog())
    r = await gowe.submit_gowe_job("wf_b7f11701", {"scientific_name": "bau_sim", "output_path": "x"}, config=_cfg())
    client.create_submission.assert_not_awaited()
    assert r.get("missing_input") == "taxonomy_id"


@pytest.mark.asyncio
async def test_submit_with_organism_goes_through(client, monkeypatch):
    monkeypatch.setattr(gowe, "_resolve_workflow_ref", AsyncMock(return_value=("wf_cga", None)))
    r = await gowe.submit_gowe_job(CGA, {"scientific_name": "Staphylococcus aureus", "taxonomy_id": 1280,
                                         "output_path": "x"}, config=_cfg())
    client.create_submission.assert_awaited_once()
    assert r["submission_id"] == "sub_1"


# --- populate loop: asks instead of failing ---------------------------------

def _reply(content="", tool_calls=None):
    calls = [SimpleNamespace(id=f"c{i}", type="function",
                             function=SimpleNamespace(name=n, arguments=json.dumps(a)))
             for i, (n, a) in enumerate(tool_calls or [])]
    msg = SimpleNamespace(content=content, tool_calls=calls or None, reasoning=None)
    return SimpleNamespace(choices=[SimpleNamespace(message=msg, finish_reason="stop")])




# --- replay: plain message ----------------------------------------------------

