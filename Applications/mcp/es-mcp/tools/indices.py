import elasticsearch


def register(mcp, es):

    # ── CRUD ──────────────────────────────────────────────────────────────────

    @mcp.tool()
    def create_index(index: str, mappings: dict = None, settings: dict = None):
        """
        Create a new index with optional mappings and settings.
        Example mappings: {"properties": {"title": {"type": "text"}}}
        Example settings: {"number_of_shards": 1, "number_of_replicas": 0}
        """
        try:
            body = {}
            if mappings:
                body["mappings"] = mappings
            if settings:
                body["settings"] = settings
            return es.indices.create(index=index, body=body if body else None)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def delete_index(index: str):
        """Delete an index by name. Supports wildcards e.g. 'logs-*'. Irreversible."""
        try:
            return es.indices.delete(index=index)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    # ── Mappings & Settings ───────────────────────────────────────────────────

    @mcp.tool()
    def get_mapping(index: str):
        """Get field mappings for an index."""
        try:
            return es.indices.get_mapping(index=index)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def put_mapping(index: str, properties: dict):
        """
        Add or update field mappings on an existing index.
        Example: properties={"new_field": {"type": "keyword"}}
        """
        try:
            return es.indices.put_mapping(index=index, body={"properties": properties})
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def get_settings(index: str):
        """Get settings for an index."""
        try:
            return es.indices.get_settings(index=index)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def update_index_settings(index: str, settings: dict):
        """
        Update settings for an index.
        Example: settings={"number_of_replicas": 0}
        """
        try:
            return es.indices.put_settings(index=index, body={"index": settings})
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    # ── Aliases ───────────────────────────────────────────────────────────────

    @mcp.tool()
    def put_alias(index: str, name: str, is_write_index: bool = False, filter: dict = None):
        """Create or update an alias on an index."""
        try:
            body = {"is_write_index": is_write_index}
            if filter:
                body["filter"] = filter
            return es.indices.put_alias(index=index, name=name, body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def delete_alias(index: str, name: str):
        """Remove an alias from an index."""
        try:
            return es.indices.delete_alias(index=index, name=name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    # ── Legacy Templates ──────────────────────────────────────────────────────

    @mcp.tool()
    def get_index_template_legacy(name: str = None):
        """Get legacy index templates. Optionally filter by name pattern."""
        try:
            return es.indices.get_template(name=name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def put_index_template_legacy(name: str, body: dict):
        """
        Create or update a legacy index template.
        Example: body={"index_patterns": ["logs-*"], "settings": {"number_of_shards": 1}}
        """
        try:
            return es.indices.put_template(name=name, body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def delete_index_template_legacy(name: str):
        """Delete a legacy index template by name."""
        try:
            return es.indices.delete_template(name=name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    # ── Component Templates ───────────────────────────────────────────────────

    @mcp.tool()
    def get_component_template(name: str = None):
        """Get component templates. Optionally filter by name."""
        try:
            return es.cluster.get_component_template(name=name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def put_component_template(name: str, template: dict, version: int = None):
        """
        Create or update a component template.
        Example: template={"mappings": {"properties": {"host": {"type": "keyword"}}}}
        """
        try:
            body = {"template": template}
            if version is not None:
                body["version"] = version
            return es.cluster.put_component_template(name=name, body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def delete_component_template(name: str):
        """Delete a component template by name."""
        try:
            return es.cluster.delete_component_template(name=name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    # ── Composable Templates ──────────────────────────────────────────────────

    @mcp.tool()
    def get_composable_template(name: str = None):
        """Get composable (index) templates. Optionally filter by name."""
        try:
            return es.indices.get_index_template(name=name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def put_composable_template(
        name: str,
        index_patterns: list,
        composed_of: list = None,
        template: dict = None,
        priority: int = None,
        version: int = None,
    ):
        """
        Create or update a composable index template.
        Example: index_patterns=["metrics-*"], composed_of=["my-component"], priority=100
        """
        try:
            body = {"index_patterns": index_patterns}
            if composed_of:
                body["composed_of"] = composed_of
            if template:
                body["template"] = template
            if priority is not None:
                body["priority"] = priority
            if version is not None:
                body["version"] = version
            return es.indices.put_index_template(name=name, body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def delete_composable_template(name: str):
        """Delete a composable index template by name."""
        try:
            return es.indices.delete_index_template(name=name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}
