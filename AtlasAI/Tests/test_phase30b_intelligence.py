"""Phase 30B — Tests for RenderPipelineCache and WorldStreamingPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    RenderPipelineCache,
    RenderPassDef,
    RenderPipelineEntry,
    PipelineCacheStats,
    WorldStreamingPipeline,
    StreamingZoneDef,
    StreamingLODRule,
    WorldStreamingResult,
)


# ---------------------------------------------------------------------------
# RenderPassDef
# ---------------------------------------------------------------------------

class TestRenderPassDef(unittest.TestCase):
    def test_pass_id_field(self):
        p = RenderPassDef(pass_id="p001", pass_name="Opaque Pass")
        self.assertEqual(p.pass_id, "p001")

    def test_pass_name_field(self):
        p = RenderPassDef(pass_id="p001", pass_name="Opaque Pass")
        self.assertEqual(p.pass_name, "Opaque Pass")

    def test_default_pass_type(self):
        p = RenderPassDef(pass_id="p001", pass_name="Opaque Pass")
        self.assertEqual(p.pass_type, "Opaque")

    def test_default_priority(self):
        p = RenderPassDef(pass_id="p001", pass_name="Opaque Pass")
        self.assertEqual(p.priority, 0)

    def test_default_enabled(self):
        p = RenderPassDef(pass_id="p001", pass_name="Opaque Pass")
        self.assertTrue(p.enabled)

    def test_is_enabled_property(self):
        p = RenderPassDef(pass_id="p001", pass_name="Opaque Pass", enabled=True)
        self.assertTrue(p.is_enabled)

    def test_is_postprocess_false(self):
        p = RenderPassDef(pass_id="p001", pass_name="Opaque Pass")
        self.assertFalse(p.is_postprocess)


# ---------------------------------------------------------------------------
# RenderPipelineEntry
# ---------------------------------------------------------------------------

class TestRenderPipelineEntry(unittest.TestCase):
    def test_entry_id(self):
        e = RenderPipelineEntry(entry_id="e001", pipeline_name="ForwardPipeline")
        self.assertEqual(e.entry_id, "e001")

    def test_pipeline_name(self):
        e = RenderPipelineEntry(entry_id="e001", pipeline_name="ForwardPipeline")
        self.assertEqual(e.pipeline_name, "ForwardPipeline")

    def test_default_version(self):
        e = RenderPipelineEntry(entry_id="e001", pipeline_name="ForwardPipeline")
        self.assertEqual(e.version, 1)

    def test_default_platform(self):
        e = RenderPipelineEntry(entry_id="e001", pipeline_name="ForwardPipeline")
        self.assertEqual(e.platform, "PC")

    def test_pass_count_zero(self):
        e = RenderPipelineEntry(entry_id="e001", pipeline_name="ForwardPipeline")
        self.assertEqual(e.pass_count, 0)

    def test_is_empty_true(self):
        e = RenderPipelineEntry(entry_id="e001", pipeline_name="ForwardPipeline")
        self.assertTrue(e.is_empty)


# ---------------------------------------------------------------------------
# PipelineCacheStats
# ---------------------------------------------------------------------------

class TestPipelineCacheStats(unittest.TestCase):
    def test_default_total_entries(self):
        s = PipelineCacheStats()
        self.assertEqual(s.total_entries, 0)

    def test_default_cache_hits(self):
        s = PipelineCacheStats()
        self.assertEqual(s.cache_hits, 0)

    def test_hit_rate_zero(self):
        s = PipelineCacheStats()
        self.assertAlmostEqual(s.hit_rate, 0.0)

    def test_total_lookups_zero(self):
        s = PipelineCacheStats()
        self.assertEqual(s.total_lookups, 0)


# ---------------------------------------------------------------------------
# RenderPipelineCache
# ---------------------------------------------------------------------------

class TestRenderPipelineCache(unittest.TestCase):
    def setUp(self):
        self.cache = RenderPipelineCache()

    def _make_entry(self, eid="e001", name="Forward"):
        return RenderPipelineEntry(entry_id=eid, pipeline_name=name)

    def test_add_entry(self):
        self.cache.add_entry(self._make_entry())
        self.assertEqual(self.cache.entry_count, 1)

    def test_remove_entry(self):
        self.cache.add_entry(self._make_entry())
        result = self.cache.remove_entry("e001")
        self.assertTrue(result)
        self.assertEqual(self.cache.entry_count, 0)

    def test_get_entry(self):
        self.cache.add_entry(self._make_entry())
        e = self.cache.get_entry("e001")
        self.assertIsNotNone(e)
        self.assertEqual(e.pipeline_name, "Forward")

    def test_get_all_entries(self):
        self.cache.add_entry(self._make_entry("e001", "Forward"))
        self.cache.add_entry(self._make_entry("e002", "Deferred"))
        self.assertEqual(len(self.cache.get_all_entries()), 2)

    def test_lookup_by_name(self):
        self.cache.add_entry(self._make_entry("e001", "Forward"))
        e = self.cache.lookup("Forward")
        self.assertIsNotNone(e)

    def test_invalidate(self):
        self.cache.add_entry(self._make_entry())
        self.cache.invalidate("e001")
        self.assertIsNone(self.cache.get_entry("e001"))

    def test_invalidate_all(self):
        self.cache.add_entry(self._make_entry("e001", "A"))
        self.cache.add_entry(self._make_entry("e002", "B"))
        self.cache.invalidate_all()
        self.assertEqual(len(self.cache.get_all_entries()), 0)

    def test_get_stats(self):
        stats = self.cache.get_stats()
        self.assertIsInstance(stats, PipelineCacheStats)

    def test_entry_count(self):
        self.assertEqual(self.cache.entry_count, 0)
        self.cache.add_entry(self._make_entry())
        self.assertEqual(self.cache.entry_count, 1)

    def test_is_empty_true(self):
        self.assertTrue(self.cache.is_empty)

    def test_is_empty_false(self):
        self.cache.add_entry(self._make_entry())
        self.assertFalse(self.cache.is_empty)

    def test_clear(self):
        self.cache.add_entry(self._make_entry())
        self.cache.clear()
        self.assertTrue(self.cache.is_empty)


# ---------------------------------------------------------------------------
# StreamingZoneDef
# ---------------------------------------------------------------------------

class TestStreamingZoneDef(unittest.TestCase):
    def test_zone_id(self):
        z = StreamingZoneDef(zone_id="z001", zone_name="Downtown")
        self.assertEqual(z.zone_id, "z001")

    def test_zone_name(self):
        z = StreamingZoneDef(zone_id="z001", zone_name="Downtown")
        self.assertEqual(z.zone_name, "Downtown")

    def test_default_zone_type(self):
        z = StreamingZoneDef(zone_id="z001", zone_name="Downtown")
        self.assertEqual(z.zone_type, "Static")

    def test_default_radius(self):
        z = StreamingZoneDef(zone_id="z001", zone_name="Downtown")
        self.assertAlmostEqual(z.radius, 500.0)

    def test_is_dynamic_false(self):
        z = StreamingZoneDef(zone_id="z001", zone_name="Downtown")
        self.assertFalse(z.is_dynamic)

    def test_is_in_range_true(self):
        z = StreamingZoneDef(zone_id="z001", zone_name="Downtown")
        self.assertTrue(z.is_in_range)


# ---------------------------------------------------------------------------
# StreamingLODRule
# ---------------------------------------------------------------------------

class TestStreamingLODRule(unittest.TestCase):
    def test_rule_id(self):
        r = StreamingLODRule(rule_id="r001", zone_id="z001")
        self.assertEqual(r.rule_id, "r001")

    def test_zone_id(self):
        r = StreamingLODRule(rule_id="r001", zone_id="z001")
        self.assertEqual(r.zone_id, "z001")

    def test_default_lod_level(self):
        r = StreamingLODRule(rule_id="r001", zone_id="z001")
        self.assertEqual(r.lod_level, 0)

    def test_default_distance_threshold(self):
        r = StreamingLODRule(rule_id="r001", zone_id="z001")
        self.assertAlmostEqual(r.distance_threshold, 200.0)

    def test_is_culled_false(self):
        r = StreamingLODRule(rule_id="r001", zone_id="z001")
        self.assertFalse(r.is_culled_at_threshold)


# ---------------------------------------------------------------------------
# WorldStreamingResult
# ---------------------------------------------------------------------------

class TestWorldStreamingResult(unittest.TestCase):
    def test_job_id(self):
        r = WorldStreamingResult(job_id="job_0001")
        self.assertEqual(r.job_id, "job_0001")

    def test_default_zones_loaded(self):
        r = WorldStreamingResult(job_id="job_0001")
        self.assertEqual(r.zones_loaded, 0)

    def test_has_errors_false(self):
        r = WorldStreamingResult(job_id="job_0001")
        self.assertFalse(r.has_errors)

    def test_total_operations_zero(self):
        r = WorldStreamingResult(job_id="job_0001")
        self.assertEqual(r.total_operations, 0)


# ---------------------------------------------------------------------------
# WorldStreamingPipeline
# ---------------------------------------------------------------------------

class TestWorldStreamingPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = WorldStreamingPipeline()
        self.zone = StreamingZoneDef(zone_id="z001", zone_name="Meadow")

    def test_register_zone(self):
        self.pipeline.register_zone(self.zone)
        self.assertEqual(self.pipeline.zone_count, 1)

    def test_unregister_zone(self):
        self.pipeline.register_zone(self.zone)
        result = self.pipeline.unregister_zone("z001")
        self.assertTrue(result)
        self.assertEqual(self.pipeline.zone_count, 0)

    def test_add_lod_rule(self):
        self.pipeline.register_zone(self.zone)
        rule = StreamingLODRule(rule_id="r001", zone_id="z001")
        self.pipeline.add_lod_rule(rule)

    def test_get_zone(self):
        self.pipeline.register_zone(self.zone)
        z = self.pipeline.get_zone("z001")
        self.assertIsNotNone(z)
        self.assertEqual(z.zone_name, "Meadow")

    def test_get_all_zones(self):
        self.pipeline.register_zone(self.zone)
        self.pipeline.register_zone(StreamingZoneDef(zone_id="z002", zone_name="Forest"))
        self.assertEqual(len(self.pipeline.get_all_zones()), 2)

    def test_stream_in(self):
        self.pipeline.register_zone(self.zone)
        result = self.pipeline.stream_in("z001")
        self.assertEqual(result.zones_loaded, 1)
        self.assertFalse(result.has_errors)

    def test_stream_out(self):
        self.pipeline.register_zone(self.zone)
        self.pipeline.stream_in("z001")
        result = self.pipeline.stream_out("z001")
        self.assertEqual(result.zones_unloaded, 1)

    def test_get_active_zones(self):
        self.pipeline.register_zone(self.zone)
        self.pipeline.stream_in("z001")
        active = self.pipeline.get_active_zones()
        self.assertEqual(len(active), 1)

    def test_validate_zone(self):
        self.assertTrue(self.pipeline.validate_zone(self.zone))

    def test_zone_count(self):
        self.assertEqual(self.pipeline.zone_count, 0)
        self.pipeline.register_zone(self.zone)
        self.assertEqual(self.pipeline.zone_count, 1)

    def test_active_zone_count(self):
        self.pipeline.register_zone(self.zone)
        self.assertEqual(self.pipeline.active_zone_count, 0)
        self.pipeline.stream_in("z001")
        self.assertEqual(self.pipeline.active_zone_count, 1)

    def test_clear(self):
        self.pipeline.register_zone(self.zone)
        self.pipeline.clear()
        self.assertEqual(self.pipeline.zone_count, 0)


if __name__ == "__main__":
    unittest.main()
