"""Tests for Phase 15 remaining hookup systems — IK, FPS, CharacterEditor, Mech."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RUNTIME = REPO_ROOT / "NovaForge/Runtime"


# ---------------------------------------------------------------------------
# IKAnimationBridge
# ---------------------------------------------------------------------------

class TestIKAnimationBridgeFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((RUNTIME / path).exists(), f"Missing: {RUNTIME / path}")

    def test_header_exists(self):
        self._check("Player/IKAnimationBridge.h")

    def test_source_exists(self):
        self._check("Player/IKAnimationBridge.cpp")


class TestIKAnimationBridgeContent(unittest.TestCase):
    def _read(self):
        return (RUNTIME / "Player/IKAnimationBridge.h").read_text(encoding="utf-8")

    def test_has_class(self):
        self.assertIn("IKAnimationBridge", self._read())

    def test_has_initialize(self):
        self.assertIn("Initialize", self._read())

    def test_has_shutdown(self):
        self.assertIn("Shutdown", self._read())

    def test_has_register_character(self):
        self.assertIn("RegisterCharacter", self._read())

    def test_has_update_from_character_state(self):
        self.assertIn("UpdateFromCharacterState", self._read())

    def test_has_tick(self):
        self.assertIn("Tick", self._read())

    def test_has_get_ik_target_count(self):
        self.assertIn("GetIKTargetCount", self._read())


# ---------------------------------------------------------------------------
# FPSRenderingBridge
# ---------------------------------------------------------------------------

class TestFPSRenderingBridgeFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((RUNTIME / path).exists(), f"Missing: {RUNTIME / path}")

    def test_header_exists(self):
        self._check("Rendering/FPSRenderingBridge.h")

    def test_source_exists(self):
        self._check("Rendering/FPSRenderingBridge.cpp")


class TestFPSRenderingBridgeContent(unittest.TestCase):
    def _read(self):
        return (RUNTIME / "Rendering/FPSRenderingBridge.h").read_text(encoding="utf-8")

    def test_has_class(self):
        self.assertIn("FPSRenderingBridge", self._read())

    def test_has_initialize(self):
        self.assertIn("Initialize", self._read())

    def test_has_shutdown(self):
        self.assertIn("Shutdown", self._read())

    def test_has_register_character(self):
        self.assertIn("RegisterCharacter", self._read())

    def test_has_submit_for_rendering(self):
        self.assertIn("SubmitForRendering", self._read())

    def test_has_is_visible(self):
        self.assertIn("IsVisible", self._read())

    def test_has_tick(self):
        self.assertIn("Tick", self._read())


# ---------------------------------------------------------------------------
# CharacterEditorBridge
# ---------------------------------------------------------------------------

class TestCharacterEditorBridgeFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((RUNTIME / path).exists(), f"Missing: {RUNTIME / path}")

    def test_header_exists(self):
        self._check("Player/CharacterEditorBridge.h")

    def test_source_exists(self):
        self._check("Player/CharacterEditorBridge.cpp")


class TestCharacterEditorBridgeContent(unittest.TestCase):
    def _read(self):
        return (RUNTIME / "Player/CharacterEditorBridge.h").read_text(encoding="utf-8")

    def test_has_class(self):
        self.assertIn("CharacterEditorBridge", self._read())

    def test_has_initialize(self):
        self.assertIn("Initialize", self._read())

    def test_has_shutdown(self):
        self.assertIn("Shutdown", self._read())

    def test_has_open_character_editor(self):
        self.assertIn("OpenCharacterEditor", self._read())

    def test_has_close_character_editor(self):
        self.assertIn("CloseCharacterEditor", self._read())

    def test_has_is_editor_open(self):
        self.assertIn("IsEditorOpen", self._read())

    def test_has_apply_editor_state(self):
        self.assertIn("ApplyEditorState", self._read())


# ---------------------------------------------------------------------------
# MechGameplayBridge
# ---------------------------------------------------------------------------

class TestMechGameplayBridgeFiles(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((RUNTIME / path).exists(), f"Missing: {RUNTIME / path}")

    def test_header_exists(self):
        self._check("Gameplay/MechGameplayBridge.h")

    def test_source_exists(self):
        self._check("Gameplay/MechGameplayBridge.cpp")


class TestMechGameplayBridgeContent(unittest.TestCase):
    def _read(self):
        return (RUNTIME / "Gameplay/MechGameplayBridge.h").read_text(encoding="utf-8")

    def test_has_class(self):
        self.assertIn("MechGameplayBridge", self._read())

    def test_has_initialize(self):
        self.assertIn("Initialize", self._read())

    def test_has_shutdown(self):
        self.assertIn("Shutdown", self._read())

    def test_has_register_character(self):
        self.assertIn("RegisterCharacter", self._read())

    def test_has_on_enter_mech_request(self):
        self.assertIn("OnEnterMechRequest", self._read())

    def test_has_on_exit_mech_request(self):
        self.assertIn("OnExitMechRequest", self._read())

    def test_has_is_in_mech(self):
        self.assertIn("IsInMech", self._read())

    def test_has_tick(self):
        self.assertIn("Tick", self._read())


# ---------------------------------------------------------------------------
# Phase 13 remaining — live modules
# ---------------------------------------------------------------------------

class TestCodegenDiffRelayFiles(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            (REPO_ROOT / "AtlasAI/AIEngine/AtlasAIEngine/live/codegen_diff_relay.py").exists()
        )


class TestCodegenDiffRelayContent(unittest.TestCase):
    def _read(self):
        return (
            REPO_ROOT / "AtlasAI/AIEngine/AtlasAIEngine/live/codegen_diff_relay.py"
        ).read_text(encoding="utf-8")

    def test_has_diff_entry(self):
        self.assertIn("DiffEntry", self._read())

    def test_has_codegen_diff_relay_class(self):
        self.assertIn("CodegenDiffRelay", self._read())

    def test_has_submit_diff(self):
        self.assertIn("submit_diff", self._read())

    def test_has_get_pending(self):
        self.assertIn("get_pending", self._read())

    def test_has_apply_diff(self):
        self.assertIn("apply_diff", self._read())

    def test_has_reject_diff(self):
        self.assertIn("reject_diff", self._read())

    def test_has_list_applied(self):
        self.assertIn("list_applied", self._read())


class TestBuildStreamRelayFiles(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(
            (REPO_ROOT / "AtlasAI/AIEngine/AtlasAIEngine/live/build_stream_relay.py").exists()
        )


class TestBuildStreamRelayContent(unittest.TestCase):
    def _read(self):
        return (
            REPO_ROOT / "AtlasAI/AIEngine/AtlasAIEngine/live/build_stream_relay.py"
        ).read_text(encoding="utf-8")

    def test_has_build_event(self):
        self.assertIn("BuildEvent", self._read())

    def test_has_build_stream_relay_class(self):
        self.assertIn("BuildStreamRelay", self._read())

    def test_has_publish(self):
        self.assertIn("publish", self._read())

    def test_has_subscribe(self):
        self.assertIn("subscribe", self._read())

    def test_has_unsubscribe(self):
        self.assertIn("unsubscribe", self._read())

    def test_has_get_history(self):
        self.assertIn("get_history", self._read())

    def test_has_subscriber_count(self):
        self.assertIn("subscriber_count", self._read())
