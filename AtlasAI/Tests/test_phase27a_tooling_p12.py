"""Phase 27A — Tests for P12 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P12_TOOLS = [
    "ClothSimulationTool",
    "CameraShakeTool",
    "SoundEffectDesignerTool",
    "AnimationBlendSpaceTool",
    "MaterialAnimatorTool",
    "EnvironmentArtTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP12ToolsExist(unittest.TestCase):
    def test_cloth_simulation_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ClothSimulationTool.h").exists())

    def test_camera_shake_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "CameraShakeTool.h").exists())

    def test_sound_effect_designer_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SoundEffectDesignerTool.h").exists())

    def test_animation_blend_space_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AnimationBlendSpaceTool.h").exists())

    def test_material_animator_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MaterialAnimatorTool.h").exists())

    def test_environment_art_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "EnvironmentArtTool.h").exists())


class TestP12PragmaOnce(unittest.TestCase):
    def test_cloth_simulation_pragma_once(self):
        self.assertIn("#pragma once", _read("ClothSimulationTool"))

    def test_camera_shake_pragma_once(self):
        self.assertIn("#pragma once", _read("CameraShakeTool"))

    def test_sound_effect_designer_pragma_once(self):
        self.assertIn("#pragma once", _read("SoundEffectDesignerTool"))

    def test_animation_blend_space_pragma_once(self):
        self.assertIn("#pragma once", _read("AnimationBlendSpaceTool"))

    def test_material_animator_pragma_once(self):
        self.assertIn("#pragma once", _read("MaterialAnimatorTool"))

    def test_environment_art_pragma_once(self):
        self.assertIn("#pragma once", _read("EnvironmentArtTool"))


class TestP12Inheritance(unittest.TestCase):
    def test_cloth_simulation_inherits_itool(self):
        self.assertIn("ITool", _read("ClothSimulationTool"))

    def test_camera_shake_inherits_itool(self):
        self.assertIn("ITool", _read("CameraShakeTool"))

    def test_sound_effect_designer_inherits_itool(self):
        self.assertIn("ITool", _read("SoundEffectDesignerTool"))

    def test_animation_blend_space_inherits_itool(self):
        self.assertIn("ITool", _read("AnimationBlendSpaceTool"))

    def test_material_animator_inherits_itool(self):
        self.assertIn("ITool", _read("MaterialAnimatorTool"))

    def test_environment_art_inherits_itool(self):
        self.assertIn("ITool", _read("EnvironmentArtTool"))


class TestP12GetToolName(unittest.TestCase):
    def test_cloth_simulation_get_tool_name(self):
        self.assertIn('"ClothSimulationTool"', _read("ClothSimulationTool"))

    def test_camera_shake_get_tool_name(self):
        self.assertIn('"CameraShakeTool"', _read("CameraShakeTool"))

    def test_sound_effect_designer_get_tool_name(self):
        self.assertIn('"SoundEffectDesignerTool"', _read("SoundEffectDesignerTool"))

    def test_animation_blend_space_get_tool_name(self):
        self.assertIn('"AnimationBlendSpaceTool"', _read("AnimationBlendSpaceTool"))

    def test_material_animator_get_tool_name(self):
        self.assertIn('"MaterialAnimatorTool"', _read("MaterialAnimatorTool"))

    def test_environment_art_get_tool_name(self):
        self.assertIn('"EnvironmentArtTool"', _read("EnvironmentArtTool"))


class TestP12Namespace(unittest.TestCase):
    def test_cloth_simulation_namespace(self):
        self.assertIn("Atlas::Editor", _read("ClothSimulationTool"))

    def test_camera_shake_namespace(self):
        self.assertIn("Atlas::Editor", _read("CameraShakeTool"))

    def test_sound_effect_designer_namespace(self):
        self.assertIn("Atlas::Editor", _read("SoundEffectDesignerTool"))

    def test_animation_blend_space_namespace(self):
        self.assertIn("Atlas::Editor", _read("AnimationBlendSpaceTool"))

    def test_material_animator_namespace(self):
        self.assertIn("Atlas::Editor", _read("MaterialAnimatorTool"))

    def test_environment_art_namespace(self):
        self.assertIn("Atlas::Editor", _read("EnvironmentArtTool"))


class TestP12SpecializedAPI(unittest.TestCase):
    # ClothSimulationTool
    def test_cloth_type_enum(self):
        self.assertIn("ClothType", _read("ClothSimulationTool"))

    def test_cloth_collision_mode_enum(self):
        self.assertIn("CollisionMode", _read("ClothSimulationTool"))

    def test_cloth_solver_type_enum(self):
        self.assertIn("SolverType", _read("ClothSimulationTool"))

    def test_cloth_tear_mode_enum(self):
        self.assertIn("TearMode", _read("ClothSimulationTool"))

    def test_cloth_constraints_struct(self):
        self.assertIn("ClothConstraints", _read("ClothSimulationTool"))

    def test_cloth_physics_struct(self):
        self.assertIn("ClothPhysics", _read("ClothSimulationTool"))

    def test_cloth_wind_response_struct(self):
        self.assertIn("ClothWindResponse", _read("ClothSimulationTool"))

    def test_cloth_create_layer(self):
        self.assertIn("CreateLayer", _read("ClothSimulationTool"))

    def test_cloth_set_stretch_stiffness(self):
        self.assertIn("SetStretchStiffness", _read("ClothSimulationTool"))

    def test_cloth_set_wind_lift(self):
        self.assertIn("SetWindLift", _read("ClothSimulationTool"))

    def test_cloth_pause_simulation(self):
        self.assertIn("PauseSimulation", _read("ClothSimulationTool"))

    def test_cloth_bake_layer(self):
        self.assertIn("BakeLayer", _read("ClothSimulationTool"))

    def test_cloth_set_tear_threshold(self):
        self.assertIn("SetTearThreshold", _read("ClothSimulationTool"))

    # CameraShakeTool
    def test_shake_profile_enum(self):
        self.assertIn("ShakeProfile", _read("CameraShakeTool"))

    def test_shake_axis_enum(self):
        self.assertIn("ShakeAxis", _read("CameraShakeTool"))

    def test_waveform_enum(self):
        self.assertIn("Waveform", _read("CameraShakeTool"))

    def test_falloff_curve_enum(self):
        self.assertIn("FalloffCurve", _read("CameraShakeTool"))

    def test_shake_channel_struct(self):
        self.assertIn("ShakeChannel", _read("CameraShakeTool"))

    def test_shake_envelope_struct(self):
        self.assertIn("ShakeEnvelope", _read("CameraShakeTool"))

    def test_shake_preset_struct(self):
        self.assertIn("ShakePreset", _read("CameraShakeTool"))

    def test_shake_create_preset(self):
        self.assertIn("CreatePreset", _read("CameraShakeTool"))

    def test_shake_add_channel(self):
        self.assertIn("AddChannel", _read("CameraShakeTool"))

    def test_shake_set_attack_time(self):
        self.assertIn("SetAttackTime", _read("CameraShakeTool"))

    def test_shake_set_max_distance(self):
        self.assertIn("SetMaxDistance", _read("CameraShakeTool"))

    def test_shake_preview_preset(self):
        self.assertIn("PreviewPreset", _read("CameraShakeTool"))

    # SoundEffectDesignerTool
    def test_synth_type_enum(self):
        self.assertIn("SynthType", _read("SoundEffectDesignerTool"))

    def test_filter_type_enum(self):
        self.assertIn("FilterType", _read("SoundEffectDesignerTool"))

    def test_modulation_target_enum(self):
        self.assertIn("ModulationTarget", _read("SoundEffectDesignerTool"))

    def test_adsr_envelope_struct(self):
        self.assertIn("ADSREnvelope", _read("SoundEffectDesignerTool"))

    def test_filter_settings_struct(self):
        self.assertIn("FilterSettings", _read("SoundEffectDesignerTool"))

    def test_lfo_settings_struct(self):
        self.assertIn("LFOSettings", _read("SoundEffectDesignerTool"))

    def test_sound_layer_struct(self):
        self.assertIn("SoundLayer", _read("SoundEffectDesignerTool"))

    def test_sound_effect_struct(self):
        self.assertIn("SoundEffect", _read("SoundEffectDesignerTool"))

    def test_sfx_create_effect(self):
        self.assertIn("CreateEffect", _read("SoundEffectDesignerTool"))

    def test_sfx_add_layer(self):
        self.assertIn("AddLayer", _read("SoundEffectDesignerTool"))

    def test_sfx_set_adsr(self):
        self.assertIn("SetADSR", _read("SoundEffectDesignerTool"))

    def test_sfx_add_lfo(self):
        self.assertIn("AddLFO", _read("SoundEffectDesignerTool"))

    def test_sfx_preview_effect(self):
        self.assertIn("PreviewEffect", _read("SoundEffectDesignerTool"))

    # AnimationBlendSpaceTool
    def test_blend_space_type_enum(self):
        self.assertIn("BlendSpaceType", _read("AnimationBlendSpaceTool"))

    def test_blend_mode_enum(self):
        self.assertIn("BlendMode", _read("AnimationBlendSpaceTool"))

    def test_sample_interpolation_enum(self):
        self.assertIn("SampleInterpolation", _read("AnimationBlendSpaceTool"))

    def test_blend_axis_struct(self):
        self.assertIn("BlendAxis", _read("AnimationBlendSpaceTool"))

    def test_blend_sample_struct(self):
        self.assertIn("BlendSample", _read("AnimationBlendSpaceTool"))

    def test_blend_space_struct(self):
        self.assertIn("BlendSpace", _read("AnimationBlendSpaceTool"))

    def test_blend_create_blend_space(self):
        self.assertIn("CreateBlendSpace", _read("AnimationBlendSpaceTool"))

    def test_blend_add_sample(self):
        self.assertIn("AddSample", _read("AnimationBlendSpaceTool"))

    def test_blend_set_axis_x(self):
        self.assertIn("SetAxisX", _read("AnimationBlendSpaceTool"))

    def test_blend_get_blend_weights(self):
        self.assertIn("GetBlendWeights", _read("AnimationBlendSpaceTool"))

    def test_blend_set_preview_position(self):
        self.assertIn("SetPreviewPosition", _read("AnimationBlendSpaceTool"))

    # MaterialAnimatorTool
    def test_property_type_enum(self):
        self.assertIn("PropertyType", _read("MaterialAnimatorTool"))

    def test_interpolation_type_enum(self):
        self.assertIn("InterpolationType", _read("MaterialAnimatorTool"))

    def test_play_mode_enum(self):
        self.assertIn("PlayMode", _read("MaterialAnimatorTool"))

    def test_keyframe_struct(self):
        self.assertIn("Keyframe", _read("MaterialAnimatorTool"))

    def test_property_track_struct(self):
        self.assertIn("PropertyTrack", _read("MaterialAnimatorTool"))

    def test_material_animation_struct(self):
        self.assertIn("MaterialAnimation", _read("MaterialAnimatorTool"))

    def test_manim_create_animation(self):
        self.assertIn("CreateAnimation", _read("MaterialAnimatorTool"))

    def test_manim_add_track(self):
        self.assertIn("AddTrack", _read("MaterialAnimatorTool"))

    def test_manim_add_float_keyframe(self):
        self.assertIn("AddFloatKeyframe", _read("MaterialAnimatorTool"))

    def test_manim_add_color_keyframe(self):
        self.assertIn("AddColorKeyframe", _read("MaterialAnimatorTool"))

    def test_manim_play(self):
        self.assertIn("Play", _read("MaterialAnimatorTool"))

    def test_manim_seek(self):
        self.assertIn("Seek", _read("MaterialAnimatorTool"))

    # EnvironmentArtTool
    def test_placement_mode_enum(self):
        self.assertIn("PlacementMode", _read("EnvironmentArtTool"))

    def test_surface_snap_enum(self):
        self.assertIn("SurfaceSnap", _read("EnvironmentArtTool"))

    def test_scatter_shape_enum(self):
        self.assertIn("ScatterShape", _read("EnvironmentArtTool"))

    def test_variation_type_enum(self):
        self.assertIn("VariationType", _read("EnvironmentArtTool"))

    def test_density_falloff_enum(self):
        self.assertIn("DensityFalloff", _read("EnvironmentArtTool"))

    def test_scatter_variance_struct(self):
        self.assertIn("ScatterVariance", _read("EnvironmentArtTool"))

    def test_mesh_variant_struct(self):
        self.assertIn("MeshVariant", _read("EnvironmentArtTool"))

    def test_art_layer_struct(self):
        self.assertIn("ArtLayer", _read("EnvironmentArtTool"))

    def test_envart_create_layer(self):
        self.assertIn("CreateLayer", _read("EnvironmentArtTool"))

    def test_envart_add_mesh_variant(self):
        self.assertIn("AddMeshVariant", _read("EnvironmentArtTool"))

    def test_envart_set_density(self):
        self.assertIn("SetDensity", _read("EnvironmentArtTool"))

    def test_envart_set_slope_range(self):
        self.assertIn("SetSlopeRange", _read("EnvironmentArtTool"))

    def test_envart_scatter_layer(self):
        self.assertIn("ScatterLayer", _read("EnvironmentArtTool"))

    def test_envart_bake_layer(self):
        self.assertIn("BakeLayer", _read("EnvironmentArtTool"))


if __name__ == "__main__":
    unittest.main()
