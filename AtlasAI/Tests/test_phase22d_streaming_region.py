"""Phase 22D — Tests for StreamingRegionRegistry.h and StreamingRegionLoader."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

from AtlasAIEngine.intelligence import (
    StreamingRegionLoader,
    StreamingRegionManifest,
    RegionBounds,
)

TMP_DIR = Path("/tmp/test_phase22d")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# StreamingRegionRegistry.h tests
# ---------------------------------------------------------------------------

def _reg() -> str:
    return (SCENE_DIR / "StreamingRegionRegistry.h").read_text()


class TestStreamingRegionRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "StreamingRegionRegistry.h").exists())


class TestStreamingRegionRegistryHeader(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _reg())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _reg())

    def test_class_declared(self):
        self.assertIn("class StreamingRegionRegistry", _reg())


class TestStreamingRegionRegistryAPI(unittest.TestCase):
    def test_register_region(self):
        self.assertIn("RegisterRegion", _reg())

    def test_unregister_region(self):
        self.assertIn("UnregisterRegion", _reg())

    def test_is_registered(self):
        self.assertIn("IsRegistered", _reg())

    def test_get_region_count(self):
        self.assertIn("GetRegionCount", _reg())

    def test_add_bundle(self):
        self.assertIn("AddBundle", _reg())

    def test_get_bundles(self):
        self.assertIn("GetBundles", _reg())

    def test_load_region(self):
        self.assertIn("LoadRegion", _reg())

    def test_unload_region(self):
        self.assertIn("UnloadRegion", _reg())

    def test_is_loaded(self):
        self.assertIn("IsLoaded", _reg())

    def test_get_loaded_count(self):
        self.assertIn("GetLoadedCount", _reg())

    def test_get_loaded_region_ids(self):
        self.assertIn("GetLoadedRegionIds", _reg())

    def test_query_point(self):
        self.assertIn("QueryPoint", _reg())

    def test_query_aabb(self):
        self.assertIn("QueryAABB", _reg())

    def test_get_always_loaded_regions(self):
        self.assertIn("GetAlwaysLoadedRegions", _reg())

    def test_get_regions_by_priority(self):
        self.assertIn("GetRegionsByPriority", _reg())

    def test_get_region(self):
        self.assertIn("GetRegion", _reg())

    def test_get_all_region_ids(self):
        self.assertIn("GetAllRegionIds", _reg())

    def test_for_each(self):
        self.assertIn("ForEach", _reg())

    def test_clear(self):
        self.assertIn("Clear", _reg())

    def test_on_loaded_callback(self):
        self.assertIn("SetOnRegionLoadedCallback", _reg())

    def test_on_unloaded_callback(self):
        self.assertIn("SetOnRegionUnloadedCallback", _reg())


class TestStreamingRegionRegistryStructs(unittest.TestCase):
    def test_region_record_struct(self):
        self.assertIn("RegionRecord", _reg())

    def test_aabb_struct(self):
        self.assertIn("AABB", _reg())

    def test_region_state_enum(self):
        self.assertIn("RegionState", _reg())

    def test_always_loaded_field(self):
        self.assertIn("alwaysLoaded", _reg())

    def test_priority_field(self):
        self.assertIn("priority", _reg())

    def test_bundle_ids_field(self):
        self.assertIn("bundleIds", _reg())


# ---------------------------------------------------------------------------
# RegionBounds dataclass
# ---------------------------------------------------------------------------

class TestRegionBoundsDataclass(unittest.TestCase):
    def test_defaults(self):
        b = RegionBounds()
        self.assertEqual(b.min_x, 0.0)
        self.assertEqual(b.max_x, 100.0)

    def test_custom_bounds(self):
        b = RegionBounds(0, 0, 0, 50, 10, 50)
        self.assertEqual(b.max_x, 50.0)

    def test_contains_point_inside(self):
        b = RegionBounds(0, 0, 0, 100, 100, 100)
        self.assertTrue(b.contains_point(50, 50, 50))

    def test_contains_point_outside(self):
        b = RegionBounds(0, 0, 0, 100, 100, 100)
        self.assertFalse(b.contains_point(150, 50, 50))

    def test_contains_point_on_boundary(self):
        b = RegionBounds(0, 0, 0, 100, 100, 100)
        self.assertTrue(b.contains_point(0, 0, 0))
        self.assertTrue(b.contains_point(100, 100, 100))


# ---------------------------------------------------------------------------
# StreamingRegionManifest dataclass
# ---------------------------------------------------------------------------

class TestStreamingRegionManifestDataclass(unittest.TestCase):
    def _manifest(self, **kw):
        defaults = dict(region_id="r1", name="Region 1",
                        bounds=RegionBounds())
        defaults.update(kw)
        return StreamingRegionManifest(**defaults)

    def test_region_id_field(self):
        m = self._manifest(region_id="zone_01")
        self.assertEqual(m.region_id, "zone_01")

    def test_name_field(self):
        m = self._manifest(name="Zone Alpha")
        self.assertEqual(m.name, "Zone Alpha")

    def test_bundle_ids_default_empty(self):
        m = self._manifest()
        self.assertEqual(m.bundle_ids, [])

    def test_always_loaded_default_false(self):
        m = self._manifest()
        self.assertFalse(m.always_loaded)

    def test_priority_default_zero(self):
        m = self._manifest()
        self.assertEqual(m.priority, 0)

    def test_bundle_count_property(self):
        m = self._manifest(bundle_ids=["b1", "b2"])
        self.assertEqual(m.bundle_count, 2)


# ---------------------------------------------------------------------------
# StreamingRegionLoader — registration
# ---------------------------------------------------------------------------

def _make_region_data(region_id: str, bounds: dict = None,
                       always_loaded: bool = False,
                       priority: int = 0,
                       bundles: list = None) -> dict:
    return {
        "region_id": region_id,
        "name": f"{region_id} name",
        "bounds": bounds or {"min_x": 0, "min_y": 0, "min_z": 0,
                              "max_x": 100, "max_y": 100, "max_z": 100},
        "bundle_ids": bundles or [],
        "always_loaded": always_loaded,
        "priority": priority,
    }


class TestStreamingRegionLoaderRegistration(unittest.TestCase):
    def setUp(self):
        self.loader = StreamingRegionLoader(str(TMP_DIR))

    def test_register_returns_manifest(self):
        m = self.loader.register_manifest(_make_region_data("r1"))
        self.assertIsInstance(m, StreamingRegionManifest)

    def test_register_increments_count(self):
        self.loader.register_manifest(_make_region_data("r1"))
        self.loader.register_manifest(_make_region_data("r2"))
        self.assertEqual(self.loader.get_registered_count(), 2)

    def test_get_manifest(self):
        self.loader.register_manifest(_make_region_data("r1"))
        m = self.loader.get_manifest("r1")
        self.assertIsNotNone(m)
        self.assertEqual(m.region_id, "r1")

    def test_get_manifest_missing_returns_none(self):
        self.assertIsNone(self.loader.get_manifest("ghost"))

    def test_get_all_region_ids(self):
        self.loader.register_manifest(_make_region_data("r1"))
        self.loader.register_manifest(_make_region_data("r2"))
        ids = self.loader.get_all_region_ids()
        self.assertIn("r1", ids)
        self.assertIn("r2", ids)

    def test_clear_removes_all(self):
        self.loader.register_manifest(_make_region_data("r1"))
        self.loader.clear()
        self.assertEqual(self.loader.get_registered_count(), 0)


# ---------------------------------------------------------------------------
# StreamingRegionLoader — load/unload
# ---------------------------------------------------------------------------

class TestStreamingRegionLoaderLoadUnload(unittest.TestCase):
    def setUp(self):
        self.loader = StreamingRegionLoader(str(TMP_DIR))
        self.loader.register_manifest(_make_region_data("zone_01"))

    def test_load_returns_true(self):
        self.assertTrue(self.loader.load_region("zone_01"))

    def test_load_marks_loaded(self):
        self.loader.load_region("zone_01")
        self.assertTrue(self.loader.is_loaded("zone_01"))

    def test_load_unknown_returns_false(self):
        self.assertFalse(self.loader.load_region("ghost"))

    def test_unload_returns_true(self):
        self.loader.load_region("zone_01")
        self.assertTrue(self.loader.unload_region("zone_01"))

    def test_unload_removes_loaded(self):
        self.loader.load_region("zone_01")
        self.loader.unload_region("zone_01")
        self.assertFalse(self.loader.is_loaded("zone_01"))

    def test_unload_not_loaded_returns_false(self):
        self.assertFalse(self.loader.unload_region("zone_01"))

    def test_get_loaded_count(self):
        self.loader.register_manifest(_make_region_data("zone_02"))
        self.loader.load_region("zone_01")
        self.loader.load_region("zone_02")
        self.assertEqual(self.loader.get_loaded_count(), 2)

    def test_get_loaded_region_ids(self):
        self.loader.load_region("zone_01")
        self.assertIn("zone_01", self.loader.get_loaded_region_ids())


# ---------------------------------------------------------------------------
# StreamingRegionLoader — spatial query
# ---------------------------------------------------------------------------

class TestStreamingRegionLoaderSpatialQuery(unittest.TestCase):
    def setUp(self):
        self.loader = StreamingRegionLoader(str(TMP_DIR))
        self.loader.register_manifest(_make_region_data(
            "zone_a",
            bounds={"min_x": 0, "min_y": 0, "min_z": 0,
                    "max_x": 100, "max_y": 50, "max_z": 100}
        ))
        self.loader.register_manifest(_make_region_data(
            "zone_b",
            bounds={"min_x": 200, "min_y": 0, "min_z": 200,
                    "max_x": 400, "max_y": 50, "max_z": 400}
        ))

    def test_query_point_inside_zone_a(self):
        results = self.loader.query_point(50, 25, 50)
        self.assertIn("zone_a", results)
        self.assertNotIn("zone_b", results)

    def test_query_point_inside_zone_b(self):
        results = self.loader.query_point(300, 25, 300)
        self.assertIn("zone_b", results)

    def test_query_point_outside_all(self):
        results = self.loader.query_point(1000, 1000, 1000)
        self.assertEqual(len(results), 0)

    def test_get_always_loaded(self):
        self.loader.register_manifest(
            _make_region_data("core", always_loaded=True)
        )
        al = self.loader.get_always_loaded()
        self.assertEqual(len(al), 1)
        self.assertEqual(al[0].region_id, "core")

    def test_get_by_priority(self):
        self.loader.register_manifest(
            _make_region_data("hi_pri", priority=10)
        )
        results = self.loader.get_by_priority(5)
        ids = [m.region_id for m in results]
        self.assertIn("hi_pri", ids)


# ---------------------------------------------------------------------------
# StreamingRegionLoader — discovery
# ---------------------------------------------------------------------------

class TestStreamingRegionLoaderDiscovery(unittest.TestCase):
    def setUp(self):
        self.root = TMP_DIR / "region_discovery"
        (self.root / "ZoneAlpha").mkdir(parents=True, exist_ok=True)
        (self.root / "ZoneBeta").mkdir(parents=True, exist_ok=True)
        (self.root / "ZoneAlpha" / "region_manifest.json").write_text(
            json.dumps(_make_region_data("disc_zone_a",
                       bundles=["bundle_a1", "bundle_a2"]))
        )
        (self.root / "ZoneBeta" / "region_manifest.json").write_text(
            json.dumps(_make_region_data("disc_zone_b"))
        )
        self.loader = StreamingRegionLoader(str(self.root))

    def test_discover_returns_list(self):
        ids = self.loader.discover()
        self.assertIsInstance(ids, list)

    def test_discover_finds_both(self):
        ids = self.loader.discover()
        self.assertIn("disc_zone_a", ids)
        self.assertIn("disc_zone_b", ids)

    def test_discover_registers_bundles(self):
        self.loader.discover()
        m = self.loader.get_manifest("disc_zone_a")
        self.assertEqual(m.bundle_count, 2)


# ---------------------------------------------------------------------------
# StreamingRegionLoader — export
# ---------------------------------------------------------------------------

class TestStreamingRegionLoaderExport(unittest.TestCase):
    def setUp(self):
        self.loader = StreamingRegionLoader(str(TMP_DIR))
        self.loader.register_manifest(
            _make_region_data("export_zone", always_loaded=True,
                               priority=5, bundles=["b1"])
        )

    def test_export_returns_true(self):
        path = str(TMP_DIR / "region_export.json")
        self.assertTrue(self.loader.export_manifest("export_zone", path))

    def test_export_creates_file(self):
        path = str(TMP_DIR / "region_export2.json")
        self.loader.export_manifest("export_zone", path)
        self.assertTrue(Path(path).exists())

    def test_export_valid_json(self):
        path = str(TMP_DIR / "region_export3.json")
        self.loader.export_manifest("export_zone", path)
        data = json.loads(Path(path).read_text())
        self.assertEqual(data["region_id"], "export_zone")
        self.assertTrue(data["always_loaded"])

    def test_export_missing_returns_false(self):
        self.assertFalse(
            self.loader.export_manifest("ghost", str(TMP_DIR / "g.json"))
        )


# ---------------------------------------------------------------------------
# __init__ exports
# ---------------------------------------------------------------------------

class TestInitExports(unittest.TestCase):
    def test_streaming_region_loader_exported(self):
        from AtlasAIEngine.intelligence import StreamingRegionLoader as SRL
        self.assertIsNotNone(SRL)

    def test_streaming_region_manifest_exported(self):
        from AtlasAIEngine.intelligence import StreamingRegionManifest as SRM
        self.assertIsNotNone(SRM)

    def test_region_bounds_exported(self):
        from AtlasAIEngine.intelligence import RegionBounds as RB
        self.assertIsNotNone(RB)


if __name__ == "__main__":
    unittest.main()
