"""Phase 18B — Tests for P3 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P3_TOOLS = [
    "PCGSnapshotManager",
    "DeltaEditsMergeTool",
    "EditPropagationTool",
    "VisualDiffTool",
    "LayerTagSystem",
    "AssetStatsPanel",
    "HotkeyActionManager",
    "ScriptConsole",
    "BatchOperationsTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP3ToolsExist(unittest.TestCase):
    def test_pcg_snapshot_manager_exists(self):
        self.assertTrue((TOOL_LAYER / "PCGSnapshotManager.h").exists())

    def test_delta_edits_merge_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "DeltaEditsMergeTool.h").exists())

    def test_edit_propagation_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "EditPropagationTool.h").exists())

    def test_visual_diff_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "VisualDiffTool.h").exists())

    def test_layer_tag_system_exists(self):
        self.assertTrue((TOOL_LAYER / "LayerTagSystem.h").exists())

    def test_asset_stats_panel_exists(self):
        self.assertTrue((TOOL_LAYER / "AssetStatsPanel.h").exists())

    def test_hotkey_action_manager_exists(self):
        self.assertTrue((TOOL_LAYER / "HotkeyActionManager.h").exists())

    def test_script_console_exists(self):
        self.assertTrue((TOOL_LAYER / "ScriptConsole.h").exists())

    def test_batch_operations_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "BatchOperationsTool.h").exists())


class TestP3PragmaOnce(unittest.TestCase):
    def test_pcg_snapshot_manager_pragma_once(self):
        self.assertIn("#pragma once", _read("PCGSnapshotManager"))

    def test_delta_edits_merge_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("DeltaEditsMergeTool"))

    def test_edit_propagation_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("EditPropagationTool"))

    def test_visual_diff_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("VisualDiffTool"))

    def test_layer_tag_system_pragma_once(self):
        self.assertIn("#pragma once", _read("LayerTagSystem"))

    def test_asset_stats_panel_pragma_once(self):
        self.assertIn("#pragma once", _read("AssetStatsPanel"))

    def test_hotkey_action_manager_pragma_once(self):
        self.assertIn("#pragma once", _read("HotkeyActionManager"))

    def test_script_console_pragma_once(self):
        self.assertIn("#pragma once", _read("ScriptConsole"))

    def test_batch_operations_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("BatchOperationsTool"))


class TestP3ClassNames(unittest.TestCase):
    def test_pcg_snapshot_manager_class(self):
        self.assertIn("class PCGSnapshotManager", _read("PCGSnapshotManager"))

    def test_delta_edits_merge_tool_class(self):
        self.assertIn("class DeltaEditsMergeTool", _read("DeltaEditsMergeTool"))

    def test_edit_propagation_tool_class(self):
        self.assertIn("class EditPropagationTool", _read("EditPropagationTool"))

    def test_visual_diff_tool_class(self):
        self.assertIn("class VisualDiffTool", _read("VisualDiffTool"))

    def test_layer_tag_system_class(self):
        self.assertIn("class LayerTagSystem", _read("LayerTagSystem"))

    def test_asset_stats_panel_class(self):
        self.assertIn("class AssetStatsPanel", _read("AssetStatsPanel"))

    def test_hotkey_action_manager_class(self):
        self.assertIn("class HotkeyActionManager", _read("HotkeyActionManager"))

    def test_script_console_class(self):
        self.assertIn("class ScriptConsole", _read("ScriptConsole"))

    def test_batch_operations_tool_class(self):
        self.assertIn("class BatchOperationsTool", _read("BatchOperationsTool"))


class TestP3CoreMethods(unittest.TestCase):
    def _assert_core(self, name: str) -> None:
        content = _read(name)
        for method in ("GetToolName", "IsActive", "Activate", "Deactivate", "Update"):
            self.assertIn(method, content, f"{method} missing from {name}.h")

    def test_pcg_snapshot_manager_core(self):
        self._assert_core("PCGSnapshotManager")

    def test_delta_edits_merge_tool_core(self):
        self._assert_core("DeltaEditsMergeTool")

    def test_edit_propagation_tool_core(self):
        self._assert_core("EditPropagationTool")

    def test_visual_diff_tool_core(self):
        self._assert_core("VisualDiffTool")

    def test_layer_tag_system_core(self):
        self._assert_core("LayerTagSystem")

    def test_asset_stats_panel_core(self):
        self._assert_core("AssetStatsPanel")

    def test_hotkey_action_manager_core(self):
        self._assert_core("HotkeyActionManager")

    def test_script_console_core(self):
        self._assert_core("ScriptConsole")

    def test_batch_operations_tool_core(self):
        self._assert_core("BatchOperationsTool")


class TestP3GetToolNameReturns(unittest.TestCase):
    def test_pcg_snapshot_manager_name_return(self):
        self.assertIn('"PCGSnapshotManager"', _read("PCGSnapshotManager"))

    def test_delta_edits_merge_tool_name_return(self):
        self.assertIn('"DeltaEditsMergeTool"', _read("DeltaEditsMergeTool"))

    def test_visual_diff_tool_name_return(self):
        self.assertIn('"VisualDiffTool"', _read("VisualDiffTool"))

    def test_layer_tag_system_name_return(self):
        self.assertIn('"LayerTagSystem"', _read("LayerTagSystem"))

    def test_hotkey_action_manager_name_return(self):
        self.assertIn('"HotkeyActionManager"', _read("HotkeyActionManager"))

    def test_script_console_name_return(self):
        self.assertIn('"ScriptConsole"', _read("ScriptConsole"))

    def test_batch_operations_tool_name_return(self):
        self.assertIn('"BatchOperationsTool"', _read("BatchOperationsTool"))


class TestSnapshotStruct(unittest.TestCase):
    def test_snapshot_struct_exists(self):
        self.assertIn("struct Snapshot", _read("PCGSnapshotManager"))

    def test_snapshot_id_field(self):
        content = _read("PCGSnapshotManager")
        self.assertIn("std::string id", content)

    def test_snapshot_label_field(self):
        self.assertIn("label", _read("PCGSnapshotManager"))

    def test_snapshot_revision_field(self):
        self.assertIn("revision", _read("PCGSnapshotManager"))

    def test_pcg_snapshot_capture_restore(self):
        content = _read("PCGSnapshotManager")
        self.assertIn("CaptureSnapshot", content)
        self.assertIn("RestoreSnapshot", content)

    def test_pcg_snapshot_delete(self):
        self.assertIn("DeleteSnapshot", _read("PCGSnapshotManager"))


class TestConflictResolutionEnum(unittest.TestCase):
    def test_conflict_resolution_enum_exists(self):
        self.assertIn("ConflictResolution", _read("DeltaEditsMergeTool"))

    def test_keep_local_value(self):
        self.assertIn("KeepLocal", _read("DeltaEditsMergeTool"))

    def test_keep_remote_value(self):
        self.assertIn("KeepRemote", _read("DeltaEditsMergeTool"))

    def test_merge_value(self):
        self.assertIn("Merge", _read("DeltaEditsMergeTool"))

    def test_delta_edits_load_resolve_commit(self):
        content = _read("DeltaEditsMergeTool")
        self.assertIn("LoadLocalEdits", content)
        self.assertIn("ResolveConflict", content)
        self.assertIn("Commit", content)


class TestDiffModeEnum(unittest.TestCase):
    def test_diff_mode_enum_exists(self):
        self.assertIn("DiffMode", _read("VisualDiffTool"))

    def test_diff_mode_scene_value(self):
        self.assertIn("Scene", _read("VisualDiffTool"))

    def test_diff_mode_asset_value(self):
        self.assertIn("Asset", _read("VisualDiffTool"))

    def test_diff_mode_transform_value(self):
        self.assertIn("Transform", _read("VisualDiffTool"))

    def test_diff_mode_material_value(self):
        self.assertIn("Material", _read("VisualDiffTool"))

    def test_visual_diff_set_baseline_refresh(self):
        content = _read("VisualDiffTool")
        self.assertIn("SetBaseline", content)
        self.assertIn("Refresh", content)


class TestSceneStatsStruct(unittest.TestCase):
    def test_scene_stats_struct_exists(self):
        self.assertIn("struct SceneStats", _read("AssetStatsPanel"))

    def test_total_entities_field(self):
        self.assertIn("totalEntities", _read("AssetStatsPanel"))

    def test_physics_body_count_field(self):
        self.assertIn("physicsBodyCount", _read("AssetStatsPanel"))

    def test_draw_call_count_field(self):
        self.assertIn("drawCallCount", _read("AssetStatsPanel"))

    def test_memory_mb_field(self):
        self.assertIn("memoryMB", _read("AssetStatsPanel"))

    def test_vertex_count_field(self):
        self.assertIn("vertexCount", _read("AssetStatsPanel"))

    def test_asset_stats_refresh_method(self):
        self.assertIn("Refresh", _read("AssetStatsPanel"))

    def test_asset_stats_auto_refresh(self):
        content = _read("AssetStatsPanel")
        self.assertIn("SetAutoRefresh", content)
        self.assertIn("IsAutoRefresh", content)


class TestConsoleEntryStruct(unittest.TestCase):
    def test_console_entry_struct_exists(self):
        self.assertIn("struct ConsoleEntry", _read("ScriptConsole"))

    def test_console_entry_text_field(self):
        self.assertIn("std::string text", _read("ScriptConsole"))

    def test_console_entry_level_field(self):
        self.assertIn("std::string level", _read("ScriptConsole"))

    def test_script_console_execute_print_clear(self):
        content = _read("ScriptConsole")
        self.assertIn("Execute", content)
        self.assertIn("Print", content)
        self.assertIn("Clear", content)


class TestBatchOperationsEnum(unittest.TestCase):
    def test_operation_enum_exists(self):
        self.assertIn("enum class Operation", _read("BatchOperationsTool"))

    def test_translate_operation(self):
        self.assertIn("Translate", _read("BatchOperationsTool"))

    def test_delete_operation(self):
        self.assertIn("Delete", _read("BatchOperationsTool"))

    def test_retag_operation(self):
        self.assertIn("Retag", _read("BatchOperationsTool"))

    def test_batch_add_clear_selection(self):
        content = _read("BatchOperationsTool")
        self.assertIn("AddToSelection", content)
        self.assertIn("ClearSelection", content)

    def test_batch_apply_delete_retag(self):
        content = _read("BatchOperationsTool")
        self.assertIn("ApplyDelete", content)
        self.assertIn("ApplyRetag", content)


class TestLayerTagSystemMethods(unittest.TestCase):
    def test_add_tag_method(self):
        self.assertIn("AddTag", _read("LayerTagSystem"))

    def test_remove_tag_method(self):
        self.assertIn("RemoveTag", _read("LayerTagSystem"))

    def test_set_layer_visible(self):
        self.assertIn("SetLayerVisible", _read("LayerTagSystem"))

    def test_is_layer_visible(self):
        self.assertIn("IsLayerVisible", _read("LayerTagSystem"))

    def test_get_entities_with_tag(self):
        self.assertIn("GetEntitiesWithTag", _read("LayerTagSystem"))


class TestHotkeyActionManagerMethods(unittest.TestCase):
    def test_bind_key(self):
        self.assertIn("BindKey", _read("HotkeyActionManager"))

    def test_unbind_key(self):
        self.assertIn("UnbindKey", _read("HotkeyActionManager"))

    def test_is_action_triggered(self):
        self.assertIn("IsActionTriggered", _read("HotkeyActionManager"))

    def test_reset_to_defaults(self):
        self.assertIn("ResetToDefaults", _read("HotkeyActionManager"))


class TestP3AllInToolLayer(unittest.TestCase):
    def test_all_p3_tools_in_tool_layer(self):
        for name in P3_TOOLS:
            path = TOOL_LAYER / f"{name}.h"
            self.assertTrue(path.exists(), f"{name}.h not in ToolLayer")


if __name__ == "__main__":
    unittest.main()
