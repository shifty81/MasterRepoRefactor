"""Phase 34A — Tests for P19 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P19_TOOLS = [
    "InterchangeTool",
    "MetaSoundTool",
    "PCGEditorTool",
    "WorldPartitionTool",
    "DataLayerTool",
    "AssetRegistryTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP19ToolsExist(unittest.TestCase):
    def test_interchange_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "InterchangeTool.h").exists())

    def test_meta_sound_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MetaSoundTool.h").exists())

    def test_pcg_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "PCGEditorTool.h").exists())

    def test_world_partition_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "WorldPartitionTool.h").exists())

    def test_data_layer_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "DataLayerTool.h").exists())

    def test_asset_registry_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AssetRegistryTool.h").exists())


class TestP19PragmaOnce(unittest.TestCase):
    def test_interchange_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("InterchangeTool"))

    def test_meta_sound_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("MetaSoundTool"))

    def test_pcg_editor_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("PCGEditorTool"))

    def test_world_partition_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("WorldPartitionTool"))

    def test_data_layer_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("DataLayerTool"))

    def test_asset_registry_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("AssetRegistryTool"))


class TestP19ToolName(unittest.TestCase):
    def test_interchange_tool_class_name(self):
        self.assertIn("InterchangeTool", _read("InterchangeTool"))

    def test_meta_sound_tool_class_name(self):
        self.assertIn("MetaSoundTool", _read("MetaSoundTool"))

    def test_pcg_editor_tool_class_name(self):
        self.assertIn("PCGEditorTool", _read("PCGEditorTool"))

    def test_world_partition_tool_class_name(self):
        self.assertIn("WorldPartitionTool", _read("WorldPartitionTool"))

    def test_data_layer_tool_class_name(self):
        self.assertIn("DataLayerTool", _read("DataLayerTool"))

    def test_asset_registry_tool_class_name(self):
        self.assertIn("AssetRegistryTool", _read("AssetRegistryTool"))


class TestP19ITool(unittest.TestCase):
    def test_interchange_tool_itool(self):
        self.assertIn(": public ITool", _read("InterchangeTool"))

    def test_meta_sound_tool_itool(self):
        self.assertIn(": public ITool", _read("MetaSoundTool"))

    def test_pcg_editor_tool_itool(self):
        self.assertIn(": public ITool", _read("PCGEditorTool"))

    def test_world_partition_tool_itool(self):
        self.assertIn(": public ITool", _read("WorldPartitionTool"))

    def test_data_layer_tool_itool(self):
        self.assertIn(": public ITool", _read("DataLayerTool"))

    def test_asset_registry_tool_itool(self):
        self.assertIn(": public ITool", _read("AssetRegistryTool"))


class TestInterchangeToolDetail(unittest.TestCase):
    def test_translator_type_enum(self):
        self.assertIn("TranslatorType", _read("InterchangeTool"))

    def test_pipeline_def_struct(self):
        self.assertIn("PipelineDef", _read("InterchangeTool"))

    def test_create_pipeline_method(self):
        self.assertIn("CreatePipeline", _read("InterchangeTool"))

    def test_run_pipeline_method(self):
        self.assertIn("RunPipeline", _read("InterchangeTool"))


class TestMetaSoundToolDetail(unittest.TestCase):
    def test_meta_sound_node_type_enum(self):
        self.assertIn("MetaSoundNodeType", _read("MetaSoundTool"))

    def test_meta_sound_graph_def_struct(self):
        self.assertIn("MetaSoundGraphDef", _read("MetaSoundTool"))

    def test_create_graph_method(self):
        self.assertIn("CreateGraph", _read("MetaSoundTool"))

    def test_export_graph_method(self):
        self.assertIn("ExportGraph", _read("MetaSoundTool"))


class TestPCGEditorToolDetail(unittest.TestCase):
    def test_pcg_node_category_enum(self):
        self.assertIn("PCGNodeCategory", _read("PCGEditorTool"))

    def test_pcg_graph_property_struct(self):
        self.assertIn("PCGGraphProperty", _read("PCGEditorTool"))

    def test_create_graph_method(self):
        self.assertIn("CreateGraph", _read("PCGEditorTool"))

    def test_execute_graph_method(self):
        self.assertIn("ExecuteGraph", _read("PCGEditorTool"))


class TestWorldPartitionToolDetail(unittest.TestCase):
    def test_streaming_source_type_enum(self):
        self.assertIn("StreamingSourceType", _read("WorldPartitionTool"))

    def test_world_partition_cell_struct(self):
        self.assertIn("WorldPartitionCell", _read("WorldPartitionTool"))

    def test_set_grid_config_method(self):
        self.assertIn("SetGridConfig", _read("WorldPartitionTool"))

    def test_force_load_cell_method(self):
        self.assertIn("ForceLoadCell", _read("WorldPartitionTool"))


class TestDataLayerToolDetail(unittest.TestCase):
    def test_data_layer_state_enum(self):
        self.assertIn("DataLayerState", _read("DataLayerTool"))

    def test_data_layer_def_struct(self):
        self.assertIn("DataLayerDef", _read("DataLayerTool"))

    def test_create_data_layer_method(self):
        self.assertIn("CreateDataLayer", _read("DataLayerTool"))

    def test_export_layers_method(self):
        self.assertIn("ExportLayers", _read("DataLayerTool"))


class TestAssetRegistryToolDetail(unittest.TestCase):
    def test_asset_loading_state_enum(self):
        self.assertIn("AssetLoadingState", _read("AssetRegistryTool"))

    def test_asset_filter_def_struct(self):
        self.assertIn("AssetFilterDef", _read("AssetRegistryTool"))

    def test_create_filter_method(self):
        self.assertIn("CreateFilter", _read("AssetRegistryTool"))

    def test_scan_assets_method(self):
        self.assertIn("ScanAssets", _read("AssetRegistryTool"))


if __name__ == "__main__":
    unittest.main()
