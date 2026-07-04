import elasticsearch


def register(mcp, es):

    @mcp.tool()
    def cat_indices(index: str = None):
        """List indices with health, status, doc count, and store size."""
        try:
            return es.cat.indices(index=index, format="json", v=True)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def cat_nodes():
        """List nodes with heap, RAM, CPU, load, and roles."""
        try:
            return es.cat.nodes(format="json", v=True)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def cat_shards(index: str = None):
        """List shards with state, docs, store, and node assignment."""
        try:
            return es.cat.shards(index=index, format="json", v=True)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def cat_allocation():
        """Show shard allocation per node — disk used, available, and shard count."""
        try:
            return es.cat.allocation(format="json", v=True)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def cat_segments(index: str = None):
        """Show low-level Lucene segment info per index."""
        try:
            return es.cat.segments(index=index, format="json", v=True)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def cat_recovery(index: str = None):
        """Show ongoing and completed shard recovery operations."""
        try:
            return es.cat.recovery(index=index, format="json", v=True)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def cat_aliases(name: str = None):
        """List index aliases. Optionally filter by alias name pattern."""
        try:
            return es.cat.aliases(name=name, format="json", v=True)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def cat_templates(name: str = None):
        """List index templates. Optionally filter by template name pattern."""
        try:
            return es.cat.templates(name=name, format="json", v=True)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}
