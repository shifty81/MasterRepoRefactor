"""AtlasAI Phase 36B — Ability Debug Pipeline.

Manages ability snapshots, attribute records, and debug frames
for the ability system runtime debugging subsystem.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class AbilitySnapshot:
    """Snapshot of a single ability's runtime state."""

    snapshot_id: str
    ability_id: str
    ability_name: str
    owner_id: str = ""
    activation_state: str = "Inactive"
    cooldown_remaining: float = 0.0
    stack_count: int = 1
    tags: list = field(default_factory=list)

    @property
    def is_active(self) -> bool:
        return self.activation_state == "Active"

    @property
    def is_on_cooldown(self) -> bool:
        return self.cooldown_remaining > 0.0

    @property
    def has_tags(self) -> bool:
        return bool(self.tags)


@dataclass
class AttributeRecord:
    """Record of a single gameplay attribute and its current value."""

    record_id: str
    owner_id: str
    attribute_name: str
    base_value: float = 0.0
    current_value: float = 0.0
    min_value: float = 0.0
    max_value: float = 100.0
    modifiers: list = field(default_factory=list)

    @property
    def is_maxed(self) -> bool:
        return self.current_value >= self.max_value

    @property
    def is_depleted(self) -> bool:
        return self.current_value <= self.min_value

    @property
    def has_modifiers(self) -> bool:
        return bool(self.modifiers)


@dataclass
class AbilityDebugFrame:
    """A single debug frame capturing ability and attribute state."""

    frame_id: str
    timestamp: float = 0.0
    snapshots: list = field(default_factory=list)
    attributes: list = field(default_factory=list)
    active_effects: list = field(default_factory=list)

    @property
    def has_snapshots(self) -> bool:
        return bool(self.snapshots)

    @property
    def has_attributes(self) -> bool:
        return bool(self.attributes)


class AbilityDebugPipeline:
    """Pipeline for managing ability debug snapshots, attribute records, and frames."""

    def __init__(self) -> None:
        self._snapshots: Dict[str, AbilitySnapshot] = {}
        self._attributes: Dict[str, AttributeRecord] = {}
        self._frames: Dict[str, AbilityDebugFrame] = {}

    def add_snapshot(self, s: AbilitySnapshot) -> None:
        """Register an ability snapshot."""
        self._snapshots[s.snapshot_id] = s

    def remove_snapshot(self, snapshot_id: str) -> bool:
        """Remove a snapshot by ID."""
        if snapshot_id in self._snapshots:
            del self._snapshots[snapshot_id]
            return True
        return False

    def get_snapshot(self, snapshot_id: str) -> Optional[AbilitySnapshot]:
        """Retrieve a snapshot by ID."""
        return self._snapshots.get(snapshot_id)

    def get_all_snapshots(self) -> List[AbilitySnapshot]:
        """Return all registered snapshots."""
        return list(self._snapshots.values())

    def add_attribute(self, a: AttributeRecord) -> None:
        """Register an attribute record."""
        self._attributes[a.record_id] = a

    def remove_attribute(self, record_id: str) -> bool:
        """Remove an attribute record by ID."""
        if record_id in self._attributes:
            del self._attributes[record_id]
            return True
        return False

    def get_attribute(self, record_id: str) -> Optional[AttributeRecord]:
        """Retrieve an attribute record by ID."""
        return self._attributes.get(record_id)

    def get_attributes_by_owner(self, owner_id: str) -> List[AttributeRecord]:
        """Return all attribute records for a given owner."""
        return [a for a in self._attributes.values() if a.owner_id == owner_id]

    def get_snapshots_by_owner(self, owner_id: str) -> List[AbilitySnapshot]:
        """Return all snapshots for a given owner."""
        return [s for s in self._snapshots.values() if s.owner_id == owner_id]

    def get_active_snapshots(self) -> List[AbilitySnapshot]:
        """Return all snapshots in the Active state."""
        return [s for s in self._snapshots.values() if s.is_active]

    def get_cooldown_snapshots(self) -> List[AbilitySnapshot]:
        """Return all snapshots that are on cooldown."""
        return [s for s in self._snapshots.values() if s.is_on_cooldown]

    def record_frame(self, frame: AbilityDebugFrame) -> None:
        """Record a debug frame."""
        self._frames[frame.frame_id] = frame

    def get_frame(self, frame_id: str) -> Optional[AbilityDebugFrame]:
        """Retrieve a debug frame by ID."""
        return self._frames.get(frame_id)

    def get_all_frames(self) -> List[AbilityDebugFrame]:
        """Return all recorded debug frames."""
        return list(self._frames.values())

    def clear_frames(self) -> None:
        """Clear all recorded debug frames."""
        self._frames.clear()

    def validate(self, frame: AbilityDebugFrame) -> bool:
        """Validate a debug frame has required fields."""
        return bool(frame.frame_id)

    def clear(self) -> None:
        """Clear all pipeline data."""
        self._snapshots.clear()
        self._attributes.clear()
        self._frames.clear()

    @property
    def snapshot_count(self) -> int:
        return len(self._snapshots)

    @property
    def is_empty(self) -> bool:
        return len(self._snapshots) == 0
