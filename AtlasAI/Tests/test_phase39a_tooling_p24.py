"""Phase 39A — Tests for P24 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P24_TOOLS = [
    "MorphTargetEditorTool",
    "PixelInspectorTool",
    "BlueprintMacroLibraryTool",
    "AnimationCurveEditorTool",
    "AssetBundleComposerTool",
    "VoxelPaintTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP24ToolsExist(unittest.TestCase):
    def test_morph_target_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MorphTargetEditorTool.h").exists())

    def test_pixel_inspector_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "PixelInspectorTool.h").exists())

    def test_blueprint_macro_library_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "BlueprintMacroLibraryTool.h").exists())

    def test_animation_curve_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AnimationCurveEditorTool.h").exists())

    def test_asset_bundle_composer_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AssetBundleComposerTool.h").exists())

    def test_voxel_paint_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "VoxelPaintTool.h").exists())


class TestP24PragmaOnce(unittest.TestCase):
    def test_morph_target_editor_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("MorphTargetEditorTool"))

    def test_pixel_inspector_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("PixelInspectorTool"))

    def test_blueprint_macro_library_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("BlueprintMacroLibraryTool"))

    def test_animation_curve_editor_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("AnimationCurveEditorTool"))

    def test_asset_bundle_composer_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("AssetBundleComposerTool"))

    def test_voxel_paint_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("VoxelPaintTool"))


class TestP24ToolName(unittest.TestCase):
    def test_morph_target_editor_tool_class_name(self):
        self.assertIn("MorphTargetEditorTool", _read("MorphTargetEditorTool"))

    def test_pixel_inspector_tool_class_name(self):
        self.assertIn("PixelInspectorTool", _read("PixelInspectorTool"))

    def test_blueprint_macro_library_tool_class_name(self):
        self.assertIn("BlueprintMacroLibraryTool", _read("BlueprintMacroLibraryTool"))

    def test_animation_curve_editor_tool_class_name(self):
        self.assertIn("AnimationCurveEditorTool", _read("AnimationCurveEditorTool"))

    def test_asset_bundle_composer_tool_class_name(self):
        self.assertIn("AssetBundleComposerTool", _read("AssetBundleComposerTool"))

    def test_voxel_paint_tool_class_name(self):
        self.assertIn("VoxelPaintTool", _read("VoxelPaintTool"))


class TestP24ITool(unittest.TestCase):
    def test_morph_target_editor_tool_itool(self):
        self.assertIn(": public ITool", _read("MorphTargetEditorTool"))

    def test_pixel_inspector_tool_itool(self):
        self.assertIn(": public ITool", _read("PixelInspectorTool"))

    def test_blueprint_macro_library_tool_itool(self):
        self.assertIn(": public ITool", _read("BlueprintMacroLibraryTool"))

    def test_animation_curve_editor_tool_itool(self):
        self.assertIn(": public ITool", _read("AnimationCurveEditorTool"))

    def test_asset_bundle_composer_tool_itool(self):
        self.assertIn(": public ITool", _read("AssetBundleComposerTool"))

    def test_voxel_paint_tool_itool(self):
        self.assertIn(": public ITool", _read("VoxelPaintTool"))


class TestMorphTargetEditorToolDetail(unittest.TestCase):
    def test_morph_blend_mode_enum(self):
        self.assertIn("MorphBlendMode", _read("MorphTargetEditorTool"))

    def test_morph_target_def_struct(self):
        self.assertIn("MorphTargetDef", _read("MorphTargetEditorTool"))

    def test_add_corrective_method(self):
        self.assertIn("AddCorrective", _read("MorphTargetEditorTool"))

    def test_morph_target_scope_enum(self):
        self.assertIn("MorphTargetScope", _read("MorphTargetEditorTool"))


class TestPixelInspectorToolDetail(unittest.TestCase):
    def test_inspector_channel_enum(self):
        self.assertIn("InspectorChannel", _read("PixelInspectorTool"))

    def test_pixel_sample_def_struct(self):
        self.assertIn("PixelSampleDef", _read("PixelInspectorTool"))

    def test_analyze_region_method(self):
        self.assertIn("AnalyzeRegion", _read("PixelInspectorTool"))

    def test_color_space_enum(self):
        self.assertIn("ColorSpace", _read("PixelInspectorTool"))


class TestBlueprintMacroLibraryToolDetail(unittest.TestCase):
    def test_macro_scope_enum(self):
        self.assertIn("MacroScope", _read("BlueprintMacroLibraryTool"))

    def test_macro_library_def_struct(self):
        self.assertIn("MacroLibraryDef", _read("BlueprintMacroLibraryTool"))

    def test_add_tunnel_method(self):
        self.assertIn("AddTunnel", _read("BlueprintMacroLibraryTool"))

    def test_tunnel_io_type_enum(self):
        self.assertIn("TunnelIOType", _read("BlueprintMacroLibraryTool"))


class TestAnimationCurveEditorToolDetail(unittest.TestCase):
    def test_curve_tangent_mode_enum(self):
        self.assertIn("CurveTangentMode", _read("AnimationCurveEditorTool"))

    def test_anim_curve_keyframe_struct(self):
        self.assertIn("AnimCurveKeyframe", _read("AnimationCurveEditorTool"))

    def test_add_keyframe_method(self):
        self.assertIn("AddKeyframe", _read("AnimationCurveEditorTool"))

    def test_curve_extrapolation_enum(self):
        self.assertIn("CurveExtrapolation", _read("AnimationCurveEditorTool"))


class TestAssetBundleComposerToolDetail(unittest.TestCase):
    def test_bundle_target_platform_enum(self):
        self.assertIn("BundleTargetPlatform", _read("AssetBundleComposerTool"))

    def test_asset_bundle_def_struct(self):
        self.assertIn("AssetBundleDef", _read("AssetBundleComposerTool"))

    def test_create_patch_method(self):
        self.assertIn("CreatePatch", _read("AssetBundleComposerTool"))

    def test_patch_strategy_enum(self):
        self.assertIn("PatchStrategy", _read("AssetBundleComposerTool"))


class TestVoxelPaintToolDetail(unittest.TestCase):
    def test_voxel_paint_mode_enum(self):
        self.assertIn("VoxelPaintMode", _read("VoxelPaintTool"))

    def test_voxel_brush_def_struct(self):
        self.assertIn("VoxelBrushDef", _read("VoxelPaintTool"))

    def test_begin_stroke_method(self):
        self.assertIn("BeginStroke", _read("VoxelPaintTool"))

    def test_voxel_brush_shape_enum(self):
        self.assertIn("VoxelBrushShape", _read("VoxelPaintTool"))


if __name__ == "__main__":
    unittest.main()
