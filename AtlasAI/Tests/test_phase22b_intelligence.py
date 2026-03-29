"""Phase 22B — Tests for AssetDependencyGraph and BuildCacheManager."""
import json
import sys
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    AssetDependencyGraph,
    AssetNode,
    BuildCacheManager,
    CacheEntry,
)

TMP_DIR = Path("/tmp/test_phase22b")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# AssetNode dataclass
# ---------------------------------------------------------------------------

class TestAssetNodeDataclass(unittest.TestCase):
    def test_asset_id_field(self):
        n = AssetNode("mesh_01", "StaticMesh", "/p/mesh.fbx")
        self.assertEqual(n.asset_id, "mesh_01")

    def test_asset_type_field(self):
        n = AssetNode("t01", "Texture", "/p/tex.png")
        self.assertEqual(n.asset_type, "Texture")

    def test_path_field(self):
        n = AssetNode("a", "T", "/some/path.json")
        self.assertEqual(n.path, "/some/path.json")

    def test_tags_default_empty(self):
        n = AssetNode("a", "T", "")
        self.assertEqual(n.tags, [])

    def test_metadata_default_empty(self):
        n = AssetNode("a", "T", "")
        self.assertEqual(n.metadata, {})


# ---------------------------------------------------------------------------
# AssetDependencyGraph — nodes
# ---------------------------------------------------------------------------

class TestAssetDependencyGraphNodes(unittest.TestCase):
    def setUp(self):
        self.g = AssetDependencyGraph()

    def test_add_node_returns_node(self):
        n = self.g.add_node("m1", "Mesh", "/p")
        self.assertIsInstance(n, AssetNode)

    def test_has_node_true(self):
        self.g.add_node("m1", "Mesh")
        self.assertTrue(self.g.has_node("m1"))

    def test_has_node_false(self):
        self.assertFalse(self.g.has_node("ghost"))

    def test_get_node_count(self):
        self.g.add_node("m1", "Mesh")
        self.g.add_node("t1", "Texture")
        self.assertEqual(self.g.get_node_count(), 2)

    def test_get_node(self):
        self.g.add_node("m1", "Mesh", "/path")
        n = self.g.get_node("m1")
        self.assertIsNotNone(n)
        self.assertEqual(n.path, "/path")

    def test_get_node_missing_returns_none(self):
        self.assertIsNone(self.g.get_node("ghost"))

    def test_remove_node(self):
        self.g.add_node("m1", "Mesh")
        self.assertTrue(self.g.remove_node("m1"))
        self.assertFalse(self.g.has_node("m1"))

    def test_remove_node_missing_returns_false(self):
        self.assertFalse(self.g.remove_node("ghost"))

    def test_get_all_node_ids(self):
        self.g.add_node("m1", "Mesh")
        self.g.add_node("t1", "Texture")
        ids = self.g.get_all_node_ids()
        self.assertIn("m1", ids)
        self.assertIn("t1", ids)

    def test_get_nodes_by_type(self):
        self.g.add_node("m1", "Mesh")
        self.g.add_node("m2", "Mesh")
        self.g.add_node("t1", "Texture")
        meshes = self.g.get_nodes_by_type("Mesh")
        self.assertEqual(len(meshes), 2)


# ---------------------------------------------------------------------------
# AssetDependencyGraph — edges
# ---------------------------------------------------------------------------

class TestAssetDependencyGraphEdges(unittest.TestCase):
    def setUp(self):
        self.g = AssetDependencyGraph()
        self.g.add_node("mesh", "Mesh")
        self.g.add_node("mat", "Material")
        self.g.add_node("tex", "Texture")

    def test_add_dependency_returns_true(self):
        self.assertTrue(self.g.add_dependency("mesh", "mat"))

    def test_has_dependency_true(self):
        self.g.add_dependency("mesh", "mat")
        self.assertTrue(self.g.has_dependency("mesh", "mat"))

    def test_has_dependency_false(self):
        self.assertFalse(self.g.has_dependency("mesh", "tex"))

    def test_add_dependency_missing_node_returns_false(self):
        self.assertFalse(self.g.add_dependency("mesh", "ghost"))

    def test_remove_dependency_returns_true(self):
        self.g.add_dependency("mesh", "mat")
        self.assertTrue(self.g.remove_dependency("mesh", "mat"))

    def test_remove_dependency_removes_edge(self):
        self.g.add_dependency("mesh", "mat")
        self.g.remove_dependency("mesh", "mat")
        self.assertFalse(self.g.has_dependency("mesh", "mat"))

    def test_get_edge_count(self):
        self.g.add_dependency("mesh", "mat")
        self.g.add_dependency("mat", "tex")
        self.assertEqual(self.g.get_edge_count(), 2)

    def test_no_duplicate_edges(self):
        self.g.add_dependency("mesh", "mat")
        self.g.add_dependency("mesh", "mat")
        deps = self.g.get_dependencies("mesh")
        self.assertEqual(deps.count("mat"), 1)


# ---------------------------------------------------------------------------
# AssetDependencyGraph — traversal
# ---------------------------------------------------------------------------

class TestAssetDependencyGraphTraversal(unittest.TestCase):
    def setUp(self):
        self.g = AssetDependencyGraph()
        for nid, ntype in [("level", "Level"), ("mesh", "Mesh"),
                            ("mat", "Material"), ("tex", "Texture")]:
            self.g.add_node(nid, ntype)
        self.g.add_dependency("level", "mesh")
        self.g.add_dependency("mesh", "mat")
        self.g.add_dependency("mat", "tex")

    def test_get_direct_dependencies(self):
        deps = self.g.get_dependencies("mesh")
        self.assertIn("mat", deps)
        self.assertNotIn("tex", deps)

    def test_get_transitive_dependencies(self):
        deps = self.g.get_dependencies("level", transitive=True)
        self.assertIn("mesh", deps)
        self.assertIn("mat", deps)
        self.assertIn("tex", deps)

    def test_get_direct_dependents(self):
        deps = self.g.get_dependents("mat")
        self.assertIn("mesh", deps)
        self.assertNotIn("level", deps)

    def test_get_transitive_dependents(self):
        deps = self.g.get_dependents("tex", transitive=True)
        self.assertIn("mat", deps)
        self.assertIn("mesh", deps)
        self.assertIn("level", deps)

    def test_get_roots(self):
        roots = self.g.get_roots()
        self.assertIn("level", roots)
        self.assertNotIn("tex", roots)

    def test_get_leaves(self):
        leaves = self.g.get_leaves()
        self.assertIn("tex", leaves)
        self.assertNotIn("level", leaves)

    def test_no_cycle_empty_list(self):
        cycles = self.g.detect_cycles()
        self.assertEqual(len(cycles), 0)

    def test_detect_cycle(self):
        g = AssetDependencyGraph()
        for nid in ["a", "b", "c"]:
            g.add_node(nid, "T")
        g.add_dependency("a", "b")
        g.add_dependency("b", "c")
        g.add_dependency("c", "a")
        cycles = g.detect_cycles()
        self.assertGreater(len(cycles), 0)

    def test_remove_node_cleans_edges(self):
        self.g.remove_node("mat")
        self.assertFalse(self.g.has_dependency("mesh", "mat"))


# ---------------------------------------------------------------------------
# AssetDependencyGraph — persistence
# ---------------------------------------------------------------------------

class TestAssetDependencyGraphPersistence(unittest.TestCase):
    def setUp(self):
        self.g = AssetDependencyGraph()
        self.g.add_node("m1", "Mesh", "/p1", tags=["hero"])
        self.g.add_node("t1", "Texture", "/p2")
        self.g.add_dependency("m1", "t1")

    def test_save_returns_true(self):
        path = str(TMP_DIR / "graph.json")
        self.assertTrue(self.g.save(path))

    def test_save_creates_file(self):
        path = str(TMP_DIR / "graph2.json")
        self.g.save(path)
        self.assertTrue(Path(path).exists())

    def test_load_restores_nodes(self):
        path = str(TMP_DIR / "graph3.json")
        self.g.save(path)
        g2 = AssetDependencyGraph()
        self.assertTrue(g2.load(path))
        self.assertTrue(g2.has_node("m1"))
        self.assertTrue(g2.has_node("t1"))

    def test_load_restores_edges(self):
        path = str(TMP_DIR / "graph4.json")
        self.g.save(path)
        g2 = AssetDependencyGraph()
        g2.load(path)
        self.assertTrue(g2.has_dependency("m1", "t1"))

    def test_clear_removes_all(self):
        self.g.clear()
        self.assertEqual(self.g.get_node_count(), 0)


# ---------------------------------------------------------------------------
# CacheEntry dataclass
# ---------------------------------------------------------------------------

class TestCacheEntryDataclass(unittest.TestCase):
    def test_target_id_field(self):
        e = CacheEntry("target_a", "src_hash", "out_hash", time.time())
        self.assertEqual(e.target_id, "target_a")

    def test_source_hash_field(self):
        e = CacheEntry("t", "abc123", "def456", 0.0)
        self.assertEqual(e.source_hash, "abc123")

    def test_output_hash_field(self):
        e = CacheEntry("t", "src", "out", 0.0)
        self.assertEqual(e.output_hash, "out")

    def test_age_seconds_positive(self):
        e = CacheEntry("t", "s", "o", time.time() - 5.0)
        self.assertGreater(e.age_seconds, 0.0)


# ---------------------------------------------------------------------------
# BuildCacheManager — core operations
# ---------------------------------------------------------------------------

class TestBuildCacheManagerCore(unittest.TestCase):
    def setUp(self):
        self.cache = BuildCacheManager()

    def test_store_returns_entry(self):
        e = self.cache.store("tgt_a", "src_hash_1", "out_hash_1")
        self.assertIsInstance(e, CacheEntry)

    def test_is_cached_true(self):
        self.cache.store("tgt_a", "src1", "out1")
        self.assertTrue(self.cache.is_cached("tgt_a"))

    def test_is_cached_false(self):
        self.assertFalse(self.cache.is_cached("ghost"))

    def test_is_valid_true(self):
        self.cache.store("tgt_a", "src1", "out1")
        self.assertTrue(self.cache.is_valid("tgt_a", "src1"))

    def test_is_valid_false_wrong_hash(self):
        self.cache.store("tgt_a", "src1", "out1")
        self.assertFalse(self.cache.is_valid("tgt_a", "src_different"))

    def test_is_valid_false_not_cached(self):
        self.assertFalse(self.cache.is_valid("ghost", "any"))

    def test_retrieve_returns_entry(self):
        self.cache.store("tgt_a", "src1", "out1")
        e = self.cache.retrieve("tgt_a")
        self.assertIsNotNone(e)
        self.assertEqual(e.source_hash, "src1")

    def test_retrieve_missing_returns_none(self):
        self.assertIsNone(self.cache.retrieve("ghost"))

    def test_invalidate_returns_true(self):
        self.cache.store("tgt_a", "s", "o")
        self.assertTrue(self.cache.invalidate("tgt_a"))

    def test_invalidate_removes_entry(self):
        self.cache.store("tgt_a", "s", "o")
        self.cache.invalidate("tgt_a")
        self.assertFalse(self.cache.is_cached("tgt_a"))

    def test_invalidate_missing_returns_false(self):
        self.assertFalse(self.cache.invalidate("ghost"))

    def test_invalidate_many(self):
        self.cache.store("a", "s", "o")
        self.cache.store("b", "s", "o")
        count = self.cache.invalidate_many(["a", "b", "ghost"])
        self.assertEqual(count, 2)

    def test_get_entry_count(self):
        self.cache.store("a", "s", "o")
        self.cache.store("b", "s", "o")
        self.assertEqual(self.cache.get_entry_count(), 2)

    def test_get_all_target_ids(self):
        self.cache.store("a", "s", "o")
        self.assertIn("a", self.cache.get_all_target_ids())

    def test_clear(self):
        self.cache.store("a", "s", "o")
        self.cache.clear()
        self.assertEqual(self.cache.get_entry_count(), 0)


# ---------------------------------------------------------------------------
# BuildCacheManager — hash utilities
# ---------------------------------------------------------------------------

class TestBuildCacheManagerHash(unittest.TestCase):
    def test_hash_string_non_empty(self):
        h = BuildCacheManager.hash_string("hello")
        self.assertTrue(len(h) == 64)

    def test_hash_string_deterministic(self):
        h1 = BuildCacheManager.hash_string("hello")
        h2 = BuildCacheManager.hash_string("hello")
        self.assertEqual(h1, h2)

    def test_hash_string_different_inputs(self):
        h1 = BuildCacheManager.hash_string("a")
        h2 = BuildCacheManager.hash_string("b")
        self.assertNotEqual(h1, h2)

    def test_hash_file_missing_returns_none(self):
        self.assertIsNone(BuildCacheManager.hash_file("/no/such/file.x"))

    def test_hash_prefix_lookup(self):
        cache = BuildCacheManager()
        h = BuildCacheManager.hash_string("src_content")
        cache.store("tgt", h, "out")
        results = cache.hash_prefix_lookup(h[:8])
        self.assertIn("tgt", results)


# ---------------------------------------------------------------------------
# BuildCacheManager — stale
# ---------------------------------------------------------------------------

class TestBuildCacheManagerStale(unittest.TestCase):
    def test_evict_stale_removes_old_entries(self):
        cache = BuildCacheManager()
        # Store an entry with a build_time in the far past
        e = CacheEntry("old_target", "src", "out", time.time() - 10000.0)
        cache._entries["old_target"] = e
        cache.store("new_target", "src2", "out2")
        removed = cache.evict_stale(max_age_seconds=5000.0)
        self.assertEqual(removed, 1)
        self.assertFalse(cache.is_cached("old_target"))
        self.assertTrue(cache.is_cached("new_target"))

    def test_get_stale_entries(self):
        cache = BuildCacheManager()
        e = CacheEntry("old", "s", "o", time.time() - 200.0)
        cache._entries["old"] = e
        stale = cache.get_stale_entries(max_age_seconds=100.0)
        self.assertEqual(len(stale), 1)


# ---------------------------------------------------------------------------
# BuildCacheManager — persistence
# ---------------------------------------------------------------------------

class TestBuildCacheManagerPersistence(unittest.TestCase):
    def setUp(self):
        self.cache = BuildCacheManager()
        self.cache.store("a", "src_a", "out_a")
        self.cache.store("b", "src_b", "out_b")

    def test_save_returns_true(self):
        path = str(TMP_DIR / "cache.json")
        self.assertTrue(self.cache.save(path))

    def test_save_creates_file(self):
        path = str(TMP_DIR / "cache2.json")
        self.cache.save(path)
        self.assertTrue(Path(path).exists())

    def test_load_restores_entries(self):
        path = str(TMP_DIR / "cache3.json")
        self.cache.save(path)
        c2 = BuildCacheManager()
        self.assertTrue(c2.load(path))
        self.assertTrue(c2.is_cached("a"))
        self.assertTrue(c2.is_cached("b"))

    def test_load_restores_source_hash(self):
        path = str(TMP_DIR / "cache4.json")
        self.cache.save(path)
        c2 = BuildCacheManager()
        c2.load(path)
        self.assertTrue(c2.is_valid("a", "src_a"))

    def test_save_no_path_returns_false(self):
        c = BuildCacheManager()
        self.assertFalse(c.save())

    def test_load_nonexistent_returns_false(self):
        c = BuildCacheManager()
        self.assertFalse(c.load("/no/such/file.json"))


# ---------------------------------------------------------------------------
# __init__ exports
# ---------------------------------------------------------------------------

class TestInitExports(unittest.TestCase):
    def test_asset_dependency_graph_exported(self):
        from AtlasAIEngine.intelligence import AssetDependencyGraph as ADG
        self.assertIsNotNone(ADG)

    def test_asset_node_exported(self):
        from AtlasAIEngine.intelligence import AssetNode as AN
        self.assertIsNotNone(AN)

    def test_build_cache_manager_exported(self):
        from AtlasAIEngine.intelligence import BuildCacheManager as BCM
        self.assertIsNotNone(BCM)

    def test_cache_entry_exported(self):
        from AtlasAIEngine.intelligence import CacheEntry as CE
        self.assertIsNotNone(CE)


if __name__ == "__main__":
    unittest.main()
