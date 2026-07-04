def register(mcp, es):

    @mcp.tool()
    def monitoring_stats():
        """
        Return cluster-wide monitoring stats covering nodes, indices, JVM, OS, and process.

        Combines cluster-level stats (index counts, shard counts, memory) with
        per-node stats (JVM heap, OS load, process info, transport, HTTP).
        """
        cluster = es.cluster.stats()
        nodes = es.nodes.stats(metric=["jvm", "os", "process", "indices", "transport", "http"])
        return {
            "cluster": cluster,
            "nodes": nodes,
        }
