"""AtlasAI Phase 21B — AI Build Monitor.

Watches build output streams, classifies errors and warnings by severity and
category, and provides a structured summary for AI-driven remediation.
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Compile-time error/warning classifiers
_ERROR_PATTERNS = [
    (re.compile(r"error\s*C\d+", re.IGNORECASE), "compiler_error"),
    (re.compile(r"undefined reference to", re.IGNORECASE), "linker_error"),
    (re.compile(r"cannot open source file", re.IGNORECASE), "missing_include"),
    (re.compile(r"syntax error", re.IGNORECASE), "syntax_error"),
    (re.compile(r"error:", re.IGNORECASE), "generic_error"),
]

_WARNING_PATTERNS = [
    (re.compile(r"warning\s*C\d+", re.IGNORECASE), "compiler_warning"),
    (re.compile(r"deprecated", re.IGNORECASE), "deprecation_warning"),
    (re.compile(r"warning:", re.IGNORECASE), "generic_warning"),
]


@dataclass
class BuildDiagnostic:
    """A single classified build diagnostic."""

    line: str
    severity: str  # "error" | "warning" | "info"
    category: str
    timestamp: str
    file_hint: Optional[str] = None


@dataclass
class BuildSummary:
    """Aggregate summary of a completed build."""

    build_id: str
    start_time: str
    end_time: str
    success: bool
    error_count: int
    warning_count: int
    diagnostics: list[BuildDiagnostic] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class AIBuildMonitor:
    """Monitor and classify build output for AI-driven remediation.

    Feed raw build lines via ``ingest_line()`` or ``ingest_lines()``.  When the
    build completes call ``finalize()`` to get a ``BuildSummary``.

    Example::

        monitor = AIBuildMonitor(build_id="build_001")
        for line in build_output:
            monitor.ingest_line(line)
        summary = monitor.finalize(success=True)
    """

    def __init__(self, build_id: str = "build_000") -> None:
        self.build_id = build_id
        self._start_time = datetime.now(timezone.utc).isoformat()
        self._diagnostics: list[BuildDiagnostic] = []
        self._error_count = 0
        self._warning_count = 0

    # ------------------------------------------------------------------
    # Ingestion
    # ------------------------------------------------------------------

    def ingest_line(self, line: str) -> Optional[BuildDiagnostic]:
        """Process a single build output line.  Returns a diagnostic if classified."""
        ts = datetime.now(timezone.utc).isoformat()
        # Classify as error first, then warning
        for pattern, category in _ERROR_PATTERNS:
            if pattern.search(line):
                diag = BuildDiagnostic(
                    line=line.rstrip(),
                    severity="error",
                    category=category,
                    timestamp=ts,
                    file_hint=self._extract_file_hint(line),
                )
                self._diagnostics.append(diag)
                self._error_count += 1
                return diag
        for pattern, category in _WARNING_PATTERNS:
            if pattern.search(line):
                diag = BuildDiagnostic(
                    line=line.rstrip(),
                    severity="warning",
                    category=category,
                    timestamp=ts,
                    file_hint=self._extract_file_hint(line),
                )
                self._diagnostics.append(diag)
                self._warning_count += 1
                return diag
        return None

    def ingest_lines(self, lines: list[str]) -> int:
        """Process multiple lines.  Returns count of classified diagnostics."""
        before = len(self._diagnostics)
        for line in lines:
            self.ingest_line(line)
        return len(self._diagnostics) - before

    @staticmethod
    def _extract_file_hint(line: str) -> Optional[str]:
        """Try to extract a filename from a build line."""
        m = re.search(r'([A-Za-z0-9_/\\.-]+\.[ch][px]{0,2})', line)
        return m.group(1) if m else None

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get_errors(self) -> list[BuildDiagnostic]:
        return [d for d in self._diagnostics if d.severity == "error"]

    def get_warnings(self) -> list[BuildDiagnostic]:
        return [d for d in self._diagnostics if d.severity == "warning"]

    def get_by_category(self, category: str) -> list[BuildDiagnostic]:
        return [d for d in self._diagnostics if d.category == category]

    def get_error_count(self) -> int:
        return self._error_count

    def get_warning_count(self) -> int:
        return self._warning_count

    def get_diagnostic_count(self) -> int:
        return len(self._diagnostics)

    # ------------------------------------------------------------------
    # Finalization
    # ------------------------------------------------------------------

    def finalize(self, success: bool = True, metadata: Optional[dict] = None) -> BuildSummary:
        """Produce a BuildSummary for the monitored build."""
        end_time = datetime.now(timezone.utc).isoformat()
        return BuildSummary(
            build_id=self.build_id,
            start_time=self._start_time,
            end_time=end_time,
            success=success,
            error_count=self._error_count,
            warning_count=self._warning_count,
            diagnostics=list(self._diagnostics),
            metadata=dict(metadata or {}),
        )

    def reset(self) -> None:
        """Reset state for a new build run."""
        self._start_time = datetime.now(timezone.utc).isoformat()
        self._diagnostics.clear()
        self._error_count = 0
        self._warning_count = 0

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_summary(self, summary: BuildSummary, path: str) -> bool:
        """Persist a BuildSummary to *path* as JSON.  Returns True on success."""
        try:
            data = {
                "build_id": summary.build_id,
                "start_time": summary.start_time,
                "end_time": summary.end_time,
                "success": summary.success,
                "error_count": summary.error_count,
                "warning_count": summary.warning_count,
                "metadata": summary.metadata,
                "diagnostics": [
                    {
                        "line": d.line,
                        "severity": d.severity,
                        "category": d.category,
                        "timestamp": d.timestamp,
                        "file_hint": d.file_hint,
                    }
                    for d in summary.diagnostics
                ],
            }
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(json.dumps(data, indent=2))
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("AIBuildMonitor.save_summary failed: %s", exc)
            return False
