"""AtlasAI Code Intelligence and PCG Learning package."""
from .clangd_bridge import ClangdBridge
from .symbol_index import SymbolIndex, SymbolEntry
from .placement_pcg_bridge import PlacementPCGBridge, PlacementRecord
from .pcg_layout_learner import PCGLayoutLearner, LayoutSample
from .delta_edit_store import DeltaEditStore, DeltaEdit
from .scene_query_engine import SceneQueryEngine, SceneEntityRecord
from .layout_export_bridge import LayoutExportBridge, LayoutEntry
from .scene_graph_snapshot import SceneGraphSnapshot, SnapshotDiff
from .agent_action_log import AgentActionLog, ActionEntry
from .content_hash_registry import ContentHashRegistry, ContentHashEntry
from .content_pack_loader import ContentPackLoader, ContentPackManifest
from .ai_build_monitor import AIBuildMonitor, BuildDiagnostic, BuildSummary
from .layout_diff_reporter import LayoutDiffReporter, LayoutDiffReport, LayoutDiffEntry
from .runtime_bundle_loader import RuntimeBundleLoader, BundleManifest, AssetRef
from .asset_dependency_graph import AssetDependencyGraph, AssetNode
from .build_cache_manager import BuildCacheManager, CacheEntry
from .streaming_region_loader import StreamingRegionLoader, StreamingRegionManifest, RegionBounds
from .shader_permutation_cache import ShaderPermutationCache, ShaderVariant
from .asset_import_pipeline import AssetImportPipeline, ImportJob, ImportSettings
from .terrain_chunk_loader import TerrainChunkLoader, TerrainChunkManifest, ChunkCoord
from .texture_atlas_packer import TextureAtlasPacker, AtlasSheet, AtlasRegion
from .lod_generation_pipeline import LODGenerationPipeline, LODJob, LODSettings, LODResult
from .scene_partition_loader import ScenePartitionLoader, ScenePartitionManifest, PartitionBounds, PartitionPortal
from .mesh_simplification_pipeline import MeshSimplificationPipeline, SimplificationTarget, SimplificationResult, SimplificationBatch
from .animation_retarget_pipeline import AnimationRetargetPipeline, RetargetProfile, BoneMapping, RetargetJob, RetargetResult
from .nav_mesh_loader import NavMeshLoader, NavMeshManifest, NavMeshAABB, NavMeshNode, NavMeshEdge

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
    "AgentActionLog",
    "ActionEntry",
    "ContentHashRegistry",
    "ContentHashEntry",
    "ContentPackLoader",
    "ContentPackManifest",
    "AIBuildMonitor",
    "BuildDiagnostic",
    "BuildSummary",
    "LayoutDiffReporter",
    "LayoutDiffReport",
    "LayoutDiffEntry",
    "RuntimeBundleLoader",
    "BundleManifest",
    "AssetRef",
    "AssetDependencyGraph",
    "AssetNode",
    "BuildCacheManager",
    "CacheEntry",
    "StreamingRegionLoader",
    "StreamingRegionManifest",
    "RegionBounds",
    "ShaderPermutationCache",
    "ShaderVariant",
    "AssetImportPipeline",
    "ImportJob",
    "ImportSettings",
    "TerrainChunkLoader",
    "TerrainChunkManifest",
    "ChunkCoord",
    "TextureAtlasPacker",
    "AtlasSheet",
    "AtlasRegion",
    "LODGenerationPipeline",
    "LODJob",
    "LODSettings",
    "LODResult",
    "ScenePartitionLoader",
    "ScenePartitionManifest",
    "PartitionBounds",
    "PartitionPortal",
    "MeshSimplificationPipeline",
    "SimplificationTarget",
    "SimplificationResult",
    "SimplificationBatch",
    "AnimationRetargetPipeline",
    "RetargetProfile",
    "BoneMapping",
    "RetargetJob",
    "RetargetResult",
    "NavMeshLoader",
    "NavMeshManifest",
    "NavMeshAABB",
    "NavMeshNode",
    "NavMeshEdge",
]
