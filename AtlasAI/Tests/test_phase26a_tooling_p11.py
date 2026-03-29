"""Phase 26A — Tests for P11 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P11_TOOLS = [
    "GrassSimulationTool",
    "TerrainErosionTool",
    "DynamicRigidbodyTool",
    "LevelOfDetailAuthorTool",
    "PrefabSpawnerTool",
    "AIBehaviorTreeTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP11ToolsExist(unittest.TestCase):
    def test_grass_simulation_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "GrassSimulationTool.h").exists())

    def test_terrain_erosion_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "TerrainErosionTool.h").exists())

    def test_dynamic_rigidbody_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "DynamicRigidbodyTool.h").exists())

    def test_level_of_detail_author_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "LevelOfDetailAuthorTool.h").exists())

    def test_prefab_spawner_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "PrefabSpawnerTool.h").exists())

    def test_ai_behavior_tree_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AIBehaviorTreeTool.h").exists())


class TestP11PragmaOnce(unittest.TestCase):
    def test_grass_simulation_pragma_once(self):
        self.assertIn("#pragma once", _read("GrassSimulationTool"))

    def test_terrain_erosion_pragma_once(self):
        self.assertIn("#pragma once", _read("TerrainErosionTool"))

    def test_dynamic_rigidbody_pragma_once(self):
        self.assertIn("#pragma once", _read("DynamicRigidbodyTool"))

    def test_level_of_detail_author_pragma_once(self):
        self.assertIn("#pragma once", _read("LevelOfDetailAuthorTool"))

    def test_prefab_spawner_pragma_once(self):
        self.assertIn("#pragma once", _read("PrefabSpawnerTool"))

    def test_ai_behavior_tree_pragma_once(self):
        self.assertIn("#pragma once", _read("AIBehaviorTreeTool"))


class TestP11Inheritance(unittest.TestCase):
    def test_grass_simulation_inherits_itool(self):
        self.assertIn("ITool", _read("GrassSimulationTool"))

    def test_terrain_erosion_inherits_itool(self):
        self.assertIn("ITool", _read("TerrainErosionTool"))

    def test_dynamic_rigidbody_inherits_itool(self):
        self.assertIn("ITool", _read("DynamicRigidbodyTool"))

    def test_level_of_detail_author_inherits_itool(self):
        self.assertIn("ITool", _read("LevelOfDetailAuthorTool"))

    def test_prefab_spawner_inherits_itool(self):
        self.assertIn("ITool", _read("PrefabSpawnerTool"))

    def test_ai_behavior_tree_inherits_itool(self):
        self.assertIn("ITool", _read("AIBehaviorTreeTool"))


class TestP11GetToolName(unittest.TestCase):
    def test_grass_simulation_get_tool_name(self):
        self.assertIn('"GrassSimulationTool"', _read("GrassSimulationTool"))

    def test_terrain_erosion_get_tool_name(self):
        self.assertIn('"TerrainErosionTool"', _read("TerrainErosionTool"))

    def test_dynamic_rigidbody_get_tool_name(self):
        self.assertIn('"DynamicRigidbodyTool"', _read("DynamicRigidbodyTool"))

    def test_level_of_detail_author_get_tool_name(self):
        self.assertIn('"LevelOfDetailAuthorTool"', _read("LevelOfDetailAuthorTool"))

    def test_prefab_spawner_get_tool_name(self):
        self.assertIn('"PrefabSpawnerTool"', _read("PrefabSpawnerTool"))

    def test_ai_behavior_tree_get_tool_name(self):
        self.assertIn('"AIBehaviorTreeTool"', _read("AIBehaviorTreeTool"))


class TestP11Namespace(unittest.TestCase):
    def test_grass_simulation_namespace(self):
        self.assertIn("Atlas::Editor", _read("GrassSimulationTool"))

    def test_terrain_erosion_namespace(self):
        self.assertIn("Atlas::Editor", _read("TerrainErosionTool"))

    def test_dynamic_rigidbody_namespace(self):
        self.assertIn("Atlas::Editor", _read("DynamicRigidbodyTool"))

    def test_level_of_detail_author_namespace(self):
        self.assertIn("Atlas::Editor", _read("LevelOfDetailAuthorTool"))

    def test_prefab_spawner_namespace(self):
        self.assertIn("Atlas::Editor", _read("PrefabSpawnerTool"))

    def test_ai_behavior_tree_namespace(self):
        self.assertIn("Atlas::Editor", _read("AIBehaviorTreeTool"))


class TestP11SpecializedAPI(unittest.TestCase):
    # GrassSimulationTool
    def test_grass_type_enum(self):
        self.assertIn("GrassType", _read("GrassSimulationTool"))

    def test_wind_model_enum(self):
        self.assertIn("WindModel", _read("GrassSimulationTool"))

    def test_culling_mode_enum(self):
        self.assertIn("CullingMode", _read("GrassSimulationTool"))

    def test_density_mode_enum(self):
        self.assertIn("DensityMode", _read("GrassSimulationTool"))

    def test_grass_create_layer(self):
        self.assertIn("CreateLayer", _read("GrassSimulationTool"))

    def test_grass_set_density(self):
        self.assertIn("SetDensity", _read("GrassSimulationTool"))

    def test_grass_set_wind_speed(self):
        self.assertIn("SetWindSpeed", _read("GrassSimulationTool"))

    def test_grass_blade_settings_struct(self):
        self.assertIn("GrassBladeSettings", _read("GrassSimulationTool"))

    def test_grass_wind_settings_struct(self):
        self.assertIn("WindSettings", _read("GrassSimulationTool"))

    def test_grass_pause_simulation(self):
        self.assertIn("PauseSimulation", _read("GrassSimulationTool"))

    def test_grass_set_max_render_distance(self):
        self.assertIn("SetMaxRenderDistance", _read("GrassSimulationTool"))

    # TerrainErosionTool
    def test_erosion_type_enum(self):
        self.assertIn("ErosionType", _read("TerrainErosionTool"))

    def test_erosion_quality_enum(self):
        self.assertIn("ErosionQuality", _read("TerrainErosionTool"))

    def test_sediment_mode_enum(self):
        self.assertIn("SedimentMode", _read("TerrainErosionTool"))

    def test_erosion_create_layer(self):
        self.assertIn("CreateLayer", _read("TerrainErosionTool"))

    def test_erosion_set_brush_radius(self):
        self.assertIn("SetBrushRadius", _read("TerrainErosionTool"))

    def test_erosion_hydraulic_params_struct(self):
        self.assertIn("HydraulicParams", _read("TerrainErosionTool"))

    def test_erosion_thermal_params_struct(self):
        self.assertIn("ThermalParams", _read("TerrainErosionTool"))

    def test_erosion_wind_params_struct(self):
        self.assertIn("WindParams", _read("TerrainErosionTool"))

    def test_erosion_bake_layer(self):
        self.assertIn("BakeLayer", _read("TerrainErosionTool"))

    def test_erosion_set_rain_amount(self):
        self.assertIn("SetRainAmount", _read("TerrainErosionTool"))

    # DynamicRigidbodyTool
    def test_body_type_enum(self):
        self.assertIn("BodyType", _read("DynamicRigidbodyTool"))

    def test_collider_shape_enum(self):
        self.assertIn("ColliderShape", _read("DynamicRigidbodyTool"))

    def test_constraint_type_enum(self):
        self.assertIn("ConstraintType", _read("DynamicRigidbodyTool"))

    def test_interpolation_mode_enum(self):
        self.assertIn("InterpolationMode", _read("DynamicRigidbodyTool"))

    def test_rigidbody_create_body(self):
        self.assertIn("CreateBody", _read("DynamicRigidbodyTool"))

    def test_rigidbody_add_collider(self):
        self.assertIn("AddCollider", _read("DynamicRigidbodyTool"))

    def test_rigidbody_add_constraint(self):
        self.assertIn("AddConstraint", _read("DynamicRigidbodyTool"))

    def test_physics_material_struct(self):
        self.assertIn("PhysicsMaterial", _read("DynamicRigidbodyTool"))

    def test_rigidbody_record_struct(self):
        self.assertIn("RigidbodyRecord", _read("DynamicRigidbodyTool"))

    def test_rigidbody_set_mass(self):
        self.assertIn("SetMass", _read("DynamicRigidbodyTool"))

    def test_rigidbody_set_freeze_position(self):
        self.assertIn("SetFreezePosition", _read("DynamicRigidbodyTool"))

    def test_rigidbody_set_constraint_limits(self):
        self.assertIn("SetConstraintLimits", _read("DynamicRigidbodyTool"))

    # LevelOfDetailAuthorTool
    def test_lod_transition_mode_enum(self):
        self.assertIn("LODTransitionMode", _read("LevelOfDetailAuthorTool"))

    def test_lod_normal_mode_enum(self):
        self.assertIn("NormalMode", _read("LevelOfDetailAuthorTool"))

    def test_lod_simplification_algorithm_enum(self):
        self.assertIn("SimplificationAlgorithm", _read("LevelOfDetailAuthorTool"))

    def test_lod_create_group(self):
        self.assertIn("CreateGroup", _read("LevelOfDetailAuthorTool"))

    def test_lod_add_variant(self):
        self.assertIn("AddVariant", _read("LevelOfDetailAuthorTool"))

    def test_lod_group_struct(self):
        self.assertIn("LODGroup", _read("LevelOfDetailAuthorTool"))

    def test_lod_mesh_variant_struct(self):
        self.assertIn("LODMeshVariant", _read("LevelOfDetailAuthorTool"))

    def test_lod_auto_generate(self):
        self.assertIn("AutoGenerateLODs", _read("LevelOfDetailAuthorTool"))

    def test_lod_preview_at_lod_level(self):
        self.assertIn("PreviewAtLODLevel", _read("LevelOfDetailAuthorTool"))

    def test_lod_set_algorithm(self):
        self.assertIn("SetAlgorithm", _read("LevelOfDetailAuthorTool"))

    # PrefabSpawnerTool
    def test_spawn_trigger_enum(self):
        self.assertIn("SpawnTrigger", _read("PrefabSpawnerTool"))

    def test_spawn_shape_enum(self):
        self.assertIn("SpawnShape", _read("PrefabSpawnerTool"))

    def test_despawn_condition_enum(self):
        self.assertIn("DespawnCondition", _read("PrefabSpawnerTool"))

    def test_pool_strategy_enum(self):
        self.assertIn("PoolStrategy", _read("PrefabSpawnerTool"))

    def test_spawner_create_pool(self):
        self.assertIn("CreatePool", _read("PrefabSpawnerTool"))

    def test_spawner_create_rule(self):
        self.assertIn("CreateRule", _read("PrefabSpawnerTool"))

    def test_spawn_pool_struct(self):
        self.assertIn("SpawnPool", _read("PrefabSpawnerTool"))

    def test_spawner_rule_struct(self):
        self.assertIn("SpawnerRule", _read("PrefabSpawnerTool"))

    def test_spawner_set_timer_interval(self):
        self.assertIn("SetTimerInterval", _read("PrefabSpawnerTool"))

    def test_spawner_trigger_spawn(self):
        self.assertIn("TriggerSpawn", _read("PrefabSpawnerTool"))

    def test_spawner_set_despawn_lifetime(self):
        self.assertIn("SetDespawnLifetime", _read("PrefabSpawnerTool"))

    # AIBehaviorTreeTool
    def test_bt_node_type_enum(self):
        self.assertIn("NodeType", _read("AIBehaviorTreeTool"))

    def test_bt_decorator_type_enum(self):
        self.assertIn("DecoratorType", _read("AIBehaviorTreeTool"))

    def test_bt_parallel_policy_enum(self):
        self.assertIn("ParallelPolicy", _read("AIBehaviorTreeTool"))

    def test_bt_blackboard_op_enum(self):
        self.assertIn("BlackboardOp", _read("AIBehaviorTreeTool"))

    def test_bt_node_status_enum(self):
        self.assertIn("NodeStatus", _read("AIBehaviorTreeTool"))

    def test_bt_create_tree(self):
        self.assertIn("CreateTree", _read("AIBehaviorTreeTool"))

    def test_bt_add_node(self):
        self.assertIn("AddNode", _read("AIBehaviorTreeTool"))

    def test_bt_behavior_tree_struct(self):
        self.assertIn("BehaviorTree", _read("AIBehaviorTreeTool"))

    def test_bt_behavior_node_struct(self):
        self.assertIn("BehaviorNode", _read("AIBehaviorTreeTool"))

    def test_bt_blackboard_entry_struct(self):
        self.assertIn("BlackboardEntry", _read("AIBehaviorTreeTool"))

    def test_bt_set_root_node(self):
        self.assertIn("SetRootNode", _read("AIBehaviorTreeTool"))

    def test_bt_add_blackboard_entry(self):
        self.assertIn("AddBlackboardEntry", _read("AIBehaviorTreeTool"))

    def test_bt_duplicate_tree(self):
        self.assertIn("DuplicateTree", _read("AIBehaviorTreeTool"))


if __name__ == "__main__":
    unittest.main()
