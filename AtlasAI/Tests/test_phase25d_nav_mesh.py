"""Phase 25D — Tests for NavMeshRegistry.h and NavMeshLoader."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    NavMeshLoader,
    NavMeshManifest,
    NavMeshAABB,
    NavMeshNode,
    NavMeshEdge,
)

TMP_DIR = Path("/tmp/test_phase25d")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# NavMeshRegistry.h
# ---------------------------------------------------------------------------

def _read_registry() -> str:
    return (SCENE_DIR / "NavMeshRegistry.h").read_text()


class TestNavMeshRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "NavMeshRegistry.h").exists())


class TestNavMeshRegistryStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_registry())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_registry())

    def test_class_declaration(self):
        self.assertIn("NavMeshRegistry", _read_registry())

    def test_nav_mesh_state_enum(self):
        self.assertIn("NavMeshState", _read_registry())

    def test_nav_mesh_type_enum(self):
        self.assertIn("NavMeshType", _read_registry())

    def test_agent_type_enum(self):
        self.assertIn("AgentType", _read_registry())

    def test_nav_mesh_aabb_struct(self):
        self.assertIn("NavMeshAABB", _read_registry())

    def test_nav_mesh_link_struct(self):
        self.assertIn("NavMeshLink", _read_registry())

    def test_agent_capability_struct(self):
        self.assertIn("AgentCapability", _read_registry())

    def test_nav_mesh_record_struct(self):
        self.assertIn("NavMeshRecord", _read_registry())


class TestNavMeshRegistryAPI(unittest.TestCase):
    def test_register_nav_mesh(self):
        self.assertIn("RegisterNavMesh", _read_registry())

    def test_unregister_nav_mesh(self):
        self.assertIn("UnregisterNavMesh", _read_registry())

    def test_load_nav_mesh(self):
        self.assertIn("LoadNavMesh", _read_registry())

    def test_unload_nav_mesh(self):
        self.assertIn("UnloadNavMesh", _read_registry())

    def test_is_loaded(self):
        self.assertIn("IsLoaded", _read_registry())

    def test_get_all_nav_mesh_ids(self):
        self.assertIn("GetAllNavMeshIds", _read_registry())

    def test_add_link(self):
        self.assertIn("AddLink", _read_registry())

    def test_remove_link(self):
        self.assertIn("RemoveLink", _read_registry())

    def test_add_neighbour(self):
        self.assertIn("AddNeighbour", _read_registry())

    def test_get_neighbours(self):
        self.assertIn("GetNeighbours", _read_registry())

    def test_add_agent_capability(self):
        self.assertIn("AddAgentCapability", _read_registry())

    def test_supports_agent(self):
        self.assertIn("SupportsAgent", _read_registry())

    def test_query_point(self):
        self.assertIn("QueryPoint", _read_registry())

    def test_query_path(self):
        self.assertIn("QueryPath", _read_registry())

    def test_find_nearest_mesh(self):
        self.assertIn("FindNearestMesh", _read_registry())

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_registry())

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_registry())

    def test_clear_method(self):
        self.assertIn("Clear", _read_registry())


# ---------------------------------------------------------------------------
# NavMeshAABB dataclass
# ---------------------------------------------------------------------------

class TestNavMeshAABBDataclass(unittest.TestCase):
    def test_default_values(self):
        b = NavMeshAABB()
        self.assertAlmostEqual(b.min_x, 0.0)
        self.assertAlmostEqual(b.max_x, 100.0)

    def test_custom_values(self):
        b = NavMeshAABB(0, 0, 0, 50, 10, 50)
        self.assertAlmostEqual(b.max_x, 50.0)

    def test_contains_point_inside(self):
        b = NavMeshAABB(0, 0, 0, 100, 100, 100)
        self.assertTrue(b.contains_point(50, 50, 50))

    def test_contains_point_outside(self):
        b = NavMeshAABB(0, 0, 0, 100, 100, 100)
        self.assertFalse(b.contains_point(200, 50, 50))

    def test_intersects_overlapping(self):
        a = NavMeshAABB(0, 0, 0, 100, 100, 100)
        b = NavMeshAABB(50, 50, 50, 150, 150, 150)
        self.assertTrue(a.intersects(b))

    def test_intersects_non_overlapping(self):
        a = NavMeshAABB(0, 0, 0, 50, 50, 50)
        b = NavMeshAABB(100, 100, 100, 200, 200, 200)
        self.assertFalse(a.intersects(b))

    def test_volume(self):
        b = NavMeshAABB(0, 0, 0, 10, 10, 10)
        self.assertAlmostEqual(b.volume, 1000.0)


# ---------------------------------------------------------------------------
# NavMeshNode dataclass
# ---------------------------------------------------------------------------

class TestNavMeshNodeDataclass(unittest.TestCase):
    def test_node_id_field(self):
        n = NavMeshNode("n001", "mesh001")
        self.assertEqual(n.node_id, "n001")

    def test_mesh_id_field(self):
        n = NavMeshNode("n001", "mesh001")
        self.assertEqual(n.mesh_id, "mesh001")

    def test_default_position(self):
        n = NavMeshNode("n001", "mesh001")
        self.assertAlmostEqual(n.pos_x, 0.0)
        self.assertAlmostEqual(n.pos_y, 0.0)
        self.assertAlmostEqual(n.pos_z, 0.0)

    def test_position_property(self):
        n = NavMeshNode("n001", "mesh001", pos_x=1.0, pos_y=2.0, pos_z=3.0)
        self.assertEqual(n.position, (1.0, 2.0, 3.0))

    def test_default_traversal_cost(self):
        n = NavMeshNode("n001", "mesh001")
        self.assertAlmostEqual(n.traversal_cost, 1.0)


# ---------------------------------------------------------------------------
# NavMeshEdge dataclass
# ---------------------------------------------------------------------------

class TestNavMeshEdgeDataclass(unittest.TestCase):
    def test_edge_id_field(self):
        e = NavMeshEdge("e001", "n001", "n002", "mesh001")
        self.assertEqual(e.edge_id, "e001")

    def test_from_node_field(self):
        e = NavMeshEdge("e001", "n001", "n002", "mesh001")
        self.assertEqual(e.from_node_id, "n001")

    def test_to_node_field(self):
        e = NavMeshEdge("e001", "n001", "n002", "mesh001")
        self.assertEqual(e.to_node_id, "n002")

    def test_default_cost(self):
        e = NavMeshEdge("e001", "n001", "n002", "mesh001")
        self.assertAlmostEqual(e.cost, 1.0)

    def test_default_bidirectional(self):
        e = NavMeshEdge("e001", "n001", "n002", "mesh001")
        self.assertTrue(e.bidirectional)


# ---------------------------------------------------------------------------
# NavMeshManifest dataclass
# ---------------------------------------------------------------------------

class TestNavMeshManifestDataclass(unittest.TestCase):
    def test_mesh_id_field(self):
        m = NavMeshManifest("m001", "Village Ground")
        self.assertEqual(m.mesh_id, "m001")

    def test_name_field(self):
        m = NavMeshManifest("m001", "Village Ground")
        self.assertEqual(m.name, "Village Ground")

    def test_default_mesh_type(self):
        m = NavMeshManifest("m001", "Village Ground")
        self.assertEqual(m.mesh_type, "Ground")

    def test_node_count_empty(self):
        m = NavMeshManifest("m001", "Village Ground")
        self.assertEqual(m.node_count, 0)

    def test_edge_count_empty(self):
        m = NavMeshManifest("m001", "Village Ground")
        self.assertEqual(m.edge_count, 0)

    def test_neighbour_count_empty(self):
        m = NavMeshManifest("m001", "Village Ground")
        self.assertEqual(m.neighbour_count, 0)

    def test_supports_agent_false(self):
        m = NavMeshManifest("m001", "Village Ground")
        self.assertFalse(m.supports_agent("Biped"))

    def test_supports_agent_true_after_add(self):
        m = NavMeshManifest("m001", "Village Ground", agent_types=["Biped"])
        self.assertTrue(m.supports_agent("Biped"))


# ---------------------------------------------------------------------------
# NavMeshLoader — registration
# ---------------------------------------------------------------------------

class TestNavMeshLoaderRegistration(unittest.TestCase):
    def setUp(self):
        self.loader = NavMeshLoader()

    def test_register_returns_manifest(self):
        m = self.loader.register("m001", "Forest Floor")
        self.assertIsInstance(m, NavMeshManifest)

    def test_registered_count(self):
        self.loader.register("m001", "Forest Floor")
        self.loader.register("m002", "Lake Bed")
        self.assertEqual(self.loader.get_registered_count(), 2)

    def test_get_manifest_by_id(self):
        self.loader.register("m001", "Forest Floor")
        m = self.loader.get_manifest("m001")
        self.assertIsNotNone(m)
        self.assertEqual(m.name, "Forest Floor")

    def test_get_manifest_missing_returns_none(self):
        self.assertIsNone(self.loader.get_manifest("ghost"))

    def test_get_all_mesh_ids(self):
        self.loader.register("m001", "Forest Floor")
        self.assertIn("m001", self.loader.get_all_mesh_ids())

    def test_unregister(self):
        self.loader.register("m001", "Forest Floor")
        self.assertTrue(self.loader.unregister("m001"))
        self.assertEqual(self.loader.get_registered_count(), 0)

    def test_unregister_missing_returns_false(self):
        self.assertFalse(self.loader.unregister("ghost"))

    def test_register_from_dict(self):
        data = {"mesh_id": "m001", "name": "Forest Floor", "mesh_type": "Ground"}
        m = self.loader.register_from_dict(data)
        self.assertIsNotNone(m)
        self.assertEqual(m.mesh_id, "m001")

    def test_register_from_dict_with_bounds(self):
        data = {
            "mesh_id": "m001",
            "name": "Forest Floor",
            "bounds": {
                "min_x": 0, "min_y": 0, "min_z": 0,
                "max_x": 200, "max_y": 50, "max_z": 200,
            },
        }
        m = self.loader.register_from_dict(data)
        self.assertIsNotNone(m)
        self.assertAlmostEqual(m.bounds.max_x, 200.0)

    def test_register_from_dict_missing_key_returns_none(self):
        self.assertIsNone(self.loader.register_from_dict({"name": "oops"}))

    def test_clear(self):
        self.loader.register("m001", "Forest Floor")
        self.loader.clear()
        self.assertEqual(self.loader.get_registered_count(), 0)


# ---------------------------------------------------------------------------
# NavMeshLoader — load/unload
# ---------------------------------------------------------------------------

class TestNavMeshLoaderLoadUnload(unittest.TestCase):
    def setUp(self):
        self.loader = NavMeshLoader()
        self.loader.register("m001", "Forest Floor", always_loaded=False)
        self.loader.register("m002", "Always Lake", always_loaded=True)

    def test_load_mesh(self):
        self.assertTrue(self.loader.load_mesh("m001"))
        self.assertTrue(self.loader.is_loaded("m001"))

    def test_load_unknown_returns_false(self):
        self.assertFalse(self.loader.load_mesh("ghost"))

    def test_unload_mesh(self):
        self.loader.load_mesh("m001")
        self.assertTrue(self.loader.unload_mesh("m001"))
        self.assertFalse(self.loader.is_loaded("m001"))

    def test_unload_not_loaded_returns_false(self):
        self.assertFalse(self.loader.unload_mesh("m001"))

    def test_get_loaded_count(self):
        self.loader.load_mesh("m001")
        self.assertEqual(self.loader.get_loaded_count(), 1)

    def test_get_loaded_ids(self):
        self.loader.load_mesh("m001")
        self.assertIn("m001", self.loader.get_loaded_ids())

    def test_load_always_loaded(self):
        count = self.loader.load_always_loaded()
        self.assertEqual(count, 1)
        self.assertTrue(self.loader.is_loaded("m002"))

    def test_clear_also_unloads(self):
        self.loader.load_mesh("m001")
        self.loader.clear()
        self.assertEqual(self.loader.get_loaded_count(), 0)


# ---------------------------------------------------------------------------
# NavMeshLoader — nodes and edges
# ---------------------------------------------------------------------------

class TestNavMeshLoaderNodesEdges(unittest.TestCase):
    def setUp(self):
        self.loader = NavMeshLoader()
        self.loader.register("m001", "Village Ground")

    def test_add_node_returns_node(self):
        n = self.loader.add_node("m001", 10.0, 0.0, 5.0)
        self.assertIsInstance(n, NavMeshNode)

    def test_node_mesh_id(self):
        n = self.loader.add_node("m001", 10.0, 0.0, 5.0)
        self.assertEqual(n.mesh_id, "m001")

    def test_node_position(self):
        n = self.loader.add_node("m001", 10.0, 2.0, 5.0)
        self.assertAlmostEqual(n.pos_x, 10.0)
        self.assertAlmostEqual(n.pos_y, 2.0)

    def test_node_count_increases(self):
        self.loader.add_node("m001", 0, 0, 0)
        self.loader.add_node("m001", 1, 0, 1)
        m = self.loader.get_manifest("m001")
        self.assertEqual(m.node_count, 2)

    def test_add_node_unknown_mesh_returns_none(self):
        self.assertIsNone(self.loader.add_node("ghost", 0, 0, 0))

    def test_add_edge_returns_edge(self):
        n1 = self.loader.add_node("m001", 0, 0, 0)
        n2 = self.loader.add_node("m001", 10, 0, 0)
        e = self.loader.add_edge("m001", n1.node_id, n2.node_id)
        self.assertIsInstance(e, NavMeshEdge)

    def test_edge_cost_default(self):
        n1 = self.loader.add_node("m001", 0, 0, 0)
        n2 = self.loader.add_node("m001", 10, 0, 0)
        e = self.loader.add_edge("m001", n1.node_id, n2.node_id)
        self.assertAlmostEqual(e.cost, 1.0)

    def test_edge_count_increases(self):
        n1 = self.loader.add_node("m001", 0, 0, 0)
        n2 = self.loader.add_node("m001", 10, 0, 0)
        self.loader.add_edge("m001", n1.node_id, n2.node_id)
        m = self.loader.get_manifest("m001")
        self.assertEqual(m.edge_count, 1)

    def test_add_edge_unknown_mesh_returns_none(self):
        self.assertIsNone(self.loader.add_edge("ghost", "n001", "n002"))


# ---------------------------------------------------------------------------
# NavMeshLoader — neighbours and agents
# ---------------------------------------------------------------------------

class TestNavMeshLoaderNeighboursAgents(unittest.TestCase):
    def setUp(self):
        self.loader = NavMeshLoader()
        self.loader.register("m001", "Village Ground")
        self.loader.register("m002", "Market Square")

    def test_add_neighbour(self):
        self.assertTrue(self.loader.add_neighbour("m001", "m002"))

    def test_get_neighbours(self):
        self.loader.add_neighbour("m001", "m002")
        neighbours = self.loader.get_neighbours("m001")
        self.assertIn("m002", neighbours)

    def test_get_neighbours_unknown_returns_empty(self):
        self.assertEqual(self.loader.get_neighbours("ghost"), [])

    def test_add_neighbour_no_duplicate(self):
        self.loader.add_neighbour("m001", "m002")
        self.loader.add_neighbour("m001", "m002")
        m = self.loader.get_manifest("m001")
        self.assertEqual(m.neighbour_ids.count("m002"), 1)

    def test_add_agent_type(self):
        self.assertTrue(self.loader.add_agent_type("m001", "Biped"))

    def test_supports_agent_after_add(self):
        self.loader.add_agent_type("m001", "Biped")
        m = self.loader.get_manifest("m001")
        self.assertTrue(m.supports_agent("Biped"))

    def test_add_agent_type_no_duplicate(self):
        self.loader.add_agent_type("m001", "Biped")
        self.loader.add_agent_type("m001", "Biped")
        m = self.loader.get_manifest("m001")
        self.assertEqual(m.agent_types.count("Biped"), 1)


# ---------------------------------------------------------------------------
# NavMeshLoader — spatial queries
# ---------------------------------------------------------------------------

class TestNavMeshLoaderSpatialQuery(unittest.TestCase):
    def setUp(self):
        self.loader = NavMeshLoader()
        m = self.loader.register("m001", "Village Ground")
        m.bounds = NavMeshAABB(0, 0, 0, 100, 10, 100)
        m2 = self.loader.register("m002", "Highlands")
        m2.bounds = NavMeshAABB(200, 0, 0, 400, 20, 200)

    def test_query_point_hit(self):
        results = self.loader.query_point(50, 5, 50)
        self.assertIn("m001", results)

    def test_query_point_miss(self):
        results = self.loader.query_point(150, 5, 50)
        self.assertEqual(results, [])

    def test_query_path_same_mesh(self):
        path = self.loader.query_path("m001", "m001")
        self.assertEqual(path, ["m001"])

    def test_query_path_returns_list(self):
        path = self.loader.query_path("m001", "m002")
        self.assertIsInstance(path, list)
        self.assertGreater(len(path), 0)

    def test_query_path_start_not_found(self):
        path = self.loader.query_path("ghost", "m001")
        self.assertEqual(path, [])


# ---------------------------------------------------------------------------
# NavMeshLoader — persistence
# ---------------------------------------------------------------------------

class TestNavMeshLoaderPersistence(unittest.TestCase):
    def setUp(self):
        self.loader = NavMeshLoader()
        m = self.loader.register("m001", "Village Ground",
                                  mesh_type="Ground", priority=5)
        m.agent_types = ["Biped", "Quadruped"]
        m.neighbour_ids = ["m002"]

    def test_save_registry(self):
        out = str(TMP_DIR / "nav_mesh_registry.json")
        self.assertTrue(self.loader.save_registry(out))
        self.assertTrue(Path(out).exists())

    def test_save_registry_content(self):
        out = str(TMP_DIR / "nav_mesh_registry2.json")
        self.loader.save_registry(out)
        data = json.loads(Path(out).read_text())
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["mesh_id"], "m001")

    def test_load_registry(self):
        out = str(TMP_DIR / "nav_mesh_registry3.json")
        self.loader.save_registry(out)
        loader2 = NavMeshLoader()
        count = loader2.load_registry(out)
        self.assertEqual(count, 1)
        self.assertIsNotNone(loader2.get_manifest("m001"))

    def test_load_registry_missing_file_returns_zero(self):
        loader2 = NavMeshLoader()
        count = loader2.load_registry("/tmp/no_such_file_xyz.json")
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
