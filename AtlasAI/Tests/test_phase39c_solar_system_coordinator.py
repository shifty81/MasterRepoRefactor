"""Phase 39C — Tests for chi_solar_system.json and SolarSystemCoordinator.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS = REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"


def _read_header(name: str) -> str:
    return (SCENE_DIR / f"{name}.h").read_text()


def _load_json(name: str) -> dict:
    return json.loads((SOLAR_SYSTEMS / f"{name}.json").read_text())


# ---------------------------------------------------------------------------
# chi_solar_system.json
# ---------------------------------------------------------------------------

class TestChiSolarSystemJson(unittest.TestCase):
    def setUp(self):
        self.data = _load_json("chi_solar_system")

    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS / "chi_solar_system.json").exists())

    def test_id_field(self):
        self.assertEqual(self.data["id"], "chi_solar_system_001")

    def test_name_field(self):
        self.assertEqual(self.data["name"], "Chi Ironveil System")

    def test_version_field(self):
        self.assertEqual(self.data["version"], "1.0")

    def test_star_type(self):
        self.assertEqual(self.data["star"]["type"], "K4V")

    def test_star_radius(self):
        self.assertEqual(self.data["star"]["radius"], 580000)

    def test_star_luminosity(self):
        self.assertAlmostEqual(self.data["star"]["luminosity"], 0.38)

    def test_total_celestials(self):
        self.assertEqual(self.data["total_celestials"], 8)

    def test_celestials_count(self):
        self.assertEqual(len(self.data["celestials"]), 8)

    def test_habitable_planet_present(self):
        habitable = [c for c in self.data["celestials"] if c.get("habitable")]
        self.assertEqual(len(habitable), 1)

    def test_habitable_planet_name(self):
        habitable = [c for c in self.data["celestials"] if c.get("habitable")]
        self.assertEqual(habitable[0]["name"], "Ironveil Haven")

    def test_gas_giant_present(self):
        gas_giants = [c for c in self.data["celestials"] if c["type"] == "GasGiant"]
        self.assertGreater(len(gas_giants), 0)

    def test_station_present(self):
        stations = [c for c in self.data["celestials"] if c["type"] == "Station"]
        self.assertGreater(len(stations), 0)

    def test_anomaly_present(self):
        anomalies = [c for c in self.data["celestials"] if c["type"] == "Anomaly"]
        self.assertGreater(len(anomalies), 0)

    def test_moon_has_parent(self):
        moons = [c for c in self.data["celestials"] if c["type"] == "Moon"]
        self.assertGreater(len(moons), 0)
        self.assertEqual(moons[0]["parent"], "chi_planet_003")

    def test_npc_factions_has_ironveil_covenant(self):
        self.assertIn("ironveil_covenant", self.data["npc_factions"])

    def test_pcg_seed(self):
        self.assertEqual(self.data["pcg_config"]["seed"], 2200)

    def test_hazards_has_magnetic_storm(self):
        self.assertIn("magnetic_storm", self.data["hazards"])

    def test_hazards_has_debris_field(self):
        self.assertIn("debris_field", self.data["hazards"])

    def test_pcg_hazard_level(self):
        self.assertEqual(self.data["pcg_config"]["hazard_level"], "high")

    def test_pcg_resource_richness(self):
        self.assertEqual(self.data["pcg_config"]["resource_richness"], "moderate")


# ---------------------------------------------------------------------------
# SolarSystemCoordinator.h
# ---------------------------------------------------------------------------

class TestSolarSystemCoordinatorHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemCoordinator.h").exists())


class TestSolarSystemCoordinatorNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("SolarSystemCoordinator"))


class TestSolarSystemCoordinatorEnums(unittest.TestCase):
    def test_coordinator_mode_enum(self):
        self.assertIn("CoordinatorMode", _read_header("SolarSystemCoordinator"))

    def test_resource_type_enum(self):
        self.assertIn("ResourceType", _read_header("SolarSystemCoordinator"))

    def test_allocation_policy_enum(self):
        self.assertIn("AllocationPolicy", _read_header("SolarSystemCoordinator"))

    def test_sync_event_type_enum(self):
        self.assertIn("SyncEventType", _read_header("SolarSystemCoordinator"))

    def test_passive_mode_value(self):
        self.assertIn("Passive", _read_header("SolarSystemCoordinator"))

    def test_arbitrating_mode_value(self):
        self.assertIn("Arbitrating", _read_header("SolarSystemCoordinator"))

    def test_cpu_resource_value(self):
        self.assertIn("CPU", _read_header("SolarSystemCoordinator"))

    def test_priority_based_policy_value(self):
        self.assertIn("PriorityBased", _read_header("SolarSystemCoordinator"))


class TestSolarSystemCoordinatorStructs(unittest.TestCase):
    def test_resource_slot_def_struct(self):
        self.assertIn("ResourceSlotDef", _read_header("SolarSystemCoordinator"))

    def test_system_participant_struct(self):
        self.assertIn("SystemParticipant", _read_header("SolarSystemCoordinator"))

    def test_sync_record_struct(self):
        self.assertIn("SyncRecord", _read_header("SolarSystemCoordinator"))

    def test_allocated_units_in_slot(self):
        self.assertIn("allocatedUnits", _read_header("SolarSystemCoordinator"))

    def test_active_priority_in_participant(self):
        self.assertIn("activePriority", _read_header("SolarSystemCoordinator"))

    def test_acknowledged_in_sync_record(self):
        self.assertIn("acknowledged", _read_header("SolarSystemCoordinator"))


class TestSolarSystemCoordinatorMethods(unittest.TestCase):
    def test_register_participant(self):
        self.assertIn("RegisterParticipant", _read_header("SolarSystemCoordinator"))

    def test_unregister_participant(self):
        self.assertIn("UnregisterParticipant", _read_header("SolarSystemCoordinator"))

    def test_set_participant_mode(self):
        self.assertIn("SetParticipantMode", _read_header("SolarSystemCoordinator"))

    def test_set_participant_priority(self):
        self.assertIn("SetParticipantPriority", _read_header("SolarSystemCoordinator"))

    def test_set_online(self):
        self.assertIn("SetOnline", _read_header("SolarSystemCoordinator"))

    def test_get_participant(self):
        self.assertIn("GetParticipant", _read_header("SolarSystemCoordinator"))

    def test_get_all_participant_ids(self):
        self.assertIn("GetAllParticipantIds", _read_header("SolarSystemCoordinator"))

    def test_get_online_participants(self):
        self.assertIn("GetOnlineParticipants", _read_header("SolarSystemCoordinator"))

    def test_get_offline_participants(self):
        self.assertIn("GetOfflineParticipants", _read_header("SolarSystemCoordinator"))

    def test_allocate_slot(self):
        self.assertIn("AllocateSlot", _read_header("SolarSystemCoordinator"))

    def test_deallocate_slot(self):
        self.assertIn("DeallocateSlot", _read_header("SolarSystemCoordinator"))

    def test_reserve_slot(self):
        self.assertIn("ReserveSlot", _read_header("SolarSystemCoordinator"))

    def test_release_slot(self):
        self.assertIn("ReleaseSlot", _read_header("SolarSystemCoordinator"))

    def test_set_allocation_policy(self):
        self.assertIn("SetAllocationPolicy", _read_header("SolarSystemCoordinator"))

    def test_get_slot(self):
        self.assertIn("GetSlot", _read_header("SolarSystemCoordinator"))

    def test_get_all_slot_ids(self):
        self.assertIn("GetAllSlotIds", _read_header("SolarSystemCoordinator"))

    def test_get_slots_by_system(self):
        self.assertIn("GetSlotsBySystem", _read_header("SolarSystemCoordinator"))

    def test_get_slots_by_resource_type(self):
        self.assertIn("GetSlotsByResourceType", _read_header("SolarSystemCoordinator"))

    def test_get_reserved_slots(self):
        self.assertIn("GetReservedSlots", _read_header("SolarSystemCoordinator"))

    def test_record_sync_event(self):
        self.assertIn("RecordSyncEvent", _read_header("SolarSystemCoordinator"))

    def test_acknowledge_sync_event(self):
        self.assertIn("AcknowledgeSyncEvent", _read_header("SolarSystemCoordinator"))

    def test_get_sync_record(self):
        self.assertIn("GetSyncRecord", _read_header("SolarSystemCoordinator"))

    def test_get_sync_by_participant(self):
        self.assertIn("GetSyncByParticipant", _read_header("SolarSystemCoordinator"))

    def test_get_unacknowledged_events(self):
        self.assertIn("GetUnacknowledgedEvents", _read_header("SolarSystemCoordinator"))

    def test_flush_sync_log(self):
        self.assertIn("FlushSyncLog", _read_header("SolarSystemCoordinator"))

    def test_reset(self):
        self.assertIn("Reset", _read_header("SolarSystemCoordinator"))


if __name__ == "__main__":
    unittest.main()
