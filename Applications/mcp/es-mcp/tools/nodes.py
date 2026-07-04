import elasticsearch


def register(mcp, es):

    @mcp.tool()
    def node_stats(node_id: str = None, metric: str = None):
        """
        Return stats for all nodes or a specific node.
        node_id: node name or ID e.g. "Manishs-MacBook-Air.local"
        metric:  "jvm" | "os" | "process" | "indices" | "transport" | "http"
        """
        try:
            return es.nodes.stats(node_id=node_id, metric=metric)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def node_info(node_id: str = None, metric: str = None):
        """
        Return static info about nodes — version, roles, settings, plugins.
        metric: "settings" | "os" | "process" | "jvm" | "plugins" | "http"
        """
        try:
            return es.nodes.info(node_id=node_id, metric=metric)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def hot_threads(
        node_id: str = None,
        threads: int = 3,
        interval: str = "500ms",
        type: str = "cpu",
    ):
        """
        Return hot threads on each node — useful for diagnosing CPU spikes.
        type: "cpu" | "wait" | "block"
        """
        try:
            return es.nodes.hot_threads(
                node_id=node_id, threads=threads, interval=interval, type=type
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
    def node_usage(node_id: str = None):
        """Return per-node REST action usage stats — shows which APIs are called most."""
        try:
            return es.nodes.usage(node_id=node_id)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def reload_secure_settings(node_id: str = None, secure_settings_password: str = None):
        """
        Reload keystore secure settings on nodes without restarting.
        Useful after updating keystore entries (S3 credentials, SMTP passwords, etc.)
        """
        try:
            body = {}
            if secure_settings_password:
                body["secure_settings_password"] = secure_settings_password
            return es.nodes.reload_secure_settings(node_id=node_id, body=body if body else None)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}
