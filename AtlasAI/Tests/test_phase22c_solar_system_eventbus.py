"""Phase 22C — Tests for epsilon_solar_system.json and SolarSystemEventBus.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = (
    REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
)
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"


# ---------------------------------------------------------------------------
# epsilon_solar_system.json
# ---------------------------------------------------------------------------

class TestEpsilonSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS_DIR / "epsilon_solar_system.json").exists())


class TestEpsilonSolarSystemStructure(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (SOLAR_SYSTEMS_DIR / "epsilon_solar_system.json").read_text()
        )

    def test_id_field(self):
        self.assertIn("id", self.data)

    def test_id_starts_with_epsilon(self):
        self.assertTrue(self.data["id"].startswith("epsilon_solar_system"))

    def test_name_field(self):
        self.assertIn("name", self.data)

    def test_star_field(self):
        self.assertIn("star", self.data)

    def test_star_has_type(self):
        self.assertIn("type", self.data["star"])

    def test_celestials_field(self):
        self.assertIn("celestials", self.data)

    def test_celestials_is_list(self):
        self.assertIsInstance(self.data["celestials"], list)

    def test_celestials_count_at_least_six(self):
        self.assertGreaterEqual(len(self.data["celestials"]), 6)

    def test_total_celestials_matches_list(self):
        self.assertEqual(
            self.data["total_celestials"], len(self.data["celestials"])
        )

    def test_npc_factions_nonempty(self):
        self.assertGreater(len(self.data["npc_factions"]), 0)

    def test_pcg_config_field(self):
        self.assertIn("pcg_config", self.data)


class TestEpsilonSolarSystemCelestialTypes(unittest.TestCase):
    def setUp(self):
        data = json.loads(
            (SOLAR_SYSTEMS_DIR / "epsilon_solar_system.json").read_text()
        )
        self.celestials = data["celestials"]
        self.types = {c["type"] for c in self.celestials}

    def test_has_planet(self):
        self.assertIn("Planet", self.types)

    def test_has_station_or_gate(self):
        self.assertTrue(
            "Station" in self.types or "Stargate" in self.types
        )

    def test_celestial_ids_unique(self):
        ids = [c["id"] for c in self.celestials]
        self.assertEqual(len(ids), len(set(ids)))

    def test_each_celestial_has_orbit_radius(self):
        for c in self.celestials:
            self.assertIn("orbit_radius", c)


class TestAllFiveSolarSystemsDistinct(unittest.TestCase):
    _FILES = [
        "dev_solar_system.json",
        "beta_solar_system.json",
        "gamma_solar_system.json",
        "delta_solar_system.json",
        "epsilon_solar_system.json",
    ]

    def _load_id(self, fname: str) -> str:
        return json.loads((SOLAR_SYSTEMS_DIR / fname).read_text())["id"]

    def test_all_five_files_exist(self):
        for f in self._FILES:
            self.assertTrue((SOLAR_SYSTEMS_DIR / f).exists())

    def test_all_ids_unique(self):
        ids = [self._load_id(f) for f in self._FILES]
        self.assertEqual(len(ids), len(set(ids)))


# ---------------------------------------------------------------------------
# SolarSystemEventBus.h
# ---------------------------------------------------------------------------

def _bus() -> str:
    return (SCENE_DIR / "SolarSystemEventBus.h").read_text()


class TestSolarSystemEventBusExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemEventBus.h").exists())


class TestSolarSystemEventBusHeader(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _bus())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _bus())

    def test_class_declared(self):
        self.assertIn("class SolarSystemEventBus", _bus())


class TestSolarSystemEventBusAPI(unittest.TestCase):
    def test_subscribe(self):
        self.assertIn("Subscribe", _bus())

    def test_unsubscribe(self):
        self.assertIn("Unsubscribe", _bus())

    def test_publish(self):
        self.assertIn("Publish", _bus())

    def test_publish_system_registered(self):
        self.assertIn("PublishSystemRegistered", _bus())

    def test_publish_system_loaded(self):
        self.assertIn("PublishSystemLoaded", _bus())

    def test_publish_system_unloaded(self):
        self.assertIn("PublishSystemUnloaded", _bus())

    def test_publish_celestial_added(self):
        self.assertIn("PublishCelestialAdded", _bus())

    def test_publish_system_linked(self):
        self.assertIn("PublishSystemLinked", _bus())

    def test_get_published_count(self):
        self.assertIn("GetPublishedCount", _bus())

    def test_clear_history(self):
        self.assertIn("ClearHistory", _bus())

    def test_get_recent_events(self):
        self.assertIn("GetRecentEvents", _bus())

    def test_instance_singleton(self):
        self.assertIn("Instance", _bus())

    def test_unsubscribe_all(self):
        self.assertIn("UnsubscribeAll", _bus())

    def test_get_handler_count(self):
        self.assertIn("GetHandlerCount", _bus())


class TestSolarSystemEventBusStructs(unittest.TestCase):
    def test_event_type_enum(self):
        self.assertIn("EventType", _bus())

    def test_solar_system_event_struct(self):
        self.assertIn("SolarSystemEvent", _bus())

    def test_event_handler_typedef(self):
        self.assertIn("EventHandler", _bus())

    def test_system_registered_event(self):
        self.assertIn("SystemRegistered", _bus())

    def test_celestial_added_event(self):
        self.assertIn("CelestialAdded", _bus())


if __name__ == "__main__":
    unittest.main()
