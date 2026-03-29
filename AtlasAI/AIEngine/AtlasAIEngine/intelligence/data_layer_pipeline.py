"""AtlasAI Phase 34B — Data Layer Pipeline.

Manages data layer specs, actor assignments, and runtime state
for the Data Layer authoring subsystem.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class DataLayerSpec:
    """Specification for a single data layer."""

    layer_id: str
    layer_name: str
    layer_type: str = "Runtime"         # Editor/Runtime/Both
    runtime_init: str = "Deactivated"   # Activated/Deactivated
    parent_id: str = ""
    visible: bool = True
    locked: bool = False

    @property
    def is_runtime(self) -> bool:
        return self.layer_type in ("Runtime", "Both")

    @property
    def is_editor_only(self) -> bool:
        return self.layer_type == "Editor"

    @property
    def has_parent(self) -> bool:
        return bool(self.parent_id)


@dataclass
class DataLayerActorAssignment:
    """Assignment of an actor to a data layer."""

    assignment_id: str
    actor_id: str
    layer_id: str
    inherited: bool = False

    @property
    def is_inherited(self) -> bool:
        return self.inherited


@dataclass
class DataLayerState:
    """Runtime state for a data layer."""

    state_id: str
    layer_id: str
    current_state: str = "Unloaded"     # Unloaded/Loaded/Activated/Deactivated/Error
    previous_state: str = "Unloaded"
    pending_request: str = ""

    @property
    def is_active(self) -> bool:
        return self.current_state == "Activated"

    @property
    def is_loaded(self) -> bool:
        return self.current_state in ("Loaded", "Activated")

    @property
    def has_pending(self) -> bool:
        return bool(self.pending_request)


class DataLayerPipeline:
    """Pipeline for managing data layers, actor assignments, and layer states."""

    def __init__(self) -> None:
        self._layers: Dict[str, DataLayerSpec] = {}
        self._assignments: Dict[str, DataLayerActorAssignment] = {}
        self._states: Dict[str, DataLayerState] = {}
        self._state_counter: int = 0

    def add_layer(self, spec: DataLayerSpec) -> None:
        """Register a data layer spec."""
        self._layers[spec.layer_id] = spec

    def remove_layer(self, layer_id: str) -> bool:
        """Remove a data layer by ID."""
        if layer_id in self._layers:
            del self._layers[layer_id]
            self._states.pop(layer_id, None)
            return True
        return False

    def get_layer(self, layer_id: str) -> Optional[DataLayerSpec]:
        """Retrieve a data layer by ID."""
        return self._layers.get(layer_id)

    def get_all_layers(self) -> List[DataLayerSpec]:
        """Return all registered data layers."""
        return list(self._layers.values())

    def assign_actor(self, assignment: DataLayerActorAssignment) -> bool:
        """Assign an actor to a data layer."""
        if assignment.layer_id not in self._layers:
            return False
        self._assignments[assignment.assignment_id] = assignment
        return True

    def unassign_actor(self, assignment_id: str) -> bool:
        """Remove an actor assignment by ID."""
        if assignment_id in self._assignments:
            del self._assignments[assignment_id]
            return True
        return False

    def set_layer_state(self, layer_id: str, state: str) -> DataLayerState:
        """Set the state of a data layer and return the updated state object."""
        self._state_counter += 1
        state_id = f"state_{self._state_counter:04d}"
        existing = self._states.get(layer_id)
        previous = existing.current_state if existing else "Unloaded"
        new_state = DataLayerState(
            state_id=state_id,
            layer_id=layer_id,
            current_state=state,
            previous_state=previous,
        )
        self._states[layer_id] = new_state
        return new_state

    def get_state(self, layer_id: str) -> Optional[DataLayerState]:
        """Retrieve the current state for a data layer."""
        return self._states.get(layer_id)

    def get_layers_by_type(self, layer_type: str) -> List[DataLayerSpec]:
        """Return all data layers matching the given type."""
        return [s for s in self._layers.values() if s.layer_type == layer_type]

    def get_actors_by_layer(self, layer_id: str) -> List[str]:
        """Return all actor IDs assigned to a given data layer."""
        return [a.actor_id for a in self._assignments.values() if a.layer_id == layer_id]

    def get_child_layers(self, parent_id: str) -> List[DataLayerSpec]:
        """Return all data layers whose parent is the given parent_id."""
        return [s for s in self._layers.values() if s.parent_id == parent_id]

    def validate(self, spec: DataLayerSpec) -> bool:
        """Validate a data layer spec has required fields."""
        return bool(spec.layer_id) and bool(spec.layer_name)

    def clear(self) -> None:
        """Clear all data layers, assignments, and states."""
        self._layers.clear()
        self._assignments.clear()
        self._states.clear()

    @property
    def layer_count(self) -> int:
        return len(self._layers)

    @property
    def is_empty(self) -> bool:
        return len(self._layers) == 0
