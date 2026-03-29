"""Phase 29A — Tests for P14 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P14_TOOLS = [
    "GameplayTagEditorTool",
    "DataTableEditorTool",
    "LocalizationEditorTool",
    "SequenceRecorderTool",
    "AssetPackagingTool",
    "ViewportGridTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP14ToolsExist(unittest.TestCase):
    def test_gameplay_tag_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "GameplayTagEditorTool.h").exists())

    def test_data_table_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "DataTableEditorTool.h").exists())

    def test_localization_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "LocalizationEditorTool.h").exists())

    def test_sequence_recorder_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SequenceRecorderTool.h").exists())

    def test_asset_packaging_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AssetPackagingTool.h").exists())

    def test_viewport_grid_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ViewportGridTool.h").exists())


class TestP14PragmaOnce(unittest.TestCase):
    def test_gameplay_tag_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("GameplayTagEditorTool"))

    def test_data_table_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("DataTableEditorTool"))

    def test_localization_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("LocalizationEditorTool"))

    def test_sequence_recorder_pragma_once(self):
        self.assertIn("#pragma once", _read("SequenceRecorderTool"))

    def test_asset_packaging_pragma_once(self):
        self.assertIn("#pragma once", _read("AssetPackagingTool"))

    def test_viewport_grid_pragma_once(self):
        self.assertIn("#pragma once", _read("ViewportGridTool"))


class TestP14Inheritance(unittest.TestCase):
    def test_gameplay_tag_editor_inherits_itool(self):
        self.assertIn(": public ITool", _read("GameplayTagEditorTool"))

    def test_data_table_editor_inherits_itool(self):
        self.assertIn(": public ITool", _read("DataTableEditorTool"))

    def test_localization_editor_inherits_itool(self):
        self.assertIn(": public ITool", _read("LocalizationEditorTool"))

    def test_sequence_recorder_inherits_itool(self):
        self.assertIn(": public ITool", _read("SequenceRecorderTool"))

    def test_asset_packaging_inherits_itool(self):
        self.assertIn(": public ITool", _read("AssetPackagingTool"))

    def test_viewport_grid_inherits_itool(self):
        self.assertIn(": public ITool", _read("ViewportGridTool"))


class TestP14GetToolName(unittest.TestCase):
    def test_gameplay_tag_editor_get_tool_name(self):
        self.assertIn("GetToolName", _read("GameplayTagEditorTool"))
        self.assertIn('"GameplayTagEditorTool"', _read("GameplayTagEditorTool"))

    def test_data_table_editor_get_tool_name(self):
        self.assertIn("GetToolName", _read("DataTableEditorTool"))
        self.assertIn('"DataTableEditorTool"', _read("DataTableEditorTool"))

    def test_localization_editor_get_tool_name(self):
        self.assertIn("GetToolName", _read("LocalizationEditorTool"))
        self.assertIn('"LocalizationEditorTool"', _read("LocalizationEditorTool"))

    def test_sequence_recorder_get_tool_name(self):
        self.assertIn("GetToolName", _read("SequenceRecorderTool"))
        self.assertIn('"SequenceRecorderTool"', _read("SequenceRecorderTool"))

    def test_asset_packaging_get_tool_name(self):
        self.assertIn("GetToolName", _read("AssetPackagingTool"))
        self.assertIn('"AssetPackagingTool"', _read("AssetPackagingTool"))

    def test_viewport_grid_get_tool_name(self):
        self.assertIn("GetToolName", _read("ViewportGridTool"))
        self.assertIn('"ViewportGridTool"', _read("ViewportGridTool"))


class TestP14Namespace(unittest.TestCase):
    def test_gameplay_tag_editor_namespace(self):
        self.assertIn("Atlas::Editor", _read("GameplayTagEditorTool"))

    def test_data_table_editor_namespace(self):
        self.assertIn("Atlas::Editor", _read("DataTableEditorTool"))

    def test_localization_editor_namespace(self):
        self.assertIn("Atlas::Editor", _read("LocalizationEditorTool"))

    def test_sequence_recorder_namespace(self):
        self.assertIn("Atlas::Editor", _read("SequenceRecorderTool"))

    def test_asset_packaging_namespace(self):
        self.assertIn("Atlas::Editor", _read("AssetPackagingTool"))

    def test_viewport_grid_namespace(self):
        self.assertIn("Atlas::Editor", _read("ViewportGridTool"))


class TestP14SpecializedAPI(unittest.TestCase):
    def test_gameplay_tag_tag_scope(self):
        content = _read("GameplayTagEditorTool")
        self.assertIn("TagScope", content)
        self.assertIn("TagHierarchyNode", content)

    def test_data_table_column_type(self):
        content = _read("DataTableEditorTool")
        self.assertIn("ColumnType", content)
        self.assertIn("TableSchema", content)

    def test_localization_editor_locale_status(self):
        content = _read("LocalizationEditorTool")
        self.assertIn("LocaleStatus", content)
        self.assertIn("GlossaryTerm", content)

    def test_sequence_recorder_record_state(self):
        content = _read("SequenceRecorderTool")
        self.assertIn("RecordState", content)
        self.assertIn("TrackType", content)

    def test_asset_packaging_package_format(self):
        content = _read("AssetPackagingTool")
        self.assertIn("PackageFormat", content)
        self.assertIn("CompressionMode", content)

    def test_viewport_grid_grid_type(self):
        content = _read("ViewportGridTool")
        self.assertIn("GridType", content)
        self.assertIn("SnapSettings", content)


if __name__ == "__main__":
    unittest.main()
