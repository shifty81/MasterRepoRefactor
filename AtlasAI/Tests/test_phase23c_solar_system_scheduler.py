"""Phase 23C — Tests for zeta_solar_system.json and SolarSystemScheduler.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = (
    REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
)
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"


# ---------------------------------------------------------------------------
# zeta_solar_system.json
# ---------------------------------------------------------------------------

class TestZetaSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS_DIR / "zeta_solar_system.json").exists())


class TestZetaSolarSystemStructure(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (SOLAR_SYSTEMS_DIR / "zeta_solar_system.json").read_text()
        )

    def test_id_field(self):
        self.assertIn("id", self.data)

    def test_id_starts_with_zeta(self):
        self.assertTrue(self.data["id"].startswith("zeta_solar_system"))

    def test_name_field(self):
        self.assertIn("name", self.data)

    def test_star_field(self):
        self.assertIn("star", self.data)

    def test_star_has_type(self):
        self.assertIn("type", self.data["star"])

    def test_star_type_g2v(self):
        self.assertEqual(self.data["star"]["type"], "G2V")

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


class TestZetaSolarSystemCelestialTypes(unittest.TestCase):
    def setUp(self):
        data = json.loads(
            (SOLAR_SYSTEMS_DIR / "zeta_solar_system.json").read_text()
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


class TestAllSixSolarSystemsDistinct(unittest.TestCase):
    _FILES = [
        "dev_solar_system.json",
        "beta_solar_system.json",
        "gamma_solar_system.json",
        "delta_solar_system.json",
        "epsilon_solar_system.json",
        "zeta_solar_system.json",
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
# SolarSystemScheduler.h tests
# ---------------------------------------------------------------------------

def _sched() -> str:
    return (SCENE_DIR / "SolarSystemScheduler.h").read_text()


class TestSolarSystemSchedulerExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemScheduler.h").exists())


class TestSolarSystemSchedulerHeader(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _sched())

    def test_namespace_atlas_engine(self):
        self.assertIn("Atlas::Engine", _sched())

    def test_class_declared(self):
        self.assertIn("class SolarSystemScheduler", _sched())


class TestSolarSystemSchedulerAPI(unittest.TestCase):
    def test_start(self):
        self.assertIn("Start", _sched())

    def test_pause(self):
        self.assertIn("Pause", _sched())

    def test_resume(self):
        self.assertIn("Resume", _sched())

    def test_stop(self):
        self.assertIn("Stop", _sched())

    def test_tick(self):
        self.assertIn("Tick", _sched())

    def test_get_current_time(self):
        self.assertIn("GetCurrentTime", _sched())

    def test_reset_time(self):
        self.assertIn("ResetTime", _sched())

    def test_schedule_once(self):
        self.assertIn("ScheduleOnce", _sched())

    def test_schedule_repeating(self):
        self.assertIn("ScheduleRepeating", _sched())

    def test_schedule_orbital_phase(self):
        self.assertIn("ScheduleOrbitalPhase", _sched())

    def test_schedule_cross_system(self):
        self.assertIn("ScheduleCrossSystem", _sched())

    def test_cancel_event(self):
        self.assertIn("CancelEvent", _sched())

    def test_enable_event(self):
        self.assertIn("EnableEvent", _sched())

    def test_is_scheduled(self):
        self.assertIn("IsScheduled", _sched())

    def test_get_event_count(self):
        self.assertIn("GetEventCount", _sched())

    def test_get_event_ids_for_system(self):
        self.assertIn("GetEventIdsForSystem", _sched())

    def test_get_events_by_priority(self):
        self.assertIn("GetEventsByPriority", _sched())

    def test_get_events_by_tag(self):
        self.assertIn("GetEventsByTag", _sched())

    def test_get_upcoming_events(self):
        self.assertIn("GetUpcomingEvents", _sched())

    def test_cancel_all_for_system(self):
        self.assertIn("CancelAllForSystem", _sched())

    def test_enable_all_for_system(self):
        self.assertIn("EnableAllForSystem", _sched())

    def test_set_on_event_fired_callback(self):
        self.assertIn("SetOnEventFiredCallback", _sched())

    def test_clear(self):
        self.assertIn("Clear", _sched())


class TestSolarSystemSchedulerStructs(unittest.TestCase):
    def test_trigger_type_enum(self):
        self.assertIn("TriggerType", _sched())

    def test_event_priority_enum(self):
        self.assertIn("EventPriority", _sched())

    def test_scheduler_state_enum(self):
        self.assertIn("SchedulerState", _sched())

    def test_scheduled_event_struct(self):
        self.assertIn("ScheduledEvent", _sched())

    def test_event_callback_typedef(self):
        self.assertIn("EventCallback", _sched())

    def test_trigger_type_once(self):
        self.assertIn("Once", _sched())

    def test_trigger_type_repeating(self):
        self.assertIn("Repeating", _sched())

    def test_trigger_type_orbital_phase(self):
        self.assertIn("OrbitalPhase", _sched())

    def test_trigger_type_cross_system(self):
        self.assertIn("CrossSystem", _sched())

    def test_scheduled_event_fire_count(self):
        self.assertIn("fireCount", _sched())

    def test_is_running(self):
        self.assertIn("IsRunning", _sched())


if __name__ == "__main__":
    unittest.main()
