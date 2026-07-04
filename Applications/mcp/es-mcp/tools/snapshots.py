import elasticsearch


def register(mcp, es):

    @mcp.tool()
    def get_repositories(repository: str = None):
        """Get all snapshot repositories or a specific one by name."""
        try:
            return es.snapshot.get_repository(repository=repository)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def get_snapshots(repository: str, snapshot: str = "_all"):
        """
        List snapshots in a repository.
        Use snapshot="_all" for all, or pass a specific snapshot name.
        """
        try:
            return es.snapshot.get(repository=repository, snapshot=snapshot)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def create_snapshot(
        repository: str,
        snapshot: str,
        indices: list = None,
        wait_for_completion: bool = False,
    ):
        """
        Create a snapshot in a repository.
        Optionally specify indices to include; defaults to all indices.
        """
        try:
            body = {}
            if indices:
                body["indices"] = ",".join(indices)
            return es.snapshot.create(
                repository=repository,
                snapshot=snapshot,
                body=body if body else None,
                wait_for_completion=wait_for_completion,
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
    def delete_snapshot(repository: str, snapshot: str):
        """Delete a snapshot from a repository."""
        try:
            return es.snapshot.delete(repository=repository, snapshot=snapshot)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def restore_snapshot(
        repository: str,
        snapshot: str,
        indices: list = None,
        rename_pattern: str = None,
        rename_replacement: str = None,
        wait_for_completion: bool = False,
    ):
        """
        Restore a snapshot from a repository.
        Optionally filter indices and rename them on restore.
        """
        try:
            body = {}
            if indices:
                body["indices"] = ",".join(indices)
            if rename_pattern:
                body["rename_pattern"] = rename_pattern
            if rename_replacement:
                body["rename_replacement"] = rename_replacement
            return es.snapshot.restore(
                repository=repository,
                snapshot=snapshot,
                body=body if body else None,
                wait_for_completion=wait_for_completion,
            )
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}
