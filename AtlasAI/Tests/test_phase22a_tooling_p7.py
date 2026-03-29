"""Phase 22A — Tests for P7 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P7_TOOLS = [
    "WaterVolumeTool",
    "AtmosphereEditorTool",
    "AnimationStateMachineTool",
    "CutsceneCameraTool",
    "SoundPropagationTool",
    "LODGroupEditorTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP7ToolsExist(unittest.TestCase):
    def test_water_volume_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "WaterVolumeTool.h").exists())

    def test_atmosphere_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AtmosphereEditorTool.h").exists())

    def test_animation_state_machine_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AnimationStateMachineTool.h").exists())

    def test_cutscene_camera_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "CutsceneCameraTool.h").exists())

    def test_sound_propagation_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SoundPropagationTool.h").exists())

    def test_lod_group_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "LODGroupEditorTool.h").exists())


class TestP7PragmaOnce(unittest.TestCase):
    def test_water_volume_pragma_once(self):
        self.assertIn("#pragma once", _read("WaterVolumeTool"))

    def test_atmosphere_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("AtmosphereEditorTool"))

    def test_animation_state_machine_pragma_once(self):
        self.assertIn("#pragma once", _read("AnimationStateMachineTool"))

    def test_cutscene_camera_pragma_once(self):
        self.assertIn("#pragma once", _read("CutsceneCameraTool"))

    def test_sound_propagation_pragma_once(self):
        self.assertIn("#pragma once", _read("SoundPropagationTool"))

    def test_lod_group_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("LODGroupEditorTool"))


class TestP7Inheritance(unittest.TestCase):
    def test_water_volume_inherits_itool(self):
        self.assertIn("ITool", _read("WaterVolumeTool"))

    def test_atmosphere_editor_inherits_itool(self):
        self.assertIn("ITool", _read("AtmosphereEditorTool"))

    def test_animation_state_machine_inherits_itool(self):
        self.assertIn("ITool", _read("AnimationStateMachineTool"))

    def test_cutscene_camera_inherits_itool(self):
        self.assertIn("ITool", _read("CutsceneCameraTool"))

    def test_sound_propagation_inherits_itool(self):
        self.assertIn("ITool", _read("SoundPropagationTool"))

    def test_lod_group_editor_inherits_itool(self):
        self.assertIn("ITool", _read("LODGroupEditorTool"))


class TestP7GetToolName(unittest.TestCase):
    def test_water_volume_get_tool_name(self):
        self.assertIn('"WaterVolumeTool"', _read("WaterVolumeTool"))

    def test_atmosphere_editor_get_tool_name(self):
        self.assertIn('"AtmosphereEditorTool"', _read("AtmosphereEditorTool"))

    def test_animation_state_machine_get_tool_name(self):
        self.assertIn('"AnimationStateMachineTool"',
                      _read("AnimationStateMachineTool"))

    def test_cutscene_camera_get_tool_name(self):
        self.assertIn('"CutsceneCameraTool"', _read("CutsceneCameraTool"))

    def test_sound_propagation_get_tool_name(self):
        self.assertIn('"SoundPropagationTool"', _read("SoundPropagationTool"))

    def test_lod_group_editor_get_tool_name(self):
        self.assertIn('"LODGroupEditorTool"', _read("LODGroupEditorTool"))


class TestP7Namespace(unittest.TestCase):
    def test_water_volume_namespace(self):
        self.assertIn("Atlas::Editor", _read("WaterVolumeTool"))

    def test_atmosphere_editor_namespace(self):
        self.assertIn("Atlas::Editor", _read("AtmosphereEditorTool"))

    def test_animation_state_machine_namespace(self):
        self.assertIn("Atlas::Editor", _read("AnimationStateMachineTool"))

    def test_cutscene_camera_namespace(self):
        self.assertIn("Atlas::Editor", _read("CutsceneCameraTool"))

    def test_sound_propagation_namespace(self):
        self.assertIn("Atlas::Editor", _read("SoundPropagationTool"))

    def test_lod_group_editor_namespace(self):
        self.assertIn("Atlas::Editor", _read("LODGroupEditorTool"))


class TestP7SpecializedAPI(unittest.TestCase):
    # WaterVolumeTool
    def test_water_volume_add_water_body(self):
        self.assertIn("AddWaterBody", _read("WaterVolumeTool"))

    def test_water_volume_set_surface_level(self):
        self.assertIn("SetSurfaceLevel", _read("WaterVolumeTool"))

    def test_water_volume_set_wave_parameters(self):
        self.assertIn("SetWaveParameters", _read("WaterVolumeTool"))

    def test_water_volume_water_body_type_enum(self):
        self.assertIn("WaterBodyType", _read("WaterVolumeTool"))

    def test_water_volume_set_flow_speed(self):
        self.assertIn("SetFlowSpeed", _read("WaterVolumeTool"))

    # AtmosphereEditorTool
    def test_atmosphere_editor_set_sun_position(self):
        self.assertIn("SetSunPosition", _read("AtmosphereEditorTool"))

    def test_atmosphere_editor_set_fog_density(self):
        self.assertIn("SetFogDensity", _read("AtmosphereEditorTool"))

    def test_atmosphere_editor_save_preset(self):
        self.assertIn("SavePreset", _read("AtmosphereEditorTool"))

    def test_atmosphere_editor_load_preset(self):
        self.assertIn("LoadPreset", _read("AtmosphereEditorTool"))

    def test_atmosphere_editor_blend_to_preset(self):
        self.assertIn("BlendToPreset", _read("AtmosphereEditorTool"))

    def test_atmosphere_editor_settings_struct(self):
        self.assertIn("AtmosphereSettings", _read("AtmosphereEditorTool"))

    # AnimationStateMachineTool
    def test_animation_state_machine_create_machine(self):
        self.assertIn("CreateStateMachine", _read("AnimationStateMachineTool"))

    def test_animation_state_machine_add_state(self):
        self.assertIn("AddState", _read("AnimationStateMachineTool"))

    def test_animation_state_machine_add_transition(self):
        self.assertIn("AddTransition", _read("AnimationStateMachineTool"))

    def test_animation_state_machine_transition_condition_enum(self):
        self.assertIn("TransitionCondition", _read("AnimationStateMachineTool"))

    def test_animation_state_machine_set_entry_state(self):
        self.assertIn("SetEntryState", _read("AnimationStateMachineTool"))

    # CutsceneCameraTool
    def test_cutscene_camera_create_track(self):
        self.assertIn("CreateTrack", _read("CutsceneCameraTool"))

    def test_cutscene_camera_add_keyframe(self):
        self.assertIn("AddKeyframe", _read("CutsceneCameraTool"))

    def test_cutscene_camera_easing_type_enum(self):
        self.assertIn("EasingType", _read("CutsceneCameraTool"))

    def test_cutscene_camera_play_track(self):
        self.assertIn("PlayTrack", _read("CutsceneCameraTool"))

    def test_cutscene_camera_keyframe_struct(self):
        self.assertIn("CameraKeyframe", _read("CutsceneCameraTool"))

    # SoundPropagationTool
    def test_sound_propagation_add_zone(self):
        self.assertIn("AddZone", _read("SoundPropagationTool"))

    def test_sound_propagation_mode_enum(self):
        self.assertIn("PropagationMode", _read("SoundPropagationTool"))

    def test_sound_propagation_set_zone_reverb(self):
        self.assertIn("SetZoneReverb", _read("SoundPropagationTool"))

    def test_sound_propagation_register_material(self):
        self.assertIn("RegisterMaterial", _read("SoundPropagationTool"))

    def test_sound_propagation_sound_material_struct(self):
        self.assertIn("SoundMaterial", _read("SoundPropagationTool"))

    # LODGroupEditorTool
    def test_lod_group_editor_create_group(self):
        self.assertIn("CreateGroup", _read("LODGroupEditorTool"))

    def test_lod_group_editor_add_lod_level(self):
        self.assertIn("AddLODLevel", _read("LODGroupEditorTool"))

    def test_lod_group_editor_auto_generate_lods(self):
        self.assertIn("AutoGenerateLODs", _read("LODGroupEditorTool"))

    def test_lod_group_editor_lod_level_struct(self):
        self.assertIn("LODLevel", _read("LODGroupEditorTool"))

    def test_lod_group_editor_get_groups_for_entity(self):
        self.assertIn("GetGroupsForEntity", _read("LODGroupEditorTool"))


if __name__ == "__main__":
    unittest.main()
