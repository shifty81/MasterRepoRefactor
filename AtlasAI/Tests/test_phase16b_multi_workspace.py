"""Phase 16B — Multi-Workspace tests."""
from __future__ import annotations

import unittest
from pathlib import Path

from AtlasAI.AIEngine.AtlasAIEngine.live.multi_workspace import (
    MultiWorkspaceManager,
    WorkspaceChangedEvent,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestWorkspaceSwitcherPanelHeader(unittest.TestCase):
    def setUp(self):
        self.header = (
            REPO_ROOT / "Atlas" / "Editor" / "Panels" / "WorkspaceSwitcherPanel.h"
        )
        self.content = self.header.read_text()

    def test_file_exists(self):
        self.assertTrue(self.header.exists())

    def test_pragma_once(self):
        self.assertIn("#pragma once", self.content)

    def test_switch_to_method(self):
        self.assertIn("SwitchTo", self.content)

    def test_refresh_method(self):
        self.assertIn("Refresh", self.content)

    def test_get_active_workspace_id_method(self):
        self.assertIn("GetActiveWorkspaceId", self.content)

    def test_active_workspace_id_member(self):
        self.assertIn("m_activeWorkspaceId", self.content)

    def test_namespace(self):
        self.assertIn("Atlas::Editor", self.content)

    def test_class_declaration(self):
        self.assertIn("WorkspaceSwitcherPanel", self.content)


class TestWorkspaceChangedEvent(unittest.TestCase):
    def test_has_workspace_id_field(self):
        evt = WorkspaceChangedEvent(workspace_id="w1", event_type="activated")
        self.assertEqual(evt.workspace_id, "w1")

    def test_has_event_type_field(self):
        evt = WorkspaceChangedEvent(workspace_id="w1", event_type="closed")
        self.assertEqual(evt.event_type, "closed")

    def test_is_dataclass(self):
        import dataclasses
        self.assertTrue(dataclasses.is_dataclass(WorkspaceChangedEvent))


class TestMultiWorkspaceManagerActivate(unittest.TestCase):
    def setUp(self):
        self.mgr = MultiWorkspaceManager()

    def test_get_active_session_none_initially(self):
        self.assertIsNone(self.mgr.get_active_session())

    def test_activate_returns_true_for_known_session(self):
        session = self.mgr.create_session("/proj", 8000)
        self.assertTrue(self.mgr.activate(session.session_id))

    def test_activate_unknown_returns_false(self):
        self.assertFalse(self.mgr.activate("nonexistent"))

    def test_get_active_session_returns_correct_session(self):
        session = self.mgr.create_session("/proj", 8000)
        self.mgr.activate(session.session_id)
        active = self.mgr.get_active_session()
        self.assertIs(active, session)

    def test_activate_switches_active_session(self):
        s1 = self.mgr.create_session("/proj1", 8001)
        s2 = self.mgr.create_session("/proj2", 8002)
        self.mgr.activate(s1.session_id)
        self.assertIs(self.mgr.get_active_session(), s1)
        self.mgr.activate(s2.session_id)
        self.assertIs(self.mgr.get_active_session(), s2)


class TestMultiWorkspaceManagerClose(unittest.TestCase):
    def setUp(self):
        self.mgr = MultiWorkspaceManager()

    def test_close_returns_true_for_known_session(self):
        session = self.mgr.create_session("/proj", 8000)
        self.assertTrue(self.mgr.close(session.session_id))

    def test_close_marks_session_inactive(self):
        session = self.mgr.create_session("/proj", 8000)
        self.mgr.close(session.session_id)
        self.assertFalse(session.active)

    def test_close_unknown_returns_false(self):
        self.assertFalse(self.mgr.close("nonexistent"))

    def test_close_active_session_clears_active(self):
        session = self.mgr.create_session("/proj", 8000)
        self.mgr.activate(session.session_id)
        self.mgr.close(session.session_id)
        self.assertIsNone(self.mgr.get_active_session())


if __name__ == "__main__":
    unittest.main()
