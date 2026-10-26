# bvbrc-mcp

Tools that let a language model work with [BV-BRC](https://www.bv-brc.org)
(the Bacterial and Viral Bioinformatics Resource Center): search its data,
read and summarize files in a user's workspace, build genome and feature
groups, find and submit analysis workflows, look up jobs and their outputs,
and search the BV-BRC documentation and the literature. Usable as a Python
library or through the MCP servers in this package.

## Install

```bash
pip install "bvbrc-mcp[server]"     # library + MCP servers
pip install "bvbrc-mcp[server,pdf,xlsx]"   # + PDF text extraction, spreadsheet metadata
```

Python 3.11 or newer.

## Use with an MCP client

**stdio** (a client that starts the server itself, such as Claude Desktop):

```json
{
  "mcpServers": {
    "bvbrc": {
      "command": "bvbrc-mcp-stdio",
      "env": {"KB_AUTH_TOKEN": "<your BV-BRC token>"}
    }
  }
}
```

**HTTP** with OAuth sign-in through BV-BRC: `bvbrc-mcp-http` (see
[DEPLOYMENT.md](DEPLOYMENT.md)). The public server is `https://www.bv-brc.org/mcp`.

## Use as a library

```python
from bvbrc_mcp import TOOLS, ToolContext, dispatch

ctx = ToolContext(bvbrc_auth_token=token, gowe_url="http://localhost:7000")
result = await dispatch("search_data",
                        {"collection": "genome", "query": 'genome_name:"Mycobacterium tuberculosis"'},
                        ctx)
```

`TOOLS` lists every tool with its JSON schema (OpenAI function-calling form),
so it can be handed to any model that calls tools. `dispatch` always returns a
dict; failures come back as `{"error": ..., "errorType": ...}`.

## Tools

| Area | Tools |
|---|---|
| Data | `search_data`, `facet_query`, `probe_data`, `list_collections`, `get_collection_fields` |
| Workspace | `workspace_browse`, `get_file_metadata`, `read_file_preview`, `search_file`, `summarize_file`, `list_samples` |
| Workflows | `list_gowe_workflows`, `get_workflow_inputs`, `submit_gowe_job`, `rerun_jobs`, `prepare_batch` |
| Groups | `create_group`, `edit_group`, `list_groups`, `get_group_ids` |
| Jobs | `list_jobs`, `get_job_details`, `get_expected_outputs` |
| Other | `get_sra_metadata`, `find_similar_genomes`, `search_literature`, `query_helpdesk`, `list_services`, `get_service_schema` |

Over MCP each is named `agent_<name>`. `submit_gowe_job`, `create_group` and
`edit_group` change the user's account (`bvbrc_mcp.SIDE_EFFECT_TOOLS`); a
caller should confirm them with the user. `rerun_jobs` and `prepare_batch`
only prepare jobs.

Workflow tools need a [GoWe](https://github.com/wilke/GoWe) server
(`gowe_url`). `get_sra_metadata` needs sra-tools in a Singularity container
(`sra_container_path`) and is unavailable without one.

## Configuration

The servers read `BVBRC_MCP_CONFIG` (a JSON file, see
[`config.example.json`](config.example.json)) and `BVBRC_MCP_<NAME>`
environment variables; see `src/bvbrc_mcp/settings.py` for every setting.

## Development

```bash
python3.11 -m venv .venv && .venv/bin/pip install -e ".[server,pdf,xlsx,dev]"
.venv/bin/pytest
```

## License

MIT
