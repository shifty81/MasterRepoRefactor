"""Phase 19C — Tests for beta_solar_system.json and SolarSystemRegistry.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = (
    REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
)
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"


# ---------------------------------------------------------------------------
# beta_solar_system.json
# ---------------------------------------------------------------------------

class TestBetaSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS_DIR / "beta_solar_system.json").exists())


class TestBetaSolarSystemStructure(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (SOLAR_SYSTEMS_DIR / "beta_solar_system.json").read_text()
        )

    def test_id_field(self):
        self.assertIn("id", self.data)

    def test_id_value(self):
        self.assertTrue(self.data["id"].startswith("beta_solar_system"))

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

    def test_total_celestials_field(self):
        self.assertIn("total_celestials", self.data)

    def test_total_celestials_matches_list(self):
        self.assertEqual(
            self.data["total_celestials"], len(self.data["celestials"])
        )

    def test_npc_factions_field(self):
        self.assertIn("npc_factions", self.data)

    def test_npc_factions_nonempty(self):
        self.assertGreater(len(self.data["npc_factions"]), 0)

    def test_pcg_config_field(self):
        self.assertIn("pcg_config", self.data)


class TestBetaSolarSystemCelestialTypes(unittest.TestCase):
    def setUp(self):
        data = json.loads(
            (SOLAR_SYSTEMS_DIR / "beta_solar_system.json").read_text()
        )
        self.celestials = data["celestials"]
        self.types = {c["type"] for c in self.celestials}

    def test_has_planet(self):
        self.assertIn("Planet", self.types)

    def test_has_station(self):
        self.assertIn("Station", self.types)

    def test_has_asteroid_belt(self):
        self.assertIn("AsteroidBelt", self.types)

    def test_has_wormhole_or_stargate(self):
        self.assertTrue(
            "Wormhole" in self.types or "Stargate" in self.types
        )

    def test_each_celestial_has_id(self):
        for c in self.celestials:
            self.assertIn("id", c)

    def test_each_celestial_has_orbit_radius(self):
        for c in self.celestials:
            self.assertIn("orbit_radius", c)

    def test_celestial_ids_unique(self):
        ids = [c["id"] for c in self.celestials]
        self.assertEqual(len(ids), len(set(ids)))


class TestBothSolarSystemsLoadable(unittest.TestCase):
    def test_dev_solar_system_still_valid(self):
        path = SOLAR_SYSTEMS_DIR / "dev_solar_system.json"
        data = json.loads(path.read_text())
        self.assertIn("id", data)

    def test_beta_solar_system_valid(self):
        path = SOLAR_SYSTEMS_DIR / "beta_solar_system.json"
        data = json.loads(path.read_text())
        self.assertIn("id", data)

    def test_ids_are_distinct(self):
        dev = json.loads(
            (SOLAR_SYSTEMS_DIR / "dev_solar_system.json").read_text()
        )["id"]
        beta = json.loads(
            (SOLAR_SYSTEMS_DIR / "beta_solar_system.json").read_text()
        )["id"]
        self.assertNotEqual(dev, beta)


# ---------------------------------------------------------------------------
# SolarSystemRegistry.h
# ---------------------------------------------------------------------------

def _reg() -> str:
    return (SCENE_DIR / "SolarSystemRegistry.h").read_text()


class TestSolarSystemRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemRegistry.h").exists())


class TestSolarSystemRegistryHeader(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _reg())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _reg())

    def test_class_declared(self):
        self.assertIn("class SolarSystemRegistry", _reg())


class TestSolarSystemRegistryAPI(unittest.TestCase):
    def test_register_system(self):
        self.assertIn("RegisterSystem", _reg())

    def test_unregister_system(self):
        self.assertIn("UnregisterSystem", _reg())

    def test_is_registered(self):
        self.assertIn("IsRegistered", _reg())

    def test_get_system_count(self):
        self.assertIn("GetSystemCount", _reg())

    def test_set_active_system(self):
        self.assertIn("SetActiveSystem", _reg())

    def test_get_active_system_id(self):
        self.assertIn("GetActiveSystemId", _reg())

    def test_has_active_system(self):
        self.assertIn("HasActiveSystem", _reg())

    def test_get_system(self):
        self.assertIn("GetSystem", _reg())

    def test_get_all_system_ids(self):
        self.assertIn("GetAllSystemIds", _reg())

    def test_mark_loaded(self):
        self.assertIn("MarkLoaded", _reg())

    def test_is_loaded(self):
        self.assertIn("IsLoaded", _reg())

    def test_for_each(self):
        self.assertIn("ForEach", _reg())

    def test_clear(self):
        self.assertIn("Clear", _reg())


class TestSolarSystemRegistrySystemRecord(unittest.TestCase):
    def test_system_record_struct(self):
        self.assertIn("SystemRecord", _reg())

    def test_system_record_id_field(self):
        self.assertIn("std::string id", _reg())

    def test_system_record_data_path_field(self):
        self.assertIn("dataPath", _reg())

    def test_system_record_loaded_flag(self):
        self.assertIn("loaded", _reg())


if __name__ == "__main__":
    unittest.main()
