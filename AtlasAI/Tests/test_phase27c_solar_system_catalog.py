"""Phase 27C — Tests for kappa_solar_system.json and SolarSystemCatalog.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = (
    REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
)
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"


# ---------------------------------------------------------------------------
# kappa_solar_system.json
# ---------------------------------------------------------------------------

class TestKappaSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS_DIR / "kappa_solar_system.json").exists())


class TestKappaSolarSystemStructure(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (SOLAR_SYSTEMS_DIR / "kappa_solar_system.json").read_text()
        )

    def test_id_field(self):
        self.assertIn("id", self.data)

    def test_id_starts_with_kappa(self):
        self.assertTrue(self.data["id"].startswith("kappa_solar_system"))

    def test_name_field(self):
        self.assertIn("name", self.data)

    def test_star_field(self):
        self.assertIn("star", self.data)

    def test_star_has_type(self):
        self.assertIn("type", self.data["star"])

    def test_star_type_o5v(self):
        self.assertEqual(self.data["star"]["type"], "O5V")

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

    def test_version_field(self):
        self.assertIn("version", self.data)


class TestKappaSolarSystemCelestialTypes(unittest.TestCase):
    def setUp(self):
        data = json.loads(
            (SOLAR_SYSTEMS_DIR / "kappa_solar_system.json").read_text()
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

    def test_has_gas_giant_or_asteroid_or_nebula(self):
        self.assertTrue(
            "GasGiant" in self.types
            or "AsteroidBelt" in self.types
            or "Nebula" in self.types
        )


class TestAllTenSolarSystemsDistinct(unittest.TestCase):
    _FILES = [
        "dev_solar_system.json",
        "beta_solar_system.json",
        "gamma_solar_system.json",
        "delta_solar_system.json",
        "epsilon_solar_system.json",
        "zeta_solar_system.json",
        "eta_solar_system.json",
        "theta_solar_system.json",
        "iota_solar_system.json",
        "kappa_solar_system.json",
    ]

    def test_all_files_exist(self):
        for fname in self._FILES:
            with self.subTest(file=fname):
                self.assertTrue((SOLAR_SYSTEMS_DIR / fname).exists())

    def test_all_ids_unique(self):
        ids = []
        for fname in self._FILES:
            data = json.loads((SOLAR_SYSTEMS_DIR / fname).read_text())
            ids.append(data["id"])
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_names_unique(self):
        names = []
        for fname in self._FILES:
            data = json.loads((SOLAR_SYSTEMS_DIR / fname).read_text())
            names.append(data["name"])
        self.assertEqual(len(names), len(set(names)))

    def test_all_pcg_seeds_unique(self):
        seeds = []
        for fname in self._FILES:
            data = json.loads((SOLAR_SYSTEMS_DIR / fname).read_text())
            if "pcg_config" in data and "seed" in data["pcg_config"]:
                seeds.append(data["pcg_config"]["seed"])
        self.assertEqual(len(seeds), len(set(seeds)))


# ---------------------------------------------------------------------------
# SolarSystemCatalog.h
# ---------------------------------------------------------------------------

def _read_catalog() -> str:
    return (SCENE_DIR / "SolarSystemCatalog.h").read_text()


class TestSolarSystemCatalogExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemCatalog.h").exists())


class TestSolarSystemCatalogStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_catalog())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_catalog())

    def test_class_declaration(self):
        self.assertIn("SolarSystemCatalog", _read_catalog())

    def test_star_class_enum(self):
        self.assertIn("StarClass", _read_catalog())

    def test_system_status_enum(self):
        self.assertIn("SystemStatus", _read_catalog())

    def test_system_hazard_enum(self):
        self.assertIn("SystemHazard", _read_catalog())

    def test_faction_alignment_enum(self):
        self.assertIn("FactionAlignment", _read_catalog())

    def test_system_coordinates_struct(self):
        self.assertIn("SystemCoordinates", _read_catalog())

    def test_trade_route_struct(self):
        self.assertIn("TradeRoute", _read_catalog())

    def test_system_catalog_entry_struct(self):
        self.assertIn("SystemCatalogEntry", _read_catalog())


class TestSolarSystemCatalogAPI(unittest.TestCase):
    def test_register_system(self):
        self.assertIn("RegisterSystem", _read_catalog())

    def test_unregister_system(self):
        self.assertIn("UnregisterSystem", _read_catalog())

    def test_set_system_status(self):
        self.assertIn("SetSystemStatus", _read_catalog())

    def test_set_system_hazard(self):
        self.assertIn("SetSystemHazard", _read_catalog())

    def test_set_faction_alignment(self):
        self.assertIn("SetFactionAlignment", _read_catalog())

    def test_find_by_star_class(self):
        self.assertIn("FindByStarClass", _read_catalog())

    def test_find_by_status(self):
        self.assertIn("FindByStatus", _read_catalog())

    def test_find_by_faction(self):
        self.assertIn("FindByFaction", _read_catalog())

    def test_find_by_ore_type(self):
        self.assertIn("FindByOreType", _read_catalog())

    def test_find_connected_to(self):
        self.assertIn("FindConnectedTo", _read_catalog())

    def test_find_shortest_path(self):
        self.assertIn("FindShortestPath", _read_catalog())

    def test_find_safest_path(self):
        self.assertIn("FindSafestPath", _read_catalog())

    def test_register_trade_route(self):
        self.assertIn("RegisterTradeRoute", _read_catalog())

    def test_get_distance_ly(self):
        self.assertIn("GetDistanceLY", _read_catalog())

    def test_save_catalog(self):
        self.assertIn("SaveCatalog", _read_catalog())

    def test_clear_method(self):
        self.assertIn("Clear", _read_catalog())


if __name__ == "__main__":
    unittest.main()
