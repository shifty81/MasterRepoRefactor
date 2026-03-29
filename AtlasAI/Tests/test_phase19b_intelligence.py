"""Phase 19B — Tests for SceneQueryEngine and LayoutExportBridge."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    SceneQueryEngine,
    SceneEntityRecord,
    LayoutExportBridge,
    LayoutEntry,
)

TMP_DIR = Path("/tmp/test_phase19b")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# SceneEntityRecord tests
# ---------------------------------------------------------------------------

class TestSceneEntityRecordDataclass(unittest.TestCase):
    def test_entity_id_field(self):
        r = SceneEntityRecord("ent_1", "Planet")
        self.assertEqual(r.entity_id, "ent_1")

    def test_entity_type_field(self):
        r = SceneEntityRecord("ent_1", "Planet")
        self.assertEqual(r.entity_type, "Planet")

    def test_xyz_defaults(self):
        r = SceneEntityRecord("e", "T")
        self.assertEqual(r.x, 0.0)
        self.assertEqual(r.y, 0.0)
        self.assertEqual(r.z, 0.0)

    def test_tags_default_empty(self):
        r = SceneEntityRecord("e", "T")
        self.assertIsInstance(r.tags, list)
        self.assertEqual(len(r.tags), 0)

    def test_properties_default_empty(self):
        r = SceneEntityRecord("e", "T")
        self.assertIsInstance(r.properties, dict)

    def test_tags_set(self):
        r = SceneEntityRecord("e", "T", tags=["habitable"])
        self.assertIn("habitable", r.tags)

    def test_properties_set(self):
        r = SceneEntityRecord("e", "T", properties={"faction": "dev"})
        self.assertEqual(r.properties["faction"], "dev")


# ---------------------------------------------------------------------------
# SceneQueryEngine — registration
# ---------------------------------------------------------------------------

class TestSceneQueryEngineRegistration(unittest.TestCase):
    def setUp(self):
        self.engine = SceneQueryEngine()

    def test_register_returns_record(self):
        rec = self.engine.register("e1", "Planet")
        self.assertIsInstance(rec, SceneEntityRecord)

    def test_register_stores_entity(self):
        self.engine.register("e1", "Planet")
        self.assertEqual(self.engine.get_entity_count(), 1)

    def test_get_entity_returns_record(self):
        self.engine.register("e1", "Planet", x=1.0)
        rec = self.engine.get_entity("e1")
        self.assertIsNotNone(rec)
        self.assertEqual(rec.x, 1.0)

    def test_get_entity_missing_returns_none(self):
        self.assertIsNone(self.engine.get_entity("nonexistent"))

    def test_unregister_returns_true(self):
        self.engine.register("e1", "Planet")
        self.assertTrue(self.engine.unregister("e1"))

    def test_unregister_removes_entity(self):
        self.engine.register("e1", "Planet")
        self.engine.unregister("e1")
        self.assertEqual(self.engine.get_entity_count(), 0)

    def test_unregister_missing_returns_false(self):
        self.assertFalse(self.engine.unregister("ghost"))

    def test_clear_removes_all(self):
        self.engine.register("e1", "Planet")
        self.engine.register("e2", "Station")
        self.engine.clear()
        self.assertEqual(self.engine.get_entity_count(), 0)


# ---------------------------------------------------------------------------
# SceneQueryEngine — query methods
# ---------------------------------------------------------------------------

class TestSceneQueryEngineQueries(unittest.TestCase):
    def setUp(self):
        self.engine = SceneQueryEngine()
        self.engine.register("p1", "Planet", x=0.0, z=0.0, tags=["habitable"])
        self.engine.register("p2", "Planet", x=5.0, z=5.0, tags=["hostile"])
        self.engine.register("s1", "Station", x=1.0, z=1.0, tags=["dev"])
        self.engine.register("a1", "Asteroid", x=20.0, z=20.0,
                              properties={"ore": "veldspar"})

    def test_query_by_type_planet(self):
        results = self.engine.query_by_type("Planet")
        self.assertEqual(len(results), 2)

    def test_query_by_type_station(self):
        results = self.engine.query_by_type("Station")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_id, "s1")

    def test_query_by_type_missing_returns_empty(self):
        self.assertEqual(self.engine.query_by_type("Wormhole"), [])

    def test_query_by_tag_habitable(self):
        results = self.engine.query_by_tag("habitable")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_id, "p1")

    def test_query_by_tag_multiple(self):
        self.engine.register("p3", "Planet", tags=["habitable", "dev"])
        results = self.engine.query_by_tag("habitable")
        self.assertEqual(len(results), 2)

    def test_query_by_property(self):
        results = self.engine.query_by_property("ore", "veldspar")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_id, "a1")

    def test_query_by_property_no_match(self):
        self.assertEqual(self.engine.query_by_property("ore", "platinum"), [])

    def test_query_within_radius_includes_nearby(self):
        # origin 0,0, radius 3 → should include p1(0,0) and s1(1,1)
        results = self.engine.query_within_radius(0.0, 0.0, 3.0)
        ids = {r.entity_id for r in results}
        self.assertIn("p1", ids)
        self.assertIn("s1", ids)

    def test_query_within_radius_excludes_far(self):
        results = self.engine.query_within_radius(0.0, 0.0, 3.0)
        ids = {r.entity_id for r in results}
        self.assertNotIn("a1", ids)

    def test_query_custom_predicate(self):
        results = self.engine.query(lambda e: e.entity_type == "Asteroid")
        self.assertEqual(len(results), 1)


# ---------------------------------------------------------------------------
# SceneQueryEngine — export
# ---------------------------------------------------------------------------

class TestSceneQueryEngineExport(unittest.TestCase):
    def setUp(self):
        self.engine = SceneQueryEngine()
        self.engine.register("e1", "Planet", x=1.0, tags=["t1"])

    def test_export_returns_true(self):
        path = str(TMP_DIR / "query_export.json")
        results = self.engine.query_by_type("Planet")
        self.assertTrue(self.engine.export_results(results, path))

    def test_export_creates_file(self):
        path = str(TMP_DIR / "query_export2.json")
        results = self.engine.query_by_type("Planet")
        self.engine.export_results(results, path)
        self.assertTrue(Path(path).exists())

    def test_export_json_structure(self):
        path = str(TMP_DIR / "query_export3.json")
        results = self.engine.query_by_type("Planet")
        self.engine.export_results(results, path)
        data = json.loads(Path(path).read_text())
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["entity_id"], "e1")


# ---------------------------------------------------------------------------
# LayoutEntry dataclass
# ---------------------------------------------------------------------------

class TestLayoutEntryDataclass(unittest.TestCase):
    def test_entity_id(self):
        e = LayoutEntry("ent_1", "Planet", 1.0, 2.0, 3.0)
        self.assertEqual(e.entity_id, "ent_1")

    def test_entity_type(self):
        e = LayoutEntry("ent_1", "Planet", 1.0, 2.0, 3.0)
        self.assertEqual(e.entity_type, "Planet")

    def test_xyz(self):
        e = LayoutEntry("e", "T", 10.0, 20.0, 30.0)
        self.assertEqual(e.x, 10.0)
        self.assertEqual(e.z, 30.0)

    def test_rotation_y_default(self):
        e = LayoutEntry("e", "T", 0.0, 0.0, 0.0)
        self.assertEqual(e.rotation_y, 0.0)

    def test_pcg_seed_default_none(self):
        e = LayoutEntry("e", "T", 0.0, 0.0, 0.0)
        self.assertIsNone(e.pcg_seed)

    def test_metadata_default_empty_dict(self):
        e = LayoutEntry("e", "T", 0.0, 0.0, 0.0)
        self.assertIsInstance(e.metadata, dict)


# ---------------------------------------------------------------------------
# LayoutExportBridge — entry management
# ---------------------------------------------------------------------------

class TestLayoutExportBridgeEntries(unittest.TestCase):
    def setUp(self):
        self.bridge = LayoutExportBridge("layout_test_001")

    def test_init_layout_id(self):
        self.assertEqual(self.bridge.layout_id, "layout_test_001")

    def test_init_version_default(self):
        self.assertEqual(self.bridge.version, "1.0")

    def test_add_entry_returns_layout_entry(self):
        entry = self.bridge.add_entry("e1", "Planet", 0.0, 0.0, 1.0)
        self.assertIsInstance(entry, LayoutEntry)

    def test_add_entry_increments_count(self):
        self.bridge.add_entry("e1", "Planet", 0.0, 0.0, 1.0)
        self.bridge.add_entry("e2", "Station", 0.0, 0.0, 1.2)
        self.assertEqual(self.bridge.get_entry_count(), 2)

    def test_remove_entry_returns_true(self):
        self.bridge.add_entry("e1", "Planet", 0.0, 0.0, 1.0)
        self.assertTrue(self.bridge.remove_entry("e1"))

    def test_remove_entry_decrements_count(self):
        self.bridge.add_entry("e1", "Planet", 0.0, 0.0, 1.0)
        self.bridge.remove_entry("e1")
        self.assertEqual(self.bridge.get_entry_count(), 0)

    def test_remove_missing_entry_returns_false(self):
        self.assertFalse(self.bridge.remove_entry("ghost"))

    def test_get_entries_by_type(self):
        self.bridge.add_entry("e1", "Planet", 0.0, 0.0, 1.0)
        self.bridge.add_entry("e2", "Planet", 0.0, 0.0, 2.0)
        self.bridge.add_entry("e3", "Station", 0.0, 0.0, 1.2)
        planets = self.bridge.get_entries_by_type("Planet")
        self.assertEqual(len(planets), 2)

    def test_clear_removes_all(self):
        self.bridge.add_entry("e1", "Planet", 0.0, 0.0, 1.0)
        self.bridge.clear()
        self.assertEqual(self.bridge.get_entry_count(), 0)


# ---------------------------------------------------------------------------
# LayoutExportBridge — serialisation
# ---------------------------------------------------------------------------

class TestLayoutExportBridgeSerialization(unittest.TestCase):
    def setUp(self):
        self.bridge = LayoutExportBridge("layout_serial_001", version="2.0")
        self.bridge.add_entry("e1", "Planet", 1.0, 0.0, 2.0,
                              rotation_y=45.0, pcg_seed=7)

    def test_to_dict_has_layout_id(self):
        d = self.bridge.to_dict()
        self.assertEqual(d["layout_id"], "layout_serial_001")

    def test_to_dict_has_version(self):
        d = self.bridge.to_dict()
        self.assertEqual(d["version"], "2.0")

    def test_to_dict_entry_count(self):
        d = self.bridge.to_dict()
        self.assertEqual(d["entry_count"], 1)

    def test_to_dict_entries_list(self):
        d = self.bridge.to_dict()
        self.assertIsInstance(d["entries"], list)

    def test_to_dict_entry_fields(self):
        entry = self.bridge.to_dict()["entries"][0]
        self.assertEqual(entry["entity_id"], "e1")
        self.assertEqual(entry["entity_type"], "Planet")
        self.assertEqual(entry["rotation_y"], 45.0)
        self.assertEqual(entry["pcg_seed"], 7)

    def test_to_dict_entry_position(self):
        pos = self.bridge.to_dict()["entries"][0]["position"]
        self.assertEqual(pos["x"], 1.0)
        self.assertEqual(pos["z"], 2.0)

    def test_export_returns_true(self):
        path = str(TMP_DIR / "layout_export.json")
        self.assertTrue(self.bridge.export(path))

    def test_export_creates_file(self):
        path = str(TMP_DIR / "layout_export2.json")
        self.bridge.export(path)
        self.assertTrue(Path(path).exists())

    def test_export_valid_json(self):
        path = str(TMP_DIR / "layout_export3.json")
        self.bridge.export(path)
        data = json.loads(Path(path).read_text())
        self.assertEqual(data["layout_id"], "layout_serial_001")


# ---------------------------------------------------------------------------
# LayoutExportBridge — round-trip load
# ---------------------------------------------------------------------------

class TestLayoutExportBridgeLoad(unittest.TestCase):
    def setUp(self):
        self.src = LayoutExportBridge("layout_roundtrip", version="1.0")
        self.src.add_entry("e1", "Planet", 1.0, 0.0, 2.0)
        self.src.add_entry("e2", "Station", 3.0, 0.0, 4.0)
        self.path = str(TMP_DIR / "layout_roundtrip.json")
        self.src.export(self.path)

    def test_load_returns_count(self):
        dst = LayoutExportBridge("layout_roundtrip_2")
        count = dst.load(self.path)
        self.assertEqual(count, 2)

    def test_load_restores_entries(self):
        dst = LayoutExportBridge("layout_roundtrip_3")
        dst.load(self.path)
        self.assertEqual(dst.get_entry_count(), 2)

    def test_load_preserves_types(self):
        dst = LayoutExportBridge("layout_roundtrip_4")
        dst.load(self.path)
        planets = dst.get_entries_by_type("Planet")
        self.assertEqual(len(planets), 1)

    def test_load_missing_file_returns_zero(self):
        dst = LayoutExportBridge("layout_missing")
        self.assertEqual(dst.load("/nonexistent/path/layout.json"), 0)


# ---------------------------------------------------------------------------
# __init__ exports
# ---------------------------------------------------------------------------

class TestInitExports(unittest.TestCase):
    def test_scene_query_engine_exported(self):
        from AtlasAIEngine.intelligence import SceneQueryEngine as SQE
        self.assertIsNotNone(SQE)

    def test_scene_entity_record_exported(self):
        from AtlasAIEngine.intelligence import SceneEntityRecord as SER
        self.assertIsNotNone(SER)

    def test_layout_export_bridge_exported(self):
        from AtlasAIEngine.intelligence import LayoutExportBridge as LEB
        self.assertIsNotNone(LEB)

    def test_layout_entry_exported(self):
        from AtlasAIEngine.intelligence import LayoutEntry as LE
        self.assertIsNotNone(LE)


if __name__ == "__main__":
    unittest.main()
