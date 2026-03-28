"""AtlasAI Phase 16A — Codegen Approval Service.

Holds pending diffs submitted by CodegenDiffRelay until the developer
approves or rejects them through the Atlas IDE diff panel.
"""
from __future__ import annotations

import uuid


class CodegenApprovalService:
    """Manages pending codegen diffs awaiting human review."""

    def __init__(self) -> None:
        self._pending: dict = {}

    def submit_diff(self, diff_payload: dict) -> str:
        """Store *diff_payload* and return a unique pending_id."""
        pending_id = str(uuid.uuid4())
        self._pending[pending_id] = dict(diff_payload)
        return pending_id

    def get_pending(self, pending_id: str) -> dict:
        """Return the payload stored under *pending_id*, or an empty dict."""
        return self._pending.get(pending_id, {})

    def approve(self, pending_id: str) -> bool:
        """Remove the pending diff and signal approval.

        Returns:
            ``True`` if the diff existed and was approved, ``False`` otherwise.
        """
        if pending_id not in self._pending:
            return False
        del self._pending[pending_id]
        return True

    def reject(self, pending_id: str) -> bool:
        """Remove the pending diff and signal rejection.

        Returns:
            ``True`` if the diff existed and was rejected, ``False`` otherwise.
        """
        if pending_id not in self._pending:
            return False
        del self._pending[pending_id]
        return True
