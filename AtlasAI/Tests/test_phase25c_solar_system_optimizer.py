"""Phase 25C — Tests for theta_solar_system.json and SolarSystemOptimizer.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = (
    REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
)
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"


# ---------------------------------------------------------------------------
# theta_solar_system.json
# ---------------------------------------------------------------------------

class TestThetaSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS_DIR / "theta_solar_system.json").exists())


class TestThetaSolarSystemStructure(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (SOLAR_SYSTEMS_DIR / "theta_solar_system.json").read_text()
        )

    def test_id_field(self):
        self.assertIn("id", self.data)

    def test_id_starts_with_theta(self):
        self.assertTrue(self.data["id"].startswith("theta_solar_system"))

    def test_name_field(self):
        self.assertIn("name", self.data)

    def test_star_field(self):
        self.assertIn("star", self.data)

    def test_star_has_type(self):
        self.assertIn("type", self.data["star"])

    def test_star_type_k3v(self):
        self.assertEqual(self.data["star"]["type"], "K3V")

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


class TestThetaSolarSystemCelestialTypes(unittest.TestCase):
    def setUp(self):
        data = json.loads(
            (SOLAR_SYSTEMS_DIR / "theta_solar_system.json").read_text()
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

    def test_has_asteroid_belt_or_gas_giant(self):
        self.assertTrue(
            "AsteroidBelt" in self.types or "GasGiant" in self.types
        )


class TestAllEightSolarSystemsDistinct(unittest.TestCase):
    _FILES = [
        "dev_solar_system.json",
        "beta_solar_system.json",
        "gamma_solar_system.json",
        "delta_solar_system.json",
        "epsilon_solar_system.json",
        "zeta_solar_system.json",
        "eta_solar_system.json",
        "theta_solar_system.json",
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
# SolarSystemOptimizer.h
# ---------------------------------------------------------------------------

def _read_optimizer() -> str:
    return (SCENE_DIR / "SolarSystemOptimizer.h").read_text()


class TestSolarSystemOptimizerExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemOptimizer.h").exists())


class TestSolarSystemOptimizerStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_optimizer())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_optimizer())

    def test_class_declaration(self):
        self.assertIn("SolarSystemOptimizer", _read_optimizer())

    def test_optimization_target_enum(self):
        self.assertIn("OptimizationTarget", _read_optimizer())

    def test_severity_level_enum(self):
        self.assertIn("SeverityLevel", _read_optimizer())

    def test_lod_boundary_policy_enum(self):
        self.assertIn("LODBoundaryPolicy", _read_optimizer())

    def test_celestial_metrics_struct(self):
        self.assertIn("CelestialMetrics", _read_optimizer())

    def test_optimization_hint_struct(self):
        self.assertIn("OptimizationHint", _read_optimizer())

    def test_budget_thresholds_struct(self):
        self.assertIn("BudgetThresholds", _read_optimizer())

    def test_optimization_report_struct(self):
        self.assertIn("OptimizationReport", _read_optimizer())


class TestSolarSystemOptimizerAPI(unittest.TestCase):
    def test_set_budget_thresholds(self):
        self.assertIn("SetBudgetThresholds", _read_optimizer())

    def test_set_lod_boundary_policy(self):
        self.assertIn("SetLODBoundaryPolicy", _read_optimizer())

    def test_register_celestial(self):
        self.assertIn("RegisterCelestial", _read_optimizer())

    def test_unregister_celestial(self):
        self.assertIn("UnregisterCelestial", _read_optimizer())

    def test_analyse_method(self):
        self.assertIn("Analyse", _read_optimizer())

    def test_is_over_memory_budget(self):
        self.assertIn("IsOverMemoryBudget", _read_optimizer())

    def test_is_over_npc_budget(self):
        self.assertIn("IsOverNPCBudget", _read_optimizer())

    def test_get_celestials_needing_lod_increase(self):
        self.assertIn("GetCelestialsNeedingLODIncrease", _read_optimizer())

    def test_get_candidates_for_culling(self):
        self.assertIn("GetCandidatesForCulling", _read_optimizer())

    def test_recalculate_streaming_priorities(self):
        self.assertIn("RecalculateStreamingPriorities", _read_optimizer())

    def test_apply_all_hints(self):
        self.assertIn("ApplyAllHints", _read_optimizer())

    def test_save_report(self):
        self.assertIn("SaveReport", _read_optimizer())

    def test_clear_method(self):
        self.assertIn("Clear", _read_optimizer())


if __name__ == "__main__":
    unittest.main()
