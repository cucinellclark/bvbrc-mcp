"""bvbrc_mcp must stand alone: no module may import the bvbrc-agents harness."""

import ast
from pathlib import Path

import bvbrc_mcp

FORBIDDEN = ("shared", "agents", "orchestrator", "common", "functions", "mcp_tools", "bvbrc_solr_api")


def _imports(path: Path):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                yield node.lineno, a.name
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            yield node.lineno, node.module


def test_no_module_imports_the_harness():
    root = Path(bvbrc_mcp.__file__).parent
    bad = []
    for path in sorted(root.rglob("*.py")):
        for line, mod in _imports(path):
            top = mod.split(".")[0]
            if top in FORBIDDEN or top.endswith("_agent"):
                bad.append(f"{path.relative_to(root)}:{line} imports {mod}")
    assert bad == []


def test_no_module_edits_sys_path():
    root = Path(bvbrc_mcp.__file__).parent
    offenders = [str(p.relative_to(root)) for p in root.rglob("*.py") if "sys.path.insert" in p.read_text()]
    assert offenders == []
