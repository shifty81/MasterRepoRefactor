"""codegen_planner.py — Codegen proposal lifecycle (propose → diff → approve → apply)."""
from __future__ import annotations

import uuid
from enum import Enum
from typing import Optional
from core.logger import get_logger

logger = get_logger(__name__)


class ProposalStatus(str, Enum):
    PENDING   = "pending"
    APPROVED  = "approved"
    REJECTED  = "rejected"
    APPLIED   = "applied"
    CANCELLED = "cancelled"


class CodeProposal:
    """A single code-generation proposal."""

    def __init__(
        self,
        title: str,
        description: str,
        target_file: str,
        diff_preview: str,
        author: str = "AtlasAI",
    ) -> None:
        self.proposal_id  = str(uuid.uuid4())
        self.title        = title
        self.description  = description
        self.target_file  = target_file
        self.diff_preview = diff_preview
        self.author       = author
        self.status       = ProposalStatus.PENDING
        self.rejection_reason: Optional[str] = None
        self.applied_patch: Optional[str]    = None

    def to_dict(self) -> dict:
        return {
            "proposal_id":    self.proposal_id,
            "title":          self.title,
            "description":    self.description,
            "target_file":    self.target_file,
            "diff_preview":   self.diff_preview,
            "author":         self.author,
            "status":         self.status.value,
            "rejection_reason": self.rejection_reason,
        }


class CodegenPlanner:
    """
    Manages the full codegen proposal lifecycle.

    Workflow:
        propose()  → returns proposal_id
        get_diff() → returns diff_preview for review
        approve()  → marks approved (required before apply)
        apply()    → marks applied, stores patch
        reject()   → marks rejected with reason
        cancel()   → cancels pending proposal
    """

    def __init__(self) -> None:
        self._proposals: dict[str, CodeProposal] = {}

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def propose(
        self,
        title: str,
        description: str,
        target_file: str,
        diff_preview: str,
        author: str = "AtlasAI",
    ) -> str:
        """Create a new proposal. Returns proposal_id."""
        proposal = CodeProposal(title, description, target_file, diff_preview, author)
        self._proposals[proposal.proposal_id] = proposal
        logger.debug("Proposal created: %s (%s)", proposal.proposal_id, title)
        return proposal.proposal_id

    def get_diff(self, proposal_id: str) -> Optional[str]:
        """Return diff_preview for the given proposal."""
        p = self._proposals.get(proposal_id)
        return p.diff_preview if p else None

    def approve(self, proposal_id: str) -> bool:
        """Approve a pending proposal. Returns True on success."""
        p = self._proposals.get(proposal_id)
        if p is None or p.status != ProposalStatus.PENDING:
            return False
        p.status = ProposalStatus.APPROVED
        logger.debug("Proposal approved: %s", proposal_id)
        return True

    def reject(self, proposal_id: str, reason: str = "") -> bool:
        """Reject a pending proposal."""
        p = self._proposals.get(proposal_id)
        if p is None or p.status not in (ProposalStatus.PENDING, ProposalStatus.APPROVED):
            return False
        p.status           = ProposalStatus.REJECTED
        p.rejection_reason = reason
        logger.debug("Proposal rejected: %s (%s)", proposal_id, reason)
        return True

    def apply(self, proposal_id: str) -> bool:
        """Apply an approved proposal. Returns True on success."""
        p = self._proposals.get(proposal_id)
        if p is None or p.status != ProposalStatus.APPROVED:
            return False
        p.status        = ProposalStatus.APPLIED
        p.applied_patch = p.diff_preview   # stub: patch equals diff preview
        logger.debug("Proposal applied: %s", proposal_id)
        return True

    def cancel(self, proposal_id: str) -> bool:
        """Cancel a pending proposal."""
        p = self._proposals.get(proposal_id)
        if p is None or p.status != ProposalStatus.PENDING:
            return False
        p.status = ProposalStatus.CANCELLED
        return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get(self, proposal_id: str) -> Optional[CodeProposal]:
        return self._proposals.get(proposal_id)

    def list_by_status(self, status: ProposalStatus) -> list[CodeProposal]:
        return [p for p in self._proposals.values() if p.status == status]

    def list_all(self) -> list[CodeProposal]:
        return list(self._proposals.values())

    def count(self) -> int:
        return len(self._proposals)
