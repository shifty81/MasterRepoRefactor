"""Phase 36A — Tests for P21 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P21_TOOLS = [
    "AbilitySystemDebuggerTool",
    "AIDebuggerTool",
    "MetaHumanTool",
    "LandscapeSplineTool",
    "PixelStreamingTool",
    "VirtualShadowMapTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP21ToolsExist(unittest.TestCase):
    def test_ability_system_debugger_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AbilitySystemDebuggerTool.h").exists())

    def test_ai_debugger_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AIDebuggerTool.h").exists())

    def test_meta_human_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MetaHumanTool.h").exists())

    def test_landscape_spline_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "LandscapeSplineTool.h").exists())

    def test_pixel_streaming_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "PixelStreamingTool.h").exists())

    def test_virtual_shadow_map_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "VirtualShadowMapTool.h").exists())


class TestP21PragmaOnce(unittest.TestCase):
    def test_ability_system_debugger_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("AbilitySystemDebuggerTool"))

    def test_ai_debugger_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("AIDebuggerTool"))

    def test_meta_human_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("MetaHumanTool"))

    def test_landscape_spline_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("LandscapeSplineTool"))

    def test_pixel_streaming_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("PixelStreamingTool"))

    def test_virtual_shadow_map_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("VirtualShadowMapTool"))


class TestP21ToolName(unittest.TestCase):
    def test_ability_system_debugger_tool_class_name(self):
        self.assertIn("AbilitySystemDebuggerTool", _read("AbilitySystemDebuggerTool"))

    def test_ai_debugger_tool_class_name(self):
        self.assertIn("AIDebuggerTool", _read("AIDebuggerTool"))

    def test_meta_human_tool_class_name(self):
        self.assertIn("MetaHumanTool", _read("MetaHumanTool"))

    def test_landscape_spline_tool_class_name(self):
        self.assertIn("LandscapeSplineTool", _read("LandscapeSplineTool"))

    def test_pixel_streaming_tool_class_name(self):
        self.assertIn("PixelStreamingTool", _read("PixelStreamingTool"))

    def test_virtual_shadow_map_tool_class_name(self):
        self.assertIn("VirtualShadowMapTool", _read("VirtualShadowMapTool"))


class TestP21ITool(unittest.TestCase):
    def test_ability_system_debugger_tool_itool(self):
        self.assertIn(": public ITool", _read("AbilitySystemDebuggerTool"))

    def test_ai_debugger_tool_itool(self):
        self.assertIn(": public ITool", _read("AIDebuggerTool"))

    def test_meta_human_tool_itool(self):
        self.assertIn(": public ITool", _read("MetaHumanTool"))

    def test_landscape_spline_tool_itool(self):
        self.assertIn(": public ITool", _read("LandscapeSplineTool"))

    def test_pixel_streaming_tool_itool(self):
        self.assertIn(": public ITool", _read("PixelStreamingTool"))

    def test_virtual_shadow_map_tool_itool(self):
        self.assertIn(": public ITool", _read("VirtualShadowMapTool"))


class TestAbilitySystemDebuggerToolDetail(unittest.TestCase):
    def test_ability_debug_mode_enum(self):
        self.assertIn("AbilityDebugMode", _read("AbilitySystemDebuggerTool"))

    def test_ability_watch_entry_struct(self):
        self.assertIn("AbilityWatchEntry", _read("AbilitySystemDebuggerTool"))

    def test_add_ability_watch_method(self):
        self.assertIn("AddAbilityWatch", _read("AbilitySystemDebuggerTool"))

    def test_cooldown_visualization_enum(self):
        self.assertIn("CooldownVisualization", _read("AbilitySystemDebuggerTool"))


class TestAIDebuggerToolDetail(unittest.TestCase):
    def test_ai_debug_mode_enum(self):
        self.assertIn("AIDebugMode", _read("AIDebuggerTool"))

    def test_blackboard_entry_struct(self):
        self.assertIn("BlackboardEntry", _read("AIDebuggerTool"))

    def test_add_agent_watch_method(self):
        self.assertIn("AddAgentWatch", _read("AIDebuggerTool"))

    def test_task_visual_mode_enum(self):
        self.assertIn("TaskVisualMode", _read("AIDebuggerTool"))


class TestMetaHumanToolDetail(unittest.TestCase):
    def test_meta_human_gender_enum(self):
        self.assertIn("MetaHumanGender", _read("MetaHumanTool"))

    def test_lod_config_def_struct(self):
        self.assertIn("LODConfigDef", _read("MetaHumanTool"))

    def test_create_identity_method(self):
        self.assertIn("CreateIdentity", _read("MetaHumanTool"))

    def test_facial_anim_channel_enum(self):
        self.assertIn("FacialAnimChannel", _read("MetaHumanTool"))


class TestLandscapeSplineToolDetail(unittest.TestCase):
    def test_spline_edit_mode_enum(self):
        self.assertIn("SplineEditMode", _read("LandscapeSplineTool"))

    def test_spline_segment_config_struct(self):
        self.assertIn("SplineSegmentConfig", _read("LandscapeSplineTool"))

    def test_add_point_method(self):
        self.assertIn("AddPoint", _read("LandscapeSplineTool"))

    def test_deformation_type_enum(self):
        self.assertIn("DeformationType", _read("LandscapeSplineTool"))


class TestPixelStreamingToolDetail(unittest.TestCase):
    def test_streaming_session_state_enum(self):
        self.assertIn("StreamingSessionState", _read("PixelStreamingTool"))

    def test_encoder_settings_def_struct(self):
        self.assertIn("EncoderSettingsDef", _read("PixelStreamingTool"))

    def test_create_session_method(self):
        self.assertIn("CreateSession", _read("PixelStreamingTool"))

    def test_client_connection_state_enum(self):
        self.assertIn("ClientConnectionState", _read("PixelStreamingTool"))


class TestVirtualShadowMapToolDetail(unittest.TestCase):
    def test_vsm_cache_mode_enum(self):
        self.assertIn("VSMCacheMode", _read("VirtualShadowMapTool"))

    def test_page_pool_entry_struct(self):
        self.assertIn("PagePoolEntry", _read("VirtualShadowMapTool"))

    def test_create_vsm_config_method(self):
        self.assertIn("CreateVSMConfig", _read("VirtualShadowMapTool"))

    def test_invalidation_cause_enum(self):
        self.assertIn("InvalidationCause", _read("VirtualShadowMapTool"))


if __name__ == "__main__":
    unittest.main()
