"""Phase 31B — Tests for LightingBakePipeline and CollisionMeshPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    LightingBakePipeline,
    BakePassDef,
    LightmapEntry,
    BakeBudget,
    CollisionMeshPipeline,
    CollisionShapeDef,
    CollisionMeshEntry,
    CollisionBuildResult,
)


# ---------------------------------------------------------------------------
# BakePassDef
# ---------------------------------------------------------------------------

class TestBakePassDef(unittest.TestCase):
    def test_pass_id(self):
        p = BakePassDef(pass_id="p001", pass_name="Direct Pass")
        self.assertEqual(p.pass_id, "p001")

    def test_pass_name(self):
        p = BakePassDef(pass_id="p001", pass_name="Direct Pass")
        self.assertEqual(p.pass_name, "Direct Pass")

    def test_default_pass_type(self):
        p = BakePassDef(pass_id="p001", pass_name="Direct Pass")
        self.assertEqual(p.pass_type, "Direct")

    def test_default_resolution(self):
        p = BakePassDef(pass_id="p001", pass_name="Direct Pass")
        self.assertEqual(p.resolution, 512)

    def test_default_samples(self):
        p = BakePassDef(pass_id="p001", pass_name="Direct Pass")
        self.assertEqual(p.samples, 64)

    def test_is_enabled(self):
        p = BakePassDef(pass_id="p001", pass_name="Direct Pass", enabled=True)
        self.assertTrue(p.is_enabled)

    def test_is_high_res_false(self):
        p = BakePassDef(pass_id="p001", pass_name="Direct Pass", resolution=512)
        self.assertFalse(p.is_high_res)


# ---------------------------------------------------------------------------
# LightmapEntry
# ---------------------------------------------------------------------------

class TestLightmapEntry(unittest.TestCase):
    def test_entry_id(self):
        e = LightmapEntry(entry_id="e001", mesh_path="meshes/wall.fbx")
        self.assertEqual(e.entry_id, "e001")

    def test_mesh_path(self):
        e = LightmapEntry(entry_id="e001", mesh_path="meshes/wall.fbx")
        self.assertEqual(e.mesh_path, "meshes/wall.fbx")

    def test_default_lightmap_path(self):
        e = LightmapEntry(entry_id="e001", mesh_path="meshes/wall.fbx")
        self.assertEqual(e.lightmap_path, "")

    def test_default_uv_channel(self):
        e = LightmapEntry(entry_id="e001", mesh_path="meshes/wall.fbx")
        self.assertEqual(e.uv_channel, 1)

    def test_is_baked_false(self):
        e = LightmapEntry(entry_id="e001", mesh_path="meshes/wall.fbx")
        self.assertFalse(e.is_baked)

    def test_needs_rebake_true(self):
        e = LightmapEntry(entry_id="e001", mesh_path="meshes/wall.fbx")
        self.assertTrue(e.needs_rebake)


# ---------------------------------------------------------------------------
# BakeBudget
# ---------------------------------------------------------------------------

class TestBakeBudget(unittest.TestCase):
    def test_default_max_resolution(self):
        b = BakeBudget()
        self.assertEqual(b.max_resolution, 2048)

    def test_default_max_samples(self):
        b = BakeBudget()
        self.assertEqual(b.max_samples, 512)

    def test_is_high_budget_true(self):
        b = BakeBudget(max_samples=512)
        self.assertTrue(b.is_high_budget)


# ---------------------------------------------------------------------------
# LightingBakePipeline
# ---------------------------------------------------------------------------

class TestLightingBakePipeline(unittest.TestCase):
    def _pipeline(self):
        return LightingBakePipeline()

    def test_add_entry(self):
        pl = self._pipeline()
        pl.add_entry(LightmapEntry(entry_id="e001", mesh_path="m.fbx"))
        self.assertEqual(pl.entry_count, 1)

    def test_remove_entry(self):
        pl = self._pipeline()
        pl.add_entry(LightmapEntry(entry_id="e001", mesh_path="m.fbx"))
        self.assertTrue(pl.remove_entry("e001"))
        self.assertEqual(pl.entry_count, 0)

    def test_get_entry(self):
        pl = self._pipeline()
        pl.add_entry(LightmapEntry(entry_id="e001", mesh_path="m.fbx"))
        self.assertIsNotNone(pl.get_entry("e001"))

    def test_get_all_entries(self):
        pl = self._pipeline()
        pl.add_entry(LightmapEntry(entry_id="e001", mesh_path="m.fbx"))
        self.assertEqual(len(pl.get_all_entries()), 1)

    def test_add_pass(self):
        pl = self._pipeline()
        pl.add_pass(BakePassDef(pass_id="p001", pass_name="Direct"))
        self.assertEqual(pl.pass_count, 1)

    def test_get_pass(self):
        pl = self._pipeline()
        pl.add_pass(BakePassDef(pass_id="p001", pass_name="Direct"))
        self.assertIsNotNone(pl.get_pass("p001"))

    def test_bake(self):
        pl = self._pipeline()
        pl.add_entry(LightmapEntry(entry_id="e001", mesh_path="m.fbx"))
        self.assertTrue(pl.bake("e001"))
        self.assertTrue(pl.get_entry("e001").is_baked)

    def test_bake_all(self):
        pl = self._pipeline()
        pl.add_entry(LightmapEntry(entry_id="e001", mesh_path="m.fbx"))
        pl.add_entry(LightmapEntry(entry_id="e002", mesh_path="n.fbx"))
        results = pl.bake_all()
        self.assertEqual(len(results), 2)

    def test_invalidate(self):
        pl = self._pipeline()
        pl.add_entry(LightmapEntry(entry_id="e001", mesh_path="m.fbx", baked=True))
        pl.invalidate("e001")
        self.assertFalse(pl.get_entry("e001").is_baked)

    def test_invalidate_all(self):
        pl = self._pipeline()
        pl.add_entry(LightmapEntry(entry_id="e001", mesh_path="m.fbx", baked=True))
        pl.invalidate_all()
        self.assertFalse(pl.get_entry("e001").is_baked)

    def test_set_budget(self):
        pl = self._pipeline()
        pl.set_budget(BakeBudget(max_samples=128))
        self.assertEqual(pl.get_budget().max_samples, 128)

    def test_get_budget(self):
        pl = self._pipeline()
        self.assertIsInstance(pl.get_budget(), BakeBudget)

    def test_get_unbaked(self):
        pl = self._pipeline()
        pl.add_entry(LightmapEntry(entry_id="e001", mesh_path="m.fbx"))
        self.assertEqual(len(pl.get_unbaked()), 1)

    def test_entry_count(self):
        pl = self._pipeline()
        self.assertEqual(pl.entry_count, 0)

    def test_pass_count(self):
        pl = self._pipeline()
        self.assertEqual(pl.pass_count, 0)

    def test_is_empty_true(self):
        pl = self._pipeline()
        self.assertTrue(pl.is_empty)

    def test_clear(self):
        pl = self._pipeline()
        pl.add_entry(LightmapEntry(entry_id="e001", mesh_path="m.fbx"))
        pl.clear()
        self.assertTrue(pl.is_empty)


# ---------------------------------------------------------------------------
# CollisionShapeDef
# ---------------------------------------------------------------------------

class TestCollisionShapeDef(unittest.TestCase):
    def test_shape_id(self):
        s = CollisionShapeDef(shape_id="s001", shape_name="Box Shape")
        self.assertEqual(s.shape_id, "s001")

    def test_shape_name(self):
        s = CollisionShapeDef(shape_id="s001", shape_name="Box Shape")
        self.assertEqual(s.shape_name, "Box Shape")

    def test_default_shape_type(self):
        s = CollisionShapeDef(shape_id="s001", shape_name="Box Shape")
        self.assertEqual(s.shape_type, "Box")

    def test_default_scale(self):
        s = CollisionShapeDef(shape_id="s001", shape_name="Box Shape")
        self.assertAlmostEqual(s.scale_x, 1.0)

    def test_is_enabled_true(self):
        s = CollisionShapeDef(shape_id="s001", shape_name="Box Shape")
        self.assertTrue(s.is_enabled)

    def test_is_simple_true(self):
        s = CollisionShapeDef(shape_id="s001", shape_name="Box Shape", shape_type="Box")
        self.assertTrue(s.is_simple)


# ---------------------------------------------------------------------------
# CollisionMeshEntry
# ---------------------------------------------------------------------------

class TestCollisionMeshEntry(unittest.TestCase):
    def test_entry_id(self):
        e = CollisionMeshEntry(entry_id="e001", mesh_path="meshes/rock.fbx")
        self.assertEqual(e.entry_id, "e001")

    def test_mesh_path(self):
        e = CollisionMeshEntry(entry_id="e001", mesh_path="meshes/rock.fbx")
        self.assertEqual(e.mesh_path, "meshes/rock.fbx")

    def test_shape_count_zero(self):
        e = CollisionMeshEntry(entry_id="e001", mesh_path="meshes/rock.fbx")
        self.assertEqual(e.shape_count, 0)

    def test_has_shapes_false(self):
        e = CollisionMeshEntry(entry_id="e001", mesh_path="meshes/rock.fbx")
        self.assertFalse(e.has_shapes)

    def test_default_simplification_ratio(self):
        e = CollisionMeshEntry(entry_id="e001", mesh_path="meshes/rock.fbx")
        self.assertAlmostEqual(e.simplification_ratio, 1.0)


# ---------------------------------------------------------------------------
# CollisionBuildResult
# ---------------------------------------------------------------------------

class TestCollisionBuildResult(unittest.TestCase):
    def test_job_id(self):
        r = CollisionBuildResult(job_id="j001", entry_id="e001")
        self.assertEqual(r.job_id, "j001")

    def test_entry_id(self):
        r = CollisionBuildResult(job_id="j001", entry_id="e001")
        self.assertEqual(r.entry_id, "e001")

    def test_default_shapes_generated(self):
        r = CollisionBuildResult(job_id="j001", entry_id="e001")
        self.assertEqual(r.shapes_generated, 0)

    def test_has_errors_false(self):
        r = CollisionBuildResult(job_id="j001", entry_id="e001")
        self.assertFalse(r.has_errors)

    def test_success_true(self):
        r = CollisionBuildResult(job_id="j001", entry_id="e001")
        self.assertTrue(r.success)


# ---------------------------------------------------------------------------
# CollisionMeshPipeline
# ---------------------------------------------------------------------------

class TestCollisionMeshPipeline(unittest.TestCase):
    def _pipeline(self):
        return CollisionMeshPipeline()

    def test_add_entry(self):
        pl = self._pipeline()
        pl.add_entry(CollisionMeshEntry(entry_id="e001", mesh_path="m.fbx"))
        self.assertEqual(pl.entry_count, 1)

    def test_remove_entry(self):
        pl = self._pipeline()
        pl.add_entry(CollisionMeshEntry(entry_id="e001", mesh_path="m.fbx"))
        self.assertTrue(pl.remove_entry("e001"))
        self.assertEqual(pl.entry_count, 0)

    def test_get_entry(self):
        pl = self._pipeline()
        pl.add_entry(CollisionMeshEntry(entry_id="e001", mesh_path="m.fbx"))
        self.assertIsNotNone(pl.get_entry("e001"))

    def test_get_all_entries(self):
        pl = self._pipeline()
        pl.add_entry(CollisionMeshEntry(entry_id="e001", mesh_path="m.fbx"))
        self.assertEqual(len(pl.get_all_entries()), 1)

    def test_add_shape(self):
        pl = self._pipeline()
        pl.add_entry(CollisionMeshEntry(entry_id="e001", mesh_path="m.fbx"))
        shape = CollisionShapeDef(shape_id="s001", shape_name="Box")
        self.assertTrue(pl.add_shape("e001", shape))
        self.assertEqual(pl.get_entry("e001").shape_count, 1)

    def test_build(self):
        pl = self._pipeline()
        pl.add_entry(CollisionMeshEntry(entry_id="e001", mesh_path="m.fbx"))
        result = pl.build("e001")
        self.assertIsInstance(result, CollisionBuildResult)

    def test_build_all(self):
        pl = self._pipeline()
        pl.add_entry(CollisionMeshEntry(entry_id="e001", mesh_path="m.fbx"))
        results = pl.build_all()
        self.assertEqual(len(results), 1)

    def test_validate(self):
        pl = self._pipeline()
        entry = CollisionMeshEntry(entry_id="e001", mesh_path="m.fbx")
        self.assertTrue(pl.validate(entry))

    def test_entry_count(self):
        pl = self._pipeline()
        self.assertEqual(pl.entry_count, 0)

    def test_is_empty_true(self):
        pl = self._pipeline()
        self.assertTrue(pl.is_empty)

    def test_clear(self):
        pl = self._pipeline()
        pl.add_entry(CollisionMeshEntry(entry_id="e001", mesh_path="m.fbx"))
        pl.clear()
        self.assertTrue(pl.is_empty)


if __name__ == "__main__":
    unittest.main()
