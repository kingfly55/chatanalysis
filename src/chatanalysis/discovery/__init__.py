"""Discovery layer for project and session inventory."""

from chatanalysis.discovery.inventory import (
    DiscoverySummary,
    InventoryRecord,
    ProjectRecord,
    discover_corpus,
)
from chatanalysis.discovery.lineage import derive_lineage
from chatanalysis.discovery.scoping import ScopedInventory, apply_scope
from chatanalysis.discovery.writer import write_discovery_artifacts

__all__ = [
    "DiscoverySummary",
    "InventoryRecord",
    "ProjectRecord",
    "ScopedInventory",
    "apply_scope",
    "derive_lineage",
    "discover_corpus",
    "write_discovery_artifacts",
]
