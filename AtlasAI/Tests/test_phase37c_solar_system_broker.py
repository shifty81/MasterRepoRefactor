"""Phase 37C — Tests for upsilon_solar_system.json and SolarSystemBroker.h."""
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
# upsilon_solar_system.json
# ---------------------------------------------------------------------------

class TestUpsilonSolarSystemJson(unittest.TestCase):
    def setUp(self):
        self.data = _load_json("upsilon_solar_system")

    def test_file_exists(self):
        self.assertTrue((SOLAR_SYSTEMS / "upsilon_solar_system.json").exists())

    def test_id_field(self):
        self.assertEqual(self.data["id"], "upsilon_solar_system_001")

    def test_name_field(self):
        self.assertEqual(self.data["name"], "Upsilon Veilreach System")

    def test_version_field(self):
        self.assertEqual(self.data["version"], "1.0")

    def test_star_type(self):
        self.assertEqual(self.data["star"]["type"], "G9V")

    def test_star_radius(self):
        self.assertEqual(self.data["star"]["radius"], 680000)

    def test_star_luminosity(self):
        self.assertAlmostEqual(self.data["star"]["luminosity"], 0.88)

    def test_total_celestials(self):
        self.assertEqual(self.data["total_celestials"], 8)

    def test_celestials_count(self):
        self.assertEqual(len(self.data["celestials"]), 8)

    def test_habitable_planet_present(self):
        habitable = [c for c in self.data["celestials"] if c.get("habitable")]
        self.assertEqual(len(habitable), 1)

    def test_habitable_planet_name(self):
        habitable = [c for c in self.data["celestials"] if c.get("habitable")]
        self.assertEqual(habitable[0]["name"], "Veilreach Cradle")

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
        self.assertEqual(moons[0]["parent"], "upsilon_planet_003")

    def test_npc_factions_has_veilreach_assembly(self):
        self.assertIn("veilreach_assembly", self.data["npc_factions"])

    def test_pcg_seed(self):
        self.assertEqual(self.data["pcg_config"]["seed"], 2000)

    def test_hazards_has_solar_flare(self):
        self.assertIn("solar_flare", self.data["hazards"])

    def test_hazards_has_void_rift(self):
        self.assertIn("void_rift", self.data["hazards"])

    def test_pcg_hazard_level(self):
        self.assertEqual(self.data["pcg_config"]["hazard_level"], "extreme")

    def test_pcg_resource_richness(self):
        self.assertEqual(self.data["pcg_config"]["resource_richness"], "moderate")


# ---------------------------------------------------------------------------
# SolarSystemBroker.h
# ---------------------------------------------------------------------------

class TestSolarSystemBrokerHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "SolarSystemBroker.h").exists())


class TestSolarSystemBrokerNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("SolarSystemBroker"))


class TestSolarSystemBrokerEnums(unittest.TestCase):
    def test_broker_state_enum(self):
        self.assertIn("BrokerState", _read_header("SolarSystemBroker"))

    def test_message_priority_enum(self):
        self.assertIn("MessagePriority", _read_header("SolarSystemBroker"))

    def test_broker_topic_type_enum(self):
        self.assertIn("BrokerTopicType", _read_header("SolarSystemBroker"))

    def test_broker_event_type_enum(self):
        self.assertIn("BrokerEventType", _read_header("SolarSystemBroker"))

    def test_active_state_value(self):
        self.assertIn("Active", _read_header("SolarSystemBroker"))

    def test_suspended_state(self):
        self.assertIn("Suspended", _read_header("SolarSystemBroker"))

    def test_critical_priority(self):
        self.assertIn("Critical", _read_header("SolarSystemBroker"))

    def test_broadcast_topic_type(self):
        self.assertIn("Broadcast", _read_header("SolarSystemBroker"))


class TestSolarSystemBrokerStructs(unittest.TestCase):
    def test_broker_config_struct(self):
        self.assertIn("BrokerConfig", _read_header("SolarSystemBroker"))

    def test_broker_message_struct(self):
        self.assertIn("BrokerMessage", _read_header("SolarSystemBroker"))

    def test_broker_subscription_struct(self):
        self.assertIn("BrokerSubscription", _read_header("SolarSystemBroker"))

    def test_max_subscribers_in_config(self):
        self.assertIn("maxSubscribers", _read_header("SolarSystemBroker"))

    def test_payload_in_message(self):
        self.assertIn("payload", _read_header("SolarSystemBroker"))

    def test_subscriber_id_in_subscription(self):
        self.assertIn("subscriberId", _read_header("SolarSystemBroker"))


class TestSolarSystemBrokerMethods(unittest.TestCase):
    def test_register_broker(self):
        self.assertIn("RegisterBroker", _read_header("SolarSystemBroker"))

    def test_unregister_broker(self):
        self.assertIn("UnregisterBroker", _read_header("SolarSystemBroker"))

    def test_create_topic(self):
        self.assertIn("CreateTopic", _read_header("SolarSystemBroker"))

    def test_delete_topic(self):
        self.assertIn("DeleteTopic", _read_header("SolarSystemBroker"))

    def test_subscribe(self):
        self.assertIn("Subscribe", _read_header("SolarSystemBroker"))

    def test_unsubscribe(self):
        self.assertIn("Unsubscribe", _read_header("SolarSystemBroker"))

    def test_publish_message(self):
        self.assertIn("PublishMessage", _read_header("SolarSystemBroker"))

    def test_broadcast_message(self):
        self.assertIn("BroadcastMessage", _read_header("SolarSystemBroker"))

    def test_get_message(self):
        self.assertIn("GetMessage", _read_header("SolarSystemBroker"))

    def test_acknowledge_message(self):
        self.assertIn("AcknowledgeMessage", _read_header("SolarSystemBroker"))

    def test_purge_messages(self):
        self.assertIn("PurgeMessages", _read_header("SolarSystemBroker"))

    def test_get_subscriptions_by_topic(self):
        self.assertIn("GetSubscriptionsByTopic", _read_header("SolarSystemBroker"))

    def test_get_active_subscriptions(self):
        self.assertIn("GetActiveSubscriptions", _read_header("SolarSystemBroker"))

    def test_get_unacknowledged_messages(self):
        self.assertIn("GetUnacknowledgedMessages", _read_header("SolarSystemBroker"))

    def test_get_broker_metrics(self):
        self.assertIn("GetBrokerMetrics", _read_header("SolarSystemBroker"))

    def test_reset_metrics(self):
        self.assertIn("ResetMetrics", _read_header("SolarSystemBroker"))

    def test_reset(self):
        self.assertIn("Reset", _read_header("SolarSystemBroker"))

    def test_set_broker_state(self):
        self.assertIn("SetBrokerState", _read_header("SolarSystemBroker"))

    def test_get_broker_state(self):
        self.assertIn("GetBrokerState", _read_header("SolarSystemBroker"))


if __name__ == "__main__":
    unittest.main()
