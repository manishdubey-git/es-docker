# Elasticsearch MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io) server that exposes Elasticsearch cluster operations as structured tools, letting AI assistants (Kiro, Claude Desktop, etc.) interact with a live Elasticsearch instance through natural language.

Covers: search, index management, cluster health, ILM, snapshots, security, ingest pipelines, and more — over 60 tools across 10 domain modules.

---

## Prerequisites

- **Python 3.x** — `python3 --version`
- **pip / pip3** — comes with Python
- **A running Elasticsearch instance** — local or remote, with HTTPS enabled and credentials available

---

## Installation

```bash
cd es-mcp
pip3 install -r requirements.txt
```

Dependencies (pinned versions):

| Package | Version |
|---|---|
| `mcp` (FastMCP) | 1.28.1 |
| `elasticsearch` | 9.4.1 |

---

## Environment Setup

All connection parameters are read from environment variables. Copy the example file and fill in your values:

```bash
cd es-mcp
cp .env.example .env
# edit .env with your credentials — never commit this file
```

Then export the variables before running the server:

```bash
export ELASTIC_URL="https://localhost:9200"   # default; omit if using localhost
export ELASTIC_USER="elastic"                 # default; omit if using elastic user
export ELASTIC_PASSWORD="your-password"       # required — no default
export ELASTIC_CA_CERTS="/path/to/http_ca.crt"  # required for self-signed TLS
```

| Variable | Default | Required | Description |
|---|---|---|---|
| `ELASTIC_URL` | `https://localhost:9200` | No | Full URL including scheme and port |
| `ELASTIC_USER` | `elastic` | No | Basic auth username |
| `ELASTIC_PASSWORD` | *(none)* | **Yes** | Basic auth password — server refuses to start without it |
| `ELASTIC_CA_CERTS` | *(none)* | For self-signed TLS | Absolute path to the CA certificate |

> For a default local Elasticsearch install, the CA cert is typically at:
> `/path/to/elasticsearch/config/certs/http_ca.crt`

---

## Running the Server

```bash
cd es-mcp
python3 server.py
```

The server starts and listens on **stdio** (standard in/out). It will refuse to start if `ELASTIC_PASSWORD` is not set. There is no HTTP port — MCP clients communicate via stdio transport.

---

## Running the Test Client

`client.py` spawns the server as a subprocess and runs a smoke test — no external MCP host needed:

```bash
cd es-mcp
python3 client.py
```

It will:
1. Connect to the server over stdio
2. List all available tools
3. Call `ping`, `cluster_health`, and `list_indices` and print results

Use this to confirm your environment is wired up correctly before connecting a real MCP host.

---

## Testing Raw Connectivity

To verify Elasticsearch connectivity independently of the MCP layer:

```bash
# From the project root
export ELASTIC_PASSWORD="your-password"
export ELASTIC_CA_CERTS="/path/to/http_ca.crt"
python3 es-test.py
```

This calls `es.info()` directly and prints the cluster response. Useful for isolating TLS or credential issues.

---

## Connecting an MCP Client

The server uses **stdio transport** — clients spawn it as a subprocess.

### Kiro

Edit `~/.kiro/settings/mcp.json` (global) or `.kiro/settings/mcp.json` (workspace):

```json
{
  "mcpServers": {
    "es-mcp": {
      "command": "python3",
      "args": ["/absolute/path/to/es-mcp/server.py"],
      "env": {
        "ELASTIC_URL": "https://localhost:9200",
        "ELASTIC_USER": "elastic",
        "ELASTIC_PASSWORD": "your-password",
        "ELASTIC_CA_CERTS": "/path/to/http_ca.crt"
      },
      "disabled": false,
      "autoApprove": ["ping", "cluster_health", "list_indices"]
    }
  }
}
```

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "es-mcp": {
      "command": "python3",
      "args": ["/absolute/path/to/es-mcp/server.py"],
      "env": {
        "ELASTIC_URL": "https://localhost:9200",
        "ELASTIC_USER": "elastic",
        "ELASTIC_PASSWORD": "your-password",
        "ELASTIC_CA_CERTS": "/path/to/http_ca.crt"
      }
    }
  }
}
```

Restart the client after saving. The server will appear in the tools list.

---

## Tool Domains

| File | Responsibility | Example Tools |
|---|---|---|
| `cluster.py` | Cluster health, stats, settings, pending tasks, reroute, allocation explain | `cluster_health`, `cluster_stats`, `allocation_explain` |
| `cat.py` | Cat APIs — indices, shards, nodes, aliases, templates, allocation, segments, recovery | `cat_indices`, `cat_shards`, `cat_nodes` |
| `search.py` | Keyword search, Query DSL, count, explain, validate, profile, msearch, async search | `search`, `advanced_search`, `async_search` |
| `indices.py` | Index CRUD, mappings, settings, aliases, legacy/composable/component templates | `create_index`, `get_mapping`, `put_alias` |
| `nodes.py` | Node stats, info, hot threads, REST usage, keystore reload | `node_stats`, `hot_threads`, `node_usage` |
| `ilm.py` | ILM status, per-index explain, policy CRUD | `ilm_status`, `ilm_explain`, `ilm_put_policy` |
| `snapshots.py` | Snapshot repositories, create/list/delete/restore | `get_snapshots`, `create_snapshot`, `restore_snapshot` |
| `security.py` | Users, roles, privileges, API keys, role mappings | `get_users`, `create_api_key`, `put_role` |
| `ingest.py` | Pipeline CRUD, simulate, stats | `put_pipeline`, `simulate_pipeline`, `ingest_stats` |
| `monitoring.py` | Cluster-wide monitoring stats | `monitoring_stats` |

---

## Extending with New Tools

Adding a new tool domain takes three steps and touches only two files.

**1. Create the domain file** — `es-mcp/tools/transforms.py`:

```python
def register(mcp, es):

    @mcp.tool()
    def get_transforms(transform_id: str = None) -> dict:
        """List transform jobs. Optionally filter by transform_id."""
        params = {}
        if transform_id is not None:
            params["transform_id"] = transform_id
        return es.transform.get_transform(**params)
```

**2. Register it in `tools/__init__.py`** — add one import and one call:

```python
from .transforms import register as register_transforms   # add this line

def register_all(mcp, es):
    # ... existing registrations ...
    register_transforms(mcp, es)                          # add this line
```

**3. That's it.** No other files change. The tool appears automatically in the MCP tool list on next server start.

Key conventions to follow:
- Every tool file exports a single `register(mcp, es)` function.
- Tools are closures over `es` — never instantiate your own ES client.
- Optional parameters default to `None`; add them to the request body only when provided.
- The docstring is the MCP tool description — keep it concise and include param examples.

---

## Project Structure

```
mcp/
├── es-mcp/
│   ├── server.py            # Entry point — creates FastMCP, calls register_all()
│   ├── config.py            # ES client factory — reads env vars, exports shared client
│   ├── client.py            # Test client — smoke tests connectivity and tool list
│   ├── requirements.txt     # Pinned dependencies
│   ├── .env.example         # Environment variable reference
│   └── tools/
│       ├── __init__.py      # Aggregates all register() calls into register_all()
│       ├── cluster.py
│       ├── cat.py
│       ├── search.py
│       ├── indices.py
│       ├── nodes.py
│       ├── ilm.py
│       ├── snapshots.py
│       ├── security.py
│       ├── ingest.py
│       └── monitoring.py
└── es-test.py               # Standalone ES connectivity test (no MCP dependency)
```
