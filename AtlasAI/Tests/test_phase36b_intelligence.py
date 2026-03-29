"""Phase 36B — Tests for AbilityDebugPipeline and LandscapeSplinePipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    AbilityDebugPipeline,
    AbilitySnapshot,
    AttributeRecord,
    AbilityDebugFrame,
    LandscapeSplinePipeline,
    SplinePointDef,
    SplineSegmentDef,
    LandscapeSplineEntry,
)


# ---------------------------------------------------------------------------
# AbilitySnapshot
# ---------------------------------------------------------------------------

class TestAbilitySnapshot(unittest.TestCase):
    def test_snapshot_id(self):
        s = AbilitySnapshot(snapshot_id="snap_001", ability_id="ab_001", ability_name="Fireball")
        self.assertEqual(s.snapshot_id, "snap_001")

    def test_ability_name(self):
        s = AbilitySnapshot(snapshot_id="snap_001", ability_id="ab_001", ability_name="Fireball")
        self.assertEqual(s.ability_name, "Fireball")

    def test_default_activation_state(self):
        s = AbilitySnapshot(snapshot_id="snap_001", ability_id="ab_001", ability_name="Fireball")
        self.assertEqual(s.activation_state, "Inactive")

    def test_is_active_false(self):
        s = AbilitySnapshot(snapshot_id="snap_001", ability_id="ab_001", ability_name="Fireball")
        self.assertFalse(s.is_active)

    def test_is_active_true(self):
        s = AbilitySnapshot(snapshot_id="snap_001", ability_id="ab_001", ability_name="Fireball",
                            activation_state="Active")
        self.assertTrue(s.is_active)

    def test_is_on_cooldown_false(self):
        s = AbilitySnapshot(snapshot_id="snap_001", ability_id="ab_001", ability_name="Fireball")
        self.assertFalse(s.is_on_cooldown)

    def test_is_on_cooldown_true(self):
        s = AbilitySnapshot(snapshot_id="snap_001", ability_id="ab_001", ability_name="Fireball",
                            cooldown_remaining=2.5)
        self.assertTrue(s.is_on_cooldown)

    def test_has_tags_false(self):
        s = AbilitySnapshot(snapshot_id="snap_001", ability_id="ab_001", ability_name="Fireball")
        self.assertFalse(s.has_tags)

    def test_has_tags_true(self):
        s = AbilitySnapshot(snapshot_id="snap_001", ability_id="ab_001", ability_name="Fireball",
                            tags=["fire", "aoe"])
        self.assertTrue(s.has_tags)


# ---------------------------------------------------------------------------
# AttributeRecord
# ---------------------------------------------------------------------------

class TestAttributeRecord(unittest.TestCase):
    def test_record_id(self):
        r = AttributeRecord(record_id="rec_001", owner_id="owner_001", attribute_name="Health")
        self.assertEqual(r.record_id, "rec_001")

    def test_attribute_name(self):
        r = AttributeRecord(record_id="rec_001", owner_id="owner_001", attribute_name="Health")
        self.assertEqual(r.attribute_name, "Health")

    def test_default_base_value(self):
        r = AttributeRecord(record_id="rec_001", owner_id="owner_001", attribute_name="Health")
        self.assertEqual(r.base_value, 0.0)

    def test_is_maxed_false(self):
        r = AttributeRecord(record_id="rec_001", owner_id="owner_001", attribute_name="Health",
                            current_value=50.0)
        self.assertFalse(r.is_maxed)

    def test_is_maxed_true(self):
        r = AttributeRecord(record_id="rec_001", owner_id="owner_001", attribute_name="Health",
                            current_value=100.0, max_value=100.0)
        self.assertTrue(r.is_maxed)

    def test_is_depleted_false(self):
        r = AttributeRecord(record_id="rec_001", owner_id="owner_001", attribute_name="Health",
                            current_value=10.0)
        self.assertFalse(r.is_depleted)

    def test_is_depleted_true(self):
        r = AttributeRecord(record_id="rec_001", owner_id="owner_001", attribute_name="Health",
                            current_value=0.0, min_value=0.0)
        self.assertTrue(r.is_depleted)

    def test_has_modifiers_false(self):
        r = AttributeRecord(record_id="rec_001", owner_id="owner_001", attribute_name="Health")
        self.assertFalse(r.has_modifiers)

    def test_has_modifiers_true(self):
        r = AttributeRecord(record_id="rec_001", owner_id="owner_001", attribute_name="Health",
                            modifiers=["mod_001"])
        self.assertTrue(r.has_modifiers)


# ---------------------------------------------------------------------------
# AbilityDebugFrame
# ---------------------------------------------------------------------------

class TestAbilityDebugFrame(unittest.TestCase):
    def test_frame_id(self):
        f = AbilityDebugFrame(frame_id="frame_001")
        self.assertEqual(f.frame_id, "frame_001")

    def test_default_timestamp(self):
        f = AbilityDebugFrame(frame_id="frame_001")
        self.assertEqual(f.timestamp, 0.0)

    def test_has_snapshots_false(self):
        f = AbilityDebugFrame(frame_id="frame_001")
        self.assertFalse(f.has_snapshots)

    def test_has_snapshots_true(self):
        f = AbilityDebugFrame(frame_id="frame_001", snapshots=["snap_001"])
        self.assertTrue(f.has_snapshots)

    def test_has_attributes_false(self):
        f = AbilityDebugFrame(frame_id="frame_001")
        self.assertFalse(f.has_attributes)

    def test_has_attributes_true(self):
        f = AbilityDebugFrame(frame_id="frame_001", attributes=["rec_001"])
        self.assertTrue(f.has_attributes)


# ---------------------------------------------------------------------------
# AbilityDebugPipeline
# ---------------------------------------------------------------------------

class TestAbilityDebugPipeline(unittest.TestCase):
    def _pipeline(self):
        return AbilityDebugPipeline()

    def _snapshot(self, sid="snap_001", owner="owner_001"):
        return AbilitySnapshot(snapshot_id=sid, ability_id="ab_001",
                               ability_name="Fireball", owner_id=owner)

    def _attribute(self, rid="rec_001", owner="owner_001"):
        return AttributeRecord(record_id=rid, owner_id=owner, attribute_name="Health")

    def test_add_snapshot(self):
        pipe = self._pipeline()
        pipe.add_snapshot(self._snapshot())
        self.assertIsNotNone(pipe.get_snapshot("snap_001"))

    def test_remove_snapshot(self):
        pipe = self._pipeline()
        pipe.add_snapshot(self._snapshot())
        self.assertTrue(pipe.remove_snapshot("snap_001"))
        self.assertIsNone(pipe.get_snapshot("snap_001"))

    def test_get_all_snapshots(self):
        pipe = self._pipeline()
        pipe.add_snapshot(self._snapshot("snap_001"))
        pipe.add_snapshot(self._snapshot("snap_002"))
        self.assertEqual(len(pipe.get_all_snapshots()), 2)

    def test_add_attribute(self):
        pipe = self._pipeline()
        pipe.add_attribute(self._attribute())
        self.assertIsNotNone(pipe.get_attribute("rec_001"))

    def test_remove_attribute(self):
        pipe = self._pipeline()
        pipe.add_attribute(self._attribute())
        self.assertTrue(pipe.remove_attribute("rec_001"))
        self.assertIsNone(pipe.get_attribute("rec_001"))

    def test_get_attributes_by_owner(self):
        pipe = self._pipeline()
        pipe.add_attribute(self._attribute("rec_001", "owner_001"))
        pipe.add_attribute(self._attribute("rec_002", "owner_001"))
        pipe.add_attribute(self._attribute("rec_003", "owner_002"))
        self.assertEqual(len(pipe.get_attributes_by_owner("owner_001")), 2)

    def test_get_snapshots_by_owner(self):
        pipe = self._pipeline()
        pipe.add_snapshot(self._snapshot("snap_001", "owner_001"))
        pipe.add_snapshot(self._snapshot("snap_002", "owner_002"))
        self.assertEqual(len(pipe.get_snapshots_by_owner("owner_001")), 1)

    def test_get_active_snapshots(self):
        pipe = self._pipeline()
        snap = AbilitySnapshot(snapshot_id="snap_001", ability_id="ab_001",
                               ability_name="Fireball", activation_state="Active")
        pipe.add_snapshot(snap)
        pipe.add_snapshot(self._snapshot("snap_002"))
        self.assertEqual(len(pipe.get_active_snapshots()), 1)

    def test_get_cooldown_snapshots(self):
        pipe = self._pipeline()
        snap = AbilitySnapshot(snapshot_id="snap_001", ability_id="ab_001",
                               ability_name="Fireball", cooldown_remaining=3.0)
        pipe.add_snapshot(snap)
        pipe.add_snapshot(self._snapshot("snap_002"))
        self.assertEqual(len(pipe.get_cooldown_snapshots()), 1)

    def test_record_frame(self):
        pipe = self._pipeline()
        frame = AbilityDebugFrame(frame_id="frame_001")
        pipe.record_frame(frame)
        self.assertIsNotNone(pipe.get_frame("frame_001"))

    def test_get_all_frames(self):
        pipe = self._pipeline()
        pipe.record_frame(AbilityDebugFrame(frame_id="frame_001"))
        pipe.record_frame(AbilityDebugFrame(frame_id="frame_002"))
        self.assertEqual(len(pipe.get_all_frames()), 2)

    def test_clear_frames(self):
        pipe = self._pipeline()
        pipe.record_frame(AbilityDebugFrame(frame_id="frame_001"))
        pipe.clear_frames()
        self.assertEqual(len(pipe.get_all_frames()), 0)

    def test_validate(self):
        pipe = self._pipeline()
        frame = AbilityDebugFrame(frame_id="frame_001")
        self.assertTrue(pipe.validate(frame))

    def test_snapshot_count(self):
        pipe = self._pipeline()
        self.assertEqual(pipe.snapshot_count, 0)
        pipe.add_snapshot(self._snapshot())
        self.assertEqual(pipe.snapshot_count, 1)

    def test_is_empty(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.is_empty)
        pipe.add_snapshot(self._snapshot())
        self.assertFalse(pipe.is_empty)

    def test_clear(self):
        pipe = self._pipeline()
        pipe.add_snapshot(self._snapshot())
        pipe.add_attribute(self._attribute())
        pipe.clear()
        self.assertTrue(pipe.is_empty)


# ---------------------------------------------------------------------------
# SplinePointDef
# ---------------------------------------------------------------------------

class TestSplinePointDef(unittest.TestCase):
    def test_point_id(self):
        p = SplinePointDef(point_id="pt_001")
        self.assertEqual(p.point_id, "pt_001")

    def test_default_position(self):
        p = SplinePointDef(point_id="pt_001")
        self.assertEqual(p.position_x, 0.0)
        self.assertEqual(p.position_y, 0.0)
        self.assertEqual(p.position_z, 0.0)

    def test_is_at_origin_true(self):
        p = SplinePointDef(point_id="pt_001")
        self.assertTrue(p.is_at_origin)

    def test_is_at_origin_false(self):
        p = SplinePointDef(point_id="pt_001", position_x=100.0)
        self.assertFalse(p.is_at_origin)

    def test_has_weight_false(self):
        p = SplinePointDef(point_id="pt_001")
        self.assertFalse(p.has_weight)

    def test_has_weight_true(self):
        p = SplinePointDef(point_id="pt_001", tangent_weight=2.0)
        self.assertTrue(p.has_weight)


# ---------------------------------------------------------------------------
# SplineSegmentDef
# ---------------------------------------------------------------------------

class TestSplineSegmentDef(unittest.TestCase):
    def test_segment_id(self):
        s = SplineSegmentDef(segment_id="seg_001", start_point_id="pt_001",
                             end_point_id="pt_002")
        self.assertEqual(s.segment_id, "seg_001")

    def test_default_width(self):
        s = SplineSegmentDef(segment_id="seg_001", start_point_id="pt_001",
                             end_point_id="pt_002")
        self.assertEqual(s.width, 200.0)

    def test_has_mesh_false(self):
        s = SplineSegmentDef(segment_id="seg_001", start_point_id="pt_001",
                             end_point_id="pt_002")
        self.assertFalse(s.has_mesh)

    def test_has_mesh_true(self):
        s = SplineSegmentDef(segment_id="seg_001", start_point_id="pt_001",
                             end_point_id="pt_002", mesh_id="mesh_001")
        self.assertTrue(s.has_mesh)

    def test_has_layers_false(self):
        s = SplineSegmentDef(segment_id="seg_001", start_point_id="pt_001",
                             end_point_id="pt_002")
        self.assertFalse(s.has_layers)

    def test_has_layers_true(self):
        s = SplineSegmentDef(segment_id="seg_001", start_point_id="pt_001",
                             end_point_id="pt_002", layers=["layer_001"])
        self.assertTrue(s.has_layers)


# ---------------------------------------------------------------------------
# LandscapeSplineEntry
# ---------------------------------------------------------------------------

class TestLandscapeSplineEntry(unittest.TestCase):
    def test_spline_id(self):
        e = LandscapeSplineEntry(spline_id="spline_001", spline_name="Road 1")
        self.assertEqual(e.spline_id, "spline_001")

    def test_spline_name(self):
        e = LandscapeSplineEntry(spline_id="spline_001", spline_name="Road 1")
        self.assertEqual(e.spline_name, "Road 1")

    def test_is_empty_true(self):
        e = LandscapeSplineEntry(spline_id="spline_001", spline_name="Road 1")
        self.assertTrue(e.is_empty)

    def test_is_empty_false(self):
        e = LandscapeSplineEntry(spline_id="spline_001", spline_name="Road 1",
                                 points=["pt_001"])
        self.assertFalse(e.is_empty)

    def test_is_enabled_true(self):
        e = LandscapeSplineEntry(spline_id="spline_001", spline_name="Road 1")
        self.assertTrue(e.is_enabled)

    def test_has_segments_false(self):
        e = LandscapeSplineEntry(spline_id="spline_001", spline_name="Road 1")
        self.assertFalse(e.has_segments)

    def test_has_segments_true(self):
        e = LandscapeSplineEntry(spline_id="spline_001", spline_name="Road 1",
                                 segments=["seg_001"])
        self.assertTrue(e.has_segments)


# ---------------------------------------------------------------------------
# LandscapeSplinePipeline
# ---------------------------------------------------------------------------

class TestLandscapeSplinePipeline(unittest.TestCase):
    def _pipeline(self):
        return LandscapeSplinePipeline()

    def _spline(self, sid="spline_001"):
        return LandscapeSplineEntry(spline_id=sid, spline_name=f"Road {sid}")

    def _point(self, pid="pt_001"):
        return SplinePointDef(point_id=pid)

    def _segment(self, seg_id="seg_001"):
        return SplineSegmentDef(segment_id=seg_id, start_point_id="pt_001",
                                end_point_id="pt_002")

    def test_add_spline(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline())
        self.assertIsNotNone(pipe.get_spline("spline_001"))

    def test_remove_spline(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline())
        self.assertTrue(pipe.remove_spline("spline_001"))
        self.assertIsNone(pipe.get_spline("spline_001"))

    def test_get_all_splines(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline("spline_001"))
        pipe.add_spline(self._spline("spline_002"))
        self.assertEqual(len(pipe.get_all_splines()), 2)

    def test_add_point(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline())
        self.assertTrue(pipe.add_point("spline_001", self._point()))
        spline = pipe.get_spline("spline_001")
        self.assertIn("pt_001", spline.points)

    def test_remove_point(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline())
        pipe.add_point("spline_001", self._point())
        self.assertTrue(pipe.remove_point("spline_001", "pt_001"))

    def test_add_segment(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline())
        self.assertTrue(pipe.add_segment("spline_001", self._segment()))
        spline = pipe.get_spline("spline_001")
        self.assertIn("seg_001", spline.segments)

    def test_remove_segment(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline())
        pipe.add_segment("spline_001", self._segment())
        self.assertTrue(pipe.remove_segment("spline_001", "seg_001"))

    def test_set_enabled(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline())
        self.assertTrue(pipe.set_enabled("spline_001", False))
        spline = pipe.get_spline("spline_001")
        self.assertFalse(spline.is_enabled)

    def test_get_enabled_splines(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline("spline_001"))
        pipe.add_spline(self._spline("spline_002"))
        pipe.set_enabled("spline_002", False)
        self.assertEqual(len(pipe.get_enabled_splines()), 1)

    def test_get_disabled_splines(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline("spline_001"))
        pipe.set_enabled("spline_001", False)
        self.assertEqual(len(pipe.get_disabled_splines()), 1)

    def test_get_points_for_spline(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline())
        pipe.add_point("spline_001", self._point("pt_001"))
        pipe.add_point("spline_001", self._point("pt_002"))
        self.assertEqual(len(pipe.get_points_for_spline("spline_001")), 2)

    def test_get_segments_for_spline(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline())
        pipe.add_segment("spline_001", self._segment("seg_001"))
        self.assertEqual(len(pipe.get_segments_for_spline("spline_001")), 1)

    def test_validate(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.validate(self._spline()))

    def test_spline_count(self):
        pipe = self._pipeline()
        self.assertEqual(pipe.spline_count, 0)
        pipe.add_spline(self._spline())
        self.assertEqual(pipe.spline_count, 1)

    def test_is_empty(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.is_empty)
        pipe.add_spline(self._spline())
        self.assertFalse(pipe.is_empty)

    def test_clear(self):
        pipe = self._pipeline()
        pipe.add_spline(self._spline())
        pipe.clear()
        self.assertTrue(pipe.is_empty)


if __name__ == "__main__":
    unittest.main()
