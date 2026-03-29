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
from .physics_simulation_cache import PhysicsSimulationCache, PhysicsSimulationEntry, PhysicsFrameData, CachePolicy
from .behavior_tree_compiler import BehaviorTreeCompiler, BTSourceTree, BTNodeDef, BTCompileResult, BTBytecodeInstruction
from .physics_body_loader import PhysicsBodyLoader, PhysicsBodyManifest, PhysicsMaterialDef, ColliderDef
from .audio_effect_pipeline import AudioEffectPipeline, AudioEffectJob, AudioProcessResult, EQBand, CompressorSettings, ReverbSettings, NormalisationSettings
from .cloth_simulation_cache import ClothSimulationCache, ClothSimEntry, ClothFrameSnapshot, ClothCachePolicy
from .audio_body_loader import AudioBodyLoader, AudioBodyManifest, AttenuationCurveDef, ReverbZoneDef
from .vfx_graph_compiler import VFXGraphCompiler, VFXEmitterNode, VFXLinkEdge, VFXGraphAsset
from .light_baking_pipeline import LightBakingPipeline, BakeJob, ProbeCluster, BakeResult
from .vfx_body_loader import VFXBodyLoader, VFXBodyManifest, EmitterBoundsDef, SimulationSettingsDef
from .particle_system_pipeline import ParticleSystemPipeline, ParticleEmitterDef, ParticleModuleDef, ParticlePipelineResult
from .procedural_mesh_pipeline import ProceduralMeshPipeline, MeshGenerationParams, MeshGenerationResult, ProceduralMeshBatch
from .animation_body_loader import AnimationBodyLoader, AnimationBodyManifest, AnimationClipDef, AnimationBlendWeightDef
from .render_pipeline_cache import RenderPipelineCache, RenderPassDef, RenderPipelineEntry, PipelineCacheStats
from .world_streaming_pipeline import WorldStreamingPipeline, StreamingZoneDef, StreamingLODRule, WorldStreamingResult
from .render_body_loader import RenderBodyLoader, RenderBodyManifest, MaterialSlotDef, LODEntryDef
from .lighting_bake_pipeline import LightingBakePipeline, BakePassDef, LightmapEntry, BakeBudget
from .collision_mesh_pipeline import CollisionMeshPipeline, CollisionShapeDef, CollisionMeshEntry, CollisionBuildResult
from .light_body_loader import LightBodyLoader, LightBodyManifest, LightColorDef, ShadowSettingsDef
from .vfx_bake_pipeline import VFXBakePipeline, VFXBakePassDef, VFXBakeEntry, VFXAtlasSettings
from .ik_solve_pipeline import IKSolvePipeline, IKJointDef, IKChainEntry, IKSolveResult
from .fx_body_loader import FXBodyLoader, FXBodyManifest, FXEmitSettingsDef, FXSimSettingsDef
from .gameplay_ability_pipeline import GameplayAbilityPipeline, AbilityEntry, AbilityCostDef, AbilityEffectDef
from .environment_query_pipeline import EnvironmentQueryPipeline, EQSGeneratorConfig, EQSTestConfig, EQSQueryResult
from .ui_body_loader import UIBodyLoader, UIBodyManifest, UIStyleManifest, UILayoutManifest
from .world_partition_pipeline import WorldPartitionPipeline, WorldPartitionEntry, StreamingCellDef, HLODLayerConfig
from .data_layer_pipeline import DataLayerPipeline, DataLayerSpec, DataLayerActorAssignment, DataLayerState
from .network_body_loader import NetworkBodyLoader, NetworkBodyManifest, ReplicationConfigManifest, NetworkPropertyManifest
from .matchmaking_pipeline import MatchmakingPipeline, MatchmakingRuleSet, MatchSession, MatchResult
from .conversation_graph_pipeline import ConversationGraphPipeline, ConversationNodeDef, ConversationEdgeDef, ConversationGraphEntry
from .game_body_loader import GameBodyLoader, GameBodyManifest, SpawnConfigManifest, GameEventManifest
from .ability_debug_pipeline import AbilityDebugPipeline, AbilitySnapshot, AttributeRecord, AbilityDebugFrame
from .landscape_spline_pipeline import LandscapeSplinePipeline, SplinePointDef, SplineSegmentDef, LandscapeSplineEntry
from .event_body_loader import EventBodyLoader, EventBodyManifest, TriggerConfigManifest, EventPayloadManifest
from .chaos_destruction_pipeline import (
    ChaosDestructionPipeline,
    GeometryCollectionEntry,
    GeometryFragmentDef,
    DestructionEventDef,
)
from .hair_groom_pipeline import (
    HairGroomPipeline,
    GroomAssetEntry,
    GroomStrandDef,
    GroomLODEntry,
)
from .script_body_loader import (
    ScriptBodyLoader,
    ScriptBodyManifest,
    ScriptConfigManifest,
    ScriptBindingManifest,
)
from .curve_linear_color_pipeline import (
    CurveLinearColorPipeline,
    ColorCurveEntry,
    ColorKeyframeEntry,
    GradientBakeDef,
)
from .network_profiler_pipeline import (
    NetworkProfilerPipeline,
    ProfilerSessionEntry,
    NetworkSampleEntry,
    NetworkAnomalyEntry,
)
from .dialog_body_loader import (
    DialogBodyLoader,
    DialogBodyManifest,
    DialogLineManifest,
    DialogResponseManifest,
)
from .morph_target_pipeline import (
    MorphTargetPipeline,
    MorphTargetEntry,
    CorrectiveShapeEntry,
    MorphBlendPresetEntry,
)
from .asset_bundle_pipeline import (
    AssetBundlePipeline,
    AssetBundleEntry,
    BundlePatchEntry,
    BundleManifestEntry,
)
from .quest_body_loader import (
    QuestBodyLoader,
    QuestBodyManifest,
    QuestObjectiveManifest,
    QuestRewardManifest,
)
from .rigid_body_joint_pipeline import (
    RigidBodyJointPipeline,
    JointEntry,
    JointConstraintEntry,
    JointVisualizationEntry,
)
from .data_validator_pipeline import (
    DataValidatorPipeline,
    ValidationRuleEntry,
    ValidationResultEntry,
    ValidationReportEntry,
)
from .achievement_body_loader import (
    AchievementBodyLoader,
    AchievementBodyManifest,
    AchievementProgressManifest,
    AchievementRewardManifest,
)
from .procedural_terrain_pipeline import (
    ProceduralTerrainPipeline,
    TerrainGenEntry,
    BiomeLayerEntry,
    ErosionSimEntry,
)
from .skeletal_mesh_pipeline import (
    SkeletalMeshPipeline,
    BoneEntry,
    WeightPaintEntry,
    MeshLODEntry,
)
from .inventory_body_loader import (
    InventoryBodyLoader,
    InventoryBodyManifest,
    InventoryItemManifest,
    InventorySlotManifest,
)
from .distance_field_pipeline import (
    DistanceFieldPipeline,
    DistanceFieldEntry,
    ShadowConfigEntry,
    FieldBlendOpEntry,
)
from .animation_compression_pipeline import (
    AnimationCompressionPipeline,
    CompressionSchemeEntry,
    TrackCompressionEntry,
    CompressionPreviewEntry,
)
from .loot_body_loader import (
    LootBodyLoader,
    LootBodyManifest,
    LootTableManifest,
    LootEntryManifest,
)
from .subsurface_scatter_pipeline import (
    SubsurfaceScatterPipeline,
    SSSProfileEntry,
    TransmissionEntry,
    SSSKernelEntry,
)
from .vector_field_pipeline import (
    VectorFieldPipeline,
    VectorFieldEntry,
    FlowVisualizationEntry,
    ParticleCouplingEntry,
)
from .trap_body_loader import (
    TrapBodyLoader,
    TrapBodyManifest,
    TrapTriggerZoneManifest,
    TrapEffectManifest,
)

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
    "PhysicsSimulationCache",
    "PhysicsSimulationEntry",
    "PhysicsFrameData",
    "CachePolicy",
    "BehaviorTreeCompiler",
    "BTSourceTree",
    "BTNodeDef",
    "BTCompileResult",
    "BTBytecodeInstruction",
    "PhysicsBodyLoader",
    "PhysicsBodyManifest",
    "PhysicsMaterialDef",
    "ColliderDef",
    "AudioEffectPipeline",
    "AudioEffectJob",
    "AudioProcessResult",
    "EQBand",
    "CompressorSettings",
    "ReverbSettings",
    "NormalisationSettings",
    "ClothSimulationCache",
    "ClothSimEntry",
    "ClothFrameSnapshot",
    "ClothCachePolicy",
    "AudioBodyLoader",
    "AudioBodyManifest",
    "AttenuationCurveDef",
    "ReverbZoneDef",
    "VFXGraphCompiler",
    "VFXEmitterNode",
    "VFXLinkEdge",
    "VFXGraphAsset",
    "LightBakingPipeline",
    "BakeJob",
    "ProbeCluster",
    "BakeResult",
    "VFXBodyLoader",
    "VFXBodyManifest",
    "EmitterBoundsDef",
    "SimulationSettingsDef",
    "ParticleSystemPipeline",
    "ParticleEmitterDef",
    "ParticleModuleDef",
    "ParticlePipelineResult",
    "ProceduralMeshPipeline",
    "MeshGenerationParams",
    "MeshGenerationResult",
    "ProceduralMeshBatch",
    "AnimationBodyLoader",
    "AnimationBodyManifest",
    "AnimationClipDef",
    "AnimationBlendWeightDef",
    "RenderPipelineCache",
    "RenderPassDef",
    "RenderPipelineEntry",
    "PipelineCacheStats",
    "WorldStreamingPipeline",
    "StreamingZoneDef",
    "StreamingLODRule",
    "WorldStreamingResult",
    "RenderBodyLoader",
    "RenderBodyManifest",
    "MaterialSlotDef",
    "LODEntryDef",
    "LightingBakePipeline",
    "BakePassDef",
    "LightmapEntry",
    "BakeBudget",
    "CollisionMeshPipeline",
    "CollisionShapeDef",
    "CollisionMeshEntry",
    "CollisionBuildResult",
    "LightBodyLoader",
    "LightBodyManifest",
    "LightColorDef",
    "ShadowSettingsDef",
    "VFXBakePipeline",
    "VFXBakePassDef",
    "VFXBakeEntry",
    "VFXAtlasSettings",
    "IKSolvePipeline",
    "IKJointDef",
    "IKChainEntry",
    "IKSolveResult",
    "FXBodyLoader",
    "FXBodyManifest",
    "FXEmitSettingsDef",
    "FXSimSettingsDef",
    "GameplayAbilityPipeline",
    "AbilityEntry",
    "AbilityCostDef",
    "AbilityEffectDef",
    "EnvironmentQueryPipeline",
    "EQSGeneratorConfig",
    "EQSTestConfig",
    "EQSQueryResult",
    "UIBodyLoader",
    "UIBodyManifest",
    "UIStyleManifest",
    "UILayoutManifest",
    "WorldPartitionPipeline",
    "WorldPartitionEntry",
    "StreamingCellDef",
    "HLODLayerConfig",
    "DataLayerPipeline",
    "DataLayerSpec",
    "DataLayerActorAssignment",
    "DataLayerState",
    "NetworkBodyLoader",
    "NetworkBodyManifest",
    "ReplicationConfigManifest",
    "NetworkPropertyManifest",
    "MatchmakingPipeline",
    "MatchmakingRuleSet",
    "MatchSession",
    "MatchResult",
    "ConversationGraphPipeline",
    "ConversationNodeDef",
    "ConversationEdgeDef",
    "ConversationGraphEntry",
    "GameBodyLoader",
    "GameBodyManifest",
    "SpawnConfigManifest",
    "GameEventManifest",
    "AbilityDebugPipeline",
    "AbilitySnapshot",
    "AttributeRecord",
    "AbilityDebugFrame",
    "LandscapeSplinePipeline",
    "SplinePointDef",
    "SplineSegmentDef",
    "LandscapeSplineEntry",
    "EventBodyLoader",
    "EventBodyManifest",
    "TriggerConfigManifest",
    "EventPayloadManifest",
    "ChaosDestructionPipeline", "GeometryCollectionEntry", "GeometryFragmentDef", "DestructionEventDef",
    "HairGroomPipeline", "GroomAssetEntry", "GroomStrandDef", "GroomLODEntry",
    "ScriptBodyLoader", "ScriptBodyManifest", "ScriptConfigManifest", "ScriptBindingManifest",
    "CurveLinearColorPipeline", "ColorCurveEntry", "ColorKeyframeEntry", "GradientBakeDef",
    "NetworkProfilerPipeline", "ProfilerSessionEntry", "NetworkSampleEntry", "NetworkAnomalyEntry",
    "DialogBodyLoader", "DialogBodyManifest", "DialogLineManifest", "DialogResponseManifest",
    "MorphTargetPipeline", "MorphTargetEntry", "CorrectiveShapeEntry", "MorphBlendPresetEntry",
    "AssetBundlePipeline", "AssetBundleEntry", "BundlePatchEntry", "BundleManifestEntry",
    "QuestBodyLoader", "QuestBodyManifest", "QuestObjectiveManifest", "QuestRewardManifest",
    "RigidBodyJointPipeline", "JointEntry", "JointConstraintEntry", "JointVisualizationEntry",
    "DataValidatorPipeline", "ValidationRuleEntry", "ValidationResultEntry", "ValidationReportEntry",
    "AchievementBodyLoader", "AchievementBodyManifest", "AchievementProgressManifest", "AchievementRewardManifest",
    "ProceduralTerrainPipeline", "TerrainGenEntry", "BiomeLayerEntry", "ErosionSimEntry",
    "SkeletalMeshPipeline", "BoneEntry", "WeightPaintEntry", "MeshLODEntry",
    "InventoryBodyLoader", "InventoryBodyManifest", "InventoryItemManifest", "InventorySlotManifest",
    "DistanceFieldPipeline", "DistanceFieldEntry", "ShadowConfigEntry", "FieldBlendOpEntry",
    "AnimationCompressionPipeline", "CompressionSchemeEntry", "TrackCompressionEntry", "CompressionPreviewEntry",
    "LootBodyLoader", "LootBodyManifest", "LootTableManifest", "LootEntryManifest",
    "SubsurfaceScatterPipeline", "SSSProfileEntry", "TransmissionEntry", "SSSKernelEntry",
    "VectorFieldPipeline", "VectorFieldEntry", "FlowVisualizationEntry", "ParticleCouplingEntry",
    "TrapBodyLoader", "TrapBodyManifest", "TrapTriggerZoneManifest", "TrapEffectManifest",
]
