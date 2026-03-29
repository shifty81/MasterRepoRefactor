"""Phase 39B — Tests for MorphTargetPipeline and AssetBundlePipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    MorphTargetPipeline,
    MorphTargetEntry,
    CorrectiveShapeEntry,
    MorphBlendPresetEntry,
    AssetBundlePipeline,
    AssetBundleEntry,
    BundlePatchEntry,
    BundleManifestEntry,
)


# ---------------------------------------------------------------------------
# MorphTargetEntry
# ---------------------------------------------------------------------------

class TestMorphTargetEntry(unittest.TestCase):
    def test_morph_id(self):
        m = MorphTargetEntry(morph_id="morph_001", morph_name="Smile")
        self.assertEqual(m.morph_id, "morph_001")

    def test_morph_name(self):
        m = MorphTargetEntry(morph_id="morph_001", morph_name="Smile")
        self.assertEqual(m.morph_name, "Smile")

    def test_default_scope_character(self):
        m = MorphTargetEntry(morph_id="morph_001", morph_name="Smile")
        self.assertEqual(m.scope, "Character")

    def test_is_active_false(self):
        m = MorphTargetEntry(morph_id="morph_001", morph_name="Smile", default_weight=0.0)
        self.assertFalse(m.is_active)

    def test_is_active_true(self):
        m = MorphTargetEntry(morph_id="morph_001", morph_name="Smile", default_weight=0.5)
        self.assertTrue(m.is_active)

    def test_is_full_false(self):
        m = MorphTargetEntry(morph_id="morph_001", morph_name="Smile", default_weight=0.5, max_weight=1.0)
        self.assertFalse(m.is_full)

    def test_is_full_true(self):
        m = MorphTargetEntry(morph_id="morph_001", morph_name="Smile", default_weight=1.0, max_weight=1.0)
        self.assertTrue(m.is_full)

    def test_is_character_true(self):
        m = MorphTargetEntry(morph_id="morph_001", morph_name="Smile", scope="Character")
        self.assertTrue(m.is_character)

    def test_weight_range(self):
        m = MorphTargetEntry(morph_id="morph_001", morph_name="Smile", min_weight=0.0, max_weight=1.0)
        self.assertAlmostEqual(m.weight_range, 1.0)


# ---------------------------------------------------------------------------
# CorrectiveShapeEntry
# ---------------------------------------------------------------------------

class TestCorrectiveShapeEntry(unittest.TestCase):
    def test_corrective_id(self):
        c = CorrectiveShapeEntry(corrective_id="corr_001", morph_id="morph_001")
        self.assertEqual(c.corrective_id, "corr_001")

    def test_morph_id(self):
        c = CorrectiveShapeEntry(corrective_id="corr_001", morph_id="morph_001")
        self.assertEqual(c.morph_id, "morph_001")

    def test_has_trigger_false(self):
        c = CorrectiveShapeEntry(corrective_id="corr_001", morph_id="morph_001", trigger_expr="")
        self.assertFalse(c.has_trigger)

    def test_has_trigger_true(self):
        c = CorrectiveShapeEntry(corrective_id="corr_001", morph_id="morph_001", trigger_expr="weight > 0.5")
        self.assertTrue(c.has_trigger)

    def test_is_automatic_true(self):
        c = CorrectiveShapeEntry(corrective_id="corr_001", morph_id="morph_001", mode="Automatic")
        self.assertTrue(c.is_automatic)

    def test_is_automatic_false(self):
        c = CorrectiveShapeEntry(corrective_id="corr_001", morph_id="morph_001", mode="Manual")
        self.assertFalse(c.is_automatic)

    def test_is_active_true(self):
        c = CorrectiveShapeEntry(corrective_id="corr_001", morph_id="morph_001", enabled=True)
        self.assertTrue(c.is_active)

    def test_is_active_false(self):
        c = CorrectiveShapeEntry(corrective_id="corr_001", morph_id="morph_001", enabled=False)
        self.assertFalse(c.is_active)


# ---------------------------------------------------------------------------
# MorphBlendPresetEntry
# ---------------------------------------------------------------------------

class TestMorphBlendPresetEntry(unittest.TestCase):
    def test_preset_id(self):
        p = MorphBlendPresetEntry(preset_id="preset_001", preset_name="Happy")
        self.assertEqual(p.preset_id, "preset_001")

    def test_preset_name(self):
        p = MorphBlendPresetEntry(preset_id="preset_001", preset_name="Happy")
        self.assertEqual(p.preset_name, "Happy")

    def test_is_empty_true(self):
        p = MorphBlendPresetEntry(preset_id="preset_001", preset_name="Happy")
        self.assertTrue(p.is_empty)

    def test_is_empty_false(self):
        p = MorphBlendPresetEntry(preset_id="preset_001", preset_name="Happy", morph_ids=["morph_001"])
        self.assertFalse(p.is_empty)

    def test_morph_count(self):
        p = MorphBlendPresetEntry(preset_id="preset_001", preset_name="Happy", morph_ids=["m1", "m2"])
        self.assertEqual(p.morph_count, 2)

    def test_is_enabled_true(self):
        p = MorphBlendPresetEntry(preset_id="preset_001", preset_name="Happy", enabled=True)
        self.assertTrue(p.is_enabled)

    def test_is_additive_true(self):
        p = MorphBlendPresetEntry(preset_id="preset_001", preset_name="Happy", blend_mode="Additive")
        self.assertTrue(p.is_additive)

    def test_is_additive_false(self):
        p = MorphBlendPresetEntry(preset_id="preset_001", preset_name="Happy", blend_mode="Override")
        self.assertFalse(p.is_additive)


# ---------------------------------------------------------------------------
# MorphTargetPipeline
# ---------------------------------------------------------------------------

class TestMorphTargetPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = MorphTargetPipeline()
        self.morph = MorphTargetEntry(morph_id="morph_001", morph_name="Smile")

    def test_add_morph(self):
        self.assertTrue(self.pipeline.add_morph(self.morph))

    def test_remove_morph(self):
        self.pipeline.add_morph(self.morph)
        self.assertTrue(self.pipeline.remove_morph("morph_001"))

    def test_get_all_morphs(self):
        self.pipeline.add_morph(self.morph)
        self.assertEqual(len(self.pipeline.get_all_morphs()), 1)

    def test_add_corrective(self):
        self.pipeline.add_morph(self.morph)
        c = CorrectiveShapeEntry(corrective_id="corr_001", morph_id="morph_001")
        self.assertTrue(self.pipeline.add_corrective("morph_001", c))

    def test_remove_corrective(self):
        self.pipeline.add_morph(self.morph)
        c = CorrectiveShapeEntry(corrective_id="corr_001", morph_id="morph_001")
        self.pipeline.add_corrective("morph_001", c)
        self.assertTrue(self.pipeline.remove_corrective("morph_001", "corr_001"))

    def test_get_correctives_for_morph(self):
        self.pipeline.add_morph(self.morph)
        c = CorrectiveShapeEntry(corrective_id="corr_001", morph_id="morph_001")
        self.pipeline.add_corrective("morph_001", c)
        self.assertEqual(len(self.pipeline.get_correctives_for_morph("morph_001")), 1)

    def test_add_preset(self):
        p = MorphBlendPresetEntry(preset_id="preset_001", preset_name="Happy")
        self.assertTrue(self.pipeline.add_preset(p))

    def test_remove_preset(self):
        p = MorphBlendPresetEntry(preset_id="preset_001", preset_name="Happy")
        self.pipeline.add_preset(p)
        self.assertTrue(self.pipeline.remove_preset("preset_001"))

    def test_get_all_presets(self):
        p = MorphBlendPresetEntry(preset_id="preset_001", preset_name="Happy")
        self.pipeline.add_preset(p)
        self.assertEqual(len(self.pipeline.get_all_presets()), 1)

    def test_get_active_morphs(self):
        m2 = MorphTargetEntry(morph_id="morph_002", morph_name="Blink", default_weight=0.8)
        self.pipeline.add_morph(self.morph)
        self.pipeline.add_morph(m2)
        active = self.pipeline.get_active_morphs()
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].morph_id, "morph_002")

    def test_get_disabled_morphs(self):
        m_disabled = MorphTargetEntry(morph_id="morph_003", morph_name="Disabled", enabled=False)
        self.pipeline.add_morph(self.morph)
        self.pipeline.add_morph(m_disabled)
        disabled = self.pipeline.get_disabled_morphs()
        self.assertEqual(len(disabled), 1)

    def test_set_weight(self):
        self.pipeline.add_morph(self.morph)
        self.assertTrue(self.pipeline.set_weight("morph_001", 0.75))
        self.assertAlmostEqual(self.pipeline.get_morph("morph_001").default_weight, 0.75)

    def test_get_morphs_by_scope(self):
        self.pipeline.add_morph(self.morph)
        m_vehicle = MorphTargetEntry(morph_id="morph_004", morph_name="Dent", scope="Vehicle")
        self.pipeline.add_morph(m_vehicle)
        chars = self.pipeline.get_morphs_by_scope("Character")
        self.assertEqual(len(chars), 1)

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.morph))
        bad = MorphTargetEntry(morph_id="", morph_name="")
        self.assertFalse(self.pipeline.validate(bad))

    def test_morph_count(self):
        self.pipeline.add_morph(self.morph)
        self.assertEqual(self.pipeline.morph_count, 1)

    def test_is_empty(self):
        self.assertTrue(self.pipeline.is_empty)
        self.pipeline.add_morph(self.morph)
        self.assertFalse(self.pipeline.is_empty)

    def test_clear(self):
        self.pipeline.add_morph(self.morph)
        self.pipeline.clear()
        self.assertTrue(self.pipeline.is_empty)


# ---------------------------------------------------------------------------
# AssetBundleEntry
# ---------------------------------------------------------------------------

class TestAssetBundleEntry(unittest.TestCase):
    def test_bundle_id(self):
        b = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets")
        self.assertEqual(b.bundle_id, "bundle_001")

    def test_bundle_name(self):
        b = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets")
        self.assertEqual(b.bundle_name, "CoreAssets")

    def test_default_platform_pc(self):
        b = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets")
        self.assertEqual(b.platform, "PC")

    def test_is_ready_false(self):
        b = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets", state="Draft")
        self.assertFalse(b.is_ready)

    def test_is_ready_true(self):
        b = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets", state="Ready")
        self.assertTrue(b.is_ready)

    def test_is_shipping_false(self):
        b = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets", state="Draft")
        self.assertFalse(b.is_shipping)

    def test_is_shipping_true(self):
        b = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets", state="Shipping")
        self.assertTrue(b.is_shipping)

    def test_asset_count(self):
        b = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets", asset_ids=["a1", "a2"])
        self.assertEqual(b.asset_count, 2)

    def test_has_assets_false(self):
        b = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets")
        self.assertFalse(b.has_assets)

    def test_has_assets_true(self):
        b = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets", asset_ids=["a1"])
        self.assertTrue(b.has_assets)

    def test_is_compressed_true(self):
        b = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets", compression="LZ4")
        self.assertTrue(b.is_compressed)

    def test_is_compressed_false(self):
        b = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets", compression="None")
        self.assertFalse(b.is_compressed)


# ---------------------------------------------------------------------------
# BundlePatchEntry
# ---------------------------------------------------------------------------

class TestBundlePatchEntry(unittest.TestCase):
    def test_patch_id(self):
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001")
        self.assertEqual(p.patch_id, "patch_001")

    def test_bundle_id(self):
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001")
        self.assertEqual(p.bundle_id, "bundle_001")

    def test_is_validated_false(self):
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001", validated=False)
        self.assertFalse(p.is_validated)

    def test_is_validated_true(self):
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001", validated=True)
        self.assertTrue(p.is_validated)

    def test_is_incremental_true(self):
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001", strategy="Incremental")
        self.assertTrue(p.is_incremental)

    def test_is_incremental_false(self):
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001", strategy="Full")
        self.assertFalse(p.is_incremental)

    def test_has_versions_false(self):
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001")
        self.assertFalse(p.has_versions)

    def test_has_versions_true(self):
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001", base_version="1.0", target_version="1.1")
        self.assertTrue(p.has_versions)

    def test_size_kb(self):
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001", patch_size_bytes=2048)
        self.assertAlmostEqual(p.size_kb, 2.0)


# ---------------------------------------------------------------------------
# BundleManifestEntry
# ---------------------------------------------------------------------------

class TestBundleManifestEntry(unittest.TestCase):
    def test_manifest_id(self):
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001")
        self.assertEqual(m.manifest_id, "manifest_001")

    def test_bundle_id(self):
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001")
        self.assertEqual(m.bundle_id, "bundle_001")

    def test_is_ready_false(self):
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001", state="Draft")
        self.assertFalse(m.is_ready)

    def test_is_ready_true(self):
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001", state="Ready")
        self.assertTrue(m.is_ready)

    def test_is_draft_true(self):
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001", state="Draft")
        self.assertTrue(m.is_draft)

    def test_is_draft_false(self):
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001", state="Ready")
        self.assertFalse(m.is_draft)

    def test_has_path_false(self):
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001")
        self.assertFalse(m.has_path)

    def test_has_path_true(self):
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001", manifest_path="/out/manifest.json")
        self.assertTrue(m.has_path)

    def test_size_mb(self):
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001", total_size_bytes=1048576)
        self.assertAlmostEqual(m.size_mb, 1.0)


# ---------------------------------------------------------------------------
# AssetBundlePipeline
# ---------------------------------------------------------------------------

class TestAssetBundlePipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = AssetBundlePipeline()
        self.bundle = AssetBundleEntry(bundle_id="bundle_001", bundle_name="CoreAssets")

    def test_add_bundle(self):
        self.assertTrue(self.pipeline.add_bundle(self.bundle))

    def test_remove_bundle(self):
        self.pipeline.add_bundle(self.bundle)
        self.assertTrue(self.pipeline.remove_bundle("bundle_001"))

    def test_get_all_bundles(self):
        self.pipeline.add_bundle(self.bundle)
        self.assertEqual(len(self.pipeline.get_all_bundles()), 1)

    def test_add_patch(self):
        self.pipeline.add_bundle(self.bundle)
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001")
        self.assertTrue(self.pipeline.add_patch("bundle_001", p))

    def test_remove_patch(self):
        self.pipeline.add_bundle(self.bundle)
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001")
        self.pipeline.add_patch("bundle_001", p)
        self.assertTrue(self.pipeline.remove_patch("bundle_001", "patch_001"))

    def test_get_patches_for_bundle(self):
        self.pipeline.add_bundle(self.bundle)
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001")
        self.pipeline.add_patch("bundle_001", p)
        self.assertEqual(len(self.pipeline.get_patches_for_bundle("bundle_001")), 1)

    def test_add_manifest(self):
        self.pipeline.add_bundle(self.bundle)
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001")
        self.assertTrue(self.pipeline.add_manifest("bundle_001", m))

    def test_remove_manifest(self):
        self.pipeline.add_bundle(self.bundle)
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001")
        self.pipeline.add_manifest("bundle_001", m)
        self.assertTrue(self.pipeline.remove_manifest("bundle_001", "manifest_001"))

    def test_get_manifests_for_bundle(self):
        self.pipeline.add_bundle(self.bundle)
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001")
        self.pipeline.add_manifest("bundle_001", m)
        self.assertEqual(len(self.pipeline.get_manifests_for_bundle("bundle_001")), 1)

    def test_get_ready_bundles(self):
        ready = AssetBundleEntry(bundle_id="bundle_002", bundle_name="ReadyBundle", state="Ready")
        self.pipeline.add_bundle(self.bundle)
        self.pipeline.add_bundle(ready)
        self.assertEqual(len(self.pipeline.get_ready_bundles()), 1)

    def test_get_shipping_bundles(self):
        shipping = AssetBundleEntry(bundle_id="bundle_003", bundle_name="ShipBundle", state="Shipping")
        self.pipeline.add_bundle(self.bundle)
        self.pipeline.add_bundle(shipping)
        self.assertEqual(len(self.pipeline.get_shipping_bundles()), 1)

    def test_get_validated_patches(self):
        self.pipeline.add_bundle(self.bundle)
        p = BundlePatchEntry(patch_id="patch_001", bundle_id="bundle_001", validated=True)
        self.pipeline.add_patch("bundle_001", p)
        self.assertEqual(len(self.pipeline.get_validated_patches()), 1)

    def test_get_ready_manifests(self):
        self.pipeline.add_bundle(self.bundle)
        m = BundleManifestEntry(manifest_id="manifest_001", bundle_id="bundle_001", state="Ready")
        self.pipeline.add_manifest("bundle_001", m)
        self.assertEqual(len(self.pipeline.get_ready_manifests()), 1)

    def test_get_bundles_by_platform(self):
        mobile = AssetBundleEntry(bundle_id="bundle_004", bundle_name="MobileBundle", platform="Mobile")
        self.pipeline.add_bundle(self.bundle)
        self.pipeline.add_bundle(mobile)
        self.assertEqual(len(self.pipeline.get_bundles_by_platform("PC")), 1)

    def test_validate(self):
        self.assertTrue(self.pipeline.validate(self.bundle))
        bad = AssetBundleEntry(bundle_id="", bundle_name="")
        self.assertFalse(self.pipeline.validate(bad))

    def test_bundle_count(self):
        self.pipeline.add_bundle(self.bundle)
        self.assertEqual(self.pipeline.bundle_count, 1)

    def test_is_empty(self):
        self.assertTrue(self.pipeline.is_empty)
        self.pipeline.add_bundle(self.bundle)
        self.assertFalse(self.pipeline.is_empty)

    def test_clear(self):
        self.pipeline.add_bundle(self.bundle)
        self.pipeline.clear()
        self.assertTrue(self.pipeline.is_empty)


if __name__ == "__main__":
    unittest.main()
