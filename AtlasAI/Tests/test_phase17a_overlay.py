"""Phase 17A tests — Dev AI Phase 3: In-Editor Overlay."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Ensure AtlasAI package is importable
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))


class TestPhase17AHeadersExist(unittest.TestCase):
    """Verify all four overlay panel headers exist."""

    PANELS_DIR = REPO_ROOT / "Atlas" / "Editor" / "Panels"

    def test_ai_prompt_panel_header_exists(self):
        self.assertTrue((self.PANELS_DIR / "AIPromptPanel.h").exists())

    def test_ai_suggestion_panel_header_exists(self):
        self.assertTrue((self.PANELS_DIR / "AISuggestionPanel.h").exists())

    def test_ai_build_log_panel_header_exists(self):
        self.assertTrue((self.PANELS_DIR / "AIBuildLogPanel.h").exists())

    def test_ai_context_panel_header_exists(self):
        self.assertTrue((self.PANELS_DIR / "AIContextPanel.h").exists())


class TestPhase17AHeaderContent(unittest.TestCase):
    """Verify header content for overlay panels."""

    PANELS_DIR = REPO_ROOT / "Atlas" / "Editor" / "Panels"

    def _read(self, name):
        return (self.PANELS_DIR / name).read_text()

    def test_ai_prompt_panel_pragma_once(self):
        self.assertIn("#pragma once", self._read("AIPromptPanel.h"))

    def test_ai_prompt_panel_class_name(self):
        self.assertIn("class AIPromptPanel", self._read("AIPromptPanel.h"))

    def test_ai_prompt_panel_set_prompt(self):
        self.assertIn("SetPrompt", self._read("AIPromptPanel.h"))

    def test_ai_prompt_panel_submit(self):
        self.assertIn("Submit", self._read("AIPromptPanel.h"))

    def test_ai_prompt_panel_clear(self):
        self.assertIn("Clear", self._read("AIPromptPanel.h"))

    def test_ai_prompt_panel_on_submit_callback(self):
        self.assertIn("SetOnSubmitCallback", self._read("AIPromptPanel.h"))

    def test_ai_suggestion_panel_pragma_once(self):
        self.assertIn("#pragma once", self._read("AISuggestionPanel.h"))

    def test_ai_suggestion_panel_class_name(self):
        self.assertIn("class AISuggestionPanel", self._read("AISuggestionPanel.h"))

    def test_ai_suggestion_panel_load_suggestion(self):
        self.assertIn("LoadSuggestion", self._read("AISuggestionPanel.h"))

    def test_ai_suggestion_panel_approve(self):
        self.assertIn("Approve", self._read("AISuggestionPanel.h"))

    def test_ai_suggestion_panel_reject(self):
        self.assertIn("Reject", self._read("AISuggestionPanel.h"))

    def test_ai_build_log_panel_pragma_once(self):
        self.assertIn("#pragma once", self._read("AIBuildLogPanel.h"))

    def test_ai_build_log_panel_class_name(self):
        self.assertIn("class AIBuildLogPanel", self._read("AIBuildLogPanel.h"))

    def test_ai_build_log_panel_append_line(self):
        self.assertIn("AppendLine", self._read("AIBuildLogPanel.h"))

    def test_ai_build_log_panel_get_line_count(self):
        self.assertIn("GetLineCount", self._read("AIBuildLogPanel.h"))

    def test_ai_context_panel_pragma_once(self):
        self.assertIn("#pragma once", self._read("AIContextPanel.h"))

    def test_ai_context_panel_class_name(self):
        self.assertIn("class AIContextPanel", self._read("AIContextPanel.h"))

    def test_ai_context_panel_set_active_file(self):
        self.assertIn("SetActiveFile", self._read("AIContextPanel.h"))

    def test_ai_context_panel_add_symbol(self):
        self.assertIn("AddSymbol", self._read("AIContextPanel.h"))

    def test_ai_context_panel_set_model_status(self):
        self.assertIn("SetModelStatus", self._read("AIContextPanel.h"))


class TestPhase17AOverlayManagerFile(unittest.TestCase):
    """Verify overlay_manager.py exists."""

    LIVE_DIR = REPO_ROOT / "AtlasAI" / "AIEngine" / "AtlasAIEngine" / "live"

    def test_overlay_manager_exists(self):
        self.assertTrue((self.LIVE_DIR / "overlay_manager.py").exists())


class TestPhase17AOverlayState(unittest.TestCase):
    """Tests for OverlayState dataclass."""

    def setUp(self):
        from AtlasAIEngine.live.overlay_manager import OverlayState
        self.OverlayState = OverlayState

    def test_overlay_state_default_active_file(self):
        state = self.OverlayState()
        self.assertEqual(state.active_file, "")

    def test_overlay_state_default_model_status(self):
        state = self.OverlayState()
        self.assertEqual(state.model_status, "idle")

    def test_overlay_state_default_build_log_lines(self):
        state = self.OverlayState()
        self.assertEqual(state.build_log_lines, [])

    def test_overlay_state_default_symbols(self):
        state = self.OverlayState()
        self.assertEqual(state.symbols, [])

    def test_overlay_state_default_pending_diff(self):
        state = self.OverlayState()
        self.assertEqual(state.pending_diff, "")

    def test_overlay_state_field_assignment(self):
        state = self.OverlayState(active_file="foo.cpp", model_status="generating")
        self.assertEqual(state.active_file, "foo.cpp")
        self.assertEqual(state.model_status, "generating")


class TestPhase17AOverlayManager(unittest.TestCase):
    """Tests for OverlayManager behaviour."""

    def setUp(self):
        from AtlasAIEngine.live.overlay_manager import OverlayManager
        self.mgr = OverlayManager()

    def test_push_build_line_appends(self):
        self.mgr.push_build_line("line one")
        self.assertIn("line one", self.mgr.get_state().build_log_lines)

    def test_push_build_line_multiple(self):
        self.mgr.push_build_line("a")
        self.mgr.push_build_line("b")
        self.assertEqual(len(self.mgr.get_state().build_log_lines), 2)

    def test_clear_build_log(self):
        self.mgr.push_build_line("x")
        self.mgr.clear_build_log()
        self.assertEqual(self.mgr.get_state().build_log_lines, [])

    def test_push_suggestion_sets_pending_diff(self):
        self.mgr.push_suggestion("--- a/foo.cpp\n+++ b/foo.cpp")
        self.assertIn("foo.cpp", self.mgr.get_state().pending_diff)

    def test_approve_suggestion_returns_true(self):
        self.mgr.push_suggestion("diff text")
        result = self.mgr.approve_suggestion()
        self.assertTrue(result)

    def test_approve_suggestion_clears_diff(self):
        self.mgr.push_suggestion("diff text")
        self.mgr.approve_suggestion()
        self.assertEqual(self.mgr.get_state().pending_diff, "")

    def test_approve_suggestion_no_pending_returns_false(self):
        self.assertFalse(self.mgr.approve_suggestion())

    def test_reject_suggestion_returns_true(self):
        self.mgr.push_suggestion("diff text")
        result = self.mgr.reject_suggestion()
        self.assertTrue(result)

    def test_reject_suggestion_clears_diff(self):
        self.mgr.push_suggestion("diff text")
        self.mgr.reject_suggestion()
        self.assertEqual(self.mgr.get_state().pending_diff, "")

    def test_reject_suggestion_no_pending_returns_false(self):
        self.assertFalse(self.mgr.reject_suggestion())

    def test_set_active_file(self):
        self.mgr.set_active_file("Engine/src/main.cpp")
        self.assertEqual(self.mgr.get_state().active_file, "Engine/src/main.cpp")

    def test_set_model_status(self):
        self.mgr.set_model_status("generating")
        self.assertEqual(self.mgr.get_state().model_status, "generating")

    def test_add_symbol(self):
        self.mgr.add_symbol("MultiSelectionManager")
        self.assertIn("MultiSelectionManager", self.mgr.get_state().symbols)

    def test_add_symbol_no_duplicates(self):
        self.mgr.add_symbol("Foo")
        self.mgr.add_symbol("Foo")
        self.assertEqual(self.mgr.get_state().symbols.count("Foo"), 1)

    def test_clear_symbols(self):
        self.mgr.add_symbol("Foo")
        self.mgr.clear_symbols()
        self.assertEqual(self.mgr.get_state().symbols, [])

    def test_state_change_callback(self):
        calls = []
        self.mgr.set_on_state_change(lambda s: calls.append(s.model_status))
        self.mgr.set_model_status("busy")
        self.assertEqual(calls[-1], "busy")

    def test_get_state_returns_state(self):
        from AtlasAIEngine.live.overlay_manager import OverlayState
        self.assertIsInstance(self.mgr.get_state(), OverlayState)


if __name__ == "__main__":
    unittest.main()
