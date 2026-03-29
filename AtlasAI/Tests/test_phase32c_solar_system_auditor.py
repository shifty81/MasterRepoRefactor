"""Phase 32C — Tests for omicron_solar_system.json and SolarSystemAuditor.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

OMICRON_JSON = SOLAR_SYSTEMS_DIR / "omicron_solar_system.json"
AUDITOR_H = SCENE_DIR / "SolarSystemAuditor.h"


def _read_auditor() -> str:
    return AUDITOR_H.read_text()


def _load_omicron() -> dict:
    with OMICRON_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# omicron_solar_system.json
# ---------------------------------------------------------------------------

class TestOmicronSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(OMICRON_JSON.exists())


class TestOmicronSolarSystemStructure(unittest.TestCase):
    def test_id_field(self):
        data = _load_omicron()
        self.assertEqual(data["id"], "omicron_solar_system_001")

    def test_name_field(self):
        data = _load_omicron()
        name = data.get("name", "")
        self.assertTrue("Omicron" in name or "omicron" in name)

    def test_version_field(self):
        data = _load_omicron()
        self.assertIn("version", data)

    def test_star_type_k7v(self):
        data = _load_omicron()
        self.assertEqual(data["star"]["type"], "K7V")

    def test_star_luminosity(self):
        data = _load_omicron()
        self.assertAlmostEqual(data["star"]["luminosity"], 0.22, delta=0.1)

    def test_star_radius(self):
        data = _load_omicron()
        self.assertIn("radius", data["star"])

    def test_total_celestials_8(self):
        data = _load_omicron()
        self.assertEqual(data["total_celestials"], 8)

    def test_celestials_list_count(self):
        data = _load_omicron()
        self.assertEqual(len(data["celestials"]), 8)

    def test_has_npc_factions(self):
        data = _load_omicron()
        self.assertIn("npc_factions", data)
        self.assertIsInstance(data["npc_factions"], list)

    def test_has_pcg_config(self):
        data = _load_omicron()
        self.assertIn("pcg_config", data)

    def test_pcg_seed_present(self):
        data = _load_omicron()
        self.assertIn("seed", data["pcg_config"])

    def test_has_hazards(self):
        data = _load_omicron()
        self.assertIn("hazards", data)
        self.assertIsInstance(data["hazards"], list)

    def test_celestials_have_ids(self):
        data = _load_omicron()
        for c in data["celestials"]:
            self.assertIn("id", c)

    def test_celestials_have_types(self):
        data = _load_omicron()
        for c in data["celestials"]:
            self.assertIn("type", c)

    def test_has_planet(self):
        data = _load_omicron()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Planet", types)

    def test_has_gas_giant(self):
        data = _load_omicron()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("GasGiant", types)

    def test_has_station(self):
        data = _load_omicron()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Station", types)


# ---------------------------------------------------------------------------
# SolarSystemAuditor.h
# ---------------------------------------------------------------------------

class TestSolarSystemAuditorExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(AUDITOR_H.exists())


class TestSolarSystemAuditorStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_auditor())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_auditor())

    def test_class_declaration(self):
        self.assertIn("SolarSystemAuditor", _read_auditor())

    def test_audit_state_enum(self):
        self.assertIn("AuditState", _read_auditor())

    def test_audit_severity_enum(self):
        self.assertIn("AuditSeverity", _read_auditor())

    def test_check_category_enum(self):
        self.assertIn("CheckCategory", _read_auditor())

    def test_audit_finding_struct(self):
        self.assertIn("AuditFinding", _read_auditor())

    def test_audit_rule_struct(self):
        self.assertIn("AuditRule", _read_auditor())

    def test_audit_report_struct(self):
        self.assertIn("AuditReport", _read_auditor())

    def test_register_rule(self):
        self.assertIn("RegisterRule", _read_auditor())

    def test_unregister_rule(self):
        self.assertIn("UnregisterRule", _read_auditor())

    def test_get_rule(self):
        self.assertIn("GetRule", _read_auditor())

    def test_get_all_rule_ids(self):
        self.assertIn("GetAllRuleIds", _read_auditor())

    def test_run_audit(self):
        self.assertIn("RunAudit", _read_auditor())

    def test_pause_audit(self):
        self.assertIn("PauseAudit", _read_auditor())

    def test_get_report(self):
        self.assertIn("GetReport", _read_auditor())

    def test_get_finding(self):
        self.assertIn("GetFinding", _read_auditor())

    def test_get_findings_by_severity(self):
        self.assertIn("GetFindingsBySeverity", _read_auditor())

    def test_get_findings_by_category(self):
        self.assertIn("GetFindingsByCategory", _read_auditor())

    def test_auto_fix(self):
        self.assertIn("AutoFix", _read_auditor())

    def test_get_pass_rate(self):
        self.assertIn("GetPassRate", _read_auditor())

    def test_export_report(self):
        self.assertIn("ExportReport", _read_auditor())

    def test_clear_findings(self):
        self.assertIn("ClearFindings", _read_auditor())

    def test_reset_method(self):
        self.assertIn("Reset", _read_auditor())

    def test_functional_include(self):
        self.assertIn("<functional>", _read_auditor())


if __name__ == "__main__":
    unittest.main()
