"""HTTP MCP server with OAuth sign-in through BV-BRC.

    BVBRC_MCP_CONFIG=/path/config.json bvbrc-mcp-http

FastMCP's OAuthProvider serves the discovery documents and the
/authorize, /token and /register endpoints; ``/login`` is the BV-BRC sign-in
page. Every OAuth address is built from ``Settings.public_url``. Behind a
path prefix (www.bv-brc.org/mcp) see DEPLOYMENT.md for the routes nginx needs.
"""

from __future__ import annotations

import logging
import sys

from fastmcp import FastMCP

from bvbrc_mcp import __version__
from bvbrc_mcp.server.mcp_tools import register_tools
from bvbrc_mcp.server.token_provider import TokenProvider
from bvbrc_mcp.settings import Settings, get_settings

log = logging.getLogger("bvbrc_mcp.server")


def create_server(settings: Settings | None = None) -> FastMCP:
    from bvbrc_mcp.server.auth import BvbrcOAuthProvider

    settings = settings or get_settings()
    oauth = BvbrcOAuthProvider(
        base_url=settings.public_url.rstrip("/"),
        authentication_url=settings.authentication_url,
        # The token audience must equal the advertised resource exactly, or
        # ChatGPT drops the token.
        resource_url=settings.public_url.rstrip("/") + settings.mcp_path,
    )
    mcp = FastMCP("BV-BRC", auth=oauth)
    oauth.register_login_route(mcp)
    register_tools(mcp, TokenProvider(mode="http", oauth_provider=oauth), settings)
    return mcp


def main() -> int:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
    settings = get_settings()
    if not settings.jwt_signing_key:
        log.warning("No jwt_signing_key: access tokens are signed with a random key, "
                    "so every client is signed out when this server restarts.")
    if not settings.gowe_url:
        log.warning("No gowe_url: the GoWe tools (workflows, submit, rerun, batch) will fail.")
    mcp = create_server(settings)
    log.info("bvbrc-mcp %s on %s:%s%s, public URL %s", __version__, settings.host,
             settings.port, settings.mcp_path, settings.public_url)
    try:
        mcp.run(transport="http", host=settings.host, port=settings.port, path=settings.mcp_path)
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
