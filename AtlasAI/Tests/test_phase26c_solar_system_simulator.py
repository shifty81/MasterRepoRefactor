"""Phase 26C — Tests for iota_solar_system.json and SolarSystemSimulator.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = (
    REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
)
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"


# ---------------------------------------------------------------------------
# iota_solar_system.json
# ---------------------------------------------------------------------------

class TestIotaSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS_DIR / "iota_solar_system.json").exists())


class TestIotaSolarSystemStructure(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (SOLAR_SYSTEMS_DIR / "iota_solar_system.json").read_text()
        )

    def test_id_field(self):
        self.assertIn("id", self.data)

    def test_id_starts_with_iota(self):
        self.assertTrue(self.data["id"].startswith("iota_solar_system"))

    def test_name_field(self):
        self.assertIn("name", self.data)

    def test_star_field(self):
        self.assertIn("star", self.data)

    def test_star_has_type(self):
        self.assertIn("type", self.data["star"])

    def test_star_type_b2v(self):
        self.assertEqual(self.data["star"]["type"], "B2V")

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


class TestIotaSolarSystemCelestialTypes(unittest.TestCase):
    def setUp(self):
        data = json.loads(
            (SOLAR_SYSTEMS_DIR / "iota_solar_system.json").read_text()
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

    def test_has_asteroid_belt_or_nebula(self):
        self.assertTrue(
            "AsteroidBelt" in self.types
            or "Nebula" in self.types
            or "GasGiant" in self.types
        )


class TestAllNineSolarSystemsDistinct(unittest.TestCase):
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
# SolarSystemSimulator.h
# ---------------------------------------------------------------------------

def _read_simulator() -> str:
    return (SCENE_DIR / "SolarSystemSimulator.h").read_text()


class TestSolarSystemSimulatorExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemSimulator.h").exists())


class TestSolarSystemSimulatorStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_simulator())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_simulator())

    def test_class_declaration(self):
        self.assertIn("SolarSystemSimulator", _read_simulator())

    def test_integrator_type_enum(self):
        self.assertIn("IntegratorType", _read_simulator())

    def test_simulation_mode_enum(self):
        self.assertIn("SimulationMode", _read_simulator())

    def test_body_category_enum(self):
        self.assertIn("BodyCategory", _read_simulator())

    def test_orbital_elements_struct(self):
        self.assertIn("OrbitalElements", _read_simulator())

    def test_celestial_body_struct(self):
        self.assertIn("CelestialBody", _read_simulator())

    def test_simulation_state_struct(self):
        self.assertIn("SimulationState", _read_simulator())

    def test_lagrange_point_struct(self):
        self.assertIn("LagrangePoint", _read_simulator())


class TestSolarSystemSimulatorAPI(unittest.TestCase):
    def test_set_integrator(self):
        self.assertIn("SetIntegrator", _read_simulator())

    def test_set_simulation_mode(self):
        self.assertIn("SetSimulationMode", _read_simulator())

    def test_set_time_step(self):
        self.assertIn("SetTimeStep", _read_simulator())

    def test_add_body(self):
        self.assertIn("AddBody", _read_simulator())

    def test_remove_body(self):
        self.assertIn("RemoveBody", _read_simulator())

    def test_start(self):
        self.assertIn("Start", _read_simulator())

    def test_pause(self):
        self.assertIn("Pause", _read_simulator())

    def test_resume(self):
        self.assertIn("Resume", _read_simulator())

    def test_stop(self):
        self.assertIn("Stop", _read_simulator())

    def test_step(self):
        self.assertIn("Step", _read_simulator())

    def test_get_distance_between(self):
        self.assertIn("GetDistanceBetween", _read_simulator())

    def test_get_escape_velocity(self):
        self.assertIn("GetEscapeVelocity", _read_simulator())

    def test_get_hill_sphere_radius(self):
        self.assertIn("GetHillSphereRadius", _read_simulator())

    def test_compute_lagrange_points(self):
        self.assertIn("ComputeLagrangePoints", _read_simulator())

    def test_get_lagrange_point(self):
        self.assertIn("GetLagrangePoint", _read_simulator())

    def test_predict_trajectory(self):
        self.assertIn("PredictTrajectory", _read_simulator())

    def test_save_state(self):
        self.assertIn("SaveState", _read_simulator())

    def test_clear_method(self):
        self.assertIn("Clear", _read_simulator())


if __name__ == "__main__":
    unittest.main()
