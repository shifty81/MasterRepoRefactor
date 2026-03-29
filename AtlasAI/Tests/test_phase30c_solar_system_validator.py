"""Phase 30C — Tests for nu_solar_system.json and SolarSystemValidator.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

NU_JSON = SOLAR_SYSTEMS_DIR / "nu_solar_system.json"
VALIDATOR_H = SCENE_DIR / "SolarSystemValidator.h"


def _load_nu() -> dict:
    return json.loads(NU_JSON.read_text())


def _read_validator() -> str:
    return VALIDATOR_H.read_text()


# ---------------------------------------------------------------------------
# Nu Solar System JSON
# ---------------------------------------------------------------------------

class TestNuSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(NU_JSON.exists())


class TestNuSolarSystemStructure(unittest.TestCase):
    def test_id_field(self):
        data = _load_nu()
        self.assertEqual(data["id"], "nu_solar_system_001")

    def test_name_field(self):
        data = _load_nu()
        self.assertIn("Nu", data["name"])

    def test_version_field(self):
        data = _load_nu()
        self.assertIn("version", data)

    def test_star_type_g8v(self):
        data = _load_nu()
        self.assertEqual(data["star"]["type"], "G8V")

    def test_star_luminosity_around_22(self):
        data = _load_nu()
        self.assertAlmostEqual(data["star"]["luminosity"], 22.0, delta=10)

    def test_star_radius(self):
        data = _load_nu()
        self.assertGreater(data["star"]["radius"], 1000000)

    def test_total_celestials_8(self):
        data = _load_nu()
        self.assertEqual(data["total_celestials"], 8)

    def test_celestials_list_count(self):
        data = _load_nu()
        self.assertEqual(len(data["celestials"]), 8)

    def test_has_npc_factions(self):
        data = _load_nu()
        self.assertIn("npc_factions", data)
        self.assertGreaterEqual(len(data["npc_factions"]), 2)

    def test_has_pcg_config(self):
        data = _load_nu()
        self.assertIn("pcg_config", data)

    def test_pcg_seed_present(self):
        data = _load_nu()
        self.assertIn("seed", data["pcg_config"])

    def test_has_hazards(self):
        data = _load_nu()
        self.assertIn("hazards", data)
        self.assertGreaterEqual(len(data["hazards"]), 1)

    def test_celestials_have_ids(self):
        data = _load_nu()
        for c in data["celestials"]:
            self.assertIn("id", c)

    def test_celestials_have_types(self):
        data = _load_nu()
        for c in data["celestials"]:
            self.assertIn("type", c)

    def test_has_planet(self):
        data = _load_nu()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Planet", types)

    def test_has_gas_giant(self):
        data = _load_nu()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("GasGiant", types)

    def test_has_asteroid_belt(self):
        data = _load_nu()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("AsteroidBelt", types)

    def test_has_station(self):
        data = _load_nu()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Station", types)


# ---------------------------------------------------------------------------
# SolarSystemValidator.h
# ---------------------------------------------------------------------------

class TestSolarSystemValidatorExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(VALIDATOR_H.exists())


class TestSolarSystemValidatorStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_validator())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_validator())

    def test_class_declaration(self):
        self.assertIn("SolarSystemValidator", _read_validator())

    def test_validation_severity_enum(self):
        self.assertIn("ValidationSeverity", _read_validator())

    def test_validation_category_enum(self):
        self.assertIn("ValidationCategory", _read_validator())

    def test_validation_state_enum(self):
        self.assertIn("ValidationState", _read_validator())

    def test_validation_issue_struct(self):
        self.assertIn("ValidationIssue", _read_validator())

    def test_validation_report_struct(self):
        self.assertIn("ValidationReport", _read_validator())

    def test_validation_rule_struct(self):
        self.assertIn("ValidationRule", _read_validator())

    def test_register_rule(self):
        self.assertIn("RegisterRule", _read_validator())

    def test_unregister_rule(self):
        self.assertIn("UnregisterRule", _read_validator())

    def test_validate_system(self):
        self.assertIn("ValidateSystem", _read_validator())

    def test_get_report(self):
        self.assertIn("GetReport", _read_validator())

    def test_get_all_reports(self):
        self.assertIn("GetAllReports", _read_validator())

    def test_get_issues_by_category(self):
        self.assertIn("GetIssuesByCategory", _read_validator())

    def test_get_issues_by_severity(self):
        self.assertIn("GetIssuesBySeverity", _read_validator())

    def test_clear_reports(self):
        self.assertIn("ClearReports", _read_validator())

    def test_export_report(self):
        self.assertIn("ExportReport", _read_validator())

    def test_is_system_valid(self):
        self.assertIn("IsSystemValid", _read_validator())

    def test_get_validation_state(self):
        self.assertIn("GetValidationState", _read_validator())

    def test_functional_include(self):
        self.assertIn("<functional>", _read_validator())


if __name__ == "__main__":
    unittest.main()
