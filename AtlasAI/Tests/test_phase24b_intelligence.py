"""Phase 24B — Tests for TextureAtlasPacker and LODGenerationPipeline."""
import json
import sys
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    TextureAtlasPacker,
    AtlasSheet,
    AtlasRegion,
    LODGenerationPipeline,
    LODJob,
    LODSettings,
    LODResult,
)

TMP_DIR = Path("/tmp/test_phase24b")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# AtlasSheet dataclass
# ---------------------------------------------------------------------------

class TestAtlasSheetDataclass(unittest.TestCase):
    def test_sheet_id_field(self):
        s = AtlasSheet("s001", "ui_atlas")
        self.assertEqual(s.sheet_id, "s001")

    def test_name_field(self):
        s = AtlasSheet("s001", "ui_atlas")
        self.assertEqual(s.name, "ui_atlas")

    def test_default_dimensions(self):
        s = AtlasSheet("s001", "ui_atlas")
        self.assertEqual(s.width, 2048)
        self.assertEqual(s.height, 2048)

    def test_region_count_empty(self):
        s = AtlasSheet("s001", "ui_atlas")
        self.assertEqual(s.region_count, 0)

    def test_fill_ratio_empty(self):
        s = AtlasSheet("s001", "ui_atlas")
        self.assertAlmostEqual(s.fill_ratio, 0.0)


# ---------------------------------------------------------------------------
# AtlasRegion dataclass
# ---------------------------------------------------------------------------

class TestAtlasRegionDataclass(unittest.TestCase):
    def test_region_id_field(self):
        r = AtlasRegion("r001", "/tex/icon.png", "s001", 0, 0, 64, 64)
        self.assertEqual(r.region_id, "r001")

    def test_source_path_field(self):
        r = AtlasRegion("r001", "/tex/icon.png", "s001")
        self.assertEqual(r.source_path, "/tex/icon.png")

    def test_sheet_id_field(self):
        r = AtlasRegion("r001", "/tex/icon.png", "s001")
        self.assertEqual(r.sheet_id, "s001")

    def test_uv_x_zero(self):
        r = AtlasRegion("r001", "/t", "s001", 0, 0, 64, 64, _sheet_width=2048, _sheet_height=2048)
        self.assertAlmostEqual(r.uv_x, 0.0)

    def test_uv_width_fraction(self):
        r = AtlasRegion("r001", "/t", "s001", 0, 0, 64, 64, _sheet_width=2048, _sheet_height=2048)
        self.assertAlmostEqual(r.uv_width, 64 / 2048)


# ---------------------------------------------------------------------------
# TextureAtlasPacker — sheet management
# ---------------------------------------------------------------------------

class TestTextureAtlasPackerSheets(unittest.TestCase):
    def setUp(self):
        self.packer = TextureAtlasPacker()

    def test_create_sheet_returns_sheet(self):
        s = self.packer.create_sheet("ui")
        self.assertIsInstance(s, AtlasSheet)

    def test_get_sheet_count(self):
        self.packer.create_sheet("ui")
        self.packer.create_sheet("world")
        self.assertEqual(self.packer.get_sheet_count(), 2)

    def test_get_all_sheet_ids(self):
        s = self.packer.create_sheet("ui")
        self.assertIn(s.sheet_id, self.packer.get_all_sheet_ids())

    def test_get_sheet_by_id(self):
        s = self.packer.create_sheet("ui")
        got = self.packer.get_sheet(s.sheet_id)
        self.assertIsNotNone(got)
        self.assertEqual(got.name, "ui")

    def test_get_sheet_missing_returns_none(self):
        self.assertIsNone(self.packer.get_sheet("ghost"))

    def test_get_sheet_by_name(self):
        self.packer.create_sheet("special")
        s = self.packer.get_sheet_by_name("special")
        self.assertIsNotNone(s)

    def test_get_sheet_by_name_missing(self):
        self.assertIsNone(self.packer.get_sheet_by_name("ghost"))

    def test_remove_sheet_returns_true(self):
        s = self.packer.create_sheet("ui")
        self.assertTrue(self.packer.remove_sheet(s.sheet_id))

    def test_remove_sheet_removes_it(self):
        s = self.packer.create_sheet("ui")
        self.packer.remove_sheet(s.sheet_id)
        self.assertIsNone(self.packer.get_sheet(s.sheet_id))

    def test_remove_sheet_missing_returns_false(self):
        self.assertFalse(self.packer.remove_sheet("ghost"))


# ---------------------------------------------------------------------------
# TextureAtlasPacker — packing
# ---------------------------------------------------------------------------

class TestTextureAtlasPackerPacking(unittest.TestCase):
    def setUp(self):
        self.packer = TextureAtlasPacker()
        self.sheet = self.packer.create_sheet("ui", 2048, 2048)

    def test_pack_texture_returns_region(self):
        r = self.packer.pack_texture(self.sheet.sheet_id, "/tex/a.png", 64, 64)
        self.assertIsInstance(r, AtlasRegion)

    def test_pack_texture_increases_region_count(self):
        self.packer.pack_texture(self.sheet.sheet_id, "/tex/a.png", 64, 64)
        self.packer.pack_texture(self.sheet.sheet_id, "/tex/b.png", 128, 128)
        self.assertEqual(self.packer.get_region_count(), 2)

    def test_pack_texture_adds_to_sheet(self):
        self.packer.pack_texture(self.sheet.sheet_id, "/tex/a.png", 64, 64)
        self.assertEqual(self.sheet.region_count, 1)

    def test_pack_texture_missing_sheet_returns_none(self):
        r = self.packer.pack_texture("ghost", "/tex/a.png", 64, 64)
        self.assertIsNone(r)

    def test_get_region_returns_region(self):
        r = self.packer.pack_texture(self.sheet.sheet_id, "/tex/a.png", 64, 64)
        got = self.packer.get_region(r.region_id)
        self.assertIsNotNone(got)

    def test_get_region_missing_returns_none(self):
        self.assertIsNone(self.packer.get_region("ghost"))

    def test_find_region_by_source(self):
        self.packer.pack_texture(self.sheet.sheet_id, "/tex/icon.png", 32, 32)
        r = self.packer.find_region_by_source("/tex/icon.png")
        self.assertIsNotNone(r)

    def test_find_region_by_source_missing(self):
        self.assertIsNone(self.packer.find_region_by_source("/ghost.png"))

    def test_remove_region_returns_true(self):
        r = self.packer.pack_texture(self.sheet.sheet_id, "/tex/a.png", 64, 64)
        self.assertTrue(self.packer.remove_region(r.region_id))

    def test_remove_region_decreases_count(self):
        r = self.packer.pack_texture(self.sheet.sheet_id, "/tex/a.png", 64, 64)
        self.packer.remove_region(r.region_id)
        self.assertEqual(self.packer.get_region_count(), 0)

    def test_remove_region_missing_returns_false(self):
        self.assertFalse(self.packer.remove_region("ghost"))

    def test_uv_coords_in_range(self):
        r = self.packer.pack_texture(self.sheet.sheet_id, "/tex/a.png", 64, 64)
        self.assertGreaterEqual(r.uv_x, 0.0)
        self.assertLessEqual(r.uv_x + r.uv_width, 1.0)
        self.assertGreaterEqual(r.uv_y, 0.0)
        self.assertLessEqual(r.uv_y + r.uv_height, 1.0)

    def test_oversized_texture_returns_none(self):
        small_sheet = self.packer.create_sheet("tiny", 16, 16)
        r = self.packer.pack_texture(small_sheet.sheet_id, "/tex/huge.png", 512, 512)
        self.assertIsNone(r)


# ---------------------------------------------------------------------------
# TextureAtlasPacker — resize / grow
# ---------------------------------------------------------------------------

class TestTextureAtlasPackerResize(unittest.TestCase):
    def setUp(self):
        self.packer = TextureAtlasPacker()
        self.sheet = self.packer.create_sheet("ui", 1024, 1024, max_size=4096)

    def test_resize_sheet_returns_true(self):
        self.assertTrue(self.packer.resize_sheet(self.sheet.sheet_id, 2048, 2048))

    def test_resize_sheet_updates_dimensions(self):
        self.packer.resize_sheet(self.sheet.sheet_id, 2048, 2048)
        self.assertEqual(self.sheet.width, 2048)

    def test_resize_beyond_max_returns_false(self):
        self.assertFalse(self.packer.resize_sheet(self.sheet.sheet_id, 8192, 8192))

    def test_resize_missing_sheet_returns_false(self):
        self.assertFalse(self.packer.resize_sheet("ghost", 2048, 2048))

    def test_grow_sheet_doubles_size(self):
        self.packer.grow_sheet(self.sheet.sheet_id)
        self.assertEqual(self.sheet.width, 2048)

    def test_grow_sheet_at_max_returns_false(self):
        self.packer.resize_sheet(self.sheet.sheet_id, 4096, 4096)
        self.assertFalse(self.packer.grow_sheet(self.sheet.sheet_id))

    def test_clear(self):
        self.packer.pack_texture(self.sheet.sheet_id, "/a.png", 64, 64)
        self.packer.clear()
        self.assertEqual(self.packer.get_sheet_count(), 0)
        self.assertEqual(self.packer.get_region_count(), 0)


# ---------------------------------------------------------------------------
# TextureAtlasPacker — persistence
# ---------------------------------------------------------------------------

class TestTextureAtlasPackerPersistence(unittest.TestCase):
    def setUp(self):
        self.packer = TextureAtlasPacker()
        s = self.packer.create_sheet("ui", 1024, 1024)
        self.packer.pack_texture(s.sheet_id, "/tex/a.png", 64, 64)
        self.packer.pack_texture(s.sheet_id, "/tex/b.png", 32, 32)

    def test_save_returns_true(self):
        self.assertTrue(self.packer.save(str(TMP_DIR / "atlas1.json")))

    def test_save_creates_file(self):
        path = str(TMP_DIR / "atlas2.json")
        self.packer.save(path)
        self.assertTrue(Path(path).exists())

    def test_load_restores_sheet_count(self):
        path = str(TMP_DIR / "atlas3.json")
        self.packer.save(path)
        p2 = TextureAtlasPacker()
        self.assertTrue(p2.load(path))
        self.assertEqual(p2.get_sheet_count(), 1)

    def test_load_restores_region_count(self):
        path = str(TMP_DIR / "atlas4.json")
        self.packer.save(path)
        p2 = TextureAtlasPacker()
        p2.load(path)
        self.assertEqual(p2.get_region_count(), 2)

    def test_load_nonexistent_returns_false(self):
        p = TextureAtlasPacker()
        self.assertFalse(p.load("/no/such/file.json"))


# ---------------------------------------------------------------------------
# LODSettings dataclass
# ---------------------------------------------------------------------------

class TestLODSettingsDataclass(unittest.TestCase):
    def test_default_reduction(self):
        s = LODSettings()
        self.assertAlmostEqual(s.target_reduction, 0.5)

    def test_default_screen_size_threshold(self):
        s = LODSettings()
        self.assertAlmostEqual(s.screen_size_threshold, 0.1)

    def test_simplification_mode_default(self):
        s = LODSettings()
        self.assertEqual(s.simplification_mode, "quadric")

    def test_preserve_borders_default(self):
        s = LODSettings()
        self.assertTrue(s.preserve_borders)


# ---------------------------------------------------------------------------
# LODResult dataclass
# ---------------------------------------------------------------------------

class TestLODResultDataclass(unittest.TestCase):
    def test_lod_index_field(self):
        r = LODResult(lod_index=2, input_tri_count=1000, output_tri_count=250)
        self.assertEqual(r.lod_index, 2)

    def test_actual_reduction(self):
        r = LODResult(lod_index=0, input_tri_count=1000, output_tri_count=500)
        self.assertAlmostEqual(r.actual_reduction, 0.5)

    def test_actual_reduction_zero_input(self):
        r = LODResult(lod_index=0, input_tri_count=0, output_tri_count=0)
        self.assertEqual(r.actual_reduction, 0.0)

    def test_output_paths_empty(self):
        j = LODJob("j1", "/src", "/dst", "mesh")
        self.assertEqual(j.output_paths, [])


# ---------------------------------------------------------------------------
# LODJob dataclass
# ---------------------------------------------------------------------------

class TestLODJobDataclass(unittest.TestCase):
    def test_job_id_field(self):
        j = LODJob("j1", "/src/mesh.fbx", "/dst/", "hero")
        self.assertEqual(j.job_id, "j1")

    def test_status_default_pending(self):
        j = LODJob("j1", "/src", "/dst", "hero")
        self.assertEqual(j.status, "pending")

    def test_is_done_false_pending(self):
        j = LODJob("j1", "/src", "/dst", "hero")
        self.assertFalse(j.is_done)

    def test_is_done_true_completed(self):
        j = LODJob("j1", "/src", "/dst", "hero", status="completed")
        self.assertTrue(j.is_done)

    def test_duration_seconds_zero(self):
        j = LODJob("j1", "/src", "/dst", "hero")
        self.assertEqual(j.duration_seconds, 0.0)


# ---------------------------------------------------------------------------
# LODGenerationPipeline — submission
# ---------------------------------------------------------------------------

class TestLODGenerationPipelineSubmit(unittest.TestCase):
    def setUp(self):
        self.pipeline = LODGenerationPipeline()

    def test_submit_returns_job(self):
        j = self.pipeline.submit("/src/mesh.fbx", "/dst/", "hero")
        self.assertIsInstance(j, LODJob)

    def test_submit_default_settings_populated(self):
        j = self.pipeline.submit("/src/mesh.fbx", "/dst/", "hero", lod_count=3)
        self.assertEqual(len(j.settings), 3)

    def test_submit_increments_count(self):
        self.pipeline.submit("/src/a.fbx", "/dst/", "a")
        self.pipeline.submit("/src/b.fbx", "/dst/", "b")
        self.assertEqual(self.pipeline.get_job_count(), 2)

    def test_cancel_job_returns_true(self):
        j = self.pipeline.submit("/src/a.fbx", "/dst/", "a")
        self.assertTrue(self.pipeline.cancel_job(j.job_id))

    def test_cancel_job_sets_cancelled(self):
        j = self.pipeline.submit("/src/a.fbx", "/dst/", "a")
        self.pipeline.cancel_job(j.job_id)
        self.assertEqual(j.status, "cancelled")

    def test_cancel_done_job_returns_false(self):
        j = self.pipeline.submit("/src/a.fbx", "/dst/", "a")
        j.status = "completed"
        self.assertFalse(self.pipeline.cancel_job(j.job_id))


# ---------------------------------------------------------------------------
# LODGenerationPipeline — lifecycle
# ---------------------------------------------------------------------------

class TestLODGenerationPipelineLifecycle(unittest.TestCase):
    def setUp(self):
        self.pipeline = LODGenerationPipeline()
        self.job = self.pipeline.submit("/src/hero.fbx", "/dst/hero", "hero")

    def test_start_job_returns_true(self):
        self.assertTrue(self.pipeline.start_job(self.job.job_id))

    def test_start_job_sets_running(self):
        self.pipeline.start_job(self.job.job_id)
        self.assertEqual(self.job.status, "running")

    def test_start_job_already_running_returns_false(self):
        self.pipeline.start_job(self.job.job_id)
        self.assertFalse(self.pipeline.start_job(self.job.job_id))

    def test_complete_job_returns_true(self):
        self.pipeline.start_job(self.job.job_id)
        results = [LODResult(lod_index=0, input_tri_count=1000, output_tri_count=500)]
        self.assertTrue(self.pipeline.complete_job(self.job.job_id, results))

    def test_complete_job_sets_completed(self):
        self.pipeline.start_job(self.job.job_id)
        self.pipeline.complete_job(self.job.job_id)
        self.assertEqual(self.job.status, "completed")

    def test_complete_job_stores_results(self):
        self.pipeline.start_job(self.job.job_id)
        results = [LODResult(lod_index=0, input_tri_count=1000, output_tri_count=500)]
        self.pipeline.complete_job(self.job.job_id, results)
        self.assertEqual(len(self.job.results), 1)

    def test_fail_job_sets_failed(self):
        self.pipeline.start_job(self.job.job_id)
        self.pipeline.fail_job(self.job.job_id, "Mesh corrupt")
        self.assertEqual(self.job.status, "failed")

    def test_fail_job_stores_error(self):
        self.pipeline.start_job(self.job.job_id)
        self.pipeline.fail_job(self.job.job_id, "Mesh corrupt")
        self.assertEqual(self.job.error_message, "Mesh corrupt")

    def test_add_warning(self):
        self.assertTrue(self.pipeline.add_warning(self.job.job_id, "No UV channel"))
        self.assertIn("No UV channel", self.job.warnings)


# ---------------------------------------------------------------------------
# LODGenerationPipeline — queries
# ---------------------------------------------------------------------------

class TestLODGenerationPipelineQueries(unittest.TestCase):
    def setUp(self):
        self.pipeline = LODGenerationPipeline()
        self.j1 = self.pipeline.submit("/s/a.fbx", "/d/", "a", tags=["hero"])
        self.j2 = self.pipeline.submit("/s/b.fbx", "/d/", "b")
        self.pipeline.start_job(self.j2.job_id)
        self.pipeline.complete_job(self.j2.job_id)

    def test_get_job(self):
        self.assertIsNotNone(self.pipeline.get_job(self.j1.job_id))

    def test_get_all_jobs(self):
        self.assertEqual(len(self.pipeline.get_all_jobs()), 2)

    def test_get_pending_jobs(self):
        self.assertEqual(len(self.pipeline.get_pending_jobs()), 1)

    def test_get_completed_jobs(self):
        self.assertEqual(len(self.pipeline.get_completed_jobs()), 1)

    def test_get_failed_jobs_empty(self):
        self.assertEqual(len(self.pipeline.get_failed_jobs()), 0)

    def test_get_jobs_by_tag(self):
        heroes = self.pipeline.get_jobs_by_tag("hero")
        self.assertEqual(len(heroes), 1)

    def test_retry_failed_jobs(self):
        self.pipeline.start_job(self.j1.job_id)
        self.pipeline.fail_job(self.j1.job_id, "Error")
        count = self.pipeline.retry_failed_jobs()
        self.assertEqual(count, 1)
        self.assertEqual(self.j1.status, "pending")

    def test_get_average_lod_count(self):
        self.assertGreater(self.pipeline.get_average_lod_count(), 0.0)

    def test_clear(self):
        self.pipeline.clear()
        self.assertEqual(self.pipeline.get_job_count(), 0)


# ---------------------------------------------------------------------------
# LODGenerationPipeline — persistence
# ---------------------------------------------------------------------------

class TestLODGenerationPipelinePersistence(unittest.TestCase):
    def setUp(self):
        self.pipeline = LODGenerationPipeline()
        j = self.pipeline.submit("/src/mesh.fbx", "/dst/", "hero", lod_count=3)
        self.pipeline.start_job(j.job_id)
        results = [
            LODResult(lod_index=0, input_tri_count=1000, output_tri_count=500,
                      output_path="/dst/hero_lod0.mesh"),
            LODResult(lod_index=1, input_tri_count=1000, output_tri_count=200,
                      output_path="/dst/hero_lod1.mesh"),
        ]
        self.pipeline.complete_job(j.job_id, results)

    def test_save_returns_true(self):
        self.assertTrue(self.pipeline.save(str(TMP_DIR / "lod1.json")))

    def test_save_creates_file(self):
        path = str(TMP_DIR / "lod2.json")
        self.pipeline.save(path)
        self.assertTrue(Path(path).exists())

    def test_load_restores_job_count(self):
        path = str(TMP_DIR / "lod3.json")
        self.pipeline.save(path)
        p2 = LODGenerationPipeline()
        self.assertTrue(p2.load(path))
        self.assertEqual(p2.get_job_count(), 1)

    def test_load_restores_results(self):
        path = str(TMP_DIR / "lod4.json")
        self.pipeline.save(path)
        p2 = LODGenerationPipeline()
        p2.load(path)
        jobs = p2.get_all_jobs()
        self.assertEqual(len(jobs[0].results), 2)

    def test_save_no_path_returns_false(self):
        p = LODGenerationPipeline()
        self.assertFalse(p.save())

    def test_load_nonexistent_returns_false(self):
        p = LODGenerationPipeline()
        self.assertFalse(p.load("/no/such/file.json"))


# ---------------------------------------------------------------------------
# __init__ exports
# ---------------------------------------------------------------------------

class TestInitExports(unittest.TestCase):
    def test_texture_atlas_packer_exported(self):
        from AtlasAIEngine.intelligence import TextureAtlasPacker as TAP
        self.assertIsNotNone(TAP)

    def test_atlas_sheet_exported(self):
        from AtlasAIEngine.intelligence import AtlasSheet as AS
        self.assertIsNotNone(AS)

    def test_atlas_region_exported(self):
        from AtlasAIEngine.intelligence import AtlasRegion as AR
        self.assertIsNotNone(AR)

    def test_lod_generation_pipeline_exported(self):
        from AtlasAIEngine.intelligence import LODGenerationPipeline as LGP
        self.assertIsNotNone(LGP)

    def test_lod_job_exported(self):
        from AtlasAIEngine.intelligence import LODJob as LJ
        self.assertIsNotNone(LJ)

    def test_lod_settings_exported(self):
        from AtlasAIEngine.intelligence import LODSettings as LS
        self.assertIsNotNone(LS)

    def test_lod_result_exported(self):
        from AtlasAIEngine.intelligence import LODResult as LR
        self.assertIsNotNone(LR)


if __name__ == "__main__":
    unittest.main()
