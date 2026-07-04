from .cluster    import register as register_cluster
from .cat        import register as register_cat
from .search     import register as register_search
from .indices    import register as register_indices
from .nodes      import register as register_nodes
from .ilm        import register as register_ilm
from .snapshots  import register as register_snapshots
from .security   import register as register_security
from .ingest     import register as register_ingest
from .monitoring import register as register_monitoring
from .transforms import register as register_transforms
from .watcher    import register as register_watcher


def register_all(mcp, es):
    register_cluster(mcp, es)
    register_cat(mcp, es)
    register_search(mcp, es)
    register_indices(mcp, es)
    register_nodes(mcp, es)
    register_ilm(mcp, es)
    register_snapshots(mcp, es)
    register_security(mcp, es)
    register_ingest(mcp, es)
    register_monitoring(mcp, es)
    register_transforms(mcp, es)
    register_watcher(mcp, es)
