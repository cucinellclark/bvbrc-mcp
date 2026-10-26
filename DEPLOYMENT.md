# Deploying the HTTP MCP server behind a path (www.bv-brc.org/mcp)

Status: **open** (2026-10-26). The production URL will be
`https://www.bv-brc.org/mcp`, replacing an older version there. The routes
below were measured from this server's own app (FastMCP 2.13, the
`BvbrcOAuthProvider` in `src/bvbrc_mcp/server/auth.py`) with
`public_url: "https://www.bv-brc.org/mcp"`; they have **not** yet been tried
with ChatGPT or Claude against a real deployment.

## Why a path prefix is not just one nginx location

MCP clients sign in with OAuth and find the sign-in endpoints through
discovery documents. The standards put those documents at the **domain root**,
with the path appended after `/.well-known/...` (RFC 9728 for the protected
resource, RFC 8414 for the authorization server). So for a server at
`https://www.bv-brc.org/mcp`, clients look for:

| Client fetches | Comes from |
|---|---|
| `https://www.bv-brc.org/.well-known/oauth-protected-resource/mcp/` | The `resource_metadata` URL in the server's 401 reply |
| `https://www.bv-brc.org/.well-known/oauth-authorization-server/mcp` | RFC 8414 discovery for the issuer `https://www.bv-brc.org/mcp` |
| `https://www.bv-brc.org/.well-known/openid-configuration/mcp` | Some clients try OpenID discovery too |

A `location /mcp/` block never sees these requests: they are outside `/mcp`.

## Server setting

Run the server with `public_url: "https://www.bv-brc.org/mcp"` and `mcp_path: "/"`
(both the defaults in `config.example.json`), and let nginx strip the `/mcp`
prefix. The server then serves:

| Server path | Public URL |
|---|---|
| `/` | `https://www.bv-brc.org/mcp/` (the MCP endpoint) |
| `/authorize`, `/token`, `/register`, `/login` | `https://www.bv-brc.org/mcp/authorize` ... (advertised in the metadata; fine under the prefix) |
| `/.well-known/oauth-protected-resource/mcp/` | must be reachable at the **root** URL above |
| `/.well-known/oauth-authorization-server` | must be reachable at `/.well-known/oauth-authorization-server/mcp` (root) |
| `/.well-known/openid-configuration` | must be reachable at `/.well-known/openid-configuration/mcp` (root) |

With `mcp_path: "/mcp"` and the same public URL, everything moves to
`/mcp/mcp` (resource `https://www.bv-brc.org/mcp/mcp`), so keep `/`.

## nginx sketch (www.bv-brc.org server block)

```nginx
# MCP endpoint and OAuth endpoints: strip the /mcp prefix
location = /mcp { proxy_pass http://<host>:<port>/; include mcp_proxy.conf; }   # no redirect: clients POST here
location /mcp/  { proxy_pass http://<host>:<port>/; include mcp_proxy.conf; }

# Discovery documents at the domain root (path-inserted, per RFC 9728 / 8414)
location = /.well-known/oauth-protected-resource/mcp  { proxy_pass http://<host>:<port>/.well-known/oauth-protected-resource/mcp/; }
location = /.well-known/oauth-protected-resource/mcp/ { proxy_pass http://<host>:<port>/.well-known/oauth-protected-resource/mcp/; }
location = /.well-known/oauth-authorization-server/mcp { proxy_pass http://<host>:<port>/.well-known/oauth-authorization-server; }
location = /.well-known/openid-configuration/mcp       { proxy_pass http://<host>:<port>/.well-known/openid-configuration; }
```

`mcp_proxy.conf` holds what the dev-9 block in `devX.bv-brc.org.conf` uses
for the streamed MCP transport: `proxy_buffering off; proxy_cache off;
proxy_http_version 1.1; proxy_set_header Connection ''; proxy_set_header Host
$host; chunked_transfer_encoding on;` and a long `proxy_read_timeout`.

These are exact-match locations, so they do not touch the rest of the site's
`/.well-known/` (for example `acme-challenge`).

## Before going live

- Token audience: the server issues tokens whose audience is exactly the
  advertised resource (`https://www.bv-brc.org/mcp/`, trailing slash
  included); ChatGPT silently drops a token whose `aud` differs.
  `tests/test_server.py` checks this for both a path and a root URL.
- Set a fixed signing key (`jwt_signing_key` / `BVBRC_MCP_JWT_SIGNING_KEY`;
  `deploy/ecosystem.config.js` reads it from `jwt.key`). Otherwise every
  restart signs every client out.
- Keep `oauth.client_store_path` on persistent disk.
- Add the production callback URLs (ChatGPT, Claude) to
  `oauth.allowed_callback_urls`.
- Connect once from ChatGPT and once from Claude; watch the access log for any
  `/.well-known/...` request that got a 404 and add a location for it.

## Running under pm2

```bash
H=/path/to/bvbrc-mcp-deploy
python3.11 -m venv $H/venv && $H/venv/bin/pip install "bvbrc-mcp[server] @ git+https://github.com/cucinellclark/bvbrc-mcp@<tag>"
cp config.example.json $H/config.json      # edit gowe_url, public_url, port
openssl rand -hex 32 > $H/jwt.key && chmod 600 $H/jwt.key
mkdir -p $H/logs $H/data
BVBRC_MCP_HOME=$H pm2 start deploy/ecosystem.config.js && pm2 save
```
