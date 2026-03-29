"""Phase 20C — Tests for gamma_solar_system.json and SolarSystemLinker.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = (
    REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
)
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"


# ---------------------------------------------------------------------------
# gamma_solar_system.json
# ---------------------------------------------------------------------------

class TestGammaSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS_DIR / "gamma_solar_system.json").exists())


class TestGammaSolarSystemStructure(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (SOLAR_SYSTEMS_DIR / "gamma_solar_system.json").read_text()
        )

    def test_id_field(self):
        self.assertIn("id", self.data)

    def test_id_starts_with_gamma(self):
        self.assertTrue(self.data["id"].startswith("gamma_solar_system"))

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


class TestGammaSolarSystemCelestialTypes(unittest.TestCase):
    def setUp(self):
        data = json.loads(
            (SOLAR_SYSTEMS_DIR / "gamma_solar_system.json").read_text()
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

    def test_celestial_ids_unique(self):
        ids = [c["id"] for c in self.celestials]
        self.assertEqual(len(ids), len(set(ids)))

    def test_each_celestial_has_orbit_radius(self):
        for c in self.celestials:
            self.assertIn("orbit_radius", c)


class TestAllThreeSolarSystemsDistinct(unittest.TestCase):
    def _load_id(self, fname: str) -> str:
        return json.loads((SOLAR_SYSTEMS_DIR / fname).read_text())["id"]

    def test_dev_still_valid(self):
        data = json.loads((SOLAR_SYSTEMS_DIR / "dev_solar_system.json").read_text())
        self.assertIn("id", data)

    def test_beta_still_valid(self):
        data = json.loads((SOLAR_SYSTEMS_DIR / "beta_solar_system.json").read_text())
        self.assertIn("id", data)

    def test_gamma_valid(self):
        data = json.loads((SOLAR_SYSTEMS_DIR / "gamma_solar_system.json").read_text())
        self.assertIn("id", data)

    def test_all_ids_unique(self):
        ids = [
            self._load_id("dev_solar_system.json"),
            self._load_id("beta_solar_system.json"),
            self._load_id("gamma_solar_system.json"),
        ]
        self.assertEqual(len(ids), len(set(ids)))


# ---------------------------------------------------------------------------
# SolarSystemLinker.h
# ---------------------------------------------------------------------------

def _linker() -> str:
    return (SCENE_DIR / "SolarSystemLinker.h").read_text()


class TestSolarSystemLinkerExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemLinker.h").exists())


class TestSolarSystemLinkerHeader(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _linker())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _linker())

    def test_class_declared(self):
        self.assertIn("class SolarSystemLinker", _linker())


class TestSolarSystemLinkerAPI(unittest.TestCase):
    def test_add_link(self):
        self.assertIn("AddLink", _linker())

    def test_remove_link(self):
        self.assertIn("RemoveLink", _linker())

    def test_has_link(self):
        self.assertIn("HasLink", _linker())

    def test_get_link_count(self):
        self.assertIn("GetLinkCount", _linker())

    def test_get_link(self):
        self.assertIn("GetLink", _linker())

    def test_get_links_from(self):
        self.assertIn("GetLinksFrom", _linker())

    def test_get_links_to(self):
        self.assertIn("GetLinksTo", _linker())

    def test_get_reachable_systems(self):
        self.assertIn("GetReachableSystems", _linker())

    def test_find_path(self):
        self.assertIn("FindPath", _linker())

    def test_clear(self):
        self.assertIn("Clear", _linker())

    def test_set_on_link_changed_callback(self):
        self.assertIn("SetOnLinkChangedCallback", _linker())


class TestSolarSystemLinkerSystemLinkStruct(unittest.TestCase):
    def test_system_link_struct(self):
        self.assertIn("SystemLink", _linker())

    def test_link_id_field(self):
        self.assertIn("linkId", _linker())

    def test_from_system_id_field(self):
        self.assertIn("fromSystemId", _linker())

    def test_to_system_id_field(self):
        self.assertIn("toSystemId", _linker())

    def test_bidirectional_field(self):
        self.assertIn("bidirectional", _linker())

    def test_link_type_field(self):
        self.assertIn("linkType", _linker())


if __name__ == "__main__":
    unittest.main()
