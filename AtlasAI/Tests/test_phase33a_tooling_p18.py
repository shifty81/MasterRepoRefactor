"""Phase 33A — Tests for P18 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P18_TOOLS = [
    "EnhancedInputTool",
    "SmartObjectTool",
    "ZoneGraphTool",
    "MassEntityTool",
    "GameplayAbilityTool",
    "EnvironmentQueryTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP18ToolsExist(unittest.TestCase):
    def test_enhanced_input_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "EnhancedInputTool.h").exists())

    def test_smart_object_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SmartObjectTool.h").exists())

    def test_zone_graph_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ZoneGraphTool.h").exists())

    def test_mass_entity_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MassEntityTool.h").exists())

    def test_gameplay_ability_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "GameplayAbilityTool.h").exists())

    def test_environment_query_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "EnvironmentQueryTool.h").exists())


class TestP18PragmaOnce(unittest.TestCase):
    def test_enhanced_input_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("EnhancedInputTool"))

    def test_smart_object_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("SmartObjectTool"))

    def test_zone_graph_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("ZoneGraphTool"))

    def test_mass_entity_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("MassEntityTool"))

    def test_gameplay_ability_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("GameplayAbilityTool"))

    def test_environment_query_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("EnvironmentQueryTool"))


class TestP18ToolName(unittest.TestCase):
    def test_enhanced_input_tool_class_name(self):
        self.assertIn("EnhancedInputTool", _read("EnhancedInputTool"))

    def test_smart_object_tool_class_name(self):
        self.assertIn("SmartObjectTool", _read("SmartObjectTool"))

    def test_zone_graph_tool_class_name(self):
        self.assertIn("ZoneGraphTool", _read("ZoneGraphTool"))

    def test_mass_entity_tool_class_name(self):
        self.assertIn("MassEntityTool", _read("MassEntityTool"))

    def test_gameplay_ability_tool_class_name(self):
        self.assertIn("GameplayAbilityTool", _read("GameplayAbilityTool"))

    def test_environment_query_tool_class_name(self):
        self.assertIn("EnvironmentQueryTool", _read("EnvironmentQueryTool"))


class TestP18ITool(unittest.TestCase):
    def test_enhanced_input_tool_itool(self):
        self.assertIn(": public ITool", _read("EnhancedInputTool"))

    def test_smart_object_tool_itool(self):
        self.assertIn(": public ITool", _read("SmartObjectTool"))

    def test_zone_graph_tool_itool(self):
        self.assertIn(": public ITool", _read("ZoneGraphTool"))

    def test_mass_entity_tool_itool(self):
        self.assertIn(": public ITool", _read("MassEntityTool"))

    def test_gameplay_ability_tool_itool(self):
        self.assertIn(": public ITool", _read("GameplayAbilityTool"))

    def test_environment_query_tool_itool(self):
        self.assertIn(": public ITool", _read("EnvironmentQueryTool"))


class TestEnhancedInputToolDetail(unittest.TestCase):
    def test_input_trigger_type_enum(self):
        self.assertIn("InputTriggerType", _read("EnhancedInputTool"))

    def test_input_action_def_struct(self):
        self.assertIn("InputActionDef", _read("EnhancedInputTool"))

    def test_create_action_method(self):
        self.assertIn("CreateAction", _read("EnhancedInputTool"))

    def test_export_input_config_method(self):
        self.assertIn("ExportInputConfig", _read("EnhancedInputTool"))


class TestSmartObjectToolDetail(unittest.TestCase):
    def test_smart_object_state_enum(self):
        self.assertIn("SmartObjectState", _read("SmartObjectTool"))

    def test_smart_object_def_struct(self):
        self.assertIn("SmartObjectDef", _read("SmartObjectTool"))

    def test_create_smart_object_method(self):
        self.assertIn("CreateSmartObject", _read("SmartObjectTool"))

    def test_export_smart_objects_method(self):
        self.assertIn("ExportSmartObjects", _read("SmartObjectTool"))


class TestZoneGraphToolDetail(unittest.TestCase):
    def test_zone_lane_type_enum(self):
        self.assertIn("ZoneLaneType", _read("ZoneGraphTool"))

    def test_zone_def_struct(self):
        self.assertIn("ZoneDef", _read("ZoneGraphTool"))

    def test_create_zone_method(self):
        self.assertIn("CreateZone", _read("ZoneGraphTool"))

    def test_export_zone_graph_method(self):
        self.assertIn("ExportZoneGraph", _read("ZoneGraphTool"))


class TestMassEntityToolDetail(unittest.TestCase):
    def test_mass_fragment_access_enum(self):
        self.assertIn("MassFragmentAccess", _read("MassEntityTool"))

    def test_mass_archetype_def_struct(self):
        self.assertIn("MassArchetypeDef", _read("MassEntityTool"))

    def test_create_archetype_method(self):
        self.assertIn("CreateArchetype", _read("MassEntityTool"))

    def test_export_archetype_method(self):
        self.assertIn("ExportArchetype", _read("MassEntityTool"))


class TestGameplayAbilityToolDetail(unittest.TestCase):
    def test_ability_activation_policy_enum(self):
        self.assertIn("AbilityActivationPolicy", _read("GameplayAbilityTool"))

    def test_gameplay_ability_def_struct(self):
        self.assertIn("GameplayAbilityDef", _read("GameplayAbilityTool"))

    def test_create_ability_method(self):
        self.assertIn("CreateAbility", _read("GameplayAbilityTool"))

    def test_export_ability_set_method(self):
        self.assertIn("ExportAbilitySet", _read("GameplayAbilityTool"))


class TestEnvironmentQueryToolDetail(unittest.TestCase):
    def test_eqs_generator_type_enum(self):
        self.assertIn("EQSGeneratorType", _read("EnvironmentQueryTool"))

    def test_eqs_query_def_struct(self):
        self.assertIn("EQSQueryDef", _read("EnvironmentQueryTool"))

    def test_create_query_method(self):
        self.assertIn("CreateQuery", _read("EnvironmentQueryTool"))

    def test_export_query_method(self):
        self.assertIn("ExportQuery", _read("EnvironmentQueryTool"))


if __name__ == "__main__":
    unittest.main()
