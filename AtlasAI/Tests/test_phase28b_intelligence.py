"""Phase 28B — Tests for VFXGraphCompiler and LightBakingPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    VFXGraphCompiler,
    VFXEmitterNode,
    VFXLinkEdge,
    VFXGraphAsset,
    LightBakingPipeline,
    BakeJob,
    ProbeCluster,
    BakeResult,
)


# ---------------------------------------------------------------------------
# VFXEmitterNode dataclass
# ---------------------------------------------------------------------------

class TestVFXEmitterNodeDataclass(unittest.TestCase):
    def test_node_id_field(self):
        n = VFXEmitterNode(node_id="n001", name="Sparks")
        self.assertEqual(n.node_id, "n001")

    def test_name_field(self):
        n = VFXEmitterNode(node_id="n001", name="Sparks")
        self.assertEqual(n.name, "Sparks")

    def test_default_emitter_type(self):
        n = VFXEmitterNode(node_id="n001", name="Sparks")
        self.assertEqual(n.emitter_type, "Point")

    def test_default_spawn_rate(self):
        n = VFXEmitterNode(node_id="n001", name="Sparks")
        self.assertAlmostEqual(n.spawn_rate, 10.0)

    def test_default_lifetime(self):
        n = VFXEmitterNode(node_id="n001", name="Sparks")
        self.assertAlmostEqual(n.lifetime, 2.0)

    def test_default_position(self):
        n = VFXEmitterNode(node_id="n001", name="Sparks")
        self.assertEqual(n.position, (0.0, 0.0, 0.0))

    def test_is_emitter_point(self):
        n = VFXEmitterNode(node_id="n001", name="Sparks", emitter_type="Point")
        self.assertTrue(n.is_emitter)

    def test_is_emitter_sphere(self):
        n = VFXEmitterNode(node_id="n001", name="Sparks", emitter_type="Sphere")
        self.assertTrue(n.is_emitter)

    def test_default_enabled(self):
        n = VFXEmitterNode(node_id="n001", name="Sparks")
        self.assertTrue(n.enabled)


# ---------------------------------------------------------------------------
# VFXLinkEdge dataclass
# ---------------------------------------------------------------------------

class TestVFXLinkEdgeDataclass(unittest.TestCase):
    def test_edge_id_field(self):
        e = VFXLinkEdge(edge_id="e001", source_id="n001", target_id="n002")
        self.assertEqual(e.edge_id, "e001")

    def test_source_id(self):
        e = VFXLinkEdge(edge_id="e001", source_id="n001", target_id="n002")
        self.assertEqual(e.source_id, "n001")

    def test_target_id(self):
        e = VFXLinkEdge(edge_id="e001", source_id="n001", target_id="n002")
        self.assertEqual(e.target_id, "n002")

    def test_default_data_type(self):
        e = VFXLinkEdge(edge_id="e001", source_id="n001", target_id="n002")
        self.assertEqual(e.data_type, "Float")

    def test_is_connected(self):
        e = VFXLinkEdge(edge_id="e001", source_id="n001", target_id="n002")
        self.assertTrue(e.is_connected)

    def test_not_connected_empty_source(self):
        e = VFXLinkEdge(edge_id="e001", source_id="", target_id="n002")
        self.assertFalse(e.is_connected)


# ---------------------------------------------------------------------------
# VFXGraphAsset dataclass
# ---------------------------------------------------------------------------

class TestVFXGraphAssetDataclass(unittest.TestCase):
    def test_asset_id(self):
        a = VFXGraphAsset(asset_id="a001", name="Fire")
        self.assertEqual(a.asset_id, "a001")

    def test_default_not_compiled(self):
        a = VFXGraphAsset(asset_id="a001", name="Fire")
        self.assertFalse(a.compiled)

    def test_node_count_empty(self):
        a = VFXGraphAsset(asset_id="a001", name="Fire")
        self.assertEqual(a.node_count, 0)

    def test_edge_count_empty(self):
        a = VFXGraphAsset(asset_id="a001", name="Fire")
        self.assertEqual(a.edge_count, 0)

    def test_is_valid_empty(self):
        a = VFXGraphAsset(asset_id="a001", name="Fire")
        self.assertTrue(a.is_valid)


# ---------------------------------------------------------------------------
# VFXGraphCompiler
# ---------------------------------------------------------------------------

class TestVFXGraphCompilerCreate(unittest.TestCase):
    def setUp(self):
        self.compiler = VFXGraphCompiler()

    def test_create_asset(self):
        a = self.compiler.create_asset("TestFX")
        self.assertIsNotNone(a)
        self.assertEqual(a.name, "TestFX")

    def test_list_assets_empty(self):
        self.assertEqual(self.compiler.list_assets(), [])

    def test_list_assets_after_create(self):
        self.compiler.create_asset("A")
        self.compiler.create_asset("B")
        self.assertEqual(len(self.compiler.list_assets()), 2)

    def test_get_asset(self):
        a = self.compiler.create_asset("FX1")
        fetched = self.compiler.get_asset(a.asset_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "FX1")

    def test_get_asset_missing(self):
        self.assertIsNone(self.compiler.get_asset("nonexistent"))

    def test_remove_asset(self):
        a = self.compiler.create_asset("Remove")
        result = self.compiler.remove_asset(a.asset_id)
        self.assertTrue(result)
        self.assertIsNone(self.compiler.get_asset(a.asset_id))

    def test_remove_asset_missing(self):
        self.assertFalse(self.compiler.remove_asset("missing"))


class TestVFXGraphCompilerNodes(unittest.TestCase):
    def setUp(self):
        self.compiler = VFXGraphCompiler()
        self.asset = self.compiler.create_asset("NodeTest")

    def test_add_node(self):
        node = self.compiler.add_node(self.asset.asset_id, "Emitter1")
        self.assertIsNotNone(node)

    def test_add_node_invalid_asset(self):
        node = self.compiler.add_node("bad_id", "Emitter")
        self.assertIsNone(node)

    def test_node_count_after_add(self):
        self.compiler.add_node(self.asset.asset_id, "E1")
        self.compiler.add_node(self.asset.asset_id, "E2")
        a = self.compiler.get_asset(self.asset.asset_id)
        self.assertEqual(a.node_count, 2)

    def test_remove_node(self):
        node = self.compiler.add_node(self.asset.asset_id, "E1")
        result = self.compiler.remove_node(self.asset.asset_id, node.node_id)
        self.assertTrue(result)
        a = self.compiler.get_asset(self.asset.asset_id)
        self.assertEqual(a.node_count, 0)

    def test_remove_node_clears_edges(self):
        n1 = self.compiler.add_node(self.asset.asset_id, "E1")
        n2 = self.compiler.add_node(self.asset.asset_id, "E2")
        self.compiler.add_edge(self.asset.asset_id, n1.node_id, n2.node_id)
        self.compiler.remove_node(self.asset.asset_id, n1.node_id)
        a = self.compiler.get_asset(self.asset.asset_id)
        self.assertEqual(a.edge_count, 0)


class TestVFXGraphCompilerEdges(unittest.TestCase):
    def setUp(self):
        self.compiler = VFXGraphCompiler()
        self.asset = self.compiler.create_asset("EdgeTest")
        self.n1 = self.compiler.add_node(self.asset.asset_id, "N1")
        self.n2 = self.compiler.add_node(self.asset.asset_id, "N2")

    def test_add_edge(self):
        edge = self.compiler.add_edge(self.asset.asset_id, self.n1.node_id, self.n2.node_id)
        self.assertIsNotNone(edge)

    def test_edge_count(self):
        self.compiler.add_edge(self.asset.asset_id, self.n1.node_id, self.n2.node_id)
        a = self.compiler.get_asset(self.asset.asset_id)
        self.assertEqual(a.edge_count, 1)

    def test_remove_edge(self):
        edge = self.compiler.add_edge(self.asset.asset_id, self.n1.node_id, self.n2.node_id)
        result = self.compiler.remove_edge(self.asset.asset_id, edge.edge_id)
        self.assertTrue(result)


class TestVFXGraphCompilerCompile(unittest.TestCase):
    def setUp(self):
        self.compiler = VFXGraphCompiler()
        self.asset = self.compiler.create_asset("CompileTest")

    def test_compile_empty_graph(self):
        result = self.compiler.compile(self.asset.asset_id)
        self.assertTrue(result)
        a = self.compiler.get_asset(self.asset.asset_id)
        self.assertTrue(a.compiled)

    def test_compile_invalid_id(self):
        result = self.compiler.compile("bad_id")
        self.assertFalse(result)

    def test_validate_graph_valid(self):
        errors = self.compiler.validate_graph(self.asset.asset_id)
        self.assertEqual(errors, [])

    def test_validate_graph_invalid_edge(self):
        n = self.compiler.add_node(self.asset.asset_id, "N1")
        edge = self.compiler.add_edge(self.asset.asset_id, n.node_id, "ghost_node")
        errors = self.compiler.validate_graph(self.asset.asset_id)
        self.assertGreater(len(errors), 0)

    def test_compile_all(self):
        self.compiler.create_asset("A2")
        compiled = self.compiler.compile_all()
        self.assertEqual(compiled, 2)

    def test_get_compiled_count(self):
        self.compiler.compile(self.asset.asset_id)
        self.assertEqual(self.compiler.get_compiled_count(), 1)


# ---------------------------------------------------------------------------
# BakeJob dataclass
# ---------------------------------------------------------------------------

class TestBakeJobDataclass(unittest.TestCase):
    def test_job_id(self):
        j = BakeJob(job_id="j001", mesh_name="Floor")
        self.assertEqual(j.job_id, "j001")

    def test_mesh_name(self):
        j = BakeJob(job_id="j001", mesh_name="Floor")
        self.assertEqual(j.mesh_name, "Floor")

    def test_default_resolution(self):
        j = BakeJob(job_id="j001", mesh_name="Floor")
        self.assertEqual(j.resolution, 512)

    def test_default_bounce_count(self):
        j = BakeJob(job_id="j001", mesh_name="Floor")
        self.assertEqual(j.bounce_count, 3)

    def test_default_quality_preset(self):
        j = BakeJob(job_id="j001", mesh_name="Floor")
        self.assertEqual(j.quality_preset, "Medium")

    def test_is_pending(self):
        j = BakeJob(job_id="j001", mesh_name="Floor")
        self.assertTrue(j.is_pending)

    def test_is_high_quality(self):
        j = BakeJob(job_id="j001", mesh_name="Floor", quality_preset="Ultra")
        self.assertTrue(j.is_high_quality)

    def test_not_high_quality_medium(self):
        j = BakeJob(job_id="j001", mesh_name="Floor", quality_preset="Medium")
        self.assertFalse(j.is_high_quality)


# ---------------------------------------------------------------------------
# ProbeCluster dataclass
# ---------------------------------------------------------------------------

class TestProbeClusterDataclass(unittest.TestCase):
    def test_cluster_id(self):
        pc = ProbeCluster(cluster_id="c001")
        self.assertEqual(pc.cluster_id, "c001")

    def test_default_probe_count(self):
        pc = ProbeCluster(cluster_id="c001")
        self.assertEqual(pc.probe_count, 8)

    def test_position(self):
        pc = ProbeCluster(cluster_id="c001", position_x=1.0, position_y=2.0, position_z=3.0)
        self.assertEqual(pc.position, (1.0, 2.0, 3.0))

    def test_total_texels(self):
        pc = ProbeCluster(cluster_id="c001", probe_count=4, resolution=16)
        self.assertEqual(pc.total_texels, 4 * 16 * 16 * 6)


# ---------------------------------------------------------------------------
# BakeResult dataclass
# ---------------------------------------------------------------------------

class TestBakeResultDataclass(unittest.TestCase):
    def test_job_id(self):
        r = BakeResult(job_id="j001", mesh_name="Wall")
        self.assertEqual(r.job_id, "j001")

    def test_default_success_false(self):
        r = BakeResult(job_id="j001", mesh_name="Wall")
        self.assertFalse(r.success)

    def test_has_warnings_false(self):
        r = BakeResult(job_id="j001", mesh_name="Wall")
        self.assertFalse(r.has_warnings)


# ---------------------------------------------------------------------------
# LightBakingPipeline
# ---------------------------------------------------------------------------

class TestLightBakingPipelineJobs(unittest.TestCase):
    def setUp(self):
        self.pipeline = LightBakingPipeline()

    def test_submit_job(self):
        j = self.pipeline.submit_job("FloorMesh")
        self.assertIsNotNone(j)
        self.assertEqual(j.mesh_name, "FloorMesh")

    def test_list_jobs_empty(self):
        self.assertEqual(self.pipeline.list_jobs(), [])

    def test_list_jobs_after_submit(self):
        self.pipeline.submit_job("A")
        self.pipeline.submit_job("B")
        self.assertEqual(len(self.pipeline.list_jobs()), 2)

    def test_get_job(self):
        j = self.pipeline.submit_job("Wall")
        fetched = self.pipeline.get_job(j.job_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.mesh_name, "Wall")

    def test_cancel_job(self):
        j = self.pipeline.submit_job("Ceil")
        result = self.pipeline.cancel_job(j.job_id)
        self.assertTrue(result)
        self.assertTrue(j.cancelled)

    def test_pending_count(self):
        self.pipeline.submit_job("M1")
        self.pipeline.submit_job("M2")
        self.assertEqual(self.pipeline.pending_count, 2)

    def test_pending_count_after_cancel(self):
        j = self.pipeline.submit_job("M1")
        self.pipeline.cancel_job(j.job_id)
        self.assertEqual(self.pipeline.pending_count, 0)


class TestLightBakingPipelineProbes(unittest.TestCase):
    def setUp(self):
        self.pipeline = LightBakingPipeline()

    def test_submit_probe_cluster(self):
        c = self.pipeline.submit_probe_cluster(probe_count=16)
        self.assertIsNotNone(c)
        self.assertEqual(c.probe_count, 16)

    def test_list_clusters(self):
        self.pipeline.submit_probe_cluster()
        self.assertEqual(len(self.pipeline.list_clusters()), 1)

    def test_remove_cluster(self):
        c = self.pipeline.submit_probe_cluster()
        result = self.pipeline.remove_cluster(c.cluster_id)
        self.assertTrue(result)
        self.assertEqual(len(self.pipeline.list_clusters()), 0)


class TestLightBakingPipelineBakeAll(unittest.TestCase):
    def setUp(self):
        self.pipeline = LightBakingPipeline()

    def test_bake_all_returns_results(self):
        self.pipeline.submit_job("M1")
        self.pipeline.submit_job("M2")
        results = self.pipeline.bake_all()
        self.assertEqual(len(results), 2)

    def test_bake_all_success(self):
        self.pipeline.submit_job("M1")
        results = self.pipeline.bake_all()
        self.assertTrue(all(r.success for r in results))

    def test_completed_count_after_bake(self):
        self.pipeline.submit_job("M1")
        self.pipeline.bake_all()
        self.assertEqual(self.pipeline.completed_count, 1)

    def test_total_bake_time_increases(self):
        self.pipeline.submit_job("M1")
        self.pipeline.bake_all()
        self.assertGreaterEqual(self.pipeline.total_bake_time, 0.0)

    def test_get_result(self):
        j = self.pipeline.submit_job("Floor")
        self.pipeline.bake_all()
        r = self.pipeline.get_result(j.job_id)
        self.assertIsNotNone(r)
        self.assertTrue(r.success)

    def test_get_stats(self):
        self.pipeline.submit_job("M1")
        stats = self.pipeline.get_stats()
        self.assertIn("total_jobs", stats)
        self.assertIn("pending", stats)

    def test_clear(self):
        self.pipeline.submit_job("M1")
        self.pipeline.clear()
        self.assertEqual(self.pipeline.pending_count, 0)


if __name__ == "__main__":
    unittest.main()
