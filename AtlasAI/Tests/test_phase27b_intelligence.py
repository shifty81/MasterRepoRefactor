"""Phase 27B — Tests for AudioEffectPipeline and ClothSimulationCache."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    AudioEffectPipeline,
    AudioEffectJob,
    AudioProcessResult,
    EQBand,
    CompressorSettings,
    ReverbSettings,
    NormalisationSettings,
    ClothSimulationCache,
    ClothSimEntry,
    ClothFrameSnapshot,
    ClothCachePolicy,
)

TMP_DIR = Path("/tmp/test_phase27b")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# EQBand dataclass
# ---------------------------------------------------------------------------

class TestEQBandDataclass(unittest.TestCase):
    def test_band_id_field(self):
        b = EQBand(band_id="b001")
        self.assertEqual(b.band_id, "b001")

    def test_default_frequency(self):
        b = EQBand(band_id="b001")
        self.assertAlmostEqual(b.frequency_hz, 1000.0)

    def test_is_boost_positive_gain(self):
        b = EQBand(band_id="b001", gain_db=3.0)
        self.assertTrue(b.is_boost)

    def test_is_cut_negative_gain(self):
        b = EQBand(band_id="b001", gain_db=-6.0)
        self.assertTrue(b.is_cut)

    def test_default_enabled(self):
        b = EQBand(band_id="b001")
        self.assertTrue(b.enabled)


# ---------------------------------------------------------------------------
# CompressorSettings dataclass
# ---------------------------------------------------------------------------

class TestCompressorSettingsDataclass(unittest.TestCase):
    def test_default_threshold(self):
        c = CompressorSettings()
        self.assertAlmostEqual(c.threshold_db, -12.0)

    def test_default_ratio(self):
        c = CompressorSettings()
        self.assertAlmostEqual(c.ratio, 4.0)

    def test_is_limiting_high_ratio(self):
        c = CompressorSettings(ratio=20.0)
        self.assertTrue(c.is_limiting)

    def test_is_not_limiting_low_ratio(self):
        c = CompressorSettings(ratio=4.0)
        self.assertFalse(c.is_limiting)

    def test_default_enabled(self):
        c = CompressorSettings()
        self.assertTrue(c.enabled)


# ---------------------------------------------------------------------------
# ReverbSettings dataclass
# ---------------------------------------------------------------------------

class TestReverbSettingsDataclass(unittest.TestCase):
    def test_default_room_size(self):
        r = ReverbSettings()
        self.assertAlmostEqual(r.room_size, 0.5)

    def test_default_wet_level(self):
        r = ReverbSettings()
        self.assertAlmostEqual(r.wet_level, 0.2)

    def test_default_algorithm(self):
        r = ReverbSettings()
        self.assertEqual(r.algorithm, "Algorithmic")


# ---------------------------------------------------------------------------
# NormalisationSettings dataclass
# ---------------------------------------------------------------------------

class TestNormalisationSettingsDataclass(unittest.TestCase):
    def test_default_target_db(self):
        n = NormalisationSettings()
        self.assertAlmostEqual(n.target_db, -6.0)

    def test_default_mode(self):
        n = NormalisationSettings()
        self.assertEqual(n.mode, "Peak")

    def test_default_enabled(self):
        n = NormalisationSettings()
        self.assertTrue(n.enabled)


# ---------------------------------------------------------------------------
# AudioEffectJob dataclass
# ---------------------------------------------------------------------------

class TestAudioEffectJobDataclass(unittest.TestCase):
    def test_job_id_field(self):
        j = AudioEffectJob(job_id="j001", input_path="sfx.wav")
        self.assertEqual(j.job_id, "j001")

    def test_input_path(self):
        j = AudioEffectJob(job_id="j001", input_path="sfx.wav")
        self.assertEqual(j.input_path, "sfx.wav")

    def test_default_sample_rate(self):
        j = AudioEffectJob(job_id="j001", input_path="sfx.wav")
        self.assertEqual(j.sample_rate, 44100)

    def test_is_stereo_two_channels(self):
        j = AudioEffectJob(job_id="j001", input_path="sfx.wav", channels=2)
        self.assertTrue(j.is_stereo)

    def test_is_not_stereo_mono(self):
        j = AudioEffectJob(job_id="j001", input_path="sfx.wav", channels=1)
        self.assertFalse(j.is_stereo)

    def test_has_pitch_shift_false(self):
        j = AudioEffectJob(job_id="j001", input_path="sfx.wav")
        self.assertFalse(j.has_pitch_shift)

    def test_has_pitch_shift_true(self):
        j = AudioEffectJob(job_id="j001", input_path="sfx.wav",
                            pitch_shift_semitones=2.0)
        self.assertTrue(j.has_pitch_shift)


# ---------------------------------------------------------------------------
# AudioProcessResult dataclass
# ---------------------------------------------------------------------------

class TestAudioProcessResultDataclass(unittest.TestCase):
    def test_job_id_field(self):
        r = AudioProcessResult(job_id="j001")
        self.assertEqual(r.job_id, "j001")

    def test_default_success_false(self):
        r = AudioProcessResult(job_id="j001")
        self.assertFalse(r.success)

    def test_has_warnings_false(self):
        r = AudioProcessResult(job_id="j001")
        self.assertFalse(r.has_warnings)


# ---------------------------------------------------------------------------
# AudioEffectPipeline — job management
# ---------------------------------------------------------------------------

class TestAudioEffectPipelineJobs(unittest.TestCase):
    def setUp(self):
        self.pipeline = AudioEffectPipeline()

    def test_add_job_returns_job(self):
        j = self.pipeline.add_job("sfx.wav")
        self.assertIsInstance(j, AudioEffectJob)

    def test_job_id_unique(self):
        j1 = self.pipeline.add_job("a.wav")
        j2 = self.pipeline.add_job("b.wav")
        self.assertNotEqual(j1.job_id, j2.job_id)

    def test_get_job_count(self):
        self.pipeline.add_job("a.wav")
        self.pipeline.add_job("b.wav")
        self.assertEqual(self.pipeline.get_job_count(), 2)

    def test_get_job_by_id(self):
        j = self.pipeline.add_job("a.wav")
        fetched = self.pipeline.get_job(j.job_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.input_path, "a.wav")

    def test_get_job_missing_returns_none(self):
        self.assertIsNone(self.pipeline.get_job("ghost"))

    def test_remove_job(self):
        j = self.pipeline.add_job("a.wav")
        self.assertTrue(self.pipeline.remove_job(j.job_id))
        self.assertEqual(self.pipeline.get_job_count(), 0)

    def test_remove_job_missing_false(self):
        self.assertFalse(self.pipeline.remove_job("ghost"))

    def test_get_all_job_ids(self):
        j = self.pipeline.add_job("a.wav")
        self.assertIn(j.job_id, self.pipeline.get_all_job_ids())

    def test_clear(self):
        self.pipeline.add_job("a.wav")
        self.pipeline.clear()
        self.assertEqual(self.pipeline.get_job_count(), 0)


# ---------------------------------------------------------------------------
# AudioEffectPipeline — DSP settings
# ---------------------------------------------------------------------------

class TestAudioEffectPipelineDSP(unittest.TestCase):
    def setUp(self):
        self.pipeline = AudioEffectPipeline()
        self.job = self.pipeline.add_job("sfx.wav")

    def test_add_eq_band_returns_band(self):
        b = self.pipeline.add_eq_band(self.job.job_id, 1000.0, 3.0)
        self.assertIsInstance(b, EQBand)

    def test_eq_band_frequency(self):
        b = self.pipeline.add_eq_band(self.job.job_id, 2000.0)
        self.assertAlmostEqual(b.frequency_hz, 2000.0)

    def test_get_eq_band_count(self):
        self.pipeline.add_eq_band(self.job.job_id)
        self.pipeline.add_eq_band(self.job.job_id)
        self.assertEqual(self.pipeline.get_eq_band_count(self.job.job_id), 2)

    def test_add_eq_band_unknown_job_returns_none(self):
        result = self.pipeline.add_eq_band("ghost")
        self.assertIsNone(result)

    def test_remove_eq_band(self):
        b = self.pipeline.add_eq_band(self.job.job_id)
        self.assertTrue(self.pipeline.remove_eq_band(self.job.job_id, b.band_id))
        self.assertEqual(self.pipeline.get_eq_band_count(self.job.job_id), 0)

    def test_get_eq_bands(self):
        self.pipeline.add_eq_band(self.job.job_id, 500.0)
        bands = self.pipeline.get_eq_bands(self.job.job_id)
        self.assertEqual(len(bands), 1)

    def test_set_compressor_returns_settings(self):
        c = self.pipeline.set_compressor(self.job.job_id, threshold_db=-18.0)
        self.assertIsInstance(c, CompressorSettings)

    def test_compressor_threshold(self):
        c = self.pipeline.set_compressor(self.job.job_id, threshold_db=-18.0)
        self.assertAlmostEqual(c.threshold_db, -18.0)

    def test_get_compressor(self):
        self.pipeline.set_compressor(self.job.job_id)
        c = self.pipeline.get_compressor(self.job.job_id)
        self.assertIsNotNone(c)

    def test_remove_compressor(self):
        self.pipeline.set_compressor(self.job.job_id)
        self.assertTrue(self.pipeline.remove_compressor(self.job.job_id))
        self.assertIsNone(self.pipeline.get_compressor(self.job.job_id))

    def test_set_reverb_returns_settings(self):
        r = self.pipeline.set_reverb(self.job.job_id, room_size=0.8)
        self.assertIsInstance(r, ReverbSettings)

    def test_reverb_room_size(self):
        r = self.pipeline.set_reverb(self.job.job_id, room_size=0.8)
        self.assertAlmostEqual(r.room_size, 0.8)

    def test_get_reverb(self):
        self.pipeline.set_reverb(self.job.job_id)
        r = self.pipeline.get_reverb(self.job.job_id)
        self.assertIsNotNone(r)

    def test_remove_reverb(self):
        self.pipeline.set_reverb(self.job.job_id)
        self.assertTrue(self.pipeline.remove_reverb(self.job.job_id))
        self.assertIsNone(self.pipeline.get_reverb(self.job.job_id))

    def test_set_normalisation_returns_settings(self):
        n = self.pipeline.set_normalisation(self.job.job_id, target_db=-3.0)
        self.assertIsInstance(n, NormalisationSettings)

    def test_normalisation_target(self):
        n = self.pipeline.set_normalisation(self.job.job_id, target_db=-3.0)
        self.assertAlmostEqual(n.target_db, -3.0)

    def test_get_normalisation(self):
        self.pipeline.set_normalisation(self.job.job_id)
        n = self.pipeline.get_normalisation(self.job.job_id)
        self.assertIsNotNone(n)


# ---------------------------------------------------------------------------
# AudioEffectPipeline — processing
# ---------------------------------------------------------------------------

class TestAudioEffectPipelineProcessing(unittest.TestCase):
    def setUp(self):
        self.pipeline = AudioEffectPipeline()
        self.job = self.pipeline.add_job("sfx.wav")
        self.pipeline.set_compressor(self.job.job_id)
        self.pipeline.set_normalisation(self.job.job_id, target_db=-6.0)

    def test_process_job_returns_result(self):
        r = self.pipeline.process_job(self.job.job_id)
        self.assertIsInstance(r, AudioProcessResult)

    def test_process_job_success(self):
        r = self.pipeline.process_job(self.job.job_id)
        self.assertTrue(r.success)

    def test_process_job_unknown_fails(self):
        r = self.pipeline.process_job("ghost")
        self.assertFalse(r.success)

    def test_process_all_returns_list(self):
        self.pipeline.add_job("b.wav")
        results = self.pipeline.process_all()
        self.assertEqual(len(results), 2)

    def test_get_result_after_processing(self):
        self.pipeline.process_job(self.job.job_id)
        r = self.pipeline.get_result(self.job.job_id)
        self.assertIsNotNone(r)

    def test_get_processed_count(self):
        self.pipeline.process_job(self.job.job_id)
        self.assertEqual(self.pipeline.get_processed_count(), 1)

    def test_get_success_count(self):
        self.pipeline.process_job(self.job.job_id)
        self.assertEqual(self.pipeline.get_success_count(), 1)

    def test_get_failure_count_no_failures(self):
        self.pipeline.process_job(self.job.job_id)
        self.assertEqual(self.pipeline.get_failure_count(), 0)

    def test_save_manifest(self):
        out = str(TMP_DIR / "audio_manifest.json")
        self.assertTrue(self.pipeline.save_manifest(out))
        self.assertTrue(Path(out).exists())

    def test_save_manifest_content(self):
        out = str(TMP_DIR / "audio_manifest2.json")
        self.pipeline.save_manifest(out)
        data = json.loads(Path(out).read_text())
        self.assertIn("jobs", data)
        self.assertIn("job_count", data)


# ---------------------------------------------------------------------------
# ClothFrameSnapshot dataclass
# ---------------------------------------------------------------------------

class TestClothFrameSnapshotDataclass(unittest.TestCase):
    def test_frame_index_field(self):
        f = ClothFrameSnapshot(frame_index=5, layer_id="l001",
                                simulation_id="cloth_0001")
        self.assertEqual(f.frame_index, 5)

    def test_total_energy(self):
        f = ClothFrameSnapshot(frame_index=0, layer_id="l001",
                                simulation_id="c",
                                kinetic_energy=3.0, potential_energy=2.0)
        self.assertAlmostEqual(f.total_energy, 5.0)

    def test_is_sleeping_zero_kinetic(self):
        f = ClothFrameSnapshot(frame_index=0, layer_id="l001",
                                simulation_id="c", kinetic_energy=0.0)
        self.assertTrue(f.is_sleeping)

    def test_is_not_sleeping_with_kinetic(self):
        f = ClothFrameSnapshot(frame_index=0, layer_id="l001",
                                simulation_id="c", kinetic_energy=1.0)
        self.assertFalse(f.is_sleeping)


# ---------------------------------------------------------------------------
# ClothSimEntry dataclass
# ---------------------------------------------------------------------------

class TestClothSimEntryDataclass(unittest.TestCase):
    def test_simulation_id_field(self):
        import time
        e = ClothSimEntry("cloth_0001", "l001", "Jacket", created_at=time.time())
        self.assertEqual(e.simulation_id, "cloth_0001")

    def test_stored_frame_count_empty(self):
        import time
        e = ClothSimEntry("cloth_0001", "l001", "Jacket", created_at=time.time())
        self.assertEqual(e.stored_frame_count, 0)

    def test_fill_ratio_zero_when_no_frames(self):
        import time
        e = ClothSimEntry("cloth_0001", "l001", "Jacket",
                           frame_count=0, created_at=time.time())
        self.assertAlmostEqual(e.fill_ratio, 0.0)

    def test_cache_size_kb(self):
        import time
        e = ClothSimEntry("cloth_0001", "l001", "Jacket",
                           cache_size_bytes=1024, created_at=time.time())
        self.assertAlmostEqual(e.cache_size_kb, 1.0)

    def test_not_complete_when_no_frames(self):
        import time
        e = ClothSimEntry("cloth_0001", "l001", "Jacket",
                           frame_count=100, created_at=time.time())
        self.assertFalse(e.is_complete)


# ---------------------------------------------------------------------------
# ClothCachePolicy dataclass
# ---------------------------------------------------------------------------

class TestClothCachePolicyDataclass(unittest.TestCase):
    def test_policy_id_field(self):
        p = ClothCachePolicy(policy_id="strict")
        self.assertEqual(p.policy_id, "strict")

    def test_default_max_entries(self):
        p = ClothCachePolicy(policy_id="default")
        self.assertEqual(p.max_entries, 50)

    def test_default_store_only_baked(self):
        p = ClothCachePolicy(policy_id="default")
        self.assertFalse(p.store_only_baked)


# ---------------------------------------------------------------------------
# ClothSimulationCache — entry management
# ---------------------------------------------------------------------------

class TestClothSimulationCacheEntries(unittest.TestCase):
    def setUp(self):
        self.cache = ClothSimulationCache()

    def test_create_entry_returns_entry(self):
        e = self.cache.create_entry("l001", "Jacket")
        self.assertIsInstance(e, ClothSimEntry)

    def test_entry_layer_id(self):
        e = self.cache.create_entry("l001", "Jacket")
        self.assertEqual(e.layer_id, "l001")

    def test_simulation_id_unique(self):
        e1 = self.cache.create_entry("l001", "Jacket")
        e2 = self.cache.create_entry("l002", "Pants")
        self.assertNotEqual(e1.simulation_id, e2.simulation_id)

    def test_get_entry_count(self):
        self.cache.create_entry("l001", "A")
        self.cache.create_entry("l002", "B")
        self.assertEqual(self.cache.get_entry_count(), 2)

    def test_get_entry_by_id(self):
        e = self.cache.create_entry("l001", "Jacket")
        fetched = self.cache.get_entry(e.simulation_id)
        self.assertIsNotNone(fetched)

    def test_get_entry_missing_returns_none(self):
        self.assertIsNone(self.cache.get_entry("ghost"))

    def test_has_entry_true(self):
        e = self.cache.create_entry("l001", "Jacket")
        self.assertTrue(self.cache.has_entry(e.simulation_id))

    def test_has_entry_false(self):
        self.assertFalse(self.cache.has_entry("ghost"))

    def test_remove_entry(self):
        e = self.cache.create_entry("l001", "Jacket")
        self.assertTrue(self.cache.remove_entry(e.simulation_id))
        self.assertEqual(self.cache.get_entry_count(), 0)

    def test_get_entries_for_layer(self):
        e = self.cache.create_entry("l001", "Jacket")
        self.cache.create_entry("l002", "Pants")
        ids = self.cache.get_entries_for_layer("l001")
        self.assertIn(e.simulation_id, ids)
        self.assertEqual(len(ids), 1)

    def test_mark_baked(self):
        e = self.cache.create_entry("l001", "Jacket")
        self.assertTrue(self.cache.mark_baked(e.simulation_id))
        self.assertTrue(e.is_baked)

    def test_get_baked_entries(self):
        e = self.cache.create_entry("l001", "Jacket")
        self.cache.mark_baked(e.simulation_id)
        baked = self.cache.get_baked_entries()
        self.assertIn(e.simulation_id, baked)

    def test_clear(self):
        self.cache.create_entry("l001", "Jacket")
        self.cache.clear()
        self.assertEqual(self.cache.get_entry_count(), 0)


# ---------------------------------------------------------------------------
# ClothSimulationCache — frame storage
# ---------------------------------------------------------------------------

class TestClothSimulationCacheFrames(unittest.TestCase):
    def setUp(self):
        self.cache = ClothSimulationCache()
        self.entry = self.cache.create_entry("l001", "Jacket",
                                               frame_count=60,
                                               frame_rate=30.0,
                                               vertex_count=1000)

    def test_store_frame_returns_snapshot(self):
        f = self.cache.store_frame(self.entry.simulation_id, 0,
                                    kinetic_energy=5.0)
        self.assertIsInstance(f, ClothFrameSnapshot)

    def test_frame_index_set(self):
        f = self.cache.store_frame(self.entry.simulation_id, 10)
        self.assertEqual(f.frame_index, 10)

    def test_frame_kinetic_energy(self):
        f = self.cache.store_frame(self.entry.simulation_id, 0,
                                    kinetic_energy=7.5)
        self.assertAlmostEqual(f.kinetic_energy, 7.5)

    def test_get_frame_count_increases(self):
        self.cache.store_frame(self.entry.simulation_id, 0)
        self.cache.store_frame(self.entry.simulation_id, 1)
        self.assertEqual(
            self.cache.get_frame_count(self.entry.simulation_id), 2
        )

    def test_get_frame_by_index(self):
        self.cache.store_frame(self.entry.simulation_id, 5, kinetic_energy=2.0)
        f = self.cache.get_frame(self.entry.simulation_id, 5)
        self.assertIsNotNone(f)
        self.assertAlmostEqual(f.kinetic_energy, 2.0)

    def test_get_frame_missing_returns_none(self):
        self.assertIsNone(
            self.cache.get_frame(self.entry.simulation_id, 999)
        )

    def test_store_frame_unknown_sim_returns_none(self):
        self.assertIsNone(self.cache.store_frame("ghost", 0))

    def test_clear_frames(self):
        self.cache.store_frame(self.entry.simulation_id, 0)
        self.assertTrue(self.cache.clear_frames(self.entry.simulation_id))
        self.assertEqual(
            self.cache.get_frame_count(self.entry.simulation_id), 0
        )

    def test_is_complete_after_enough_frames(self):
        for i in range(60):
            self.cache.store_frame(self.entry.simulation_id, i)
        self.assertTrue(self.entry.is_complete)


# ---------------------------------------------------------------------------
# ClothSimulationCache — stats and eviction
# ---------------------------------------------------------------------------

class TestClothSimulationCacheStats(unittest.TestCase):
    def setUp(self):
        self.cache = ClothSimulationCache()

    def test_hit_count_increments(self):
        e = self.cache.create_entry("l001", "A")
        self.cache.get_entry(e.simulation_id)
        self.assertEqual(self.cache.get_hit_count(), 1)

    def test_miss_count_increments(self):
        self.cache.get_entry("ghost")
        self.assertEqual(self.cache.get_miss_count(), 1)

    def test_hit_rate_calculation(self):
        e = self.cache.create_entry("l001", "A")
        self.cache.get_entry(e.simulation_id)
        self.cache.get_entry("ghost")
        self.assertAlmostEqual(self.cache.get_hit_rate(), 0.5)

    def test_reset_stats(self):
        e = self.cache.create_entry("l001", "A")
        self.cache.get_entry(e.simulation_id)
        self.cache.reset_stats()
        self.assertEqual(self.cache.get_hit_count(), 0)

    def test_evict_oldest(self):
        self.cache.create_entry("l001", "A")
        self.cache.create_entry("l002", "B")
        evicted = self.cache.evict_oldest(1)
        self.assertEqual(evicted, 1)
        self.assertEqual(self.cache.get_entry_count(), 1)

    def test_evict_by_layer(self):
        self.cache.create_entry("l001", "A")
        self.cache.create_entry("l001", "B")
        self.cache.create_entry("l002", "C")
        evicted = self.cache.evict_by_layer("l001")
        self.assertEqual(evicted, 2)
        self.assertEqual(self.cache.get_entry_count(), 1)

    def test_evict_unbaked(self):
        e1 = self.cache.create_entry("l001", "A")
        e2 = self.cache.create_entry("l002", "B")
        self.cache.mark_baked(e1.simulation_id)
        evicted = self.cache.evict_unbaked()
        self.assertEqual(evicted, 1)
        self.assertTrue(self.cache.has_entry(e1.simulation_id))
        self.assertFalse(self.cache.has_entry(e2.simulation_id))

    def test_set_policy(self):
        p = ClothCachePolicy(policy_id="custom", max_entries=10)
        self.cache.set_policy(p)
        self.assertEqual(self.cache.get_policy().max_entries, 10)

    def test_save_index(self):
        self.cache.create_entry("l001", "Jacket")
        out = str(TMP_DIR / "cloth_cache_index.json")
        self.assertTrue(self.cache.save_index(out))
        self.assertTrue(Path(out).exists())

    def test_save_index_content(self):
        self.cache.create_entry("l001", "Jacket")
        out = str(TMP_DIR / "cloth_cache_index2.json")
        self.cache.save_index(out)
        data = json.loads(Path(out).read_text())
        self.assertIn("entries", data)
        self.assertIn("entry_count", data)

    def test_total_cache_size_bytes_nonnegative(self):
        self.cache.create_entry("l001", "Jacket")
        self.assertGreaterEqual(self.cache.get_total_cache_size_bytes(), 0)


if __name__ == "__main__":
    unittest.main()
