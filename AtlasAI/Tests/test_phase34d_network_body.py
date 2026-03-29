"""Phase 34D — Tests for NetworkBodyRegistry.h and NetworkBodyLoader."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    NetworkBodyLoader,
    NetworkBodyManifest,
    ReplicationConfigManifest,
    NetworkPropertyManifest,
)

NETWORK_REGISTRY_H = SCENE_DIR / "NetworkBodyRegistry.h"


def _read_registry() -> str:
    return NETWORK_REGISTRY_H.read_text()


# ---------------------------------------------------------------------------
# NetworkBodyRegistry.h
# ---------------------------------------------------------------------------

class TestNetworkBodyRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(NETWORK_REGISTRY_H.exists())


class TestNetworkBodyRegistryStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_registry())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_registry())

    def test_class_declaration(self):
        self.assertIn("NetworkBodyRegistry", _read_registry())

    def test_network_body_state_enum(self):
        self.assertIn("NetworkBodyState", _read_registry())

    def test_network_body_role_enum(self):
        self.assertIn("NetworkBodyRole", _read_registry())

    def test_replication_mode_enum(self):
        self.assertIn("ReplicationMode", _read_registry())

    def test_network_channel_enum(self):
        self.assertIn("NetworkChannel", _read_registry())

    def test_sync_frequency_enum(self):
        self.assertIn("SyncFrequency", _read_registry())

    def test_replication_config_struct(self):
        self.assertIn("ReplicationConfig", _read_registry())

    def test_network_property_def_struct(self):
        self.assertIn("NetworkPropertyDef", _read_registry())

    def test_network_body_record_struct(self):
        self.assertIn("NetworkBodyRecord", _read_registry())

    def test_register_body(self):
        self.assertIn("RegisterBody", _read_registry())

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_registry())

    def test_set_body_role(self):
        self.assertIn("SetBodyRole", _read_registry())

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_registry())

    def test_set_replication_mode(self):
        self.assertIn("SetReplicationMode", _read_registry())

    def test_set_sync_frequency(self):
        self.assertIn("SetSyncFrequency", _read_registry())

    def test_add_network_property(self):
        self.assertIn("AddNetworkProperty", _read_registry())

    def test_remove_network_property(self):
        self.assertIn("RemoveNetworkProperty", _read_registry())

    def test_get_all_body_ids(self):
        self.assertIn("GetAllBodyIds", _read_registry())

    def test_get_bodies_by_role(self):
        self.assertIn("GetBodiesByRole", _read_registry())

    def test_get_bodies_by_state(self):
        self.assertIn("GetBodiesByState", _read_registry())

    def test_get_connected_bodies(self):
        self.assertIn("GetConnectedBodies", _read_registry())

    def test_get_authority_bodies(self):
        self.assertIn("GetAuthorityBodies", _read_registry())

    def test_get_proxies(self):
        self.assertIn("GetProxies", _read_registry())

    def test_clear_method(self):
        self.assertIn("Clear", _read_registry())

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_registry())

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_registry())


# ---------------------------------------------------------------------------
# ReplicationConfigManifest
# ---------------------------------------------------------------------------

class TestReplicationConfigManifest(unittest.TestCase):
    def test_config_id(self):
        c = ReplicationConfigManifest(config_id="cfg_001")
        self.assertEqual(c.config_id, "cfg_001")

    def test_default_mode(self):
        c = ReplicationConfigManifest(config_id="cfg_001")
        self.assertEqual(c.mode, "RepGraph")

    def test_default_channel(self):
        c = ReplicationConfigManifest(config_id="cfg_001")
        self.assertEqual(c.channel, "Reliable")

    def test_is_reliable_true(self):
        c = ReplicationConfigManifest(config_id="cfg_001", channel="Reliable")
        self.assertTrue(c.is_reliable)

    def test_has_relevancy_true(self):
        c = ReplicationConfigManifest(config_id="cfg_001", relevancy_radius=10000.0)
        self.assertTrue(c.has_relevancy)


# ---------------------------------------------------------------------------
# NetworkPropertyManifest
# ---------------------------------------------------------------------------

class TestNetworkPropertyManifest(unittest.TestCase):
    def test_prop_id(self):
        p = NetworkPropertyManifest(prop_id="prop_001", prop_name="Health")
        self.assertEqual(p.prop_id, "prop_001")

    def test_prop_name(self):
        p = NetworkPropertyManifest(prop_id="prop_001", prop_name="Health")
        self.assertEqual(p.prop_name, "Health")

    def test_default_prop_type(self):
        p = NetworkPropertyManifest(prop_id="prop_001", prop_name="Health")
        self.assertEqual(p.prop_type, "Float")

    def test_is_owner_only_false(self):
        p = NetworkPropertyManifest(prop_id="prop_001", prop_name="Health")
        self.assertFalse(p.is_owner_only)

    def test_is_always_replicated_true(self):
        p = NetworkPropertyManifest(prop_id="prop_001", prop_name="Health", condition="Always")
        self.assertTrue(p.is_always_replicated)


# ---------------------------------------------------------------------------
# NetworkBodyManifest
# ---------------------------------------------------------------------------

class TestNetworkBodyManifest(unittest.TestCase):
    def test_body_id(self):
        m = NetworkBodyManifest(body_id="body_001", name="PlayerCharacter")
        self.assertEqual(m.body_id, "body_001")

    def test_name_field(self):
        m = NetworkBodyManifest(body_id="body_001", name="PlayerCharacter")
        self.assertEqual(m.name, "PlayerCharacter")

    def test_default_role(self):
        m = NetworkBodyManifest(body_id="body_001", name="PlayerCharacter")
        self.assertEqual(m.role, "SimulatedProxy")

    def test_is_connected_false(self):
        m = NetworkBodyManifest(body_id="body_001", name="PlayerCharacter", body_state="Offline")
        self.assertFalse(m.is_connected)

    def test_is_authority_false(self):
        m = NetworkBodyManifest(body_id="body_001", name="PlayerCharacter", role="SimulatedProxy")
        self.assertFalse(m.is_authority)

    def test_has_properties_false(self):
        m = NetworkBodyManifest(body_id="body_001", name="PlayerCharacter")
        self.assertFalse(m.has_properties)


# ---------------------------------------------------------------------------
# NetworkBodyLoader
# ---------------------------------------------------------------------------

class TestNetworkBodyLoader(unittest.TestCase):
    def _loader(self):
        return NetworkBodyLoader()

    def test_load_manifest_returns_manifest(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "body_001", "name": "PlayerCharacter"})
        self.assertIsInstance(m, NetworkBodyManifest)

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
        m = NetworkBodyManifest(body_id="body_001", name="PlayerCharacter")
        self.assertTrue(loader.validate(m))

    def test_validate_empty_name_fails(self):
        loader = self._loader()
        m = NetworkBodyManifest(body_id="body_001", name="")
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
        m = NetworkBodyManifest(body_id="body_001", name="PlayerCharacter")
        save_path = REPO_ROOT / "AtlasAI" / "Tests" / "_test_network_save_34d.json"
        try:
            loader.save_manifest(m, save_path)
            self.assertTrue(save_path.exists())
        finally:
            if save_path.exists():
                save_path.unlink()


if __name__ == "__main__":
    unittest.main()
