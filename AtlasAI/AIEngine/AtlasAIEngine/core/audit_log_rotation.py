"""Phase 14 — Audit Log Rotation + Workspace Snapshot Export.

Automates rotating JSONL audit logs and exporting workspace snapshots so
old entries don't bloat the repository and every snapshot is versioned.
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


class AuditLogRotator:
    """Rotates JSONL audit log files when they exceed a size threshold."""

    def __init__(
        self,
        log_dir: Path,
        max_size_bytes: int = 5 * 1024 * 1024,
        max_backups: int = 5,
    ) -> None:
        self.log_dir = Path(log_dir)
        self.max_size_bytes = max_size_bytes
        self.max_backups = max_backups

    def rotate_if_needed(self, log_file: Path) -> bool:
        """Rotate *log_file* if it exceeds max_size_bytes.

        Rotates by renaming existing backups (log.1 -> log.2, …) and moving
        the current file to log.1.  Returns True when a rotation occurred.
        """
        log_file = Path(log_file)
        if not log_file.exists() or log_file.stat().st_size <= self.max_size_bytes:
            return False

        # Shift existing backups upward
        for n in range(self.max_backups - 1, 0, -1):
            src = log_file.with_suffix(f"{log_file.suffix}.{n}")
            dst = log_file.with_suffix(f"{log_file.suffix}.{n + 1}")
            if src.exists():
                src.rename(dst)

        rotated = log_file.with_suffix(f"{log_file.suffix}.1")
        log_file.rename(rotated)
        log_file.touch()
        return True

    def list_rotated_files(self, log_file: Path) -> list[Path]:
        """Return sorted list of existing backup files for *log_file*."""
        log_file = Path(log_file)
        results: list[Path] = []
        for n in range(1, self.max_backups + 1):
            candidate = log_file.with_suffix(f"{log_file.suffix}.{n}")
            if candidate.exists():
                results.append(candidate)
        return results

    def prune_old_backups(self, log_file: Path) -> int:
        """Delete backup files beyond max_backups.  Returns number deleted."""
        log_file = Path(log_file)
        deleted = 0
        for n in range(self.max_backups + 1, self.max_backups + 100):
            candidate = log_file.with_suffix(f"{log_file.suffix}.{n}")
            if candidate.exists():
                candidate.unlink()
                deleted += 1
            else:
                break
        return deleted


class WorkspaceSnapshotExporter:
    """Exports workspace state snapshots as timestamped JSON files."""

    def __init__(self, snapshot_dir: Path) -> None:
        self.snapshot_dir = Path(snapshot_dir)
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)

    def export_snapshot(self, session_id: str, data: dict) -> Path:
        """Write *data* to snapshot_dir/{session_id}_{timestamp}.json.

        Returns the path of the written file.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
        filename = f"{session_id}_{timestamp}.json"
        path = self.snapshot_dir / filename
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return path

    def list_snapshots(self) -> list[Path]:
        """Return all snapshot files sorted by name (chronological)."""
        return sorted(self.snapshot_dir.glob("*.json"))

    def prune_old_snapshots(self, keep_last: int = 10) -> int:
        """Delete all but the *keep_last* newest snapshots.

        Returns the number of files deleted.
        """
        snapshots = self.list_snapshots()
        to_delete = snapshots[: max(0, len(snapshots) - keep_last)]
        for path in to_delete:
            path.unlink()
        return len(to_delete)
