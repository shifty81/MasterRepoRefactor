"""Phase 28D — Tests for VFXBodyRegistry.h and VFXBodyLoader."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    VFXBodyLoader,
    VFXBodyManifest,
    EmitterBoundsDef,
    SimulationSettingsDef,
)

VFX_REGISTRY_H = SCENE_DIR / "VFXBodyRegistry.h"


def _read_registry() -> str:
    return VFX_REGISTRY_H.read_text()


# ---------------------------------------------------------------------------
# VFXBodyRegistry.h
# ---------------------------------------------------------------------------

class TestVFXBodyRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(VFX_REGISTRY_H.exists())


class TestVFXBodyRegistryStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_registry())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_registry())

    def test_class_declaration(self):
        self.assertIn("VFXBodyRegistry", _read_registry())

    def test_vfx_body_state_enum(self):
        self.assertIn("VFXBodyState", _read_registry())

    def test_emitter_shape_enum(self):
        self.assertIn("EmitterShape", _read_registry())

    def test_simulation_space_enum(self):
        self.assertIn("SimulationSpace", _read_registry())

    def test_blend_mode_enum(self):
        self.assertIn("BlendMode", _read_registry())

    def test_vfx_layer_enum(self):
        self.assertIn("VFXLayer", _read_registry())

    def test_emitter_bounds_struct(self):
        self.assertIn("EmitterBounds", _read_registry())

    def test_simulation_settings_struct(self):
        self.assertIn("SimulationSettings", _read_registry())

    def test_render_settings_struct(self):
        self.assertIn("RenderSettings", _read_registry())

    def test_lod_settings_struct(self):
        self.assertIn("LODSettings", _read_registry())

    def test_vfx_body_record_struct(self):
        self.assertIn("VFXBodyRecord", _read_registry())

    def test_register_body(self):
        self.assertIn("RegisterBody", _read_registry())

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_registry())

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_registry())

    def test_set_body_position(self):
        self.assertIn("SetBodyPosition", _read_registry())

    def test_activate_body(self):
        self.assertIn("ActivateBody", _read_registry())

    def test_deactivate_body(self):
        self.assertIn("DeactivateBody", _read_registry())

    def test_play_body(self):
        self.assertIn("PlayBody", _read_registry())

    def test_get_all_body_ids(self):
        self.assertIn("GetAllBodyIds", _read_registry())

    def test_get_bodies_by_scene(self):
        self.assertIn("GetBodiesByScene", _read_registry())

    def test_get_bodies_by_layer(self):
        self.assertIn("GetBodiesByLayer", _read_registry())

    def test_clear_method(self):
        self.assertIn("Clear()", _read_registry())

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_registry())

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_registry())

    def test_lod_distances_method(self):
        self.assertIn("SetLODDistances", _read_registry())

    def test_set_spawn_rate(self):
        self.assertIn("SetSpawnRate", _read_registry())

    def test_functional_include(self):
        self.assertIn("<functional>", _read_registry())


# ---------------------------------------------------------------------------
# EmitterBoundsDef dataclass
# ---------------------------------------------------------------------------

class TestEmitterBoundsDefDataclass(unittest.TestCase):
    def test_default_shape(self):
        b = EmitterBoundsDef()
        self.assertEqual(b.shape, "Sphere")

    def test_default_radius(self):
        b = EmitterBoundsDef()
        self.assertAlmostEqual(b.radius, 1.0)

    def test_custom_shape(self):
        b = EmitterBoundsDef(shape="Box")
        self.assertEqual(b.shape, "Box")

    def test_is_bounded(self):
        b = EmitterBoundsDef(radius=2.0)
        self.assertTrue(b.is_bounded)

    def test_volume_box(self):
        b = EmitterBoundsDef(shape="Box", extent_x=2.0, extent_y=3.0, extent_z=4.0)
        self.assertAlmostEqual(b.volume, 24.0)


# ---------------------------------------------------------------------------
# SimulationSettingsDef dataclass
# ---------------------------------------------------------------------------

class TestSimulationSettingsDefDataclass(unittest.TestCase):
    def test_default_space(self):
        s = SimulationSettingsDef()
        self.assertEqual(s.simulation_space, "World")

    def test_default_max_particles(self):
        s = SimulationSettingsDef()
        self.assertEqual(s.max_particles, 1000)

    def test_is_gpu_simulated_false(self):
        s = SimulationSettingsDef()
        self.assertFalse(s.is_gpu_simulated)

    def test_is_gpu_simulated_true(self):
        s = SimulationSettingsDef(use_gpu_simulation=True)
        self.assertTrue(s.is_gpu_simulated)

    def test_effective_time_step_non_fixed(self):
        s = SimulationSettingsDef(fixed_time_step=False)
        self.assertEqual(s.effective_time_step, 0.0)


# ---------------------------------------------------------------------------
# VFXBodyManifest dataclass
# ---------------------------------------------------------------------------

class TestVFXBodyManifestDataclass(unittest.TestCase):
    def test_body_id(self):
        m = VFXBodyManifest(body_id="b001", name="Fire")
        self.assertEqual(m.body_id, "b001")

    def test_name(self):
        m = VFXBodyManifest(body_id="b001", name="Fire")
        self.assertEqual(m.name, "Fire")

    def test_default_emitter_type(self):
        m = VFXBodyManifest(body_id="b001", name="Fire")
        self.assertEqual(m.emitter_type, "Point")

    def test_default_body_state(self):
        m = VFXBodyManifest(body_id="b001", name="Fire")
        self.assertEqual(m.body_state, "Inactive")

    def test_is_active_false(self):
        m = VFXBodyManifest(body_id="b001", name="Fire")
        self.assertFalse(m.is_active)

    def test_position_tuple(self):
        m = VFXBodyManifest(body_id="b001", name="Fire", pos_x=1.0, pos_y=2.0, pos_z=3.0)
        self.assertEqual(m.position, (1.0, 2.0, 3.0))

    def test_is_looping(self):
        m = VFXBodyManifest(body_id="b001", name="Fire", loop=True)
        self.assertTrue(m.is_looping)


# ---------------------------------------------------------------------------
# VFXBodyLoader
# ---------------------------------------------------------------------------

class TestVFXBodyLoaderBasic(unittest.TestCase):
    def setUp(self):
        self.loader = VFXBodyLoader()

    def test_load_manifest(self):
        m = self.loader.load_manifest("b001", "Fire")
        self.assertIsNotNone(m)
        self.assertEqual(m.name, "Fire")

    def test_count_empty(self):
        self.assertEqual(self.loader.count(), 0)

    def test_count_after_load(self):
        self.loader.load_manifest("b001", "Fire")
        self.loader.load_manifest("b002", "Smoke")
        self.assertEqual(self.loader.count(), 2)

    def test_list_manifests(self):
        self.loader.load_manifest("b001", "Fire")
        ids = self.loader.list_manifests()
        self.assertIn("b001", ids)

    def test_get_manifest(self):
        self.loader.load_manifest("b001", "Fire")
        m = self.loader.get_manifest("b001")
        self.assertIsNotNone(m)

    def test_get_manifest_missing(self):
        self.assertIsNone(self.loader.get_manifest("missing"))

    def test_remove_manifest(self):
        self.loader.load_manifest("b001", "Fire")
        result = self.loader.remove_manifest("b001")
        self.assertTrue(result)
        self.assertEqual(self.loader.count(), 0)

    def test_remove_manifest_missing(self):
        self.assertFalse(self.loader.remove_manifest("missing"))


class TestVFXBodyLoaderActivation(unittest.TestCase):
    def setUp(self):
        self.loader = VFXBodyLoader()
        self.loader.load_manifest("b001", "Fire")

    def test_activate(self):
        result = self.loader.activate("b001")
        self.assertTrue(result)
        self.assertTrue(self.loader.is_active("b001"))

    def test_deactivate(self):
        self.loader.activate("b001")
        result = self.loader.deactivate("b001")
        self.assertTrue(result)
        self.assertFalse(self.loader.is_active("b001"))

    def test_play(self):
        result = self.loader.play("b001")
        self.assertTrue(result)
        self.assertTrue(self.loader.is_playing("b001"))

    def test_stop(self):
        self.loader.play("b001")
        result = self.loader.stop("b001")
        self.assertTrue(result)
        self.assertFalse(self.loader.is_playing("b001"))

    def test_activate_unknown(self):
        self.assertFalse(self.loader.activate("ghost"))

    def test_get_active_ids(self):
        self.loader.activate("b001")
        self.assertIn("b001", self.loader.get_active_ids())

    def test_get_playing_ids(self):
        self.loader.play("b001")
        self.assertIn("b001", self.loader.get_playing_ids())


class TestVFXBodyLoaderFilters(unittest.TestCase):
    def setUp(self):
        self.loader = VFXBodyLoader()
        self.loader.load_manifest("b001", "Fire", scene_id="scene_a", vfx_layer="World")
        self.loader.load_manifest("b002", "Smoke", scene_id="scene_b", vfx_layer="UI")
        self.loader.load_manifest("b003", "Sparks", scene_id="scene_a", emitter_type="Sphere",
                                   vfx_layer="World")

    def test_get_bodies_by_scene(self):
        ids = self.loader.get_bodies_by_scene("scene_a")
        self.assertIn("b001", ids)
        self.assertIn("b003", ids)
        self.assertNotIn("b002", ids)

    def test_get_bodies_by_layer(self):
        ids = self.loader.get_bodies_by_layer("UI")
        self.assertIn("b002", ids)

    def test_get_bodies_by_type(self):
        ids = self.loader.get_bodies_by_type("Sphere")
        self.assertIn("b003", ids)


class TestVFXBodyLoaderFromDict(unittest.TestCase):
    def setUp(self):
        self.loader = VFXBodyLoader()

    def test_load_from_dict(self):
        data = {
            "body_id": "b_dict",
            "name": "DictFire",
            "emitter_type": "Cone",
            "scene_id": "s001",
            "spawn_rate": 25.0,
        }
        m = self.loader.load_manifest_from_dict(data)
        self.assertIsNotNone(m)
        self.assertEqual(m.emitter_type, "Cone")
        self.assertAlmostEqual(m.spawn_rate, 25.0)

    def test_load_from_dict_missing_key(self):
        result = self.loader.load_manifest_from_dict({"name": "NoId"})
        self.assertIsNone(result)


class TestVFXBodyLoaderExport(unittest.TestCase):
    def setUp(self):
        self.loader = VFXBodyLoader()
        self.loader.load_manifest("b001", "Fire")
        self.loader.load_manifest("b002", "Smoke")

    def test_export_registry_json(self):
        out = str(REPO_ROOT / "AtlasAI" / "Tests" / "_test_vfx_registry_p28d.json")
        result = self.loader.export_registry_json(out)
        self.assertTrue(result)
        data = json.loads(Path(out).read_text())
        self.assertIn("bodies", data)
        self.assertEqual(data["vfx_body_count"], 2)
        Path(out).unlink(missing_ok=True)

    def test_clear(self):
        self.loader.clear()
        self.assertEqual(self.loader.count(), 0)


if __name__ == "__main__":
    unittest.main()
