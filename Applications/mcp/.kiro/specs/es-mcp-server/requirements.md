# Requirements — Elasticsearch MCP Server

## Overview
Build a Model Context Protocol (MCP) server that exposes Elasticsearch cluster operations as structured tools, enabling AI assistants to interact with a live Elasticsearch instance through natural language.

---

## Functional Requirements

### FR-1: Connectivity & Cluster Operations
- **FR-1.1** The server MUST verify connectivity to Elasticsearch via a `ping` tool.
- **FR-1.2** The server MUST expose cluster health, info, and stats as discrete tools.
- **FR-1.3** The server MUST support reading current cluster settings (persistent and transient).
- **FR-1.4** The server MUST support pending task inspection and shard rerouting.
- **FR-1.5** The server MUST support shard allocation explain for diagnosing unassigned shards.

### FR-2: Index Management
- **FR-2.1** The server MUST support creating and deleting indices with optional mappings and settings.
- **FR-2.2** The server MUST support reading and updating index mappings and settings.
- **FR-2.3** The server MUST support creating, updating, and deleting index aliases.
- **FR-2.4** The server MUST support legacy index templates (get, put, delete).
- **FR-2.5** The server MUST support composable index templates and component templates (get, put, delete).

### FR-3: Search & Query
- **FR-3.1** The server MUST support full-text keyword search via `multi_match` across all fields.
- **FR-3.2** The server MUST support full Elasticsearch Query DSL execution (`advanced_search`).
- **FR-3.3** The server MUST support document count per index.
- **FR-3.4** The server MUST support query explain, validation, and profiling.
- **FR-3.5** The server MUST support multi-search (`msearch`) in a single request.
- **FR-3.6** The server MUST support asynchronous search submission and result retrieval/deletion.

### FR-4: Cat APIs
- **FR-4.1** The server MUST expose cat APIs for indices, shards, nodes, aliases, templates, allocation, segments, and recovery.

### FR-5: Node Management
- **FR-5.1** The server MUST expose node stats and static node info, with optional filtering by node ID and metric.
- **FR-5.2** The server MUST support hot thread diagnostics per node.
- **FR-5.3** The server MUST support per-node REST action usage stats.
- **FR-5.4** The server MUST support reloading keystore secure settings without a node restart.

### FR-6: Index Lifecycle Management (ILM)
- **FR-6.1** The server MUST expose ILM status and per-index ILM explain.
- **FR-6.2** The server MUST support full CRUD for ILM policies.

### FR-7: Snapshot Management
- **FR-7.1** The server MUST support listing and getting snapshot repositories.
- **FR-7.2** The server MUST support creating, listing, and deleting snapshots.
- **FR-7.3** The server MUST support restoring snapshots with optional index filtering and rename patterns.

### FR-8: Security
- **FR-8.1** The server MUST support full CRUD for native users, roles, and role mappings.
- **FR-8.2** The server MUST support reading application privileges.
- **FR-8.3** The server MUST support creating, listing, and invalidating API keys.

### FR-9: Ingest Pipelines
- **FR-9.1** The server MUST support full CRUD for ingest pipelines.
- **FR-9.2** The server MUST support pipeline simulation against sample documents.
- **FR-9.3** The server MUST expose ingest pipeline stats (doc counts, failures, processing time).

---

## Non-Functional Requirements

### NFR-1: Configuration
- All connection parameters (URL, credentials, TLS certs) MUST be configurable via environment variables.
- Hardcoded defaults MAY exist for local development but MUST NOT be used in production.

### NFR-2: Security
- TLS certificate verification MUST be enabled by default.
- Credentials MUST NOT be embedded in source-controlled files in production deployments.

### NFR-3: Extensibility
- Adding a new tool domain MUST require only: a new tool file + a `register()` function + one line in `__init__.py`.
- Tools MUST remain thin — direct ES client calls only, no intermediate service layers.

### NFR-4: Tool Documentation
- Every tool MUST have a docstring that serves as its MCP description.
- Docstrings MUST be concise and include parameter examples for complex inputs.

### NFR-5: Testability
- A standalone test client (`client.py`) MUST exist to validate server connectivity and tool availability without requiring an external MCP host.
