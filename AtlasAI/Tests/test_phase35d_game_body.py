"""Phase 35D — Tests for GameBodyRegistry.h and GameBodyLoader."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    GameBodyLoader,
    GameBodyManifest,
    SpawnConfigManifest,
    GameEventManifest,
)

GAME_REGISTRY_H = SCENE_DIR / "GameBodyRegistry.h"


def _read_registry() -> str:
    return GAME_REGISTRY_H.read_text()


# ---------------------------------------------------------------------------
# GameBodyRegistry.h
# ---------------------------------------------------------------------------

class TestGameBodyRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(GAME_REGISTRY_H.exists())


class TestGameBodyRegistryStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_registry())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_registry())

    def test_class_declaration(self):
        self.assertIn("GameBodyRegistry", _read_registry())

    def test_game_body_state_enum(self):
        self.assertIn("GameBodyState", _read_registry())

    def test_game_body_role_enum(self):
        self.assertIn("GameBodyRole", _read_registry())

    def test_game_event_type_enum(self):
        self.assertIn("GameEventType", _read_registry())

    def test_game_body_flags_enum(self):
        self.assertIn("GameBodyFlags", _read_registry())

    def test_spawn_policy_enum(self):
        self.assertIn("SpawnPolicy", _read_registry())

    def test_spawn_config_struct(self):
        self.assertIn("SpawnConfig", _read_registry())

    def test_game_event_record_struct(self):
        self.assertIn("GameEventRecord", _read_registry())

    def test_game_body_record_struct(self):
        self.assertIn("GameBodyRecord", _read_registry())

    def test_register_body(self):
        self.assertIn("RegisterBody", _read_registry())

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_registry())

    def test_set_body_role(self):
        self.assertIn("SetBodyRole", _read_registry())

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_registry())

    def test_set_spawn_policy(self):
        self.assertIn("SetSpawnPolicy", _read_registry())

    def test_set_health(self):
        self.assertIn("SetHealth", _read_registry())

    def test_add_event(self):
        self.assertIn("AddEvent", _read_registry())

    def test_remove_event(self):
        self.assertIn("RemoveEvent", _read_registry())

    def test_get_all_body_ids(self):
        self.assertIn("GetAllBodyIds", _read_registry())

    def test_get_bodies_by_role(self):
        self.assertIn("GetBodiesByRole", _read_registry())

    def test_get_bodies_by_state(self):
        self.assertIn("GetBodiesByState", _read_registry())

    def test_get_active_body(self):
        self.assertIn("GetActiveBody", _read_registry())

    def test_get_dead_bodies(self):
        self.assertIn("GetDeadBodies", _read_registry())

    def test_respawn_body(self):
        self.assertIn("RespawnBody", _read_registry())

    def test_despawn_body(self):
        self.assertIn("DespawnBody", _read_registry())

    def test_clear_method(self):
        self.assertIn("Clear", _read_registry())

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_registry())

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_registry())


# ---------------------------------------------------------------------------
# SpawnConfigManifest
# ---------------------------------------------------------------------------

class TestSpawnConfigManifest(unittest.TestCase):
    def test_default_policy(self):
        c = SpawnConfigManifest()
        self.assertEqual(c.policy, "Immediate")

    def test_default_spawn_radius(self):
        c = SpawnConfigManifest()
        self.assertAlmostEqual(c.spawn_radius, 500.0)

    def test_default_max_instances(self):
        c = SpawnConfigManifest()
        self.assertEqual(c.max_instances, 100)

    def test_is_pooled_false(self):
        c = SpawnConfigManifest()
        self.assertFalse(c.is_pooled)

    def test_is_pooled_true(self):
        c = SpawnConfigManifest(policy="Pooled")
        self.assertTrue(c.is_pooled)

    def test_is_persistent_false(self):
        c = SpawnConfigManifest()
        self.assertFalse(c.is_persistent)


# ---------------------------------------------------------------------------
# GameEventManifest
# ---------------------------------------------------------------------------

class TestGameEventManifest(unittest.TestCase):
    def test_event_id(self):
        e = GameEventManifest(event_id="ev_001", body_id="body_001")
        self.assertEqual(e.event_id, "ev_001")

    def test_body_id(self):
        e = GameEventManifest(event_id="ev_001", body_id="body_001")
        self.assertEqual(e.body_id, "body_001")

    def test_default_event_type(self):
        e = GameEventManifest(event_id="ev_001", body_id="body_001")
        self.assertEqual(e.event_type, "Spawn")

    def test_is_spawn_true(self):
        e = GameEventManifest(event_id="ev_001", body_id="body_001", event_type="Spawn")
        self.assertTrue(e.is_spawn)

    def test_is_death_false(self):
        e = GameEventManifest(event_id="ev_001", body_id="body_001")
        self.assertFalse(e.is_death)


# ---------------------------------------------------------------------------
# GameBodyManifest
# ---------------------------------------------------------------------------

class TestGameBodyManifest(unittest.TestCase):
    def test_body_id(self):
        m = GameBodyManifest(body_id="body_001", name="PlayerCharacter")
        self.assertEqual(m.body_id, "body_001")

    def test_name_field(self):
        m = GameBodyManifest(body_id="body_001", name="PlayerCharacter")
        self.assertEqual(m.name, "PlayerCharacter")

    def test_default_role(self):
        m = GameBodyManifest(body_id="body_001", name="PlayerCharacter")
        self.assertEqual(m.role, "NPC")

    def test_is_alive_false(self):
        m = GameBodyManifest(body_id="body_001", name="PlayerCharacter", body_state="Inactive")
        self.assertFalse(m.is_alive)

    def test_is_player_false(self):
        m = GameBodyManifest(body_id="body_001", name="PlayerCharacter", role="NPC")
        self.assertFalse(m.is_player)

    def test_has_events_false(self):
        m = GameBodyManifest(body_id="body_001", name="PlayerCharacter")
        self.assertFalse(m.has_events)


# ---------------------------------------------------------------------------
# GameBodyLoader
# ---------------------------------------------------------------------------

class TestGameBodyLoader(unittest.TestCase):
    def _loader(self):
        return GameBodyLoader()

    def test_load_manifest_returns_manifest(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "body_001", "name": "PlayerCharacter"})
        self.assertIsInstance(m, GameBodyManifest)

    def test_load_manifest_id(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "body_001", "name": "PlayerCharacter"})
        self.assertEqual(m.body_id, "body_001")

    def test_load_manifest_name(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "body_001", "name": "PlayerCharacter"})
        self.assertEqual(m.name, "PlayerCharacter")

    def test_load_batch(self):
        loader = self._loader()
        batch = loader.load_batch([
            {"body_id": "body_001", "name": "PlayerCharacter"},
            {"body_id": "body_002", "name": "NPC"},
        ])
        self.assertEqual(len(batch), 2)

    def test_validate_valid_manifest(self):
        loader = self._loader()
        m = GameBodyManifest(body_id="body_001", name="PlayerCharacter")
        self.assertTrue(loader.validate(m))

    def test_validate_empty_name_fails(self):
        loader = self._loader()
        m = GameBodyManifest(body_id="body_001", name="")
        self.assertFalse(loader.validate(m))

    def test_loaded_count_zero(self):
        loader = self._loader()
        self.assertEqual(loader.loaded_count, 0)

    def test_clear_resets(self):
        loader = self._loader()
        loader.load_manifest({"body_id": "body_001", "name": "PlayerCharacter"})
        loader.clear()
        self.assertEqual(loader.loaded_count, 0)

    def test_save_manifest_creates_file(self):
        loader = self._loader()
        m = GameBodyManifest(body_id="body_001", name="PlayerCharacter")
        save_path = REPO_ROOT / "AtlasAI" / "Tests" / "_test_game_body_save_35d.json"
        try:
            loader.save_manifest(m, save_path)
            self.assertTrue(save_path.exists())
        finally:
            if save_path.exists():
                save_path.unlink()


if __name__ == "__main__":
    unittest.main()
