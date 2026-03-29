"""Phase 40C — Tests for psi_solar_system.json and SolarSystemNavigator.h."""
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
# psi_solar_system.json
# ---------------------------------------------------------------------------

class TestPsiSolarSystemJson(unittest.TestCase):
    def setUp(self):
        self.data = _load_json("psi_solar_system")

    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS / "psi_solar_system.json").exists())

    def test_id_field(self):
        self.assertEqual(self.data["id"], "psi_solar_system_001")

    def test_name_field(self):
        self.assertEqual(self.data["name"], "Psi Embervast System")

    def test_version_field(self):
        self.assertEqual(self.data["version"], "1.0")

    def test_star_type(self):
        self.assertEqual(self.data["star"]["type"], "G6V")

    def test_star_radius(self):
        self.assertEqual(self.data["star"]["radius"], 720000)

    def test_star_luminosity(self):
        self.assertAlmostEqual(self.data["star"]["luminosity"], 0.85)

    def test_total_celestials(self):
        self.assertEqual(self.data["total_celestials"], 8)

    def test_celestials_count(self):
        self.assertEqual(len(self.data["celestials"]), 8)

    def test_habitable_planet_present(self):
        habitable = [c for c in self.data["celestials"] if c.get("habitable")]
        self.assertEqual(len(habitable), 1)

    def test_habitable_planet_name(self):
        habitable = [c for c in self.data["celestials"] if c.get("habitable")]
        self.assertEqual(habitable[0]["name"], "Embervast Cradle")

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
        self.assertEqual(moons[0]["parent"], "psi_planet_003")

    def test_npc_factions_has_embervast_dominion(self):
        self.assertIn("embervast_dominion", self.data["npc_factions"])

    def test_pcg_seed(self):
        self.assertEqual(self.data["pcg_config"]["seed"], 2300)

    def test_hazards_has_solar_flare(self):
        self.assertIn("solar_flare", self.data["hazards"])

    def test_hazards_has_asteroid_belt(self):
        self.assertIn("asteroid_belt", self.data["hazards"])

    def test_pcg_hazard_level(self):
        self.assertEqual(self.data["pcg_config"]["hazard_level"], "medium")

    def test_pcg_resource_richness(self):
        self.assertEqual(self.data["pcg_config"]["resource_richness"], "high")


# ---------------------------------------------------------------------------
# SolarSystemNavigator.h
# ---------------------------------------------------------------------------

class TestSolarSystemNavigatorHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemNavigator.h").exists())


class TestSolarSystemNavigatorNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("SolarSystemNavigator"))


class TestSolarSystemNavigatorEnums(unittest.TestCase):
    def test_navigation_state_enum(self):
        self.assertIn("NavigationState", _read_header("SolarSystemNavigator"))

    def test_route_type_enum(self):
        self.assertIn("RouteType", _read_header("SolarSystemNavigator"))

    def test_waypoint_type_enum(self):
        self.assertIn("WaypointType", _read_header("SolarSystemNavigator"))

    def test_travel_mode_enum(self):
        self.assertIn("TravelMode", _read_header("SolarSystemNavigator"))

    def test_idle_state_value(self):
        self.assertIn("Idle", _read_header("SolarSystemNavigator"))

    def test_planning_state_value(self):
        self.assertIn("Planning", _read_header("SolarSystemNavigator"))

    def test_ftl_mode_value(self):
        self.assertIn("FTL", _read_header("SolarSystemNavigator"))

    def test_direct_route_value(self):
        self.assertIn("Direct", _read_header("SolarSystemNavigator"))

    def test_transit_waypoint_value(self):
        self.assertIn("Transit", _read_header("SolarSystemNavigator"))


class TestSolarSystemNavigatorStructs(unittest.TestCase):
    def test_waypoint_def_struct(self):
        self.assertIn("WaypointDef", _read_header("SolarSystemNavigator"))

    def test_route_def_struct(self):
        self.assertIn("RouteDef", _read_header("SolarSystemNavigator"))

    def test_travel_record_struct(self):
        self.assertIn("TravelRecord", _read_header("SolarSystemNavigator"))

    def test_mandatory_in_waypoint(self):
        self.assertIn("mandatory", _read_header("SolarSystemNavigator"))

    def test_validated_in_route(self):
        self.assertIn("validated", _read_header("SolarSystemNavigator"))

    def test_progress_pct_in_travel(self):
        self.assertIn("progressPct", _read_header("SolarSystemNavigator"))


class TestSolarSystemNavigatorMethods(unittest.TestCase):
    def test_add_waypoint(self):
        self.assertIn("AddWaypoint", _read_header("SolarSystemNavigator"))

    def test_remove_waypoint(self):
        self.assertIn("RemoveWaypoint", _read_header("SolarSystemNavigator"))

    def test_set_waypoint_type(self):
        self.assertIn("SetWaypointType", _read_header("SolarSystemNavigator"))

    def test_get_waypoint(self):
        self.assertIn("GetWaypoint", _read_header("SolarSystemNavigator"))

    def test_get_all_waypoint_ids(self):
        self.assertIn("GetAllWaypointIds", _read_header("SolarSystemNavigator"))

    def test_get_waypoints_by_type(self):
        self.assertIn("GetWaypointsByType", _read_header("SolarSystemNavigator"))

    def test_get_waypoints_by_system(self):
        self.assertIn("GetWaypointsBySystem", _read_header("SolarSystemNavigator"))

    def test_get_mandatory_waypoints(self):
        self.assertIn("GetMandatoryWaypoints", _read_header("SolarSystemNavigator"))

    def test_create_route(self):
        self.assertIn("CreateRoute", _read_header("SolarSystemNavigator"))

    def test_delete_route(self):
        self.assertIn("DeleteRoute", _read_header("SolarSystemNavigator"))

    def test_validate_route(self):
        self.assertIn("ValidateRoute", _read_header("SolarSystemNavigator"))

    def test_set_travel_mode(self):
        self.assertIn("SetTravelMode", _read_header("SolarSystemNavigator"))

    def test_get_route(self):
        self.assertIn("GetRoute", _read_header("SolarSystemNavigator"))

    def test_get_all_route_ids(self):
        self.assertIn("GetAllRouteIds", _read_header("SolarSystemNavigator"))

    def test_get_routes_by_type(self):
        self.assertIn("GetRoutesByType", _read_header("SolarSystemNavigator"))

    def test_get_validated_routes(self):
        self.assertIn("GetValidatedRoutes", _read_header("SolarSystemNavigator"))

    def test_begin_travel(self):
        self.assertIn("BeginTravel", _read_header("SolarSystemNavigator"))

    def test_update_travel(self):
        self.assertIn("UpdateTravel", _read_header("SolarSystemNavigator"))

    def test_complete_travel(self):
        self.assertIn("CompleteTravel", _read_header("SolarSystemNavigator"))

    def test_abort_travel(self):
        self.assertIn("AbortTravel", _read_header("SolarSystemNavigator"))

    def test_get_travel_record(self):
        self.assertIn("GetTravelRecord", _read_header("SolarSystemNavigator"))

    def test_get_all_travel_ids(self):
        self.assertIn("GetAllTravelIds", _read_header("SolarSystemNavigator"))

    def test_get_active_travels(self):
        self.assertIn("GetActiveTravels", _read_header("SolarSystemNavigator"))

    def test_get_completed_travels(self):
        self.assertIn("GetCompletedTravels", _read_header("SolarSystemNavigator"))

    def test_get_travels_by_route(self):
        self.assertIn("GetTravelsByRoute", _read_header("SolarSystemNavigator"))

    def test_reset(self):
        self.assertIn("Reset", _read_header("SolarSystemNavigator"))


if __name__ == "__main__":
    unittest.main()
