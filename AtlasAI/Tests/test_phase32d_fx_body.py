"""Phase 32D — Tests for FXBodyRegistry.h and FXBodyLoader."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    FXBodyLoader,
    FXBodyManifest,
    FXEmitSettingsDef,
    FXSimSettingsDef,
)

FX_REGISTRY_H = SCENE_DIR / "FXBodyRegistry.h"


def _read_registry() -> str:
    return FX_REGISTRY_H.read_text()


# ---------------------------------------------------------------------------
# FXBodyRegistry.h
# ---------------------------------------------------------------------------

class TestFXBodyRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(FX_REGISTRY_H.exists())


class TestFXBodyRegistryStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_registry())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_registry())

    def test_class_declaration(self):
        self.assertIn("FXBodyRegistry", _read_registry())

    def test_fx_body_state_enum(self):
        self.assertIn("FXBodyState", _read_registry())

    def test_fx_body_type_enum(self):
        self.assertIn("FXBodyType", _read_registry())

    def test_fx_mobility_enum(self):
        self.assertIn("FXMobility", _read_registry())

    def test_lod_reduction_mode_enum(self):
        self.assertIn("LODReductionMode", _read_registry())

    def test_simulation_target_enum(self):
        self.assertIn("SimulationTarget", _read_registry())

    def test_fx_emit_settings_struct(self):
        self.assertIn("FXEmitSettings", _read_registry())

    def test_fx_sim_settings_struct(self):
        self.assertIn("FXSimSettings", _read_registry())

    def test_fx_body_record_struct(self):
        self.assertIn("FXBodyRecord", _read_registry())

    def test_register_body(self):
        self.assertIn("RegisterBody", _read_registry())

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_registry())

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_registry())

    def test_set_body_position(self):
        self.assertIn("SetBodyPosition", _read_registry())

    def test_set_fx_type(self):
        self.assertIn("SetFXType", _read_registry())

    def test_set_fx_mobility(self):
        self.assertIn("SetFXMobility", _read_registry())

    def test_set_emit_settings(self):
        self.assertIn("SetEmitSettings", _read_registry())

    def test_set_sim_settings(self):
        self.assertIn("SetSimSettings", _read_registry())

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

    def test_get_playing_bodies(self):
        self.assertIn("GetPlayingBodies", _read_registry())

    def test_clear_method(self):
        self.assertIn("Clear", _read_registry())

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_registry())

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_registry())


# ---------------------------------------------------------------------------
# FXEmitSettingsDef
# ---------------------------------------------------------------------------

class TestFXEmitSettingsDef(unittest.TestCase):
    def test_default_spawn_rate(self):
        e = FXEmitSettingsDef()
        self.assertAlmostEqual(e.spawn_rate, 100.0)

    def test_default_lifetime(self):
        e = FXEmitSettingsDef()
        self.assertAlmostEqual(e.lifetime, 2.0)

    def test_has_burst_false(self):
        e = FXEmitSettingsDef()
        self.assertFalse(e.has_burst)

    def test_is_fading_true(self):
        e = FXEmitSettingsDef(start_size=10.0, end_size=0.0)
        self.assertTrue(e.is_fading)


# ---------------------------------------------------------------------------
# FXSimSettingsDef
# ---------------------------------------------------------------------------

class TestFXSimSettingsDef(unittest.TestCase):
    def test_default_target(self):
        s = FXSimSettingsDef()
        self.assertEqual(s.target, "GPU")

    def test_default_max_particles(self):
        s = FXSimSettingsDef()
        self.assertEqual(s.max_particles, 1000)

    def test_is_gpu_true(self):
        s = FXSimSettingsDef(target="GPU")
        self.assertTrue(s.is_gpu)

    def test_has_warmup_false(self):
        s = FXSimSettingsDef()
        self.assertFalse(s.has_warmup)


# ---------------------------------------------------------------------------
# FXBodyManifest
# ---------------------------------------------------------------------------

class TestFXBodyManifest(unittest.TestCase):
    def test_body_id(self):
        m = FXBodyManifest(body_id="fx001", name="Fire Effect")
        self.assertEqual(m.body_id, "fx001")

    def test_name_field(self):
        m = FXBodyManifest(body_id="fx001", name="Fire Effect")
        self.assertEqual(m.name, "Fire Effect")

    def test_default_fx_type(self):
        m = FXBodyManifest(body_id="fx001", name="Fire Effect")
        self.assertEqual(m.fx_type, "Particle")

    def test_default_mobility(self):
        m = FXBodyManifest(body_id="fx001", name="Fire Effect")
        self.assertEqual(m.mobility, "Movable")

    def test_default_range(self):
        m = FXBodyManifest(body_id="fx001", name="Fire Effect")
        self.assertAlmostEqual(m.range, 5000.0)

    def test_is_visible_true(self):
        m = FXBodyManifest(body_id="fx001", name="Fire Effect", visible=True, enabled=True)
        self.assertTrue(m.is_visible)

    def test_is_movable_true(self):
        m = FXBodyManifest(body_id="fx001", name="Fire Effect", mobility="Movable")
        self.assertTrue(m.is_movable)

    def test_is_looping_true(self):
        m = FXBodyManifest(body_id="fx001", name="Fire Effect", looping=True)
        self.assertTrue(m.is_looping)


# ---------------------------------------------------------------------------
# FXBodyLoader
# ---------------------------------------------------------------------------

class TestFXBodyLoader(unittest.TestCase):
    def _loader(self):
        return FXBodyLoader()

    def test_load_manifest_returns_manifest(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "fx001", "name": "Fire Effect"})
        self.assertIsInstance(m, FXBodyManifest)

    def test_load_manifest_id(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "fx001", "name": "Fire Effect"})
        self.assertEqual(m.body_id, "fx001")

    def test_load_manifest_name(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "fx001", "name": "Fire Effect"})
        self.assertEqual(m.name, "Fire Effect")

    def test_load_batch(self):
        loader = self._loader()
        batch = loader.load_batch([
            {"body_id": "fx001", "name": "Fire Effect"},
            {"body_id": "fx002", "name": "Smoke Effect"},
        ])
        self.assertEqual(len(batch), 2)

    def test_validate_valid_manifest(self):
        loader = self._loader()
        m = FXBodyManifest(body_id="fx001", name="Fire Effect")
        self.assertTrue(loader.validate(m))

    def test_validate_empty_name_fails(self):
        loader = self._loader()
        m = FXBodyManifest(body_id="fx001", name="")
        self.assertFalse(loader.validate(m))

    def test_loaded_count_zero(self):
        loader = self._loader()
        self.assertEqual(loader.loaded_count, 0)

    def test_clear_resets(self):
        loader = self._loader()
        loader.load_manifest({"body_id": "fx001", "name": "Fire Effect"})
        loader.clear()
        self.assertEqual(loader.loaded_count, 0)

    def test_save_manifest_creates_file(self):
        loader = self._loader()
        m = FXBodyManifest(body_id="fx001", name="Fire Effect")
        save_path = REPO_ROOT / "AtlasAI" / "Tests" / "_test_fx_save_32d.json"
        try:
            loader.save_manifest(m, save_path)
            self.assertTrue(save_path.exists())
        finally:
            if save_path.exists():
                save_path.unlink()


if __name__ == "__main__":
    unittest.main()
