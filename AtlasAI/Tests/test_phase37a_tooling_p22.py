"""Phase 37A — Tests for P22 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P22_TOOLS = [
    "ChaosDestructionTool",
    "HairGroomTool",
    "RuntimeVirtualTextureTool",
    "WaterBodyTool",
    "PCGAttributeTool",
    "SoundCueTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP22ToolsExist(unittest.TestCase):
    def test_chaos_destruction_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ChaosDestructionTool.h").exists())

    def test_hair_groom_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "HairGroomTool.h").exists())

    def test_runtime_virtual_texture_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "RuntimeVirtualTextureTool.h").exists())

    def test_water_body_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "WaterBodyTool.h").exists())

    def test_pcg_attribute_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "PCGAttributeTool.h").exists())

    def test_sound_cue_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SoundCueTool.h").exists())


class TestP22PragmaOnce(unittest.TestCase):
    def test_chaos_destruction_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("ChaosDestructionTool"))

    def test_hair_groom_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("HairGroomTool"))

    def test_runtime_virtual_texture_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("RuntimeVirtualTextureTool"))

    def test_water_body_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("WaterBodyTool"))

    def test_pcg_attribute_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("PCGAttributeTool"))

    def test_sound_cue_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("SoundCueTool"))


class TestP22ToolName(unittest.TestCase):
    def test_chaos_destruction_tool_class_name(self):
        self.assertIn("ChaosDestructionTool", _read("ChaosDestructionTool"))

    def test_hair_groom_tool_class_name(self):
        self.assertIn("HairGroomTool", _read("HairGroomTool"))

    def test_runtime_virtual_texture_tool_class_name(self):
        self.assertIn("RuntimeVirtualTextureTool", _read("RuntimeVirtualTextureTool"))

    def test_water_body_tool_class_name(self):
        self.assertIn("WaterBodyTool", _read("WaterBodyTool"))

    def test_pcg_attribute_tool_class_name(self):
        self.assertIn("PCGAttributeTool", _read("PCGAttributeTool"))

    def test_sound_cue_tool_class_name(self):
        self.assertIn("SoundCueTool", _read("SoundCueTool"))


class TestP22ITool(unittest.TestCase):
    def test_chaos_destruction_tool_itool(self):
        self.assertIn(": public ITool", _read("ChaosDestructionTool"))

    def test_hair_groom_tool_itool(self):
        self.assertIn(": public ITool", _read("HairGroomTool"))

    def test_runtime_virtual_texture_tool_itool(self):
        self.assertIn(": public ITool", _read("RuntimeVirtualTextureTool"))

    def test_water_body_tool_itool(self):
        self.assertIn(": public ITool", _read("WaterBodyTool"))

    def test_pcg_attribute_tool_itool(self):
        self.assertIn(": public ITool", _read("PCGAttributeTool"))

    def test_sound_cue_tool_itool(self):
        self.assertIn(": public ITool", _read("SoundCueTool"))


class TestChaosDestructionToolDetail(unittest.TestCase):
    def test_destruction_mode_enum(self):
        self.assertIn("DestructionMode", _read("ChaosDestructionTool"))

    def test_fragment_policy_enum(self):
        self.assertIn("FragmentPolicy", _read("ChaosDestructionTool"))

    def test_geometry_collection_def_struct(self):
        self.assertIn("GeometryCollectionDef", _read("ChaosDestructionTool"))

    def test_cluster_id_in_struct(self):
        self.assertIn("clusterId", _read("ChaosDestructionTool"))

    def test_destruction_event_record_struct(self):
        self.assertIn("DestructionEventRecord", _read("ChaosDestructionTool"))

    def test_damage_amount_in_event(self):
        self.assertIn("damageAmount", _read("ChaosDestructionTool"))

    def test_fragment_config_def_struct(self):
        self.assertIn("FragmentConfigDef", _read("ChaosDestructionTool"))

    def test_min_fragment_volume_in_config(self):
        self.assertIn("minFragmentVolume", _read("ChaosDestructionTool"))

    def test_create_geometry_collection_method(self):
        self.assertIn("CreateGeometryCollection", _read("ChaosDestructionTool"))

    def test_record_destruction_event_method(self):
        self.assertIn("RecordDestructionEvent", _read("ChaosDestructionTool"))

    def test_get_events_by_collection_method(self):
        self.assertIn("GetEventsByCollection", _read("ChaosDestructionTool"))

    def test_flush_event_log_method(self):
        self.assertIn("FlushEventLog", _read("ChaosDestructionTool"))


class TestHairGroomToolDetail(unittest.TestCase):
    def test_groom_sim_mode_enum(self):
        self.assertIn("GroomSimMode", _read("HairGroomTool"))

    def test_strand_render_mode_enum(self):
        self.assertIn("StrandRenderMode", _read("HairGroomTool"))

    def test_groom_asset_def_struct(self):
        self.assertIn("GroomAssetDef", _read("HairGroomTool"))

    def test_strand_count_in_struct(self):
        self.assertIn("strandCount", _read("HairGroomTool"))

    def test_groom_sim_config_struct(self):
        self.assertIn("GroomSimConfig", _read("HairGroomTool"))

    def test_simulation_substeps_in_config(self):
        self.assertIn("simulationSubsteps", _read("HairGroomTool"))

    def test_groom_lod_def_struct(self):
        self.assertIn("GroomLODDef", _read("HairGroomTool"))

    def test_screen_size_in_lod(self):
        self.assertIn("screenSize", _read("HairGroomTool"))

    def test_register_groom_asset_method(self):
        self.assertIn("RegisterGroomAsset", _read("HairGroomTool"))

    def test_apply_sim_config_method(self):
        self.assertIn("ApplySimConfig", _read("HairGroomTool"))

    def test_add_lod_method(self):
        self.assertIn("AddLOD", _read("HairGroomTool"))

    def test_set_wind_response_method(self):
        self.assertIn("SetWindResponse", _read("HairGroomTool"))


class TestRuntimeVirtualTextureToolDetail(unittest.TestCase):
    def test_rvt_layout_enum(self):
        self.assertIn("RVTLayout", _read("RuntimeVirtualTextureTool"))

    def test_rvt_streaming_mode_enum(self):
        self.assertIn("RVTStreamingMode", _read("RuntimeVirtualTextureTool"))

    def test_rvt_volume_def_struct(self):
        self.assertIn("RVTVolumeDef", _read("RuntimeVirtualTextureTool"))

    def test_bounds_extent_in_struct(self):
        self.assertIn("boundsExtent", _read("RuntimeVirtualTextureTool"))

    def test_rvt_material_binding_struct(self):
        self.assertIn("RVTMaterialBinding", _read("RuntimeVirtualTextureTool"))

    def test_material_id_in_binding(self):
        self.assertIn("materialId", _read("RuntimeVirtualTextureTool"))

    def test_rvt_build_config_struct(self):
        self.assertIn("RVTBuildConfig", _read("RuntimeVirtualTextureTool"))

    def test_tile_size_in_config(self):
        self.assertIn("tileSize", _read("RuntimeVirtualTextureTool"))

    def test_create_rvt_volume_method(self):
        self.assertIn("CreateRVTVolume", _read("RuntimeVirtualTextureTool"))

    def test_trigger_build_method(self):
        self.assertIn("TriggerBuild", _read("RuntimeVirtualTextureTool"))

    def test_invalidate_cache_method(self):
        self.assertIn("InvalidateCache", _read("RuntimeVirtualTextureTool"))

    def test_get_volumes_with_layout_method(self):
        self.assertIn("GetVolumesWithLayout", _read("RuntimeVirtualTextureTool"))


class TestWaterBodyToolDetail(unittest.TestCase):
    def test_water_body_type_enum(self):
        self.assertIn("WaterBodyType", _read("WaterBodyTool"))

    def test_wave_type_enum(self):
        self.assertIn("WaveType", _read("WaterBodyTool"))

    def test_water_body_def_struct(self):
        self.assertIn("WaterBodyDef", _read("WaterBodyTool"))

    def test_depth_level_in_struct(self):
        self.assertIn("depthLevel", _read("WaterBodyTool"))

    def test_wave_settings_def_struct(self):
        self.assertIn("WaveSettingsDef", _read("WaterBodyTool"))

    def test_wave_height_in_struct(self):
        self.assertIn("waveHeight", _read("WaterBodyTool"))

    def test_buoyancy_config_struct(self):
        self.assertIn("BuoyancyConfig", _read("WaterBodyTool"))

    def test_pontoon_count_in_config(self):
        self.assertIn("pontoonCount", _read("WaterBodyTool"))

    def test_register_water_body_method(self):
        self.assertIn("RegisterWaterBody", _read("WaterBodyTool"))

    def test_apply_wave_settings_method(self):
        self.assertIn("ApplyWaveSettings", _read("WaterBodyTool"))

    def test_get_ocean_bodies_method(self):
        self.assertIn("GetOceanBodies", _read("WaterBodyTool"))

    def test_get_river_bodies_method(self):
        self.assertIn("GetRiverBodies", _read("WaterBodyTool"))


class TestPCGAttributeToolDetail(unittest.TestCase):
    def test_attribute_type_enum(self):
        self.assertIn("AttributeType", _read("PCGAttributeTool"))

    def test_attribute_scope_enum(self):
        self.assertIn("AttributeScope", _read("PCGAttributeTool"))

    def test_pcg_attribute_def_struct(self):
        self.assertIn("PCGAttributeDef", _read("PCGAttributeTool"))

    def test_attribute_id_in_struct(self):
        self.assertIn("attributeId", _read("PCGAttributeTool"))

    def test_attribute_name_in_struct(self):
        self.assertIn("attributeName", _read("PCGAttributeTool"))

    def test_attribute_type_in_struct(self):
        self.assertIn("attributeType", _read("PCGAttributeTool"))

    def test_scope_in_struct(self):
        self.assertIn("scope", _read("PCGAttributeTool"))

    def test_attribute_set_def_struct(self):
        self.assertIn("AttributeSetDef", _read("PCGAttributeTool"))

    def test_set_id_in_struct(self):
        self.assertIn("setId", _read("PCGAttributeTool"))

    def test_attribute_ids_vector_in_struct(self):
        self.assertIn("attributeIds", _read("PCGAttributeTool"))

    def test_attribute_override_def_struct(self):
        self.assertIn("AttributeOverrideDef", _read("PCGAttributeTool"))

    def test_override_id_in_struct(self):
        self.assertIn("overrideId", _read("PCGAttributeTool"))

    def test_target_attribute_id_in_struct(self):
        self.assertIn("targetAttributeId", _read("PCGAttributeTool"))

    def test_register_attribute_method(self):
        self.assertIn("RegisterAttribute", _read("PCGAttributeTool"))

    def test_create_attribute_set_method(self):
        self.assertIn("CreateAttributeSet", _read("PCGAttributeTool"))

    def test_get_attributes_by_type_method(self):
        self.assertIn("GetAttributesByType", _read("PCGAttributeTool"))

    def test_get_attributes_by_scope_method(self):
        self.assertIn("GetAttributesByScope", _read("PCGAttributeTool"))


class TestSoundCueToolDetail(unittest.TestCase):
    def test_sound_cue_node_type_enum(self):
        self.assertIn("SoundCueNodeType", _read("SoundCueTool"))

    def test_audio_bus_routing_enum(self):
        self.assertIn("AudioBusRouting", _read("SoundCueTool"))

    def test_sound_cue_node_def_struct(self):
        self.assertIn("SoundCueNodeDef", _read("SoundCueTool"))

    def test_node_id_in_struct(self):
        self.assertIn("nodeId", _read("SoundCueTool"))

    def test_sound_cue_edge_def_struct(self):
        self.assertIn("SoundCueEdgeDef", _read("SoundCueTool"))

    def test_edge_id_in_struct(self):
        self.assertIn("edgeId", _read("SoundCueTool"))

    def test_src_node_id_in_edge(self):
        self.assertIn("srcNodeId", _read("SoundCueTool"))

    def test_dst_node_id_in_edge(self):
        self.assertIn("dstNodeId", _read("SoundCueTool"))

    def test_sound_cue_def_struct(self):
        self.assertIn("SoundCueDef", _read("SoundCueTool"))

    def test_cue_id_in_struct(self):
        self.assertIn("cueId", _read("SoundCueTool"))

    def test_create_sound_cue_method(self):
        self.assertIn("CreateSoundCue", _read("SoundCueTool"))

    def test_get_cues_by_node_type_method(self):
        self.assertIn("GetCuesByNodeType", _read("SoundCueTool"))

    def test_set_attenuation_shape_method(self):
        self.assertIn("SetAttenuationShape", _read("SoundCueTool"))

    def test_add_edge_method(self):
        self.assertIn("AddEdge", _read("SoundCueTool"))


if __name__ == "__main__":
    unittest.main()
