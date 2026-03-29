"""Phase 42A — Tests for P27 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P27_TOOLS = [
    "DistanceFieldTool",
    "LensFlareEditorTool",
    "TerrainMaterialBlendTool",
    "AnimationCompressionTool",
    "BlueprintNativeEventTool",
    "SplineDeformerTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP27ToolsExist(unittest.TestCase):
    def test_distance_field_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "DistanceFieldTool.h").exists())

    def test_lens_flare_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "LensFlareEditorTool.h").exists())

    def test_terrain_material_blend_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "TerrainMaterialBlendTool.h").exists())

    def test_animation_compression_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AnimationCompressionTool.h").exists())

    def test_blueprint_native_event_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "BlueprintNativeEventTool.h").exists())

    def test_spline_deformer_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SplineDeformerTool.h").exists())


class TestP27PragmaOnce(unittest.TestCase):
    def test_distance_field_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("DistanceFieldTool"))

    def test_lens_flare_editor_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("LensFlareEditorTool"))

    def test_terrain_material_blend_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("TerrainMaterialBlendTool"))

    def test_animation_compression_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("AnimationCompressionTool"))

    def test_blueprint_native_event_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("BlueprintNativeEventTool"))

    def test_spline_deformer_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("SplineDeformerTool"))


class TestP27ToolName(unittest.TestCase):
    def test_distance_field_tool_class_name(self):
        self.assertIn("DistanceFieldTool", _read("DistanceFieldTool"))

    def test_lens_flare_editor_tool_class_name(self):
        self.assertIn("LensFlareEditorTool", _read("LensFlareEditorTool"))

    def test_terrain_material_blend_tool_class_name(self):
        self.assertIn("TerrainMaterialBlendTool", _read("TerrainMaterialBlendTool"))

    def test_animation_compression_tool_class_name(self):
        self.assertIn("AnimationCompressionTool", _read("AnimationCompressionTool"))

    def test_blueprint_native_event_tool_class_name(self):
        self.assertIn("BlueprintNativeEventTool", _read("BlueprintNativeEventTool"))

    def test_spline_deformer_tool_class_name(self):
        self.assertIn("SplineDeformerTool", _read("SplineDeformerTool"))


class TestP27ITool(unittest.TestCase):
    def test_distance_field_tool_itool(self):
        self.assertIn(": public ITool", _read("DistanceFieldTool"))

    def test_lens_flare_editor_tool_itool(self):
        self.assertIn(": public ITool", _read("LensFlareEditorTool"))

    def test_terrain_material_blend_tool_itool(self):
        self.assertIn(": public ITool", _read("TerrainMaterialBlendTool"))

    def test_animation_compression_tool_itool(self):
        self.assertIn(": public ITool", _read("AnimationCompressionTool"))

    def test_blueprint_native_event_tool_itool(self):
        self.assertIn(": public ITool", _read("BlueprintNativeEventTool"))

    def test_spline_deformer_tool_itool(self):
        self.assertIn(": public ITool", _read("SplineDeformerTool"))


class TestDistanceFieldToolDetail(unittest.TestCase):
    def test_field_resolution_enum(self):
        self.assertIn("FieldResolution", _read("DistanceFieldTool"))

    def test_field_shape_enum(self):
        self.assertIn("FieldShape", _read("DistanceFieldTool"))

    def test_shadow_type_enum(self):
        self.assertIn("ShadowType", _read("DistanceFieldTool"))

    def test_field_blend_mode_enum(self):
        self.assertIn("FieldBlendMode", _read("DistanceFieldTool"))

    def test_distance_field_def_struct(self):
        self.assertIn("DistanceFieldDef", _read("DistanceFieldTool"))

    def test_shadow_config_def_struct(self):
        self.assertIn("ShadowConfigDef", _read("DistanceFieldTool"))

    def test_field_blend_op_def_struct(self):
        self.assertIn("FieldBlendOpDef", _read("DistanceFieldTool"))

    def test_create_field_method(self):
        self.assertIn("CreateField", _read("DistanceFieldTool"))

    def test_add_shadow_config_method(self):
        self.assertIn("AddShadowConfig", _read("DistanceFieldTool"))

    def test_create_blend_op_method(self):
        self.assertIn("CreateBlendOp", _read("DistanceFieldTool"))


class TestLensFlareEditorToolDetail(unittest.TestCase):
    def test_flare_element_type_enum(self):
        self.assertIn("FlareElementType", _read("LensFlareEditorTool"))

    def test_occlusion_mode_enum(self):
        self.assertIn("OcclusionMode", _read("LensFlareEditorTool"))

    def test_blend_function_enum(self):
        self.assertIn("BlendFunction", _read("LensFlareEditorTool"))

    def test_flare_trigger_enum(self):
        self.assertIn("FlareTrigger", _read("LensFlareEditorTool"))

    def test_flare_asset_def_struct(self):
        self.assertIn("FlareAssetDef", _read("LensFlareEditorTool"))

    def test_flare_element_def_struct(self):
        self.assertIn("FlareElementDef", _read("LensFlareEditorTool"))

    def test_flare_occlusion_def_struct(self):
        self.assertIn("FlareOcclusionDef", _read("LensFlareEditorTool"))

    def test_create_flare_method(self):
        self.assertIn("CreateFlare", _read("LensFlareEditorTool"))

    def test_add_element_method(self):
        self.assertIn("AddElement", _read("LensFlareEditorTool"))

    def test_set_occlusion_method(self):
        self.assertIn("SetOcclusion", _read("LensFlareEditorTool"))


class TestTerrainMaterialBlendToolDetail(unittest.TestCase):
    def test_blend_layer_type_enum(self):
        self.assertIn("BlendLayerType", _read("TerrainMaterialBlendTool"))

    def test_weight_paint_mode_enum(self):
        self.assertIn("WeightPaintMode", _read("TerrainMaterialBlendTool"))

    def test_splat_channel_enum(self):
        self.assertIn("SplatChannel", _read("TerrainMaterialBlendTool"))

    def test_blend_layer_def_struct(self):
        self.assertIn("BlendLayerDef", _read("TerrainMaterialBlendTool"))

    def test_weight_paint_op_def_struct(self):
        self.assertIn("WeightPaintOpDef", _read("TerrainMaterialBlendTool"))

    def test_splat_map_bake_def_struct(self):
        self.assertIn("SplatMapBakeDef", _read("TerrainMaterialBlendTool"))

    def test_create_layer_method(self):
        self.assertIn("CreateLayer", _read("TerrainMaterialBlendTool"))

    def test_apply_weight_paint_op_method(self):
        self.assertIn("ApplyWeightPaintOp", _read("TerrainMaterialBlendTool"))

    def test_execute_splat_map_bake_method(self):
        self.assertIn("ExecuteSplatMapBake", _read("TerrainMaterialBlendTool"))


class TestAnimationCompressionToolDetail(unittest.TestCase):
    def test_compression_codec_enum(self):
        self.assertIn("CompressionCodec", _read("AnimationCompressionTool"))

    def test_compression_quality_enum(self):
        self.assertIn("CompressionQuality", _read("AnimationCompressionTool"))

    def test_track_type_enum(self):
        self.assertIn("TrackType", _read("AnimationCompressionTool"))

    def test_key_reduction_method_enum(self):
        self.assertIn("KeyReductionMethod", _read("AnimationCompressionTool"))

    def test_compression_scheme_def_struct(self):
        self.assertIn("CompressionSchemeDef", _read("AnimationCompressionTool"))

    def test_track_compression_def_struct(self):
        self.assertIn("TrackCompressionDef", _read("AnimationCompressionTool"))

    def test_compression_preview_def_struct(self):
        self.assertIn("CompressionPreviewDef", _read("AnimationCompressionTool"))

    def test_create_scheme_method(self):
        self.assertIn("CreateScheme", _read("AnimationCompressionTool"))

    def test_add_track_compression_method(self):
        self.assertIn("AddTrackCompression", _read("AnimationCompressionTool"))

    def test_generate_preview_method(self):
        self.assertIn("GeneratePreview", _read("AnimationCompressionTool"))


class TestBlueprintNativeEventToolDetail(unittest.TestCase):
    def test_event_binding_type_enum(self):
        self.assertIn("EventBindingType", _read("BlueprintNativeEventTool"))

    def test_event_visibility_enum(self):
        self.assertIn("EventVisibility", _read("BlueprintNativeEventTool"))

    def test_stub_gen_mode_enum(self):
        self.assertIn("StubGenMode", _read("BlueprintNativeEventTool"))

    def test_native_event_def_struct(self):
        self.assertIn("NativeEventDef", _read("BlueprintNativeEventTool"))

    def test_stub_gen_def_struct(self):
        self.assertIn("StubGenDef", _read("BlueprintNativeEventTool"))

    def test_event_graph_wire_def_struct(self):
        self.assertIn("EventGraphWireDef", _read("BlueprintNativeEventTool"))

    def test_register_event_method(self):
        self.assertIn("RegisterEvent", _read("BlueprintNativeEventTool"))

    def test_generate_stub_method(self):
        self.assertIn("GenerateStub", _read("BlueprintNativeEventTool"))

    def test_add_wire_method(self):
        self.assertIn("AddWire", _read("BlueprintNativeEventTool"))


class TestSplineDeformerToolDetail(unittest.TestCase):
    def test_deformer_type_enum(self):
        self.assertIn("DeformerType", _read("SplineDeformerTool"))

    def test_binding_method_enum(self):
        self.assertIn("BindingMethod", _read("SplineDeformerTool"))

    def test_deformation_axis_enum(self):
        self.assertIn("DeformationAxis", _read("SplineDeformerTool"))

    def test_interpolation_mode_enum(self):
        self.assertIn("InterpolationMode", _read("SplineDeformerTool"))

    def test_spline_deformer_def_struct(self):
        self.assertIn("SplineDeformerDef", _read("SplineDeformerTool"))

    def test_spline_control_point_def_struct(self):
        self.assertIn("SplineControlPointDef", _read("SplineDeformerTool"))

    def test_deformation_bake_def_struct(self):
        self.assertIn("DeformationBakeDef", _read("SplineDeformerTool"))

    def test_create_deformer_method(self):
        self.assertIn("CreateDeformer", _read("SplineDeformerTool"))

    def test_add_control_point_method(self):
        self.assertIn("AddControlPoint", _read("SplineDeformerTool"))

    def test_execute_bake_method(self):
        self.assertIn("ExecuteBake", _read("SplineDeformerTool"))


if __name__ == "__main__":
    unittest.main()
