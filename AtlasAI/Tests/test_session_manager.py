"""Tests for AtlasAI core/session_manager.py — SessionManager."""

import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "AIEngine" / "AtlasAIEngine"))

from core.session_manager import Session, SessionManager, SessionState


class TestSessionManagerCreate(unittest.TestCase):
    def setUp(self):
        self.manager = SessionManager()

    def test_create_session_returns_session(self):
        session = self.manager.create_session("proj-1", "client-a")
        self.assertIsInstance(session, Session)

    def test_create_session_fields_populated(self):
        session = self.manager.create_session("proj-1", "client-a")
        self.assertEqual(session.project_id, "proj-1")
        self.assertEqual(session.client_id, "client-a")
        self.assertTrue(session.session_id)

    def test_create_session_initial_state_is_active(self):
        session = self.manager.create_session("proj-1", "client-a")
        self.assertEqual(session.state, SessionState.ACTIVE)

    def test_create_session_has_created_at(self):
        session = self.manager.create_session("proj-1", "client-a")
        self.assertTrue(session.created_at)

    def test_create_session_appears_in_list_active(self):
        session = self.manager.create_session("proj-1", "client-a")
        active_ids = [s.session_id for s in self.manager.list_active()]
        self.assertIn(session.session_id, active_ids)

    def test_create_session_appears_in_list_all(self):
        session = self.manager.create_session("proj-1", "client-a")
        all_ids = [s.session_id for s in self.manager.list_all()]
        self.assertIn(session.session_id, all_ids)

    def test_create_session_unique_ids(self):
        s1 = self.manager.create_session("proj-1", "client-a")
        s2 = self.manager.create_session("proj-1", "client-a")
        self.assertNotEqual(s1.session_id, s2.session_id)

    def test_create_session_to_dict_contains_all_keys(self):
        session = self.manager.create_session("proj-1", "client-a")
        d = session.to_dict()
        for key in ("session_id", "project_id", "client_id", "state", "created_at", "last_active"):
            self.assertIn(key, d)

    def test_create_session_to_dict_state_is_string(self):
        session = self.manager.create_session("proj-1", "client-a")
        self.assertEqual(session.to_dict()["state"], "active")


class TestSessionManagerStateTransitions(unittest.TestCase):
    def setUp(self):
        self.manager = SessionManager()
        self.session = self.manager.create_session("proj-2", "client-b")
        self.sid = self.session.session_id

    def test_suspend_active_session_succeeds(self):
        result = self.manager.suspend_session(self.sid)
        self.assertTrue(result)

    def test_suspend_sets_state_suspended(self):
        self.manager.suspend_session(self.sid)
        self.assertEqual(self.session.state, SessionState.SUSPENDED)

    def test_resume_suspended_session_succeeds(self):
        self.manager.suspend_session(self.sid)
        result = self.manager.resume_session(self.sid)
        self.assertTrue(result)

    def test_resume_sets_state_active(self):
        self.manager.suspend_session(self.sid)
        self.manager.resume_session(self.sid)
        self.assertEqual(self.session.state, SessionState.ACTIVE)

    def test_terminate_session_returns_true(self):
        result = self.manager.terminate_session(self.sid)
        self.assertTrue(result)

    def test_terminate_sets_state_terminated(self):
        self.manager.terminate_session(self.sid)
        self.assertEqual(self.session.state, SessionState.TERMINATED)

    def test_double_suspend_fails(self):
        self.manager.suspend_session(self.sid)
        result = self.manager.suspend_session(self.sid)
        self.assertFalse(result)

    def test_resume_active_session_fails(self):
        result = self.manager.resume_session(self.sid)
        self.assertFalse(result)

    def test_suspend_terminated_session_fails(self):
        self.manager.terminate_session(self.sid)
        result = self.manager.suspend_session(self.sid)
        self.assertFalse(result)

    def test_resume_terminated_session_fails(self):
        self.manager.terminate_session(self.sid)
        result = self.manager.resume_session(self.sid)
        self.assertFalse(result)

    def test_terminate_nonexistent_returns_false(self):
        result = self.manager.terminate_session("no-such-id")
        self.assertFalse(result)

    def test_resume_updates_last_active(self):
        old_last_active = self.session.last_active
        self.manager.suspend_session(self.sid)
        time.sleep(0.01)
        self.manager.resume_session(self.sid)
        self.assertGreaterEqual(self.session.last_active, old_last_active)


class TestSessionManagerQueries(unittest.TestCase):
    def setUp(self):
        self.manager = SessionManager()
        self.s1 = self.manager.create_session("proj-3", "client-c")
        self.s2 = self.manager.create_session("proj-3", "client-d")
        self.s3 = self.manager.create_session("proj-4", "client-e")

    def test_get_session_by_id(self):
        result = self.manager.get_session(self.s1.session_id)
        self.assertIs(result, self.s1)

    def test_get_session_unknown_id_returns_none(self):
        result = self.manager.get_session("unknown")
        self.assertIsNone(result)

    def test_list_all_includes_all_sessions(self):
        all_sessions = self.manager.list_all()
        self.assertEqual(len(all_sessions), 3)

    def test_count_active_all_active(self):
        self.assertEqual(self.manager.count_active(), 3)

    def test_count_active_after_terminate(self):
        self.manager.terminate_session(self.s1.session_id)
        self.assertEqual(self.manager.count_active(), 2)

    def test_list_active_excludes_terminated(self):
        self.manager.terminate_session(self.s1.session_id)
        active_ids = [s.session_id for s in self.manager.list_active()]
        self.assertNotIn(self.s1.session_id, active_ids)

    def test_list_active_excludes_suspended(self):
        self.manager.suspend_session(self.s2.session_id)
        active_ids = [s.session_id for s in self.manager.list_active()]
        self.assertNotIn(self.s2.session_id, active_ids)

    def test_list_all_includes_terminated(self):
        self.manager.terminate_session(self.s3.session_id)
        all_ids = [s.session_id for s in self.manager.list_all()]
        self.assertIn(self.s3.session_id, all_ids)

    def test_empty_manager_count_active_is_zero(self):
        m = SessionManager()
        self.assertEqual(m.count_active(), 0)

    def test_empty_manager_list_active_is_empty(self):
        m = SessionManager()
        self.assertEqual(m.list_active(), [])


if __name__ == "__main__":
    unittest.main()
