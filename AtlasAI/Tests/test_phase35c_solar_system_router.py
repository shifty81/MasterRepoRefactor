"""Phase 35C — Tests for sigma_solar_system.json and SolarSystemRouter.h."""
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOLAR_SYSTEMS_DIR = REPO_ROOT / "NovaForge" / "Content" / "Data" / "SolarSystems"
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"

SIGMA_JSON = SOLAR_SYSTEMS_DIR / "sigma_solar_system.json"
ROUTER_H = SCENE_DIR / "SolarSystemRouter.h"


def _read_router() -> str:
    return ROUTER_H.read_text()


def _load_sigma() -> dict:
    with SIGMA_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# sigma_solar_system.json
# ---------------------------------------------------------------------------

class TestSigmaSolarSystemExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(SIGMA_JSON.exists())


class TestSigmaSolarSystemStructure(unittest.TestCase):
    def test_id_field(self):
        data = _load_sigma()
        self.assertEqual(data["id"], "sigma_solar_system_001")

    def test_name_field(self):
        data = _load_sigma()
        name = data.get("name", "")
        self.assertTrue("Sigma" in name or "sigma" in name)

    def test_version_field(self):
        data = _load_sigma()
        self.assertIn("version", data)

    def test_star_type_g5v(self):
        data = _load_sigma()
        self.assertEqual(data["star"]["type"], "G5V")

    def test_star_luminosity(self):
        data = _load_sigma()
        self.assertAlmostEqual(data["star"]["luminosity"], 0.9, delta=0.1)

    def test_star_radius(self):
        data = _load_sigma()
        self.assertIn("radius", data["star"])

    def test_total_celestials_8(self):
        data = _load_sigma()
        self.assertEqual(data["total_celestials"], 8)

    def test_celestials_list_count(self):
        data = _load_sigma()
        self.assertEqual(len(data["celestials"]), 8)

    def test_has_npc_factions(self):
        data = _load_sigma()
        self.assertIn("npc_factions", data)
        self.assertIsInstance(data["npc_factions"], list)

    def test_has_pcg_config(self):
        data = _load_sigma()
        self.assertIn("pcg_config", data)

    def test_pcg_seed_present(self):
        data = _load_sigma()
        self.assertIn("seed", data["pcg_config"])

    def test_has_hazards(self):
        data = _load_sigma()
        self.assertIn("hazards", data)
        self.assertIsInstance(data["hazards"], list)

    def test_celestials_have_ids(self):
        data = _load_sigma()
        for c in data["celestials"]:
            self.assertIn("id", c)

    def test_celestials_have_types(self):
        data = _load_sigma()
        for c in data["celestials"]:
            self.assertIn("type", c)

    def test_has_planet(self):
        data = _load_sigma()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Planet", types)

    def test_has_gas_giant(self):
        data = _load_sigma()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("GasGiant", types)

    def test_has_station(self):
        data = _load_sigma()
        types = [c["type"] for c in data["celestials"]]
        self.assertIn("Station", types)


# ---------------------------------------------------------------------------
# SolarSystemRouter.h
# ---------------------------------------------------------------------------

class TestSolarSystemRouterExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(ROUTER_H.exists())


class TestSolarSystemRouterStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_router())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_router())

    def test_class_declaration(self):
        self.assertIn("SolarSystemRouter", _read_router())

    def test_route_state_enum(self):
        self.assertIn("RouteState", _read_router())

    def test_route_protocol_enum(self):
        self.assertIn("RouteProtocol", _read_router())

    def test_message_type_enum(self):
        self.assertIn("MessageType", _read_router())

    def test_route_def_struct(self):
        self.assertIn("RouteDef", _read_router())

    def test_route_message_struct(self):
        self.assertIn("RouteMessage", _read_router())

    def test_route_log_struct(self):
        self.assertIn("RouteLog", _read_router())

    def test_register_route(self):
        self.assertIn("RegisterRoute", _read_router())

    def test_unregister_route(self):
        self.assertIn("UnregisterRoute", _read_router())

    def test_set_route_protocol(self):
        self.assertIn("SetRouteProtocol", _read_router())

    def test_set_route_priority(self):
        self.assertIn("SetRoutePriority", _read_router())

    def test_set_ttl(self):
        self.assertIn("SetTTL", _read_router())

    def test_send_message(self):
        self.assertIn("SendMessage", _read_router())

    def test_send_message_async(self):
        self.assertIn("SendMessageAsync", _read_router())

    def test_broadcast_message(self):
        self.assertIn("BroadcastMessage", _read_router())

    def test_multicast_message(self):
        self.assertIn("MulticastMessage", _read_router())

    def test_get_route(self):
        self.assertIn("GetRoute", _read_router())

    def test_get_all_route_ids(self):
        self.assertIn("GetAllRouteIds", _read_router())

    def test_get_routes_by_protocol(self):
        self.assertIn("GetRoutesByProtocol", _read_router())

    def test_get_active_routes(self):
        self.assertIn("GetActiveRoutes", _read_router())

    def test_get_blocked_routes(self):
        self.assertIn("GetBlockedRoutes", _read_router())

    def test_acknowledge_message(self):
        self.assertIn("AcknowledgeMessage", _read_router())

    def test_retry_message(self):
        self.assertIn("RetryMessage", _read_router())

    def test_cancel_message(self):
        self.assertIn("CancelMessage", _read_router())

    def test_get_log(self):
        self.assertIn("GetLog", _read_router())

    def test_get_all_logs(self):
        self.assertIn("GetAllLogs", _read_router())

    def test_flush_logs(self):
        self.assertIn("FlushLogs", _read_router())

    def test_validate_route(self):
        self.assertIn("ValidateRoute", _read_router())

    def test_reset_method(self):
        self.assertIn("Reset", _read_router())

    def test_functional_include(self):
        self.assertIn("<functional>", _read_router())


if __name__ == "__main__":
    unittest.main()
