import elasticsearch


def register(mcp, es):

    @mcp.tool()
    def get_transforms(transform_id: str = None):
        """
        Get all transforms or a specific one by ID.
        Leave transform_id empty to list all transforms.
        """
        try:
            if transform_id:
                return es.transform.get_transform(transform_id=transform_id)
            return es.transform.get_transform(transform_id="_all")
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def put_transform(
        transform_id: str,
        source: dict,
        dest: dict,
        pivot: dict = None,
        latest: dict = None,
        description: str = None,
    ):
        """
        Create or update a transform.
        Example source: {"index": ["logs-*"], "query": {"match_all": {}}}
        Example dest:   {"index": "logs-summary"}
        Example pivot:  {"group_by": {"host": {"terms": {"field": "host.keyword"}}},
                         "aggregations": {"avg_bytes": {"avg": {"field": "bytes"}}}}
        Example latest: {"unique_key": ["host.keyword"], "sort": "@timestamp"}
        """
        try:
            body = {"source": source, "dest": dest}
            if pivot is not None:
                body["pivot"] = pivot
            if latest is not None:
                body["latest"] = latest
            if description is not None:
                body["description"] = description
            return es.transform.put_transform(transform_id=transform_id, body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def delete_transform(transform_id: str, force: bool = False):
        """
        Delete a transform by ID.
        Set force=True to delete a transform that is not stopped.
        """
        try:
            return es.transform.delete_transform(transform_id=transform_id, force=force)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def start_transform(transform_id: str):
        """Start a transform by ID."""
        try:
            return es.transform.start_transform(transform_id=transform_id)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def stop_transform(transform_id: str, wait_for_completion: bool = False):
        """
        Stop a transform by ID.
        Set wait_for_completion=True to block until the transform fully stops.
        """
        try:
            return es.transform.stop_transform(
                transform_id=transform_id,
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
    def get_transform_stats(transform_id: str = None):
        """
        Get stats for all transforms or a specific one.
        Returns docs processed, state, checkpointing info, and more.
        Leave transform_id empty to get stats for all transforms.
        """
        try:
            tid = transform_id if transform_id else "_all"
            return es.transform.get_transform_stats(transform_id=tid)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def preview_transform(
        transform_id: str = None,
        source: dict = None,
        pivot: dict = None,
        latest: dict = None,
    ):
        """
        Preview the output of a transform without running it.
        Pass transform_id to preview an existing transform, or provide
        source + pivot/latest inline to preview a new transform definition.
        Example source: {"index": ["logs-*"], "query": {"match_all": {}}}
        Example pivot:  {"group_by": {"host": {"terms": {"field": "host.keyword"}}},
                         "aggregations": {"count": {"value_count": {"field": "_index"}}}}
        """
        try:
            if transform_id:
                return es.transform.preview_transform(transform_id=transform_id)
            body = {}
            if source is not None:
                body["source"] = source
            if pivot is not None:
                body["pivot"] = pivot
            if latest is not None:
                body["latest"] = latest
            return es.transform.preview_transform(body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}
