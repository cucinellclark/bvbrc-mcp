"""BV-BRC tools for language models, and MCP servers that expose them.

    from bvbrc_mcp import TOOLS, ToolContext, dispatch

    ctx = ToolContext(bvbrc_auth_token=token, gowe_url="http://localhost:7000")
    result = await dispatch("search_data", {"collection": "genome", "query": "genus:Salmonella"}, ctx)
"""

__version__ = "0.1.0"

from bvbrc_mcp.context import ToolContext
from bvbrc_mcp.registry import SIDE_EFFECT_TOOLS, TOOLS, TOOLS_BY_NAME, Tool, dispatch

__all__ = ["SIDE_EFFECT_TOOLS", "TOOLS", "TOOLS_BY_NAME", "Tool", "ToolContext", "dispatch", "__version__"]
