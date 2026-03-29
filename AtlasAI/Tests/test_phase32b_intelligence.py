"""Phase 32B — Tests for VFXBakePipeline and IKSolvePipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    VFXBakePipeline,
    VFXBakePassDef,
    VFXBakeEntry,
    VFXAtlasSettings,
    IKSolvePipeline,
    IKJointDef,
    IKChainEntry,
    IKSolveResult,
)


# ---------------------------------------------------------------------------
# VFXBakePassDef
# ---------------------------------------------------------------------------

class TestVFXBakePassDef(unittest.TestCase):
    def test_pass_id(self):
        p = VFXBakePassDef(pass_id="p001", pass_name="Main Pass")
        self.assertEqual(p.pass_id, "p001")

    def test_pass_name(self):
        p = VFXBakePassDef(pass_id="p001", pass_name="Main Pass")
        self.assertEqual(p.pass_name, "Main Pass")

    def test_default_effect_type(self):
        p = VFXBakePassDef(pass_id="p001", pass_name="Main Pass")
        self.assertEqual(p.effect_type, "Particle")

    def test_default_resolution(self):
        p = VFXBakePassDef(pass_id="p001", pass_name="Main Pass")
        self.assertEqual(p.resolution, 512)

    def test_default_sample_count(self):
        p = VFXBakePassDef(pass_id="p001", pass_name="Main Pass")
        self.assertEqual(p.sample_count, 64)

    def test_is_enabled(self):
        p = VFXBakePassDef(pass_id="p001", pass_name="Main Pass")
        self.assertTrue(p.is_enabled)

    def test_is_volumetric_false(self):
        p = VFXBakePassDef(pass_id="p001", pass_name="Main Pass", effect_type="Particle")
        self.assertFalse(p.is_volumetric)


# ---------------------------------------------------------------------------
# VFXBakeEntry
# ---------------------------------------------------------------------------

class TestVFXBakeEntry(unittest.TestCase):
    def test_entry_id(self):
        e = VFXBakeEntry(entry_id="e001", asset_path="/vfx/fire.uasset")
        self.assertEqual(e.entry_id, "e001")

    def test_asset_path(self):
        e = VFXBakeEntry(entry_id="e001", asset_path="/vfx/fire.uasset")
        self.assertEqual(e.asset_path, "/vfx/fire.uasset")

    def test_default_baked_path(self):
        e = VFXBakeEntry(entry_id="e001", asset_path="/vfx/fire.uasset")
        self.assertEqual(e.baked_path, "")

    def test_default_uv_channel(self):
        e = VFXBakeEntry(entry_id="e001", asset_path="/vfx/fire.uasset")
        self.assertEqual(e.uv_channel, 0)

    def test_is_baked_false(self):
        e = VFXBakeEntry(entry_id="e001", asset_path="/vfx/fire.uasset")
        self.assertFalse(e.is_baked)

    def test_needs_rebake_true(self):
        e = VFXBakeEntry(entry_id="e001", asset_path="/vfx/fire.uasset")
        self.assertTrue(e.needs_rebake)


# ---------------------------------------------------------------------------
# VFXAtlasSettings
# ---------------------------------------------------------------------------

class TestVFXAtlasSettings(unittest.TestCase):
    def test_atlas_id(self):
        a = VFXAtlasSettings(atlas_id="atlas001")
        self.assertEqual(a.atlas_id, "atlas001")

    def test_default_rows(self):
        a = VFXAtlasSettings(atlas_id="atlas001")
        self.assertEqual(a.rows, 4)

    def test_default_cols(self):
        a = VFXAtlasSettings(atlas_id="atlas001")
        self.assertEqual(a.cols, 4)

    def test_frame_count(self):
        a = VFXAtlasSettings(atlas_id="atlas001", rows=4, cols=4)
        self.assertEqual(a.frame_count, 16)

    def test_is_looping_true(self):
        a = VFXAtlasSettings(atlas_id="atlas001")
        self.assertTrue(a.is_looping)


# ---------------------------------------------------------------------------
# VFXBakePipeline
# ---------------------------------------------------------------------------

class TestVFXBakePipeline(unittest.TestCase):
    def _pipeline(self):
        return VFXBakePipeline()

    def test_add_entry(self):
        pipe = self._pipeline()
        pipe.add_entry(VFXBakeEntry(entry_id="e001", asset_path="/vfx/fire.uasset"))
        self.assertEqual(pipe.entry_count, 1)

    def test_remove_entry(self):
        pipe = self._pipeline()
        pipe.add_entry(VFXBakeEntry(entry_id="e001", asset_path="/vfx/fire.uasset"))
        self.assertTrue(pipe.remove_entry("e001"))
        self.assertEqual(pipe.entry_count, 0)

    def test_get_entry(self):
        pipe = self._pipeline()
        pipe.add_entry(VFXBakeEntry(entry_id="e001", asset_path="/vfx/fire.uasset"))
        e = pipe.get_entry("e001")
        self.assertIsNotNone(e)

    def test_get_all_entries(self):
        pipe = self._pipeline()
        pipe.add_entry(VFXBakeEntry(entry_id="e001", asset_path="/a"))
        pipe.add_entry(VFXBakeEntry(entry_id="e002", asset_path="/b"))
        self.assertEqual(len(pipe.get_all_entries()), 2)

    def test_add_pass(self):
        pipe = self._pipeline()
        pipe.add_pass(VFXBakePassDef(pass_id="p001", pass_name="Main"))
        self.assertEqual(pipe.pass_count, 1)

    def test_get_pass(self):
        pipe = self._pipeline()
        pipe.add_pass(VFXBakePassDef(pass_id="p001", pass_name="Main"))
        self.assertIsNotNone(pipe.get_pass("p001"))

    def test_bake(self):
        pipe = self._pipeline()
        pipe.add_entry(VFXBakeEntry(entry_id="e001", asset_path="/vfx/fire.uasset"))
        self.assertTrue(pipe.bake("e001"))
        self.assertTrue(pipe.get_entry("e001").is_baked)

    def test_bake_all(self):
        pipe = self._pipeline()
        pipe.add_entry(VFXBakeEntry(entry_id="e001", asset_path="/a"))
        pipe.add_entry(VFXBakeEntry(entry_id="e002", asset_path="/b"))
        results = pipe.bake_all()
        self.assertEqual(len(results), 2)
        self.assertTrue(all(results.values()))

    def test_invalidate(self):
        pipe = self._pipeline()
        pipe.add_entry(VFXBakeEntry(entry_id="e001", asset_path="/a"))
        pipe.bake("e001")
        pipe.invalidate("e001")
        self.assertFalse(pipe.get_entry("e001").is_baked)

    def test_invalidate_all(self):
        pipe = self._pipeline()
        pipe.add_entry(VFXBakeEntry(entry_id="e001", asset_path="/a"))
        pipe.bake("e001")
        pipe.invalidate_all()
        self.assertFalse(pipe.get_entry("e001").is_baked)

    def test_set_atlas_settings(self):
        pipe = self._pipeline()
        pipe.set_atlas_settings(VFXAtlasSettings(atlas_id="a001"))
        self.assertIsNotNone(pipe.get_atlas_settings())

    def test_get_atlas_settings(self):
        pipe = self._pipeline()
        settings = VFXAtlasSettings(atlas_id="a001", rows=8, cols=8)
        pipe.set_atlas_settings(settings)
        self.assertEqual(pipe.get_atlas_settings().rows, 8)

    def test_get_unbaked(self):
        pipe = self._pipeline()
        pipe.add_entry(VFXBakeEntry(entry_id="e001", asset_path="/a"))
        pipe.add_entry(VFXBakeEntry(entry_id="e002", asset_path="/b"))
        pipe.bake("e001")
        unbaked = pipe.get_unbaked()
        self.assertEqual(len(unbaked), 1)

    def test_entry_count(self):
        pipe = self._pipeline()
        self.assertEqual(pipe.entry_count, 0)
        pipe.add_entry(VFXBakeEntry(entry_id="e001", asset_path="/a"))
        self.assertEqual(pipe.entry_count, 1)

    def test_pass_count(self):
        pipe = self._pipeline()
        self.assertEqual(pipe.pass_count, 0)

    def test_is_empty_true(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.is_empty)

    def test_clear(self):
        pipe = self._pipeline()
        pipe.add_entry(VFXBakeEntry(entry_id="e001", asset_path="/a"))
        pipe.clear()
        self.assertTrue(pipe.is_empty)


# ---------------------------------------------------------------------------
# IKJointDef
# ---------------------------------------------------------------------------

class TestIKJointDef(unittest.TestCase):
    def test_joint_id(self):
        j = IKJointDef(joint_id="j001", joint_name="Hip")
        self.assertEqual(j.joint_id, "j001")

    def test_joint_name(self):
        j = IKJointDef(joint_id="j001", joint_name="Hip")
        self.assertEqual(j.joint_name, "Hip")

    def test_default_min_angle(self):
        j = IKJointDef(joint_id="j001", joint_name="Hip")
        self.assertAlmostEqual(j.min_angle, -180.0)

    def test_default_max_angle(self):
        j = IKJointDef(joint_id="j001", joint_name="Hip")
        self.assertAlmostEqual(j.max_angle, 180.0)

    def test_is_enabled_true(self):
        j = IKJointDef(joint_id="j001", joint_name="Hip")
        self.assertTrue(j.is_enabled)

    def test_has_parent_false(self):
        j = IKJointDef(joint_id="j001", joint_name="Hip")
        self.assertFalse(j.has_parent)


# ---------------------------------------------------------------------------
# IKChainEntry
# ---------------------------------------------------------------------------

class TestIKChainEntry(unittest.TestCase):
    def test_entry_id(self):
        c = IKChainEntry(entry_id="c001", chain_name="Arm", root_joint_id="j001", end_effector_id="j004")
        self.assertEqual(c.entry_id, "c001")

    def test_chain_name(self):
        c = IKChainEntry(entry_id="c001", chain_name="Arm", root_joint_id="j001", end_effector_id="j004")
        self.assertEqual(c.chain_name, "Arm")

    def test_default_solver(self):
        c = IKChainEntry(entry_id="c001", chain_name="Arm", root_joint_id="j001", end_effector_id="j004")
        self.assertEqual(c.solver, "FABRIK")

    def test_default_iterations(self):
        c = IKChainEntry(entry_id="c001", chain_name="Arm", root_joint_id="j001", end_effector_id="j004")
        self.assertEqual(c.iterations, 10)

    def test_joint_count_zero(self):
        c = IKChainEntry(entry_id="c001", chain_name="Arm", root_joint_id="j001", end_effector_id="j004")
        self.assertEqual(c.joint_count, 0)

    def test_has_joints_false(self):
        c = IKChainEntry(entry_id="c001", chain_name="Arm", root_joint_id="j001", end_effector_id="j004")
        self.assertFalse(c.has_joints)


# ---------------------------------------------------------------------------
# IKSolveResult
# ---------------------------------------------------------------------------

class TestIKSolveResult(unittest.TestCase):
    def test_job_id(self):
        r = IKSolveResult(job_id="job001", entry_id="c001")
        self.assertEqual(r.job_id, "job001")

    def test_entry_id(self):
        r = IKSolveResult(job_id="job001", entry_id="c001")
        self.assertEqual(r.entry_id, "c001")

    def test_converged_false(self):
        r = IKSolveResult(job_id="job001", entry_id="c001")
        self.assertFalse(r.converged)

    def test_is_converged_false(self):
        r = IKSolveResult(job_id="job001", entry_id="c001")
        self.assertFalse(r.is_converged)

    def test_is_fast_true(self):
        r = IKSolveResult(job_id="job001", entry_id="c001", elapsed_ms=0.5)
        self.assertTrue(r.is_fast)


# ---------------------------------------------------------------------------
# IKSolvePipeline
# ---------------------------------------------------------------------------

class TestIKSolvePipeline(unittest.TestCase):
    def _pipeline(self):
        return IKSolvePipeline()

    def _chain(self, cid="c001"):
        return IKChainEntry(entry_id=cid, chain_name="Arm", root_joint_id="j001", end_effector_id="j004")

    def test_add_chain(self):
        pipe = self._pipeline()
        pipe.add_chain(self._chain())
        self.assertEqual(pipe.chain_count, 1)

    def test_remove_chain(self):
        pipe = self._pipeline()
        pipe.add_chain(self._chain())
        self.assertTrue(pipe.remove_chain("c001"))
        self.assertEqual(pipe.chain_count, 0)

    def test_get_chain(self):
        pipe = self._pipeline()
        pipe.add_chain(self._chain())
        self.assertIsNotNone(pipe.get_chain("c001"))

    def test_get_all_chains(self):
        pipe = self._pipeline()
        pipe.add_chain(self._chain("c001"))
        pipe.add_chain(self._chain("c002"))
        self.assertEqual(len(pipe.get_all_chains()), 2)

    def test_add_joint(self):
        pipe = self._pipeline()
        pipe.add_chain(self._chain())
        joint = IKJointDef(joint_id="j001", joint_name="Hip")
        result = pipe.add_joint("c001", joint)
        self.assertTrue(result)

    def test_solve(self):
        pipe = self._pipeline()
        pipe.add_chain(self._chain())
        result = pipe.solve("c001", target_pos=(100, 0, 0))
        self.assertIsInstance(result, IKSolveResult)

    def test_solve_all(self):
        pipe = self._pipeline()
        pipe.add_chain(self._chain("c001"))
        pipe.add_chain(self._chain("c002"))
        results = pipe.solve_all()
        self.assertEqual(len(results), 2)

    def test_validate(self):
        pipe = self._pipeline()
        chain = self._chain()
        self.assertTrue(pipe.validate(chain))

    def test_chain_count(self):
        pipe = self._pipeline()
        self.assertEqual(pipe.chain_count, 0)

    def test_is_empty_true(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.is_empty)

    def test_clear(self):
        pipe = self._pipeline()
        pipe.add_chain(self._chain())
        pipe.clear()
        self.assertTrue(pipe.is_empty)


if __name__ == "__main__":
    unittest.main()
