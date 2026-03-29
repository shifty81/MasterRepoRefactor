"""Phase 16A — Codegen Workflow tests."""
from __future__ import annotations

import unittest
from pathlib import Path

from AtlasAI.Services.codegen_approval_service import CodegenApprovalService

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestDiffPanelWidgetHeader(unittest.TestCase):
    def setUp(self):
        self.header = REPO_ROOT / "Atlas" / "Editor" / "Panels" / "DiffPanelWidget.h"
        self.content = self.header.read_text()

    def test_file_exists(self):
        self.assertTrue(self.header.exists())

    def test_pragma_once(self):
        self.assertIn("#pragma once", self.content)

    def test_load_diff_method(self):
        self.assertIn("LoadDiff", self.content)

    def test_on_approve_method(self):
        self.assertIn("OnApprove", self.content)

    def test_on_reject_method(self):
        self.assertIn("OnReject", self.content)

    def test_pending_diff_member(self):
        self.assertIn("m_pendingDiff", self.content)

    def test_namespace(self):
        self.assertIn("Atlas::Editor", self.content)

    def test_class_declaration(self):
        self.assertIn("DiffPanelWidget", self.content)


class TestPatchApplicatorHeader(unittest.TestCase):
    def setUp(self):
        self.header = REPO_ROOT / "Atlas" / "Editor" / "Core" / "PatchApplicator.h"
        self.content = self.header.read_text()

    def test_file_exists(self):
        self.assertTrue(self.header.exists())

    def test_pragma_once(self):
        self.assertIn("#pragma once", self.content)

    def test_apply_patch_method(self):
        self.assertIn("ApplyPatch", self.content)

    def test_validate_patch_method(self):
        self.assertIn("ValidatePatch", self.content)

    def test_namespace(self):
        self.assertIn("Atlas::Editor", self.content)

    def test_class_declaration(self):
        self.assertIn("PatchApplicator", self.content)


class TestCodegenApprovalService(unittest.TestCase):
    def setUp(self):
        self.service = CodegenApprovalService()

    def test_submit_returns_pending_id(self):
        pid = self.service.submit_diff({"diff": "--- a\n+++ b"})
        self.assertIsInstance(pid, str)
        self.assertTrue(len(pid) > 0)

    def test_get_pending_returns_payload(self):
        payload = {"diff": "--- a\n+++ b", "file": "foo.cpp"}
        pid = self.service.submit_diff(payload)
        result = self.service.get_pending(pid)
        self.assertEqual(result["diff"], payload["diff"])

    def test_approve_returns_true(self):
        pid = self.service.submit_diff({"diff": "x"})
        self.assertTrue(self.service.approve(pid))

    def test_approve_removes_pending(self):
        pid = self.service.submit_diff({"diff": "x"})
        self.service.approve(pid)
        self.assertEqual(self.service.get_pending(pid), {})

    def test_reject_returns_true(self):
        pid = self.service.submit_diff({"diff": "y"})
        self.assertTrue(self.service.reject(pid))

    def test_reject_removes_pending(self):
        pid = self.service.submit_diff({"diff": "y"})
        self.service.reject(pid)
        self.assertEqual(self.service.get_pending(pid), {})

    def test_approve_unknown_returns_false(self):
        self.assertFalse(self.service.approve("nonexistent"))

    def test_reject_unknown_returns_false(self):
        self.assertFalse(self.service.reject("nonexistent"))

    def test_multiple_pending_diffs(self):
        pid1 = self.service.submit_diff({"diff": "a"})
        pid2 = self.service.submit_diff({"diff": "b"})
        self.assertNotEqual(pid1, pid2)
        self.assertEqual(self.service.get_pending(pid1)["diff"], "a")
        self.assertEqual(self.service.get_pending(pid2)["diff"], "b")


class TestServicesDirectory(unittest.TestCase):
    def test_services_directory_exists(self):
        services_dir = REPO_ROOT / "AtlasAI" / "Services"
        self.assertTrue(services_dir.is_dir())

    def test_services_init_exists(self):
        init_file = REPO_ROOT / "AtlasAI" / "Services" / "__init__.py"
        self.assertTrue(init_file.exists())


if __name__ == "__main__":
    unittest.main()
