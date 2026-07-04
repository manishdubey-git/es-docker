import elasticsearch


def register(mcp, es):

    @mcp.tool()
    def search(index: str, keyword: str):
        """Full-text search across all text fields using multi_match."""
        try:
            body = {"query": {"multi_match": {"query": keyword, "fields": ["*"]}}}
            return es.search(index=index, body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def advanced_search(
        index: str,
        query: dict,
        size: int = 10,
        from_: int = 0,
        sort: list = None,
        source: list = None,
        aggs: dict = None,
    ):
        """
        Execute a full Elasticsearch query DSL search.

        Examples:
          Term:    query={"term": {"category": "Smartphones"}}
          Range:   query={"range": {"price": {"gte": 500, "lte": 1500}}}
          Bool:    query={"bool": {"must": [...], "filter": [...]}}
          Match all + aggs: query={"match_all": {}}, size=0,
                            aggs={"by_cat": {"terms": {"field": "category"}}}
        """
        try:
            body = {"query": query, "size": size, "from": from_}
            if sort:
                body["sort"] = sort
            if source:
                body["_source"] = source
            if aggs:
                body["aggs"] = aggs
            return es.search(index=index, body=body)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def count(index: str):
        """Return document count for an index."""
        try:
            return es.count(index=index)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def explain(index: str, doc_id: str, query: dict):
        """
        Explain why a document matches or doesn't match a query.
        Example: query={"match": {"description": "wireless"}}
        """
        try:
            return es.explain(index=index, id=doc_id, body={"query": query})
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def validate_query(index: str, query: dict, explain: bool = True):
        """
        Validate a query without executing it.
        Example: query={"match": {"message": "error"}}
        """
        try:
            return es.indices.validate_query(index=index, body={"query": query}, explain=explain)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def profile(index: str, query: dict):
        """
        Profile a search query to understand execution time breakdown.
        Example: query={"match": {"description": "wireless"}}
        """
        try:
            return es.search(index=index, body={"profile": True, "query": query})
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def msearch(searches: list):
        """
        Execute multiple searches in one request.
        Alternating header + body pairs:
          [{"index": "my-index"}, {"query": {"match_all": {}}}, ...]
        """
        try:
            return es.msearch(body=searches)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}

    @mcp.tool()
    def async_search(index: str, query: dict, wait_for_completion_timeout: str = "1s"):
        """
        Submit a long-running search asynchronously.
        Returns a search ID if not complete within wait_for_completion_timeout.
        """
        try:
            return es.async_search.submit(
                index=index,
                body={"query": query},
                wait_for_completion_timeout=wait_for_completion_timeout,
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
    def get_async_search(search_id: str, wait_for_completion_timeout: str = "1s"):
        """Retrieve results of a previously submitted async search by its ID."""
        try:
            return es.async_search.get(
                id=search_id,
                wait_for_completion_timeout=wait_for_completion_timeout,
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
    def delete_async_search(search_id: str):
        """Delete an async search and free its resources."""
        try:
            return es.async_search.delete(id=search_id)
        except elasticsearch.ConnectionError as e:
            return {"error": "ConnectionError", "message": f"Could not connect to Elasticsearch: {e}"}
        except elasticsearch.AuthenticationException as e:
            return {"error": "AuthenticationException", "message": f"Authentication failed: {e}"}
        except elasticsearch.NotFoundError as e:
            return {"error": "NotFoundError", "message": f"Resource not found: {e}"}
        except elasticsearch.BadRequestError as e:
            return {"error": "BadRequestError", "message": f"Bad request: {e}"}
