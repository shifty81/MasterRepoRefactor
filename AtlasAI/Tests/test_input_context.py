"""Tests for B1 (InputContextManager) and B2 (RenderViewport)."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# =============================================================================
# B1 — Input Context System
# =============================================================================

class TestInputContextManagerExists(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_input_context_manager_header(self):
        self._check("Atlas/Engine/Input/InputContextManager.h")

    def test_input_context_manager_source(self):
        self._check("Atlas/Engine/Input/InputContextManager.cpp")


class TestInputContextManagerContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Engine/Input/InputContextManager.h").read_text(encoding="utf-8")

    def test_has_einput_context_enum(self):
        self.assertIn("EInputContext", self._read())

    def test_has_emouse_capture_mode_enum(self):
        self.assertIn("EMouseCaptureMode", self._read())

    def test_has_remappable_binding(self):
        self.assertIn("RemappableBinding", self._read())

    def test_has_keybind_config(self):
        self.assertIn("KeybindConfig", self._read())

    def test_has_context_transition(self):
        self.assertIn("ContextTransition", self._read())

    def test_has_push_context(self):
        self.assertIn("PushContext", self._read())

    def test_has_pop_context(self):
        self.assertIn("PopContext", self._read())

    def test_has_set_context(self):
        self.assertIn("SetContext", self._read())

    def test_has_current_context(self):
        self.assertIn("CurrentContext", self._read())

    def test_has_is_game_active(self):
        self.assertIn("IsGameActive", self._read())

    def test_has_is_editor_active(self):
        self.assertIn("IsEditorActive", self._read())

    def test_has_set_mouse_capture(self):
        self.assertIn("SetMouseCapture", self._read())

    def test_has_apply_default_mouse_policy(self):
        self.assertIn("ApplyDefaultMousePolicy", self._read())

    def test_has_load_keybind_config(self):
        self.assertIn("LoadKeybindConfig", self._read())

    def test_has_remap(self):
        self.assertIn("Remap", self._read())

    def test_has_reset_to_default(self):
        self.assertIn("ResetToDefault", self._read())

    def test_has_reset_all_to_default(self):
        self.assertIn("ResetAllToDefault", self._read())

    def test_has_should_dispatch(self):
        self.assertIn("ShouldDispatch", self._read())

    def test_has_route_press(self):
        self.assertIn("RoutePress", self._read())

    def test_has_route_release(self):
        self.assertIn("RouteRelease", self._read())

    def test_has_context_changed_callback(self):
        self.assertIn("ContextChangedCallback", self._read())

    def test_has_transition_history(self):
        self.assertIn("GetTransitionHistory", self._read())

    def test_context_types_cover_key_cases(self):
        text = self._read()
        for ctx in ["Game", "UI", "Editor", "EditorModal", "Debug"]:
            self.assertIn(ctx, text, f"Missing context: {ctx}")

    def test_mouse_modes_cover_key_cases(self):
        text = self._read()
        for mode in ["Free", "Locked", "Confined"]:
            self.assertIn(mode, text, f"Missing mouse mode: {mode}")


class TestInputContextManagerImpl(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Engine/Input/InputContextManager.cpp").read_text(encoding="utf-8")

    def test_game_context_locks_mouse(self):
        text = self._read()
        self.assertIn("Locked", text)
        self.assertIn("Game", text)

    def test_ui_context_frees_mouse(self):
        self.assertIn("Free", self._read())

    def test_editor_context_confines_mouse(self):
        self.assertIn("Confined", self._read())

    def test_gameplay_actions_blocked_in_ui(self):
        self.assertIn("ShouldDispatch", self._read())

    def test_fires_context_changed(self):
        self.assertIn("FireContextChanged", self._read())


class TestEngineCMakeUpdated(unittest.TestCase):
    def _cmake(self) -> str:
        return (REPO_ROOT / "Atlas/Engine/CMakeLists.txt").read_text(encoding="utf-8")

    def test_has_render_viewport(self):
        self.assertIn("RenderViewport.cpp", self._cmake())

    def test_has_input_context_manager(self):
        self.assertIn("InputContextManager.cpp", self._cmake())

    def test_has_input_dir(self):
        self.assertIn("/Input", self._cmake())


# =============================================================================
# B2 — Rendering Viewport
# =============================================================================

class TestRenderViewportExists(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_render_viewport_header(self):
        self._check("Atlas/Engine/Rendering/RenderViewport.h")

    def test_render_viewport_source(self):
        self._check("Atlas/Engine/Rendering/RenderViewport.cpp")


class TestRenderViewportContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Engine/Rendering/RenderViewport.h").read_text(encoding="utf-8")

    def test_has_erender_layer_enum(self):
        self.assertIn("ERenderLayer", self._read())

    def test_has_render_pass_stats(self):
        self.assertIn("RenderPassStats", self._read())

    def test_has_viewport_config(self):
        self.assertIn("ViewportConfig", self._read())

    def test_has_camera_state(self):
        self.assertIn("CameraState", self._read())

    def test_has_voxel_chunk_drawable(self):
        self.assertIn("VoxelChunkDrawable", self._read())

    def test_has_entity_drawable(self):
        self.assertIn("EntityDrawable", self._read())

    def test_has_debug_line(self):
        self.assertIn("DebugLine", self._read())

    def test_has_hud_element(self):
        self.assertIn("HUDElement", self._read())

    def test_has_selection_highlight(self):
        self.assertIn("SelectionHighlight", self._read())

    def test_has_submit_voxel_chunk(self):
        self.assertIn("SubmitVoxelChunk", self._read())

    def test_has_submit_entity(self):
        self.assertIn("SubmitEntity", self._read())

    def test_has_submit_debug_line(self):
        self.assertIn("SubmitDebugLine", self._read())

    def test_has_submit_hud_element(self):
        self.assertIn("SubmitHUDElement", self._read())

    def test_has_submit_selection_highlight(self):
        self.assertIn("SubmitSelectionHighlight", self._read())

    def test_has_begin_frame(self):
        self.assertIn("BeginFrame", self._read())

    def test_has_render_frame(self):
        self.assertIn("RenderFrame", self._read())

    def test_has_end_frame(self):
        self.assertIn("EndFrame", self._read())

    def test_has_set_layer_enabled(self):
        self.assertIn("SetLayerEnabled", self._read())

    def test_has_register_pass_delegate(self):
        self.assertIn("RegisterPassDelegate", self._read())

    def test_has_get_last_frame_stats(self):
        self.assertIn("GetLastFrameStats", self._read())

    def test_has_update_hud_element(self):
        self.assertIn("UpdateHUDElement", self._read())

    def test_has_resize(self):
        self.assertIn("Resize", self._read())

    def test_has_set_camera(self):
        self.assertIn("SetCamera", self._read())

    def test_layers_cover_all_required(self):
        text = self._read()
        for layer in ["Background", "VoxelChunks", "Entities", "Transparent",
                      "DebugOverlay", "HUD", "EditorOverlay", "ImGui"]:
            self.assertIn(layer, text, f"Missing render layer: {layer}")


if __name__ == "__main__":
    unittest.main()
