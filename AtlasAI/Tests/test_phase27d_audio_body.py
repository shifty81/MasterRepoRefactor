"""Phase 27D — Tests for AudioBodyRegistry.h and AudioBodyLoader."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    AudioBodyLoader,
    AudioBodyManifest,
    AttenuationCurveDef,
    ReverbZoneDef,
)

TMP_DIR = Path("/tmp/test_phase27d")
TMP_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# AudioBodyRegistry.h
# ---------------------------------------------------------------------------

def _read_registry() -> str:
    return (SCENE_DIR / "AudioBodyRegistry.h").read_text()


class TestAudioBodyRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "AudioBodyRegistry.h").exists())


class TestAudioBodyRegistryStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_registry())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_registry())

    def test_class_declaration(self):
        self.assertIn("AudioBodyRegistry", _read_registry())

    def test_audio_body_state_enum(self):
        self.assertIn("AudioBodyState", _read_registry())

    def test_audio_source_type_enum(self):
        self.assertIn("AudioSourceType", _read_registry())

    def test_attenuation_model_enum(self):
        self.assertIn("AttenuationModel", _read_registry())

    def test_occlusion_type_enum(self):
        self.assertIn("OcclusionType", _read_registry())

    def test_audio_layer_enum(self):
        self.assertIn("AudioLayer", _read_registry())

    def test_attenuation_curve_struct(self):
        self.assertIn("AttenuationCurve", _read_registry())

    def test_occlusion_settings_struct(self):
        self.assertIn("OcclusionSettings", _read_registry())

    def test_doppler_settings_struct(self):
        self.assertIn("DopplerSettings", _read_registry())

    def test_audio_body_record_struct(self):
        self.assertIn("AudioBodyRecord", _read_registry())

    def test_reverb_zone_record_struct(self):
        self.assertIn("ReverbZoneRecord", _read_registry())


class TestAudioBodyRegistryAPI(unittest.TestCase):
    def test_register_body(self):
        self.assertIn("RegisterBody", _read_registry())

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_registry())

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_registry())

    def test_set_body_volume(self):
        self.assertIn("SetBodyVolume", _read_registry())

    def test_set_body_position(self):
        self.assertIn("SetBodyPosition", _read_registry())

    def test_set_attenuation_model(self):
        self.assertIn("SetAttenuationModel", _read_registry())

    def test_set_attenuation_range(self):
        self.assertIn("SetAttenuationRange", _read_registry())

    def test_set_occlusion_enabled(self):
        self.assertIn("SetOcclusionEnabled", _read_registry())

    def test_set_doppler_enabled(self):
        self.assertIn("SetDopplerEnabled", _read_registry())

    def test_get_bodies_by_scene(self):
        self.assertIn("GetBodiesByScene", _read_registry())

    def test_get_bodies_by_layer(self):
        self.assertIn("GetBodiesByLayer", _read_registry())

    def test_activate_body(self):
        self.assertIn("ActivateBody", _read_registry())

    def test_deactivate_body(self):
        self.assertIn("DeactivateBody", _read_registry())

    def test_play_body(self):
        self.assertIn("PlayBody", _read_registry())

    def test_pause_body(self):
        self.assertIn("PauseBody", _read_registry())

    def test_stop_body(self):
        self.assertIn("StopBody", _read_registry())

    def test_activate_always_play(self):
        self.assertIn("ActivateAlwaysPlay", _read_registry())

    def test_register_reverb_zone(self):
        self.assertIn("RegisterReverbZone", _read_registry())

    def test_get_reverb_zones_in_range(self):
        self.assertIn("GetReverbZonesInRange", _read_registry())

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_registry())

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_registry())


# ---------------------------------------------------------------------------
# AttenuationCurveDef dataclass
# ---------------------------------------------------------------------------

class TestAttenuationCurveDefDataclass(unittest.TestCase):
    def test_default_model(self):
        a = AttenuationCurveDef()
        self.assertEqual(a.model, "InverseDistance")

    def test_default_min_distance(self):
        a = AttenuationCurveDef()
        self.assertAlmostEqual(a.min_distance, 1.0)

    def test_distance_range(self):
        a = AttenuationCurveDef(min_distance=5.0, max_distance=30.0)
        self.assertAlmostEqual(a.distance_range, 25.0)

    def test_is_attenuated_true(self):
        a = AttenuationCurveDef(model="InverseDistance")
        self.assertTrue(a.is_attenuated)

    def test_is_attenuated_false_for_none(self):
        a = AttenuationCurveDef(model="None")
        self.assertFalse(a.is_attenuated)


# ---------------------------------------------------------------------------
# ReverbZoneDef dataclass
# ---------------------------------------------------------------------------

class TestReverbZoneDefDataclass(unittest.TestCase):
    def test_zone_id_field(self):
        z = ReverbZoneDef(zone_id="z001", name="Cave")
        self.assertEqual(z.zone_id, "z001")

    def test_name_field(self):
        z = ReverbZoneDef(zone_id="z001", name="Cave")
        self.assertEqual(z.name, "Cave")

    def test_position_property(self):
        z = ReverbZoneDef(zone_id="z001", name="Cave",
                           pos_x=1.0, pos_y=2.0, pos_z=3.0)
        self.assertEqual(z.position, (1.0, 2.0, 3.0))

    def test_contains_point_inside(self):
        z = ReverbZoneDef(zone_id="z001", name="Cave",
                           pos_x=0.0, pos_y=0.0, pos_z=0.0, radius=10.0)
        self.assertTrue(z.contains_point(1.0, 0.0, 0.0))

    def test_contains_point_outside(self):
        z = ReverbZoneDef(zone_id="z001", name="Cave",
                           pos_x=0.0, pos_y=0.0, pos_z=0.0, radius=5.0)
        self.assertFalse(z.contains_point(10.0, 0.0, 0.0))

    def test_default_preset_name(self):
        z = ReverbZoneDef(zone_id="z001", name="Cave")
        self.assertEqual(z.preset_name, "Generic")


# ---------------------------------------------------------------------------
# AudioBodyManifest dataclass
# ---------------------------------------------------------------------------

class TestAudioBodyManifestDataclass(unittest.TestCase):
    def test_body_id_field(self):
        m = AudioBodyManifest("b001", "Footstep")
        self.assertEqual(m.body_id, "b001")

    def test_name_field(self):
        m = AudioBodyManifest("b001", "Footstep")
        self.assertEqual(m.name, "Footstep")

    def test_default_source_type(self):
        m = AudioBodyManifest("b001", "Footstep")
        self.assertEqual(m.source_type, "Point")

    def test_default_is_active_false(self):
        m = AudioBodyManifest("b001", "Footstep")
        self.assertFalse(m.is_active)

    def test_default_is_playing_false(self):
        m = AudioBodyManifest("b001", "Footstep")
        self.assertFalse(m.is_playing)

    def test_is_spatialized_true(self):
        m = AudioBodyManifest("b001", "Footstep", spatialize=True)
        self.assertTrue(m.is_spatialized)

    def test_position_property(self):
        m = AudioBodyManifest("b001", "Footstep",
                               pos_x=1.0, pos_y=2.0, pos_z=3.0)
        self.assertEqual(m.position, (1.0, 2.0, 3.0))


# ---------------------------------------------------------------------------
# AudioBodyLoader — registration
# ---------------------------------------------------------------------------

class TestAudioBodyLoaderRegistration(unittest.TestCase):
    def setUp(self):
        self.loader = AudioBodyLoader()

    def test_register_returns_manifest(self):
        m = self.loader.register("b001", "Footstep")
        self.assertIsInstance(m, AudioBodyManifest)

    def test_register_name(self):
        m = self.loader.register("b001", "Footstep")
        self.assertEqual(m.name, "Footstep")

    def test_registered_count(self):
        self.loader.register("b001", "A")
        self.loader.register("b002", "B")
        self.assertEqual(self.loader.get_registered_count(), 2)

    def test_get_manifest_by_id(self):
        self.loader.register("b001", "Footstep")
        m = self.loader.get_manifest("b001")
        self.assertIsNotNone(m)

    def test_get_manifest_missing_returns_none(self):
        self.assertIsNone(self.loader.get_manifest("ghost"))

    def test_get_all_body_ids(self):
        self.loader.register("b001", "A")
        self.assertIn("b001", self.loader.get_all_body_ids())

    def test_unregister(self):
        self.loader.register("b001", "A")
        self.assertTrue(self.loader.unregister("b001"))
        self.assertEqual(self.loader.get_registered_count(), 0)

    def test_unregister_missing_returns_false(self):
        self.assertFalse(self.loader.unregister("ghost"))

    def test_get_bodies_by_scene(self):
        self.loader.register("b001", "A", scene_id="scA")
        self.loader.register("b002", "B", scene_id="scB")
        ids = self.loader.get_bodies_by_scene("scA")
        self.assertIn("b001", ids)
        self.assertEqual(len(ids), 1)

    def test_get_bodies_by_layer(self):
        self.loader.register("b001", "A", audio_layer="SFX")
        self.loader.register("b002", "B", audio_layer="Music")
        ids = self.loader.get_bodies_by_layer("SFX")
        self.assertIn("b001", ids)
        self.assertEqual(len(ids), 1)

    def test_get_bodies_by_type(self):
        self.loader.register("b001", "A", source_type="Point")
        self.loader.register("b002", "B", source_type="Ambient")
        ids = self.loader.get_bodies_by_type("Ambient")
        self.assertIn("b002", ids)
        self.assertEqual(len(ids), 1)

    def test_register_from_dict(self):
        data = {"body_id": "b001", "name": "Footstep", "source_type": "Point"}
        m = self.loader.register_from_dict(data)
        self.assertIsNotNone(m)
        self.assertEqual(m.body_id, "b001")

    def test_register_from_dict_with_attenuation(self):
        data = {
            "body_id": "b001",
            "name": "Footstep",
            "attenuation": {"model": "Linear", "min_distance": 2.0,
                             "max_distance": 30.0},
        }
        m = self.loader.register_from_dict(data)
        self.assertIsNotNone(m)
        self.assertEqual(m.attenuation.model, "Linear")

    def test_register_from_dict_missing_key_returns_none(self):
        self.assertIsNone(self.loader.register_from_dict({"name": "oops"}))

    def test_clear(self):
        self.loader.register("b001", "A")
        self.loader.clear()
        self.assertEqual(self.loader.get_registered_count(), 0)


# ---------------------------------------------------------------------------
# AudioBodyLoader — activation and playback
# ---------------------------------------------------------------------------

class TestAudioBodyLoaderActivation(unittest.TestCase):
    def setUp(self):
        self.loader = AudioBodyLoader()
        self.loader.register("b001", "Footstep", scene_id="s1",
                               always_play=False)
        self.loader.register("b002", "Ambient", scene_id="s1",
                               always_play=True, audio_layer="Ambient")
        self.loader.register("b003", "Music", scene_id="s2",
                               audio_layer="Music")

    def test_activate(self):
        self.assertTrue(self.loader.activate("b001"))
        self.assertTrue(self.loader.is_active("b001"))

    def test_activate_unknown_returns_false(self):
        self.assertFalse(self.loader.activate("ghost"))

    def test_deactivate(self):
        self.loader.activate("b001")
        self.assertTrue(self.loader.deactivate("b001"))
        self.assertFalse(self.loader.is_active("b001"))

    def test_deactivate_not_active_returns_false(self):
        self.assertFalse(self.loader.deactivate("b001"))

    def test_play(self):
        self.assertTrue(self.loader.play("b001"))
        self.assertTrue(self.loader.is_playing("b001"))

    def test_pause(self):
        self.loader.play("b001")
        self.assertTrue(self.loader.pause("b001"))
        self.assertFalse(self.loader.is_playing("b001"))

    def test_pause_not_playing_returns_false(self):
        self.assertFalse(self.loader.pause("b001"))

    def test_stop(self):
        self.loader.play("b001")
        self.assertTrue(self.loader.stop("b001"))
        self.assertFalse(self.loader.is_playing("b001"))

    def test_stop_not_playing_returns_false(self):
        self.assertFalse(self.loader.stop("b001"))

    def test_get_active_count(self):
        self.loader.activate("b001")
        self.assertEqual(self.loader.get_active_count(), 1)

    def test_get_playing_count(self):
        self.loader.play("b001")
        self.assertEqual(self.loader.get_playing_count(), 1)

    def test_activate_all_in_scene(self):
        count = self.loader.activate_all_in_scene("s1")
        self.assertEqual(count, 2)

    def test_deactivate_all_in_scene(self):
        self.loader.activate_all_in_scene("s1")
        deactivated = self.loader.deactivate_all_in_scene("s1")
        self.assertEqual(deactivated, 2)

    def test_activate_always_play(self):
        count = self.loader.activate_always_play()
        self.assertEqual(count, 1)
        self.assertTrue(self.loader.is_active("b002"))

    def test_body_state_active_after_activate(self):
        self.loader.activate("b001")
        m = self.loader.get_manifest("b001")
        self.assertEqual(m.body_state, "Active")

    def test_body_state_playing_after_play(self):
        self.loader.play("b001")
        m = self.loader.get_manifest("b001")
        self.assertEqual(m.body_state, "Playing")

    def test_play_on_activate_all(self):
        self.loader.get_manifest("b001").play_on_activate = True
        self.loader.activate("b001")
        played = self.loader.play_on_activate_all()
        self.assertEqual(played, 1)


# ---------------------------------------------------------------------------
# AudioBodyLoader — reverb zones
# ---------------------------------------------------------------------------

class TestAudioBodyLoaderReverbZones(unittest.TestCase):
    def setUp(self):
        self.loader = AudioBodyLoader()

    def test_register_reverb_zone_returns_zone(self):
        z = self.loader.register_reverb_zone("Cave", radius=10.0)
        self.assertIsInstance(z, ReverbZoneDef)

    def test_zone_name(self):
        z = self.loader.register_reverb_zone("Cave")
        self.assertEqual(z.name, "Cave")

    def test_zone_id_unique(self):
        z1 = self.loader.register_reverb_zone("Cave")
        z2 = self.loader.register_reverb_zone("Hall")
        self.assertNotEqual(z1.zone_id, z2.zone_id)

    def test_get_reverb_zone_count(self):
        self.loader.register_reverb_zone("Cave")
        self.loader.register_reverb_zone("Hall")
        self.assertEqual(self.loader.get_reverb_zone_count(), 2)

    def test_get_reverb_zone_by_id(self):
        z = self.loader.register_reverb_zone("Cave")
        fetched = self.loader.get_reverb_zone(z.zone_id)
        self.assertIsNotNone(fetched)

    def test_unregister_reverb_zone(self):
        z = self.loader.register_reverb_zone("Cave")
        self.assertTrue(self.loader.unregister_reverb_zone(z.zone_id))
        self.assertEqual(self.loader.get_reverb_zone_count(), 0)

    def test_get_all_zone_ids(self):
        z = self.loader.register_reverb_zone("Cave")
        self.assertIn(z.zone_id, self.loader.get_all_zone_ids())

    def test_get_zones_containing_point_inside(self):
        z = self.loader.register_reverb_zone("Cave",
                                               pos_x=0.0, pos_y=0.0, pos_z=0.0,
                                               radius=10.0)
        ids = self.loader.get_zones_containing_point(0.0, 0.0, 0.0)
        self.assertIn(z.zone_id, ids)

    def test_get_zones_containing_point_outside(self):
        self.loader.register_reverb_zone("Cave",
                                          pos_x=0.0, pos_y=0.0, pos_z=0.0,
                                          radius=5.0)
        ids = self.loader.get_zones_containing_point(100.0, 0.0, 0.0)
        self.assertEqual(len(ids), 0)


# ---------------------------------------------------------------------------
# AudioBodyLoader — persistence
# ---------------------------------------------------------------------------

class TestAudioBodyLoaderPersistence(unittest.TestCase):
    def setUp(self):
        self.loader = AudioBodyLoader()
        self.loader.register("b001", "Footstep", scene_id="scene_01",
                               audio_layer="SFX")
        self.loader.register_reverb_zone("Cave", radius=10.0)

    def test_save_registry(self):
        out = str(TMP_DIR / "audio_registry.json")
        self.assertTrue(self.loader.save_registry(out))
        self.assertTrue(Path(out).exists())

    def test_save_registry_content(self):
        out = str(TMP_DIR / "audio_registry2.json")
        self.loader.save_registry(out)
        data = json.loads(Path(out).read_text())
        self.assertIn("bodies", data)
        self.assertIn("reverb_zones", data)
        self.assertEqual(data["bodies"][0]["body_id"], "b001")

    def test_load_registry(self):
        out = str(TMP_DIR / "audio_registry3.json")
        self.loader.save_registry(out)
        loader2 = AudioBodyLoader()
        count = loader2.load_registry(out)
        self.assertEqual(count, 1)
        self.assertIsNotNone(loader2.get_manifest("b001"))

    def test_load_registry_missing_file_returns_zero(self):
        loader2 = AudioBodyLoader()
        count = loader2.load_registry("/tmp/no_such_audio_file.json")
        self.assertEqual(count, 0)

    def test_load_registry_restores_reverb_zones(self):
        out = str(TMP_DIR / "audio_registry4.json")
        self.loader.save_registry(out)
        loader2 = AudioBodyLoader()
        loader2.load_registry(out)
        self.assertGreater(loader2.get_reverb_zone_count(), 0)


if __name__ == "__main__":
    unittest.main()
