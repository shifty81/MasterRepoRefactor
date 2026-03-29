"""Phase 20A — Tests for P5 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P5_TOOLS = [
    "ProceduralPlacementTool",
    "EnvironmentProbesTool",
    "ClimateZoneTool",
    "NavMeshEditorTool",
    "DecalPainterTool",
    "TriggerVolumeTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP5ToolsExist(unittest.TestCase):
    def test_procedural_placement_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ProceduralPlacementTool.h").exists())

    def test_environment_probes_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "EnvironmentProbesTool.h").exists())

    def test_climate_zone_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ClimateZoneTool.h").exists())

    def test_nav_mesh_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "NavMeshEditorTool.h").exists())

    def test_decal_painter_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "DecalPainterTool.h").exists())

    def test_trigger_volume_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "TriggerVolumeTool.h").exists())

    def test_itool_h_present(self):
        self.assertTrue((TOOL_LAYER / "ITool.h").exists())


class TestP5PragmaOnce(unittest.TestCase):
    def test_procedural_placement_pragma_once(self):
        self.assertIn("#pragma once", _read("ProceduralPlacementTool"))

    def test_environment_probes_pragma_once(self):
        self.assertIn("#pragma once", _read("EnvironmentProbesTool"))

    def test_climate_zone_pragma_once(self):
        self.assertIn("#pragma once", _read("ClimateZoneTool"))

    def test_nav_mesh_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("NavMeshEditorTool"))

    def test_decal_painter_pragma_once(self):
        self.assertIn("#pragma once", _read("DecalPainterTool"))

    def test_trigger_volume_pragma_once(self):
        self.assertIn("#pragma once", _read("TriggerVolumeTool"))


class TestP5Inheritance(unittest.TestCase):
    def test_procedural_placement_inherits_itool(self):
        self.assertIn("ITool", _read("ProceduralPlacementTool"))

    def test_environment_probes_inherits_itool(self):
        self.assertIn("ITool", _read("EnvironmentProbesTool"))

    def test_climate_zone_inherits_itool(self):
        self.assertIn("ITool", _read("ClimateZoneTool"))

    def test_nav_mesh_editor_inherits_itool(self):
        self.assertIn("ITool", _read("NavMeshEditorTool"))

    def test_decal_painter_inherits_itool(self):
        self.assertIn("ITool", _read("DecalPainterTool"))

    def test_trigger_volume_inherits_itool(self):
        self.assertIn("ITool", _read("TriggerVolumeTool"))


class TestP5GetToolName(unittest.TestCase):
    def test_procedural_placement_get_tool_name(self):
        self.assertIn("GetToolName", _read("ProceduralPlacementTool"))

    def test_environment_probes_get_tool_name(self):
        self.assertIn("GetToolName", _read("EnvironmentProbesTool"))

    def test_climate_zone_get_tool_name(self):
        self.assertIn("GetToolName", _read("ClimateZoneTool"))

    def test_nav_mesh_editor_get_tool_name(self):
        self.assertIn("GetToolName", _read("NavMeshEditorTool"))

    def test_decal_painter_get_tool_name(self):
        self.assertIn("GetToolName", _read("DecalPainterTool"))

    def test_trigger_volume_get_tool_name(self):
        self.assertIn("GetToolName", _read("TriggerVolumeTool"))


class TestP5ToolNameStrings(unittest.TestCase):
    def test_procedural_placement_name_string(self):
        self.assertIn('"ProceduralPlacementTool"', _read("ProceduralPlacementTool"))

    def test_environment_probes_name_string(self):
        self.assertIn('"EnvironmentProbesTool"', _read("EnvironmentProbesTool"))

    def test_climate_zone_name_string(self):
        self.assertIn('"ClimateZoneTool"', _read("ClimateZoneTool"))

    def test_nav_mesh_editor_name_string(self):
        self.assertIn('"NavMeshEditorTool"', _read("NavMeshEditorTool"))

    def test_decal_painter_name_string(self):
        self.assertIn('"DecalPainterTool"', _read("DecalPainterTool"))

    def test_trigger_volume_name_string(self):
        self.assertIn('"TriggerVolumeTool"', _read("TriggerVolumeTool"))


class TestP5SpecializedAPI(unittest.TestCase):
    """Each P5 tool exposes its primary domain API."""

    def test_procedural_placement_has_add_rule(self):
        self.assertIn("AddRule", _read("ProceduralPlacementTool"))

    def test_procedural_placement_has_run_placement(self):
        self.assertIn("RunPlacement", _read("ProceduralPlacementTool"))

    def test_procedural_placement_has_placement_rule_struct(self):
        self.assertIn("PlacementRule", _read("ProceduralPlacementTool"))

    def test_environment_probes_has_add_probe(self):
        self.assertIn("AddProbe", _read("EnvironmentProbesTool"))

    def test_environment_probes_has_bake_probe(self):
        self.assertIn("BakeProbe", _read("EnvironmentProbesTool"))

    def test_environment_probes_has_probe_type_enum(self):
        self.assertIn("ProbeType", _read("EnvironmentProbesTool"))

    def test_climate_zone_has_create_zone(self):
        self.assertIn("CreateZone", _read("ClimateZoneTool"))

    def test_climate_zone_has_set_weather_preset(self):
        self.assertIn("SetWeatherPreset", _read("ClimateZoneTool"))

    def test_climate_zone_has_register_climate_preset(self):
        self.assertIn("RegisterClimatePreset", _read("ClimateZoneTool"))

    def test_nav_mesh_editor_has_bake_nav_mesh(self):
        self.assertIn("BakeNavMesh", _read("NavMeshEditorTool"))

    def test_nav_mesh_editor_has_off_mesh_link(self):
        self.assertIn("OffMeshLink", _read("NavMeshEditorTool"))

    def test_nav_mesh_editor_has_exclusion_zone(self):
        self.assertIn("ExclusionZone", _read("NavMeshEditorTool"))

    def test_decal_painter_has_place_decal(self):
        self.assertIn("PlaceDecal", _read("DecalPainterTool"))

    def test_decal_painter_has_set_active_material(self):
        self.assertIn("SetActiveMaterial", _read("DecalPainterTool"))

    def test_trigger_volume_has_create_volume(self):
        self.assertIn("CreateVolume", _read("TriggerVolumeTool"))

    def test_trigger_volume_has_trigger_shape_enum(self):
        self.assertIn("TriggerShape", _read("TriggerVolumeTool"))

    def test_trigger_volume_has_bind_event(self):
        self.assertIn("BindEvent", _read("TriggerVolumeTool"))


class TestP5NamespaceAtlasEditor(unittest.TestCase):
    def test_procedural_placement_namespace(self):
        self.assertIn("Atlas::Editor", _read("ProceduralPlacementTool"))

    def test_environment_probes_namespace(self):
        self.assertIn("Atlas::Editor", _read("EnvironmentProbesTool"))

    def test_climate_zone_namespace(self):
        self.assertIn("Atlas::Editor", _read("ClimateZoneTool"))

    def test_nav_mesh_editor_namespace(self):
        self.assertIn("Atlas::Editor", _read("NavMeshEditorTool"))

    def test_decal_painter_namespace(self):
        self.assertIn("Atlas::Editor", _read("DecalPainterTool"))

    def test_trigger_volume_namespace(self):
        self.assertIn("Atlas::Editor", _read("TriggerVolumeTool"))


if __name__ == "__main__":
    unittest.main()
