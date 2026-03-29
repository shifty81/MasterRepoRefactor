"""Phase 31C — Tests for xi_solar_system.json and SolarSystemProfiler.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS = REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

XI_JSON = SOLAR_SYSTEMS / "xi_solar_system.json"
PROFILER_H = SCENE_DIR / "SolarSystemProfiler.h"


def _read_json() -> dict:
    with XI_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


def _read_profiler() -> str:
    return PROFILER_H.read_text()


# ---------------------------------------------------------------------------
# xi_solar_system.json
# ---------------------------------------------------------------------------

class TestXiSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(XI_JSON.exists())


class TestXiSolarSystemStructure(unittest.TestCase):
    def test_id_field(self):
        self.assertEqual(_read_json()["id"], "xi_solar_system_001")

    def test_name_field(self):
        self.assertIn("Xi", _read_json()["name"])

    def test_version_field(self):
        self.assertIn("version", _read_json())

    def test_star_type_a2v(self):
        self.assertEqual(_read_json()["star"]["type"], "A2V")

    def test_star_luminosity(self):
        self.assertAlmostEqual(_read_json()["star"]["luminosity"], 35.0, delta=10)

    def test_star_radius(self):
        self.assertGreater(_read_json()["star"]["radius"], 0)

    def test_total_celestials_8(self):
        self.assertEqual(_read_json()["total_celestials"], 8)

    def test_celestials_list_count(self):
        self.assertEqual(len(_read_json()["celestials"]), 8)

    def test_has_npc_factions(self):
        self.assertIn("npc_factions", _read_json())

    def test_has_pcg_config(self):
        self.assertIn("pcg_config", _read_json())

    def test_pcg_seed_present(self):
        self.assertIn("seed", _read_json()["pcg_config"])

    def test_has_hazards(self):
        self.assertIn("hazards", _read_json())

    def test_celestials_have_ids(self):
        for c in _read_json()["celestials"]:
            self.assertIn("id", c)

    def test_celestials_have_types(self):
        for c in _read_json()["celestials"]:
            self.assertIn("type", c)

    def test_has_planet(self):
        types = [c["type"] for c in _read_json()["celestials"]]
        self.assertIn("Planet", types)

    def test_has_gas_giant(self):
        types = [c["type"] for c in _read_json()["celestials"]]
        self.assertIn("GasGiant", types)

    def test_has_asteroid_belt(self):
        types = [c["type"] for c in _read_json()["celestials"]]
        self.assertIn("AsteroidBelt", types)

    def test_has_station(self):
        types = [c["type"] for c in _read_json()["celestials"]]
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

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_profiler())

    def test_class_declaration(self):
        self.assertIn("SolarSystemProfiler", _read_profiler())

    def test_profiler_state_enum(self):
        self.assertIn("ProfilerState", _read_profiler())

    def test_metric_category_enum(self):
        self.assertIn("MetricCategory", _read_profiler())

    def test_sampling_mode_enum(self):
        self.assertIn("SamplingMode", _read_profiler())

    def test_profile_sample_struct(self):
        self.assertIn("ProfileSample", _read_profiler())

    def test_metric_series_struct(self):
        self.assertIn("MetricSeries", _read_profiler())

    def test_profiler_config_struct(self):
        self.assertIn("ProfilerConfig", _read_profiler())

    def test_start_profiling(self):
        self.assertIn("StartProfiling", _read_profiler())

    def test_stop_profiling(self):
        self.assertIn("StopProfiling", _read_profiler())

    def test_record_sample(self):
        self.assertIn("RecordSample", _read_profiler())

    def test_record_series(self):
        self.assertIn("RecordSeries", _read_profiler())

    def test_get_sample(self):
        self.assertIn("GetSample", _read_profiler())

    def test_get_series(self):
        self.assertIn("GetSeries", _read_profiler())

    def test_get_series_by_category(self):
        self.assertIn("GetSeriesByCategory", _read_profiler())

    def test_detect_bottlenecks(self):
        self.assertIn("DetectBottlenecks", _read_profiler())

    def test_export_profile(self):
        self.assertIn("ExportProfile", _read_profiler())

    def test_clear_samples(self):
        self.assertIn("ClearSamples", _read_profiler())

    def test_reset_method(self):
        self.assertIn("Reset", _read_profiler())

    def test_functional_include(self):
        self.assertIn("#include <functional>", _read_profiler())


if __name__ == "__main__":
    unittest.main()
