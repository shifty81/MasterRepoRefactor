"""Phase 24D — Tests for ScenePartitionRegistry.h and ScenePartitionLoader."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

from AtlasAIEngine.intelligence import (
    ScenePartitionLoader,
    ScenePartitionManifest,
    PartitionBounds,
    PartitionPortal,
)

TMP_DIR = Path("/tmp/test_phase24d")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# ScenePartitionRegistry.h tests
# ---------------------------------------------------------------------------

def _reg() -> str:
    return (SCENE_DIR / "ScenePartitionRegistry.h").read_text()


class TestScenePartitionRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "ScenePartitionRegistry.h").exists())


class TestScenePartitionRegistryHeader(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _reg())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _reg())

    def test_class_declared(self):
        self.assertIn("class ScenePartitionRegistry", _reg())


class TestScenePartitionRegistryAPI(unittest.TestCase):
    def test_register_partition(self):
        self.assertIn("RegisterPartition", _reg())

    def test_unregister_partition(self):
        self.assertIn("UnregisterPartition", _reg())

    def test_is_registered(self):
        self.assertIn("IsRegistered", _reg())

    def test_get_partition_count(self):
        self.assertIn("GetPartitionCount", _reg())

    def test_load_partition(self):
        self.assertIn("LoadPartition", _reg())

    def test_unload_partition(self):
        self.assertIn("UnloadPartition", _reg())

    def test_is_loaded(self):
        self.assertIn("IsLoaded", _reg())

    def test_get_loaded_count(self):
        self.assertIn("GetLoadedCount", _reg())

    def test_get_loaded_partition_ids(self):
        self.assertIn("GetLoadedPartitionIds", _reg())

    def test_register_portal(self):
        self.assertIn("RegisterPortal", _reg())

    def test_unregister_portal(self):
        self.assertIn("UnregisterPortal", _reg())

    def test_get_portal_count(self):
        self.assertIn("GetPortalCount", _reg())

    def test_get_portals_for_partition(self):
        self.assertIn("GetPortalsForPartition", _reg())

    def test_get_neighbours(self):
        self.assertIn("GetNeighbours", _reg())

    def test_add_bundle(self):
        self.assertIn("AddBundle", _reg())

    def test_get_bundles(self):
        self.assertIn("GetBundles", _reg())

    def test_query_point(self):
        self.assertIn("QueryPoint", _reg())

    def test_query_aabb(self):
        self.assertIn("QueryAABB", _reg())

    def test_get_always_loaded_partitions(self):
        self.assertIn("GetAlwaysLoadedPartitions", _reg())

    def test_get_partitions_by_type(self):
        self.assertIn("GetPartitionsByType", _reg())

    def test_get_partitions_by_priority(self):
        self.assertIn("GetPartitionsByPriority", _reg())

    def test_set_parent(self):
        self.assertIn("SetParent", _reg())

    def test_get_children(self):
        self.assertIn("GetChildren", _reg())

    def test_get_partition(self):
        self.assertIn("GetPartition", _reg())

    def test_get_all_partition_ids(self):
        self.assertIn("GetAllPartitionIds", _reg())

    def test_for_each(self):
        self.assertIn("ForEach", _reg())

    def test_on_loaded_callback(self):
        self.assertIn("SetOnPartitionLoadedCallback", _reg())

    def test_on_unloaded_callback(self):
        self.assertIn("SetOnPartitionUnloadedCallback", _reg())

    def test_clear(self):
        self.assertIn("Clear", _reg())


class TestScenePartitionRegistryStructs(unittest.TestCase):
    def test_partition_record_struct(self):
        self.assertIn("PartitionRecord", _reg())

    def test_portal_link_struct(self):
        self.assertIn("PortalLink", _reg())

    def test_aabb_struct(self):
        self.assertIn("AABB", _reg())

    def test_partition_state_enum(self):
        self.assertIn("PartitionState", _reg())

    def test_partition_type_enum(self):
        self.assertIn("PartitionType", _reg())

    def test_always_loaded_field(self):
        self.assertIn("alwaysLoaded", _reg())

    def test_priority_field(self):
        self.assertIn("priority", _reg())

    def test_portal_ids_field(self):
        self.assertIn("portalIds", _reg())

    def test_neighbour_ids_field(self):
        self.assertIn("neighbourIds", _reg())


# ---------------------------------------------------------------------------
# PartitionBounds dataclass
# ---------------------------------------------------------------------------

class TestPartitionBoundsDataclass(unittest.TestCase):
    def test_defaults(self):
        b = PartitionBounds()
        self.assertEqual(b.min_x, 0.0)
        self.assertEqual(b.max_x, 100.0)

    def test_custom_bounds(self):
        b = PartitionBounds(0, 0, 0, 50, 10, 50)
        self.assertEqual(b.max_x, 50.0)

    def test_contains_point_inside(self):
        b = PartitionBounds(0, 0, 0, 100, 100, 100)
        self.assertTrue(b.contains_point(50, 50, 50))

    def test_contains_point_outside(self):
        b = PartitionBounds(0, 0, 0, 100, 100, 100)
        self.assertFalse(b.contains_point(200, 50, 50))

    def test_intersects_true(self):
        a = PartitionBounds(0, 0, 0, 100, 100, 100)
        b = PartitionBounds(50, 50, 50, 150, 150, 150)
        self.assertTrue(a.intersects(b))

    def test_intersects_false(self):
        a = PartitionBounds(0, 0, 0, 50, 50, 50)
        b = PartitionBounds(100, 100, 100, 200, 200, 200)
        self.assertFalse(a.intersects(b))

    def test_volume_positive(self):
        b = PartitionBounds(0, 0, 0, 10, 5, 2)
        self.assertAlmostEqual(b.volume, 100.0)

    def test_volume_zero_degenerate(self):
        b = PartitionBounds(5, 5, 5, 5, 5, 5)
        self.assertEqual(b.volume, 0.0)


# ---------------------------------------------------------------------------
# ScenePartitionManifest dataclass
# ---------------------------------------------------------------------------

class TestScenePartitionManifestDataclass(unittest.TestCase):
    def test_partition_id_field(self):
        m = ScenePartitionManifest("sector_01", "Zone A")
        self.assertEqual(m.partition_id, "sector_01")

    def test_name_field(self):
        m = ScenePartitionManifest("sector_01", "Zone A")
        self.assertEqual(m.name, "Zone A")

    def test_default_type(self):
        m = ScenePartitionManifest("sector_01", "Zone A")
        self.assertEqual(m.partition_type, "Sector")

    def test_bundle_count_zero(self):
        m = ScenePartitionManifest("sector_01", "Zone A")
        self.assertEqual(m.bundle_count, 0)

    def test_neighbour_count_zero(self):
        m = ScenePartitionManifest("sector_01", "Zone A")
        self.assertEqual(m.neighbour_count, 0)


# ---------------------------------------------------------------------------
# ScenePartitionLoader — registration
# ---------------------------------------------------------------------------

def _make_loader() -> ScenePartitionLoader:
    loader = ScenePartitionLoader("/tmp")
    loader.register_from_dict({
        "partition_id": "p_a",
        "name": "Zone A",
        "partition_type": "Sector",
        "bounds": {"min_x": 0, "min_y": 0, "min_z": 0,
                   "max_x": 100, "max_y": 50, "max_z": 100},
    })
    loader.register_from_dict({
        "partition_id": "p_b",
        "name": "Zone B",
        "partition_type": "Cell",
        "bounds": {"min_x": 100, "min_y": 0, "min_z": 0,
                   "max_x": 200, "max_y": 50, "max_z": 100},
        "priority": 5,
        "always_loaded": True,
    })
    loader.register_from_dict({
        "partition_id": "p_c",
        "name": "Room C",
        "partition_type": "Room",
        "bounds": {"min_x": 200, "min_y": 0, "min_z": 0,
                   "max_x": 300, "max_y": 50, "max_z": 100},
        "parent_partition_id": "p_a",
    })
    return loader


class TestScenePartitionLoaderRegistration(unittest.TestCase):
    def setUp(self):
        self.loader = _make_loader()

    def test_register_from_dict_returns_manifest(self):
        m = self.loader.register_from_dict({"partition_id": "px", "name": "X"})
        self.assertIsInstance(m, ScenePartitionManifest)

    def test_get_partition_count(self):
        self.assertEqual(self.loader.get_partition_count(), 3)

    def test_get_all_partition_ids(self):
        ids = self.loader.get_all_partition_ids()
        self.assertIn("p_a", ids)
        self.assertIn("p_c", ids)

    def test_get_partition_returns_manifest(self):
        m = self.loader.get_partition("p_b")
        self.assertIsNotNone(m)
        self.assertEqual(m.name, "Zone B")

    def test_get_partition_missing_returns_none(self):
        self.assertIsNone(self.loader.get_partition("ghost"))

    def test_unregister_returns_true(self):
        self.assertTrue(self.loader.unregister("p_c"))

    def test_unregister_removes_partition(self):
        self.loader.unregister("p_c")
        self.assertIsNone(self.loader.get_partition("p_c"))

    def test_unregister_missing_returns_false(self):
        self.assertFalse(self.loader.unregister("ghost"))


# ---------------------------------------------------------------------------
# ScenePartitionLoader — load/unload
# ---------------------------------------------------------------------------

class TestScenePartitionLoaderLoadUnload(unittest.TestCase):
    def setUp(self):
        self.loader = _make_loader()

    def test_load_partition_returns_true(self):
        self.assertTrue(self.loader.load_partition("p_a"))

    def test_is_loaded_true(self):
        self.loader.load_partition("p_a")
        self.assertTrue(self.loader.is_loaded("p_a"))

    def test_is_loaded_false_before_load(self):
        self.assertFalse(self.loader.is_loaded("p_a"))

    def test_load_missing_returns_false(self):
        self.assertFalse(self.loader.load_partition("ghost"))

    def test_unload_partition_returns_true(self):
        self.loader.load_partition("p_a")
        self.assertTrue(self.loader.unload_partition("p_a"))

    def test_unload_removes_from_loaded(self):
        self.loader.load_partition("p_a")
        self.loader.unload_partition("p_a")
        self.assertFalse(self.loader.is_loaded("p_a"))

    def test_unload_not_loaded_returns_false(self):
        self.assertFalse(self.loader.unload_partition("p_a"))

    def test_get_loaded_count(self):
        self.loader.load_partition("p_a")
        self.loader.load_partition("p_b")
        self.assertEqual(self.loader.get_loaded_count(), 2)

    def test_get_loaded_partition_ids(self):
        self.loader.load_partition("p_a")
        self.assertIn("p_a", self.loader.get_loaded_partition_ids())


# ---------------------------------------------------------------------------
# ScenePartitionLoader — portals
# ---------------------------------------------------------------------------

class TestScenePartitionLoaderPortals(unittest.TestCase):
    def setUp(self):
        self.loader = _make_loader()

    def test_register_portal_returns_portal(self):
        p = self.loader.register_portal("p_a", "p_b", 100, 0, 50)
        self.assertIsInstance(p, PartitionPortal)

    def test_register_portal_increments_count(self):
        self.loader.register_portal("p_a", "p_b", 100, 0, 50)
        self.assertEqual(self.loader.get_portal_count(), 1)

    def test_register_portal_missing_partition_returns_none(self):
        p = self.loader.register_portal("ghost", "p_b", 0, 0, 0)
        self.assertIsNone(p)

    def test_get_portals_for_partition(self):
        self.loader.register_portal("p_a", "p_b", 100, 0, 50)
        portals = self.loader.get_portals_for_partition("p_a")
        self.assertEqual(len(portals), 1)

    def test_bidirectional_portal_appears_for_both(self):
        self.loader.register_portal("p_a", "p_b", 100, 0, 50, bidirectional=True)
        self.assertEqual(len(self.loader.get_portals_for_partition("p_b")), 1)

    def test_get_neighbours_populated_by_portal(self):
        self.loader.register_portal("p_a", "p_b", 100, 0, 50)
        neighbours = self.loader.get_neighbours("p_a")
        self.assertIn("p_b", neighbours)

    def test_unregister_portal_returns_true(self):
        p = self.loader.register_portal("p_a", "p_b", 100, 0, 50)
        self.assertTrue(self.loader.unregister_portal(p.portal_id))

    def test_unregister_portal_decrements_count(self):
        p = self.loader.register_portal("p_a", "p_b", 100, 0, 50)
        self.loader.unregister_portal(p.portal_id)
        self.assertEqual(self.loader.get_portal_count(), 0)


# ---------------------------------------------------------------------------
# ScenePartitionLoader — queries
# ---------------------------------------------------------------------------

class TestScenePartitionLoaderQueries(unittest.TestCase):
    def setUp(self):
        self.loader = _make_loader()

    def test_query_point_inside_a(self):
        results = self.loader.query_point(50, 25, 50)
        ids = [m.partition_id for m in results]
        self.assertIn("p_a", ids)

    def test_query_point_outside_all(self):
        results = self.loader.query_point(999, 999, 999)
        self.assertEqual(len(results), 0)

    def test_get_always_loaded_partitions(self):
        partitions = self.loader.get_always_loaded_partitions()
        ids = [m.partition_id for m in partitions]
        self.assertIn("p_b", ids)

    def test_get_partitions_by_type_sector(self):
        partitions = self.loader.get_partitions_by_type("Sector")
        self.assertEqual(len(partitions), 1)

    def test_get_partitions_by_priority(self):
        partitions = self.loader.get_partitions_by_priority(min_priority=3)
        ids = [m.partition_id for m in partitions]
        self.assertIn("p_b", ids)

    def test_get_children(self):
        children = self.loader.get_children("p_a")
        ids = [m.partition_id for m in children]
        self.assertIn("p_c", ids)

    def test_clear(self):
        self.loader.clear()
        self.assertEqual(self.loader.get_partition_count(), 0)
        self.assertEqual(self.loader.get_portal_count(), 0)


# ---------------------------------------------------------------------------
# __init__ exports
# ---------------------------------------------------------------------------

class TestInitExports(unittest.TestCase):
    def test_scene_partition_loader_exported(self):
        from AtlasAIEngine.intelligence import ScenePartitionLoader as SPL
        self.assertIsNotNone(SPL)

    def test_scene_partition_manifest_exported(self):
        from AtlasAIEngine.intelligence import ScenePartitionManifest as SPM
        self.assertIsNotNone(SPM)

    def test_partition_bounds_exported(self):
        from AtlasAIEngine.intelligence import PartitionBounds as PB
        self.assertIsNotNone(PB)

    def test_partition_portal_exported(self):
        from AtlasAIEngine.intelligence import PartitionPortal as PP
        self.assertIsNotNone(PP)


if __name__ == "__main__":
    unittest.main()
