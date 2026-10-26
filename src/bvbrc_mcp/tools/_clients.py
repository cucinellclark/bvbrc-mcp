"""Access to the BV-BRC API client modules in ``bvbrc_mcp.clients``.

The getters keep the names the tool modules used when the clients lived in a
separate MCP server checkout reached through ``sys.path``; they now just
return the package modules. The ``mcp_server_path`` argument is accepted and
ignored so existing call sites keep working.
"""

from __future__ import annotations

from types import ModuleType
from typing import Optional


def get_workspace_functions(mcp_server_path: Optional[str] = None) -> ModuleType:
    from bvbrc_mcp.clients import workspace_functions
    return workspace_functions


def get_data_functions(mcp_server_path: Optional[str] = None) -> ModuleType:
    from bvbrc_mcp.clients import data_functions
    return data_functions


def get_group_functions(mcp_server_path: Optional[str] = None) -> ModuleType:
    from bvbrc_mcp.clients import group_functions
    return group_functions


def get_sra_functions(mcp_server_path: Optional[str] = None) -> ModuleType:
    from bvbrc_mcp.clients import sra_functions
    return sra_functions


def get_json_rpc(mcp_server_path: Optional[str] = None) -> ModuleType:
    from bvbrc_mcp.clients import json_rpc
    return json_rpc


def get_gowe_client(mcp_server_path: Optional[str] = None) -> ModuleType:
    from bvbrc_mcp.clients import gowe_client
    return gowe_client


def get_service_functions(mcp_server_path: Optional[str] = None) -> ModuleType:
    from bvbrc_mcp.clients import service_functions
    return service_functions
