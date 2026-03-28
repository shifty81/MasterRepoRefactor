"""Tests for Phase 15 — NovaForge runtime gameplay hookup systems."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RUNTIME = REPO_ROOT / "NovaForge/Runtime"


class TestPlayerControllerHookupFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((RUNTIME / path).exists(), f"Missing: {RUNTIME / path}")

    def test_header_exists(self):
        self._check("Player/PlayerControllerHookup.h")

    def test_source_exists(self):
        self._check("Player/PlayerControllerHookup.cpp")


class TestPlayerControllerHookupContent(unittest.TestCase):
    def _read(self):
        return (RUNTIME / "Player/PlayerControllerHookup.h").read_text(encoding="utf-8")

    def test_has_class(self):
        self.assertIn("PlayerControllerHookup", self._read())

    def test_has_initialize(self):
        self.assertIn("Initialize", self._read())

    def test_has_shutdown(self):
        self.assertIn("Shutdown", self._read())

    def test_has_tick(self):
        self.assertIn("Tick", self._read())

    def test_has_on_movement_mode_changed(self):
        self.assertIn("OnMovementModeChanged", self._read())

    def test_has_dispatch_to_character_system(self):
        self.assertIn("DispatchToCharacterSystem", self._read())


class TestEquipmentToolBridgeFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((RUNTIME / path).exists(), f"Missing: {RUNTIME / path}")

    def test_header_exists(self):
        self._check("Interaction/EquipmentToolBridge.h")

    def test_source_exists(self):
        self._check("Interaction/EquipmentToolBridge.cpp")


class TestEquipmentToolBridgeContent(unittest.TestCase):
    def _read(self):
        return (RUNTIME / "Interaction/EquipmentToolBridge.h").read_text(encoding="utf-8")

    def test_has_class(self):
        self.assertIn("EquipmentToolBridge", self._read())

    def test_has_initialize(self):
        self.assertIn("Initialize", self._read())

    def test_has_on_tool_equipped(self):
        self.assertIn("OnToolEquipped", self._read())

    def test_has_on_tool_unequipped(self):
        self.assertIn("OnToolUnequipped", self._read())

    def test_has_get_active_tool_id(self):
        self.assertIn("GetActiveToolId", self._read())


class TestGameOrchestratorBootFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((RUNTIME / path).exists(), f"Missing: {RUNTIME / path}")

    def test_header_exists(self):
        self._check("Session/GameOrchestratorBoot.h")

    def test_source_exists(self):
        self._check("Session/GameOrchestratorBoot.cpp")


class TestGameOrchestratorBootContent(unittest.TestCase):
    def _read(self):
        return (RUNTIME / "Session/GameOrchestratorBoot.h").read_text(encoding="utf-8")

    def test_has_class(self):
        self.assertIn("GameOrchestratorBoot", self._read())

    def test_has_eboot_phase(self):
        self.assertIn("EBootPhase", self._read())

    def test_has_initialize(self):
        self.assertIn("Initialize", self._read())

    def test_has_run_boot(self):
        self.assertIn("RunBoot", self._read())

    def test_has_get_boot_phase(self):
        self.assertIn("GetBootPhase", self._read())

    def test_has_shutdown(self):
        self.assertIn("Shutdown", self._read())

    def test_has_gameplay_ready(self):
        self.assertIn("GameplayReady", self._read())


class TestSaveManagerHookupFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((RUNTIME / path).exists(), f"Missing: {RUNTIME / path}")

    def test_header_exists(self):
        self._check("SaveLoad/SaveManagerHookup.h")

    def test_source_exists(self):
        self._check("SaveLoad/SaveManagerHookup.cpp")


class TestSaveManagerHookupContent(unittest.TestCase):
    def _read(self):
        return (RUNTIME / "SaveLoad/SaveManagerHookup.h").read_text(encoding="utf-8")

    def test_has_class(self):
        self.assertIn("SaveManagerHookup", self._read())

    def test_has_initialize(self):
        self.assertIn("Initialize", self._read())

    def test_has_save_world(self):
        self.assertIn("SaveWorld", self._read())

    def test_has_load_world(self):
        self.assertIn("LoadWorld", self._read())

    def test_has_on_world_state_changed(self):
        self.assertIn("OnWorldStateChanged", self._read())

    def test_has_get_last_save_slot(self):
        self.assertIn("GetLastSaveSlot", self._read())


class TestRuntimeUIHookupFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((RUNTIME / path).exists(), f"Missing: {RUNTIME / path}")

    def test_header_exists(self):
        self._check("UI/RuntimeUIHookup.h")

    def test_source_exists(self):
        self._check("UI/RuntimeUIHookup.cpp")


class TestRuntimeUIHookupContent(unittest.TestCase):
    def _read(self):
        return (RUNTIME / "UI/RuntimeUIHookup.h").read_text(encoding="utf-8")

    def test_has_class(self):
        self.assertIn("RuntimeUIHookup", self._read())

    def test_has_initialize(self):
        self.assertIn("Initialize", self._read())

    def test_has_show_hud(self):
        self.assertIn("ShowHUD", self._read())

    def test_has_hide_hud(self):
        self.assertIn("HideHUD", self._read())

    def test_has_update_hud(self):
        self.assertIn("UpdateHUD", self._read())

    def test_has_is_hud_visible(self):
        self.assertIn("IsHUDVisible", self._read())


if __name__ == "__main__":
    unittest.main()
