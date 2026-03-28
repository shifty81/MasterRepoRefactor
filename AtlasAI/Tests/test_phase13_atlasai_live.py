"""Tests for Phase 13 — AtlasAI live viewport, hot-reload, and multi-workspace."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LIVE_ROOT = REPO_ROOT / "AtlasAI/AIEngine/AtlasAIEngine/live"


class TestLiveModuleFilesExist(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((LIVE_ROOT / path).exists(), f"Missing: {LIVE_ROOT / path}")

    def test_init_exists(self):
        self._check("__init__.py")

    def test_live_viewport_exists(self):
        self._check("live_viewport.py")

    def test_hot_reload_exists(self):
        self._check("hot_reload.py")

    def test_multi_workspace_exists(self):
        self._check("multi_workspace.py")


class TestLiveViewportContent(unittest.TestCase):
    def _read(self):
        return (LIVE_ROOT / "live_viewport.py").read_text(encoding="utf-8")

    def test_has_live_viewport_config(self):
        self.assertIn("LiveViewportConfig", self._read())

    def test_has_live_viewport_client(self):
        self.assertIn("LiveViewportClient", self._read())

    def test_has_connect(self):
        self.assertIn("connect", self._read())

    def test_has_disconnect(self):
        self.assertIn("disconnect", self._read())

    def test_has_send_snapshot(self):
        self.assertIn("send_snapshot", self._read())

    def test_has_is_connected(self):
        self.assertIn("is_connected", self._read())

    def test_has_supports_viewport_attach(self):
        self.assertIn("supportsViewportAttach", self._read())


class TestHotReloadContent(unittest.TestCase):
    def _read(self):
        return (LIVE_ROOT / "hot_reload.py").read_text(encoding="utf-8")

    def test_has_hot_reload_config(self):
        self.assertIn("HotReloadConfig", self._read())

    def test_has_hot_reload_coordinator(self):
        self.assertIn("HotReloadCoordinator", self._read())

    def test_has_start(self):
        self.assertIn("start", self._read())

    def test_has_stop(self):
        self.assertIn("stop", self._read())

    def test_has_add_patch(self):
        self.assertIn("add_patch", self._read())

    def test_has_get_pending_patches(self):
        self.assertIn("get_pending_patches", self._read())

    def test_has_supports_live_patch(self):
        self.assertIn("supportsLivePatch", self._read())


class TestMultiWorkspaceContent(unittest.TestCase):
    def _read(self):
        return (LIVE_ROOT / "multi_workspace.py").read_text(encoding="utf-8")

    def test_has_workspace_session(self):
        self.assertIn("WorkspaceSession", self._read())

    def test_has_multi_workspace_manager(self):
        self.assertIn("MultiWorkspaceManager", self._read())

    def test_has_create_session(self):
        self.assertIn("create_session", self._read())

    def test_has_get_session(self):
        self.assertIn("get_session", self._read())

    def test_has_list_sessions(self):
        self.assertIn("list_sessions", self._read())

    def test_has_close_session(self):
        self.assertIn("close_session", self._read())


if __name__ == "__main__":
    unittest.main()
