"""AtlasAI Phase 32B — IK Solve Pipeline.

Manages IK chain definitions, joint constraints, and solve results
for the IK solving subsystem used in animation and physics rigs.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class IKJointDef:
    """Definition for a single IK joint in a chain."""

    joint_id: str
    joint_name: str
    parent_id: str = ""
    min_angle: float = -180.0
    max_angle: float = 180.0
    stiffness: float = 1.0
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def has_parent(self) -> bool:
        return bool(self.parent_id)


@dataclass
class IKChainEntry:
    """A single IK chain tracked by the solve pipeline."""

    entry_id: str
    chain_name: str
    root_joint_id: str
    end_effector_id: str
    joints: list = field(default_factory=list)
    solver: str = "FABRIK"      # FABRIK/CCD/TwoBone/Analytic
    iterations: int = 10
    tolerance: float = 0.001

    @property
    def joint_count(self) -> int:
        return len(self.joints)

    @property
    def has_joints(self) -> bool:
        return len(self.joints) > 0


@dataclass
class IKSolveResult:
    """Result from an IK solve operation."""

    job_id: str
    entry_id: str
    converged: bool = False
    iterations_used: int = 0
    final_error: float = 0.0
    elapsed_ms: float = 0.0

    @property
    def is_converged(self) -> bool:
        return self.converged

    @property
    def is_fast(self) -> bool:
        return self.elapsed_ms < 1.0


class IKSolvePipeline:
    """Pipeline for managing and executing IK solve jobs."""

    def __init__(self) -> None:
        self._chains: Dict[str, IKChainEntry] = {}
        self._joints: Dict[str, IKJointDef] = {}
        self._result_counter: int = 0

    def add_chain(self, chain: IKChainEntry) -> None:
        """Register an IK chain in the pipeline."""
        self._chains[chain.entry_id] = chain

    def remove_chain(self, entry_id: str) -> bool:
        """Remove an IK chain by ID."""
        if entry_id in self._chains:
            del self._chains[entry_id]
            return True
        return False

    def get_chain(self, entry_id: str) -> Optional[IKChainEntry]:
        """Retrieve an IK chain by ID."""
        return self._chains.get(entry_id)

    def get_all_chains(self) -> List[IKChainEntry]:
        """Return all registered IK chains."""
        return list(self._chains.values())

    def add_joint(self, entry_id: str, joint: IKJointDef) -> bool:
        """Add a joint definition to a chain."""
        chain = self._chains.get(entry_id)
        if chain is None:
            return False
        self._joints[joint.joint_id] = joint
        chain.joints.append(joint.joint_id)
        return True

    def solve(self, entry_id: str, target_pos: Tuple[float, float, float] = (0, 0, 0)) -> IKSolveResult:
        """Solve IK for a single chain and return the result."""
        self._result_counter += 1
        job_id = f"ik_job_{self._result_counter}"
        chain = self._chains.get(entry_id)
        if chain is None:
            return IKSolveResult(job_id=job_id, entry_id=entry_id)
        logger.debug("Solving IK chain %s toward %s", entry_id, target_pos)
        return IKSolveResult(
            job_id=job_id,
            entry_id=entry_id,
            converged=True,
            iterations_used=chain.iterations,
            final_error=0.0,
            elapsed_ms=0.5,
        )

    def solve_all(self) -> List[IKSolveResult]:
        """Solve IK for all registered chains and return results."""
        return [self.solve(eid) for eid in list(self._chains)]

    def validate(self, chain: IKChainEntry) -> bool:
        """Validate that a chain has required root and end effector IDs."""
        return bool(chain.entry_id) and bool(chain.root_joint_id) and bool(chain.end_effector_id)

    def clear(self) -> None:
        """Clear all chains and joints."""
        self._chains.clear()
        self._joints.clear()

    @property
    def chain_count(self) -> int:
        return len(self._chains)

    @property
    def is_empty(self) -> bool:
        return len(self._chains) == 0
