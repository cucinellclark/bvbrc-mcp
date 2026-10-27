"""build_workspace_url: links to workspace folders are encoded per segment.

A raw "#" in a folder name cut the URL (same bug as the website's JIRA-4420);
the encoding matches the chat's path chips (WorkspacePathUtils.js), so a chip
and an agent link to one folder are the same URL.
"""
from urllib.parse import unquote

from bvbrc_mcp.tools.url_utils import build_workspace_url

BASE = "https://www.bv-brc.org/workspace/"


def test_plain_path_unchanged():
    assert build_workspace_url("/user@bv-brc.org/home/MyData") == BASE + "user@bv-brc.org/home/MyData"


def test_segments_encoded_like_encodeURIComponent():
    assert (
        build_workspace_url("/user@bv-brc.org/home/Run #3/50% done?/a&b (c)!*'~")
        == BASE + "user@bv-brc.org/home/Run%20%233/50%25%20done%3F/a%26b%20(c)!*'~"
    )


def test_spaces_and_at_in_later_segments():
    assert (
        build_workspace_url("/ARWattam@patricbrc.org/BV-BRC Workshop/x@y")
        == BASE + "ARWattam@patricbrc.org/BV-BRC%20Workshop/x%40y"
    )


def test_public_keeps_owner_segment():
    assert (
        build_workspace_url("/public/ARWattam@patricbrc.org/BV-BRC Workshop")
        == BASE + "public/ARWattam@patricbrc.org/BV-BRC%20Workshop"
    )


def test_round_trip():
    path = "/user@bv-brc.org/home/Run #3/a&b (c)"
    url = build_workspace_url(path)
    assert "/" + "/".join(unquote(p) for p in url[len(BASE):].split("/")) == path


def test_empty():
    assert build_workspace_url("") is None
    assert build_workspace_url(None) is None
