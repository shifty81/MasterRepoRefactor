"""Phase 34C — Tests for rho_solar_system.json and SolarSystemDispatcher.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

RHO_JSON = SOLAR_SYSTEMS_DIR / "rho_solar_system.json"
DISPATCHER_H = SCENE_DIR / "SolarSystemDispatcher.h"


def _read_dispatcher() -> str:
    return DISPATCHER_H.read_text()


def _load_rho() -> dict:
    with RHO_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# rho_solar_system.json
# ---------------------------------------------------------------------------

class TestRhoSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(RHO_JSON.exists())


class TestRhoSolarSystemStructure(unittest.TestCase):
    def test_id_field(self):
        data = _load_rho()
        self.assertEqual(data["id"], "rho_solar_system_001")

    def test_name_field(self):
        data = _load_rho()
        name = data.get("name", "")
        self.assertTrue("Rho" in name or "rho" in name)

    def test_version_field(self):
        data = _load_rho()
        self.assertIn("version", data)

    def test_star_type_f8v(self):
        data = _load_rho()
        self.assertEqual(data["star"]["type"], "F8V")

    def test_star_luminosity(self):
        data = _load_rho()
        self.assertAlmostEqual(data["star"]["luminosity"], 1.5, delta=0.1)

    def test_star_radius(self):
        data = _load_rho()
        self.assertIn("radius", data["star"])

    def test_total_celestials_8(self):
        data = _load_rho()
        self.assertEqual(data["total_celestials"], 8)

    def test_celestials_list_count(self):
        data = _load_rho()
        self.assertEqual(len(data["celestials"]), 8)

    def test_has_npc_factions(self):
        data = _load_rho()
        self.assertIn("npc_factions", data)
        self.assertIsInstance(data["npc_factions"], list)

    def test_has_pcg_config(self):
        data = _load_rho()
        self.assertIn("pcg_config", data)

    def test_pcg_seed_present(self):
        data = _load_rho()
        self.assertIn("seed", data["pcg_config"])

    def test_has_hazards(self):
        data = _load_rho()
        self.assertIn("hazards", data)
        self.assertIsInstance(data["hazards"], list)

    def test_celestials_have_ids(self):
        data = _load_rho()
        for c in data["celestials"]:
            self.assertIn("id", c)

    def test_celestials_have_types(self):
        data = _load_rho()
        for c in data["celestials"]:
            self.assertIn("type", c)

    def test_has_planet(self):
        data = _load_rho()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Planet", types)

    def test_has_gas_giant(self):
        data = _load_rho()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("GasGiant", types)

    def test_has_station(self):
        data = _load_rho()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Station", types)


# ---------------------------------------------------------------------------
# SolarSystemDispatcher.h
# ---------------------------------------------------------------------------

class TestSolarSystemDispatcherExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(DISPATCHER_H.exists())


class TestSolarSystemDispatcherStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_dispatcher())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_dispatcher())

    def test_class_declaration(self):
        self.assertIn("SolarSystemDispatcher", _read_dispatcher())

    def test_dispatch_state_enum(self):
        self.assertIn("DispatchState", _read_dispatcher())

    def test_dispatch_priority_enum(self):
        self.assertIn("DispatchPriority", _read_dispatcher())

    def test_event_type_enum(self):
        self.assertIn("EventType", _read_dispatcher())

    def test_dispatch_filter_struct(self):
        self.assertIn("DispatchFilter", _read_dispatcher())

    def test_dispatch_job_struct(self):
        self.assertIn("DispatchJob", _read_dispatcher())

    def test_dispatch_result_struct(self):
        self.assertIn("DispatchResult", _read_dispatcher())

    def test_register_handler(self):
        self.assertIn("RegisterHandler", _read_dispatcher())

    def test_create_job(self):
        self.assertIn("CreateJob", _read_dispatcher())

    def test_cancel_job(self):
        self.assertIn("CancelJob", _read_dispatcher())

    def test_pause_job(self):
        self.assertIn("PauseJob", _read_dispatcher())

    def test_resume_job(self):
        self.assertIn("ResumeJob", _read_dispatcher())

    def test_get_all_job_ids(self):
        self.assertIn("GetAllJobIds", _read_dispatcher())

    def test_set_priority(self):
        self.assertIn("SetPriority", _read_dispatcher())

    def test_set_max_retries(self):
        self.assertIn("SetMaxRetries", _read_dispatcher())

    def test_dispatch_method(self):
        self.assertIn("Dispatch", _read_dispatcher())

    def test_dispatch_async_method(self):
        self.assertIn("DispatchAsync", _read_dispatcher())

    def test_dispatch_batch(self):
        self.assertIn("DispatchBatch", _read_dispatcher())

    def test_flush_queue(self):
        self.assertIn("FlushQueue", _read_dispatcher())

    def test_drain_queue(self):
        self.assertIn("DrainQueue", _read_dispatcher())

    def test_get_result(self):
        self.assertIn("GetResult", _read_dispatcher())

    def test_get_jobs_by_state(self):
        self.assertIn("GetJobsByState", _read_dispatcher())

    def test_get_jobs_by_priority(self):
        self.assertIn("GetJobsByPriority", _read_dispatcher())

    def test_get_queue_depth(self):
        self.assertIn("GetQueueDepth", _read_dispatcher())

    def test_validate_job(self):
        self.assertIn("ValidateJob", _read_dispatcher())

    def test_list_handlers(self):
        self.assertIn("ListHandlers", _read_dispatcher())

    def test_clear_results(self):
        self.assertIn("ClearResults", _read_dispatcher())

    def test_reset_method(self):
        self.assertIn("Reset", _read_dispatcher())

    def test_functional_include(self):
        self.assertIn("<functional>", _read_dispatcher())


if __name__ == "__main__":
    unittest.main()
