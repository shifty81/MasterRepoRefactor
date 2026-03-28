"""Tests for AtlasAI core/codegen_planner.py — CodegenPlanner."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "AIEngine" / "AtlasAIEngine"))

from core.codegen_planner import CodeProposal, CodegenPlanner, ProposalStatus


def _proposal_kwargs(**overrides):
    base = {
        "title": "Add feature X",
        "description": "Implements feature X in module Y.",
        "target_file": "src/module_y.py",
        "diff_preview": "--- a/src/module_y.py\n+++ b/src/module_y.py\n@@ -1 +1,2 @@\n+# feature X\n",
    }
    base.update(overrides)
    return base


class TestCodegenPlannerPropose(unittest.TestCase):
    def setUp(self):
        self.planner = CodegenPlanner()

    def test_propose_returns_string_id(self):
        pid = self.planner.propose(**_proposal_kwargs())
        self.assertIsInstance(pid, str)
        self.assertTrue(pid)

    def test_propose_creates_proposal(self):
        pid = self.planner.propose(**_proposal_kwargs())
        self.assertIsNotNone(self.planner.get(pid))

    def test_proposal_fields_title(self):
        pid = self.planner.propose(**_proposal_kwargs(title="My Title"))
        self.assertEqual(self.planner.get(pid).title, "My Title")

    def test_proposal_fields_description(self):
        pid = self.planner.propose(**_proposal_kwargs(description="Desc"))
        self.assertEqual(self.planner.get(pid).description, "Desc")

    def test_proposal_fields_target_file(self):
        pid = self.planner.propose(**_proposal_kwargs(target_file="foo/bar.py"))
        self.assertEqual(self.planner.get(pid).target_file, "foo/bar.py")

    def test_proposal_initial_status_is_pending(self):
        pid = self.planner.propose(**_proposal_kwargs())
        self.assertEqual(self.planner.get(pid).status, ProposalStatus.PENDING)

    def test_proposal_default_author_is_atlasai(self):
        pid = self.planner.propose(**_proposal_kwargs())
        self.assertEqual(self.planner.get(pid).author, "AtlasAI")

    def test_proposal_custom_author(self):
        pid = self.planner.propose(**_proposal_kwargs(author="dev-bot"))
        self.assertEqual(self.planner.get(pid).author, "dev-bot")

    def test_get_diff_returns_diff_preview(self):
        diff = "--- a/f\n+++ b/f\n+new line\n"
        pid = self.planner.propose(**_proposal_kwargs(diff_preview=diff))
        self.assertEqual(self.planner.get_diff(pid), diff)

    def test_get_diff_unknown_id_returns_none(self):
        self.assertIsNone(self.planner.get_diff("no-such-id"))

    def test_propose_multiple_unique_ids(self):
        ids = {self.planner.propose(**_proposal_kwargs()) for _ in range(5)}
        self.assertEqual(len(ids), 5)

    def test_to_dict_contains_all_keys(self):
        pid = self.planner.propose(**_proposal_kwargs())
        d = self.planner.get(pid).to_dict()
        for key in ("proposal_id", "title", "description", "target_file",
                    "diff_preview", "author", "status", "rejection_reason"):
            self.assertIn(key, d)


class TestCodegenPlannerApproveApply(unittest.TestCase):
    def setUp(self):
        self.planner = CodegenPlanner()
        self.pid = self.planner.propose(**_proposal_kwargs())

    def test_approve_pending_returns_true(self):
        self.assertTrue(self.planner.approve(self.pid))

    def test_approve_sets_status_approved(self):
        self.planner.approve(self.pid)
        self.assertEqual(self.planner.get(self.pid).status, ProposalStatus.APPROVED)

    def test_approve_already_approved_returns_false(self):
        self.planner.approve(self.pid)
        self.assertFalse(self.planner.approve(self.pid))

    def test_apply_approved_returns_true(self):
        self.planner.approve(self.pid)
        self.assertTrue(self.planner.apply(self.pid))

    def test_apply_sets_status_applied(self):
        self.planner.approve(self.pid)
        self.planner.apply(self.pid)
        self.assertEqual(self.planner.get(self.pid).status, ProposalStatus.APPLIED)

    def test_apply_sets_applied_patch(self):
        self.planner.approve(self.pid)
        self.planner.apply(self.pid)
        proposal = self.planner.get(self.pid)
        self.assertEqual(proposal.applied_patch, proposal.diff_preview)

    def test_cannot_apply_pending_directly(self):
        self.assertFalse(self.planner.apply(self.pid))

    def test_cannot_apply_twice(self):
        self.planner.approve(self.pid)
        self.planner.apply(self.pid)
        self.assertFalse(self.planner.apply(self.pid))

    def test_approve_nonexistent_returns_false(self):
        self.assertFalse(self.planner.approve("no-such-id"))

    def test_apply_nonexistent_returns_false(self):
        self.assertFalse(self.planner.apply("no-such-id"))


class TestCodegenPlannerReject(unittest.TestCase):
    def setUp(self):
        self.planner = CodegenPlanner()
        self.pid = self.planner.propose(**_proposal_kwargs())

    def test_reject_pending_returns_true(self):
        self.assertTrue(self.planner.reject(self.pid))

    def test_reject_sets_status_rejected(self):
        self.planner.reject(self.pid)
        self.assertEqual(self.planner.get(self.pid).status, ProposalStatus.REJECTED)

    def test_reject_stores_reason(self):
        self.planner.reject(self.pid, reason="Not needed")
        self.assertEqual(self.planner.get(self.pid).rejection_reason, "Not needed")

    def test_reject_approved_returns_true(self):
        self.planner.approve(self.pid)
        self.assertTrue(self.planner.reject(self.pid, reason="Changed mind"))

    def test_cannot_apply_rejected(self):
        self.planner.reject(self.pid)
        self.assertFalse(self.planner.apply(self.pid))

    def test_reject_nonexistent_returns_false(self):
        self.assertFalse(self.planner.reject("no-such-id"))

    def test_reject_applied_returns_false(self):
        self.planner.approve(self.pid)
        self.planner.apply(self.pid)
        self.assertFalse(self.planner.reject(self.pid))


class TestCodegenPlannerCancel(unittest.TestCase):
    def setUp(self):
        self.planner = CodegenPlanner()
        self.pid = self.planner.propose(**_proposal_kwargs())

    def test_cancel_pending_returns_true(self):
        self.assertTrue(self.planner.cancel(self.pid))

    def test_cancel_sets_status_cancelled(self):
        self.planner.cancel(self.pid)
        self.assertEqual(self.planner.get(self.pid).status, ProposalStatus.CANCELLED)

    def test_cannot_cancel_approved(self):
        self.planner.approve(self.pid)
        self.assertFalse(self.planner.cancel(self.pid))

    def test_cannot_cancel_applied(self):
        self.planner.approve(self.pid)
        self.planner.apply(self.pid)
        self.assertFalse(self.planner.cancel(self.pid))

    def test_cannot_cancel_rejected(self):
        self.planner.reject(self.pid)
        self.assertFalse(self.planner.cancel(self.pid))

    def test_cancel_nonexistent_returns_false(self):
        self.assertFalse(self.planner.cancel("no-such-id"))


class TestCodegenPlannerQueries(unittest.TestCase):
    def setUp(self):
        self.planner = CodegenPlanner()
        # Create proposals in various states
        self.pid_pending1  = self.planner.propose(**_proposal_kwargs(title="P1"))
        self.pid_pending2  = self.planner.propose(**_proposal_kwargs(title="P2"))
        self.pid_approved  = self.planner.propose(**_proposal_kwargs(title="P3"))
        self.planner.approve(self.pid_approved)
        self.pid_applied   = self.planner.propose(**_proposal_kwargs(title="P4"))
        self.planner.approve(self.pid_applied)
        self.planner.apply(self.pid_applied)
        self.pid_rejected  = self.planner.propose(**_proposal_kwargs(title="P5"))
        self.planner.reject(self.pid_rejected)
        self.pid_cancelled = self.planner.propose(**_proposal_kwargs(title="P6"))
        self.planner.cancel(self.pid_cancelled)

    def test_count_is_total(self):
        self.assertEqual(self.planner.count(), 6)

    def test_list_all_returns_all(self):
        self.assertEqual(len(self.planner.list_all()), 6)

    def test_list_by_status_pending(self):
        pending = self.planner.list_by_status(ProposalStatus.PENDING)
        self.assertEqual(len(pending), 2)

    def test_list_by_status_approved(self):
        approved = self.planner.list_by_status(ProposalStatus.APPROVED)
        self.assertEqual(len(approved), 1)
        self.assertEqual(approved[0].proposal_id, self.pid_approved)

    def test_list_by_status_applied(self):
        applied = self.planner.list_by_status(ProposalStatus.APPLIED)
        self.assertEqual(len(applied), 1)
        self.assertEqual(applied[0].proposal_id, self.pid_applied)

    def test_list_by_status_rejected(self):
        rejected = self.planner.list_by_status(ProposalStatus.REJECTED)
        self.assertEqual(len(rejected), 1)

    def test_list_by_status_cancelled(self):
        cancelled = self.planner.list_by_status(ProposalStatus.CANCELLED)
        self.assertEqual(len(cancelled), 1)

    def test_get_nonexistent_returns_none(self):
        self.assertIsNone(self.planner.get("no-such-id"))

    def test_empty_planner_count_is_zero(self):
        p = CodegenPlanner()
        self.assertEqual(p.count(), 0)

    def test_empty_planner_list_all_empty(self):
        p = CodegenPlanner()
        self.assertEqual(p.list_all(), [])


if __name__ == "__main__":
    unittest.main()
