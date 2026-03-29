"""Phase 31A — Tests for P16 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P16_TOOLS = [
    "VolumetricCloudTool",
    "DecalProjectorTool",
    "SoundOcclusionTool",
    "LevelStreamingTool",
    "AIPerceptionTool",
    "HapticFeedbackTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP16ToolsExist(unittest.TestCase):
    def test_volumetric_cloud_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "VolumetricCloudTool.h").exists())

    def test_decal_projector_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "DecalProjectorTool.h").exists())

    def test_sound_occlusion_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SoundOcclusionTool.h").exists())

    def test_level_streaming_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "LevelStreamingTool.h").exists())

    def test_ai_perception_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AIPerceptionTool.h").exists())

    def test_haptic_feedback_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "HapticFeedbackTool.h").exists())


class TestP16PragmaOnce(unittest.TestCase):
    def test_volumetric_cloud_pragma_once(self):
        self.assertIn("#pragma once", _read("VolumetricCloudTool"))

    def test_decal_projector_pragma_once(self):
        self.assertIn("#pragma once", _read("DecalProjectorTool"))

    def test_sound_occlusion_pragma_once(self):
        self.assertIn("#pragma once", _read("SoundOcclusionTool"))

    def test_level_streaming_pragma_once(self):
        self.assertIn("#pragma once", _read("LevelStreamingTool"))

    def test_ai_perception_pragma_once(self):
        self.assertIn("#pragma once", _read("AIPerceptionTool"))

    def test_haptic_feedback_pragma_once(self):
        self.assertIn("#pragma once", _read("HapticFeedbackTool"))


class TestP16ToolName(unittest.TestCase):
    def test_volumetric_cloud_tool_class_name(self):
        self.assertIn("VolumetricCloudTool", _read("VolumetricCloudTool"))

    def test_decal_projector_tool_class_name(self):
        self.assertIn("DecalProjectorTool", _read("DecalProjectorTool"))

    def test_sound_occlusion_tool_class_name(self):
        self.assertIn("SoundOcclusionTool", _read("SoundOcclusionTool"))

    def test_level_streaming_tool_class_name(self):
        self.assertIn("LevelStreamingTool", _read("LevelStreamingTool"))

    def test_ai_perception_tool_class_name(self):
        self.assertIn("AIPerceptionTool", _read("AIPerceptionTool"))

    def test_haptic_feedback_tool_class_name(self):
        self.assertIn("HapticFeedbackTool", _read("HapticFeedbackTool"))


class TestP16ITool(unittest.TestCase):
    def test_volumetric_cloud_tool_itool(self):
        self.assertIn(": public ITool", _read("VolumetricCloudTool"))

    def test_decal_projector_tool_itool(self):
        self.assertIn(": public ITool", _read("DecalProjectorTool"))

    def test_sound_occlusion_tool_itool(self):
        self.assertIn(": public ITool", _read("SoundOcclusionTool"))

    def test_level_streaming_tool_itool(self):
        self.assertIn(": public ITool", _read("LevelStreamingTool"))

    def test_ai_perception_tool_itool(self):
        self.assertIn(": public ITool", _read("AIPerceptionTool"))

    def test_haptic_feedback_tool_itool(self):
        self.assertIn(": public ITool", _read("HapticFeedbackTool"))


class TestVolumetricCloudToolDetail(unittest.TestCase):
    def test_cloud_layer_enum(self):
        self.assertIn("CloudLayer", _read("VolumetricCloudTool"))

    def test_cloud_layer_def_struct(self):
        self.assertIn("CloudLayerDef", _read("VolumetricCloudTool"))

    def test_add_layer_method(self):
        self.assertIn("AddLayer", _read("VolumetricCloudTool"))

    def test_export_cloud_config_method(self):
        self.assertIn("ExportCloudConfig", _read("VolumetricCloudTool"))


class TestDecalProjectorToolDetail(unittest.TestCase):
    def test_decal_surface_enum(self):
        self.assertIn("DecalSurface", _read("DecalProjectorTool"))

    def test_decal_def_struct(self):
        self.assertIn("DecalDef", _read("DecalProjectorTool"))

    def test_create_decal_method(self):
        self.assertIn("CreateDecal", _read("DecalProjectorTool"))

    def test_export_decal_set_method(self):
        self.assertIn("ExportDecalSet", _read("DecalProjectorTool"))


class TestSoundOcclusionToolDetail(unittest.TestCase):
    def test_occlusion_method_enum(self):
        self.assertIn("OcclusionMethod", _read("SoundOcclusionTool"))

    def test_reverb_zone_struct(self):
        self.assertIn("ReverbZone", _read("SoundOcclusionTool"))

    def test_create_occlusion_volume_method(self):
        self.assertIn("CreateOcclusionVolume", _read("SoundOcclusionTool"))

    def test_simulate_reverb_method(self):
        self.assertIn("SimulateReverb", _read("SoundOcclusionTool"))


class TestLevelStreamingToolDetail(unittest.TestCase):
    def test_streaming_method_enum(self):
        self.assertIn("StreamingMethod", _read("LevelStreamingTool"))

    def test_streaming_tile_struct(self):
        self.assertIn("StreamingTile", _read("LevelStreamingTool"))

    def test_create_tile_method(self):
        self.assertIn("CreateTile", _read("LevelStreamingTool"))

    def test_export_streaming_manifest_method(self):
        self.assertIn("ExportStreamingManifest", _read("LevelStreamingTool"))


class TestAIPerceptionToolDetail(unittest.TestCase):
    def test_sense_type_enum(self):
        self.assertIn("SenseType", _read("AIPerceptionTool"))

    def test_perception_config_struct(self):
        self.assertIn("PerceptionConfig", _read("AIPerceptionTool"))

    def test_create_sense_method(self):
        self.assertIn("CreateSense", _read("AIPerceptionTool"))

    def test_simulate_perception_method(self):
        self.assertIn("SimulatePerception", _read("AIPerceptionTool"))


class TestHapticFeedbackToolDetail(unittest.TestCase):
    def test_haptic_device_enum(self):
        self.assertIn("HapticDevice", _read("HapticFeedbackTool"))

    def test_haptic_pattern_struct(self):
        self.assertIn("HapticPattern", _read("HapticFeedbackTool"))

    def test_create_pattern_method(self):
        self.assertIn("CreatePattern", _read("HapticFeedbackTool"))

    def test_export_pattern_method(self):
        self.assertIn("ExportPattern", _read("HapticFeedbackTool"))


if __name__ == "__main__":
    unittest.main()
