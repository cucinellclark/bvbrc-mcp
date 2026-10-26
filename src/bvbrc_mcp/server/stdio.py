"""stdio MCP server, for clients that start it themselves (Claude Desktop).

    KB_AUTH_TOKEN=<BV-BRC token> bvbrc-mcp-stdio

Tools run as the KB_AUTH_TOKEN user unless a call passes ``bvbrc_token``.
Logs go to stderr (stdout carries the protocol).
"""

from __future__ import annotations

import logging
import os
import sys

from fastmcp import FastMCP

from bvbrc_mcp import __version__
from bvbrc_mcp.server.mcp_tools import register_tools
from bvbrc_mcp.server.token_provider import TokenProvider
from bvbrc_mcp.settings import get_settings


def create_server() -> FastMCP:
    mcp = FastMCP("BV-BRC")
    register_tools(mcp, TokenProvider(mode="stdio"), get_settings())
    return mcp


def main() -> int:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
    log = logging.getLogger("bvbrc_mcp.server")
    if not os.getenv("KB_AUTH_TOKEN"):
        log.warning("KB_AUTH_TOKEN is not set: tools need a bvbrc_token argument.")
    log.info("bvbrc-mcp %s (stdio)", __version__)
    create_server().run(transport="stdio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
