"""Phase 23D — Tests for TerrainChunkRegistry.h and TerrainChunkLoader."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

from AtlasAIEngine.intelligence import (
    TerrainChunkLoader,
    TerrainChunkManifest,
    ChunkCoord,
)

TMP_DIR = Path("/tmp/test_phase23d")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# TerrainChunkRegistry.h tests
# ---------------------------------------------------------------------------

def _reg() -> str:
    return (SCENE_DIR / "TerrainChunkRegistry.h").read_text()


class TestTerrainChunkRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "TerrainChunkRegistry.h").exists())


class TestTerrainChunkRegistryHeader(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _reg())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _reg())

    def test_class_declared(self):
        self.assertIn("class TerrainChunkRegistry", _reg())


class TestTerrainChunkRegistryAPI(unittest.TestCase):
    def test_register_chunk(self):
        self.assertIn("RegisterChunk", _reg())

    def test_unregister_chunk(self):
        self.assertIn("UnregisterChunk", _reg())

    def test_is_registered(self):
        self.assertIn("IsRegistered", _reg())

    def test_get_chunk_count(self):
        self.assertIn("GetChunkCount", _reg())

    def test_load_chunk(self):
        self.assertIn("LoadChunk", _reg())

    def test_unload_chunk(self):
        self.assertIn("UnloadChunk", _reg())

    def test_is_loaded(self):
        self.assertIn("IsLoaded", _reg())

    def test_get_loaded_count(self):
        self.assertIn("GetLoadedCount", _reg())

    def test_get_loaded_chunk_ids(self):
        self.assertIn("GetLoadedChunkIds", _reg())

    def test_find_chunk_at_coord(self):
        self.assertIn("FindChunkAtCoord", _reg())

    def test_get_chunks_in_range(self):
        self.assertIn("GetChunksInRange", _reg())

    def test_add_bundle(self):
        self.assertIn("AddBundle", _reg())

    def test_get_bundles(self):
        self.assertIn("GetBundles", _reg())

    def test_set_active_lod(self):
        self.assertIn("SetActiveLOD", _reg())

    def test_get_active_lod(self):
        self.assertIn("GetActiveLOD", _reg())

    def test_set_material(self):
        self.assertIn("SetMaterial", _reg())

    def test_mark_modified(self):
        self.assertIn("MarkModified", _reg())

    def test_get_modified_chunk_ids(self):
        self.assertIn("GetModifiedChunkIds", _reg())

    def test_get_always_loaded_chunk_ids(self):
        self.assertIn("GetAlwaysLoadedChunkIds", _reg())

    def test_get_chunks_by_priority(self):
        self.assertIn("GetChunksByPriority", _reg())

    def test_get_chunk(self):
        self.assertIn("GetChunk", _reg())

    def test_get_all_chunk_ids(self):
        self.assertIn("GetAllChunkIds", _reg())

    def test_for_each(self):
        self.assertIn("ForEach", _reg())

    def test_on_loaded_callback(self):
        self.assertIn("SetOnChunkLoadedCallback", _reg())

    def test_on_unloaded_callback(self):
        self.assertIn("SetOnChunkUnloadedCallback", _reg())

    def test_clear(self):
        self.assertIn("Clear", _reg())


class TestTerrainChunkRegistryStructs(unittest.TestCase):
    def test_chunk_record_struct(self):
        self.assertIn("ChunkRecord", _reg())

    def test_chunk_coord_struct(self):
        self.assertIn("ChunkCoord", _reg())

    def test_chunk_state_enum(self):
        self.assertIn("ChunkState", _reg())

    def test_lod_level_enum(self):
        self.assertIn("LODLevel", _reg())

    def test_is_modified_field(self):
        self.assertIn("isModified", _reg())

    def test_always_loaded_field(self):
        self.assertIn("alwaysLoaded", _reg())

    def test_bundle_ids_field(self):
        self.assertIn("bundleIds", _reg())

    def test_resolution_field(self):
        self.assertIn("resolution", _reg())


# ---------------------------------------------------------------------------
# ChunkCoord dataclass
# ---------------------------------------------------------------------------

class TestChunkCoordDataclass(unittest.TestCase):
    def test_defaults(self):
        c = ChunkCoord()
        self.assertEqual(c.x, 0)
        self.assertEqual(c.z, 0)

    def test_custom_values(self):
        c = ChunkCoord(3, 7)
        self.assertEqual(c.x, 3)
        self.assertEqual(c.z, 7)

    def test_equality_true(self):
        self.assertEqual(ChunkCoord(1, 2), ChunkCoord(1, 2))

    def test_equality_false(self):
        self.assertNotEqual(ChunkCoord(1, 2), ChunkCoord(1, 3))

    def test_hashable(self):
        s = {ChunkCoord(0, 0), ChunkCoord(1, 0)}
        self.assertEqual(len(s), 2)

    def test_distance_to_zero(self):
        self.assertEqual(ChunkCoord(0, 0).distance_to(ChunkCoord(0, 0)), 0.0)

    def test_distance_to_nonzero(self):
        self.assertGreater(ChunkCoord(0, 0).distance_to(ChunkCoord(3, 4)), 0.0)


# ---------------------------------------------------------------------------
# TerrainChunkManifest dataclass
# ---------------------------------------------------------------------------

class TestTerrainChunkManifestDataclass(unittest.TestCase):
    def test_chunk_id_field(self):
        m = TerrainChunkManifest("chunk_0_0", ChunkCoord(0, 0))
        self.assertEqual(m.chunk_id, "chunk_0_0")

    def test_resolution_default(self):
        m = TerrainChunkManifest("chunk_0_0", ChunkCoord(0, 0))
        self.assertEqual(m.resolution, 16)

    def test_bundle_ids_default_empty(self):
        m = TerrainChunkManifest("c", ChunkCoord())
        self.assertEqual(m.bundle_ids, [])

    def test_bundle_count_zero(self):
        m = TerrainChunkManifest("c", ChunkCoord())
        self.assertEqual(m.bundle_count, 0)

    def test_world_origin_x(self):
        m = TerrainChunkManifest("c", ChunkCoord(2, 0), chunk_size=100.0)
        self.assertAlmostEqual(m.world_origin_x, 200.0)

    def test_world_origin_z(self):
        m = TerrainChunkManifest("c", ChunkCoord(0, 3), chunk_size=100.0)
        self.assertAlmostEqual(m.world_origin_z, 300.0)


# ---------------------------------------------------------------------------
# TerrainChunkLoader — registration
# ---------------------------------------------------------------------------

def _make_loader_with_chunks() -> TerrainChunkLoader:
    loader = TerrainChunkLoader("/tmp")
    for (cx, cz, cid) in [(0, 0, "c00"), (1, 0, "c10"), (0, 1, "c01"), (2, 2, "c22")]:
        loader.register_from_dict({
            "chunk_id": cid,
            "coord_x": cx,
            "coord_z": cz,
            "resolution": 16,
            "chunk_size": 100.0,
            "priority": cx + cz,
        })
    return loader


class TestTerrainChunkLoaderRegistration(unittest.TestCase):
    def setUp(self):
        self.loader = _make_loader_with_chunks()

    def test_register_from_dict_returns_manifest(self):
        m = self.loader.register_from_dict({"chunk_id": "cx", "coord_x": 9, "coord_z": 9})
        self.assertIsInstance(m, TerrainChunkManifest)

    def test_get_chunk_count(self):
        self.assertEqual(self.loader.get_chunk_count(), 4)

    def test_get_all_chunk_ids(self):
        ids = self.loader.get_all_chunk_ids()
        self.assertIn("c00", ids)
        self.assertIn("c22", ids)

    def test_get_chunk_returns_manifest(self):
        m = self.loader.get_chunk("c10")
        self.assertIsNotNone(m)
        self.assertEqual(m.coord.x, 1)

    def test_get_chunk_missing_returns_none(self):
        self.assertIsNone(self.loader.get_chunk("ghost"))

    def test_get_chunk_at_coord(self):
        m = self.loader.get_chunk_at_coord(1, 0)
        self.assertIsNotNone(m)
        self.assertEqual(m.chunk_id, "c10")

    def test_get_chunk_at_coord_missing(self):
        self.assertIsNone(self.loader.get_chunk_at_coord(99, 99))

    def test_unregister_returns_true(self):
        self.assertTrue(self.loader.unregister("c22"))

    def test_unregister_removes_chunk(self):
        self.loader.unregister("c22")
        self.assertIsNone(self.loader.get_chunk("c22"))

    def test_unregister_missing_returns_false(self):
        self.assertFalse(self.loader.unregister("ghost"))


# ---------------------------------------------------------------------------
# TerrainChunkLoader — load/unload
# ---------------------------------------------------------------------------

class TestTerrainChunkLoaderLoadUnload(unittest.TestCase):
    def setUp(self):
        self.loader = _make_loader_with_chunks()

    def test_load_chunk_returns_true(self):
        self.assertTrue(self.loader.load_chunk("c00"))

    def test_is_loaded_true(self):
        self.loader.load_chunk("c00")
        self.assertTrue(self.loader.is_loaded("c00"))

    def test_is_loaded_false_before_load(self):
        self.assertFalse(self.loader.is_loaded("c00"))

    def test_load_missing_returns_false(self):
        self.assertFalse(self.loader.load_chunk("ghost"))

    def test_unload_chunk_returns_true(self):
        self.loader.load_chunk("c00")
        self.assertTrue(self.loader.unload_chunk("c00"))

    def test_unload_removes_from_loaded(self):
        self.loader.load_chunk("c00")
        self.loader.unload_chunk("c00")
        self.assertFalse(self.loader.is_loaded("c00"))

    def test_unload_not_loaded_returns_false(self):
        self.assertFalse(self.loader.unload_chunk("c00"))

    def test_get_loaded_count(self):
        self.loader.load_chunk("c00")
        self.loader.load_chunk("c10")
        self.assertEqual(self.loader.get_loaded_count(), 2)

    def test_get_loaded_chunk_ids(self):
        self.loader.load_chunk("c00")
        ids = self.loader.get_loaded_chunk_ids()
        self.assertIn("c00", ids)


# ---------------------------------------------------------------------------
# TerrainChunkLoader — queries
# ---------------------------------------------------------------------------

class TestTerrainChunkLoaderQueries(unittest.TestCase):
    def setUp(self):
        self.loader = _make_loader_with_chunks()
        # Add an always_loaded chunk
        self.loader.register_from_dict({
            "chunk_id": "al_chunk",
            "coord_x": 5,
            "coord_z": 5,
            "always_loaded": True,
            "priority": 10,
        })
        # Add a material chunk
        self.loader.register_from_dict({
            "chunk_id": "mat_chunk",
            "coord_x": 6,
            "coord_z": 6,
            "material_id": "rock_material",
        })

    def test_get_chunks_in_range(self):
        center = ChunkCoord(1, 0)
        chunks = self.loader.get_chunks_in_range(center, radius=1)
        ids = [c.chunk_id for c in chunks]
        self.assertIn("c00", ids)
        self.assertIn("c10", ids)
        self.assertIn("c01", ids)

    def test_get_chunks_in_range_excludes_far(self):
        center = ChunkCoord(0, 0)
        chunks = self.loader.get_chunks_in_range(center, radius=1)
        ids = [c.chunk_id for c in chunks]
        self.assertNotIn("c22", ids)

    def test_get_always_loaded_chunks(self):
        chunks = self.loader.get_always_loaded_chunks()
        ids = [c.chunk_id for c in chunks]
        self.assertIn("al_chunk", ids)

    def test_get_chunks_by_priority(self):
        chunks = self.loader.get_chunks_by_priority(min_priority=5)
        ids = [c.chunk_id for c in chunks]
        self.assertIn("al_chunk", ids)

    def test_get_chunks_by_material(self):
        chunks = self.loader.get_chunks_by_material("rock_material")
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].chunk_id, "mat_chunk")

    def test_clear(self):
        self.loader.clear()
        self.assertEqual(self.loader.get_chunk_count(), 0)
        self.assertEqual(self.loader.get_loaded_count(), 0)


# ---------------------------------------------------------------------------
# __init__ exports
# ---------------------------------------------------------------------------

class TestInitExports(unittest.TestCase):
    def test_terrain_chunk_loader_exported(self):
        from AtlasAIEngine.intelligence import TerrainChunkLoader as TCL
        self.assertIsNotNone(TCL)

    def test_terrain_chunk_manifest_exported(self):
        from AtlasAIEngine.intelligence import TerrainChunkManifest as TCM
        self.assertIsNotNone(TCM)

    def test_chunk_coord_exported(self):
        from AtlasAIEngine.intelligence import ChunkCoord as CC
        self.assertIsNotNone(CC)


if __name__ == "__main__":
    unittest.main()
