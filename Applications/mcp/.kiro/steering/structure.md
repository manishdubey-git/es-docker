# Project Structure

```
mcp/
├── es-mcp/                  # Main MCP server package
│   ├── server.py            # Entry point — creates FastMCP instance, calls register_all()
│   ├── config.py            # Elasticsearch client instantiation and env-var config
│   ├── client.py            # Test client — connects via stdio, lists tools, runs sample calls
│   └── tools/               # One module per ES domain area
│       ├── __init__.py      # Imports all register() functions, exposes register_all()
│       ├── cluster.py       # Cluster health, stats, settings, reroute, allocation explain
│       ├── cat.py           # Cat APIs — indices, shards, aliases, nodes, templates, etc.
│       ├── search.py        # Search, advanced search, async search, explain, validate, profile, msearch
│       ├── indices.py       # Index CRUD, mappings, settings, aliases, legacy/composable templates
│       ├── nodes.py         # Node stats, info, hot threads, usage, reload secure settings
│       ├── ilm.py           # ILM status, explain, get/put/delete policies
│       ├── snapshots.py     # Snapshot repositories, create/list/delete/restore snapshots
│       ├── security.py      # Users, roles, privileges, API keys, role mappings
│       └── ingest.py        # Ingest pipelines — get/put/delete/simulate, ingest stats
└── es-test.py               # Standalone connectivity test (no MCP dependency)
```

## Architecture Patterns

- **Domain-per-file**: Each tool file owns one ES domain (cluster, search, indices, etc.). New domains get their own file.
- **Register pattern**: Every tool file exports a single `register(mcp, es)` function. Tools are defined as closures inside it using `@mcp.tool()`. `tools/__init__.py` aggregates all `register()` calls into `register_all()`.
- **Shared ES client**: A single `Elasticsearch` instance is created in `config.py` and passed into every `register()` call — tools never instantiate their own client.
- **No abstraction layers**: Tools call the ES Python client directly. Keep logic thin; avoid introducing service or repository layers.

## Conventions

- Tool docstrings are the MCP tool descriptions — keep them concise and include parameter examples where helpful.
- Optional parameters default to `None`; conditionally add them to the request body only when provided.
- Adding a new tool: implement it in the appropriate domain file, or create a new domain file + `register()` function and add it to `__init__.py`.
