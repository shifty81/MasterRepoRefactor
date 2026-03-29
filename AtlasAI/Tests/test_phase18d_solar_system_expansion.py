"""Phase 18D — Tests for Solar System Expansion + DeltaEditStore."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import DeltaEditStore, DeltaEdit

TMP_DIR = Path("/tmp/test_phase18d")
TMP_DIR.mkdir(parents=True, exist_ok=True)

DEV_SOLAR = (
    REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems" / "dev_solar_system.json"
)
BRIDGE_H = REPO_ROOT / "Atlas" / "Engine" / "Scene" / "SolarSystemEditorBridge.h"


class TestDevSolarSystemJSON(unittest.TestCase):
    def _data(self):
        return json.loads(DEV_SOLAR.read_text())

    def test_file_exists(self):
        self.assertTrue(DEV_SOLAR.exists())

    def test_has_at_least_8_celestials(self):
        data = self._data()
        self.assertGreaterEqual(len(data["celestials"]), 8)

    def test_total_celestials_field(self):
        data = self._data()
        self.assertEqual(data.get("total_celestials"), 8)

    def test_ship_spawn_points_field(self):
        data = self._data()
        self.assertEqual(data.get("ship_spawn_points"), 1)

    def test_moon_type_present(self):
        data = self._data()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Moon", types)

    def test_stargate_type_present(self):
        data = self._data()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Stargate", types)

    def test_ship_spawn_point_type_present(self):
        data = self._data()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("ShipSpawnPoint", types)

    def test_moon_id_is_moon_001(self):
        data = self._data()
        ids = [c["id"] for c in data["celestials"]]
        self.assertIn("moon_001", ids)

    def test_stargate_id_is_stargate_001(self):
        data = self._data()
        ids = [c["id"] for c in data["celestials"]]
        self.assertIn("stargate_001", ids)

    def test_ship_spawn_id_is_ship_spawn_001(self):
        data = self._data()
        ids = [c["id"] for c in data["celestials"]]
        self.assertIn("ship_spawn_001", ids)

    def test_moon_has_parent(self):
        data = self._data()
        moon = next(c for c in data["celestials"] if c["id"] == "moon_001")
        self.assertEqual(moon.get("parent"), "planet_001")

    def test_stargate_has_destination_system(self):
        data = self._data()
        gate = next(c for c in data["celestials"] if c["id"] == "stargate_001")
        self.assertIn("destination_system", gate)

    def test_ship_spawn_has_max_ships(self):
        data = self._data()
        spawn = next(c for c in data["celestials"] if c["id"] == "ship_spawn_001")
        self.assertEqual(spawn.get("max_ships"), 5)

    def test_original_5_celestials_still_present(self):
        data = self._data()
        ids = {c["id"] for c in data["celestials"]}
        for original_id in ["planet_001", "station_001", "asteroid_belt_001",
                             "wormhole_001", "anomaly_001"]:
            self.assertIn(original_id, ids)


class TestSolarSystemEditorBridgeHeader(unittest.TestCase):
    def _content(self):
        return BRIDGE_H.read_text()

    def test_file_exists(self):
        self.assertTrue(BRIDGE_H.exists())

    def test_pragma_once(self):
        self.assertIn("#pragma once", self._content())

    def test_class_name(self):
        self.assertIn("class SolarSystemEditorBridge", self._content())

    def test_edit_record_struct(self):
        self.assertIn("struct EditRecord", self._content())

    def test_set_active_system(self):
        self.assertIn("SetActiveSystem", self._content())

    def test_select_entity(self):
        self.assertIn("SelectEntity", self._content())

    def test_edit_property(self):
        self.assertIn("EditProperty", self._content())

    def test_move_entity(self):
        self.assertIn("MoveEntity", self._content())

    def test_undo_last_edit(self):
        self.assertIn("UndoLastEdit", self._content())

    def test_propagate_edits_to_baseline(self):
        self.assertIn("PropagateEditsToBaseline", self._content())

    def test_namespace_atlas_engine(self):
        self.assertIn("namespace Atlas::Engine", self._content())


class TestDeltaEditDataclass(unittest.TestCase):
    def test_edit_id_field(self):
        e = DeltaEdit("edit_0", "ent_1", "pos.x", 0.0, 1.0)
        self.assertEqual(e.edit_id, "edit_0")

    def test_entity_id_field(self):
        e = DeltaEdit("edit_0", "ent_1", "pos.x", 0.0, 1.0)
        self.assertEqual(e.entity_id, "ent_1")

    def test_property_name_field(self):
        e = DeltaEdit("edit_0", "ent_1", "pos.x", 0.0, 1.0)
        self.assertEqual(e.property_name, "pos.x")

    def test_old_value_field(self):
        e = DeltaEdit("edit_0", "ent_1", "pos.x", 0.0, 1.0)
        self.assertEqual(e.old_value, 0.0)

    def test_new_value_field(self):
        e = DeltaEdit("edit_0", "ent_1", "pos.x", 0.0, 1.0)
        self.assertEqual(e.new_value, 1.0)

    def test_committed_default_false(self):
        e = DeltaEdit("edit_0", "ent_1", "pos.x", 0.0, 1.0)
        self.assertFalse(e.committed)

    def test_session_id_default(self):
        e = DeltaEdit("edit_0", "ent_1", "pos.x", 0.0, 1.0)
        self.assertEqual(e.session_id, "default")


class TestDeltaEditStoreBasic(unittest.TestCase):
    def setUp(self):
        self.store = DeltaEditStore()

    def test_record_returns_string(self):
        eid = self.store.record("ent_1", "pos.x", 0.0, 5.0)
        self.assertIsInstance(eid, str)

    def test_record_id_format(self):
        eid = self.store.record("ent_1", "pos.x", 0.0, 5.0)
        self.assertTrue(eid.startswith("edit_"))

    def test_multiple_records_unique_ids(self):
        ids = {self.store.record("e", "p", 0, i) for i in range(5)}
        self.assertEqual(len(ids), 5)

    def test_commit_returns_true(self):
        eid = self.store.record("e", "p", 0.0, 1.0)
        self.assertTrue(self.store.commit(eid))

    def test_commit_missing_returns_false(self):
        self.assertFalse(self.store.commit("nonexistent"))

    def test_rollback_uncommitted(self):
        eid = self.store.record("e", "p", 0.0, 1.0)
        self.assertTrue(self.store.rollback(eid))

    def test_rollback_committed_returns_false(self):
        eid = self.store.record("e", "p", 0.0, 1.0)
        self.store.commit(eid)
        self.assertFalse(self.store.rollback(eid))

    def test_rollback_missing_returns_false(self):
        self.assertFalse(self.store.rollback("nonexistent"))


class TestDeltaEditStoreQueries(unittest.TestCase):
    def setUp(self):
        self.store = DeltaEditStore()
        self.eid1 = self.store.record("ent_A", "pos.x", 0.0, 1.0)
        self.eid2 = self.store.record("ent_A", "pos.y", 0.0, 2.0)
        self.eid3 = self.store.record("ent_B", "scale", 1.0, 2.0)
        self.store.commit(self.eid1)

    def test_get_committed(self):
        committed = self.store.get_committed()
        self.assertEqual(len(committed), 1)
        self.assertEqual(committed[0].edit_id, self.eid1)

    def test_get_pending(self):
        pending = self.store.get_pending()
        self.assertEqual(len(pending), 2)

    def test_get_by_entity(self):
        edits = self.store.get_by_entity("ent_A")
        self.assertEqual(len(edits), 2)

    def test_get_by_entity_other(self):
        edits = self.store.get_by_entity("ent_B")
        self.assertEqual(len(edits), 1)

    def test_get_stats_keys(self):
        stats = self.store.get_stats()
        self.assertIn("total", stats)
        self.assertIn("committed", stats)
        self.assertIn("pending", stats)

    def test_get_stats_values(self):
        stats = self.store.get_stats()
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["committed"], 1)
        self.assertEqual(stats["pending"], 2)

    def test_clear_removes_all(self):
        self.store.clear()
        self.assertEqual(self.store.get_stats()["total"], 0)


class TestDeltaEditStorePersistence(unittest.TestCase):
    def setUp(self):
        self.store = DeltaEditStore()
        eid = self.store.record("ent_persist", "name", "old_name", "new_name", "sess_1")
        self.store.commit(eid)

    def test_save_returns_true(self):
        path = str(TMP_DIR / "delta_edits_save.json")
        self.assertTrue(self.store.save(path))

    def test_save_creates_file(self):
        path = str(TMP_DIR / "delta_edits_save2.json")
        self.store.save(path)
        self.assertTrue(Path(path).exists())

    def test_load_returns_count(self):
        path = str(TMP_DIR / "delta_edits_load.json")
        self.store.save(path)
        store2 = DeltaEditStore()
        count = store2.load(path)
        self.assertEqual(count, 1)

    def test_load_restores_committed(self):
        path = str(TMP_DIR / "delta_edits_committed.json")
        self.store.save(path)
        store2 = DeltaEditStore()
        store2.load(path)
        committed = store2.get_committed()
        self.assertEqual(len(committed), 1)

    def test_load_missing_file_returns_zero(self):
        store2 = DeltaEditStore()
        self.assertEqual(store2.load("/nonexistent/file.json"), 0)


class TestInitExportsDeltaEdit(unittest.TestCase):
    def test_delta_edit_store_exported(self):
        from AtlasAIEngine.intelligence import DeltaEditStore as DES
        self.assertIsNotNone(DES)

    def test_delta_edit_exported(self):
        from AtlasAIEngine.intelligence import DeltaEdit as DE
        self.assertIsNotNone(DE)


if __name__ == "__main__":
    unittest.main()
