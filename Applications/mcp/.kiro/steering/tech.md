# Tech Stack

## Language & Runtime
- Python 3.x

## Core Libraries
- `mcp` (FastMCP) — MCP server framework; tools are registered via `@mcp.tool()` decorator
- `elasticsearch` — official Python Elasticsearch client; used for all ES API calls
- `asyncio` — used in the test client for async MCP session management

## Configuration
- Connection settings are driven by environment variables with fallbacks in `config.py`:
  - `ELASTIC_URL` (default: `https://localhost:9200`)
  - `ELASTIC_USER` (default: `elastic`)
  - `ELASTIC_PASSWORD`
  - `ELASTIC_CA_CERTS` — path to the CA certificate for TLS verification

## Common Commands

### Run the MCP server
```bash
cd es-mcp
python server.py
```

### Run the test client (validates connectivity and tool listing)
```bash
cd es-mcp
python client.py
```

### Test raw Elasticsearch connectivity
```bash
python es-test.py
```

## No Build Step
There is no compilation, bundling, or build system. The project runs directly as Python scripts. Dependencies are managed externally (pip/uv); there is no `requirements.txt` or `pyproject.toml` currently in the repo.
