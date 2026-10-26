// pm2 config for the HTTP MCP server. Set BVBRC_MCP_HOME to the deployment
// directory: a venv at $BVBRC_MCP_HOME/venv with bvbrc-mcp[server] installed,
// config.json (see config.example.json), jwt.key, data/, logs/.
const H = process.env.BVBRC_MCP_HOME || '/path/to/bvbrc-mcp';
const fs = require('fs');

module.exports = {
  apps: [{
    name: 'bvbrc-mcp',
    script: `${H}/venv/bin/bvbrc-mcp-http`,
    interpreter: 'none',
    cwd: H,                       // data/oauth_clients.json is relative to this
    env: {
      BVBRC_MCP_CONFIG: `${H}/config.json`,
      // Fixed signing key: without it every restart signs all clients out.
      BVBRC_MCP_JWT_SIGNING_KEY: fs.existsSync(`${H}/jwt.key`) ? fs.readFileSync(`${H}/jwt.key`, 'utf8').trim() : '',
    },
    autorestart: true,
    max_restarts: 10,
    restart_delay: 5000,
    kill_timeout: 15000,
    out_file: `${H}/logs/bvbrc-mcp.out.log`,
    error_file: `${H}/logs/bvbrc-mcp.err.log`,
    time: true,
  }],
};
