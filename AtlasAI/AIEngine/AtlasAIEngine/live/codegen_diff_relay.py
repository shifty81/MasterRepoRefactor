"""Phase 13 — Codegen Diff Relay.

Connects the CodegenPlanner proposal lifecycle to the live patch system so
AI-proposed diffs can be queued, reviewed, and applied without a full restart.
"""
from __future__ import annotations

import logging
import threading
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..core.codegen_planner import CodegenPlanner
    from .hot_reload import HotReloadCoordinator

logger = logging.getLogger(__name__)


@dataclass
class DiffEntry:
    proposal_id: str
    file_path: str
    diff_text: str
    applied: bool = False


class CodegenDiffRelay:
    """Bridges ``CodegenPlanner`` proposals to the live hot-reload patch system.

    Workflow::

        relay = CodegenDiffRelay(planner, coordinator)
        entry = relay.submit_diff(proposal_id, "src/foo.py", unified_diff)
        relay.apply_diff(proposal_id)   # queues patch via coordinator
    """

    def __init__(
        self,
        planner: CodegenPlanner | Any,
        coordinator: HotReloadCoordinator | Any,
    ) -> None:
        self._planner = planner
        self._coordinator = coordinator
        self._entries: dict[str, DiffEntry] = {}
        self._rejected: dict[str, str] = {}  # proposal_id → reason
        self._lock = threading.Lock()

    # ── submission ─────────────────────────────────────────────────────────

    def submit_diff(
        self, proposal_id: str, file_path: str, diff_text: str
    ) -> DiffEntry:
        """Record a new diff proposal for later review and application.

        Args:
            proposal_id: Identifier from the originating ``CodegenPlanner``.
            file_path:   Path of the file this diff targets.
            diff_text:   Unified-diff text describing the change.

        Returns:
            The newly created :class:`DiffEntry`.
        """
        entry = DiffEntry(
            proposal_id=proposal_id,
            file_path=file_path,
            diff_text=diff_text,
        )
        with self._lock:
            self._entries[proposal_id] = entry
        logger.debug(
            "CodegenDiffRelay: submitted diff for proposal=%s file=%s",
            proposal_id,
            file_path,
        )
        return entry

    # ── queries ────────────────────────────────────────────────────────────

    def get_pending(self) -> list[DiffEntry]:
        """Return all diff entries that have not yet been applied or rejected."""
        with self._lock:
            rejected_ids = set(self._rejected)
            return [
                e
                for e in self._entries.values()
                if not e.applied and e.proposal_id not in rejected_ids
            ]

    def list_applied(self) -> list[DiffEntry]:
        """Return all diff entries that have been successfully applied."""
        with self._lock:
            return [e for e in self._entries.values() if e.applied]

    def count(self) -> int:
        """Return the total number of tracked diff entries."""
        with self._lock:
            return len(self._entries)

    # ── actions ────────────────────────────────────────────────────────────

    def apply_diff(self, proposal_id: str) -> bool:
        """Mark a diff as applied and forward patch content to the coordinator.

        Extracts the ``+`` lines from the unified diff as patch content and
        queues them via :meth:`HotReloadCoordinator.add_patch`.

        Args:
            proposal_id: ID of the :class:`DiffEntry` to apply.

        Returns:
            ``True`` if the entry was found, not yet applied, and the patch
            was accepted by the coordinator.  ``False`` otherwise.
        """
        with self._lock:
            entry = self._entries.get(proposal_id)
            if entry is None or entry.applied:
                return False
            if proposal_id in self._rejected:
                logger.warning(
                    "CodegenDiffRelay.apply_diff: proposal=%s was already rejected",
                    proposal_id,
                )
                return False
            entry.applied = True

        patch_content = self._extract_patch_content(entry.diff_text)
        queued = self._coordinator.add_patch(entry.file_path, patch_content)
        logger.info(
            "CodegenDiffRelay: applied diff proposal=%s file=%s queued=%s",
            proposal_id,
            entry.file_path,
            queued,
        )
        return queued

    def reject_diff(self, proposal_id: str, reason: str = "") -> bool:
        """Reject a pending diff entry.

        Args:
            proposal_id: ID of the :class:`DiffEntry` to reject.
            reason:      Optional human-readable rejection reason.

        Returns:
            ``True`` if the entry existed and was not already applied.
        """
        with self._lock:
            entry = self._entries.get(proposal_id)
            if entry is None or entry.applied:
                return False
            self._rejected[proposal_id] = reason
        logger.debug(
            "CodegenDiffRelay: rejected diff proposal=%s reason=%r",
            proposal_id,
            reason,
        )
        return True

    # ── internal ───────────────────────────────────────────────────────────

    @staticmethod
    def _extract_patch_content(diff_text: str) -> str:
        """Return only the added lines from a unified diff as plain text."""
        added_lines = [
            line[1:]
            for line in diff_text.splitlines()
            if line.startswith("+") and not line.startswith("+++")
        ]
        return "\n".join(added_lines)
