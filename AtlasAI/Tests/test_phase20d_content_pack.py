"""Phase 20D — Tests for ContentPackRegistry.h and ContentPackLoader."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

from AtlasAIEngine.intelligence import (
    ContentPackLoader,
    ContentPackManifest,
)

TMP_DIR = Path("/tmp/test_phase20d")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# ContentPackRegistry.h tests
# ---------------------------------------------------------------------------

def _reg() -> str:
    return (SCENE_DIR / "ContentPackRegistry.h").read_text()


class TestContentPackRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "ContentPackRegistry.h").exists())


class TestContentPackRegistryHeader(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _reg())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _reg())

    def test_class_declared(self):
        self.assertIn("class ContentPackRegistry", _reg())


class TestContentPackRegistryAPI(unittest.TestCase):
    def test_register_pack(self):
        self.assertIn("RegisterPack", _reg())

    def test_unregister_pack(self):
        self.assertIn("UnregisterPack", _reg())

    def test_is_registered(self):
        self.assertIn("IsRegistered", _reg())

    def test_get_pack_count(self):
        self.assertIn("GetPackCount", _reg())

    def test_load_pack(self):
        self.assertIn("LoadPack", _reg())

    def test_unload_pack(self):
        self.assertIn("UnloadPack", _reg())

    def test_is_loaded(self):
        self.assertIn("IsLoaded", _reg())

    def test_get_loaded_count(self):
        self.assertIn("GetLoadedCount", _reg())

    def test_get_pack(self):
        self.assertIn("GetPack", _reg())

    def test_get_all_pack_ids(self):
        self.assertIn("GetAllPackIds", _reg())

    def test_get_loaded_packs(self):
        self.assertIn("GetLoadedPacks", _reg())

    def test_set_asset_count(self):
        self.assertIn("SetAssetCount", _reg())

    def test_for_each(self):
        self.assertIn("ForEach", _reg())

    def test_clear(self):
        self.assertIn("Clear", _reg())

    def test_set_on_pack_loaded_callback(self):
        self.assertIn("SetOnPackLoadedCallback", _reg())

    def test_set_on_pack_unloaded_callback(self):
        self.assertIn("SetOnPackUnloadedCallback", _reg())


class TestContentPackRegistryPackRecord(unittest.TestCase):
    def test_pack_record_struct(self):
        self.assertIn("PackRecord", _reg())

    def test_pack_id_field(self):
        self.assertIn("packId", _reg())

    def test_name_field(self):
        self.assertIn("name", _reg())

    def test_version_field(self):
        self.assertIn("version", _reg())

    def test_manifest_path_field(self):
        self.assertIn("manifestPath", _reg())

    def test_pack_state_enum(self):
        self.assertIn("PackState", _reg())

    def test_asset_count_field(self):
        self.assertIn("assetCount", _reg())


# ---------------------------------------------------------------------------
# ContentPackManifest dataclass
# ---------------------------------------------------------------------------

class TestContentPackManifestDataclass(unittest.TestCase):
    def test_pack_id_field(self):
        m = ContentPackManifest("pack_01", "Test Pack", "1.0", "/tmp/m.json")
        self.assertEqual(m.pack_id, "pack_01")

    def test_name_field(self):
        m = ContentPackManifest("p", "My Pack", "2.0", "/tmp/m.json")
        self.assertEqual(m.name, "My Pack")

    def test_version_field(self):
        m = ContentPackManifest("p", "N", "3.1", "/tmp/m.json")
        self.assertEqual(m.version, "3.1")

    def test_assets_default_empty(self):
        m = ContentPackManifest("p", "N", "1.0", "")
        self.assertEqual(m.assets, [])

    def test_dependencies_default_empty(self):
        m = ContentPackManifest("p", "N", "1.0", "")
        self.assertEqual(m.dependencies, [])

    def test_metadata_default_empty(self):
        m = ContentPackManifest("p", "N", "1.0", "")
        self.assertIsInstance(m.metadata, dict)

    def test_asset_count_property(self):
        m = ContentPackManifest("p", "N", "1.0", "",
                                assets=["a.json", "b.json", "c.json"])
        self.assertEqual(m.asset_count, 3)


# ---------------------------------------------------------------------------
# ContentPackLoader — registration
# ---------------------------------------------------------------------------

def _make_manifest_data(pack_id: str, assets: list = None,
                         deps: list = None) -> dict:
    return {
        "pack_id": pack_id,
        "name": f"{pack_id} pack",
        "version": "1.0",
        "assets": assets or [],
        "dependencies": deps or [],
    }


class TestContentPackLoaderRegistration(unittest.TestCase):
    def setUp(self):
        self.loader = ContentPackLoader(str(TMP_DIR))

    def test_register_manifest_returns_manifest(self):
        m = self.loader.register_manifest(_make_manifest_data("pack_a"))
        self.assertIsInstance(m, ContentPackManifest)

    def test_register_increments_count(self):
        self.loader.register_manifest(_make_manifest_data("pack_a"))
        self.loader.register_manifest(_make_manifest_data("pack_b"))
        self.assertEqual(self.loader.get_registered_count(), 2)

    def test_get_manifest_returns_manifest(self):
        self.loader.register_manifest(_make_manifest_data("pack_a"))
        m = self.loader.get_manifest("pack_a")
        self.assertIsNotNone(m)
        self.assertEqual(m.pack_id, "pack_a")

    def test_get_manifest_missing_returns_none(self):
        self.assertIsNone(self.loader.get_manifest("ghost"))

    def test_get_all_pack_ids(self):
        self.loader.register_manifest(_make_manifest_data("p1"))
        self.loader.register_manifest(_make_manifest_data("p2"))
        ids = self.loader.get_all_pack_ids()
        self.assertIn("p1", ids)
        self.assertIn("p2", ids)

    def test_clear_removes_all(self):
        self.loader.register_manifest(_make_manifest_data("pack_a"))
        self.loader.clear()
        self.assertEqual(self.loader.get_registered_count(), 0)


# ---------------------------------------------------------------------------
# ContentPackLoader — load / unload
# ---------------------------------------------------------------------------

class TestContentPackLoaderLoadUnload(unittest.TestCase):
    def setUp(self):
        self.loader = ContentPackLoader(str(TMP_DIR))
        self.loader.register_manifest(_make_manifest_data("pack_alpha"))

    def test_load_pack_returns_true(self):
        self.assertTrue(self.loader.load_pack("pack_alpha"))

    def test_load_pack_marks_loaded(self):
        self.loader.load_pack("pack_alpha")
        self.assertTrue(self.loader.is_loaded("pack_alpha"))

    def test_load_pack_unknown_returns_false(self):
        self.assertFalse(self.loader.load_pack("ghost"))

    def test_unload_pack_returns_true(self):
        self.loader.load_pack("pack_alpha")
        self.assertTrue(self.loader.unload_pack("pack_alpha"))

    def test_unload_pack_removes_loaded(self):
        self.loader.load_pack("pack_alpha")
        self.loader.unload_pack("pack_alpha")
        self.assertFalse(self.loader.is_loaded("pack_alpha"))

    def test_unload_pack_not_loaded_returns_false(self):
        self.assertFalse(self.loader.unload_pack("pack_alpha"))

    def test_get_loaded_count(self):
        self.loader.register_manifest(_make_manifest_data("pack_beta"))
        self.loader.load_pack("pack_alpha")
        self.loader.load_pack("pack_beta")
        self.assertEqual(self.loader.get_loaded_count(), 2)


# ---------------------------------------------------------------------------
# ContentPackLoader — discovery via real files
# ---------------------------------------------------------------------------

class TestContentPackLoaderDiscovery(unittest.TestCase):
    def setUp(self):
        self.root = TMP_DIR / "discovery_root"
        (self.root / "PackA").mkdir(parents=True, exist_ok=True)
        (self.root / "PackB").mkdir(parents=True, exist_ok=True)
        (self.root / "PackA" / "pack_manifest.json").write_text(
            json.dumps(_make_manifest_data("disc_pack_a", assets=["f1.json"]))
        )
        (self.root / "PackB" / "pack_manifest.json").write_text(
            json.dumps(_make_manifest_data("disc_pack_b"))
        )
        self.loader = ContentPackLoader(str(self.root))

    def test_discover_returns_list(self):
        ids = self.loader.discover()
        self.assertIsInstance(ids, list)

    def test_discover_finds_both_packs(self):
        ids = self.loader.discover()
        self.assertIn("disc_pack_a", ids)
        self.assertIn("disc_pack_b", ids)

    def test_discover_registers_assets(self):
        self.loader.discover()
        m = self.loader.get_manifest("disc_pack_a")
        self.assertEqual(m.asset_count, 1)


# ---------------------------------------------------------------------------
# ContentPackLoader — dependency resolution
# ---------------------------------------------------------------------------

class TestContentPackLoaderDependencies(unittest.TestCase):
    def setUp(self):
        self.loader = ContentPackLoader(str(TMP_DIR))
        self.loader.register_manifest(_make_manifest_data("core"))
        self.loader.register_manifest(_make_manifest_data("audio", deps=["core"]))
        self.loader.register_manifest(
            _make_manifest_data("full", deps=["core", "audio"])
        )

    def test_load_order_no_deps(self):
        order = self.loader.get_load_order("core")
        self.assertIn("core", order)

    def test_load_order_single_dep(self):
        order = self.loader.get_load_order("audio")
        self.assertIn("core", order)
        self.assertIn("audio", order)
        # core must come before audio
        self.assertLess(order.index("core"), order.index("audio"))

    def test_load_order_transitive(self):
        order = self.loader.get_load_order("full")
        self.assertIn("core", order)
        self.assertIn("audio", order)
        self.assertIn("full", order)
        self.assertLess(order.index("core"), order.index("full"))


# ---------------------------------------------------------------------------
# ContentPackLoader — export
# ---------------------------------------------------------------------------

class TestContentPackLoaderExport(unittest.TestCase):
    def setUp(self):
        self.loader = ContentPackLoader(str(TMP_DIR))
        self.loader.register_manifest(
            _make_manifest_data("export_pack", assets=["x.json"])
        )

    def test_export_manifest_returns_true(self):
        path = str(TMP_DIR / "export_test.json")
        self.assertTrue(self.loader.export_manifest("export_pack", path))

    def test_export_manifest_creates_file(self):
        path = str(TMP_DIR / "export_test2.json")
        self.loader.export_manifest("export_pack", path)
        self.assertTrue(Path(path).exists())

    def test_export_manifest_valid_json(self):
        path = str(TMP_DIR / "export_test3.json")
        self.loader.export_manifest("export_pack", path)
        data = json.loads(Path(path).read_text())
        self.assertEqual(data["pack_id"], "export_pack")

    def test_export_manifest_missing_pack_returns_false(self):
        self.assertFalse(
            self.loader.export_manifest("ghost", str(TMP_DIR / "ghost.json"))
        )


# ---------------------------------------------------------------------------
# __init__ exports
# ---------------------------------------------------------------------------

class TestInitExports(unittest.TestCase):
    def test_content_pack_loader_exported(self):
        from AtlasAIEngine.intelligence import ContentPackLoader as CPL
        self.assertIsNotNone(CPL)

    def test_content_pack_manifest_exported(self):
        from AtlasAIEngine.intelligence import ContentPackManifest as CPM
        self.assertIsNotNone(CPM)


if __name__ == "__main__":
    unittest.main()
