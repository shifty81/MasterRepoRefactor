"""Phase 17C tests — Dev Solar System scaffold."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

SOLAR_SYSTEMS_DIR = REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
DEV_SOLAR_JSON = SOLAR_SYSTEMS_DIR / "dev_solar_system.json"
SOLAR_MGR_H = REPO_ROOT / "Atlas" / "Engine" / "Scene" / "SolarSystemManager.h"
PCG_CONFIG_JSON = REPO_ROOT / "NovaForge" / "Content" / "Config" / "PCG" / "solar_system_pcg_config.json"
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"


class TestPhase17CDirectories(unittest.TestCase):
    def test_solar_systems_directory_exists(self):
        self.assertTrue(SOLAR_SYSTEMS_DIR.is_dir())

    def test_atlas_engine_scene_directory_exists(self):
        self.assertTrue(SCENE_DIR.is_dir())


class TestPhase17CDevSolarJson(unittest.TestCase):
    def _data(self):
        return json.loads(DEV_SOLAR_JSON.read_text())

    def test_dev_solar_json_exists(self):
        self.assertTrue(DEV_SOLAR_JSON.exists())

    def test_dev_solar_json_is_valid_json(self):
        data = self._data()
        self.assertIsInstance(data, dict)

    def test_dev_solar_json_has_id(self):
        self.assertIn("id", self._data())

    def test_dev_solar_json_has_name(self):
        self.assertIn("name", self._data())

    def test_dev_solar_json_has_star(self):
        self.assertIn("star", self._data())

    def test_dev_solar_json_has_celestials(self):
        self.assertIn("celestials", self._data())

    def test_dev_solar_json_celestials_is_list(self):
        self.assertIsInstance(self._data()["celestials"], list)

    def test_dev_solar_json_celestials_at_least_four(self):
        self.assertGreaterEqual(len(self._data()["celestials"]), 4)

    def test_dev_solar_json_has_planet_type(self):
        types = {c["type"] for c in self._data()["celestials"]}
        self.assertIn("Planet", types)

    def test_dev_solar_json_has_station_type(self):
        types = {c["type"] for c in self._data()["celestials"]}
        self.assertIn("Station", types)

    def test_dev_solar_json_has_asteroid_belt_type(self):
        types = {c["type"] for c in self._data()["celestials"]}
        self.assertIn("AsteroidBelt", types)

    def test_dev_solar_json_star_has_type(self):
        self.assertIn("type", self._data()["star"])

    def test_dev_solar_json_id_value(self):
        self.assertEqual(self._data()["id"], "dev_solar_system_001")

    def test_dev_solar_json_celestials_each_have_id(self):
        for c in self._data()["celestials"]:
            self.assertIn("id", c)

    def test_dev_solar_json_celestials_each_have_type(self):
        for c in self._data()["celestials"]:
            self.assertIn("type", c)

    def test_dev_solar_json_has_npc_factions(self):
        self.assertIn("npc_factions", self._data())

    def test_dev_solar_json_has_pcg_config(self):
        self.assertIn("pcg_config", self._data())


class TestPhase17CSolarSystemManagerHeader(unittest.TestCase):
    def _content(self):
        return SOLAR_MGR_H.read_text()

    def test_solar_system_manager_header_exists(self):
        self.assertTrue(SOLAR_MGR_H.exists())

    def test_solar_system_manager_pragma_once(self):
        self.assertIn("#pragma once", self._content())

    def test_solar_system_manager_class(self):
        self.assertIn("class SolarSystemManager", self._content())

    def test_solar_system_manager_load_from_file(self):
        self.assertIn("LoadFromFile", self._content())

    def test_solar_system_manager_get_celestial_count(self):
        self.assertIn("GetCelestialCount", self._content())

    def test_solar_system_manager_get_system_id(self):
        self.assertIn("GetSystemId", self._content())

    def test_solar_system_manager_celestial_body_struct(self):
        self.assertIn("CelestialBody", self._content())

    def test_solar_system_manager_load_from_json(self):
        self.assertIn("LoadFromJson", self._content())


class TestPhase17CPCGConfig(unittest.TestCase):
    def _data(self):
        return json.loads(PCG_CONFIG_JSON.read_text())

    def test_pcg_config_exists(self):
        self.assertTrue(PCG_CONFIG_JSON.exists())

    def test_pcg_config_is_valid_json(self):
        self.assertIsInstance(self._data(), dict)

    def test_pcg_config_has_asset_types(self):
        self.assertIn("asset_types", self._data())

    def test_pcg_config_asset_types_multiple_entries(self):
        self.assertGreater(len(self._data()["asset_types"]), 1)

    def test_pcg_config_has_generator(self):
        self.assertIn("generator", self._data())

    def test_pcg_config_has_faction_distribution(self):
        self.assertIn("faction_distribution", self._data())


if __name__ == "__main__":
    unittest.main()
