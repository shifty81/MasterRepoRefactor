"""Phase 38B — Tests for CurveLinearColorPipeline and NetworkProfilerPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    CurveLinearColorPipeline,
    ColorCurveEntry,
    ColorKeyframeEntry,
    GradientBakeDef,
    NetworkProfilerPipeline,
    ProfilerSessionEntry,
    NetworkSampleEntry,
    NetworkAnomalyEntry,
)


# ---------------------------------------------------------------------------
# ColorKeyframeEntry
# ---------------------------------------------------------------------------

class TestColorKeyframeEntry(unittest.TestCase):
    def test_keyframe_id(self):
        k = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001")
        self.assertEqual(k.keyframe_id, "kf_001")

    def test_default_r(self):
        k = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001")
        self.assertEqual(k.r, 1.0)

    def test_is_at_start_true(self):
        k = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001", time=0.0)
        self.assertTrue(k.is_at_start)

    def test_is_at_start_false(self):
        k = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001", time=1.0)
        self.assertFalse(k.is_at_start)

    def test_is_opaque_true(self):
        k = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001", a=1.0)
        self.assertTrue(k.is_opaque)

    def test_is_opaque_false(self):
        k = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001", a=0.5)
        self.assertFalse(k.is_opaque)

    def test_is_transparent_false(self):
        k = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001", a=1.0)
        self.assertFalse(k.is_transparent)

    def test_is_transparent_true(self):
        k = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001", a=0.0)
        self.assertTrue(k.is_transparent)


# ---------------------------------------------------------------------------
# GradientBakeDef
# ---------------------------------------------------------------------------

class TestGradientBakeDef(unittest.TestCase):
    def test_bake_id(self):
        b = GradientBakeDef(bake_id="bake_001", curve_id="curve_001")
        self.assertEqual(b.bake_id, "bake_001")

    def test_default_resolution(self):
        b = GradientBakeDef(bake_id="bake_001", curve_id="curve_001")
        self.assertEqual(b.resolution, 256)

    def test_is_hd_false(self):
        b = GradientBakeDef(bake_id="bake_001", curve_id="curve_001", resolution=256)
        self.assertFalse(b.is_hd)

    def test_is_hd_true(self):
        b = GradientBakeDef(bake_id="bake_001", curve_id="curve_001", resolution=512)
        self.assertTrue(b.is_hd)

    def test_has_output_false(self):
        b = GradientBakeDef(bake_id="bake_001", curve_id="curve_001")
        self.assertFalse(b.has_output)

    def test_has_output_true(self):
        b = GradientBakeDef(bake_id="bake_001", curve_id="curve_001", output_path="/out/gradient.png")
        self.assertTrue(b.has_output)

    def test_is_complete_false(self):
        b = GradientBakeDef(bake_id="bake_001", curve_id="curve_001")
        self.assertFalse(b.is_complete)

    def test_is_complete_true(self):
        b = GradientBakeDef(bake_id="bake_001", curve_id="curve_001", success=True)
        self.assertTrue(b.is_complete)


# ---------------------------------------------------------------------------
# ColorCurveEntry
# ---------------------------------------------------------------------------

class TestColorCurveEntry(unittest.TestCase):
    def test_curve_id(self):
        c = ColorCurveEntry(curve_id="curve_001", curve_name="Fire Gradient")
        self.assertEqual(c.curve_id, "curve_001")

    def test_is_empty_true(self):
        c = ColorCurveEntry(curve_id="curve_001", curve_name="Fire Gradient")
        self.assertTrue(c.is_empty)

    def test_is_empty_false(self):
        kf = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001")
        c = ColorCurveEntry(curve_id="curve_001", curve_name="Fire Gradient", keyframes=[kf])
        self.assertFalse(c.is_empty)

    def test_has_bakes_false(self):
        c = ColorCurveEntry(curve_id="curve_001", curve_name="Fire Gradient")
        self.assertFalse(c.has_bakes)

    def test_has_bakes_true(self):
        bake = GradientBakeDef(bake_id="bake_001", curve_id="curve_001")
        c = ColorCurveEntry(curve_id="curve_001", curve_name="Fire Gradient", bakes=[bake])
        self.assertTrue(c.has_bakes)

    def test_is_enabled_true(self):
        c = ColorCurveEntry(curve_id="curve_001", curve_name="Fire Gradient")
        self.assertTrue(c.is_enabled)

    def test_keyframe_count_zero(self):
        c = ColorCurveEntry(curve_id="curve_001", curve_name="Fire Gradient")
        self.assertEqual(c.keyframe_count, 0)

    def test_keyframe_count_one(self):
        kf = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001")
        c = ColorCurveEntry(curve_id="curve_001", curve_name="Fire Gradient", keyframes=[kf])
        self.assertEqual(c.keyframe_count, 1)


# ---------------------------------------------------------------------------
# CurveLinearColorPipeline
# ---------------------------------------------------------------------------

class TestCurveLinearColorPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = CurveLinearColorPipeline()
        self.curve = ColorCurveEntry(curve_id="curve_001", curve_name="Fire Gradient")

    def test_add_curve(self):
        self.assertTrue(self.pipeline.add_curve(self.curve))

    def test_remove_curve(self):
        self.pipeline.add_curve(self.curve)
        self.assertTrue(self.pipeline.remove_curve("curve_001"))

    def test_get_all_curves(self):
        self.pipeline.add_curve(self.curve)
        self.assertEqual(len(self.pipeline.get_all_curves()), 1)

    def test_add_keyframe(self):
        self.pipeline.add_curve(self.curve)
        kf = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001")
        self.assertTrue(self.pipeline.add_keyframe("curve_001", kf))

    def test_remove_keyframe(self):
        self.pipeline.add_curve(self.curve)
        kf = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001")
        self.pipeline.add_keyframe("curve_001", kf)
        self.assertTrue(self.pipeline.remove_keyframe("curve_001", "kf_001"))

    def test_get_keyframes_for_curve(self):
        self.pipeline.add_curve(self.curve)
        kf = ColorKeyframeEntry(keyframe_id="kf_001", curve_id="curve_001")
        self.pipeline.add_keyframe("curve_001", kf)
        self.assertEqual(len(self.pipeline.get_keyframes_for_curve("curve_001")), 1)

    def test_add_bake(self):
        self.pipeline.add_curve(self.curve)
        bake = GradientBakeDef(bake_id="bake_001", curve_id="curve_001")
        self.assertTrue(self.pipeline.add_bake("curve_001", bake))

    def test_remove_bake(self):
        self.pipeline.add_curve(self.curve)
        bake = GradientBakeDef(bake_id="bake_001", curve_id="curve_001")
        self.pipeline.add_bake("curve_001", bake)
        self.assertTrue(self.pipeline.remove_bake("curve_001", "bake_001"))

    def test_get_bakes_for_curve(self):
        self.pipeline.add_curve(self.curve)
        bake = GradientBakeDef(bake_id="bake_001", curve_id="curve_001")
        self.pipeline.add_bake("curve_001", bake)
        self.assertEqual(len(self.pipeline.get_bakes_for_curve("curve_001")), 1)

    def test_get_completed_bakes(self):
        self.pipeline.add_curve(self.curve)
        bake = GradientBakeDef(bake_id="bake_001", curve_id="curve_001", success=True)
        self.pipeline.add_bake("curve_001", bake)
        completed = self.pipeline.get_completed_bakes()
        self.assertEqual(len(completed), 1)

    def test_set_enabled(self):
        self.pipeline.add_curve(self.curve)
        self.assertTrue(self.pipeline.set_enabled("curve_001", False))

    def test_get_enabled_curves(self):
        self.pipeline.add_curve(self.curve)
        self.assertEqual(len(self.pipeline.get_enabled_curves()), 1)

    def test_get_disabled_curves(self):
        self.pipeline.add_curve(self.curve)
        self.pipeline.set_enabled("curve_001", False)
        self.assertEqual(len(self.pipeline.get_disabled_curves()), 1)

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.curve))

    def test_curve_count(self):
        self.pipeline.add_curve(self.curve)
        self.assertEqual(self.pipeline.curve_count, 1)

    def test_is_empty(self):
        self.assertTrue(self.pipeline.is_empty)

    def test_clear(self):
        self.pipeline.add_curve(self.curve)
        self.pipeline.clear()
        self.assertTrue(self.pipeline.is_empty)


# ---------------------------------------------------------------------------
# NetworkSampleEntry
# ---------------------------------------------------------------------------

class TestNetworkSampleEntry(unittest.TestCase):
    def test_sample_id(self):
        s = NetworkSampleEntry(sample_id="s_001", session_id="sess_001")
        self.assertEqual(s.sample_id, "s_001")

    def test_default_metric_type(self):
        s = NetworkSampleEntry(sample_id="s_001", session_id="sess_001")
        self.assertEqual(s.metric_type, "Bandwidth")

    def test_is_latency_false(self):
        s = NetworkSampleEntry(sample_id="s_001", session_id="sess_001", metric_type="Bandwidth")
        self.assertFalse(s.is_latency)

    def test_is_latency_true(self):
        s = NetworkSampleEntry(sample_id="s_001", session_id="sess_001", metric_type="Latency")
        self.assertTrue(s.is_latency)

    def test_is_high_value_false(self):
        s = NetworkSampleEntry(sample_id="s_001", session_id="sess_001", value=500.0)
        self.assertFalse(s.is_high_value)

    def test_is_high_value_true(self):
        s = NetworkSampleEntry(sample_id="s_001", session_id="sess_001", value=2000.0)
        self.assertTrue(s.is_high_value)

    def test_has_timestamp_false(self):
        s = NetworkSampleEntry(sample_id="s_001", session_id="sess_001", timestamp=0.0)
        self.assertFalse(s.has_timestamp)

    def test_has_timestamp_true(self):
        s = NetworkSampleEntry(sample_id="s_001", session_id="sess_001", timestamp=1000.0)
        self.assertTrue(s.has_timestamp)


# ---------------------------------------------------------------------------
# NetworkAnomalyEntry
# ---------------------------------------------------------------------------

class TestNetworkAnomalyEntry(unittest.TestCase):
    def test_anomaly_id(self):
        a = NetworkAnomalyEntry(anomaly_id="anom_001", session_id="sess_001")
        self.assertEqual(a.anomaly_id, "anom_001")

    def test_default_metric_type(self):
        a = NetworkAnomalyEntry(anomaly_id="anom_001", session_id="sess_001")
        self.assertEqual(a.metric_type, "Latency")

    def test_is_critical_false(self):
        a = NetworkAnomalyEntry(anomaly_id="anom_001", session_id="sess_001",
                                threshold=100.0, actual_value=150.0)
        self.assertFalse(a.is_critical)

    def test_is_critical_true(self):
        a = NetworkAnomalyEntry(anomaly_id="anom_001", session_id="sess_001",
                                threshold=100.0, actual_value=250.0)
        self.assertTrue(a.is_critical)

    def test_is_acknowledged_false(self):
        a = NetworkAnomalyEntry(anomaly_id="anom_001", session_id="sess_001")
        self.assertFalse(a.is_acknowledged)

    def test_is_acknowledged_true(self):
        a = NetworkAnomalyEntry(anomaly_id="anom_001", session_id="sess_001", acknowledged=True)
        self.assertTrue(a.is_acknowledged)


# ---------------------------------------------------------------------------
# ProfilerSessionEntry
# ---------------------------------------------------------------------------

class TestProfilerSessionEntry(unittest.TestCase):
    def test_session_id(self):
        s = ProfilerSessionEntry(session_id="sess_001", session_name="Test Session")
        self.assertEqual(s.session_id, "sess_001")

    def test_is_recording_false(self):
        s = ProfilerSessionEntry(session_id="sess_001", session_name="Test Session", state="Idle")
        self.assertFalse(s.is_recording)

    def test_is_recording_true(self):
        s = ProfilerSessionEntry(session_id="sess_001", session_name="Test Session", state="Recording")
        self.assertTrue(s.is_recording)

    def test_is_completed_false(self):
        s = ProfilerSessionEntry(session_id="sess_001", session_name="Test Session", state="Idle")
        self.assertFalse(s.is_completed)

    def test_is_completed_true(self):
        s = ProfilerSessionEntry(session_id="sess_001", session_name="Test Session", state="Completed")
        self.assertTrue(s.is_completed)

    def test_has_anomalies_false(self):
        s = ProfilerSessionEntry(session_id="sess_001", session_name="Test Session")
        self.assertFalse(s.has_anomalies)

    def test_has_anomalies_true(self):
        a = NetworkAnomalyEntry(anomaly_id="anom_001", session_id="sess_001")
        s = ProfilerSessionEntry(session_id="sess_001", session_name="Test Session", anomalies=[a])
        self.assertTrue(s.has_anomalies)

    def test_sample_count_zero(self):
        s = ProfilerSessionEntry(session_id="sess_001", session_name="Test Session")
        self.assertEqual(s.sample_count, 0)


# ---------------------------------------------------------------------------
# NetworkProfilerPipeline
# ---------------------------------------------------------------------------

class TestNetworkProfilerPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = NetworkProfilerPipeline()
        self.session = ProfilerSessionEntry(session_id="sess_001", session_name="Test Session")

    def test_add_session(self):
        self.assertTrue(self.pipeline.add_session(self.session))

    def test_remove_session(self):
        self.pipeline.add_session(self.session)
        self.assertTrue(self.pipeline.remove_session("sess_001"))

    def test_get_all_sessions(self):
        self.pipeline.add_session(self.session)
        self.assertEqual(len(self.pipeline.get_all_sessions()), 1)

    def test_add_sample(self):
        self.pipeline.add_session(self.session)
        sample = NetworkSampleEntry(sample_id="s_001", session_id="sess_001")
        self.assertTrue(self.pipeline.add_sample("sess_001", sample))

    def test_remove_sample(self):
        self.pipeline.add_session(self.session)
        sample = NetworkSampleEntry(sample_id="s_001", session_id="sess_001")
        self.pipeline.add_sample("sess_001", sample)
        self.assertTrue(self.pipeline.remove_sample("sess_001", "s_001"))

    def test_get_samples_for_session(self):
        self.pipeline.add_session(self.session)
        sample = NetworkSampleEntry(sample_id="s_001", session_id="sess_001")
        self.pipeline.add_sample("sess_001", sample)
        self.assertEqual(len(self.pipeline.get_samples_for_session("sess_001")), 1)

    def test_add_anomaly(self):
        self.pipeline.add_session(self.session)
        anom = NetworkAnomalyEntry(anomaly_id="anom_001", session_id="sess_001")
        self.assertTrue(self.pipeline.add_anomaly("sess_001", anom))

    def test_remove_anomaly(self):
        self.pipeline.add_session(self.session)
        anom = NetworkAnomalyEntry(anomaly_id="anom_001", session_id="sess_001")
        self.pipeline.add_anomaly("sess_001", anom)
        self.assertTrue(self.pipeline.remove_anomaly("sess_001", "anom_001"))

    def test_get_anomalies_for_session(self):
        self.pipeline.add_session(self.session)
        anom = NetworkAnomalyEntry(anomaly_id="anom_001", session_id="sess_001")
        self.pipeline.add_anomaly("sess_001", anom)
        self.assertEqual(len(self.pipeline.get_anomalies_for_session("sess_001")), 1)

    def test_get_unacknowledged_anomalies(self):
        self.pipeline.add_session(self.session)
        anom = NetworkAnomalyEntry(anomaly_id="anom_001", session_id="sess_001", acknowledged=False)
        self.pipeline.add_anomaly("sess_001", anom)
        self.assertEqual(len(self.pipeline.get_unacknowledged_anomalies()), 1)

    def test_get_recording_sessions(self):
        self.pipeline.add_session(self.session)
        self.pipeline.set_state("sess_001", "Recording")
        self.assertEqual(len(self.pipeline.get_recording_sessions()), 1)

    def test_set_state(self):
        self.pipeline.add_session(self.session)
        self.assertTrue(self.pipeline.set_state("sess_001", "Recording"))

    def test_get_enabled_sessions(self):
        self.pipeline.add_session(self.session)
        self.assertEqual(len(self.pipeline.get_enabled_sessions()), 1)

    def test_get_disabled_sessions(self):
        self.pipeline.add_session(self.session)
        self.session.enabled = False
        self.assertEqual(len(self.pipeline.get_disabled_sessions()), 1)

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.session))

    def test_session_count(self):
        self.pipeline.add_session(self.session)
        self.assertEqual(self.pipeline.session_count, 1)

    def test_is_empty(self):
        self.assertTrue(self.pipeline.is_empty)

    def test_clear(self):
        self.pipeline.add_session(self.session)
        self.pipeline.clear()
        self.assertTrue(self.pipeline.is_empty)


if __name__ == "__main__":
    unittest.main()
