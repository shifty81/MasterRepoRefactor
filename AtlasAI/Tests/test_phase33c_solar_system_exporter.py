"""Phase 33C — Tests for pi_solar_system.json and SolarSystemExporter.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

PI_JSON = SOLAR_SYSTEMS_DIR / "pi_solar_system.json"
EXPORTER_H = SCENE_DIR / "SolarSystemExporter.h"


def _read_exporter() -> str:
    return EXPORTER_H.read_text()


def _load_pi() -> dict:
    with PI_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# pi_solar_system.json
# ---------------------------------------------------------------------------

class TestPiSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(PI_JSON.exists())


class TestPiSolarSystemStructure(unittest.TestCase):
    def test_id_field(self):
        data = _load_pi()
        self.assertEqual(data["id"], "pi_solar_system_001")

    def test_name_field(self):
        data = _load_pi()
        name = data.get("name", "")
        self.assertTrue("Pi" in name or "pi" in name)

    def test_version_field(self):
        data = _load_pi()
        self.assertIn("version", data)

    def test_star_type_m2v(self):
        data = _load_pi()
        self.assertEqual(data["star"]["type"], "M2V")

    def test_star_luminosity(self):
        data = _load_pi()
        self.assertAlmostEqual(data["star"]["luminosity"], 0.04, delta=0.05)

    def test_star_radius(self):
        data = _load_pi()
        self.assertIn("radius", data["star"])

    def test_total_celestials_8(self):
        data = _load_pi()
        self.assertEqual(data["total_celestials"], 8)

    def test_celestials_list_count(self):
        data = _load_pi()
        self.assertEqual(len(data["celestials"]), 8)

    def test_has_npc_factions(self):
        data = _load_pi()
        self.assertIn("npc_factions", data)
        self.assertIsInstance(data["npc_factions"], list)

    def test_has_pcg_config(self):
        data = _load_pi()
        self.assertIn("pcg_config", data)

    def test_pcg_seed_present(self):
        data = _load_pi()
        self.assertIn("seed", data["pcg_config"])

    def test_has_hazards(self):
        data = _load_pi()
        self.assertIn("hazards", data)
        self.assertIsInstance(data["hazards"], list)

    def test_celestials_have_ids(self):
        data = _load_pi()
        for c in data["celestials"]:
            self.assertIn("id", c)

    def test_celestials_have_types(self):
        data = _load_pi()
        for c in data["celestials"]:
            self.assertIn("type", c)

    def test_has_planet(self):
        data = _load_pi()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Planet", types)

    def test_has_gas_giant(self):
        data = _load_pi()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("GasGiant", types)

    def test_has_station(self):
        data = _load_pi()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Station", types)


# ---------------------------------------------------------------------------
# SolarSystemExporter.h
# ---------------------------------------------------------------------------

class TestSolarSystemExporterExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(EXPORTER_H.exists())


class TestSolarSystemExporterStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_exporter())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_exporter())

    def test_class_declaration(self):
        self.assertIn("SolarSystemExporter", _read_exporter())

    def test_export_state_enum(self):
        self.assertIn("ExportState", _read_exporter())

    def test_export_format_enum(self):
        self.assertIn("ExportFormat", _read_exporter())

    def test_export_target_enum(self):
        self.assertIn("ExportTarget", _read_exporter())

    def test_export_filter_struct(self):
        self.assertIn("ExportFilter", _read_exporter())

    def test_export_manifest_struct(self):
        self.assertIn("ExportManifest", _read_exporter())

    def test_export_result_struct(self):
        self.assertIn("ExportResult", _read_exporter())

    def test_register_exporter(self):
        self.assertIn("RegisterExporter", _read_exporter())

    def test_create_manifest(self):
        self.assertIn("CreateManifest", _read_exporter())

    def test_get_manifest(self):
        self.assertIn("GetManifest", _read_exporter())

    def test_get_all_manifest_ids(self):
        self.assertIn("GetAllManifestIds", _read_exporter())

    def test_set_export_format(self):
        self.assertIn("SetExportFormat", _read_exporter())

    def test_set_export_target(self):
        self.assertIn("SetExportTarget", _read_exporter())

    def test_set_output_path(self):
        self.assertIn("SetOutputPath", _read_exporter())

    def test_export_method(self):
        self.assertIn("Export", _read_exporter())

    def test_export_async_method(self):
        self.assertIn("ExportAsync", _read_exporter())

    def test_cancel_export(self):
        self.assertIn("CancelExport", _read_exporter())

    def test_get_result(self):
        self.assertIn("GetResult", _read_exporter())

    def test_get_export_state(self):
        self.assertIn("GetExportState", _read_exporter())

    def test_validate_manifest(self):
        self.assertIn("ValidateManifest", _read_exporter())

    def test_list_formats(self):
        self.assertIn("ListFormats", _read_exporter())

    def test_list_targets(self):
        self.assertIn("ListTargets", _read_exporter())

    def test_clear_results(self):
        self.assertIn("ClearResults", _read_exporter())

    def test_reset_method(self):
        self.assertIn("Reset", _read_exporter())

    def test_functional_include(self):
        self.assertIn("<functional>", _read_exporter())


if __name__ == "__main__":
    unittest.main()
