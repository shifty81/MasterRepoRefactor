"""Phase 25A — Tests for P10 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P10_TOOLS = [
    "VirtualCameraRigTool",
    "RenderPipelineTool",
    "InstancePainterTool",
    "MaterialLayerTool",
    "CharacterCustomizerTool",
    "CinematicLightingTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP10ToolsExist(unittest.TestCase):
    def test_virtual_camera_rig_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "VirtualCameraRigTool.h").exists())

    def test_render_pipeline_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "RenderPipelineTool.h").exists())

    def test_instance_painter_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "InstancePainterTool.h").exists())

    def test_material_layer_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MaterialLayerTool.h").exists())

    def test_character_customizer_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "CharacterCustomizerTool.h").exists())

    def test_cinematic_lighting_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "CinematicLightingTool.h").exists())


class TestP10PragmaOnce(unittest.TestCase):
    def test_virtual_camera_rig_pragma_once(self):
        self.assertIn("#pragma once", _read("VirtualCameraRigTool"))

    def test_render_pipeline_pragma_once(self):
        self.assertIn("#pragma once", _read("RenderPipelineTool"))

    def test_instance_painter_pragma_once(self):
        self.assertIn("#pragma once", _read("InstancePainterTool"))

    def test_material_layer_pragma_once(self):
        self.assertIn("#pragma once", _read("MaterialLayerTool"))

    def test_character_customizer_pragma_once(self):
        self.assertIn("#pragma once", _read("CharacterCustomizerTool"))

    def test_cinematic_lighting_pragma_once(self):
        self.assertIn("#pragma once", _read("CinematicLightingTool"))


class TestP10Inheritance(unittest.TestCase):
    def test_virtual_camera_rig_inherits_itool(self):
        self.assertIn("ITool", _read("VirtualCameraRigTool"))

    def test_render_pipeline_inherits_itool(self):
        self.assertIn("ITool", _read("RenderPipelineTool"))

    def test_instance_painter_inherits_itool(self):
        self.assertIn("ITool", _read("InstancePainterTool"))

    def test_material_layer_inherits_itool(self):
        self.assertIn("ITool", _read("MaterialLayerTool"))

    def test_character_customizer_inherits_itool(self):
        self.assertIn("ITool", _read("CharacterCustomizerTool"))

    def test_cinematic_lighting_inherits_itool(self):
        self.assertIn("ITool", _read("CinematicLightingTool"))


class TestP10GetToolName(unittest.TestCase):
    def test_virtual_camera_rig_get_tool_name(self):
        self.assertIn('"VirtualCameraRigTool"', _read("VirtualCameraRigTool"))

    def test_render_pipeline_get_tool_name(self):
        self.assertIn('"RenderPipelineTool"', _read("RenderPipelineTool"))

    def test_instance_painter_get_tool_name(self):
        self.assertIn('"InstancePainterTool"', _read("InstancePainterTool"))

    def test_material_layer_get_tool_name(self):
        self.assertIn('"MaterialLayerTool"', _read("MaterialLayerTool"))

    def test_character_customizer_get_tool_name(self):
        self.assertIn('"CharacterCustomizerTool"', _read("CharacterCustomizerTool"))

    def test_cinematic_lighting_get_tool_name(self):
        self.assertIn('"CinematicLightingTool"', _read("CinematicLightingTool"))


class TestP10Namespace(unittest.TestCase):
    def test_virtual_camera_rig_namespace(self):
        self.assertIn("Atlas::Editor", _read("VirtualCameraRigTool"))

    def test_render_pipeline_namespace(self):
        self.assertIn("Atlas::Editor", _read("RenderPipelineTool"))

    def test_instance_painter_namespace(self):
        self.assertIn("Atlas::Editor", _read("InstancePainterTool"))

    def test_material_layer_namespace(self):
        self.assertIn("Atlas::Editor", _read("MaterialLayerTool"))

    def test_character_customizer_namespace(self):
        self.assertIn("Atlas::Editor", _read("CharacterCustomizerTool"))

    def test_cinematic_lighting_namespace(self):
        self.assertIn("Atlas::Editor", _read("CinematicLightingTool"))


class TestP10SpecializedAPI(unittest.TestCase):
    # VirtualCameraRigTool
    def test_vcr_rig_type_enum(self):
        self.assertIn("RigType", _read("VirtualCameraRigTool"))

    def test_vcr_focus_mode_enum(self):
        self.assertIn("FocusMode", _read("VirtualCameraRigTool"))

    def test_vcr_lens_preset_enum(self):
        self.assertIn("LensPreset", _read("VirtualCameraRigTool"))

    def test_vcr_create_rig(self):
        self.assertIn("CreateRig", _read("VirtualCameraRigTool"))

    def test_vcr_add_node(self):
        self.assertIn("AddNode", _read("VirtualCameraRigTool"))

    def test_vcr_set_focal_length(self):
        self.assertIn("SetFocalLength", _read("VirtualCameraRigTool"))

    def test_vcr_camera_rig_struct(self):
        self.assertIn("CameraRig", _read("VirtualCameraRigTool"))

    def test_vcr_lens_settings_struct(self):
        self.assertIn("LensSettings", _read("VirtualCameraRigTool"))

    def test_vcr_set_shake_intensity(self):
        self.assertIn("SetShakeIntensity", _read("VirtualCameraRigTool"))

    # RenderPipelineTool
    def test_rpt_pipeline_type_enum(self):
        self.assertIn("PipelineType", _read("RenderPipelineTool"))

    def test_rpt_pass_type_enum(self):
        self.assertIn("PassType", _read("RenderPipelineTool"))

    def test_rpt_anti_aliasing_mode_enum(self):
        self.assertIn("AntiAliasingMode", _read("RenderPipelineTool"))

    def test_rpt_create_pipeline(self):
        self.assertIn("CreatePipeline", _read("RenderPipelineTool"))

    def test_rpt_add_pass(self):
        self.assertIn("AddPass", _read("RenderPipelineTool"))

    def test_rpt_add_feature(self):
        self.assertIn("AddFeature", _read("RenderPipelineTool"))

    def test_rpt_pipeline_config_struct(self):
        self.assertIn("PipelineConfig", _read("RenderPipelineTool"))

    def test_rpt_render_pass_struct(self):
        self.assertIn("RenderPass", _read("RenderPipelineTool"))

    def test_rpt_set_shadow_cascades(self):
        self.assertIn("SetShadowCascades", _read("RenderPipelineTool"))

    # InstancePainterTool
    def test_ipt_paint_mode_enum(self):
        self.assertIn("PaintMode", _read("InstancePainterTool"))

    def test_ipt_distribution_mode_enum(self):
        self.assertIn("DistributionMode", _read("InstancePainterTool"))

    def test_ipt_surface_snap_mode_enum(self):
        self.assertIn("SurfaceSnapMode", _read("InstancePainterTool"))

    def test_ipt_create_layer(self):
        self.assertIn("CreateLayer", _read("InstancePainterTool"))

    def test_ipt_paint_instance(self):
        self.assertIn("PaintInstance", _read("InstancePainterTool"))

    def test_ipt_erase_instance(self):
        self.assertIn("EraseInstance", _read("InstancePainterTool"))

    def test_ipt_set_brush_radius(self):
        self.assertIn("SetBrushRadius", _read("InstancePainterTool"))

    def test_ipt_instance_variation_struct(self):
        self.assertIn("InstanceVariation", _read("InstancePainterTool"))

    def test_ipt_paint_layer_struct(self):
        self.assertIn("PaintLayer", _read("InstancePainterTool"))

    def test_ipt_set_slope_filter(self):
        self.assertIn("SetSlopeFilter", _read("InstancePainterTool"))

    # MaterialLayerTool
    def test_mlt_blend_operation_enum(self):
        self.assertIn("BlendOperation", _read("MaterialLayerTool"))

    def test_mlt_mask_type_enum(self):
        self.assertIn("MaskType", _read("MaterialLayerTool"))

    def test_mlt_shading_model_enum(self):
        self.assertIn("ShadingModel", _read("MaterialLayerTool"))

    def test_mlt_create_stack(self):
        self.assertIn("CreateStack", _read("MaterialLayerTool"))

    def test_mlt_add_layer(self):
        self.assertIn("AddLayer", _read("MaterialLayerTool"))

    def test_mlt_move_layer_up(self):
        self.assertIn("MoveLayerUp", _read("MaterialLayerTool"))

    def test_mlt_add_texture_slot(self):
        self.assertIn("AddTextureSlot", _read("MaterialLayerTool"))

    def test_mlt_material_stack_struct(self):
        self.assertIn("MaterialStack", _read("MaterialLayerTool"))

    def test_mlt_material_layer_struct(self):
        self.assertIn("MaterialLayer", _read("MaterialLayerTool"))

    def test_mlt_set_layer_roughness(self):
        self.assertIn("SetLayerRoughness", _read("MaterialLayerTool"))

    # CharacterCustomizerTool
    def test_cct_slot_category_enum(self):
        self.assertIn("SlotCategory", _read("CharacterCustomizerTool"))

    def test_cct_morph_target_enum(self):
        self.assertIn("MorphTarget", _read("CharacterCustomizerTool"))

    def test_cct_color_channel_enum(self):
        self.assertIn("ColorChannel", _read("CharacterCustomizerTool"))

    def test_cct_create_preset(self):
        self.assertIn("CreatePreset", _read("CharacterCustomizerTool"))

    def test_cct_add_slot(self):
        self.assertIn("AddSlot", _read("CharacterCustomizerTool"))

    def test_cct_equip_mesh(self):
        self.assertIn("EquipMesh", _read("CharacterCustomizerTool"))

    def test_cct_add_morph(self):
        self.assertIn("AddMorph", _read("CharacterCustomizerTool"))

    def test_cct_set_color_channel(self):
        self.assertIn("SetColorChannel", _read("CharacterCustomizerTool"))

    def test_cct_character_preset_struct(self):
        self.assertIn("CharacterPreset", _read("CharacterCustomizerTool"))

    def test_cct_duplicate_preset(self):
        self.assertIn("DuplicatePreset", _read("CharacterCustomizerTool"))

    # CinematicLightingTool
    def test_clt_light_type_enum(self):
        self.assertIn("LightType", _read("CinematicLightingTool"))

    def test_clt_shadow_quality_enum(self):
        self.assertIn("ShadowQuality", _read("CinematicLightingTool"))

    def test_clt_lighting_unit_enum(self):
        self.assertIn("LightingUnit", _read("CinematicLightingTool"))

    def test_clt_add_light(self):
        self.assertIn("AddLight", _read("CinematicLightingTool"))

    def test_clt_set_light_intensity(self):
        self.assertIn("SetLightIntensity", _read("CinematicLightingTool"))

    def test_clt_set_light_color(self):
        self.assertIn("SetLightColor", _read("CinematicLightingTool"))

    def test_clt_set_light_temperature(self):
        self.assertIn("SetLightTemperature", _read("CinematicLightingTool"))

    def test_clt_set_shadow_quality(self):
        self.assertIn("SetShadowQuality", _read("CinematicLightingTool"))

    def test_clt_create_scenario(self):
        self.assertIn("CreateScenario", _read("CinematicLightingTool"))

    def test_clt_light_rig_struct(self):
        self.assertIn("LightRig", _read("CinematicLightingTool"))

    def test_clt_set_ies_profile(self):
        self.assertIn("SetIESProfile", _read("CinematicLightingTool"))


if __name__ == "__main__":
    unittest.main()
