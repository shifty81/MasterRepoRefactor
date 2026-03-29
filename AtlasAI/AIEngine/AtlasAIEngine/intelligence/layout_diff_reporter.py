"""AtlasAI Phase 21B — Layout Diff Reporter.

Compares two layout export snapshots produced by LayoutExportBridge and
generates a structured diff report describing added, removed, moved, and
property-changed placements.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class LayoutDiffEntry:
    """A single change record between two layout snapshots."""

    change_type: str   # "added" | "removed" | "moved" | "property_changed"
    entity_id: str
    entity_type: str
    old_value: Optional[dict] = None
    new_value: Optional[dict] = None


@dataclass
class LayoutDiffReport:
    """Complete diff between two named layout snapshots."""

    snapshot_a: str
    snapshot_b: str
    added: list[LayoutDiffEntry] = field(default_factory=list)
    removed: list[LayoutDiffEntry] = field(default_factory=list)
    moved: list[LayoutDiffEntry] = field(default_factory=list)
    property_changed: list[LayoutDiffEntry] = field(default_factory=list)

    @property
    def total_changes(self) -> int:
        return (len(self.added) + len(self.removed) +
                len(self.moved) + len(self.property_changed))

    @property
    def is_empty(self) -> bool:
        return self.total_changes == 0


def _pos_key(entry: dict) -> tuple:
    return (entry.get("x", 0.0), entry.get("y", 0.0), entry.get("z", 0.0))


_MOVE_THRESHOLD = 0.01


class LayoutDiffReporter:
    """Compare two layout exports and produce a diff report.

    Layout exports are dicts of ``{entity_id: {type, x, y, z, ...}}``.
    They can be passed directly or loaded from JSON files.

    Example::

        reporter = LayoutDiffReporter()
        report = reporter.compare_files("layout_v1.json", "layout_v2.json")
        print(report.total_changes)
    """

    def __init__(self) -> None:
        self._reports: list[LayoutDiffReport] = []

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

    def compare(
        self,
        snapshot_a: dict,
        snapshot_b: dict,
        label_a: str = "snapshot_a",
        label_b: str = "snapshot_b",
    ) -> LayoutDiffReport:
        """Compare two in-memory layout snapshots.

        Each snapshot maps ``entity_id -> dict(type, x, y, z, ...)``
        """
        report = LayoutDiffReport(snapshot_a=label_a, snapshot_b=label_b)

        ids_a = set(snapshot_a.keys())
        ids_b = set(snapshot_b.keys())

        # Added
        for eid in ids_b - ids_a:
            entry_b = snapshot_b[eid]
            report.added.append(LayoutDiffEntry(
                change_type="added",
                entity_id=eid,
                entity_type=entry_b.get("type", "Unknown"),
                new_value=dict(entry_b),
            ))

        # Removed
        for eid in ids_a - ids_b:
            entry_a = snapshot_a[eid]
            report.removed.append(LayoutDiffEntry(
                change_type="removed",
                entity_id=eid,
                entity_type=entry_a.get("type", "Unknown"),
                old_value=dict(entry_a),
            ))

        # Common — check moved and property changes
        for eid in ids_a & ids_b:
            ea = snapshot_a[eid]
            eb = snapshot_b[eid]
            pos_a = _pos_key(ea)
            pos_b = _pos_key(eb)
            moved = any(abs(a - b) > _MOVE_THRESHOLD for a, b in zip(pos_a, pos_b))
            other_changed = {k: v for k, v in eb.items()
                             if k not in ("x", "y", "z") and ea.get(k) != v}

            if moved:
                report.moved.append(LayoutDiffEntry(
                    change_type="moved",
                    entity_id=eid,
                    entity_type=ea.get("type", "Unknown"),
                    old_value={"x": ea.get("x"), "y": ea.get("y"), "z": ea.get("z")},
                    new_value={"x": eb.get("x"), "y": eb.get("y"), "z": eb.get("z")},
                ))
            if other_changed:
                report.property_changed.append(LayoutDiffEntry(
                    change_type="property_changed",
                    entity_id=eid,
                    entity_type=ea.get("type", "Unknown"),
                    old_value={k: ea.get(k) for k in other_changed},
                    new_value=other_changed,
                ))

        self._reports.append(report)
        logger.debug("LayoutDiffReporter: %s vs %s → %d changes",
                     label_a, label_b, report.total_changes)
        return report

    def compare_files(self, path_a: str, path_b: str) -> LayoutDiffReport:
        """Load two JSON layout files and compare them."""
        try:
            data_a = json.loads(Path(path_a).read_text())
            data_b = json.loads(Path(path_b).read_text())
        except Exception as exc:  # pragma: no cover
            logger.error("LayoutDiffReporter.compare_files failed: %s", exc)
            return LayoutDiffReport(snapshot_a=path_a, snapshot_b=path_b)
        return self.compare(data_a, data_b, label_a=path_a, label_b=path_b)

    # ------------------------------------------------------------------
    # History
    # ------------------------------------------------------------------

    def get_report_count(self) -> int:
        return len(self._reports)

    def get_last_report(self) -> Optional[LayoutDiffReport]:
        return self._reports[-1] if self._reports else None

    def clear_history(self) -> None:
        self._reports.clear()

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def save_report(self, report: LayoutDiffReport, path: str) -> bool:
        """Write a diff report to *path* as JSON.  Returns True on success."""
        try:
            def _entry_to_dict(e: LayoutDiffEntry) -> dict:
                return {
                    "change_type": e.change_type,
                    "entity_id": e.entity_id,
                    "entity_type": e.entity_type,
                    "old_value": e.old_value,
                    "new_value": e.new_value,
                }
            data = {
                "snapshot_a": report.snapshot_a,
                "snapshot_b": report.snapshot_b,
                "total_changes": report.total_changes,
                "added": [_entry_to_dict(e) for e in report.added],
                "removed": [_entry_to_dict(e) for e in report.removed],
                "moved": [_entry_to_dict(e) for e in report.moved],
                "property_changed": [_entry_to_dict(e) for e in report.property_changed],
            }
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(json.dumps(data, indent=2))
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("LayoutDiffReporter.save_report failed: %s", exc)
            return False
