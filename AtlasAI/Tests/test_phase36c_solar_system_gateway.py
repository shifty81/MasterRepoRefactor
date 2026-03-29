"""Phase 36C — Tests for tau_solar_system.json and SolarSystemGateway.h."""
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
# tau_solar_system.json
# ---------------------------------------------------------------------------

class TestTauSolarSystemJson(unittest.TestCase):
    def setUp(self):
        self.data = _load_json("tau_solar_system")

    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS / "tau_solar_system.json").exists())

    def test_id_field(self):
        self.assertEqual(self.data["id"], "tau_solar_system_001")

    def test_name_field(self):
        self.assertEqual(self.data["name"], "Tau Duskfield System")

    def test_version_field(self):
        self.assertEqual(self.data["version"], "1.0")

    def test_star_type(self):
        self.assertEqual(self.data["star"]["type"], "K1V")

    def test_star_radius(self):
        self.assertEqual(self.data["star"]["radius"], 620000)

    def test_star_luminosity(self):
        self.assertAlmostEqual(self.data["star"]["luminosity"], 0.75)

    def test_total_celestials(self):
        self.assertEqual(self.data["total_celestials"], 8)

    def test_celestials_count(self):
        self.assertEqual(len(self.data["celestials"]), 8)

    def test_habitable_planet_present(self):
        habitable = [c for c in self.data["celestials"] if c.get("habitable")]
        self.assertEqual(len(habitable), 1)

    def test_habitable_planet_name(self):
        habitable = [c for c in self.data["celestials"] if c.get("habitable")]
        self.assertEqual(habitable[0]["name"], "Duskfield Cradle")

    def test_gas_giant_present(self):
        giants = [c for c in self.data["celestials"] if c["type"] == "GasGiant"]
        self.assertEqual(len(giants), 1)

    def test_station_present(self):
        stations = [c for c in self.data["celestials"] if c["type"] == "Station"]
        self.assertEqual(len(stations), 1)

    def test_anomaly_present(self):
        anomalies = [c for c in self.data["celestials"] if c["type"] == "Anomaly"]
        self.assertEqual(len(anomalies), 1)

    def test_moon_has_parent(self):
        moons = [c for c in self.data["celestials"] if c["type"] == "Moon"]
        self.assertTrue(len(moons) >= 1)
        self.assertEqual(moons[0]["parent"], "duskfield_planet_003")

    def test_npc_factions(self):
        self.assertIn("duskfield_accord", self.data["npc_factions"])

    def test_pcg_seed(self):
        self.assertEqual(self.data["pcg_config"]["seed"], 1900)

    def test_hazards(self):
        self.assertIn("plasma_storm", self.data["hazards"])
        self.assertIn("void_rift", self.data["hazards"])

    def test_pcg_hazard_level(self):
        self.assertEqual(self.data["pcg_config"]["hazard_level"], "high")

    def test_pcg_resource_richness(self):
        self.assertEqual(self.data["pcg_config"]["resource_richness"], "rich")


# ---------------------------------------------------------------------------
# SolarSystemGateway.h
# ---------------------------------------------------------------------------

class TestSolarSystemGatewayHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemGateway.h").exists())


class TestSolarSystemGatewayNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("SolarSystemGateway"))


class TestSolarSystemGatewayEnums(unittest.TestCase):
    def test_gateway_state_enum(self):
        self.assertIn("GatewayState", _read_header("SolarSystemGateway"))

    def test_access_policy_enum(self):
        self.assertIn("AccessPolicy", _read_header("SolarSystemGateway"))

    def test_gateway_event_type_enum(self):
        self.assertIn("GatewayEventType", _read_header("SolarSystemGateway"))

    def test_open_state_value(self):
        self.assertIn("Open", _read_header("SolarSystemGateway"))

    def test_throttled_state_value(self):
        self.assertIn("Throttled", _read_header("SolarSystemGateway"))

    def test_authenticated_policy(self):
        self.assertIn("Authenticated", _read_header("SolarSystemGateway"))


class TestSolarSystemGatewayStructs(unittest.TestCase):
    def test_gateway_config_struct(self):
        self.assertIn("GatewayConfig", _read_header("SolarSystemGateway"))

    def test_gateway_request_struct(self):
        self.assertIn("GatewayRequest", _read_header("SolarSystemGateway"))

    def test_gateway_audit_entry_struct(self):
        self.assertIn("GatewayAuditEntry", _read_header("SolarSystemGateway"))

    def test_config_has_max_connections(self):
        self.assertIn("maxConnections", _read_header("SolarSystemGateway"))

    def test_request_has_auth_token(self):
        self.assertIn("authToken", _read_header("SolarSystemGateway"))


class TestSolarSystemGatewayMethods(unittest.TestCase):
    def test_register_gateway(self):
        self.assertIn("RegisterGateway", _read_header("SolarSystemGateway"))

    def test_unregister_gateway(self):
        self.assertIn("UnregisterGateway", _read_header("SolarSystemGateway"))

    def test_open_gateway(self):
        self.assertIn("OpenGateway", _read_header("SolarSystemGateway"))

    def test_close_gateway(self):
        self.assertIn("CloseGateway", _read_header("SolarSystemGateway"))

    def test_throttle_gateway(self):
        self.assertIn("ThrottleGateway", _read_header("SolarSystemGateway"))

    def test_send_request(self):
        self.assertIn("SendRequest", _read_header("SolarSystemGateway"))

    def test_send_request_async(self):
        self.assertIn("SendRequestAsync", _read_header("SolarSystemGateway"))

    def test_authenticate_request(self):
        self.assertIn("AuthenticateRequest", _read_header("SolarSystemGateway"))

    def test_validate_request(self):
        self.assertIn("ValidateRequest", _read_header("SolarSystemGateway"))

    def test_get_all_gateway_ids(self):
        self.assertIn("GetAllGatewayIds", _read_header("SolarSystemGateway"))

    def test_get_open_gateways(self):
        self.assertIn("GetOpenGateways", _read_header("SolarSystemGateway"))

    def test_get_throttled_gateways(self):
        self.assertIn("GetThrottledGateways", _read_header("SolarSystemGateway"))

    def test_get_audit_entry(self):
        self.assertIn("GetAuditEntry", _read_header("SolarSystemGateway"))

    def test_flush_audit_log(self):
        self.assertIn("FlushAuditLog", _read_header("SolarSystemGateway"))

    def test_reset(self):
        self.assertIn("Reset", _read_header("SolarSystemGateway"))

    def test_set_rate_limit(self):
        self.assertIn("SetRateLimit", _read_header("SolarSystemGateway"))

    def test_set_auth_required(self):
        self.assertIn("SetAuthRequired", _read_header("SolarSystemGateway"))

    def test_add_allowed_system(self):
        self.assertIn("AddAllowedSystem", _read_header("SolarSystemGateway"))

    def test_remove_allowed_system(self):
        self.assertIn("RemoveAllowedSystem", _read_header("SolarSystemGateway"))

    def test_cancel_request(self):
        self.assertIn("CancelRequest", _read_header("SolarSystemGateway"))


if __name__ == "__main__":
    unittest.main()
