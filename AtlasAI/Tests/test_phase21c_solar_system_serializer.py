"""Phase 21C — Tests for delta_solar_system.json and SolarSystemSerializer.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = (
    REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
)
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"


# ---------------------------------------------------------------------------
# delta_solar_system.json
# ---------------------------------------------------------------------------

class TestDeltaSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS_DIR / "delta_solar_system.json").exists())


class TestDeltaSolarSystemStructure(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (SOLAR_SYSTEMS_DIR / "delta_solar_system.json").read_text()
        )

    def test_id_field(self):
        self.assertIn("id", self.data)

    def test_id_starts_with_delta(self):
        self.assertTrue(self.data["id"].startswith("delta_solar_system"))

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
        self.assertEqual(self.data["total_celestials"], len(self.data["celestials"]))

    def test_npc_factions_nonempty(self):
        self.assertGreater(len(self.data["npc_factions"]), 0)

    def test_pcg_config_field(self):
        self.assertIn("pcg_config", self.data)


class TestDeltaSolarSystemCelestialTypes(unittest.TestCase):
    def setUp(self):
        data = json.loads(
            (SOLAR_SYSTEMS_DIR / "delta_solar_system.json").read_text()
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


class TestAllFourSolarSystemsDistinct(unittest.TestCase):
    def _load_id(self, fname: str) -> str:
        return json.loads((SOLAR_SYSTEMS_DIR / fname).read_text())["id"]

    def test_dev_still_valid(self):
        data = json.loads((SOLAR_SYSTEMS_DIR / "dev_solar_system.json").read_text())
        self.assertIn("id", data)

    def test_beta_still_valid(self):
        data = json.loads((SOLAR_SYSTEMS_DIR / "beta_solar_system.json").read_text())
        self.assertIn("id", data)

    def test_gamma_still_valid(self):
        data = json.loads((SOLAR_SYSTEMS_DIR / "gamma_solar_system.json").read_text())
        self.assertIn("id", data)

    def test_delta_valid(self):
        data = json.loads((SOLAR_SYSTEMS_DIR / "delta_solar_system.json").read_text())
        self.assertIn("id", data)

    def test_all_ids_unique(self):
        ids = [
            self._load_id("dev_solar_system.json"),
            self._load_id("beta_solar_system.json"),
            self._load_id("gamma_solar_system.json"),
            self._load_id("delta_solar_system.json"),
        ]
        self.assertEqual(len(ids), len(set(ids)))


# ---------------------------------------------------------------------------
# SolarSystemSerializer.h
# ---------------------------------------------------------------------------

def _ser() -> str:
    return (SCENE_DIR / "SolarSystemSerializer.h").read_text()


class TestSolarSystemSerializerExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemSerializer.h").exists())


class TestSolarSystemSerializerHeader(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _ser())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _ser())

    def test_class_declared(self):
        self.assertIn("class SolarSystemSerializer", _ser())


class TestSolarSystemSerializerAPI(unittest.TestCase):
    def test_serialize(self):
        self.assertIn("Serialize", _ser())

    def test_deserialize(self):
        self.assertIn("Deserialize", _ser())

    def test_save_to_file(self):
        self.assertIn("SaveToFile", _ser())

    def test_load_from_file(self):
        self.assertIn("LoadFromFile", _ser())

    def test_save_all(self):
        self.assertIn("SaveAll", _ser())

    def test_load_all(self):
        self.assertIn("LoadAll", _ser())

    def test_validate_json(self):
        self.assertIn("ValidateJson", _ser())

    def test_get_last_error(self):
        self.assertIn("GetLastError", _ser())

    def test_upgrade_to_latest(self):
        self.assertIn("UpgradeToLatest", _ser())

    def test_get_current_version(self):
        self.assertIn("GetCurrentVersion", _ser())

    def test_on_serialized_callback(self):
        self.assertIn("SetOnSerializedCallback", _ser())

    def test_on_deserialized_callback(self):
        self.assertIn("SetOnDeserializedCallback", _ser())


class TestSolarSystemSerializerStructs(unittest.TestCase):
    def test_serialized_system_struct(self):
        self.assertIn("SerializedSystem", _ser())

    def test_system_id_field(self):
        self.assertIn("systemId", _ser())

    def test_json_field(self):
        self.assertIn("json", _ser())

    def test_version_field(self):
        self.assertIn("version", _ser())

    def test_valid_field(self):
        self.assertIn("valid", _ser())


if __name__ == "__main__":
    unittest.main()
