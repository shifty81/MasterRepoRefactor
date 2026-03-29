"""Phase 29C — Tests for mu_solar_system.json and SolarSystemReplicator.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

MU_JSON = SOLAR_SYSTEMS_DIR / "mu_solar_system.json"
REPLICATOR_H = SCENE_DIR / "SolarSystemReplicator.h"


def _load_mu() -> dict:
    return json.loads(MU_JSON.read_text())


def _read_replicator() -> str:
    return REPLICATOR_H.read_text()


# ---------------------------------------------------------------------------
# Mu Solar System JSON
# ---------------------------------------------------------------------------

class TestMuSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(MU_JSON.exists())


class TestMuSolarSystemStructure(unittest.TestCase):
    def test_id_field(self):
        data = _load_mu()
        self.assertEqual(data["id"], "mu_solar_system_001")

    def test_name_field(self):
        data = _load_mu()
        self.assertIn("Mu", data["name"])

    def test_version_field(self):
        data = _load_mu()
        self.assertIn("version", data)

    def test_star_type_f5v(self):
        data = _load_mu()
        self.assertEqual(data["star"]["type"], "F5V")

    def test_star_luminosity(self):
        data = _load_mu()
        self.assertGreater(data["star"]["luminosity"], 0)

    def test_star_radius(self):
        data = _load_mu()
        self.assertGreater(data["star"]["radius"], 1000000)

    def test_total_celestials_8(self):
        data = _load_mu()
        self.assertEqual(data["total_celestials"], 8)

    def test_celestials_list_count(self):
        data = _load_mu()
        self.assertEqual(len(data["celestials"]), 8)

    def test_has_npc_factions(self):
        data = _load_mu()
        self.assertIn("npc_factions", data)
        self.assertGreaterEqual(len(data["npc_factions"]), 2)

    def test_has_pcg_config(self):
        data = _load_mu()
        self.assertIn("pcg_config", data)

    def test_pcg_seed_present(self):
        data = _load_mu()
        self.assertIn("seed", data["pcg_config"])

    def test_has_hazards(self):
        data = _load_mu()
        self.assertIn("hazards", data)
        self.assertGreaterEqual(len(data["hazards"]), 1)

    def test_celestials_have_ids(self):
        data = _load_mu()
        for c in data["celestials"]:
            self.assertIn("id", c)

    def test_celestials_have_types(self):
        data = _load_mu()
        for c in data["celestials"]:
            self.assertIn("type", c)

    def test_has_planet(self):
        data = _load_mu()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Planet", types)

    def test_has_gas_giant(self):
        data = _load_mu()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("GasGiant", types)

    def test_has_asteroid_belt(self):
        data = _load_mu()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("AsteroidBelt", types)

    def test_has_station(self):
        data = _load_mu()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Station", types)


# ---------------------------------------------------------------------------
# SolarSystemReplicator.h
# ---------------------------------------------------------------------------

class TestSolarSystemReplicatorExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(REPLICATOR_H.exists())


class TestSolarSystemReplicatorStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_replicator())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _read_replicator())

    def test_class_declaration(self):
        self.assertIn("SolarSystemReplicator", _read_replicator())

    def test_replica_mode_enum(self):
        self.assertIn("ReplicaMode", _read_replicator())

    def test_sync_state_enum(self):
        self.assertIn("SyncState", _read_replicator())

    def test_replica_role_enum(self):
        self.assertIn("ReplicaRole", _read_replicator())

    def test_replica_descriptor_struct(self):
        self.assertIn("ReplicaDescriptor", _read_replicator())

    def test_sync_checkpoint_struct(self):
        self.assertIn("SyncCheckpoint", _read_replicator())

    def test_replication_policy_struct(self):
        self.assertIn("ReplicationPolicy", _read_replicator())

    def test_conflict_record_struct(self):
        self.assertIn("ConflictRecord", _read_replicator())

    def test_register_replica_method(self):
        self.assertIn("RegisterReplica", _read_replicator())

    def test_unregister_replica_method(self):
        self.assertIn("UnregisterReplica", _read_replicator())

    def test_start_replication_method(self):
        self.assertIn("StartReplication", _read_replicator())

    def test_stop_replication_method(self):
        self.assertIn("StopReplication", _read_replicator())

    def test_sync_now_method(self):
        self.assertIn("SyncNow", _read_replicator())

    def test_get_sync_state_method(self):
        self.assertIn("GetSyncState", _read_replicator())

    def test_checkpoint_method(self):
        self.assertIn("Checkpoint", _read_replicator())

    def test_restore_from_checkpoint_method(self):
        self.assertIn("RestoreFromCheckpoint", _read_replicator())

    def test_get_conflicts_method(self):
        self.assertIn("GetConflicts", _read_replicator())

    def test_resolve_conflict_method(self):
        self.assertIn("ResolveConflict", _read_replicator())

    def test_get_replicas_method(self):
        self.assertIn("GetReplicas", _read_replicator())

    def test_get_leader_method(self):
        self.assertIn("GetLeader", _read_replicator())

    def test_replication_stats_struct(self):
        self.assertIn("ReplicationStats", _read_replicator())

    def test_get_replication_stats_method(self):
        self.assertIn("GetReplicationStats", _read_replicator())

    def test_set_replica_role_method(self):
        self.assertIn("SetReplicaRole", _read_replicator())

    def test_clear_method(self):
        self.assertIn("Clear()", _read_replicator())

    def test_save_state_method(self):
        self.assertIn("SaveReplicatorState", _read_replicator())

    def test_load_state_method(self):
        self.assertIn("LoadReplicatorState", _read_replicator())

    def test_functional_include(self):
        self.assertIn("<functional>", _read_replicator())

    def test_replica_fields(self):
        content = _read_replicator()
        self.assertIn("replicaId", content)
        self.assertIn("systemId", content)
        self.assertIn("endpoint", content)
        self.assertIn("lastSyncTimestamp", content)


if __name__ == "__main__":
    unittest.main()
