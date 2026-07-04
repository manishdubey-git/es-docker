import elasticsearch


def register(mcp, es):

    # ── Users ─────────────────────────────────────────────────────────────────

    @mcp.tool()
    def get_users(username: str = None):
        """Get all users or a specific user by username."""
        try:
            return es.security.get_user(username=username)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def put_user(
        username: str,
        password: str,
        roles: list,
        full_name: str = None,
        email: str = None,
        enabled: bool = True,
    ):
        """Create or update a native user."""
        try:
            body = {"password": password, "roles": roles, "enabled": enabled}
            if full_name:
                body["full_name"] = full_name
            if email:
                body["email"] = email
            return es.security.put_user(username=username, body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def delete_user(username: str):
        """Delete a native user by username."""
        try:
            return es.security.delete_user(username=username)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    # ── Roles ─────────────────────────────────────────────────────────────────

    @mcp.tool()
    def get_roles(name: str = None):
        """Get all roles or a specific role by name."""
        try:
            return es.security.get_role(name=name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def put_role(name: str, body: dict):
        """
        Create or update a security role.
        Example: body={"cluster": ["monitor"],
                        "indices": [{"names": ["logs-*"], "privileges": ["read"]}]}
        """
        try:
            return es.security.put_role(name=name, body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def delete_role(name: str):
        """Delete a security role by name."""
        try:
            return es.security.delete_role(name=name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    # ── Privileges ────────────────────────────────────────────────────────────

    @mcp.tool()
    def get_privileges(application: str = None, name: str = None):
        """Get application privileges. Optionally filter by application and privilege name."""
        try:
            return es.security.get_privileges(application=application, name=name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    # ── API Keys ──────────────────────────────────────────────────────────────

    @mcp.tool()
    def get_api_keys(
        id: str = None,
        name: str = None,
        username: str = None,
        realm_name: str = None,
    ):
        """Get API keys. Filter by id, name, username, or realm."""
        try:
            return es.security.get_api_key(id=id, name=name, username=username, realm_name=realm_name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def create_api_key(name: str, role_descriptors: dict = None, expiration: str = None):
        """
        Create an API key.
        Example expiration: "30d"
        """
        try:
            body = {"name": name}
            if role_descriptors:
                body["role_descriptors"] = role_descriptors
            if expiration:
                body["expiration"] = expiration
            return es.security.create_api_key(body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def invalidate_api_keys(ids: list = None, name: str = None, username: str = None):
        """Invalidate one or more API keys by id list, name, or username."""
        try:
            body = {}
            if ids:
                body["ids"] = ids
            if name:
                body["name"] = name
            if username:
                body["username"] = username
            return es.security.invalidate_api_key(body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    # ── Role Mappings ─────────────────────────────────────────────────────────

    @mcp.tool()
    def get_role_mappings(name: str = None):
        """Get role mappings. Optionally filter by name."""
        try:
            return es.security.get_role_mapping(name=name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def put_role_mapping(name: str, roles: list, rules: dict, enabled: bool = True):
        """
        Create or update a role mapping.
        Example rules: {"field": {"username": "johndoe"}}
        """
        try:
            return es.security.put_role_mapping(
                name=name,
                body={"roles": roles, "rules": rules, "enabled": enabled},
            )
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def delete_role_mapping(name: str):
        """Delete a role mapping by name."""
        try:
            return es.security.delete_role_mapping(name=name)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}
