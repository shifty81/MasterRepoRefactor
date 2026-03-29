"""AtlasAI Code Intelligence and PCG Learning package."""
from .clangd_bridge import ClangdBridge
from .symbol_index import SymbolIndex, SymbolEntry
from .placement_pcg_bridge import PlacementPCGBridge, PlacementRecord
from .pcg_layout_learner import PCGLayoutLearner, LayoutSample
from .delta_edit_store import DeltaEditStore, DeltaEdit
from .scene_query_engine import SceneQueryEngine, SceneEntityRecord
from .layout_export_bridge import LayoutExportBridge, LayoutEntry
from .scene_graph_snapshot import SceneGraphSnapshot, SnapshotDiff

__all__ = [
    "ClangdBridge",
    "SymbolIndex",
    "SymbolEntry",
    "PlacementPCGBridge",
    "PlacementRecord",
    "PCGLayoutLearner",
    "LayoutSample",
    "DeltaEditStore",
    "DeltaEdit",
    "SceneQueryEngine",
    "SceneEntityRecord",
    "LayoutExportBridge",
    "LayoutEntry",
    "SceneGraphSnapshot",
    "SnapshotDiff",
]
