"""Phase 23B — Tests for ShaderPermutationCache and AssetImportPipeline."""
import json
import sys
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    ShaderPermutationCache,
    ShaderVariant,
    AssetImportPipeline,
    ImportJob,
    ImportSettings,
)

TMP_DIR = Path("/tmp/test_phase23b")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# ShaderVariant dataclass
# ---------------------------------------------------------------------------

class TestShaderVariantDataclass(unittest.TestCase):
    def test_variant_id_field(self):
        v = ShaderVariant("sv_abc", "MyShader")
        self.assertEqual(v.variant_id, "sv_abc")

    def test_shader_name_field(self):
        v = ShaderVariant("sv_abc", "MyShader")
        self.assertEqual(v.shader_name, "MyShader")

    def test_defines_default_empty(self):
        v = ShaderVariant("sv_abc", "MyShader")
        self.assertEqual(v.defines, [])

    def test_stage_default_vertex(self):
        v = ShaderVariant("sv_abc", "MyShader")
        self.assertEqual(v.stage, "vertex")

    def test_age_seconds_positive(self):
        v = ShaderVariant("sv_abc", "MyShader")
        v.compile_time = time.time() - 5.0
        self.assertGreater(v.age_seconds, 0.0)

    def test_define_key_sorted(self):
        v = ShaderVariant("sv_abc", "MyShader", defines=["B", "A"])
        self.assertEqual(v.define_key, "A;B")


# ---------------------------------------------------------------------------
# ShaderPermutationCache — registration & lookup
# ---------------------------------------------------------------------------

class TestShaderPermutationCacheRegistration(unittest.TestCase):
    def setUp(self):
        self.cache = ShaderPermutationCache()

    def test_register_returns_variant(self):
        v = self.cache.register("Shader", ["ALPHA"], stage="fragment")
        self.assertIsInstance(v, ShaderVariant)

    def test_is_cached_true(self):
        self.cache.register("Shader", ["ALPHA"], stage="fragment")
        self.assertTrue(self.cache.is_cached("Shader", ["ALPHA"], stage="fragment"))

    def test_is_cached_false(self):
        self.assertFalse(self.cache.is_cached("Ghost", [], stage="vertex"))

    def test_is_valid_true(self):
        self.cache.register("Shader", ["ALPHA"], stage="vertex", source_hash="abc")
        self.assertTrue(self.cache.is_valid("Shader", ["ALPHA"], stage="vertex", source_hash="abc"))

    def test_is_valid_false_wrong_hash(self):
        self.cache.register("Shader", ["ALPHA"], stage="vertex", source_hash="abc")
        self.assertFalse(self.cache.is_valid("Shader", ["ALPHA"], stage="vertex", source_hash="xyz"))

    def test_is_valid_false_not_cached(self):
        self.assertFalse(self.cache.is_valid("Ghost", [], stage="vertex", source_hash="abc"))

    def test_get_variant_returns_variant(self):
        v = self.cache.register("Shader", ["X"])
        got = self.cache.get_variant(v.variant_id)
        self.assertIsNotNone(got)
        self.assertEqual(got.shader_name, "Shader")

    def test_get_variant_missing_returns_none(self):
        self.assertIsNone(self.cache.get_variant("sv_ghost"))

    def test_get_variant_by_key(self):
        self.cache.register("Shader", ["X"], stage="vertex")
        v = self.cache.get_variant_by_key("Shader", ["X"], stage="vertex")
        self.assertIsNotNone(v)

    def test_get_compiled_hash(self):
        v = self.cache.register("Shader", [], compiled_hash="compiled_abc")
        self.assertEqual(self.cache.get_compiled_hash(v.variant_id), "compiled_abc")

    def test_get_variant_count(self):
        self.cache.register("A", [])
        self.cache.register("B", [])
        self.assertEqual(self.cache.get_variant_count(), 2)

    def test_get_all_variant_ids(self):
        v = self.cache.register("Shader", [])
        self.assertIn(v.variant_id, self.cache.get_all_variant_ids())

    def test_defines_order_irrelevant(self):
        self.cache.register("Shader", ["B", "A"])
        self.assertTrue(self.cache.is_cached("Shader", ["A", "B"]))


# ---------------------------------------------------------------------------
# ShaderPermutationCache — invalidation
# ---------------------------------------------------------------------------

class TestShaderPermutationCacheInvalidation(unittest.TestCase):
    def setUp(self):
        self.cache = ShaderPermutationCache()

    def test_invalidate_returns_true(self):
        self.cache.register("Shader", ["X"])
        self.assertTrue(self.cache.invalidate("Shader", ["X"]))

    def test_invalidate_removes_variant(self):
        self.cache.register("Shader", ["X"])
        self.cache.invalidate("Shader", ["X"])
        self.assertFalse(self.cache.is_cached("Shader", ["X"]))

    def test_invalidate_missing_returns_false(self):
        self.assertFalse(self.cache.invalidate("Ghost", []))

    def test_invalidate_shader_removes_all(self):
        self.cache.register("MyShader", ["A"])
        self.cache.register("MyShader", ["B"])
        self.cache.register("Other", [])
        count = self.cache.invalidate_shader("MyShader")
        self.assertEqual(count, 2)
        self.assertTrue(self.cache.is_cached("Other", []))

    def test_evict_stale(self):
        v = self.cache.register("Old", [])
        v.compile_time = time.time() - 10000.0
        self.cache.register("New", ["X"])
        removed = self.cache.evict_stale(max_age_seconds=5000.0)
        self.assertEqual(removed, 1)
        self.assertFalse(self.cache.is_cached("Old", []))
        self.assertTrue(self.cache.is_cached("New", ["X"]))

    def test_get_stale_variants(self):
        v = self.cache.register("Old", [])
        v.compile_time = time.time() - 200.0
        stale = self.cache.get_stale_variants(max_age_seconds=100.0)
        self.assertEqual(len(stale), 1)

    def test_clear(self):
        self.cache.register("Shader", [])
        self.cache.clear()
        self.assertEqual(self.cache.get_variant_count(), 0)


# ---------------------------------------------------------------------------
# ShaderPermutationCache — queries
# ---------------------------------------------------------------------------

class TestShaderPermutationCacheQueries(unittest.TestCase):
    def setUp(self):
        self.cache = ShaderPermutationCache()
        self.cache.register("Shader", ["A"], stage="vertex", size_bytes=1024)
        self.cache.register("Shader", ["B"], stage="fragment", size_bytes=2048)
        self.cache.register("Other", [], stage="vertex", size_bytes=512)

    def test_get_variants_for_shader(self):
        vs = self.cache.get_variants_for_shader("Shader")
        self.assertEqual(len(vs), 2)

    def test_get_variants_by_stage(self):
        vs = self.cache.get_variants_by_stage("vertex")
        self.assertEqual(len(vs), 2)

    def test_get_total_size_bytes(self):
        self.assertEqual(self.cache.get_total_size_bytes(), 1024 + 2048 + 512)


# ---------------------------------------------------------------------------
# ShaderPermutationCache — persistence
# ---------------------------------------------------------------------------

class TestShaderPermutationCachePersistence(unittest.TestCase):
    def setUp(self):
        self.cache = ShaderPermutationCache()
        self.cache.register("Shader", ["A"], stage="vertex",
                             source_hash="sh1", compiled_hash="ch1", size_bytes=100)

    def test_save_returns_true(self):
        path = str(TMP_DIR / "spc1.json")
        self.assertTrue(self.cache.save(path))

    def test_save_creates_file(self):
        path = str(TMP_DIR / "spc2.json")
        self.cache.save(path)
        self.assertTrue(Path(path).exists())

    def test_load_restores_variant(self):
        path = str(TMP_DIR / "spc3.json")
        self.cache.save(path)
        c2 = ShaderPermutationCache()
        self.assertTrue(c2.load(path))
        self.assertTrue(c2.is_cached("Shader", ["A"], stage="vertex"))

    def test_load_restores_source_hash(self):
        path = str(TMP_DIR / "spc4.json")
        self.cache.save(path)
        c2 = ShaderPermutationCache()
        c2.load(path)
        self.assertTrue(c2.is_valid("Shader", ["A"], stage="vertex", source_hash="sh1"))

    def test_save_no_path_returns_false(self):
        c = ShaderPermutationCache()
        self.assertFalse(c.save())

    def test_load_nonexistent_returns_false(self):
        c = ShaderPermutationCache()
        self.assertFalse(c.load("/no/such/file.json"))


# ---------------------------------------------------------------------------
# ImportSettings dataclass
# ---------------------------------------------------------------------------

class TestImportSettingsDataclass(unittest.TestCase):
    def test_generate_mipmaps_default(self):
        s = ImportSettings()
        self.assertTrue(s.generate_mipmaps)

    def test_compress_textures_default(self):
        s = ImportSettings()
        self.assertTrue(s.compress_textures)

    def test_lod_levels_default(self):
        s = ImportSettings()
        self.assertEqual(s.lod_levels, 3)

    def test_collision_type_default(self):
        s = ImportSettings()
        self.assertEqual(s.collision_type, "none")

    def test_custom_default_empty(self):
        s = ImportSettings()
        self.assertEqual(s.custom, {})


# ---------------------------------------------------------------------------
# ImportJob dataclass
# ---------------------------------------------------------------------------

class TestImportJobDataclass(unittest.TestCase):
    def test_job_id_field(self):
        j = ImportJob("j1", "/src/mesh.fbx", "/dst/mesh", "Mesh")
        self.assertEqual(j.job_id, "j1")

    def test_status_default_pending(self):
        j = ImportJob("j1", "/src", "/dst", "Mesh")
        self.assertEqual(j.status, "pending")

    def test_is_done_false_pending(self):
        j = ImportJob("j1", "/src", "/dst", "Mesh")
        self.assertFalse(j.is_done)

    def test_is_done_true_completed(self):
        j = ImportJob("j1", "/src", "/dst", "Mesh", status="completed")
        self.assertTrue(j.is_done)

    def test_is_done_true_failed(self):
        j = ImportJob("j1", "/src", "/dst", "Mesh", status="failed")
        self.assertTrue(j.is_done)

    def test_duration_seconds_zero_before_completion(self):
        j = ImportJob("j1", "/src", "/dst", "Mesh")
        self.assertEqual(j.duration_seconds, 0.0)

    def test_warnings_default_empty(self):
        j = ImportJob("j1", "/src", "/dst", "Mesh")
        self.assertEqual(j.warnings, [])


# ---------------------------------------------------------------------------
# AssetImportPipeline — submission
# ---------------------------------------------------------------------------

class TestAssetImportPipelineSubmit(unittest.TestCase):
    def setUp(self):
        self.pipeline = AssetImportPipeline()

    def test_submit_returns_job(self):
        j = self.pipeline.submit("/src/mesh.fbx", "/dst/mesh", "Mesh")
        self.assertIsInstance(j, ImportJob)

    def test_submit_sets_status_pending(self):
        j = self.pipeline.submit("/src/mesh.fbx", "/dst/mesh", "Mesh")
        self.assertEqual(j.status, "pending")

    def test_submit_increments_count(self):
        self.pipeline.submit("/src/a.fbx", "/dst/a", "Mesh")
        self.pipeline.submit("/src/b.png", "/dst/b", "Texture")
        self.assertEqual(self.pipeline.get_job_count(), 2)

    def test_cancel_job_returns_true(self):
        j = self.pipeline.submit("/src/a.fbx", "/dst/a", "Mesh")
        self.assertTrue(self.pipeline.cancel_job(j.job_id))

    def test_cancel_job_sets_cancelled(self):
        j = self.pipeline.submit("/src/a.fbx", "/dst/a", "Mesh")
        self.pipeline.cancel_job(j.job_id)
        self.assertEqual(j.status, "cancelled")

    def test_cancel_done_job_returns_false(self):
        j = self.pipeline.submit("/src/a.fbx", "/dst/a", "Mesh")
        j.status = "completed"
        self.assertFalse(self.pipeline.cancel_job(j.job_id))


# ---------------------------------------------------------------------------
# AssetImportPipeline — lifecycle
# ---------------------------------------------------------------------------

class TestAssetImportPipelineLifecycle(unittest.TestCase):
    def setUp(self):
        self.pipeline = AssetImportPipeline()
        self.job = self.pipeline.submit("/src/hero.fbx", "/dst/hero", "Mesh")

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
        self.assertTrue(self.pipeline.complete_job(self.job.job_id, ["/dst/hero.mesh"]))

    def test_complete_job_sets_completed(self):
        self.pipeline.start_job(self.job.job_id)
        self.pipeline.complete_job(self.job.job_id, ["/dst/hero.mesh"])
        self.assertEqual(self.job.status, "completed")

    def test_complete_job_sets_output_paths(self):
        self.pipeline.start_job(self.job.job_id)
        self.pipeline.complete_job(self.job.job_id, ["/dst/hero.mesh"])
        self.assertIn("/dst/hero.mesh", self.job.output_paths)

    def test_fail_job_returns_true(self):
        self.pipeline.start_job(self.job.job_id)
        self.assertTrue(self.pipeline.fail_job(self.job.job_id, "Parse error"))

    def test_fail_job_sets_failed(self):
        self.pipeline.start_job(self.job.job_id)
        self.pipeline.fail_job(self.job.job_id, "Parse error")
        self.assertEqual(self.job.status, "failed")

    def test_fail_job_sets_error_message(self):
        self.pipeline.start_job(self.job.job_id)
        self.pipeline.fail_job(self.job.job_id, "Parse error")
        self.assertEqual(self.job.error_message, "Parse error")

    def test_add_warning(self):
        self.assertTrue(self.pipeline.add_warning(self.job.job_id, "No UV map"))
        self.assertIn("No UV map", self.job.warnings)

    def test_duration_seconds_after_complete(self):
        self.pipeline.start_job(self.job.job_id)
        self.pipeline.complete_job(self.job.job_id)
        self.assertGreaterEqual(self.job.duration_seconds, 0.0)


# ---------------------------------------------------------------------------
# AssetImportPipeline — queries
# ---------------------------------------------------------------------------

class TestAssetImportPipelineQueries(unittest.TestCase):
    def setUp(self):
        self.pipeline = AssetImportPipeline()
        self.j1 = self.pipeline.submit("/s/a.fbx", "/d/a", "Mesh", tags=["hero"])
        self.j2 = self.pipeline.submit("/s/b.png", "/d/b", "Texture")
        self.j3 = self.pipeline.submit("/s/c.wav", "/d/c", "Audio", tags=["hero"])
        self.pipeline.start_job(self.j2.job_id)
        self.pipeline.complete_job(self.j2.job_id)

    def test_get_job(self):
        self.assertIsNotNone(self.pipeline.get_job(self.j1.job_id))

    def test_get_job_missing(self):
        self.assertIsNone(self.pipeline.get_job("ghost"))

    def test_get_all_jobs(self):
        self.assertEqual(len(self.pipeline.get_all_jobs()), 3)

    def test_get_pending_jobs(self):
        pending = self.pipeline.get_pending_jobs()
        self.assertEqual(len(pending), 2)

    def test_get_running_jobs(self):
        self.pipeline.start_job(self.j1.job_id)
        self.assertEqual(len(self.pipeline.get_running_jobs()), 1)

    def test_get_completed_jobs(self):
        completed = self.pipeline.get_completed_jobs()
        self.assertEqual(len(completed), 1)

    def test_get_failed_jobs_empty(self):
        self.assertEqual(len(self.pipeline.get_failed_jobs()), 0)

    def test_get_jobs_by_type(self):
        meshes = self.pipeline.get_jobs_by_type("Mesh")
        self.assertEqual(len(meshes), 1)

    def test_get_jobs_by_tag(self):
        heroes = self.pipeline.get_jobs_by_tag("hero")
        self.assertEqual(len(heroes), 2)

    def test_get_pending_count(self):
        self.assertEqual(self.pipeline.get_pending_count(), 2)

    def test_get_completed_count(self):
        self.assertEqual(self.pipeline.get_completed_count(), 1)

    def test_retry_failed_jobs(self):
        self.pipeline.start_job(self.j3.job_id)
        self.pipeline.fail_job(self.j3.job_id, "Error")
        count = self.pipeline.retry_failed_jobs()
        self.assertEqual(count, 1)
        self.assertEqual(self.j3.status, "pending")

    def test_clear(self):
        self.pipeline.clear()
        self.assertEqual(self.pipeline.get_job_count(), 0)


# ---------------------------------------------------------------------------
# AssetImportPipeline — persistence
# ---------------------------------------------------------------------------

class TestAssetImportPipelinePersistence(unittest.TestCase):
    def setUp(self):
        self.pipeline = AssetImportPipeline()
        j = self.pipeline.submit("/src/mesh.fbx", "/dst/mesh", "Mesh")
        self.pipeline.start_job(j.job_id)
        self.pipeline.complete_job(j.job_id, ["/dst/mesh.mesh"])
        self.pipeline.submit("/src/tex.png", "/dst/tex", "Texture")

    def test_save_returns_true(self):
        path = str(TMP_DIR / "pipeline1.json")
        self.assertTrue(self.pipeline.save(path))

    def test_save_creates_file(self):
        path = str(TMP_DIR / "pipeline2.json")
        self.pipeline.save(path)
        self.assertTrue(Path(path).exists())

    def test_load_restores_job_count(self):
        path = str(TMP_DIR / "pipeline3.json")
        self.pipeline.save(path)
        p2 = AssetImportPipeline()
        self.assertTrue(p2.load(path))
        self.assertEqual(p2.get_job_count(), 2)

    def test_load_restores_statuses(self):
        path = str(TMP_DIR / "pipeline4.json")
        self.pipeline.save(path)
        p2 = AssetImportPipeline()
        p2.load(path)
        completed = p2.get_completed_jobs()
        self.assertEqual(len(completed), 1)

    def test_save_no_path_returns_false(self):
        p = AssetImportPipeline()
        self.assertFalse(p.save())

    def test_load_nonexistent_returns_false(self):
        p = AssetImportPipeline()
        self.assertFalse(p.load("/no/such/file.json"))


# ---------------------------------------------------------------------------
# __init__ exports
# ---------------------------------------------------------------------------

class TestInitExports(unittest.TestCase):
    def test_shader_permutation_cache_exported(self):
        from AtlasAIEngine.intelligence import ShaderPermutationCache as SPC
        self.assertIsNotNone(SPC)

    def test_shader_variant_exported(self):
        from AtlasAIEngine.intelligence import ShaderVariant as SV
        self.assertIsNotNone(SV)

    def test_asset_import_pipeline_exported(self):
        from AtlasAIEngine.intelligence import AssetImportPipeline as AIP
        self.assertIsNotNone(AIP)

    def test_import_job_exported(self):
        from AtlasAIEngine.intelligence import ImportJob as IJ
        self.assertIsNotNone(IJ)

    def test_import_settings_exported(self):
        from AtlasAIEngine.intelligence import ImportSettings as IS
        self.assertIsNotNone(IS)


if __name__ == "__main__":
    unittest.main()
