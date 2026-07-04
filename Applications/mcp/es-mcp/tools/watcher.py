import elasticsearch


def register(mcp, es):

    @mcp.tool()
    def watcher_stats(metric: str = None):
        """
        Return watcher stats — queued watches, currently executing watches, etc.
        Optional metric: e.g. "queued_watches", "current_watches", "pending_watches"
        """
        try:
            kwargs = {}
            if metric is not None:
                kwargs["metric"] = metric
            return es.watcher.stats(**kwargs)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def watcher_status():
        """Return the watcher service status — whether it is started or stopped."""
        try:
            return es.watcher.get_settings()
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def start_watcher():
        """Start the watcher service."""
        try:
            return es.watcher.start()
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def stop_watcher():
        """Stop the watcher service."""
        try:
            return es.watcher.stop()
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def get_watch(watch_id: str):
        """Get the definition of a specific watch by its ID."""
        try:
            return es.watcher.get_watch(id=watch_id)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def put_watch(watch_id: str, body: dict):
        """
        Create or update a watch.
        body is the full watch definition. Example:
          {
            "trigger": {"schedule": {"interval": "10m"}},
            "input": {"search": {"request": {"indices": ["logs-*"], "body": {"query": {"match_all": {}}}}}},
            "condition": {"compare": {"ctx.payload.hits.total": {"gt": 0}}},
            "actions": {
              "log_error": {
                "logging": {"text": "Found {{ctx.payload.hits.total}} hits"}
              }
            }
          }
        """
        try:
            return es.watcher.put_watch(id=watch_id, body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def delete_watch(watch_id: str):
        """Delete a watch by its ID."""
        try:
            return es.watcher.delete_watch(id=watch_id)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def execute_watch(watch_id: str = None, body: dict = None):
        """
        Manually execute a watch — either an existing watch by ID or an inline watch definition.
        To run an existing watch: provide watch_id.
        To run an inline watch: provide body with a full watch definition.
        Example body for inline execution:
          {"watch": {"trigger": {"schedule": {"interval": "10m"}}, "input": {...}, "condition": {...}, "actions": {...}}}
        """
        try:
            kwargs = {}
            if watch_id is not None:
                kwargs["id"] = watch_id
            if body is not None:
                kwargs["body"] = body
            return es.watcher.execute_watch(**kwargs)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def ack_watch(watch_id: str, action_id: str = None):
        """
        Acknowledge a watch to suppress further alert actions until the watch condition is resolved.
        Optionally acknowledge only a specific action within the watch by providing action_id.
        """
        try:
            kwargs = {"watch_id": watch_id}
            if action_id is not None:
                kwargs["action_id"] = action_id
            return es.watcher.ack_watch(**kwargs)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def activate_watch(watch_id: str):
        """Activate a watch so it is eligible to be triggered."""
        try:
            return es.watcher.activate_watch(watch_id=watch_id)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def deactivate_watch(watch_id: str):
        """Deactivate a watch so it will no longer be triggered."""
        try:
            return es.watcher.deactivate_watch(watch_id=watch_id)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}
