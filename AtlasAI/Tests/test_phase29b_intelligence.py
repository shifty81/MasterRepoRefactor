"""Phase 29B — Tests for ParticleSystemPipeline and ProceduralMeshPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    ParticleSystemPipeline,
    ParticleEmitterDef,
    ParticleModuleDef,
    ParticlePipelineResult,
    ProceduralMeshPipeline,
    MeshGenerationParams,
    MeshGenerationResult,
    ProceduralMeshBatch,
)


# ---------------------------------------------------------------------------
# ParticleModuleDef dataclass
# ---------------------------------------------------------------------------

class TestParticleModuleDefDataclass(unittest.TestCase):
    def test_module_id_field(self):
        m = ParticleModuleDef(module_id="m001")
        self.assertEqual(m.module_id, "m001")

    def test_default_module_type(self):
        m = ParticleModuleDef(module_id="m001")
        self.assertEqual(m.module_type, "Spawn")

    def test_default_enabled(self):
        m = ParticleModuleDef(module_id="m001")
        self.assertTrue(m.enabled)

    def test_default_priority(self):
        m = ParticleModuleDef(module_id="m001")
        self.assertEqual(m.priority, 0)

    def test_is_active_true(self):
        m = ParticleModuleDef(module_id="m001", module_type="Color")
        self.assertTrue(m.is_active)

    def test_is_active_false_when_disabled(self):
        m = ParticleModuleDef(module_id="m001", enabled=False)
        self.assertFalse(m.is_active)

    def test_is_active_false_when_empty_type(self):
        m = ParticleModuleDef(module_id="m001", module_type="")
        self.assertFalse(m.is_active)


# ---------------------------------------------------------------------------
# ParticleEmitterDef dataclass
# ---------------------------------------------------------------------------

class TestParticleEmitterDefDataclass(unittest.TestCase):
    def test_emitter_id_field(self):
        e = ParticleEmitterDef(emitter_id="e001", name="Fire")
        self.assertEqual(e.emitter_id, "e001")

    def test_name_field(self):
        e = ParticleEmitterDef(emitter_id="e001", name="Fire")
        self.assertEqual(e.name, "Fire")

    def test_default_shape(self):
        e = ParticleEmitterDef(emitter_id="e001", name="Fire")
        self.assertEqual(e.shape, "Point")

    def test_default_spawn_rate(self):
        e = ParticleEmitterDef(emitter_id="e001", name="Fire")
        self.assertAlmostEqual(e.spawn_rate, 10.0)

    def test_default_lifetime(self):
        e = ParticleEmitterDef(emitter_id="e001", name="Fire")
        self.assertAlmostEqual(e.lifetime, 2.0)

    def test_default_loop(self):
        e = ParticleEmitterDef(emitter_id="e001", name="Fire")
        self.assertTrue(e.is_looping)

    def test_has_modules_false_empty(self):
        e = ParticleEmitterDef(emitter_id="e001", name="Fire")
        self.assertFalse(e.has_modules)

    def test_has_modules_true(self):
        m = ParticleModuleDef(module_id="m001")
        e = ParticleEmitterDef(emitter_id="e001", name="Fire", modules=[m])
        self.assertTrue(e.has_modules)

    def test_active_module_count(self):
        m1 = ParticleModuleDef(module_id="m001", enabled=True)
        m2 = ParticleModuleDef(module_id="m002", enabled=False)
        e = ParticleEmitterDef(emitter_id="e001", name="Fire", modules=[m1, m2])
        self.assertEqual(e.active_module_count, 1)


# ---------------------------------------------------------------------------
# ParticlePipelineResult dataclass
# ---------------------------------------------------------------------------

class TestParticlePipelineResultDataclass(unittest.TestCase):
    def test_job_id_field(self):
        r = ParticlePipelineResult(job_id="j001")
        self.assertEqual(r.job_id, "j001")

    def test_default_success(self):
        r = ParticlePipelineResult(job_id="j001")
        self.assertTrue(r.success)

    def test_has_errors_false(self):
        r = ParticlePipelineResult(job_id="j001")
        self.assertFalse(r.has_errors)

    def test_has_errors_true(self):
        r = ParticlePipelineResult(job_id="j001", errors=["bad emitter"])
        self.assertTrue(r.has_errors)

    def test_total_processed(self):
        r = ParticlePipelineResult(job_id="j001", emitter_count=3, module_count=5)
        self.assertEqual(r.total_processed, 8)


# ---------------------------------------------------------------------------
# ParticleSystemPipeline
# ---------------------------------------------------------------------------

class TestParticleSystemPipelineBasic(unittest.TestCase):
    def setUp(self):
        self.pipeline = ParticleSystemPipeline()

    def test_initial_empty(self):
        self.assertTrue(self.pipeline.is_empty)

    def test_add_emitter(self):
        e = ParticleEmitterDef(emitter_id="e001", name="Sparks")
        self.pipeline.add_emitter(e)
        self.assertEqual(self.pipeline.emitter_count, 1)

    def test_get_emitter(self):
        e = ParticleEmitterDef(emitter_id="e001", name="Sparks")
        self.pipeline.add_emitter(e)
        fetched = self.pipeline.get_emitter("e001")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "Sparks")

    def test_get_emitter_missing(self):
        self.assertIsNone(self.pipeline.get_emitter("nope"))

    def test_remove_emitter(self):
        e = ParticleEmitterDef(emitter_id="e001", name="Sparks")
        self.pipeline.add_emitter(e)
        result = self.pipeline.remove_emitter("e001")
        self.assertTrue(result)
        self.assertEqual(self.pipeline.emitter_count, 0)

    def test_remove_emitter_missing(self):
        self.assertFalse(self.pipeline.remove_emitter("ghost"))

    def test_get_all_emitters(self):
        self.pipeline.add_emitter(ParticleEmitterDef(emitter_id="e001", name="A"))
        self.pipeline.add_emitter(ParticleEmitterDef(emitter_id="e002", name="B"))
        self.assertEqual(len(self.pipeline.get_all_emitters()), 2)

    def test_clear(self):
        self.pipeline.add_emitter(ParticleEmitterDef(emitter_id="e001", name="A"))
        self.pipeline.clear()
        self.assertTrue(self.pipeline.is_empty)


class TestParticleSystemPipelineCompile(unittest.TestCase):
    def setUp(self):
        self.pipeline = ParticleSystemPipeline()

    def test_compile_empty(self):
        result = self.pipeline.compile()
        self.assertTrue(result.success)
        self.assertEqual(result.emitter_count, 0)

    def test_compile_valid_emitters(self):
        self.pipeline.add_emitter(ParticleEmitterDef(emitter_id="e001", name="Smoke"))
        self.pipeline.add_emitter(ParticleEmitterDef(emitter_id="e002", name="Fire"))
        result = self.pipeline.compile()
        self.assertTrue(result.success)
        self.assertEqual(result.emitter_count, 2)

    def test_compile_with_modules(self):
        m = ParticleModuleDef(module_id="m001", module_type="Color")
        e = ParticleEmitterDef(emitter_id="e001", name="Sparks", modules=[m])
        self.pipeline.add_emitter(e)
        result = self.pipeline.compile()
        self.assertEqual(result.module_count, 1)

    def test_compile_invalid_emitter(self):
        e = ParticleEmitterDef(emitter_id="e001", name="Bad", spawn_rate=-1.0)
        self.pipeline.add_emitter(e)
        result = self.pipeline.compile()
        self.assertFalse(result.success)
        self.assertTrue(result.has_errors)

    def test_validate_emitter_valid(self):
        e = ParticleEmitterDef(emitter_id="e001", name="Fire")
        self.assertTrue(self.pipeline.validate_emitter(e))

    def test_validate_emitter_invalid_no_name(self):
        e = ParticleEmitterDef(emitter_id="e001", name="")
        self.assertFalse(self.pipeline.validate_emitter(e))


# ---------------------------------------------------------------------------
# MeshGenerationParams dataclass
# ---------------------------------------------------------------------------

class TestMeshGenerationParamsDataclass(unittest.TestCase):
    def test_param_id(self):
        p = MeshGenerationParams(param_id="p001")
        self.assertEqual(p.param_id, "p001")

    def test_default_mesh_type(self):
        p = MeshGenerationParams(param_id="p001")
        self.assertEqual(p.mesh_type, "Plane")

    def test_default_resolution(self):
        p = MeshGenerationParams(param_id="p001")
        self.assertEqual(p.resolution_u, 8)
        self.assertEqual(p.resolution_v, 8)

    def test_vertex_estimate(self):
        p = MeshGenerationParams(param_id="p001", resolution_u=3, resolution_v=3)
        self.assertEqual(p.vertex_estimate, 16)

    def test_is_subdivided_true(self):
        p = MeshGenerationParams(param_id="p001", resolution_u=4, resolution_v=4)
        self.assertTrue(p.is_subdivided)

    def test_is_subdivided_false(self):
        p = MeshGenerationParams(param_id="p001", resolution_u=1, resolution_v=1)
        self.assertFalse(p.is_subdivided)


# ---------------------------------------------------------------------------
# MeshGenerationResult dataclass
# ---------------------------------------------------------------------------

class TestMeshGenerationResultDataclass(unittest.TestCase):
    def test_result_id(self):
        r = MeshGenerationResult(result_id="r001")
        self.assertEqual(r.result_id, "r001")

    def test_default_success(self):
        r = MeshGenerationResult(result_id="r001")
        self.assertTrue(r.success)

    def test_is_valid(self):
        r = MeshGenerationResult(result_id="r001", success=True, vertex_count=10)
        self.assertTrue(r.is_valid)

    def test_not_valid_with_errors(self):
        r = MeshGenerationResult(result_id="r001", errors=["oops"])
        self.assertFalse(r.is_valid)

    def test_total_primitives(self):
        r = MeshGenerationResult(result_id="r001", vertex_count=10, triangle_count=8)
        self.assertEqual(r.total_primitives, 18)


# ---------------------------------------------------------------------------
# ProceduralMeshBatch dataclass
# ---------------------------------------------------------------------------

class TestProceduralMeshBatchDataclass(unittest.TestCase):
    def test_batch_id(self):
        b = ProceduralMeshBatch(batch_id="b001")
        self.assertEqual(b.batch_id, "b001")

    def test_empty_batch(self):
        b = ProceduralMeshBatch(batch_id="b001")
        self.assertTrue(b.is_empty)
        self.assertEqual(b.count, 0)

    def test_batch_count(self):
        p1 = MeshGenerationParams(param_id="p001")
        p2 = MeshGenerationParams(param_id="p002")
        b = ProceduralMeshBatch(batch_id="b001", params=[p1, p2])
        self.assertEqual(b.count, 2)
        self.assertFalse(b.is_empty)


# ---------------------------------------------------------------------------
# ProceduralMeshPipeline
# ---------------------------------------------------------------------------

class TestProceduralMeshPipelineGenerate(unittest.TestCase):
    def setUp(self):
        self.pipeline = ProceduralMeshPipeline()

    def test_generate_valid(self):
        p = MeshGenerationParams(param_id="p001", mesh_type="Plane")
        result = self.pipeline.generate(p)
        self.assertTrue(result.success)
        self.assertTrue(result.is_valid)

    def test_generate_invalid_type(self):
        p = MeshGenerationParams(param_id="p001", mesh_type="BadType")
        result = self.pipeline.generate(p)
        self.assertFalse(result.success)

    def test_generate_vertex_count(self):
        p = MeshGenerationParams(param_id="p001", resolution_u=3, resolution_v=3)
        result = self.pipeline.generate(p)
        self.assertEqual(result.vertex_count, 16)

    def test_generate_triangle_count(self):
        p = MeshGenerationParams(param_id="p001", resolution_u=3, resolution_v=3)
        result = self.pipeline.generate(p)
        self.assertEqual(result.triangle_count, 18)

    def test_generate_caches_result(self):
        p = MeshGenerationParams(param_id="p001", mesh_type="Sphere")
        self.pipeline.generate(p)
        self.assertEqual(self.pipeline.cache_size, 1)

    def test_clear_cache(self):
        p = MeshGenerationParams(param_id="p001")
        self.pipeline.generate(p)
        self.pipeline.clear_cache()
        self.assertEqual(self.pipeline.cache_size, 0)

    def test_generate_batch(self):
        b = ProceduralMeshBatch(
            batch_id="b001",
            params=[
                MeshGenerationParams(param_id="p001", mesh_type="Box"),
                MeshGenerationParams(param_id="p002", mesh_type="Cylinder"),
            ],
        )
        results = self.pipeline.generate_batch(b)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r.success for r in results))

    def test_get_supported_types(self):
        types = self.pipeline.get_supported_types()
        self.assertIn("Plane", types)
        self.assertIn("Sphere", types)
        self.assertIn("Box", types)

    def test_validate_valid(self):
        p = MeshGenerationParams(param_id="p001", mesh_type="Cone")
        self.assertTrue(self.pipeline.validate(p))

    def test_validate_invalid_resolution(self):
        p = MeshGenerationParams(param_id="p001", mesh_type="Plane", resolution_u=0)
        self.assertFalse(self.pipeline.validate(p))


if __name__ == "__main__":
    unittest.main()
