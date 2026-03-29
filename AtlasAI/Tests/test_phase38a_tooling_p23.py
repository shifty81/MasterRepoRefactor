"""Phase 38A — Tests for P23 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P23_TOOLS = [
    "CurveLinearColorTool",
    "ActorPaletteTool",
    "ImportExportProfileTool",
    "NetworkProfilerTool",
    "SlateBlueprintTool",
    "MaterialParameterCollectionTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP23ToolsExist(unittest.TestCase):
    def test_curve_linear_color_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "CurveLinearColorTool.h").exists())

    def test_actor_palette_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ActorPaletteTool.h").exists())

    def test_import_export_profile_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ImportExportProfileTool.h").exists())

    def test_network_profiler_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "NetworkProfilerTool.h").exists())

    def test_slate_blueprint_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SlateBlueprintTool.h").exists())

    def test_material_parameter_collection_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MaterialParameterCollectionTool.h").exists())


class TestP23PragmaOnce(unittest.TestCase):
    def test_curve_linear_color_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("CurveLinearColorTool"))

    def test_actor_palette_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("ActorPaletteTool"))

    def test_import_export_profile_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("ImportExportProfileTool"))

    def test_network_profiler_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("NetworkProfilerTool"))

    def test_slate_blueprint_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("SlateBlueprintTool"))

    def test_material_parameter_collection_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("MaterialParameterCollectionTool"))


class TestP23ToolName(unittest.TestCase):
    def test_curve_linear_color_tool_class_name(self):
        self.assertIn("CurveLinearColorTool", _read("CurveLinearColorTool"))

    def test_actor_palette_tool_class_name(self):
        self.assertIn("ActorPaletteTool", _read("ActorPaletteTool"))

    def test_import_export_profile_tool_class_name(self):
        self.assertIn("ImportExportProfileTool", _read("ImportExportProfileTool"))

    def test_network_profiler_tool_class_name(self):
        self.assertIn("NetworkProfilerTool", _read("NetworkProfilerTool"))

    def test_slate_blueprint_tool_class_name(self):
        self.assertIn("SlateBlueprintTool", _read("SlateBlueprintTool"))

    def test_material_parameter_collection_tool_class_name(self):
        self.assertIn("MaterialParameterCollectionTool", _read("MaterialParameterCollectionTool"))


class TestP23ITool(unittest.TestCase):
    def test_curve_linear_color_tool_itool(self):
        self.assertIn(": public ITool", _read("CurveLinearColorTool"))

    def test_actor_palette_tool_itool(self):
        self.assertIn(": public ITool", _read("ActorPaletteTool"))

    def test_import_export_profile_tool_itool(self):
        self.assertIn(": public ITool", _read("ImportExportProfileTool"))

    def test_network_profiler_tool_itool(self):
        self.assertIn(": public ITool", _read("NetworkProfilerTool"))

    def test_slate_blueprint_tool_itool(self):
        self.assertIn(": public ITool", _read("SlateBlueprintTool"))

    def test_material_parameter_collection_tool_itool(self):
        self.assertIn(": public ITool", _read("MaterialParameterCollectionTool"))


class TestCurveLinearColorToolDetail(unittest.TestCase):
    def test_curve_interpolation_enum(self):
        self.assertIn("CurveInterpolation", _read("CurveLinearColorTool"))

    def test_color_keyframe_def_struct(self):
        self.assertIn("ColorKeyframeDef", _read("CurveLinearColorTool"))

    def test_bake_gradient_method(self):
        self.assertIn("BakeGradient", _read("CurveLinearColorTool"))

    def test_gradient_bake_mode_enum(self):
        self.assertIn("GradientBakeMode", _read("CurveLinearColorTool"))


class TestActorPaletteToolDetail(unittest.TestCase):
    def test_palette_category_enum(self):
        self.assertIn("PaletteCategory", _read("ActorPaletteTool"))

    def test_palette_actor_def_struct(self):
        self.assertIn("PaletteActorDef", _read("ActorPaletteTool"))

    def test_begin_stamp_method(self):
        self.assertIn("BeginStamp", _read("ActorPaletteTool"))

    def test_placement_mode_enum(self):
        self.assertIn("PlacementMode", _read("ActorPaletteTool"))


class TestImportExportProfileToolDetail(unittest.TestCase):
    def test_transfer_direction_enum(self):
        self.assertIn("TransferDirection", _read("ImportExportProfileTool"))

    def test_import_export_profile_def_struct(self):
        self.assertIn("ImportExportProfileDef", _read("ImportExportProfileTool"))

    def test_start_batch_job_method(self):
        self.assertIn("StartBatchJob", _read("ImportExportProfileTool"))

    def test_batch_status_enum(self):
        self.assertIn("BatchStatus", _read("ImportExportProfileTool"))


class TestNetworkProfilerToolDetail(unittest.TestCase):
    def test_profiler_session_state_enum(self):
        self.assertIn("ProfilerSessionState", _read("NetworkProfilerTool"))

    def test_network_sample_def_struct(self):
        self.assertIn("NetworkSampleDef", _read("NetworkProfilerTool"))

    def test_start_recording_method(self):
        self.assertIn("StartRecording", _read("NetworkProfilerTool"))

    def test_network_metric_type_enum(self):
        self.assertIn("NetworkMetricType", _read("NetworkProfilerTool"))


class TestSlateBlueprintToolDetail(unittest.TestCase):
    def test_widget_slot_type_enum(self):
        self.assertIn("WidgetSlotType", _read("SlateBlueprintTool"))

    def test_slate_widget_def_struct(self):
        self.assertIn("SlateWidgetDef", _read("SlateBlueprintTool"))

    def test_add_binding_method(self):
        self.assertIn("AddBinding", _read("SlateBlueprintTool"))

    def test_binding_mode_enum(self):
        self.assertIn("BindingMode", _read("SlateBlueprintTool"))


class TestMaterialParameterCollectionToolDetail(unittest.TestCase):
    def test_parameter_type_enum(self):
        self.assertIn("ParameterType", _read("MaterialParameterCollectionTool"))

    def test_mpc_parameter_def_struct(self):
        self.assertIn("MPCParameterDef", _read("MaterialParameterCollectionTool"))

    def test_add_override_method(self):
        self.assertIn("AddOverride", _read("MaterialParameterCollectionTool"))

    def test_collection_scope_enum(self):
        self.assertIn("CollectionScope", _read("MaterialParameterCollectionTool"))


if __name__ == "__main__":
    unittest.main()
