"""Phase 25B — Tests for MeshSimplificationPipeline and AnimationRetargetPipeline."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    MeshSimplificationPipeline,
    SimplificationTarget,
    SimplificationResult,
    SimplificationBatch,
    AnimationRetargetPipeline,
    RetargetProfile,
    BoneMapping,
    RetargetJob,
    RetargetResult,
)

TMP_DIR = Path("/tmp/test_phase25b")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# SimplificationTarget dataclass
# ---------------------------------------------------------------------------

class TestSimplificationTargetDataclass(unittest.TestCase):
    def test_target_id_field(self):
        t = SimplificationTarget("t001", "/meshes/rock.fbx")
        self.assertEqual(t.target_id, "t001")

    def test_mesh_path_field(self):
        t = SimplificationTarget("t001", "/meshes/rock.fbx")
        self.assertEqual(t.mesh_path, "/meshes/rock.fbx")

    def test_default_target_ratio(self):
        t = SimplificationTarget("t001", "/meshes/rock.fbx")
        self.assertAlmostEqual(t.target_ratio, 0.5)

    def test_default_max_error(self):
        t = SimplificationTarget("t001", "/meshes/rock.fbx")
        self.assertAlmostEqual(t.max_error, 0.01)

    def test_default_preserve_boundaries(self):
        t = SimplificationTarget("t001", "/meshes/rock.fbx")
        self.assertTrue(t.preserve_boundaries)

    def test_reduction_percent_at_half(self):
        t = SimplificationTarget("t001", "/meshes/rock.fbx", target_ratio=0.5)
        self.assertAlmostEqual(t.reduction_percent, 50.0)

    def test_reduction_percent_at_full(self):
        t = SimplificationTarget("t001", "/meshes/rock.fbx", target_ratio=1.0)
        self.assertAlmostEqual(t.reduction_percent, 0.0)


# ---------------------------------------------------------------------------
# SimplificationResult dataclass
# ---------------------------------------------------------------------------

class TestSimplificationResultDataclass(unittest.TestCase):
    def test_target_id_field(self):
        r = SimplificationResult("t001", "/meshes/rock.fbx")
        self.assertEqual(r.target_id, "t001")

    def test_default_success_false(self):
        r = SimplificationResult("t001", "/meshes/rock.fbx")
        self.assertFalse(r.success)

    def test_triangle_reduction_percent_zero(self):
        r = SimplificationResult("t001", "/meshes/rock.fbx",
                                  original_triangles=0)
        self.assertAlmostEqual(r.triangle_reduction_percent, 0.0)

    def test_triangle_reduction_percent(self):
        r = SimplificationResult("t001", "/meshes/rock.fbx",
                                  original_triangles=10000,
                                  simplified_triangles=5000)
        self.assertAlmostEqual(r.triangle_reduction_percent, 50.0)

    def test_vertex_reduction_percent(self):
        r = SimplificationResult("t001", "/m.fbx",
                                  original_vertices=4000,
                                  simplified_vertices=2000)
        self.assertAlmostEqual(r.vertex_reduction_percent, 50.0)


# ---------------------------------------------------------------------------
# SimplificationBatch dataclass
# ---------------------------------------------------------------------------

class TestSimplificationBatchDataclass(unittest.TestCase):
    def test_batch_id_field(self):
        b = SimplificationBatch("b001", "test_batch")
        self.assertEqual(b.batch_id, "b001")

    def test_name_field(self):
        b = SimplificationBatch("b001", "test_batch")
        self.assertEqual(b.name, "test_batch")

    def test_target_count_empty(self):
        b = SimplificationBatch("b001", "test_batch")
        self.assertEqual(b.target_count, 0)

    def test_success_count_empty(self):
        b = SimplificationBatch("b001", "test_batch")
        self.assertEqual(b.success_count, 0)

    def test_average_ratio_empty(self):
        b = SimplificationBatch("b001", "test_batch")
        self.assertAlmostEqual(b.average_ratio, 0.0)


# ---------------------------------------------------------------------------
# MeshSimplificationPipeline — batch management
# ---------------------------------------------------------------------------

class TestMeshSimplificationPipelineBatches(unittest.TestCase):
    def setUp(self):
        self.pipeline = MeshSimplificationPipeline()

    def test_create_batch_returns_batch(self):
        b = self.pipeline.create_batch("terrain")
        self.assertIsInstance(b, SimplificationBatch)

    def test_batch_name_set(self):
        b = self.pipeline.create_batch("terrain")
        self.assertEqual(b.name, "terrain")

    def test_batch_id_unique(self):
        b1 = self.pipeline.create_batch("a")
        b2 = self.pipeline.create_batch("b")
        self.assertNotEqual(b1.batch_id, b2.batch_id)

    def test_get_batch_count(self):
        self.pipeline.create_batch("a")
        self.pipeline.create_batch("b")
        self.assertEqual(self.pipeline.get_batch_count(), 2)

    def test_get_all_batch_ids(self):
        b = self.pipeline.create_batch("a")
        self.assertIn(b.batch_id, self.pipeline.get_all_batch_ids())

    def test_get_batch_by_id(self):
        b = self.pipeline.create_batch("terrain")
        fetched = self.pipeline.get_batch(b.batch_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.batch_id, b.batch_id)

    def test_get_batch_missing_returns_none(self):
        self.assertIsNone(self.pipeline.get_batch("no_such_batch"))

    def test_remove_batch(self):
        b = self.pipeline.create_batch("terrain")
        result = self.pipeline.remove_batch(b.batch_id)
        self.assertTrue(result)
        self.assertEqual(self.pipeline.get_batch_count(), 0)

    def test_remove_batch_missing_returns_false(self):
        self.assertFalse(self.pipeline.remove_batch("ghost"))

    def test_clear_resets(self):
        self.pipeline.create_batch("a")
        self.pipeline.clear()
        self.assertEqual(self.pipeline.get_batch_count(), 0)


# ---------------------------------------------------------------------------
# MeshSimplificationPipeline — target management
# ---------------------------------------------------------------------------

class TestMeshSimplificationPipelineTargets(unittest.TestCase):
    def setUp(self):
        self.pipeline = MeshSimplificationPipeline()
        self.batch = self.pipeline.create_batch("tb")

    def test_add_target_returns_target(self):
        t = self.pipeline.add_target(self.batch.batch_id, "/mesh/rock.fbx")
        self.assertIsInstance(t, SimplificationTarget)

    def test_target_ratio_clamped(self):
        t = self.pipeline.add_target(self.batch.batch_id, "/m.fbx", target_ratio=2.0)
        self.assertLessEqual(t.target_ratio, 1.0)

    def test_target_ratio_min_clamped(self):
        t = self.pipeline.add_target(self.batch.batch_id, "/m.fbx", target_ratio=0.0)
        self.assertGreater(t.target_ratio, 0.0)

    def test_get_target_count(self):
        self.pipeline.add_target(self.batch.batch_id, "/m1.fbx")
        self.pipeline.add_target(self.batch.batch_id, "/m2.fbx")
        self.assertEqual(self.pipeline.get_target_count(self.batch.batch_id), 2)

    def test_remove_target(self):
        t = self.pipeline.add_target(self.batch.batch_id, "/m.fbx")
        removed = self.pipeline.remove_target(self.batch.batch_id, t.target_id)
        self.assertTrue(removed)
        self.assertEqual(self.pipeline.get_target_count(self.batch.batch_id), 0)

    def test_add_target_unknown_batch_returns_none(self):
        result = self.pipeline.add_target("no_batch", "/m.fbx")
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# MeshSimplificationPipeline — processing
# ---------------------------------------------------------------------------

class TestMeshSimplificationPipelineProcessing(unittest.TestCase):
    def setUp(self):
        self.pipeline = MeshSimplificationPipeline()
        self.batch = self.pipeline.create_batch("proc")
        self.pipeline.add_target(self.batch.batch_id, "/m1.fbx", target_ratio=0.5)
        self.pipeline.add_target(self.batch.batch_id, "/m2.fbx", target_ratio=0.25)

    def test_process_batch_returns_results(self):
        results = self.pipeline.process_batch(self.batch.batch_id)
        self.assertEqual(len(results), 2)

    def test_process_batch_all_success(self):
        results = self.pipeline.process_batch(self.batch.batch_id)
        self.assertTrue(all(r.success for r in results))

    def test_process_batch_simplified_le_original(self):
        results = self.pipeline.process_batch(self.batch.batch_id)
        for r in results:
            self.assertLessEqual(r.simplified_triangles, r.original_triangles)

    def test_process_batch_unknown_returns_empty(self):
        results = self.pipeline.process_batch("ghost")
        self.assertEqual(results, [])

    def test_batch_success_count_after_process(self):
        self.pipeline.process_batch(self.batch.batch_id)
        self.assertEqual(self.batch.success_count, 2)

    def test_batch_summary_keys(self):
        self.pipeline.process_batch(self.batch.batch_id)
        summary = self.pipeline.get_batch_summary(self.batch.batch_id)
        self.assertIn("batch_id", summary)
        self.assertIn("success_count", summary)
        self.assertIn("average_ratio", summary)

    def test_save_report(self):
        self.pipeline.process_batch(self.batch.batch_id)
        out = str(TMP_DIR / "simplify_report.json")
        self.assertTrue(self.pipeline.save_report(self.batch.batch_id, out))
        self.assertTrue(Path(out).exists())


# ---------------------------------------------------------------------------
# BoneMapping dataclass
# ---------------------------------------------------------------------------

class TestBoneMappingDataclass(unittest.TestCase):
    def test_mapping_id_field(self):
        m = BoneMapping("m001", "Hip", "Pelvis")
        self.assertEqual(m.mapping_id, "m001")

    def test_source_bone_field(self):
        m = BoneMapping("m001", "Hip", "Pelvis")
        self.assertEqual(m.source_bone, "Hip")

    def test_target_bone_field(self):
        m = BoneMapping("m001", "Hip", "Pelvis")
        self.assertEqual(m.target_bone, "Pelvis")

    def test_default_position_scale(self):
        m = BoneMapping("m001", "Hip", "Pelvis")
        self.assertAlmostEqual(m.position_scale, 1.0)

    def test_default_weight(self):
        m = BoneMapping("m001", "Hip", "Pelvis")
        self.assertAlmostEqual(m.weight, 1.0)


# ---------------------------------------------------------------------------
# RetargetProfile dataclass
# ---------------------------------------------------------------------------

class TestRetargetProfileDataclass(unittest.TestCase):
    def test_profile_id_field(self):
        import time
        p = RetargetProfile("p001", "HumanoidA->B", "rig_a", "rig_b",
                            created_at=time.time())
        self.assertEqual(p.profile_id, "p001")

    def test_name_field(self):
        import time
        p = RetargetProfile("p001", "HumanoidA->B", "rig_a", "rig_b",
                            created_at=time.time())
        self.assertEqual(p.name, "HumanoidA->B")

    def test_mapping_count_empty(self):
        import time
        p = RetargetProfile("p001", "H->B", "a", "b", created_at=time.time())
        self.assertEqual(p.mapping_count, 0)

    def test_get_mapping_for_source_none(self):
        import time
        p = RetargetProfile("p001", "H->B", "a", "b", created_at=time.time())
        self.assertIsNone(p.get_mapping_for_source("NoSuchBone"))


# ---------------------------------------------------------------------------
# AnimationRetargetPipeline — profile management
# ---------------------------------------------------------------------------

class TestAnimationRetargetPipelineProfiles(unittest.TestCase):
    def setUp(self):
        self.pipeline = AnimationRetargetPipeline()

    def test_create_profile_returns_profile(self):
        p = self.pipeline.create_profile("H->B", "rig_a", "rig_b")
        self.assertIsInstance(p, RetargetProfile)

    def test_profile_source_rig(self):
        p = self.pipeline.create_profile("H->B", "rig_a", "rig_b")
        self.assertEqual(p.source_rig, "rig_a")

    def test_profile_target_rig(self):
        p = self.pipeline.create_profile("H->B", "rig_a", "rig_b")
        self.assertEqual(p.target_rig, "rig_b")

    def test_get_profile_count(self):
        self.pipeline.create_profile("A->B", "a", "b")
        self.pipeline.create_profile("B->C", "b", "c")
        self.assertEqual(self.pipeline.get_profile_count(), 2)

    def test_get_all_profile_ids(self):
        p = self.pipeline.create_profile("A->B", "a", "b")
        self.assertIn(p.profile_id, self.pipeline.get_all_profile_ids())

    def test_get_profile_by_id(self):
        p = self.pipeline.create_profile("A->B", "a", "b")
        fetched = self.pipeline.get_profile(p.profile_id)
        self.assertIsNotNone(fetched)

    def test_remove_profile(self):
        p = self.pipeline.create_profile("A->B", "a", "b")
        self.assertTrue(self.pipeline.remove_profile(p.profile_id))
        self.assertEqual(self.pipeline.get_profile_count(), 0)

    def test_remove_profile_missing(self):
        self.assertFalse(self.pipeline.remove_profile("ghost"))

    def test_clear_resets(self):
        self.pipeline.create_profile("A->B", "a", "b")
        self.pipeline.clear()
        self.assertEqual(self.pipeline.get_profile_count(), 0)


# ---------------------------------------------------------------------------
# AnimationRetargetPipeline — bone mappings
# ---------------------------------------------------------------------------

class TestAnimationRetargetPipelineMappings(unittest.TestCase):
    def setUp(self):
        self.pipeline = AnimationRetargetPipeline()
        self.profile = self.pipeline.create_profile("H->B", "a", "b")

    def test_add_bone_mapping_returns_mapping(self):
        m = self.pipeline.add_bone_mapping(self.profile.profile_id, "Hip", "Pelvis")
        self.assertIsInstance(m, BoneMapping)

    def test_mapping_source_bone(self):
        m = self.pipeline.add_bone_mapping(self.profile.profile_id, "Hip", "Pelvis")
        self.assertEqual(m.source_bone, "Hip")

    def test_get_mapping_count(self):
        self.pipeline.add_bone_mapping(self.profile.profile_id, "Hip", "Pelvis")
        self.pipeline.add_bone_mapping(self.profile.profile_id, "Spine", "Chest")
        self.assertEqual(self.pipeline.get_mapping_count(self.profile.profile_id), 2)

    def test_remove_bone_mapping(self):
        m = self.pipeline.add_bone_mapping(self.profile.profile_id, "Hip", "Pelvis")
        self.assertTrue(
            self.pipeline.remove_bone_mapping(self.profile.profile_id, m.mapping_id)
        )
        self.assertEqual(self.pipeline.get_mapping_count(self.profile.profile_id), 0)

    def test_weight_clamped_to_1(self):
        m = self.pipeline.add_bone_mapping(
            self.profile.profile_id, "Hip", "Pelvis", weight=5.0
        )
        self.assertLessEqual(m.weight, 1.0)

    def test_set_mapping_offset(self):
        m = self.pipeline.add_bone_mapping(self.profile.profile_id, "Spine", "Chest")
        result = self.pipeline.set_mapping_offset(
            self.profile.profile_id, m.mapping_id, rx=10.0, ry=0.0, rz=0.0
        )
        self.assertTrue(result)

    def test_add_mapping_unknown_profile_returns_none(self):
        result = self.pipeline.add_bone_mapping("ghost", "Hip", "Pelvis")
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# AnimationRetargetPipeline — jobs and processing
# ---------------------------------------------------------------------------

class TestAnimationRetargetPipelineJobs(unittest.TestCase):
    def setUp(self):
        self.pipeline = AnimationRetargetPipeline()
        self.profile = self.pipeline.create_profile("H->B", "a", "b")
        self.pipeline.add_bone_mapping(self.profile.profile_id, "Hip", "Pelvis")
        self.pipeline.add_bone_mapping(self.profile.profile_id, "Spine", "Chest")

    def test_create_job_returns_job(self):
        j = self.pipeline.create_job(
            self.profile.profile_id, "/anim/walk.anim"
        )
        self.assertIsInstance(j, RetargetJob)

    def test_create_job_unknown_profile_returns_none(self):
        self.assertIsNone(
            self.pipeline.create_job("ghost", "/anim/walk.anim")
        )

    def test_get_job_count(self):
        self.pipeline.create_job(self.profile.profile_id, "/a.anim")
        self.pipeline.create_job(self.profile.profile_id, "/b.anim")
        self.assertEqual(self.pipeline.get_job_count(), 2)

    def test_run_job_returns_result(self):
        j = self.pipeline.create_job(self.profile.profile_id, "/a.anim")
        result = self.pipeline.run_job(j.job_id)
        self.assertIsInstance(result, RetargetResult)

    def test_run_job_success(self):
        j = self.pipeline.create_job(self.profile.profile_id, "/a.anim")
        result = self.pipeline.run_job(j.job_id)
        self.assertTrue(result.success)

    def test_run_job_bones_retargeted(self):
        j = self.pipeline.create_job(self.profile.profile_id, "/a.anim")
        result = self.pipeline.run_job(j.job_id)
        self.assertEqual(result.bones_retargeted, 2)

    def test_coverage_ratio(self):
        j = self.pipeline.create_job(self.profile.profile_id, "/a.anim")
        result = self.pipeline.run_job(j.job_id)
        self.assertGreater(result.coverage_ratio, 0.0)
        self.assertLessEqual(result.coverage_ratio, 1.0)

    def test_run_job_unknown_returns_none(self):
        self.assertIsNone(self.pipeline.run_job("ghost"))

    def test_get_result_after_run(self):
        j = self.pipeline.create_job(self.profile.profile_id, "/a.anim")
        self.pipeline.run_job(j.job_id)
        result = self.pipeline.get_result(j.job_id)
        self.assertIsNotNone(result)

    def test_run_all_jobs(self):
        self.pipeline.create_job(self.profile.profile_id, "/a.anim")
        self.pipeline.create_job(self.profile.profile_id, "/b.anim")
        results = self.pipeline.run_all_jobs()
        self.assertEqual(len(results), 2)

    def test_remove_job(self):
        j = self.pipeline.create_job(self.profile.profile_id, "/a.anim")
        self.assertTrue(self.pipeline.remove_job(j.job_id))
        self.assertEqual(self.pipeline.get_job_count(), 0)

    def test_has_warnings_when_bones_missing(self):
        j = self.pipeline.create_job(self.profile.profile_id, "/a.anim")
        result = self.pipeline.run_job(j.job_id)
        if result.bones_missing > 0:
            self.assertTrue(result.has_warnings)


# ---------------------------------------------------------------------------
# AnimationRetargetPipeline — profile settings helpers
# ---------------------------------------------------------------------------

class TestAnimationRetargetPipelineSettings(unittest.TestCase):
    def setUp(self):
        self.pipeline = AnimationRetargetPipeline()
        self.profile = self.pipeline.create_profile("H->B", "a", "b")

    def test_set_preserve_foot_contact(self):
        self.assertTrue(
            self.pipeline.set_preserve_foot_contact(
                self.profile.profile_id, False
            )
        )
        p = self.pipeline.get_profile(self.profile.profile_id)
        self.assertFalse(p.preserve_foot_contact)

    def test_set_preserve_hand_contact(self):
        self.assertTrue(
            self.pipeline.set_preserve_hand_contact(
                self.profile.profile_id, False
            )
        )

    def test_set_normalize_hip_height(self):
        self.assertTrue(
            self.pipeline.set_normalize_hip_height(
                self.profile.profile_id, False
            )
        )

    def test_set_ik_solving_enabled(self):
        self.assertTrue(
            self.pipeline.set_ik_solving_enabled(
                self.profile.profile_id, False
            )
        )
        p = self.pipeline.get_profile(self.profile.profile_id)
        self.assertFalse(p.ik_solving_enabled)

    def test_settings_unknown_profile_returns_false(self):
        self.assertFalse(
            self.pipeline.set_preserve_foot_contact("ghost", True)
        )


# ---------------------------------------------------------------------------
# AnimationRetargetPipeline — persistence
# ---------------------------------------------------------------------------

class TestAnimationRetargetPipelinePersistence(unittest.TestCase):
    def setUp(self):
        self.pipeline = AnimationRetargetPipeline()
        self.profile = self.pipeline.create_profile("H->B", "a", "b")
        self.pipeline.add_bone_mapping(self.profile.profile_id, "Hip", "Pelvis")

    def test_save_profile(self):
        out = str(TMP_DIR / "retarget_profile.json")
        self.assertTrue(self.pipeline.save_profile(self.profile.profile_id, out))
        self.assertTrue(Path(out).exists())

    def test_save_profile_content(self):
        out = str(TMP_DIR / "retarget_profile2.json")
        self.pipeline.save_profile(self.profile.profile_id, out)
        data = json.loads(Path(out).read_text())
        self.assertIn("profile_id", data)
        self.assertIn("bone_mappings", data)

    def test_save_unknown_profile_returns_false(self):
        self.assertFalse(
            self.pipeline.save_profile("ghost", str(TMP_DIR / "x.json"))
        )


if __name__ == "__main__":
    unittest.main()
