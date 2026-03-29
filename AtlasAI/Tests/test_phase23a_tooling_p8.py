"""Phase 23A — Tests for P8 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P8_TOOLS = [
    "ShaderGraphEditorTool",
    "VoxelTerrainTool",
    "MaterialBlendTool",
    "WeatherSystemTool",
    "RopeSimulationTool",
    "ConstraintEditorTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP8ToolsExist(unittest.TestCase):
    def test_shader_graph_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ShaderGraphEditorTool.h").exists())

    def test_voxel_terrain_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "VoxelTerrainTool.h").exists())

    def test_material_blend_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MaterialBlendTool.h").exists())

    def test_weather_system_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "WeatherSystemTool.h").exists())

    def test_rope_simulation_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "RopeSimulationTool.h").exists())

    def test_constraint_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ConstraintEditorTool.h").exists())


class TestP8PragmaOnce(unittest.TestCase):
    def test_shader_graph_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("ShaderGraphEditorTool"))

    def test_voxel_terrain_pragma_once(self):
        self.assertIn("#pragma once", _read("VoxelTerrainTool"))

    def test_material_blend_pragma_once(self):
        self.assertIn("#pragma once", _read("MaterialBlendTool"))

    def test_weather_system_pragma_once(self):
        self.assertIn("#pragma once", _read("WeatherSystemTool"))

    def test_rope_simulation_pragma_once(self):
        self.assertIn("#pragma once", _read("RopeSimulationTool"))

    def test_constraint_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("ConstraintEditorTool"))


class TestP8Inheritance(unittest.TestCase):
    def test_shader_graph_editor_inherits_itool(self):
        self.assertIn("ITool", _read("ShaderGraphEditorTool"))

    def test_voxel_terrain_inherits_itool(self):
        self.assertIn("ITool", _read("VoxelTerrainTool"))

    def test_material_blend_inherits_itool(self):
        self.assertIn("ITool", _read("MaterialBlendTool"))

    def test_weather_system_inherits_itool(self):
        self.assertIn("ITool", _read("WeatherSystemTool"))

    def test_rope_simulation_inherits_itool(self):
        self.assertIn("ITool", _read("RopeSimulationTool"))

    def test_constraint_editor_inherits_itool(self):
        self.assertIn("ITool", _read("ConstraintEditorTool"))


class TestP8GetToolName(unittest.TestCase):
    def test_shader_graph_editor_get_tool_name(self):
        self.assertIn('"ShaderGraphEditorTool"', _read("ShaderGraphEditorTool"))

    def test_voxel_terrain_get_tool_name(self):
        self.assertIn('"VoxelTerrainTool"', _read("VoxelTerrainTool"))

    def test_material_blend_get_tool_name(self):
        self.assertIn('"MaterialBlendTool"', _read("MaterialBlendTool"))

    def test_weather_system_get_tool_name(self):
        self.assertIn('"WeatherSystemTool"', _read("WeatherSystemTool"))

    def test_rope_simulation_get_tool_name(self):
        self.assertIn('"RopeSimulationTool"', _read("RopeSimulationTool"))

    def test_constraint_editor_get_tool_name(self):
        self.assertIn('"ConstraintEditorTool"', _read("ConstraintEditorTool"))


class TestP8Namespace(unittest.TestCase):
    def test_shader_graph_editor_namespace(self):
        self.assertIn("Atlas::Editor", _read("ShaderGraphEditorTool"))

    def test_voxel_terrain_namespace(self):
        self.assertIn("Atlas::Editor", _read("VoxelTerrainTool"))

    def test_material_blend_namespace(self):
        self.assertIn("Atlas::Editor", _read("MaterialBlendTool"))

    def test_weather_system_namespace(self):
        self.assertIn("Atlas::Editor", _read("WeatherSystemTool"))

    def test_rope_simulation_namespace(self):
        self.assertIn("Atlas::Editor", _read("RopeSimulationTool"))

    def test_constraint_editor_namespace(self):
        self.assertIn("Atlas::Editor", _read("ConstraintEditorTool"))


class TestP8SpecializedAPI(unittest.TestCase):
    # ShaderGraphEditorTool
    def test_shader_graph_create_graph(self):
        self.assertIn("CreateGraph", _read("ShaderGraphEditorTool"))

    def test_shader_graph_add_node(self):
        self.assertIn("AddNode", _read("ShaderGraphEditorTool"))

    def test_shader_graph_connect_nodes(self):
        self.assertIn("ConnectNodes", _read("ShaderGraphEditorTool"))

    def test_shader_graph_node_type_enum(self):
        self.assertIn("NodeType", _read("ShaderGraphEditorTool"))

    def test_shader_graph_compile_graph(self):
        self.assertIn("CompileGraph", _read("ShaderGraphEditorTool"))

    def test_shader_graph_shader_node_struct(self):
        self.assertIn("ShaderNode", _read("ShaderGraphEditorTool"))

    # VoxelTerrainTool
    def test_voxel_terrain_create_chunk(self):
        self.assertIn("CreateChunk", _read("VoxelTerrainTool"))

    def test_voxel_terrain_sculpt_at(self):
        self.assertIn("SculptAt", _read("VoxelTerrainTool"))

    def test_voxel_terrain_brush_mode_enum(self):
        self.assertIn("BrushMode", _read("VoxelTerrainTool"))

    def test_voxel_terrain_generate_chunk_noise(self):
        self.assertIn("GenerateChunkNoise", _read("VoxelTerrainTool"))

    def test_voxel_terrain_terrain_chunk_struct(self):
        self.assertIn("TerrainChunk", _read("VoxelTerrainTool"))

    def test_voxel_terrain_smooth_region(self):
        self.assertIn("SmoothRegion", _read("VoxelTerrainTool"))

    # MaterialBlendTool
    def test_material_blend_add_layer(self):
        self.assertIn("AddLayer", _read("MaterialBlendTool"))

    def test_material_blend_blend_mode_enum(self):
        self.assertIn("BlendMode", _read("MaterialBlendTool"))

    def test_material_blend_set_layer_weight(self):
        self.assertIn("SetLayerWeight", _read("MaterialBlendTool"))

    def test_material_blend_add_mask(self):
        self.assertIn("AddMask", _read("MaterialBlendTool"))

    def test_material_blend_blend_layer_struct(self):
        self.assertIn("BlendLayer", _read("MaterialBlendTool"))

    def test_material_blend_bake_blend_map(self):
        self.assertIn("BakeBlendMap", _read("MaterialBlendTool"))

    # WeatherSystemTool
    def test_weather_system_create_weather_state(self):
        self.assertIn("CreateWeatherState", _read("WeatherSystemTool"))

    def test_weather_system_weather_type_enum(self):
        self.assertIn("WeatherType", _read("WeatherSystemTool"))

    def test_weather_system_add_transition(self):
        self.assertIn("AddTransition", _read("WeatherSystemTool"))

    def test_weather_system_set_active_state(self):
        self.assertIn("SetActiveState", _read("WeatherSystemTool"))

    def test_weather_system_weather_state_struct(self):
        self.assertIn("WeatherState", _read("WeatherSystemTool"))

    def test_weather_system_set_fog_density(self):
        self.assertIn("SetFogDensity", _read("WeatherSystemTool"))

    # RopeSimulationTool
    def test_rope_simulation_create_rope(self):
        self.assertIn("CreateRope", _read("RopeSimulationTool"))

    def test_rope_simulation_rope_type_enum(self):
        self.assertIn("RopeType", _read("RopeSimulationTool"))

    def test_rope_simulation_add_anchor(self):
        self.assertIn("AddAnchor", _read("RopeSimulationTool"))

    def test_rope_simulation_simulate_rope(self):
        self.assertIn("SimulateRope", _read("RopeSimulationTool"))

    def test_rope_simulation_rope_definition_struct(self):
        self.assertIn("RopeDefinition", _read("RopeSimulationTool"))

    def test_rope_simulation_set_rope_stiffness(self):
        self.assertIn("SetRopeStiffness", _read("RopeSimulationTool"))

    # ConstraintEditorTool
    def test_constraint_editor_create_constraint(self):
        self.assertIn("CreateConstraint", _read("ConstraintEditorTool"))

    def test_constraint_editor_constraint_type_enum(self):
        self.assertIn("ConstraintType", _read("ConstraintEditorTool"))

    def test_constraint_editor_set_angular_limit(self):
        self.assertIn("SetAngularLimit", _read("ConstraintEditorTool"))

    def test_constraint_editor_set_angular_drive(self):
        self.assertIn("SetAngularDrive", _read("ConstraintEditorTool"))

    def test_constraint_editor_constraint_definition_struct(self):
        self.assertIn("ConstraintDefinition", _read("ConstraintEditorTool"))

    def test_constraint_editor_get_constraints_for_entity(self):
        self.assertIn("GetConstraintsForEntity", _read("ConstraintEditorTool"))


if __name__ == "__main__":
    unittest.main()
