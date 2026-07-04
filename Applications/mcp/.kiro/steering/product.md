# Product

This is an Elasticsearch MCP (Model Context Protocol) Server. It exposes Elasticsearch cluster operations as MCP tools, allowing AI assistants to interact with an Elasticsearch instance directly — running searches, managing indices, inspecting cluster health, handling security, ILM policies, snapshots, ingest pipelines, and more.

The server acts as a bridge between MCP-compatible AI clients and a live Elasticsearch cluster. It is intended for operational and administrative use: querying data, monitoring cluster state, and managing cluster configuration through natural language.

A test client (`client.py`) is included for validating connectivity and tool availability without an external MCP host.
