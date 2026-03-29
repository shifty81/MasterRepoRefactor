"""Phase 31D — Tests for LightBodyRegistry.h and LightBodyLoader."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    LightBodyLoader,
    LightBodyManifest,
    LightColorDef,
    ShadowSettingsDef,
)

LIGHT_REGISTRY_H = SCENE_DIR / "LightBodyRegistry.h"


def _read_registry() -> str:
    return LIGHT_REGISTRY_H.read_text()


# ---------------------------------------------------------------------------
# LightBodyRegistry.h
# ---------------------------------------------------------------------------

class TestLightBodyRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(LIGHT_REGISTRY_H.exists())


class TestLightBodyRegistryStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_registry())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_registry())

    def test_class_declaration(self):
        self.assertIn("LightBodyRegistry", _read_registry())

    def test_light_body_state_enum(self):
        self.assertIn("LightBodyState", _read_registry())

    def test_light_type_enum(self):
        self.assertIn("LightType", _read_registry())

    def test_light_mobility_enum(self):
        self.assertIn("LightMobility", _read_registry())

    def test_shadow_resolution_enum(self):
        self.assertIn("ShadowResolution", _read_registry())

    def test_attenuation_shape_enum(self):
        self.assertIn("AttenuationShape", _read_registry())

    def test_light_color_def_struct(self):
        self.assertIn("LightColorDef", _read_registry())

    def test_shadow_settings_struct(self):
        self.assertIn("ShadowSettings", _read_registry())

    def test_atmospheric_settings_struct(self):
        self.assertIn("AtmosphericSettings", _read_registry())

    def test_light_body_record_struct(self):
        self.assertIn("LightBodyRecord", _read_registry())

    def test_register_body(self):
        self.assertIn("RegisterBody", _read_registry())

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_registry())

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_registry())

    def test_set_body_position(self):
        self.assertIn("SetBodyPosition", _read_registry())

    def test_set_light_type(self):
        self.assertIn("SetLightType", _read_registry())

    def test_set_light_color(self):
        self.assertIn("SetLightColor", _read_registry())

    def test_set_light_intensity(self):
        self.assertIn("SetLightIntensity", _read_registry())

    def test_set_shadow_settings(self):
        self.assertIn("SetShadowSettings", _read_registry())

    def test_get_all_body_ids(self):
        self.assertIn("GetAllBodyIds", _read_registry())

    def test_get_bodies_by_type(self):
        self.assertIn("GetBodiesByType", _read_registry())

    def test_get_bodies_by_mobility(self):
        self.assertIn("GetBodiesByMobility", _read_registry())

    def test_get_bodies_by_state(self):
        self.assertIn("GetBodiesByState", _read_registry())

    def test_get_active_bodies(self):
        self.assertIn("GetActiveBodies", _read_registry())

    def test_get_shadow_casting_bodies(self):
        self.assertIn("GetShadowCastingBodies", _read_registry())

    def test_clear_method(self):
        self.assertIn("Clear", _read_registry())

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_registry())

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_registry())


# ---------------------------------------------------------------------------
# LightColorDef
# ---------------------------------------------------------------------------

class TestLightColorDef(unittest.TestCase):
    def test_default_r(self):
        c = LightColorDef()
        self.assertAlmostEqual(c.r, 1.0)

    def test_default_g(self):
        c = LightColorDef()
        self.assertAlmostEqual(c.g, 1.0)

    def test_default_b(self):
        c = LightColorDef()
        self.assertAlmostEqual(c.b, 1.0)

    def test_default_temperature(self):
        c = LightColorDef()
        self.assertAlmostEqual(c.temperature, 6500.0)

    def test_is_warm_false(self):
        c = LightColorDef(temperature=6500.0)
        self.assertFalse(c.is_warm)

    def test_is_daylight_true(self):
        c = LightColorDef(temperature=6500.0)
        self.assertTrue(c.is_daylight)


# ---------------------------------------------------------------------------
# ShadowSettingsDef
# ---------------------------------------------------------------------------

class TestShadowSettingsDef(unittest.TestCase):
    def test_default_resolution(self):
        s = ShadowSettingsDef()
        self.assertEqual(s.resolution, "Medium")

    def test_default_bias(self):
        s = ShadowSettingsDef()
        self.assertAlmostEqual(s.bias, 0.01)

    def test_default_cascades(self):
        s = ShadowSettingsDef()
        self.assertEqual(s.cascades, 4)

    def test_has_contact_shadow_false(self):
        s = ShadowSettingsDef()
        self.assertFalse(s.has_contact_shadow)

    def test_is_high_res_false(self):
        s = ShadowSettingsDef(resolution="Medium")
        self.assertFalse(s.is_high_res)


# ---------------------------------------------------------------------------
# LightBodyManifest
# ---------------------------------------------------------------------------

class TestLightBodyManifest(unittest.TestCase):
    def test_body_id(self):
        m = LightBodyManifest(body_id="lb001", name="Sun Light")
        self.assertEqual(m.body_id, "lb001")

    def test_name_field(self):
        m = LightBodyManifest(body_id="lb001", name="Sun Light")
        self.assertEqual(m.name, "Sun Light")

    def test_default_light_type(self):
        m = LightBodyManifest(body_id="lb001", name="Sun Light")
        self.assertEqual(m.light_type, "Point")

    def test_default_mobility(self):
        m = LightBodyManifest(body_id="lb001", name="Sun Light")
        self.assertEqual(m.mobility, "Stationary")

    def test_default_range(self):
        m = LightBodyManifest(body_id="lb001", name="Sun Light")
        self.assertAlmostEqual(m.range, 1000.0)

    def test_default_visible(self):
        m = LightBodyManifest(body_id="lb001", name="Sun Light")
        self.assertTrue(m.visible)

    def test_is_visible_true(self):
        m = LightBodyManifest(body_id="lb001", name="Sun Light", visible=True, enabled=True)
        self.assertTrue(m.is_visible)

    def test_is_static_false(self):
        m = LightBodyManifest(body_id="lb001", name="Sun Light", mobility="Stationary")
        self.assertFalse(m.is_static)

    def test_is_shadow_caster_true(self):
        m = LightBodyManifest(body_id="lb001", name="Sun Light", cast_shadow=True)
        self.assertTrue(m.is_shadow_caster)


# ---------------------------------------------------------------------------
# LightBodyLoader
# ---------------------------------------------------------------------------

class TestLightBodyLoader(unittest.TestCase):
    def _loader(self):
        return LightBodyLoader()

    def test_load_manifest_returns_manifest(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "lb001", "name": "Key Light"})
        self.assertIsInstance(m, LightBodyManifest)

    def test_load_manifest_id(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "lb001", "name": "Key Light"})
        self.assertEqual(m.body_id, "lb001")

    def test_load_manifest_name(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "lb001", "name": "Key Light"})
        self.assertEqual(m.name, "Key Light")

    def test_load_batch(self):
        loader = self._loader()
        batch = loader.load_batch([
            {"body_id": "lb001", "name": "Key Light"},
            {"body_id": "lb002", "name": "Fill Light"},
        ])
        self.assertEqual(len(batch), 2)

    def test_validate_valid_manifest(self):
        loader = self._loader()
        m = LightBodyManifest(body_id="lb001", name="Key Light")
        self.assertTrue(loader.validate(m))

    def test_validate_empty_name_fails(self):
        loader = self._loader()
        m = LightBodyManifest(body_id="lb001", name="")
        self.assertFalse(loader.validate(m))

    def test_loaded_count_zero(self):
        loader = self._loader()
        self.assertEqual(loader.loaded_count, 0)

    def test_clear_resets(self):
        loader = self._loader()
        loader.load_manifest({"body_id": "lb001", "name": "Key Light"})
        loader.clear()
        self.assertEqual(loader.loaded_count, 0)

    def test_save_manifest_creates_file(self):
        loader = self._loader()
        m = LightBodyManifest(body_id="lb001", name="Key Light")
        save_path = REPO_ROOT / "AtlasAI" / "Tests" / "_test_lb_save_31d.json"
        try:
            loader.save_manifest(m, save_path)
            self.assertTrue(save_path.exists())
        finally:
            if save_path.exists():
                save_path.unlink()


if __name__ == "__main__":
    unittest.main()
