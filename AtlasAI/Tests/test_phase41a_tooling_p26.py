"""Phase 41A — Tests for P26 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P26_TOOLS = [
    "ProceduralTerrainTool",
    "SkeletalMeshEditorTool",
    "MaterialFunctionLibraryTool",
    "NavModifierVolumeTool",
    "AudioSpatializationTool",
    "SceneCaptureTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP26ToolsExist(unittest.TestCase):
    def test_procedural_terrain_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ProceduralTerrainTool.h").exists())

    def test_skeletal_mesh_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SkeletalMeshEditorTool.h").exists())

    def test_material_function_library_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MaterialFunctionLibraryTool.h").exists())

    def test_nav_modifier_volume_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "NavModifierVolumeTool.h").exists())

    def test_audio_spatialization_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AudioSpatializationTool.h").exists())

    def test_scene_capture_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SceneCaptureTool.h").exists())


class TestP26PragmaOnce(unittest.TestCase):
    def test_procedural_terrain_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("ProceduralTerrainTool"))

    def test_skeletal_mesh_editor_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("SkeletalMeshEditorTool"))

    def test_material_function_library_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("MaterialFunctionLibraryTool"))

    def test_nav_modifier_volume_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("NavModifierVolumeTool"))

    def test_audio_spatialization_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("AudioSpatializationTool"))

    def test_scene_capture_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("SceneCaptureTool"))


class TestP26ToolName(unittest.TestCase):
    def test_procedural_terrain_tool_class_name(self):
        self.assertIn("ProceduralTerrainTool", _read("ProceduralTerrainTool"))

    def test_skeletal_mesh_editor_tool_class_name(self):
        self.assertIn("SkeletalMeshEditorTool", _read("SkeletalMeshEditorTool"))

    def test_material_function_library_tool_class_name(self):
        self.assertIn("MaterialFunctionLibraryTool", _read("MaterialFunctionLibraryTool"))

    def test_nav_modifier_volume_tool_class_name(self):
        self.assertIn("NavModifierVolumeTool", _read("NavModifierVolumeTool"))

    def test_audio_spatialization_tool_class_name(self):
        self.assertIn("AudioSpatializationTool", _read("AudioSpatializationTool"))

    def test_scene_capture_tool_class_name(self):
        self.assertIn("SceneCaptureTool", _read("SceneCaptureTool"))


class TestP26ITool(unittest.TestCase):
    def test_procedural_terrain_tool_itool(self):
        self.assertIn(": public ITool", _read("ProceduralTerrainTool"))

    def test_skeletal_mesh_editor_tool_itool(self):
        self.assertIn(": public ITool", _read("SkeletalMeshEditorTool"))

    def test_material_function_library_tool_itool(self):
        self.assertIn(": public ITool", _read("MaterialFunctionLibraryTool"))

    def test_nav_modifier_volume_tool_itool(self):
        self.assertIn(": public ITool", _read("NavModifierVolumeTool"))

    def test_audio_spatialization_tool_itool(self):
        self.assertIn(": public ITool", _read("AudioSpatializationTool"))

    def test_scene_capture_tool_itool(self):
        self.assertIn(": public ITool", _read("SceneCaptureTool"))


class TestProceduralTerrainToolDetail(unittest.TestCase):
    def test_generation_mode_enum(self):
        self.assertIn("GenerationMode", _read("ProceduralTerrainTool"))

    def test_biome_type_enum(self):
        self.assertIn("BiomeType", _read("ProceduralTerrainTool"))

    def test_erosion_type_enum(self):
        self.assertIn("ErosionType", _read("ProceduralTerrainTool"))

    def test_terrain_gen_def_struct(self):
        self.assertIn("TerrainGenDef", _read("ProceduralTerrainTool"))

    def test_biome_layer_def_struct(self):
        self.assertIn("BiomeLayerDef", _read("ProceduralTerrainTool"))

    def test_erosion_sim_def_struct(self):
        self.assertIn("ErosionSimDef", _read("ProceduralTerrainTool"))

    def test_create_terrain_method(self):
        self.assertIn("CreateTerrain", _read("ProceduralTerrainTool"))

    def test_add_biome_layer_method(self):
        self.assertIn("AddBiomeLayer", _read("ProceduralTerrainTool"))

    def test_run_erosion_method(self):
        self.assertIn("RunErosion", _read("ProceduralTerrainTool"))

    def test_export_heightmap_method(self):
        self.assertIn("ExportHeightmap", _read("ProceduralTerrainTool"))


class TestSkeletalMeshEditorToolDetail(unittest.TestCase):
    def test_edit_mode_enum(self):
        self.assertIn("EditMode", _read("SkeletalMeshEditorTool"))

    def test_weight_mode_enum(self):
        self.assertIn("WeightMode", _read("SkeletalMeshEditorTool"))

    def test_bone_def_struct(self):
        self.assertIn("BoneDef", _read("SkeletalMeshEditorTool"))

    def test_weight_paint_entry_struct(self):
        self.assertIn("WeightPaintEntry", _read("SkeletalMeshEditorTool"))

    def test_mesh_lod_entry_struct(self):
        self.assertIn("MeshLODEntry", _read("SkeletalMeshEditorTool"))

    def test_add_bone_method(self):
        self.assertIn("AddBone", _read("SkeletalMeshEditorTool"))

    def test_apply_weight_paint_method(self):
        self.assertIn("ApplyWeightPaint", _read("SkeletalMeshEditorTool"))

    def test_generate_lod_method(self):
        self.assertIn("GenerateLOD", _read("SkeletalMeshEditorTool"))

    def test_mesh_lod_strategy_enum(self):
        self.assertIn("MeshLODStrategy", _read("SkeletalMeshEditorTool"))


class TestMaterialFunctionLibraryToolDetail(unittest.TestCase):
    def test_function_category_enum(self):
        self.assertIn("FunctionCategory", _read("MaterialFunctionLibraryTool"))

    def test_parameter_type_enum(self):
        self.assertIn("ParameterType", _read("MaterialFunctionLibraryTool"))

    def test_function_scope_enum(self):
        self.assertIn("FunctionScope", _read("MaterialFunctionLibraryTool"))

    def test_material_function_def_struct(self):
        self.assertIn("MaterialFunctionDef", _read("MaterialFunctionLibraryTool"))

    def test_function_parameter_def_struct(self):
        self.assertIn("FunctionParameterDef", _read("MaterialFunctionLibraryTool"))

    def test_function_output_def_struct(self):
        self.assertIn("FunctionOutputDef", _read("MaterialFunctionLibraryTool"))

    def test_create_function_method(self):
        self.assertIn("CreateFunction", _read("MaterialFunctionLibraryTool"))

    def test_publish_function_method(self):
        self.assertIn("PublishFunction", _read("MaterialFunctionLibraryTool"))

    def test_expose_parameter_method(self):
        self.assertIn("ExposeParameter", _read("MaterialFunctionLibraryTool"))


class TestNavModifierVolumeToolDetail(unittest.TestCase):
    def test_volume_shape_enum(self):
        self.assertIn("VolumeShape", _read("NavModifierVolumeTool"))

    def test_nav_area_type_enum(self):
        self.assertIn("NavAreaType", _read("NavModifierVolumeTool"))

    def test_agent_type_enum(self):
        self.assertIn("AgentType", _read("NavModifierVolumeTool"))

    def test_nav_modifier_volume_def_struct(self):
        self.assertIn("NavModifierVolumeDef", _read("NavModifierVolumeTool"))

    def test_agent_cost_override_def_struct(self):
        self.assertIn("AgentCostOverrideDef", _read("NavModifierVolumeTool"))

    def test_nav_area_flag_def_struct(self):
        self.assertIn("NavAreaFlagDef", _read("NavModifierVolumeTool"))

    def test_create_volume_method(self):
        self.assertIn("CreateVolume", _read("NavModifierVolumeTool"))

    def test_set_area_type_method(self):
        self.assertIn("SetAreaType", _read("NavModifierVolumeTool"))

    def test_add_agent_cost_override_method(self):
        self.assertIn("AddAgentCostOverride", _read("NavModifierVolumeTool"))


class TestAudioSpatializationToolDetail(unittest.TestCase):
    def test_spatialization_algorithm_enum(self):
        self.assertIn("SpatializationAlgorithm", _read("AudioSpatializationTool"))

    def test_attenuation_model_enum(self):
        self.assertIn("AttenuationModel", _read("AudioSpatializationTool"))

    def test_reverb_preset_enum(self):
        self.assertIn("ReverbPreset", _read("AudioSpatializationTool"))

    def test_spatialization_profile_def_struct(self):
        self.assertIn("SpatializationProfileDef", _read("AudioSpatializationTool"))

    def test_reverb_zone_def_struct(self):
        self.assertIn("ReverbZoneDef", _read("AudioSpatializationTool"))

    def test_audio_source_binding_def_struct(self):
        self.assertIn("AudioSourceBindingDef", _read("AudioSpatializationTool"))

    def test_create_profile_method(self):
        self.assertIn("CreateProfile", _read("AudioSpatializationTool"))

    def test_create_reverb_zone_method(self):
        self.assertIn("CreateReverbZone", _read("AudioSpatializationTool"))

    def test_bind_audio_source_method(self):
        self.assertIn("BindAudioSource", _read("AudioSpatializationTool"))

    def test_occlusion_type_enum(self):
        self.assertIn("OcclusionType", _read("AudioSpatializationTool"))


class TestSceneCaptureToolDetail(unittest.TestCase):
    def test_capture_type_enum(self):
        self.assertIn("CaptureType", _read("SceneCaptureTool"))

    def test_capture_resolution_enum(self):
        self.assertIn("CaptureResolution", _read("SceneCaptureTool"))

    def test_update_mode_enum(self):
        self.assertIn("UpdateMode", _read("SceneCaptureTool"))

    def test_scene_capture_def_struct(self):
        self.assertIn("SceneCaptureDef", _read("SceneCaptureTool"))

    def test_render_target_def_struct(self):
        self.assertIn("RenderTargetDef", _read("SceneCaptureTool"))

    def test_capture_filter_def_struct(self):
        self.assertIn("CaptureFilterDef", _read("SceneCaptureTool"))

    def test_create_capture_method(self):
        self.assertIn("CreateCapture", _read("SceneCaptureTool"))

    def test_trigger_capture_method(self):
        self.assertIn("TriggerCapture", _read("SceneCaptureTool"))

    def test_create_render_target_method(self):
        self.assertIn("CreateRenderTarget", _read("SceneCaptureTool"))

    def test_set_update_mode_method(self):
        self.assertIn("SetUpdateMode", _read("SceneCaptureTool"))


if __name__ == "__main__":
    unittest.main()
