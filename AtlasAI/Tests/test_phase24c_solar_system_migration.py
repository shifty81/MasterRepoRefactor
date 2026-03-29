"""Phase 24C — Tests for eta_solar_system.json and SolarSystemMigration.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = (
    REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
)
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"


# ---------------------------------------------------------------------------
# eta_solar_system.json
# ---------------------------------------------------------------------------

class TestEtaSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS_DIR / "eta_solar_system.json").exists())


class TestEtaSolarSystemStructure(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (SOLAR_SYSTEMS_DIR / "eta_solar_system.json").read_text()
        )

    def test_id_field(self):
        self.assertIn("id", self.data)

    def test_id_starts_with_eta(self):
        self.assertTrue(self.data["id"].startswith("eta_solar_system"))

    def test_name_field(self):
        self.assertIn("name", self.data)

    def test_star_field(self):
        self.assertIn("star", self.data)

    def test_star_has_type(self):
        self.assertIn("type", self.data["star"])

    def test_star_type_m5v(self):
        self.assertEqual(self.data["star"]["type"], "M5V")

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


class TestEtaSolarSystemCelestialTypes(unittest.TestCase):
    def setUp(self):
        data = json.loads(
            (SOLAR_SYSTEMS_DIR / "eta_solar_system.json").read_text()
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


class TestAllSevenSolarSystemsDistinct(unittest.TestCase):
    _FILES = [
        "dev_solar_system.json",
        "beta_solar_system.json",
        "gamma_solar_system.json",
        "delta_solar_system.json",
        "epsilon_solar_system.json",
        "zeta_solar_system.json",
        "eta_solar_system.json",
    ]

    def _load_id(self, fname: str) -> str:
        return json.loads((SOLAR_SYSTEMS_DIR / fname).read_text())["id"]

    def test_all_files_exist(self):
        for fname in self._FILES:
            self.assertTrue((SOLAR_SYSTEMS_DIR / fname).exists(), fname)

    def test_all_ids_unique(self):
        ids = [self._load_id(f) for f in self._FILES]
        self.assertEqual(len(ids), len(set(ids)))


# ---------------------------------------------------------------------------
# SolarSystemMigration.h tests
# ---------------------------------------------------------------------------

def _mig() -> str:
    return (SCENE_DIR / "SolarSystemMigration.h").read_text()


class TestSolarSystemMigrationExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemMigration.h").exists())


class TestSolarSystemMigrationHeader(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _mig())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _mig())

    def test_class_declared(self):
        self.assertIn("class SolarSystemMigration", _mig())


class TestSolarSystemMigrationAPI(unittest.TestCase):
    def test_register_version(self):
        self.assertIn("RegisterVersion", _mig())

    def test_is_version_registered(self):
        self.assertIn("IsVersionRegistered", _mig())

    def test_get_current_schema_version(self):
        self.assertIn("GetCurrentSchemaVersion", _mig())

    def test_set_current_schema_version(self):
        self.assertIn("SetCurrentSchemaVersion", _mig())

    def test_get_min_supported_version(self):
        self.assertIn("GetMinSupportedVersion", _mig())

    def test_register_migration_step(self):
        self.assertIn("RegisterMigrationStep", _mig())

    def test_add_field_rename(self):
        self.assertIn("AddFieldRename", _mig())

    def test_add_removed_field(self):
        self.assertIn("AddRemovedField", _mig())

    def test_add_added_field(self):
        self.assertIn("AddAddedField", _mig())

    def test_migrate(self):
        self.assertIn("Migrate", _mig())

    def test_migrate_to_latest(self):
        self.assertIn("MigrateToLatest", _mig())

    def test_can_migrate(self):
        self.assertIn("CanMigrate", _mig())

    def test_get_migration_path(self):
        self.assertIn("GetMigrationPath", _mig())

    def test_has_breaking_changes(self):
        self.assertIn("HasBreakingChanges", _mig())

    def test_validate_schema(self):
        self.assertIn("ValidateSchema", _mig())

    def test_log_migration(self):
        self.assertIn("LogMigration", _mig())

    def test_get_migration_log_count(self):
        self.assertIn("GetMigrationLogCount", _mig())

    def test_clear_log(self):
        self.assertIn("ClearLog", _mig())

    def test_save_migration_log(self):
        self.assertIn("SaveMigrationLog", _mig())

    def test_clear(self):
        self.assertIn("Clear", _mig())


class TestSolarSystemMigrationStructs(unittest.TestCase):
    def test_migration_result_enum(self):
        self.assertIn("MigrationResult", _mig())

    def test_migration_direction_enum(self):
        self.assertIn("MigrationDirection", _mig())

    def test_migration_step_struct(self):
        self.assertIn("MigrationStep", _mig())

    def test_migration_report_struct(self):
        self.assertIn("MigrationReport", _mig())

    def test_field_rename_struct(self):
        self.assertIn("FieldRename", _mig())

    def test_migration_callback_typedef(self):
        self.assertIn("MigrationCallback", _mig())

    def test_breaking_change_field(self):
        self.assertIn("breakingChange", _mig())

    def test_data_loss_field(self):
        self.assertIn("dataLoss", _mig())


if __name__ == "__main__":
    unittest.main()
