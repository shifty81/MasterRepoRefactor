"""Phase 19A — Tests for P4 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P4_TOOLS = [
    "TerrainSculptTool",
    "BiomePainterTool",
    "ObjectScatterTool",
    "WaypointEditorTool",
    "AudioZoneTool",
    "CinematicSequencerTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP4ToolsExist(unittest.TestCase):
    def test_terrain_sculpt_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "TerrainSculptTool.h").exists())

    def test_biome_painter_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "BiomePainterTool.h").exists())

    def test_object_scatter_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ObjectScatterTool.h").exists())

    def test_waypoint_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "WaypointEditorTool.h").exists())

    def test_audio_zone_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AudioZoneTool.h").exists())

    def test_cinematic_sequencer_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "CinematicSequencerTool.h").exists())

    def test_itool_h_present(self):
        self.assertTrue((TOOL_LAYER / "ITool.h").exists())


class TestP4PragmaOnce(unittest.TestCase):
    def test_terrain_sculpt_pragma_once(self):
        self.assertIn("#pragma once", _read("TerrainSculptTool"))

    def test_biome_painter_pragma_once(self):
        self.assertIn("#pragma once", _read("BiomePainterTool"))

    def test_object_scatter_pragma_once(self):
        self.assertIn("#pragma once", _read("ObjectScatterTool"))

    def test_waypoint_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("WaypointEditorTool"))

    def test_audio_zone_pragma_once(self):
        self.assertIn("#pragma once", _read("AudioZoneTool"))

    def test_cinematic_sequencer_pragma_once(self):
        self.assertIn("#pragma once", _read("CinematicSequencerTool"))


class TestP4Inheritance(unittest.TestCase):
    def test_terrain_sculpt_inherits_itool(self):
        self.assertIn("ITool", _read("TerrainSculptTool"))

    def test_biome_painter_inherits_itool(self):
        self.assertIn("ITool", _read("BiomePainterTool"))

    def test_object_scatter_inherits_itool(self):
        self.assertIn("ITool", _read("ObjectScatterTool"))

    def test_waypoint_editor_inherits_itool(self):
        self.assertIn("ITool", _read("WaypointEditorTool"))

    def test_audio_zone_inherits_itool(self):
        self.assertIn("ITool", _read("AudioZoneTool"))

    def test_cinematic_sequencer_inherits_itool(self):
        self.assertIn("ITool", _read("CinematicSequencerTool"))


class TestP4GetToolName(unittest.TestCase):
    def test_terrain_sculpt_get_tool_name(self):
        self.assertIn("GetToolName", _read("TerrainSculptTool"))

    def test_biome_painter_get_tool_name(self):
        self.assertIn("GetToolName", _read("BiomePainterTool"))

    def test_object_scatter_get_tool_name(self):
        self.assertIn("GetToolName", _read("ObjectScatterTool"))

    def test_waypoint_editor_get_tool_name(self):
        self.assertIn("GetToolName", _read("WaypointEditorTool"))

    def test_audio_zone_get_tool_name(self):
        self.assertIn("GetToolName", _read("AudioZoneTool"))

    def test_cinematic_sequencer_get_tool_name(self):
        self.assertIn("GetToolName", _read("CinematicSequencerTool"))


class TestP4ToolNameStrings(unittest.TestCase):
    def test_terrain_sculpt_tool_name_string(self):
        self.assertIn('"TerrainSculptTool"', _read("TerrainSculptTool"))

    def test_biome_painter_tool_name_string(self):
        self.assertIn('"BiomePainterTool"', _read("BiomePainterTool"))

    def test_object_scatter_tool_name_string(self):
        self.assertIn('"ObjectScatterTool"', _read("ObjectScatterTool"))

    def test_waypoint_editor_tool_name_string(self):
        self.assertIn('"WaypointEditorTool"', _read("WaypointEditorTool"))

    def test_audio_zone_tool_name_string(self):
        self.assertIn('"AudioZoneTool"', _read("AudioZoneTool"))

    def test_cinematic_sequencer_tool_name_string(self):
        self.assertIn('"CinematicSequencerTool"', _read("CinematicSequencerTool"))


class TestP4SpecializedAPI(unittest.TestCase):
    """Each P4 tool exposes its primary domain API."""

    def test_terrain_sculpt_has_apply_brush(self):
        self.assertIn("ApplyBrush", _read("TerrainSculptTool"))

    def test_terrain_sculpt_has_brush_mode_enum(self):
        self.assertIn("BrushMode", _read("TerrainSculptTool"))

    def test_biome_painter_has_register_biome(self):
        self.assertIn("RegisterBiome", _read("BiomePainterTool"))

    def test_biome_painter_has_paint_at(self):
        self.assertIn("PaintAt", _read("BiomePainterTool"))

    def test_object_scatter_has_scatter_params(self):
        self.assertIn("ScatterParams", _read("ObjectScatterTool"))

    def test_object_scatter_has_scatter_at(self):
        self.assertIn("ScatterAt", _read("ObjectScatterTool"))

    def test_waypoint_editor_has_add_waypoint(self):
        self.assertIn("AddWaypoint", _read("WaypointEditorTool"))

    def test_waypoint_editor_has_chain_waypoints(self):
        self.assertIn("ChainWaypoints", _read("WaypointEditorTool"))

    def test_audio_zone_has_create_zone(self):
        self.assertIn("CreateZone", _read("AudioZoneTool"))

    def test_audio_zone_has_get_zones(self):
        self.assertIn("GetZones", _read("AudioZoneTool"))

    def test_cinematic_sequencer_has_create_track(self):
        self.assertIn("CreateTrack", _read("CinematicSequencerTool"))

    def test_cinematic_sequencer_has_keyframe(self):
        self.assertIn("Keyframe", _read("CinematicSequencerTool"))

    def test_cinematic_sequencer_has_play(self):
        self.assertIn("Play", _read("CinematicSequencerTool"))


class TestP4NamespaceAtlasEditor(unittest.TestCase):
    def test_terrain_sculpt_namespace(self):
        self.assertIn("Atlas::Editor", _read("TerrainSculptTool"))

    def test_biome_painter_namespace(self):
        self.assertIn("Atlas::Editor", _read("BiomePainterTool"))

    def test_object_scatter_namespace(self):
        self.assertIn("Atlas::Editor", _read("ObjectScatterTool"))

    def test_waypoint_editor_namespace(self):
        self.assertIn("Atlas::Editor", _read("WaypointEditorTool"))

    def test_audio_zone_namespace(self):
        self.assertIn("Atlas::Editor", _read("AudioZoneTool"))

    def test_cinematic_sequencer_namespace(self):
        self.assertIn("Atlas::Editor", _read("CinematicSequencerTool"))


if __name__ == "__main__":
    unittest.main()
