"""Phase 30A — Tests for P15 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P15_TOOLS = [
    "CinematicDirectorTool",
    "NetworkReplicationTool",
    "InputActionMapTool",
    "RuntimeDebugOverlayTool",
    "MaterialInstanceTool",
    "EventGraphEditorTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP15ToolsExist(unittest.TestCase):
    def test_cinematic_director_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "CinematicDirectorTool.h").exists())

    def test_network_replication_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "NetworkReplicationTool.h").exists())

    def test_input_action_map_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "InputActionMapTool.h").exists())

    def test_runtime_debug_overlay_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "RuntimeDebugOverlayTool.h").exists())

    def test_material_instance_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MaterialInstanceTool.h").exists())

    def test_event_graph_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "EventGraphEditorTool.h").exists())


class TestP15PragmaOnce(unittest.TestCase):
    def test_cinematic_director_pragma_once(self):
        self.assertIn("#pragma once", _read("CinematicDirectorTool"))

    def test_network_replication_pragma_once(self):
        self.assertIn("#pragma once", _read("NetworkReplicationTool"))

    def test_input_action_map_pragma_once(self):
        self.assertIn("#pragma once", _read("InputActionMapTool"))

    def test_runtime_debug_overlay_pragma_once(self):
        self.assertIn("#pragma once", _read("RuntimeDebugOverlayTool"))

    def test_material_instance_pragma_once(self):
        self.assertIn("#pragma once", _read("MaterialInstanceTool"))

    def test_event_graph_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("EventGraphEditorTool"))


class TestP15ToolName(unittest.TestCase):
    def test_cinematic_director_tool_class_name(self):
        self.assertIn("CinematicDirectorTool", _read("CinematicDirectorTool"))

    def test_network_replication_tool_class_name(self):
        self.assertIn("NetworkReplicationTool", _read("NetworkReplicationTool"))

    def test_input_action_map_tool_class_name(self):
        self.assertIn("InputActionMapTool", _read("InputActionMapTool"))

    def test_runtime_debug_overlay_tool_class_name(self):
        self.assertIn("RuntimeDebugOverlayTool", _read("RuntimeDebugOverlayTool"))

    def test_material_instance_tool_class_name(self):
        self.assertIn("MaterialInstanceTool", _read("MaterialInstanceTool"))

    def test_event_graph_editor_tool_class_name(self):
        self.assertIn("EventGraphEditorTool", _read("EventGraphEditorTool"))


class TestP15ITool(unittest.TestCase):
    def test_cinematic_director_inherits_itool(self):
        self.assertIn(": public ITool", _read("CinematicDirectorTool"))

    def test_network_replication_inherits_itool(self):
        self.assertIn(": public ITool", _read("NetworkReplicationTool"))

    def test_input_action_map_inherits_itool(self):
        self.assertIn(": public ITool", _read("InputActionMapTool"))

    def test_runtime_debug_overlay_inherits_itool(self):
        self.assertIn(": public ITool", _read("RuntimeDebugOverlayTool"))

    def test_material_instance_inherits_itool(self):
        self.assertIn(": public ITool", _read("MaterialInstanceTool"))

    def test_event_graph_editor_inherits_itool(self):
        self.assertIn(": public ITool", _read("EventGraphEditorTool"))


class TestCinematicDirectorToolDetail(unittest.TestCase):
    def test_shot_type_enum(self):
        self.assertIn("ShotType", _read("CinematicDirectorTool"))

    def test_director_timeline_struct(self):
        self.assertIn("DirectorTimeline", _read("CinematicDirectorTool"))

    def test_create_shot_method(self):
        self.assertIn("CreateShot", _read("CinematicDirectorTool"))

    def test_export_timeline_method(self):
        self.assertIn("ExportTimeline", _read("CinematicDirectorTool"))


class TestNetworkReplicationToolDetail(unittest.TestCase):
    def test_replica_policy_enum(self):
        self.assertIn("ReplicaPolicy", _read("NetworkReplicationTool"))

    def test_entity_net_config_struct(self):
        self.assertIn("EntityNetConfig", _read("NetworkReplicationTool"))

    def test_create_entity_config_method(self):
        self.assertIn("CreateEntityConfig", _read("NetworkReplicationTool"))

    def test_export_replication_manifest_method(self):
        self.assertIn("ExportReplicationManifest", _read("NetworkReplicationTool"))


class TestInputActionMapToolDetail(unittest.TestCase):
    def test_input_device_enum(self):
        self.assertIn("InputDevice", _read("InputActionMapTool"))

    def test_input_action_struct(self):
        self.assertIn("InputAction", _read("InputActionMapTool"))

    def test_create_action_method(self):
        self.assertIn("CreateAction", _read("InputActionMapTool"))

    def test_activate_context_method(self):
        self.assertIn("ActivateContext", _read("InputActionMapTool"))


class TestRuntimeDebugOverlayToolDetail(unittest.TestCase):
    def test_overlay_panel_enum(self):
        self.assertIn("OverlayPanel", _read("RuntimeDebugOverlayTool"))

    def test_overlay_config_struct(self):
        self.assertIn("OverlayConfig", _read("RuntimeDebugOverlayTool"))

    def test_add_panel_method(self):
        self.assertIn("AddPanel", _read("RuntimeDebugOverlayTool"))

    def test_add_visualiser_method(self):
        self.assertIn("AddVisualiser", _read("RuntimeDebugOverlayTool"))


class TestMaterialInstanceToolDetail(unittest.TestCase):
    def test_parameter_type_enum(self):
        self.assertIn("ParameterType", _read("MaterialInstanceTool"))

    def test_material_instance_def_struct(self):
        self.assertIn("MaterialInstanceDef", _read("MaterialInstanceTool"))

    def test_create_instance_method(self):
        self.assertIn("CreateInstance", _read("MaterialInstanceTool"))

    def test_apply_variant_method(self):
        self.assertIn("ApplyVariant", _read("MaterialInstanceTool"))


class TestEventGraphEditorToolDetail(unittest.TestCase):
    def test_node_type_enum(self):
        self.assertIn("NodeType", _read("EventGraphEditorTool"))

    def test_event_graph_struct(self):
        self.assertIn("EventGraph", _read("EventGraphEditorTool"))

    def test_create_graph_method(self):
        self.assertIn("CreateGraph", _read("EventGraphEditorTool"))

    def test_compile_graph_method(self):
        self.assertIn("CompileGraph", _read("EventGraphEditorTool"))


if __name__ == "__main__":
    unittest.main()
