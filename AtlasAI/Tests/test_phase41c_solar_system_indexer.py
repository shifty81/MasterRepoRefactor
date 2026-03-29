"""Phase 41C — Tests for omega_solar_system.json and SolarSystemIndexer.h."""
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
# omega_solar_system.json
# ---------------------------------------------------------------------------

class TestOmegaSolarSystemJson(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS / "omega_solar_system.json").exists())

    def test_has_id(self):
        data = _load_json("omega_solar_system")
        self.assertIn("id", data)
        self.assertIn("omega", data["id"])

    def test_has_name(self):
        data = _load_json("omega_solar_system")
        self.assertIn("name", data)
        self.assertIn("Omega", data["name"])

    def test_has_star(self):
        data = _load_json("omega_solar_system")
        self.assertIn("star", data)

    def test_star_type_f1v(self):
        data = _load_json("omega_solar_system")
        self.assertEqual(data["star"]["type"], "F1V")

    def test_has_celestials(self):
        data = _load_json("omega_solar_system")
        self.assertIn("celestials", data)

    def test_total_celestials_8(self):
        data = _load_json("omega_solar_system")
        self.assertEqual(data["total_celestials"], 8)

    def test_celestials_count_8(self):
        data = _load_json("omega_solar_system")
        self.assertEqual(len(data["celestials"]), 8)

    def test_has_habitable_planet(self):
        data = _load_json("omega_solar_system")
        habitable = [c for c in data["celestials"] if c.get("habitable", False)]
        self.assertGreaterEqual(len(habitable), 1)

    def test_has_gas_giant(self):
        data = _load_json("omega_solar_system")
        gas_giants = [c for c in data["celestials"] if c.get("type") == "GasGiant"]
        self.assertEqual(len(gas_giants), 1)

    def test_has_station(self):
        data = _load_json("omega_solar_system")
        stations = [c for c in data["celestials"] if c.get("type") == "Station"]
        self.assertEqual(len(stations), 1)

    def test_has_anomaly(self):
        data = _load_json("omega_solar_system")
        anomalies = [c for c in data["celestials"] if c.get("type") == "Anomaly"]
        self.assertEqual(len(anomalies), 1)

    def test_has_moon(self):
        data = _load_json("omega_solar_system")
        moons = [c for c in data["celestials"] if c.get("type") == "Moon"]
        self.assertGreaterEqual(len(moons), 1)

    def test_has_npc_factions(self):
        data = _load_json("omega_solar_system")
        self.assertIn("npc_factions", data)
        self.assertGreaterEqual(len(data["npc_factions"]), 1)

    def test_has_pcg_config(self):
        data = _load_json("omega_solar_system")
        self.assertIn("pcg_config", data)

    def test_pcg_config_seed(self):
        data = _load_json("omega_solar_system")
        self.assertIn("seed", data["pcg_config"])

    def test_has_version(self):
        data = _load_json("omega_solar_system")
        self.assertIn("version", data)

    def test_habitable_has_atmosphere(self):
        data = _load_json("omega_solar_system")
        habitable = [c for c in data["celestials"] if c.get("habitable", False)]
        for h in habitable:
            self.assertIn("atmosphere", h)

    def test_star_has_luminosity(self):
        data = _load_json("omega_solar_system")
        self.assertIn("luminosity", data["star"])

    def test_star_has_temperature(self):
        data = _load_json("omega_solar_system")
        self.assertIn("temperature", data["star"])


# ---------------------------------------------------------------------------
# SolarSystemIndexer.h
# ---------------------------------------------------------------------------

class TestSolarSystemIndexerHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemIndexer.h").exists())


class TestSolarSystemIndexerNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("SolarSystemIndexer"))


class TestSolarSystemIndexerEnums(unittest.TestCase):
    def test_index_state_enum(self):
        self.assertIn("IndexState", _read_header("SolarSystemIndexer"))

    def test_asset_category_enum(self):
        self.assertIn("AssetCategory", _read_header("SolarSystemIndexer"))

    def test_search_scope_enum(self):
        self.assertIn("SearchScope", _read_header("SolarSystemIndexer"))

    def test_index_sort_order_enum(self):
        self.assertIn("IndexSortOrder", _read_header("SolarSystemIndexer"))

    def test_unindexed_state_value(self):
        self.assertIn("Unindexed", _read_header("SolarSystemIndexer"))

    def test_indexed_state_value(self):
        self.assertIn("Indexed", _read_header("SolarSystemIndexer"))

    def test_stale_state_value(self):
        self.assertIn("Stale", _read_header("SolarSystemIndexer"))

    def test_planet_category_value(self):
        self.assertIn("Planet", _read_header("SolarSystemIndexer"))

    def test_star_category_value(self):
        self.assertIn("Star", _read_header("SolarSystemIndexer"))

    def test_global_scope_value(self):
        self.assertIn("Global", _read_header("SolarSystemIndexer"))


class TestSolarSystemIndexerStructs(unittest.TestCase):
    def test_index_entry_def_struct(self):
        self.assertIn("IndexEntryDef", _read_header("SolarSystemIndexer"))

    def test_search_query_def_struct(self):
        self.assertIn("SearchQueryDef", _read_header("SolarSystemIndexer"))

    def test_search_result_def_struct(self):
        self.assertIn("SearchResultDef", _read_header("SolarSystemIndexer"))

    def test_orbit_radius_in_entry(self):
        self.assertIn("orbitRadius", _read_header("SolarSystemIndexer"))

    def test_total_matches_in_result(self):
        self.assertIn("totalMatches", _read_header("SolarSystemIndexer"))

    def test_query_text_in_query(self):
        self.assertIn("queryText", _read_header("SolarSystemIndexer"))


class TestSolarSystemIndexerMethods(unittest.TestCase):
    def test_add_entry(self):
        self.assertIn("AddEntry", _read_header("SolarSystemIndexer"))

    def test_remove_entry(self):
        self.assertIn("RemoveEntry", _read_header("SolarSystemIndexer"))

    def test_update_entry_state(self):
        self.assertIn("UpdateEntryState", _read_header("SolarSystemIndexer"))

    def test_mark_stale(self):
        self.assertIn("MarkStale", _read_header("SolarSystemIndexer"))

    def test_reindex_entry(self):
        self.assertIn("ReindexEntry", _read_header("SolarSystemIndexer"))

    def test_get_entry(self):
        self.assertIn("GetEntry", _read_header("SolarSystemIndexer"))

    def test_get_all_entry_ids(self):
        self.assertIn("GetAllEntryIds", _read_header("SolarSystemIndexer"))

    def test_get_entries_by_system(self):
        self.assertIn("GetEntriesBySystem", _read_header("SolarSystemIndexer"))

    def test_get_entries_by_category(self):
        self.assertIn("GetEntriesByCategory", _read_header("SolarSystemIndexer"))

    def test_get_habitable_entries(self):
        self.assertIn("GetHabitableEntries", _read_header("SolarSystemIndexer"))

    def test_get_stale_entries(self):
        self.assertIn("GetStaleEntries", _read_header("SolarSystemIndexer"))

    def test_execute_search(self):
        self.assertIn("ExecuteSearch", _read_header("SolarSystemIndexer"))

    def test_save_query(self):
        self.assertIn("SaveQuery", _read_header("SolarSystemIndexer"))

    def test_get_child_assets(self):
        self.assertIn("GetChildAssets", _read_header("SolarSystemIndexer"))

    def test_has_entry(self):
        self.assertIn("HasEntry", _read_header("SolarSystemIndexer"))

    def test_reset(self):
        self.assertIn("Reset", _read_header("SolarSystemIndexer"))


if __name__ == "__main__":
    unittest.main()
