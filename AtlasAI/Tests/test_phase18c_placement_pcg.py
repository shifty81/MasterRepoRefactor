"""Phase 18C — Tests for PlacementPCGBridge and PCGLayoutLearner."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    PlacementPCGBridge,
    PlacementRecord,
    PCGLayoutLearner,
    LayoutSample,
    ClangdBridge,
    SymbolIndex,
    SymbolEntry,
)

TMP_DIR = Path("/tmp/test_phase18c")
TMP_DIR.mkdir(parents=True, exist_ok=True)


class TestPlacementRecordDataclass(unittest.TestCase):
    def test_entity_id_field(self):
        r = PlacementRecord("ent_1", "Station", 1.0, 2.0, 3.0)
        self.assertEqual(r.entity_id, "ent_1")

    def test_entity_type_field(self):
        r = PlacementRecord("ent_1", "Station", 1.0, 2.0, 3.0)
        self.assertEqual(r.entity_type, "Station")

    def test_x_y_z_fields(self):
        r = PlacementRecord("e", "T", 10.0, 20.0, 30.0)
        self.assertEqual(r.x, 10.0)
        self.assertEqual(r.y, 20.0)
        self.assertEqual(r.z, 30.0)

    def test_rotation_y_default(self):
        r = PlacementRecord("e", "T", 0.0, 0.0, 0.0)
        self.assertEqual(r.rotation_y, 0.0)

    def test_rotation_y_set(self):
        r = PlacementRecord("e", "T", 0.0, 0.0, 0.0, rotation_y=45.0)
        self.assertEqual(r.rotation_y, 45.0)

    def test_pcg_seed_default_none(self):
        r = PlacementRecord("e", "T", 0.0, 0.0, 0.0)
        self.assertIsNone(r.pcg_seed)

    def test_pcg_seed_set(self):
        r = PlacementRecord("e", "T", 0.0, 0.0, 0.0, pcg_seed=99)
        self.assertEqual(r.pcg_seed, 99)

    def test_approved_default_false(self):
        r = PlacementRecord("e", "T", 0.0, 0.0, 0.0)
        self.assertFalse(r.approved)

    def test_approved_can_be_set(self):
        r = PlacementRecord("e", "T", 0.0, 0.0, 0.0, approved=True)
        self.assertTrue(r.approved)


class TestPlacementPCGBridgeInit(unittest.TestCase):
    def test_init_with_content_root(self):
        bridge = PlacementPCGBridge(str(TMP_DIR))
        self.assertIsNotNone(bridge)

    def test_content_root_is_path(self):
        bridge = PlacementPCGBridge(str(TMP_DIR))
        self.assertIsInstance(bridge.content_root, Path)


class TestPlacementPCGBridgeRecordApprove(unittest.TestCase):
    def setUp(self):
        self.bridge = PlacementPCGBridge(str(TMP_DIR))

    def test_record_placement_returns_string(self):
        pid = self.bridge.record_placement("e1", "Planet", 0.0, 0.0, 0.0)
        self.assertIsInstance(pid, str)

    def test_record_placement_id_format(self):
        pid = self.bridge.record_placement("e1", "Planet", 0.0, 0.0, 0.0)
        self.assertTrue(pid.startswith("placement_"))

    def test_multiple_records_unique_ids(self):
        ids = {self.bridge.record_placement("e", "T", 0, 0, 0) for _ in range(5)}
        self.assertEqual(len(ids), 5)

    def test_approve_placement_returns_true(self):
        pid = self.bridge.record_placement("e1", "Station", 0.0, 0.0, 0.0)
        self.assertTrue(self.bridge.approve_placement(pid))

    def test_approve_missing_returns_false(self):
        self.assertFalse(self.bridge.approve_placement("nonexistent"))

    def test_reject_placement_returns_true(self):
        pid = self.bridge.record_placement("e2", "Moon", 0.0, 0.0, 0.0)
        self.assertTrue(self.bridge.reject_placement(pid))

    def test_reject_missing_returns_false(self):
        self.assertFalse(self.bridge.reject_placement("nonexistent"))


class TestPlacementPCGBridgeQueries(unittest.TestCase):
    def setUp(self):
        self.bridge = PlacementPCGBridge(str(TMP_DIR))
        self.pid1 = self.bridge.record_placement("e1", "Station", 0.0, 0.0, 0.0)
        self.pid2 = self.bridge.record_placement("e2", "Planet", 1.0, 0.0, 0.0)
        self.bridge.approve_placement(self.pid1)

    def test_get_approved_placements(self):
        approved = self.bridge.get_approved_placements()
        self.assertEqual(len(approved), 1)
        self.assertEqual(approved[0].entity_id, "e1")

    def test_get_pending_placements(self):
        pending = self.bridge.get_pending_placements()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].entity_id, "e2")

    def test_get_stats_keys(self):
        stats = self.bridge.get_stats()
        self.assertIn("total", stats)
        self.assertIn("approved", stats)
        self.assertIn("pending", stats)

    def test_get_stats_values(self):
        stats = self.bridge.get_stats()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["approved"], 1)
        self.assertEqual(stats["pending"], 1)

    def test_clear_removes_all(self):
        self.bridge.clear()
        self.assertEqual(self.bridge.get_stats()["total"], 0)


class TestPlacementPCGBridgeExport(unittest.TestCase):
    def setUp(self):
        self.bridge = PlacementPCGBridge(str(TMP_DIR))
        pid = self.bridge.record_placement("ent_x", "Stargate", 5.0, 0.0, 0.0,
                                           rotation_y=90.0, pcg_seed=77)
        self.bridge.approve_placement(pid)

    def test_export_approved_layout_returns_path(self):
        out = self.bridge.export_approved_layout("test_layout_18c.json")
        self.assertIsInstance(out, Path)

    def test_export_approved_layout_file_written(self):
        out = self.bridge.export_approved_layout("test_layout_18c_2.json")
        self.assertTrue(out.exists())

    def test_export_approved_layout_json_valid(self):
        out = self.bridge.export_approved_layout("test_layout_18c_3.json")
        data = json.loads(out.read_text())
        self.assertIn("placements", data)
        self.assertEqual(len(data["placements"]), 1)

    def test_export_layout_id_from_filename(self):
        out = self.bridge.export_approved_layout("my_layout.json")
        data = json.loads(out.read_text())
        self.assertEqual(data["layout_id"], "my_layout")


class TestPCGLayoutLearner(unittest.TestCase):
    def setUp(self):
        self.learner = PCGLayoutLearner()

    def test_ingest_missing_file_returns_false(self):
        self.assertFalse(self.learner.ingest("/nonexistent/path/layout.json"))

    def test_get_sample_count_initial(self):
        self.assertEqual(self.learner.get_sample_count(), 0)

    def test_compute_baseline_empty_returns_empty_dict(self):
        self.assertEqual(self.learner.compute_baseline(), {})

    def test_get_entity_types_initial_empty(self):
        self.assertEqual(self.learner.get_entity_types(), [])

    def test_ingest_valid_file(self):
        layout_file = TMP_DIR / "learner_layout.json"
        layout = {
            "layout_id": "learner_test",
            "placements": [
                {"entity_id": "e1", "entity_type": "Station"},
                {"entity_id": "e2", "entity_type": "Station"},
                {"entity_id": "e3", "entity_type": "Planet"},
            ],
        }
        layout_file.write_text(json.dumps(layout))
        result = self.learner.ingest(str(layout_file))
        self.assertTrue(result)

    def test_get_sample_count_after_ingest(self):
        layout_file = TMP_DIR / "learner_layout2.json"
        layout = {"layout_id": "l2", "placements": [{"entity_id": "e1", "entity_type": "Moon"}]}
        layout_file.write_text(json.dumps(layout))
        self.learner.ingest(str(layout_file))
        self.assertEqual(self.learner.get_sample_count(), 1)

    def test_compute_baseline_after_ingest(self):
        layout_file = TMP_DIR / "learner_layout3.json"
        layout = {
            "layout_id": "l3",
            "placements": [{"entity_id": "e1", "entity_type": "Asteroid"}],
        }
        layout_file.write_text(json.dumps(layout))
        self.learner.ingest(str(layout_file))
        baseline = self.learner.compute_baseline()
        self.assertIn("sample_count", baseline)
        self.assertEqual(baseline["sample_count"], 1)

    def test_get_entity_types_after_ingest(self):
        layout_file = TMP_DIR / "learner_layout4.json"
        layout = {
            "layout_id": "l4",
            "placements": [{"entity_id": "e1", "entity_type": "Wormhole"}],
        }
        layout_file.write_text(json.dumps(layout))
        self.learner.ingest(str(layout_file))
        self.assertIn("Wormhole", self.learner.get_entity_types())

    def test_clear_resets_samples(self):
        layout_file = TMP_DIR / "learner_layout5.json"
        layout = {"layout_id": "l5", "placements": [{"entity_id": "e1", "entity_type": "X"}]}
        layout_file.write_text(json.dumps(layout))
        self.learner.ingest(str(layout_file))
        self.learner.clear()
        self.assertEqual(self.learner.get_sample_count(), 0)

    def test_export_baseline_creates_file(self):
        layout_file = TMP_DIR / "learner_export_input.json"
        layout = {
            "layout_id": "export_test",
            "placements": [{"entity_id": "e1", "entity_type": "Station"}],
        }
        layout_file.write_text(json.dumps(layout))
        self.learner.ingest(str(layout_file))
        config_path = str(TMP_DIR / "pcg_config_out.json")
        result = self.learner.export_baseline(config_path)
        self.assertTrue(result)
        self.assertTrue(Path(config_path).exists())


class TestLayoutSampleDataclass(unittest.TestCase):
    def test_layout_sample_layout_id(self):
        s = LayoutSample(layout_id="test_id")
        self.assertEqual(s.layout_id, "test_id")

    def test_layout_sample_defaults(self):
        s = LayoutSample(layout_id="x")
        self.assertEqual(s.average_spacing, 0.0)
        self.assertEqual(s.placement_count, 0)
        self.assertIsInstance(s.entity_type_counts, dict)


class TestIntelligenceInitExports(unittest.TestCase):
    def test_placement_pcg_bridge_exported(self):
        from AtlasAIEngine.intelligence import PlacementPCGBridge as PPB
        self.assertIsNotNone(PPB)

    def test_placement_record_exported(self):
        from AtlasAIEngine.intelligence import PlacementRecord as PR
        self.assertIsNotNone(PR)

    def test_pcg_layout_learner_exported(self):
        from AtlasAIEngine.intelligence import PCGLayoutLearner as PLL
        self.assertIsNotNone(PLL)

    def test_layout_sample_exported(self):
        from AtlasAIEngine.intelligence import LayoutSample as LS
        self.assertIsNotNone(LS)

    def test_clangd_bridge_still_exported(self):
        from AtlasAIEngine.intelligence import ClangdBridge as CB
        self.assertIsNotNone(CB)

    def test_symbol_index_still_exported(self):
        from AtlasAIEngine.intelligence import SymbolIndex as SI
        self.assertIsNotNone(SI)


if __name__ == "__main__":
    unittest.main()
