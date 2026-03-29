"""Phase 38C — Tests for phi_solar_system.json and SolarSystemOrchestrator.h."""
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
# phi_solar_system.json
# ---------------------------------------------------------------------------

class TestPhiSolarSystemJson(unittest.TestCase):
    def setUp(self):
        self.data = _load_json("phi_solar_system")

    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS / "phi_solar_system.json").exists())

    def test_id_field(self):
        self.assertEqual(self.data["id"], "phi_solar_system_001")

    def test_name_field(self):
        self.assertEqual(self.data["name"], "Phi Ashenwing System")

    def test_version_field(self):
        self.assertEqual(self.data["version"], "1.0")

    def test_star_type(self):
        self.assertEqual(self.data["star"]["type"], "F3V")

    def test_star_radius(self):
        self.assertEqual(self.data["star"]["radius"], 740000)

    def test_star_luminosity(self):
        self.assertAlmostEqual(self.data["star"]["luminosity"], 1.45)

    def test_total_celestials(self):
        self.assertEqual(self.data["total_celestials"], 8)

    def test_celestials_count(self):
        self.assertEqual(len(self.data["celestials"]), 8)

    def test_habitable_planet_present(self):
        habitable = [c for c in self.data["celestials"] if c.get("habitable")]
        self.assertEqual(len(habitable), 1)

    def test_habitable_planet_name(self):
        habitable = [c for c in self.data["celestials"] if c.get("habitable")]
        self.assertEqual(habitable[0]["name"], "Ashenwing Cradle")

    def test_gas_giant_present(self):
        gas_giants = [c for c in self.data["celestials"] if c["type"] == "GasGiant"]
        self.assertGreater(len(gas_giants), 0)

    def test_station_present(self):
        stations = [c for c in self.data["celestials"] if c["type"] == "Station"]
        self.assertGreater(len(stations), 0)

    def test_anomaly_present(self):
        anomalies = [c for c in self.data["celestials"] if c["type"] == "Anomaly"]
        self.assertGreater(len(anomalies), 0)

    def test_moon_has_parent(self):
        moons = [c for c in self.data["celestials"] if c["type"] == "Moon"]
        self.assertGreater(len(moons), 0)
        self.assertEqual(moons[0]["parent"], "phi_planet_003")

    def test_npc_factions_has_ashenwing_coalition(self):
        self.assertIn("ashenwing_coalition", self.data["npc_factions"])

    def test_pcg_seed(self):
        self.assertEqual(self.data["pcg_config"]["seed"], 2100)

    def test_hazards_has_ion_storm(self):
        self.assertIn("ion_storm", self.data["hazards"])

    def test_hazards_has_gravity_shear(self):
        self.assertIn("gravity_shear", self.data["hazards"])

    def test_pcg_hazard_level(self):
        self.assertEqual(self.data["pcg_config"]["hazard_level"], "medium")

    def test_pcg_resource_richness(self):
        self.assertEqual(self.data["pcg_config"]["resource_richness"], "abundant")


# ---------------------------------------------------------------------------
# SolarSystemOrchestrator.h
# ---------------------------------------------------------------------------

class TestSolarSystemOrchestratorHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemOrchestrator.h").exists())


class TestSolarSystemOrchestratorNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("SolarSystemOrchestrator"))


class TestSolarSystemOrchestratorEnums(unittest.TestCase):
    def test_orchestrator_state_enum(self):
        self.assertIn("OrchestratorState", _read_header("SolarSystemOrchestrator"))

    def test_task_priority_enum(self):
        self.assertIn("TaskPriority", _read_header("SolarSystemOrchestrator"))

    def test_dependency_mode_enum(self):
        self.assertIn("DependencyMode", _read_header("SolarSystemOrchestrator"))

    def test_workflow_event_type_enum(self):
        self.assertIn("WorkflowEventType", _read_header("SolarSystemOrchestrator"))

    def test_idle_state(self):
        self.assertIn("Idle", _read_header("SolarSystemOrchestrator"))

    def test_executing_state(self):
        self.assertIn("Executing", _read_header("SolarSystemOrchestrator"))

    def test_critical_priority(self):
        self.assertIn("Critical", _read_header("SolarSystemOrchestrator"))

    def test_sequential_dep_mode(self):
        self.assertIn("Sequential", _read_header("SolarSystemOrchestrator"))


class TestSolarSystemOrchestratorStructs(unittest.TestCase):
    def test_orchestrator_task_struct(self):
        self.assertIn("OrchestratorTask", _read_header("SolarSystemOrchestrator"))

    def test_workflow_def_struct(self):
        self.assertIn("WorkflowDef", _read_header("SolarSystemOrchestrator"))

    def test_workflow_audit_entry_struct(self):
        self.assertIn("WorkflowAuditEntry", _read_header("SolarSystemOrchestrator"))

    def test_dependency_ids_in_task(self):
        self.assertIn("dependencyIds", _read_header("SolarSystemOrchestrator"))

    def test_total_tasks_in_workflow(self):
        self.assertIn("totalTasks", _read_header("SolarSystemOrchestrator"))

    def test_success_in_audit_entry(self):
        self.assertIn("success", _read_header("SolarSystemOrchestrator"))


class TestSolarSystemOrchestratorMethods(unittest.TestCase):
    def test_register_workflow(self):
        self.assertIn("RegisterWorkflow", _read_header("SolarSystemOrchestrator"))

    def test_unregister_workflow(self):
        self.assertIn("UnregisterWorkflow", _read_header("SolarSystemOrchestrator"))

    def test_set_workflow_state(self):
        self.assertIn("SetWorkflowState", _read_header("SolarSystemOrchestrator"))

    def test_get_workflow_state(self):
        self.assertIn("GetWorkflowState", _read_header("SolarSystemOrchestrator"))

    def test_get_workflow(self):
        self.assertIn("GetWorkflow", _read_header("SolarSystemOrchestrator"))

    def test_get_all_workflow_ids(self):
        self.assertIn("GetAllWorkflowIds", _read_header("SolarSystemOrchestrator"))

    def test_get_active_workflows(self):
        self.assertIn("GetActiveWorkflows", _read_header("SolarSystemOrchestrator"))

    def test_get_completed_workflows(self):
        self.assertIn("GetCompletedWorkflows", _read_header("SolarSystemOrchestrator"))

    def test_get_failed_workflows(self):
        self.assertIn("GetFailedWorkflows", _read_header("SolarSystemOrchestrator"))

    def test_add_task(self):
        self.assertIn("AddTask", _read_header("SolarSystemOrchestrator"))

    def test_remove_task(self):
        self.assertIn("RemoveTask", _read_header("SolarSystemOrchestrator"))

    def test_complete_task(self):
        self.assertIn("CompleteTask", _read_header("SolarSystemOrchestrator"))

    def test_retry_task(self):
        self.assertIn("RetryTask", _read_header("SolarSystemOrchestrator"))

    def test_start_workflow(self):
        self.assertIn("StartWorkflow", _read_header("SolarSystemOrchestrator"))

    def test_pause_workflow(self):
        self.assertIn("PauseWorkflow", _read_header("SolarSystemOrchestrator"))

    def test_resume_workflow(self):
        self.assertIn("ResumeWorkflow", _read_header("SolarSystemOrchestrator"))

    def test_abort_workflow(self):
        self.assertIn("AbortWorkflow", _read_header("SolarSystemOrchestrator"))

    def test_log_event(self):
        self.assertIn("LogEvent", _read_header("SolarSystemOrchestrator"))

    def test_flush_audit_log(self):
        self.assertIn("FlushAuditLog", _read_header("SolarSystemOrchestrator"))

    def test_reset(self):
        self.assertIn("Reset", _read_header("SolarSystemOrchestrator"))


if __name__ == "__main__":
    unittest.main()
