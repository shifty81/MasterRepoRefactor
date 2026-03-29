"""Phase 18A — Tests for P2 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P2_TOOLS = [
    "FunctionAssignmentTool",
    "EventTimelineTool",
    "NPCSpawnerTool",
    "MapEditorTool",
    "ShipModuleEditorTool",
    "ResourceBalancerTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP2ToolsExist(unittest.TestCase):
    def test_function_assignment_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "FunctionAssignmentTool.h").exists())

    def test_event_timeline_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "EventTimelineTool.h").exists())

    def test_npc_spawner_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "NPCSpawnerTool.h").exists())

    def test_map_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MapEditorTool.h").exists())

    def test_ship_module_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ShipModuleEditorTool.h").exists())

    def test_resource_balancer_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ResourceBalancerTool.h").exists())

    def test_itool_h_exists_in_same_dir(self):
        self.assertTrue((TOOL_LAYER / "ITool.h").exists())


class TestP2PragmaOnce(unittest.TestCase):
    def test_function_assignment_pragma_once(self):
        self.assertIn("#pragma once", _read("FunctionAssignmentTool"))

    def test_event_timeline_pragma_once(self):
        self.assertIn("#pragma once", _read("EventTimelineTool"))

    def test_npc_spawner_pragma_once(self):
        self.assertIn("#pragma once", _read("NPCSpawnerTool"))

    def test_map_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("MapEditorTool"))

    def test_ship_module_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("ShipModuleEditorTool"))

    def test_resource_balancer_pragma_once(self):
        self.assertIn("#pragma once", _read("ResourceBalancerTool"))


class TestP2Inheritance(unittest.TestCase):
    def test_function_assignment_inherits_itool(self):
        self.assertIn("ITool", _read("FunctionAssignmentTool"))

    def test_event_timeline_inherits_itool(self):
        self.assertIn("ITool", _read("EventTimelineTool"))

    def test_npc_spawner_inherits_itool(self):
        self.assertIn("ITool", _read("NPCSpawnerTool"))

    def test_map_editor_inherits_itool(self):
        self.assertIn("ITool", _read("MapEditorTool"))

    def test_ship_module_editor_inherits_itool(self):
        self.assertIn("ITool", _read("ShipModuleEditorTool"))

    def test_resource_balancer_inherits_itool(self):
        self.assertIn("ITool", _read("ResourceBalancerTool"))


class TestP2ClassName(unittest.TestCase):
    def test_function_assignment_class_name(self):
        self.assertIn("class FunctionAssignmentTool", _read("FunctionAssignmentTool"))

    def test_event_timeline_class_name(self):
        self.assertIn("class EventTimelineTool", _read("EventTimelineTool"))

    def test_npc_spawner_class_name(self):
        self.assertIn("class NPCSpawnerTool", _read("NPCSpawnerTool"))

    def test_map_editor_class_name(self):
        self.assertIn("class MapEditorTool", _read("MapEditorTool"))

    def test_ship_module_editor_class_name(self):
        self.assertIn("class ShipModuleEditorTool", _read("ShipModuleEditorTool"))

    def test_resource_balancer_class_name(self):
        self.assertIn("class ResourceBalancerTool", _read("ResourceBalancerTool"))


class TestP2CoreMethods(unittest.TestCase):
    def _assert_methods(self, name: str) -> None:
        content = _read(name)
        self.assertIn("GetToolName", content)
        self.assertIn("IsActive", content)
        self.assertIn("Activate", content)
        self.assertIn("Deactivate", content)
        self.assertIn("Update", content)
        self.assertIn("OnMouseDown", content)
        self.assertIn("OnMouseUp", content)
        self.assertIn("OnKeyDown", content)

    def test_function_assignment_core_methods(self):
        self._assert_methods("FunctionAssignmentTool")

    def test_event_timeline_core_methods(self):
        self._assert_methods("EventTimelineTool")

    def test_npc_spawner_core_methods(self):
        self._assert_methods("NPCSpawnerTool")

    def test_map_editor_core_methods(self):
        self._assert_methods("MapEditorTool")

    def test_ship_module_editor_core_methods(self):
        self._assert_methods("ShipModuleEditorTool")

    def test_resource_balancer_core_methods(self):
        self._assert_methods("ResourceBalancerTool")


class TestP2GetToolNameReturns(unittest.TestCase):
    def test_function_assignment_tool_name_return(self):
        self.assertIn('"FunctionAssignmentTool"', _read("FunctionAssignmentTool"))

    def test_event_timeline_tool_name_return(self):
        self.assertIn('"EventTimelineTool"', _read("EventTimelineTool"))

    def test_npc_spawner_tool_name_return(self):
        self.assertIn('"NPCSpawnerTool"', _read("NPCSpawnerTool"))

    def test_map_editor_tool_name_return(self):
        self.assertIn('"MapEditorTool"', _read("MapEditorTool"))

    def test_ship_module_editor_tool_name_return(self):
        self.assertIn('"ShipModuleEditorTool"', _read("ShipModuleEditorTool"))

    def test_resource_balancer_tool_name_return(self):
        self.assertIn('"ResourceBalancerTool"', _read("ResourceBalancerTool"))


class TestTimelineEventStruct(unittest.TestCase):
    def test_timeline_event_struct_exists(self):
        self.assertIn("struct TimelineEvent", _read("EventTimelineTool"))

    def test_timeline_event_time_seconds_field(self):
        self.assertIn("timeSeconds", _read("EventTimelineTool"))

    def test_timeline_event_event_name_field(self):
        self.assertIn("eventName", _read("EventTimelineTool"))

    def test_timeline_event_target_entity_id_field(self):
        self.assertIn("targetEntityId", _read("EventTimelineTool"))

    def test_event_timeline_play_stop_methods(self):
        content = _read("EventTimelineTool")
        self.assertIn("Play", content)
        self.assertIn("Stop", content)

    def test_event_timeline_scrub_to(self):
        self.assertIn("ScrubTo", _read("EventTimelineTool"))


class TestMapNodeStruct(unittest.TestCase):
    def test_map_node_struct_exists(self):
        self.assertIn("struct MapNode", _read("MapEditorTool"))

    def test_map_node_id_field(self):
        content = _read("MapEditorTool")
        self.assertIn("std::string id", content)

    def test_map_node_type_field(self):
        content = _read("MapEditorTool")
        self.assertIn("std::string type", content)

    def test_map_node_orbit_radius_field(self):
        self.assertIn("orbitRadius", _read("MapEditorTool"))

    def test_map_editor_add_remove_move(self):
        content = _read("MapEditorTool")
        self.assertIn("AddNode", content)
        self.assertIn("RemoveNode", content)
        self.assertIn("MoveNode", content)


class TestResourceZoneStruct(unittest.TestCase):
    def test_resource_zone_struct_exists(self):
        self.assertIn("struct ResourceZone", _read("ResourceBalancerTool"))

    def test_resource_zone_zone_id_field(self):
        self.assertIn("zoneId", _read("ResourceBalancerTool"))

    def test_resource_zone_resource_type_field(self):
        self.assertIn("resourceType", _read("ResourceBalancerTool"))

    def test_resource_zone_abundance_field(self):
        self.assertIn("abundance", _read("ResourceBalancerTool"))

    def test_resource_balancer_normalize_all(self):
        self.assertIn("NormalizeAll", _read("ResourceBalancerTool"))

    def test_resource_balancer_export_config(self):
        self.assertIn("ExportConfig", _read("ResourceBalancerTool"))


class TestP2SpecificMethods(unittest.TestCase):
    def test_function_assignment_assign_remove(self):
        content = _read("FunctionAssignmentTool")
        self.assertIn("AssignFunction", content)
        self.assertIn("RemoveFunction", content)

    def test_npc_spawner_spawn_at(self):
        self.assertIn("SpawnAt", _read("NPCSpawnerTool"))

    def test_npc_spawner_despawn_all(self):
        self.assertIn("DespawnAll", _read("NPCSpawnerTool"))

    def test_ship_module_fit_unfit(self):
        content = _read("ShipModuleEditorTool")
        self.assertIn("FitModule", content)
        self.assertIn("UnfitModule", content)

    def test_ship_module_swap(self):
        self.assertIn("SwapModules", _read("ShipModuleEditorTool"))

    def test_ship_module_validate_fit(self):
        self.assertIn("ValidateFit", _read("ShipModuleEditorTool"))


class TestP2ToolsInCorrectDirectory(unittest.TestCase):
    def test_all_p2_tools_in_tool_layer(self):
        for name in P2_TOOLS:
            path = TOOL_LAYER / f"{name}.h"
            self.assertTrue(path.exists(), f"{name}.h not found in ToolLayer")

    def test_tool_layer_path_contains_atlas_editor(self):
        self.assertIn("Atlas", str(TOOL_LAYER))
        self.assertIn("Editor", str(TOOL_LAYER))
        self.assertIn("ToolLayer", str(TOOL_LAYER))


if __name__ == "__main__":
    unittest.main()
