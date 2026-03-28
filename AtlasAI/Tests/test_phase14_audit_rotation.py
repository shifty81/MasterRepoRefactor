"""Tests for Phase 14 — AuditLogRotator and WorkspaceSnapshotExporter."""

import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CORE_DIR = REPO_ROOT / "AtlasAI" / "AIEngine" / "AtlasAIEngine" / "core"
SOURCE_FILE = CORE_DIR / "audit_log_rotation.py"


class TestAuditLogRotatorFiles(unittest.TestCase):
    def test_audit_log_rotation_exists(self):
        self.assertTrue(SOURCE_FILE.exists(), f"Missing: {SOURCE_FILE}")


class TestAuditLogRotatorContent(unittest.TestCase):
    def _read(self) -> str:
        return SOURCE_FILE.read_text(encoding="utf-8")

    def test_has_audit_log_rotator_class(self):
        self.assertIn("AuditLogRotator", self._read())

    def test_has_rotate_if_needed(self):
        self.assertIn("rotate_if_needed", self._read())

    def test_has_list_rotated_files(self):
        self.assertIn("list_rotated_files", self._read())

    def test_has_prune_old_backups(self):
        self.assertIn("prune_old_backups", self._read())

    def test_has_init_params(self):
        src = self._read()
        self.assertIn("max_size_bytes", src)
        self.assertIn("max_backups", src)


class TestWorkspaceSnapshotExporterContent(unittest.TestCase):
    def _read(self) -> str:
        return SOURCE_FILE.read_text(encoding="utf-8")

    def test_has_workspace_snapshot_exporter_class(self):
        self.assertIn("WorkspaceSnapshotExporter", self._read())

    def test_has_export_snapshot(self):
        self.assertIn("export_snapshot", self._read())

    def test_has_list_snapshots(self):
        self.assertIn("list_snapshots", self._read())

    def test_has_prune_old_snapshots(self):
        self.assertIn("prune_old_snapshots", self._read())


class TestAuditLogRotatorFunctional(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._tmp_path = Path(self._tmp)
        import sys
        sys.path.insert(0, str(CORE_DIR.parent.parent))
        from AtlasAIEngine.core.audit_log_rotation import (
            AuditLogRotator,
            WorkspaceSnapshotExporter,
        )
        self._Rotator = AuditLogRotator
        self._Exporter = WorkspaceSnapshotExporter

    def tearDown(self):
        import shutil
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_rotate_when_oversized(self):
        log_file = self._tmp_path / "audit.jsonl"
        log_file.write_bytes(b"x" * 100)
        rotator = self._Rotator(self._tmp_path, max_size_bytes=50, max_backups=5)
        result = rotator.rotate_if_needed(log_file)
        self.assertTrue(result, "Expected rotation to occur for oversized file")
        self.assertTrue(log_file.exists(), "Log file should be recreated after rotation")

    def test_no_rotate_when_small(self):
        log_file = self._tmp_path / "audit_small.jsonl"
        log_file.write_bytes(b"tiny")
        rotator = self._Rotator(self._tmp_path, max_size_bytes=1024, max_backups=5)
        result = rotator.rotate_if_needed(log_file)
        self.assertFalse(result, "Expected no rotation for small file")

    def test_export_snapshot(self):
        snap_dir = self._tmp_path / "snapshots"
        exporter = self._Exporter(snap_dir)
        path = exporter.export_snapshot("session-abc", {"key": "value"})
        self.assertTrue(path.exists(), f"Snapshot file not found: {path}")
        self.assertIn("session-abc", path.name)

    def test_prune_snapshots(self):
        snap_dir = self._tmp_path / "snapshots2"
        exporter = self._Exporter(snap_dir)
        import time
        for i in range(15):
            exporter.export_snapshot(f"sess-{i:03d}", {"i": i})
            time.sleep(0.01)
        deleted = exporter.prune_old_snapshots(keep_last=10)
        self.assertEqual(deleted, 5, f"Expected 5 deleted, got {deleted}")
        remaining = exporter.list_snapshots()
        self.assertEqual(len(remaining), 10)


if __name__ == "__main__":
    unittest.main()
