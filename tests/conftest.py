import pytest

from bvbrc_mcp.tools import workspace as _workspace


@pytest.fixture(autouse=True)
def _fresh_workspace_caches():
    """The top-level listing and permissions are cached per user for minutes."""
    _workspace.clear_workspace_caches()
    yield
    _workspace.clear_workspace_caches()
