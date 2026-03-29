"""Phase 37D — Tests for ScriptBodyRegistry.h and script_body_loader.py."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    ScriptBodyLoader,
    ScriptBodyManifest,
    ScriptConfigManifest,
    ScriptBindingManifest,
)


def _read_header(name: str) -> str:
    return (SCENE_DIR / f"{name}.h").read_text()


# ---------------------------------------------------------------------------
# ScriptBodyRegistry.h
# ---------------------------------------------------------------------------

class TestScriptBodyRegistryHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "ScriptBodyRegistry.h").exists())


class TestScriptBodyRegistryNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("ScriptBodyRegistry"))


class TestScriptBodyRegistryEnums(unittest.TestCase):
    def test_script_body_state_enum(self):
        self.assertIn("ScriptBodyState", _read_header("ScriptBodyRegistry"))

    def test_script_body_scope_enum(self):
        self.assertIn("ScriptBodyScope", _read_header("ScriptBodyRegistry"))

    def test_script_language_enum(self):
        self.assertIn("ScriptLanguage", _read_header("ScriptBodyRegistry"))

    def test_script_execution_mode_enum(self):
        self.assertIn("ScriptExecutionMode", _read_header("ScriptBodyRegistry"))

    def test_script_body_flags_enum(self):
        self.assertIn("ScriptBodyFlags", _read_header("ScriptBodyRegistry"))

    def test_running_state_value(self):
        self.assertIn("Running", _read_header("ScriptBodyRegistry"))

    def test_failed_state_value(self):
        self.assertIn("Failed", _read_header("ScriptBodyRegistry"))

    def test_lua_language_value(self):
        self.assertIn("Lua", _read_header("ScriptBodyRegistry"))

    def test_python_language_value(self):
        self.assertIn("Python", _read_header("ScriptBodyRegistry"))

    def test_blueprint_language_value(self):
        self.assertIn("Blueprint", _read_header("ScriptBodyRegistry"))

    def test_immediate_mode_value(self):
        self.assertIn("Immediate", _read_header("ScriptBodyRegistry"))


class TestScriptBodyRegistryStructs(unittest.TestCase):
    def test_script_config_struct(self):
        self.assertIn("ScriptConfig", _read_header("ScriptBodyRegistry"))

    def test_script_binding_struct(self):
        self.assertIn("ScriptBinding", _read_header("ScriptBodyRegistry"))

    def test_script_body_record_struct(self):
        self.assertIn("ScriptBodyRecord", _read_header("ScriptBodyRegistry"))

    def test_script_path_in_config(self):
        self.assertIn("scriptPath", _read_header("ScriptBodyRegistry"))

    def test_target_id_in_binding(self):
        self.assertIn("targetId", _read_header("ScriptBodyRegistry"))

    def test_trigger_count_in_record(self):
        self.assertIn("triggerCount", _read_header("ScriptBodyRegistry"))


class TestScriptBodyRegistryMethods(unittest.TestCase):
    def test_register_body(self):
        self.assertIn("RegisterBody", _read_header("ScriptBodyRegistry"))

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_header("ScriptBodyRegistry"))

    def test_set_body_scope(self):
        self.assertIn("SetBodyScope", _read_header("ScriptBodyRegistry"))

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_header("ScriptBodyRegistry"))

    def test_set_script_language(self):
        self.assertIn("SetScriptLanguage", _read_header("ScriptBodyRegistry"))

    def test_execute_body(self):
        self.assertIn("ExecuteBody", _read_header("ScriptBodyRegistry"))

    def test_pause_body(self):
        self.assertIn("PauseBody", _read_header("ScriptBodyRegistry"))

    def test_resume_body(self):
        self.assertIn("ResumeBody", _read_header("ScriptBodyRegistry"))

    def test_get_body_by_id(self):
        self.assertIn("GetBodyById", _read_header("ScriptBodyRegistry"))

    def test_get_all_body_ids(self):
        self.assertIn("GetAllBodyIds", _read_header("ScriptBodyRegistry"))

    def test_get_bodies_by_scope(self):
        self.assertIn("GetBodiesByScope", _read_header("ScriptBodyRegistry"))

    def test_get_bodies_by_language(self):
        self.assertIn("GetBodiesByLanguage", _read_header("ScriptBodyRegistry"))

    def test_get_running_bodies(self):
        self.assertIn("GetRunningBodies", _read_header("ScriptBodyRegistry"))

    def test_get_failed_bodies(self):
        self.assertIn("GetFailedBodies", _read_header("ScriptBodyRegistry"))

    def test_add_script_config(self):
        self.assertIn("AddScriptConfig", _read_header("ScriptBodyRegistry"))

    def test_remove_script_config(self):
        self.assertIn("RemoveScriptConfig", _read_header("ScriptBodyRegistry"))

    def test_get_configs_by_body(self):
        self.assertIn("GetConfigsByBody", _read_header("ScriptBodyRegistry"))

    def test_add_binding(self):
        self.assertIn("AddBinding", _read_header("ScriptBodyRegistry"))

    def test_remove_binding(self):
        self.assertIn("RemoveBinding", _read_header("ScriptBodyRegistry"))

    def test_get_bindings_by_body(self):
        self.assertIn("GetBindingsByBody", _read_header("ScriptBodyRegistry"))

    def test_clear(self):
        self.assertIn("Clear", _read_header("ScriptBodyRegistry"))

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_header("ScriptBodyRegistry"))

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_header("ScriptBodyRegistry"))


# ---------------------------------------------------------------------------
# ScriptConfigManifest
# ---------------------------------------------------------------------------

class TestScriptConfigManifest(unittest.TestCase):
    def test_default_language(self):
        cfg = ScriptConfigManifest()
        self.assertEqual(cfg.language, "Lua")

    def test_default_execution_mode(self):
        cfg = ScriptConfigManifest()
        self.assertEqual(cfg.execution_mode, "Immediate")

    def test_is_scheduled_false(self):
        cfg = ScriptConfigManifest(execution_mode="Immediate")
        self.assertFalse(cfg.is_scheduled)

    def test_is_scheduled_true(self):
        cfg = ScriptConfigManifest(execution_mode="Scheduled")
        self.assertTrue(cfg.is_scheduled)

    def test_has_script_false(self):
        cfg = ScriptConfigManifest()
        self.assertFalse(cfg.has_script)

    def test_has_script_true(self):
        cfg = ScriptConfigManifest(script_path="scripts/my_script.lua")
        self.assertTrue(cfg.has_script)

    def test_is_safe_true(self):
        cfg = ScriptConfigManifest(sandboxed=True)
        self.assertTrue(cfg.is_safe)

    def test_is_safe_false(self):
        cfg = ScriptConfigManifest(sandboxed=False)
        self.assertFalse(cfg.is_safe)


# ---------------------------------------------------------------------------
# ScriptBindingManifest
# ---------------------------------------------------------------------------

class TestScriptBindingManifest(unittest.TestCase):
    def test_binding_id(self):
        b = ScriptBindingManifest(binding_id="bind_001", body_id="body_001")
        self.assertEqual(b.binding_id, "bind_001")

    def test_body_id(self):
        b = ScriptBindingManifest(binding_id="bind_001", body_id="body_001")
        self.assertEqual(b.body_id, "body_001")

    def test_has_target_false(self):
        b = ScriptBindingManifest(binding_id="bind_001", body_id="body_001")
        self.assertFalse(b.has_target)

    def test_has_target_true(self):
        b = ScriptBindingManifest(binding_id="bind_001", body_id="body_001", target_id="actor_001")
        self.assertTrue(b.has_target)

    def test_has_handler_false(self):
        b = ScriptBindingManifest(binding_id="bind_001", body_id="body_001")
        self.assertFalse(b.has_handler)

    def test_has_handler_true(self):
        b = ScriptBindingManifest(binding_id="bind_001", body_id="body_001", handler_name="OnTick")
        self.assertTrue(b.has_handler)

    def test_is_active_true(self):
        b = ScriptBindingManifest(binding_id="bind_001", body_id="body_001", active=True)
        self.assertTrue(b.is_active)

    def test_is_active_false(self):
        b = ScriptBindingManifest(binding_id="bind_001", body_id="body_001", active=False)
        self.assertFalse(b.is_active)


# ---------------------------------------------------------------------------
# ScriptBodyManifest
# ---------------------------------------------------------------------------

class TestScriptBodyManifest(unittest.TestCase):
    def test_body_id(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript")
        self.assertEqual(m.body_id, "body_001")

    def test_name(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript")
        self.assertEqual(m.name, "SpawnScript")

    def test_default_scope(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript")
        self.assertEqual(m.scope, "Global")

    def test_default_body_state(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript")
        self.assertEqual(m.body_state, "Idle")

    def test_is_running_false(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript", body_state="Idle")
        self.assertFalse(m.is_running)

    def test_is_running_true(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript", body_state="Running")
        self.assertTrue(m.is_running)

    def test_is_failed_false(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript", body_state="Idle")
        self.assertFalse(m.is_failed)

    def test_is_failed_true(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript", body_state="Failed")
        self.assertTrue(m.is_failed)

    def test_has_bindings_false(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript")
        self.assertFalse(m.has_bindings)

    def test_has_bindings_true(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript",
                               bindings=[ScriptBindingManifest(binding_id="b1", body_id="body_001")])
        self.assertTrue(m.has_bindings)

    def test_has_error_false(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript")
        self.assertFalse(m.has_error)

    def test_has_error_true(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript", last_error="nil ref")
        self.assertTrue(m.has_error)


# ---------------------------------------------------------------------------
# ScriptBodyLoader
# ---------------------------------------------------------------------------

class TestScriptBodyLoader(unittest.TestCase):
    def setUp(self):
        self.loader = ScriptBodyLoader()

    def test_load_manifest(self):
        data = {"body_id": "body_001", "name": "SpawnScript"}
        manifest = self.loader.load_manifest(data)
        self.assertEqual(manifest.body_id, "body_001")

    def test_load_manifest_name(self):
        data = {"body_id": "body_001", "name": "SpawnScript"}
        manifest = self.loader.load_manifest(data)
        self.assertEqual(manifest.name, "SpawnScript")

    def test_load_manifest_scope(self):
        data = {"body_id": "body_001", "name": "SpawnScript", "scope": "Scene"}
        manifest = self.loader.load_manifest(data)
        self.assertEqual(manifest.scope, "Scene")

    def test_load_batch(self):
        data_list = [
            {"body_id": "body_001", "name": "ScriptA"},
            {"body_id": "body_002", "name": "ScriptB"},
        ]
        manifests = self.loader.load_batch(data_list)
        self.assertEqual(len(manifests), 2)

    def test_loaded_count(self):
        data = {"body_id": "body_001", "name": "SpawnScript"}
        self.loader.load_manifest(data)
        self.assertEqual(self.loader.loaded_count, 1)

    def test_validate(self):
        m = ScriptBodyManifest(body_id="body_001", name="SpawnScript")
        self.assertTrue(self.loader.validate(m))

    def test_clear(self):
        data = {"body_id": "body_001", "name": "SpawnScript"}
        self.loader.load_manifest(data)
        self.loader.clear()
        self.assertEqual(self.loader.loaded_count, 0)

    def test_script_config_loaded(self):
        data = {
            "body_id": "body_001",
            "name": "SpawnScript",
            "script_config": {
                "script_path": "scripts/spawn.lua",
                "language": "Lua",
                "execution_mode": "Deferred",
            },
        }
        manifest = self.loader.load_manifest(data)
        self.assertEqual(manifest.script_config.script_path, "scripts/spawn.lua")
        self.assertEqual(manifest.script_config.language, "Lua")
        self.assertEqual(manifest.script_config.execution_mode, "Deferred")

    def test_binding_loaded(self):
        data = {
            "body_id": "body_001",
            "name": "SpawnScript",
            "bindings": [
                {
                    "binding_id": "bind_001",
                    "body_id": "body_001",
                    "target_id": "actor_001",
                    "handler_name": "OnSpawn",
                }
            ],
        }
        manifest = self.loader.load_manifest(data)
        self.assertEqual(len(manifest.bindings), 1)
        self.assertEqual(manifest.bindings[0].binding_id, "bind_001")
        self.assertEqual(manifest.bindings[0].target_id, "actor_001")
        self.assertEqual(manifest.bindings[0].handler_name, "OnSpawn")

    def test_save_and_load(self):
        import tempfile, os
        m = ScriptBodyManifest(body_id="body_save", name="SaveTest", scope="Local",
                               body_state="Idle", language="Python")
        # Use a path relative to the project to avoid /tmp
        save_path = REPO_ROOT / "AtlasAI" / "Tests" / "_test_script_body_save.json"
        try:
            self.loader.save_manifest(m, save_path)
            loader2 = ScriptBodyLoader()
            loaded = loader2.load_from_file(save_path)
            self.assertEqual(loaded.body_id, "body_save")
            self.assertEqual(loaded.name, "SaveTest")
            self.assertEqual(loaded.scope, "Local")
        finally:
            if save_path.exists():
                save_path.unlink()


if __name__ == "__main__":
    unittest.main()
