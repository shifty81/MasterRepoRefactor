"""Phase 21D — Tests for RuntimeBundleRegistry.h and RuntimeBundleLoader."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

from AtlasAIEngine.intelligence import (
    RuntimeBundleLoader,
    BundleManifest,
    AssetRef,
)

TMP_DIR = Path("/tmp/test_phase21d")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# RuntimeBundleRegistry.h tests
# ---------------------------------------------------------------------------

def _reg() -> str:
    return (SCENE_DIR / "RuntimeBundleRegistry.h").read_text()


class TestRuntimeBundleRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "RuntimeBundleRegistry.h").exists())


class TestRuntimeBundleRegistryHeader(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _reg())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _reg())

    def test_class_declared(self):
        self.assertIn("class RuntimeBundleRegistry", _reg())


class TestRuntimeBundleRegistryAPI(unittest.TestCase):
    def test_register_bundle(self):
        self.assertIn("RegisterBundle", _reg())

    def test_unregister_bundle(self):
        self.assertIn("UnregisterBundle", _reg())

    def test_is_registered(self):
        self.assertIn("IsRegistered", _reg())

    def test_get_bundle_count(self):
        self.assertIn("GetBundleCount", _reg())

    def test_add_asset(self):
        self.assertIn("AddAsset", _reg())

    def test_get_asset_count(self):
        self.assertIn("GetAssetCount", _reg())

    def test_load_bundle(self):
        self.assertIn("LoadBundle", _reg())

    def test_unload_bundle(self):
        self.assertIn("UnloadBundle", _reg())

    def test_is_loaded(self):
        self.assertIn("IsLoaded", _reg())

    def test_get_loaded_count(self):
        self.assertIn("GetLoadedCount", _reg())

    def test_get_loaded_bundle_ids(self):
        self.assertIn("GetLoadedBundleIds", _reg())

    def test_get_bundle(self):
        self.assertIn("GetBundle", _reg())

    def test_get_all_bundle_ids(self):
        self.assertIn("GetAllBundleIds", _reg())

    def test_get_required_bundles(self):
        self.assertIn("GetRequiredBundles", _reg())

    def test_for_each(self):
        self.assertIn("ForEach", _reg())

    def test_get_total_estimated_size(self):
        self.assertIn("GetTotalEstimatedSize", _reg())

    def test_clear(self):
        self.assertIn("Clear", _reg())

    def test_on_bundle_loaded_callback(self):
        self.assertIn("SetOnBundleLoadedCallback", _reg())

    def test_on_bundle_unloaded_callback(self):
        self.assertIn("SetOnBundleUnloadedCallback", _reg())


class TestRuntimeBundleRegistryStructs(unittest.TestCase):
    def test_bundle_record_struct(self):
        self.assertIn("BundleRecord", _reg())

    def test_asset_ref_struct(self):
        self.assertIn("AssetRef", _reg())

    def test_bundle_state_enum(self):
        self.assertIn("BundleState", _reg())

    def test_bundle_id_field(self):
        self.assertIn("bundleId", _reg())

    def test_required_field(self):
        self.assertIn("required", _reg())

    def test_estimated_size_bytes_field(self):
        self.assertIn("estimatedSizeBytes", _reg())


# ---------------------------------------------------------------------------
# AssetRef dataclass
# ---------------------------------------------------------------------------

class TestAssetRefDataclass(unittest.TestCase):
    def test_asset_id_field(self):
        a = AssetRef("asset_01", "StaticMesh", "/path/mesh.fbx")
        self.assertEqual(a.asset_id, "asset_01")

    def test_asset_type_field(self):
        a = AssetRef("a", "Texture", "/path/tex.png")
        self.assertEqual(a.asset_type, "Texture")

    def test_path_field(self):
        a = AssetRef("a", "T", "/some/path.json")
        self.assertEqual(a.path, "/some/path.json")


# ---------------------------------------------------------------------------
# BundleManifest dataclass
# ---------------------------------------------------------------------------

class TestBundleManifestDataclass(unittest.TestCase):
    def test_bundle_id_field(self):
        m = BundleManifest("bundle_01", "Level 01", "1.0", "")
        self.assertEqual(m.bundle_id, "bundle_01")

    def test_name_field(self):
        m = BundleManifest("b", "Bundle Name", "2.0", "")
        self.assertEqual(m.name, "Bundle Name")

    def test_version_field(self):
        m = BundleManifest("b", "N", "3.1", "")
        self.assertEqual(m.version, "3.1")

    def test_assets_default_empty(self):
        m = BundleManifest("b", "N", "1.0", "")
        self.assertEqual(m.assets, [])

    def test_required_default_false(self):
        m = BundleManifest("b", "N", "1.0", "")
        self.assertFalse(m.required)

    def test_estimated_size_default_zero(self):
        m = BundleManifest("b", "N", "1.0", "")
        self.assertEqual(m.estimated_size_bytes, 0)

    def test_asset_count_property(self):
        a1 = AssetRef("a1", "T", "/p")
        a2 = AssetRef("a2", "T", "/p2")
        m = BundleManifest("b", "N", "1.0", "", assets=[a1, a2])
        self.assertEqual(m.asset_count, 2)


# ---------------------------------------------------------------------------
# RuntimeBundleLoader — registration
# ---------------------------------------------------------------------------

def _make_bundle_data(bundle_id: str, assets: list = None,
                      required: bool = False, size: int = 0) -> dict:
    return {
        "bundle_id": bundle_id,
        "name": f"{bundle_id} bundle",
        "version": "1.0",
        "required": required,
        "estimated_size_bytes": size,
        "assets": assets or [],
    }


class TestRuntimeBundleLoaderRegistration(unittest.TestCase):
    def setUp(self):
        self.loader = RuntimeBundleLoader(str(TMP_DIR))

    def test_register_manifest_returns_manifest(self):
        m = self.loader.register_manifest(_make_bundle_data("b1"))
        self.assertIsInstance(m, BundleManifest)

    def test_register_increments_count(self):
        self.loader.register_manifest(_make_bundle_data("b1"))
        self.loader.register_manifest(_make_bundle_data("b2"))
        self.assertEqual(self.loader.get_registered_count(), 2)

    def test_get_manifest_returns_manifest(self):
        self.loader.register_manifest(_make_bundle_data("b1"))
        m = self.loader.get_manifest("b1")
        self.assertIsNotNone(m)
        self.assertEqual(m.bundle_id, "b1")

    def test_get_manifest_missing_returns_none(self):
        self.assertIsNone(self.loader.get_manifest("ghost"))

    def test_get_all_bundle_ids(self):
        self.loader.register_manifest(_make_bundle_data("b1"))
        self.loader.register_manifest(_make_bundle_data("b2"))
        ids = self.loader.get_all_bundle_ids()
        self.assertIn("b1", ids)
        self.assertIn("b2", ids)

    def test_clear_removes_all(self):
        self.loader.register_manifest(_make_bundle_data("b1"))
        self.loader.clear()
        self.assertEqual(self.loader.get_registered_count(), 0)


# ---------------------------------------------------------------------------
# RuntimeBundleLoader — load/unload
# ---------------------------------------------------------------------------

class TestRuntimeBundleLoaderLoadUnload(unittest.TestCase):
    def setUp(self):
        self.loader = RuntimeBundleLoader(str(TMP_DIR))
        self.loader.register_manifest(_make_bundle_data("level_01"))

    def test_load_bundle_returns_true(self):
        self.assertTrue(self.loader.load_bundle("level_01"))

    def test_load_bundle_marks_loaded(self):
        self.loader.load_bundle("level_01")
        self.assertTrue(self.loader.is_loaded("level_01"))

    def test_load_unknown_returns_false(self):
        self.assertFalse(self.loader.load_bundle("ghost"))

    def test_unload_bundle_returns_true(self):
        self.loader.load_bundle("level_01")
        self.assertTrue(self.loader.unload_bundle("level_01"))

    def test_unload_removes_loaded(self):
        self.loader.load_bundle("level_01")
        self.loader.unload_bundle("level_01")
        self.assertFalse(self.loader.is_loaded("level_01"))

    def test_unload_not_loaded_returns_false(self):
        self.assertFalse(self.loader.unload_bundle("level_01"))

    def test_get_loaded_count(self):
        self.loader.register_manifest(_make_bundle_data("level_02"))
        self.loader.load_bundle("level_01")
        self.loader.load_bundle("level_02")
        self.assertEqual(self.loader.get_loaded_count(), 2)

    def test_get_loaded_bundle_ids(self):
        self.loader.load_bundle("level_01")
        ids = self.loader.get_loaded_bundle_ids()
        self.assertIn("level_01", ids)


# ---------------------------------------------------------------------------
# RuntimeBundleLoader — required bundles and size
# ---------------------------------------------------------------------------

class TestRuntimeBundleLoaderMetadata(unittest.TestCase):
    def setUp(self):
        self.loader = RuntimeBundleLoader(str(TMP_DIR))
        self.loader.register_manifest(
            _make_bundle_data("core", required=True, size=1024)
        )
        self.loader.register_manifest(
            _make_bundle_data("optional", required=False, size=512)
        )

    def test_get_required_bundles(self):
        req = self.loader.get_required_bundles()
        self.assertEqual(len(req), 1)
        self.assertEqual(req[0].bundle_id, "core")

    def test_get_total_estimated_size(self):
        total = self.loader.get_total_estimated_size()
        self.assertEqual(total, 1536)


# ---------------------------------------------------------------------------
# RuntimeBundleLoader — discovery
# ---------------------------------------------------------------------------

class TestRuntimeBundleLoaderDiscovery(unittest.TestCase):
    def setUp(self):
        self.root = TMP_DIR / "bundle_discovery"
        (self.root / "Level01").mkdir(parents=True, exist_ok=True)
        (self.root / "Level02").mkdir(parents=True, exist_ok=True)
        (self.root / "Level01" / "bundle_manifest.json").write_text(
            json.dumps(_make_bundle_data("disc_bundle_a",
                       assets=[{"asset_id": "a1", "asset_type": "Mesh",
                                 "path": "/p/a.fbx"}]))
        )
        (self.root / "Level02" / "bundle_manifest.json").write_text(
            json.dumps(_make_bundle_data("disc_bundle_b"))
        )
        self.loader = RuntimeBundleLoader(str(self.root))

    def test_discover_returns_list(self):
        ids = self.loader.discover()
        self.assertIsInstance(ids, list)

    def test_discover_finds_both(self):
        ids = self.loader.discover()
        self.assertIn("disc_bundle_a", ids)
        self.assertIn("disc_bundle_b", ids)

    def test_discover_registers_assets(self):
        self.loader.discover()
        m = self.loader.get_manifest("disc_bundle_a")
        self.assertEqual(m.asset_count, 1)


# ---------------------------------------------------------------------------
# RuntimeBundleLoader — export
# ---------------------------------------------------------------------------

class TestRuntimeBundleLoaderExport(unittest.TestCase):
    def setUp(self):
        self.loader = RuntimeBundleLoader(str(TMP_DIR))
        self.loader.register_manifest(
            _make_bundle_data("export_bundle", required=True, size=2048)
        )

    def test_export_manifest_returns_true(self):
        path = str(TMP_DIR / "bundle_export.json")
        self.assertTrue(self.loader.export_manifest("export_bundle", path))

    def test_export_manifest_creates_file(self):
        path = str(TMP_DIR / "bundle_export2.json")
        self.loader.export_manifest("export_bundle", path)
        self.assertTrue(Path(path).exists())

    def test_export_manifest_valid_json(self):
        path = str(TMP_DIR / "bundle_export3.json")
        self.loader.export_manifest("export_bundle", path)
        data = json.loads(Path(path).read_text())
        self.assertEqual(data["bundle_id"], "export_bundle")
        self.assertTrue(data["required"])

    def test_export_missing_returns_false(self):
        self.assertFalse(
            self.loader.export_manifest("ghost", str(TMP_DIR / "ghost.json"))
        )


# ---------------------------------------------------------------------------
# __init__ exports
# ---------------------------------------------------------------------------

class TestInitExports(unittest.TestCase):
    def test_runtime_bundle_loader_exported(self):
        from AtlasAIEngine.intelligence import RuntimeBundleLoader as RBL
        self.assertIsNotNone(RBL)

    def test_bundle_manifest_exported(self):
        from AtlasAIEngine.intelligence import BundleManifest as BM
        self.assertIsNotNone(BM)

    def test_asset_ref_exported(self):
        from AtlasAIEngine.intelligence import AssetRef as AR
        self.assertIsNotNone(AR)


if __name__ == "__main__":
    unittest.main()
