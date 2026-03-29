"""AtlasAI Phase 40B — Rigid Body Joint Pipeline.

Manages rigid body joint entries, constraints, and visualization configs
for the RigidBodyJointTool cross-language pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class JointEntry:
    """A rigid body joint definition."""
    joint_id: str
    joint_name: str
    joint_type: str = "Hinge"
    body_a_id: str = ""
    body_b_id: str = ""
    limit_low: float = 0.0
    limit_high: float = 0.0
    limit_mode: str = "Hard"
    enabled: bool = True

    @property
    def is_fixed(self) -> bool:
        return self.joint_type == "Fixed"

    @property
    def is_hinge(self) -> bool:
        return self.joint_type == "Hinge"

    @property
    def is_broken(self) -> bool:
        return self.limit_mode == "Free"

    @property
    def has_bodies(self) -> bool:
        return bool(self.body_a_id) and bool(self.body_b_id)

    @property
    def limit_range(self) -> float:
        return self.limit_high - self.limit_low

    @property
    def is_enabled(self) -> bool:
        return self.enabled


@dataclass
class JointConstraintEntry:
    """A joint constraint record."""
    constraint_id: str
    joint_id: str
    axis: str = "X"
    stiffness: float = 1.0
    damping: float = 0.1
    break_force: float = 1000.0
    enabled: bool = True

    @property
    def is_stiff(self) -> bool:
        return self.stiffness > 5.0

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def can_break(self) -> bool:
        return self.break_force < float("inf")

    @property
    def is_x_axis(self) -> bool:
        return self.axis == "X"


@dataclass
class JointVisualizationEntry:
    """A joint visualization config."""
    vis_config_id: str
    joint_id: str
    vis_mode: str = "Axes"
    scale: float = 1.0
    show_labels: bool = False
    enabled: bool = True

    @property
    def is_none(self) -> bool:
        return self.vis_mode == "None"

    @property
    def shows_all(self) -> bool:
        return self.vis_mode == "All"

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_labeled(self) -> bool:
        return self.show_labels


class RigidBodyJointPipeline:
    """Pipeline managing rigid body joint entries, constraints, and visualizations."""

    def __init__(self) -> None:
        self._joints: Dict[str, JointEntry] = {}
        self._constraints: Dict[str, Dict[str, JointConstraintEntry]] = {}
        self._vis_configs: Dict[str, Dict[str, JointVisualizationEntry]] = {}

    def add_joint(self, entry: JointEntry) -> bool:
        if not entry.joint_id:
            return False
        self._joints[entry.joint_id] = entry
        if entry.joint_id not in self._constraints:
            self._constraints[entry.joint_id] = {}
        if entry.joint_id not in self._vis_configs:
            self._vis_configs[entry.joint_id] = {}
        return True

    def get_joint(self, joint_id: str) -> Optional[JointEntry]:
        return self._joints.get(joint_id)

    def remove_joint(self, joint_id: str) -> bool:
        if joint_id not in self._joints:
            return False
        del self._joints[joint_id]
        self._constraints.pop(joint_id, None)
        self._vis_configs.pop(joint_id, None)
        return True

    def get_all_joints(self) -> List[JointEntry]:
        return list(self._joints.values())

    def add_constraint(self, joint_id: str, constraint: JointConstraintEntry) -> bool:
        if joint_id not in self._joints:
            return False
        if joint_id not in self._constraints:
            self._constraints[joint_id] = {}
        self._constraints[joint_id][constraint.constraint_id] = constraint
        return True

    def remove_constraint(self, joint_id: str, constraint_id: str) -> bool:
        if joint_id not in self._constraints:
            return False
        if constraint_id not in self._constraints[joint_id]:
            return False
        del self._constraints[joint_id][constraint_id]
        return True

    def get_constraints_for_joint(self, joint_id: str) -> List[JointConstraintEntry]:
        return list(self._constraints.get(joint_id, {}).values())

    def add_vis_config(self, joint_id: str, vis_config: JointVisualizationEntry) -> bool:
        if joint_id not in self._joints:
            return False
        if joint_id not in self._vis_configs:
            self._vis_configs[joint_id] = {}
        self._vis_configs[joint_id][vis_config.vis_config_id] = vis_config
        return True

    def remove_vis_config(self, joint_id: str, vis_config_id: str) -> bool:
        if joint_id not in self._vis_configs:
            return False
        if vis_config_id not in self._vis_configs[joint_id]:
            return False
        del self._vis_configs[joint_id][vis_config_id]
        return True

    def get_vis_configs_for_joint(self, joint_id: str) -> List[JointVisualizationEntry]:
        return list(self._vis_configs.get(joint_id, {}).values())

    def get_enabled_joints(self) -> List[JointEntry]:
        return [j for j in self._joints.values() if j.enabled]

    def get_disabled_joints(self) -> List[JointEntry]:
        return [j for j in self._joints.values() if not j.enabled]

    def get_joints_by_type(self, joint_type: str) -> List[JointEntry]:
        return [j for j in self._joints.values() if j.joint_type == joint_type]

    def break_joint(self, joint_id: str) -> bool:
        if joint_id not in self._joints:
            return False
        self._joints[joint_id].limit_mode = "Free"
        return True

    def validate(self, entry: JointEntry) -> bool:
        return bool(entry.joint_id) and bool(entry.joint_name)

    @property
    def joint_count(self) -> int:
        return len(self._joints)

    @property
    def is_empty(self) -> bool:
        return len(self._joints) == 0

    def clear(self) -> None:
        self._joints.clear()
        self._constraints.clear()
        self._vis_configs.clear()
