# Design — Elasticsearch MCP Server

## Architecture Overview

The server follows a flat, domain-partitioned architecture. A single `FastMCP` instance is created at startup and all tools are registered onto it by domain-specific modules. There are no service layers, repositories, or abstractions between tools and the Elasticsearch Python client.

```
┌─────────────────────────────────────────────┐
│              MCP Client / AI Host            │
│         (Kiro, Claude Desktop, etc.)         │
└───────────────────┬─────────────────────────┘
                    │ MCP Protocol (stdio / SSE)
┌───────────────────▼─────────────────────────┐
│               server.py                      │
│   FastMCP("Elastic MCP Server")              │
│   register_all(mcp, es)                      │
└───────────────────┬─────────────────────────┘
                    │
        ┌───────────▼───────────┐
        │     tools/__init__.py  │
        │  register_all()        │
        └──┬──┬──┬──┬──┬──┬──┬─┘
           │  │  │  │  │  │  │
     cluster  cat  search  indices  nodes  ilm  snapshots  security  ingest
           │
     ┌─────▼──────────────────────────────────┐
     │         config.py                        │
     │   Elasticsearch(url, auth, ca_certs)     │
     │   (single shared instance)               │
     └─────────────────────────────────────────┘
                    │
     ┌──────────────▼──────────────────────────┐
     │         Elasticsearch Cluster            │
     │         https://localhost:9200           │
     └─────────────────────────────────────────┘
```

---

## Component Design

### `server.py` — Entry Point
- Instantiates `FastMCP` with a human-readable server name.
- Imports the shared `es` client from `config.py`.
- Calls `register_all(mcp, es)` to bind all tools.
- Runs `mcp.run()` which starts the MCP transport (stdio by default).

### `config.py` — Client Factory
- Reads connection params from environment variables with safe local defaults.
- Constructs and exports a single `Elasticsearch` instance with TLS verification enabled.
- This is the only place an ES client is ever created.

### `tools/__init__.py` — Tool Registry
- Imports one `register` function per domain module.
- Exposes `register_all(mcp, es)` which calls each domain's `register()` in order.
- Adding a new domain = one import + one call here.

### Domain Tool Modules
Each file follows this exact pattern:

```python
def register(mcp, es):

    @mcp.tool()
    def tool_name(param: type = default) -> ...:
        """One-line description. Optional param examples."""
        body = {}
        if param is not None:
            body["key"] = param
        return es.<namespace>.<method>(...)
```

Key rules:
- Tools are closures over `es` — they never import or instantiate ES clients themselves.
- Optional parameters default to `None` and are only added to the request body when provided.
- Return values are the raw ES API response (dict/list); no transformation or envelope wrapping.
- Docstrings double as MCP tool descriptions — they must be self-contained and example-rich for complex tools.

### Domain Breakdown

| File | ES Namespace(s) | Responsibility |
|---|---|---|
| `cluster.py` | `es.cluster` | Health, stats, settings, pending tasks, reroute, allocation explain |
| `cat.py` | `es.cat` | Cat APIs — indices, shards, nodes, aliases, templates, allocation, segments, recovery |
| `search.py` | `es.search`, `es.async_search` | Keyword search, query DSL, count, explain, validate, profile, msearch, async search |
| `indices.py` | `es.indices`, `es.cluster` | Index CRUD, mappings, settings, aliases, legacy/composable/component templates |
| `nodes.py` | `es.nodes` | Stats, info, hot threads, usage, reload secure settings |
| `ilm.py` | `es.ilm` | ILM status, explain, policy CRUD |
| `snapshots.py` | `es.snapshot` | Repository listing, snapshot CRUD, restore |
| `security.py` | `es.security` | Users, roles, privileges, API keys, role mappings |
| `ingest.py` | `es.ingest` | Pipeline CRUD, simulate, stats |

---

## Configuration Design

```
Environment Variable     Default                          Notes
────────────────────     ──────────────────────────────   ──────────────────────────
ELASTIC_URL              https://localhost:9200            Full URL including scheme/port
ELASTIC_USER             elastic                          Basic auth username
ELASTIC_PASSWORD         (local dev default)              Must be set in production
ELASTIC_CA_CERTS         /path/to/http_ca.crt             Required for self-signed TLS
```

---

## Test Client Design (`client.py`)

The test client uses the MCP Python SDK to connect to the server over stdio, simulating how a real MCP host would interact with it. It:
1. Spawns the server as a subprocess using the same Python interpreter.
2. Initializes an MCP `ClientSession`.
3. Lists all available tools.
4. Executes a fixed set of smoke-test tool calls (`ping`, `cluster_health`, `list_indices`).

This validates the full tool registration and serialization path without needing Kiro or another MCP host.

---

## Data Flow — Tool Call Example

```
AI sends:  call_tool("advanced_search", {"index": "products", "query": {"term": {"category": "laptops"}}})
              │
              ▼
        FastMCP routes to advanced_search() closure
              │
              ▼
        es.search(index="products", body={"query": {...}, "size": 10, "from": 0})
              │
              ▼
        ES returns raw response dict
              │
              ▼
        FastMCP serializes and returns to AI client
```

---

## Extension Pattern

To add a new domain (e.g., `transforms`):

1. Create `es-mcp/tools/transforms.py` with a `register(mcp, es)` function.
2. Add `from .transforms import register as register_transforms` to `tools/__init__.py`.
3. Add `register_transforms(mcp, es)` inside `register_all()`.

No other files need to change.
