"""Phase 19D — Tests for SceneQueryBridge.h and SceneGraphSnapshot."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

from AtlasAIEngine.intelligence import (
    SceneGraphSnapshot,
    SnapshotDiff,
    SceneQueryEngine,
)

TMP_DIR = Path("/tmp/test_phase19d")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# SceneQueryBridge.h tests
# ---------------------------------------------------------------------------

def _sqb() -> str:
    return (SCENE_DIR / "SceneQueryBridge.h").read_text()


class TestSceneQueryBridgeExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SceneQueryBridge.h").exists())


class TestSceneQueryBridgeHeader(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _sqb())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _sqb())

    def test_class_declared(self):
        self.assertIn("class SceneQueryBridge", _sqb())


class TestSceneQueryBridgeAPI(unittest.TestCase):
    def test_add_entity(self):
        self.assertIn("AddEntity", _sqb())

    def test_remove_entity(self):
        self.assertIn("RemoveEntity", _sqb())

    def test_has_entity(self):
        self.assertIn("HasEntity", _sqb())

    def test_get_entity_count(self):
        self.assertIn("GetEntityCount", _sqb())

    def test_query_by_type(self):
        self.assertIn("QueryByType", _sqb())

    def test_query_by_tag(self):
        self.assertIn("QueryByTag", _sqb())

    def test_export_to_json(self):
        self.assertIn("ExportToJson", _sqb())

    def test_export_to_file(self):
        self.assertIn("ExportToFile", _sqb())

    def test_clear(self):
        self.assertIn("Clear", _sqb())

    def test_set_system_id(self):
        self.assertIn("SetSystemId", _sqb())

    def test_get_system_id(self):
        self.assertIn("GetSystemId", _sqb())

    def test_set_on_snapshot_changed(self):
        self.assertIn("SetOnSnapshotChanged", _sqb())


class TestSceneQueryBridgeEntitySnapshot(unittest.TestCase):
    def test_entity_snapshot_struct(self):
        self.assertIn("EntitySnapshot", _sqb())

    def test_entity_id_field(self):
        self.assertIn("entityId", _sqb())

    def test_entity_type_field(self):
        self.assertIn("entityType", _sqb())

    def test_tags_field(self):
        self.assertIn("tags", _sqb())


# ---------------------------------------------------------------------------
# SnapshotDiff dataclass
# ---------------------------------------------------------------------------

class TestSnapshotDiffDataclass(unittest.TestCase):
    def test_added_default_empty(self):
        d = SnapshotDiff()
        self.assertEqual(d.added, [])

    def test_removed_default_empty(self):
        d = SnapshotDiff()
        self.assertEqual(d.removed, [])

    def test_moved_default_empty(self):
        d = SnapshotDiff()
        self.assertEqual(d.moved, [])

    def test_is_empty_when_no_changes(self):
        self.assertTrue(SnapshotDiff().is_empty)

    def test_is_empty_false_when_added(self):
        d = SnapshotDiff(added=["e1"])
        self.assertFalse(d.is_empty)

    def test_total_changes_zero(self):
        self.assertEqual(SnapshotDiff().total_changes(), 0)

    def test_total_changes_sum(self):
        d = SnapshotDiff(added=["a"], removed=["b", "c"], moved=["d"])
        self.assertEqual(d.total_changes(), 4)


# ---------------------------------------------------------------------------
# SceneGraphSnapshot — construction
# ---------------------------------------------------------------------------

def _make_snap_data(system_id: str, entities: list) -> dict:
    return {"system_id": system_id, "entities": entities}


class TestSceneGraphSnapshotFromDict(unittest.TestCase):
    def test_from_dict_creates_snapshot(self):
        data = _make_snap_data("sys_001", [])
        snap = SceneGraphSnapshot.from_dict(data)
        self.assertIsNotNone(snap)

    def test_from_dict_system_id(self):
        data = _make_snap_data("sys_abc", [])
        snap = SceneGraphSnapshot.from_dict(data)
        self.assertEqual(snap.system_id, "sys_abc")

    def test_from_dict_empty_entities(self):
        data = _make_snap_data("sys_001", [])
        snap = SceneGraphSnapshot.from_dict(data)
        self.assertEqual(snap.get_entity_count(), 0)

    def test_from_dict_populates_entities(self):
        entities = [
            {"entity_id": "e1", "entity_type": "Planet", "x": 1.0, "y": 0.0, "z": 2.0},
            {"entity_id": "e2", "entity_type": "Station", "x": 0.0, "y": 0.0, "z": 1.2},
        ]
        snap = SceneGraphSnapshot.from_dict(_make_snap_data("sys_001", entities))
        self.assertEqual(snap.get_entity_count(), 2)

    def test_from_dict_query_by_type(self):
        entities = [
            {"entity_id": "e1", "entity_type": "Planet", "x": 0.0, "y": 0.0, "z": 0.0},
            {"entity_id": "e2", "entity_type": "Station", "x": 0.0, "y": 0.0, "z": 0.0},
        ]
        snap = SceneGraphSnapshot.from_dict(_make_snap_data("sys_001", entities))
        planets = snap.engine.query_by_type("Planet")
        self.assertEqual(len(planets), 1)
        self.assertEqual(planets[0].entity_id, "e1")

    def test_from_dict_tags_loaded(self):
        entities = [
            {"entity_id": "e1", "entity_type": "Planet",
             "x": 0.0, "y": 0.0, "z": 0.0, "tags": ["habitable"]},
        ]
        snap = SceneGraphSnapshot.from_dict(_make_snap_data("sys_001", entities))
        tagged = snap.engine.query_by_tag("habitable")
        self.assertEqual(len(tagged), 1)


# ---------------------------------------------------------------------------
# SceneGraphSnapshot — file I/O
# ---------------------------------------------------------------------------

class TestSceneGraphSnapshotFileIO(unittest.TestCase):
    def _write_snap(self, fname: str, entities: list) -> str:
        path = str(TMP_DIR / fname)
        Path(path).write_text(json.dumps({"system_id": "sys_001", "entities": entities}))
        return path

    def test_from_file_creates_snapshot(self):
        path = self._write_snap("snap_load.json", [])
        snap = SceneGraphSnapshot.from_file(path)
        self.assertIsNotNone(snap)

    def test_from_file_missing_returns_empty(self):
        snap = SceneGraphSnapshot.from_file("/nonexistent/snap.json")
        self.assertEqual(snap.get_entity_count(), 0)

    def test_save_returns_true(self):
        snap = SceneGraphSnapshot.from_dict(_make_snap_data("sys_x", []))
        self.assertTrue(snap.save(str(TMP_DIR / "snap_save.json")))

    def test_save_creates_file(self):
        snap = SceneGraphSnapshot.from_dict(_make_snap_data("sys_x", []))
        path = str(TMP_DIR / "snap_save2.json")
        snap.save(path)
        self.assertTrue(Path(path).exists())

    def test_round_trip_system_id(self):
        snap_in = SceneGraphSnapshot.from_dict(_make_snap_data("round_trip_sys", []))
        path = str(TMP_DIR / "snap_rt.json")
        snap_in.save(path)
        snap_out = SceneGraphSnapshot.from_file(path)
        self.assertEqual(snap_out.system_id, "round_trip_sys")

    def test_to_dict_has_system_id(self):
        snap = SceneGraphSnapshot.from_dict(_make_snap_data("sys_dict", []))
        self.assertEqual(snap.to_dict()["system_id"], "sys_dict")

    def test_to_dict_has_entity_count(self):
        snap = SceneGraphSnapshot.from_dict(_make_snap_data("sys_x", []))
        self.assertIn("entity_count", snap.to_dict())


# ---------------------------------------------------------------------------
# SceneGraphSnapshot — diff
# ---------------------------------------------------------------------------

class TestSceneGraphSnapshotDiff(unittest.TestCase):
    def _snap(self, entities: list) -> SceneGraphSnapshot:
        return SceneGraphSnapshot.from_dict(_make_snap_data("sys_001", entities))

    def test_diff_empty_snapshots(self):
        d = SceneGraphSnapshot.diff(self._snap([]), self._snap([]))
        self.assertTrue(d.is_empty)

    def test_diff_detects_added(self):
        before = self._snap([])
        after = self._snap([{"entity_id": "e1", "entity_type": "Planet",
                              "x": 0.0, "y": 0.0, "z": 0.0}])
        d = SceneGraphSnapshot.diff(before, after)
        self.assertIn("e1", d.added)

    def test_diff_detects_removed(self):
        before = self._snap([{"entity_id": "e1", "entity_type": "Planet",
                               "x": 0.0, "y": 0.0, "z": 0.0}])
        after = self._snap([])
        d = SceneGraphSnapshot.diff(before, after)
        self.assertIn("e1", d.removed)

    def test_diff_detects_moved(self):
        before = self._snap([{"entity_id": "e1", "entity_type": "Planet",
                               "x": 0.0, "y": 0.0, "z": 0.0}])
        after = self._snap([{"entity_id": "e1", "entity_type": "Planet",
                              "x": 10.0, "y": 0.0, "z": 0.0}])
        d = SceneGraphSnapshot.diff(before, after)
        self.assertIn("e1", d.moved)

    def test_diff_no_move_for_unchanged(self):
        ent = {"entity_id": "e1", "entity_type": "Planet",
               "x": 1.0, "y": 0.0, "z": 2.0}
        before = self._snap([ent])
        after = self._snap([ent])
        d = SceneGraphSnapshot.diff(before, after)
        self.assertEqual(d.moved, [])

    def test_diff_total_changes(self):
        before = self._snap([])
        after = self._snap([{"entity_id": "e1", "entity_type": "Planet",
                              "x": 0.0, "y": 0.0, "z": 0.0},
                             {"entity_id": "e2", "entity_type": "Station",
                              "x": 0.0, "y": 0.0, "z": 1.0}])
        d = SceneGraphSnapshot.diff(before, after)
        self.assertEqual(d.total_changes(), 2)


# ---------------------------------------------------------------------------
# __init__ exports
# ---------------------------------------------------------------------------

class TestInitExports(unittest.TestCase):
    def test_scene_graph_snapshot_exported(self):
        from AtlasAIEngine.intelligence import SceneGraphSnapshot as SGS
        self.assertIsNotNone(SGS)

    def test_snapshot_diff_exported(self):
        from AtlasAIEngine.intelligence import SnapshotDiff as SD
        self.assertIsNotNone(SD)


if __name__ == "__main__":
    unittest.main()
