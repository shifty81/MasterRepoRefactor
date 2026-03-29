"""Phase 36D — Tests for EventBodyRegistry.h and event_body_loader.py."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    EventBodyLoader,
    EventBodyManifest,
    TriggerConfigManifest,
    EventPayloadManifest,
)


def _read_header(name: str) -> str:
    return (SCENE_DIR / f"{name}.h").read_text()


# ---------------------------------------------------------------------------
# EventBodyRegistry.h
# ---------------------------------------------------------------------------

class TestEventBodyRegistryHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "EventBodyRegistry.h").exists())


class TestEventBodyRegistryNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("EventBodyRegistry"))


class TestEventBodyRegistryEnums(unittest.TestCase):
    def test_event_body_state_enum(self):
        self.assertIn("EventBodyState", _read_header("EventBodyRegistry"))

    def test_event_body_scope_enum(self):
        self.assertIn("EventBodyScope", _read_header("EventBodyRegistry"))

    def test_trigger_type_enum(self):
        self.assertIn("TriggerType", _read_header("EventBodyRegistry"))

    def test_event_priority_enum(self):
        self.assertIn("EventPriority", _read_header("EventBodyRegistry"))

    def test_event_body_flags_enum(self):
        self.assertIn("EventBodyFlags", _read_header("EventBodyRegistry"))

    def test_listening_state_value(self):
        self.assertIn("Listening", _read_header("EventBodyRegistry"))

    def test_triggered_state_value(self):
        self.assertIn("Triggered", _read_header("EventBodyRegistry"))

    def test_on_signal_trigger(self):
        self.assertIn("OnSignal", _read_header("EventBodyRegistry"))

    def test_on_timer_trigger(self):
        self.assertIn("OnTimer", _read_header("EventBodyRegistry"))


class TestEventBodyRegistryStructs(unittest.TestCase):
    def test_trigger_config_struct(self):
        self.assertIn("TriggerConfig", _read_header("EventBodyRegistry"))

    def test_event_payload_struct(self):
        self.assertIn("EventPayload", _read_header("EventBodyRegistry"))

    def test_event_body_record_struct(self):
        self.assertIn("EventBodyRecord", _read_header("EventBodyRegistry"))

    def test_trigger_config_has_debounce(self):
        self.assertIn("debounceMs", _read_header("EventBodyRegistry"))

    def test_payload_has_recipients(self):
        self.assertIn("recipients", _read_header("EventBodyRegistry"))

    def test_body_record_has_trigger_count(self):
        self.assertIn("triggerCount", _read_header("EventBodyRegistry"))


class TestEventBodyRegistryMethods(unittest.TestCase):
    def test_register_body(self):
        self.assertIn("RegisterBody", _read_header("EventBodyRegistry"))

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_header("EventBodyRegistry"))

    def test_set_body_scope(self):
        self.assertIn("SetBodyScope", _read_header("EventBodyRegistry"))

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_header("EventBodyRegistry"))

    def test_set_trigger_type(self):
        self.assertIn("SetTriggerType", _read_header("EventBodyRegistry"))

    def test_trigger_body(self):
        self.assertIn("TriggerBody", _read_header("EventBodyRegistry"))

    def test_reset_body(self):
        self.assertIn("ResetBody", _read_header("EventBodyRegistry"))

    def test_disable_body(self):
        self.assertIn("DisableBody", _read_header("EventBodyRegistry"))

    def test_get_body_by_id(self):
        self.assertIn("GetBodyById", _read_header("EventBodyRegistry"))

    def test_get_all_body_ids(self):
        self.assertIn("GetAllBodyIds", _read_header("EventBodyRegistry"))

    def test_get_bodies_by_scope(self):
        self.assertIn("GetBodiesByScope", _read_header("EventBodyRegistry"))

    def test_get_listening_bodies(self):
        self.assertIn("GetListeningBodies", _read_header("EventBodyRegistry"))

    def test_get_triggered_bodies(self):
        self.assertIn("GetTriggeredBodies", _read_header("EventBodyRegistry"))

    def test_add_payload(self):
        self.assertIn("AddPayload", _read_header("EventBodyRegistry"))

    def test_remove_payload(self):
        self.assertIn("RemovePayload", _read_header("EventBodyRegistry"))

    def test_get_payloads_by_body(self):
        self.assertIn("GetPayloadsByBody", _read_header("EventBodyRegistry"))

    def test_clear(self):
        self.assertIn("Clear", _read_header("EventBodyRegistry"))

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_header("EventBodyRegistry"))

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_header("EventBodyRegistry"))


# ---------------------------------------------------------------------------
# TriggerConfigManifest
# ---------------------------------------------------------------------------

class TestTriggerConfigManifest(unittest.TestCase):
    def test_default_trigger_type(self):
        t = TriggerConfigManifest()
        self.assertEqual(t.trigger_type, "OnSignal")

    def test_default_priority(self):
        t = TriggerConfigManifest()
        self.assertEqual(t.priority, "Normal")

    def test_is_repeatable_true_zero(self):
        t = TriggerConfigManifest(max_triggers=0)
        self.assertTrue(t.is_repeatable)

    def test_is_repeatable_false_one(self):
        t = TriggerConfigManifest(max_triggers=1)
        self.assertFalse(t.is_repeatable)

    def test_has_cooldown_false(self):
        t = TriggerConfigManifest()
        self.assertFalse(t.has_cooldown)

    def test_has_cooldown_true(self):
        t = TriggerConfigManifest(cooldown_ms=500.0)
        self.assertTrue(t.has_cooldown)


# ---------------------------------------------------------------------------
# EventPayloadManifest
# ---------------------------------------------------------------------------

class TestEventPayloadManifest(unittest.TestCase):
    def test_payload_id(self):
        p = EventPayloadManifest(payload_id="pay_001", body_id="body_001")
        self.assertEqual(p.payload_id, "pay_001")

    def test_body_id(self):
        p = EventPayloadManifest(payload_id="pay_001", body_id="body_001")
        self.assertEqual(p.body_id, "body_001")

    def test_default_event_type(self):
        p = EventPayloadManifest(payload_id="pay_001", body_id="body_001")
        self.assertEqual(p.event_type, "OnSignal")

    def test_has_recipients_false(self):
        p = EventPayloadManifest(payload_id="pay_001", body_id="body_001")
        self.assertFalse(p.has_recipients)

    def test_has_recipients_true(self):
        p = EventPayloadManifest(payload_id="pay_001", body_id="body_001",
                                 recipients=["recv_001"])
        self.assertTrue(p.has_recipients)

    def test_is_broadcast_true(self):
        p = EventPayloadManifest(payload_id="pay_001", body_id="body_001")
        self.assertTrue(p.is_broadcast)

    def test_is_broadcast_false(self):
        p = EventPayloadManifest(payload_id="pay_001", body_id="body_001",
                                 recipients=["recv_001"])
        self.assertFalse(p.is_broadcast)


# ---------------------------------------------------------------------------
# EventBodyManifest
# ---------------------------------------------------------------------------

class TestEventBodyManifest(unittest.TestCase):
    def test_body_id(self):
        m = EventBodyManifest(body_id="body_001", name="Trigger Zone A")
        self.assertEqual(m.body_id, "body_001")

    def test_name(self):
        m = EventBodyManifest(body_id="body_001", name="Trigger Zone A")
        self.assertEqual(m.name, "Trigger Zone A")

    def test_default_scope(self):
        m = EventBodyManifest(body_id="body_001", name="Trigger Zone A")
        self.assertEqual(m.scope, "Global")

    def test_default_body_state(self):
        m = EventBodyManifest(body_id="body_001", name="Trigger Zone A")
        self.assertEqual(m.body_state, "Idle")

    def test_is_listening_false(self):
        m = EventBodyManifest(body_id="body_001", name="Trigger Zone A")
        self.assertFalse(m.is_listening)

    def test_is_listening_true(self):
        m = EventBodyManifest(body_id="body_001", name="Trigger Zone A",
                              body_state="Listening")
        self.assertTrue(m.is_listening)

    def test_is_triggered_false(self):
        m = EventBodyManifest(body_id="body_001", name="Trigger Zone A")
        self.assertFalse(m.is_triggered)

    def test_is_triggered_true(self):
        m = EventBodyManifest(body_id="body_001", name="Trigger Zone A",
                              body_state="Triggered")
        self.assertTrue(m.is_triggered)

    def test_has_payloads_false(self):
        m = EventBodyManifest(body_id="body_001", name="Trigger Zone A")
        self.assertFalse(m.has_payloads)

    def test_has_payloads_true(self):
        m = EventBodyManifest(body_id="body_001", name="Trigger Zone A",
                              payloads=["pay_001"])
        self.assertTrue(m.has_payloads)


# ---------------------------------------------------------------------------
# EventBodyLoader
# ---------------------------------------------------------------------------

class TestEventBodyLoader(unittest.TestCase):
    def _loader(self):
        return EventBodyLoader()

    def _data(self, bid="body_001"):
        return {
            "body_id": bid,
            "name": f"Zone {bid}",
            "scope": "Global",
            "body_state": "Idle",
        }

    def test_load_manifest(self):
        loader = self._loader()
        m = loader.load_manifest(self._data())
        self.assertIsInstance(m, EventBodyManifest)
        self.assertEqual(m.body_id, "body_001")

    def test_load_manifest_name(self):
        loader = self._loader()
        m = loader.load_manifest(self._data())
        self.assertEqual(m.name, "Zone body_001")

    def test_load_manifest_scope(self):
        loader = self._loader()
        m = loader.load_manifest(self._data())
        self.assertEqual(m.scope, "Global")

    def test_load_batch(self):
        loader = self._loader()
        manifests = loader.load_batch([self._data("body_001"), self._data("body_002")])
        self.assertEqual(len(manifests), 2)

    def test_loaded_count(self):
        loader = self._loader()
        loader.load_manifest(self._data("body_001"))
        loader.load_manifest(self._data("body_002"))
        self.assertEqual(loader.loaded_count, 2)

    def test_validate(self):
        loader = self._loader()
        m = loader.load_manifest(self._data())
        self.assertTrue(loader.validate(m))

    def test_clear(self):
        loader = self._loader()
        loader.load_manifest(self._data())
        loader.clear()
        self.assertEqual(loader.loaded_count, 0)

    def test_trigger_config_loaded(self):
        loader = self._loader()
        data = self._data()
        data["trigger_config"] = {"trigger_type": "OnEnter", "priority": "High",
                                  "cooldown_ms": 1000.0}
        m = loader.load_manifest(data)
        self.assertEqual(m.trigger_config.trigger_type, "OnEnter")
        self.assertEqual(m.trigger_config.priority, "High")
        self.assertTrue(m.trigger_config.has_cooldown)

    def test_payload_loaded(self):
        loader = self._loader()
        data = self._data()
        data["payloads"] = [{"payload_id": "pay_001", "body_id": "body_001",
                             "event_type": "OnSignal", "recipients": ["r1"]}]
        m = loader.load_manifest(data)
        self.assertTrue(m.has_payloads)
        self.assertTrue(m.payloads[0].has_recipients)

    def test_save_and_load(self, tmp_path=None):
        import tempfile, os
        loader = self._loader()
        m = loader.load_manifest(self._data())
        with tempfile.TemporaryDirectory() as td:
            fpath = Path(td) / "body.json"
            loader.save_manifest(m, fpath)
            loader2 = EventBodyLoader()
            m2 = loader2.load_from_file(fpath)
            self.assertEqual(m2.body_id, m.body_id)
            self.assertEqual(m2.name, m.name)


if __name__ == "__main__":
    unittest.main()
