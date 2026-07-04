# Implementation Plan: Elasticsearch MCP Server

## Overview
Build and harden an MCP server that bridges AI assistants with a live Elasticsearch cluster. All core tool domains are implemented; remaining work covers optional extensions and long-term quality improvements.

## Tasks

- [x] 1. Set up project layout — `es-mcp/` folder with `server.py`, `config.py`, `client.py`, `tools/` package
- [x] 2. Implement `config.py` — env-var-driven `Elasticsearch` client with TLS support (`ELASTIC_URL`, `ELASTIC_USER`, `ELASTIC_PASSWORD`, `ELASTIC_CA_CERTS`)
- [x] 3. Implement `server.py` — FastMCP instance creation, `register_all()` call, `mcp.run()` entry point
- [x] 4. Implement `tools/__init__.py` — `register_all()` aggregator that calls every domain `register(mcp, es)`
- [x] 5. Implement `tools/cluster.py` — `ping`, `cluster_health`, `cluster_info`, `cluster_stats`, `cluster_settings`, `pending_tasks`, `reroute`, `allocation_explain`
- [x] 6. Implement `tools/cat.py` — `list_indices`, `cat_indices`, `cat_shards`, `cat_nodes`, `cat_aliases`, `cat_templates`, `cat_allocation`, `cat_segments`, `cat_recovery`
- [x] 7. Implement `tools/search.py` — `search`, `advanced_search`, `count`, `explain`, `validate_query`, `profile`, `msearch`, `async_search`, `get_async_search`, `delete_async_search`
- [x] 8. Implement `tools/indices.py` — index CRUD, mappings, settings, aliases, legacy templates, component templates, composable templates
- [x] 9. Implement `tools/nodes.py` — `node_stats`, `node_info`, `hot_threads`, `node_usage`, `reload_secure_settings`
- [x] 10. Implement `tools/ilm.py` — `ilm_status`, `ilm_explain`, `ilm_get_policies`, `ilm_put_policy`, `ilm_delete_policy`
- [x] 11. Implement `tools/snapshots.py` — `get_repositories`, `get_snapshots`, `create_snapshot`, `delete_snapshot`, `restore_snapshot`
- [x] 12. Implement `tools/security.py` — users, roles, privileges, API keys, role mappings (full CRUD)
- [x] 13. Implement `tools/ingest.py` — `get_pipelines`, `put_pipeline`, `delete_pipeline`, `simulate_pipeline`, `ingest_stats`
- [x] 14. Implement `client.py` — stdio MCP client that spawns the server, lists tools, and runs smoke tests (`ping`, `cluster_health`, `list_indices`)
- [x] 15. Add `requirements.txt` with pinned dependencies (`mcp`, `elasticsearch`)
- [x] 16. Add `.env.example` documenting all required environment variables
- [x] 17. Validate that `ELASTIC_PASSWORD` is not hardcoded; ensure no credentials are committed to source control
- [x] 18. Add error handling — wrap ES client calls to catch `ConnectionError`, `AuthenticationException`, and `NotFoundError`; return structured error messages instead of raising
- [x] 19. Implement `tools/monitoring.py` — cluster-wide monitoring stats (`monitoring_stats`)
- [x] 20. Add `README.md` covering prerequisites, environment setup, running the server, connecting an MCP client, and extending with new tools
- [x] 21. Implement `tools/transforms.py` — Elasticsearch Transform APIs
- [x] 22. Implement `tools/watcher.py` — Elasticsearch Watcher / Alerting APIs
- [ ] 23. Implement `tools/data_streams.py` — data stream management: create, delete, rollover, get stats
- [ ] 24. Implement `tools/enrich.py` — enrich policy APIs: get, put, delete, execute
- [ ] 25. Implement `tools/tasks.py` — task management APIs: list tasks, get task by ID, cancel task
- [ ] 26. Add type hints to all tool function signatures and the config module
- [ ] 27. Add integration tests — pytest-based suite that runs against a live ES instance using `testcontainers` or a Docker Compose setup

## Task Dependency Graph

```json
{
  "waves": [
    { "wave": 1, "tasks": [1] },
    { "wave": 2, "tasks": [2, 3] },
    { "wave": 3, "tasks": [4] },
    { "wave": 4, "tasks": [5, 6, 7, 8, 9, 10, 11, 12, 13] },
    { "wave": 5, "tasks": [14] },
    { "wave": 6, "tasks": [15, 16, 17, 18] },
    { "wave": 7, "tasks": [19, 20] },
    { "wave": 8, "tasks": [21, 22] },
    { "wave": 9, "tasks": [23, 24, 25, 26] },
    { "wave": 10, "tasks": [27] }
  ]
}
```

## Notes

- Tasks 1–22 are complete. The server is fully functional against a live Elasticsearch cluster.
- Tasks 23–25 follow the same domain-per-file pattern: create the tool file, implement `register(mcp, es)`, and add it to `tools/__init__.py`.
- Task 26 (type hints) is low-risk and can be done incrementally per tool file.
- Task 27 (integration tests) requires Docker or a reachable ES instance and should be treated as a separate effort.
