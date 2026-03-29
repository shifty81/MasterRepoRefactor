"""Phase 28C — Tests for lambda_solar_system.json and SolarSystemProfiler.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

LAMBDA_JSON = SOLAR_SYSTEMS_DIR / "lambda_solar_system.json"
PROFILER_H = SCENE_DIR / "SolarSystemProfiler.h"


def _load_lambda() -> dict:
    return json.loads(LAMBDA_JSON.read_text())


def _read_profiler() -> str:
    return PROFILER_H.read_text()


# ---------------------------------------------------------------------------
# Lambda Solar System JSON
# ---------------------------------------------------------------------------

class TestLambdaSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(LAMBDA_JSON.exists())


class TestLambdaSolarSystemStructure(unittest.TestCase):
    def test_id_field(self):
        data = _load_lambda()
        self.assertEqual(data["id"], "lambda_solar_system_001")

    def test_name_field(self):
        data = _load_lambda()
        self.assertIn("Lambda", data["name"])

    def test_version_field(self):
        data = _load_lambda()
        self.assertIn("version", data)

    def test_star_type_a2v(self):
        data = _load_lambda()
        self.assertEqual(data["star"]["type"], "A2V")

    def test_star_luminosity_around_50(self):
        data = _load_lambda()
        self.assertAlmostEqual(data["star"]["luminosity"], 50.0, delta=10.0)

    def test_star_radius(self):
        data = _load_lambda()
        self.assertGreater(data["star"]["radius"], 1000000)

    def test_total_celestials_8(self):
        data = _load_lambda()
        self.assertEqual(data["total_celestials"], 8)

    def test_celestials_list_count(self):
        data = _load_lambda()
        self.assertEqual(len(data["celestials"]), 8)

    def test_has_npc_factions(self):
        data = _load_lambda()
        self.assertIn("npc_factions", data)
        self.assertGreaterEqual(len(data["npc_factions"]), 2)

    def test_has_pcg_config(self):
        data = _load_lambda()
        self.assertIn("pcg_config", data)

    def test_pcg_seed_present(self):
        data = _load_lambda()
        self.assertIn("seed", data["pcg_config"])

    def test_has_hazards(self):
        data = _load_lambda()
        self.assertIn("hazards", data)
        self.assertGreaterEqual(len(data["hazards"]), 1)

    def test_celestials_have_ids(self):
        data = _load_lambda()
        for c in data["celestials"]:
            self.assertIn("id", c)

    def test_celestials_have_types(self):
        data = _load_lambda()
        for c in data["celestials"]:
            self.assertIn("type", c)

    def test_has_planet(self):
        data = _load_lambda()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Planet", types)

    def test_has_gas_giant(self):
        data = _load_lambda()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("GasGiant", types)

    def test_has_asteroid_belt(self):
        data = _load_lambda()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("AsteroidBelt", types)

    def test_has_station(self):
        data = _load_lambda()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Station", types)


# ---------------------------------------------------------------------------
# SolarSystemProfiler.h
# ---------------------------------------------------------------------------

class TestSolarSystemProfilerExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(PROFILER_H.exists())


class TestSolarSystemProfilerStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_profiler())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _read_profiler())

    def test_class_declaration(self):
        self.assertIn("SolarSystemProfiler", _read_profiler())

    def test_profiler_state_enum(self):
        self.assertIn("ProfilerState", _read_profiler())

    def test_metric_category_enum(self):
        self.assertIn("MetricCategory", _read_profiler())

    def test_sample_resolution_enum(self):
        self.assertIn("SampleResolution", _read_profiler())

    def test_profile_metric_struct(self):
        self.assertIn("ProfileMetric", _read_profiler())

    def test_system_load_snapshot_struct(self):
        self.assertIn("SystemLoadSnapshot", _read_profiler())

    def test_profile_session_struct(self):
        self.assertIn("ProfileSession", _read_profiler())

    def test_profile_record_struct(self):
        self.assertIn("ProfileRecord", _read_profiler())

    def test_register_method(self):
        self.assertIn("RegisterRecord", _read_profiler())

    def test_find_method(self):
        self.assertIn("FindRecord", _read_profiler())

    def test_list_ids_method(self):
        self.assertIn("ListRecordIds", _read_profiler())

    def test_has_method(self):
        self.assertIn("HasRecord", _read_profiler())

    def test_remove_method(self):
        self.assertIn("RemoveRecord", _read_profiler())

    def test_count_method(self):
        self.assertIn("Count()", _read_profiler())

    def test_clear_method(self):
        self.assertIn("Clear()", _read_profiler())

    def test_start_profiling_method(self):
        self.assertIn("StartProfiling", _read_profiler())

    def test_run_analysis_method(self):
        self.assertIn("RunAnalysis", _read_profiler())

    def test_take_snapshot_method(self):
        self.assertIn("TakeSnapshot", _read_profiler())

    def test_get_bottleneck_metrics(self):
        self.assertIn("GetBottleneckMetrics", _read_profiler())

    def test_8_plus_fields_in_record(self):
        content = _read_profiler()
        # ProfileRecord struct contains 8+ fields
        self.assertIn("recordId", content)
        self.assertIn("systemId", content)
        self.assertIn("systemName", content)
        self.assertIn("state", content)
        self.assertIn("session", content)
        self.assertIn("metrics", content)
        self.assertIn("totalSamples", content)
        self.assertIn("analysisComplete", content)

    def test_functional_include(self):
        self.assertIn("<functional>", _read_profiler())


if __name__ == "__main__":
    unittest.main()
