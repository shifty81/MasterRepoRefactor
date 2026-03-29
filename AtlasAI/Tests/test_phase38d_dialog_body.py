"""Phase 38D — Tests for DialogBodyRegistry.h and dialog_body_loader.py."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    DialogBodyLoader,
    DialogBodyManifest,
    DialogLineManifest,
    DialogResponseManifest,
)


def _read_header(name: str) -> str:
    return (SCENE_DIR / f"{name}.h").read_text()


# ---------------------------------------------------------------------------
# DialogBodyRegistry.h
# ---------------------------------------------------------------------------

class TestDialogBodyRegistryHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "DialogBodyRegistry.h").exists())


class TestDialogBodyRegistryNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("DialogBodyRegistry"))


class TestDialogBodyRegistryEnums(unittest.TestCase):
    def test_dialog_body_state_enum(self):
        self.assertIn("DialogBodyState", _read_header("DialogBodyRegistry"))

    def test_dialog_body_scope_enum(self):
        self.assertIn("DialogBodyScope", _read_header("DialogBodyRegistry"))

    def test_dialog_trigger_type_enum(self):
        self.assertIn("DialogTriggerType", _read_header("DialogBodyRegistry"))

    def test_dialog_flow_type_enum(self):
        self.assertIn("DialogFlowType", _read_header("DialogBodyRegistry"))

    def test_dialog_body_flags_enum(self):
        self.assertIn("DialogBodyFlags", _read_header("DialogBodyRegistry"))

    def test_active_state_value(self):
        self.assertIn("Active", _read_header("DialogBodyRegistry"))

    def test_speaking_state_value(self):
        self.assertIn("Speaking", _read_header("DialogBodyRegistry"))

    def test_npc_scope_value(self):
        self.assertIn("NPC", _read_header("DialogBodyRegistry"))

    def test_branching_flow_value(self):
        self.assertIn("Branching", _read_header("DialogBodyRegistry"))

    def test_voice_acted_flag(self):
        self.assertIn("VoiceActed", _read_header("DialogBodyRegistry"))


class TestDialogBodyRegistryStructs(unittest.TestCase):
    def test_dialog_line_config_struct(self):
        self.assertIn("DialogLineConfig", _read_header("DialogBodyRegistry"))

    def test_dialog_response_def_struct(self):
        self.assertIn("DialogResponseDef", _read_header("DialogBodyRegistry"))

    def test_dialog_body_record_struct(self):
        self.assertIn("DialogBodyRecord", _read_header("DialogBodyRegistry"))

    def test_response_ids_in_line_config(self):
        self.assertIn("responseIds", _read_header("DialogBodyRegistry"))

    def test_condition_expr_in_response(self):
        self.assertIn("conditionExpr", _read_header("DialogBodyRegistry"))

    def test_play_count_in_body_record(self):
        self.assertIn("playCount", _read_header("DialogBodyRegistry"))


class TestDialogBodyRegistryMethods(unittest.TestCase):
    def test_register_body(self):
        self.assertIn("RegisterBody", _read_header("DialogBodyRegistry"))

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_header("DialogBodyRegistry"))

    def test_set_body_scope(self):
        self.assertIn("SetBodyScope", _read_header("DialogBodyRegistry"))

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_header("DialogBodyRegistry"))

    def test_set_flow_type(self):
        self.assertIn("SetFlowType", _read_header("DialogBodyRegistry"))

    def test_set_trigger_type(self):
        self.assertIn("SetTriggerType", _read_header("DialogBodyRegistry"))

    def test_activate_body(self):
        self.assertIn("ActivateBody", _read_header("DialogBodyRegistry"))

    def test_complete_body(self):
        self.assertIn("CompleteBody", _read_header("DialogBodyRegistry"))

    def test_cancel_body(self):
        self.assertIn("CancelBody", _read_header("DialogBodyRegistry"))

    def test_disable_body(self):
        self.assertIn("DisableBody", _read_header("DialogBodyRegistry"))

    def test_get_body_by_id(self):
        self.assertIn("GetBodyById", _read_header("DialogBodyRegistry"))

    def test_get_all_body_ids(self):
        self.assertIn("GetAllBodyIds", _read_header("DialogBodyRegistry"))

    def test_get_bodies_by_scope(self):
        self.assertIn("GetBodiesByScope", _read_header("DialogBodyRegistry"))

    def test_get_bodies_by_flow(self):
        self.assertIn("GetBodiesByFlow", _read_header("DialogBodyRegistry"))

    def test_get_active_bodies(self):
        self.assertIn("GetActiveBodies", _read_header("DialogBodyRegistry"))

    def test_get_completed_bodies(self):
        self.assertIn("GetCompletedBodies", _read_header("DialogBodyRegistry"))

    def test_add_line(self):
        self.assertIn("AddLine", _read_header("DialogBodyRegistry"))

    def test_remove_line(self):
        self.assertIn("RemoveLine", _read_header("DialogBodyRegistry"))

    def test_get_line(self):
        self.assertIn("GetLine", _read_header("DialogBodyRegistry"))

    def test_get_lines_by_body(self):
        self.assertIn("GetLinesByBody", _read_header("DialogBodyRegistry"))

    def test_add_response(self):
        self.assertIn("AddResponse", _read_header("DialogBodyRegistry"))

    def test_remove_response(self):
        self.assertIn("RemoveResponse", _read_header("DialogBodyRegistry"))

    def test_get_response(self):
        self.assertIn("GetResponse", _read_header("DialogBodyRegistry"))

    def test_get_responses_by_line(self):
        self.assertIn("GetResponsesByLine", _read_header("DialogBodyRegistry"))

    def test_clear(self):
        self.assertIn("Clear", _read_header("DialogBodyRegistry"))

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_header("DialogBodyRegistry"))

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_header("DialogBodyRegistry"))


# ---------------------------------------------------------------------------
# DialogLineManifest
# ---------------------------------------------------------------------------

class TestDialogLineManifest(unittest.TestCase):
    def test_line_id(self):
        l = DialogLineManifest(line_id="line_001", body_id="body_001")
        self.assertEqual(l.line_id, "line_001")

    def test_body_id(self):
        l = DialogLineManifest(line_id="line_001", body_id="body_001")
        self.assertEqual(l.body_id, "body_001")

    def test_has_voice_false(self):
        l = DialogLineManifest(line_id="line_001", body_id="body_001")
        self.assertFalse(l.has_voice)

    def test_has_voice_true(self):
        l = DialogLineManifest(line_id="line_001", body_id="body_001", voice_asset_id="va_001")
        self.assertTrue(l.has_voice)

    def test_has_responses_false(self):
        l = DialogLineManifest(line_id="line_001", body_id="body_001")
        self.assertFalse(l.has_responses)

    def test_has_responses_true(self):
        l = DialogLineManifest(line_id="line_001", body_id="body_001", response_ids=["resp_001"])
        self.assertTrue(l.has_responses)

    def test_is_timed_false(self):
        l = DialogLineManifest(line_id="line_001", body_id="body_001", duration=0.0)
        self.assertFalse(l.is_timed)

    def test_is_timed_true(self):
        l = DialogLineManifest(line_id="line_001", body_id="body_001", duration=3.5)
        self.assertTrue(l.is_timed)


# ---------------------------------------------------------------------------
# DialogResponseManifest
# ---------------------------------------------------------------------------

class TestDialogResponseManifest(unittest.TestCase):
    def test_response_id(self):
        r = DialogResponseManifest(response_id="resp_001", line_id="line_001")
        self.assertEqual(r.response_id, "resp_001")

    def test_line_id(self):
        r = DialogResponseManifest(response_id="resp_001", line_id="line_001")
        self.assertEqual(r.line_id, "line_001")

    def test_has_condition_false(self):
        r = DialogResponseManifest(response_id="resp_001", line_id="line_001")
        self.assertFalse(r.has_condition)

    def test_has_condition_true(self):
        r = DialogResponseManifest(response_id="resp_001", line_id="line_001",
                                   condition_expr="player.rep > 50")
        self.assertTrue(r.has_condition)

    def test_has_next_false(self):
        r = DialogResponseManifest(response_id="resp_001", line_id="line_001")
        self.assertFalse(r.has_next)

    def test_has_next_true(self):
        r = DialogResponseManifest(response_id="resp_001", line_id="line_001",
                                   next_line_id="line_002")
        self.assertTrue(r.has_next)

    def test_is_default_false(self):
        r = DialogResponseManifest(response_id="resp_001", line_id="line_001")
        self.assertFalse(r.is_default)

    def test_is_default_true(self):
        r = DialogResponseManifest(response_id="resp_001", line_id="line_001", is_default=True)
        self.assertTrue(r.is_default)


# ---------------------------------------------------------------------------
# DialogBodyManifest
# ---------------------------------------------------------------------------

class TestDialogBodyManifest(unittest.TestCase):
    def test_body_id(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting")
        self.assertEqual(m.body_id, "body_001")

    def test_name(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting")
        self.assertEqual(m.name, "Merchant Greeting")

    def test_default_scope(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting")
        self.assertEqual(m.scope, "NPC")

    def test_default_body_state(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting")
        self.assertEqual(m.body_state, "Idle")

    def test_is_active_false(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting")
        self.assertFalse(m.is_active)

    def test_is_active_true(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting", body_state="Active")
        self.assertTrue(m.is_active)

    def test_is_completed_false(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting")
        self.assertFalse(m.is_completed)

    def test_is_completed_true(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting", body_state="Completed")
        self.assertTrue(m.is_completed)

    def test_is_branching_false(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting")
        self.assertFalse(m.is_branching)

    def test_is_branching_true(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting", flow_type="Branching")
        self.assertTrue(m.is_branching)

    def test_has_lines_false(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting")
        self.assertFalse(m.has_lines)

    def test_has_lines_true(self):
        l = DialogLineManifest(line_id="line_001", body_id="body_001")
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting", lines=[l])
        self.assertTrue(m.has_lines)

    def test_has_responses_false(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting")
        self.assertFalse(m.has_responses)

    def test_has_responses_true(self):
        r = DialogResponseManifest(response_id="resp_001", line_id="line_001")
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting", responses=[r])
        self.assertTrue(m.has_responses)

    def test_has_start_false(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting")
        self.assertFalse(m.has_start)

    def test_has_start_true(self):
        m = DialogBodyManifest(body_id="body_001", name="Merchant Greeting",
                               start_line_id="line_001")
        self.assertTrue(m.has_start)


# ---------------------------------------------------------------------------
# DialogBodyLoader
# ---------------------------------------------------------------------------

class TestDialogBodyLoader(unittest.TestCase):
    def setUp(self):
        self.loader = DialogBodyLoader()
        self.data = {
            "body_id": "body_001",
            "name": "Merchant Greeting",
            "scope": "NPC",
            "body_state": "Idle",
            "flow_type": "Linear",
            "trigger_type": "OnInteract",
            "start_line_id": "line_001",
            "play_count": 0,
            "lines": [
                {
                    "line_id": "line_001",
                    "body_id": "body_001",
                    "speaker_id": "merchant_001",
                    "text": "Welcome, traveler!",
                    "voice_asset_id": "",
                    "duration": 0.0,
                    "auto_advance": True,
                    "response_ids": ["resp_001"],
                }
            ],
            "responses": [
                {
                    "response_id": "resp_001",
                    "line_id": "line_001",
                    "response_text": "Hello!",
                    "next_line_id": "line_002",
                    "condition_expr": "",
                    "is_default": True,
                }
            ],
        }

    def test_load_manifest(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.body_id, "body_001")

    def test_load_manifest_name(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.name, "Merchant Greeting")

    def test_load_manifest_scope(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.scope, "NPC")

    def test_load_batch(self):
        manifests = self.loader.load_batch([self.data, self.data])
        self.assertEqual(len(manifests), 2)

    def test_loaded_count(self):
        self.loader.load_manifest(self.data)
        self.assertEqual(self.loader.loaded_count, 1)

    def test_validate(self):
        m = self.loader.load_manifest(self.data)
        self.assertTrue(self.loader.validate(m))

    def test_clear(self):
        self.loader.load_manifest(self.data)
        self.loader.clear()
        self.assertEqual(self.loader.loaded_count, 0)

    def test_line_loaded(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(len(m.lines), 1)
        self.assertEqual(m.lines[0].line_id, "line_001")
        self.assertEqual(m.lines[0].speaker_id, "merchant_001")
        self.assertEqual(m.lines[0].text, "Welcome, traveler!")

    def test_response_loaded(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(len(m.responses), 1)
        self.assertEqual(m.responses[0].response_id, "resp_001")
        self.assertEqual(m.responses[0].line_id, "line_001")
        self.assertEqual(m.responses[0].next_line_id, "line_002")

    def test_save_and_load(self):
        import tempfile, os
        m = self.loader.load_manifest(self.data)
        save_path = REPO_ROOT / "AtlasAI" / "Tests" / "_test_dialog_body_save.json"
        try:
            self.loader.save_manifest(m, save_path)
            loader2 = DialogBodyLoader()
            m2 = loader2.load_from_file(save_path)
            self.assertEqual(m2.body_id, "body_001")
            self.assertEqual(m2.name, "Merchant Greeting")
        finally:
            if save_path.exists():
                save_path.unlink()


if __name__ == "__main__":
    unittest.main()
