"""AtlasAI Phase 37B — Chaos Destruction Pipeline.

Manages geometry collection destruction entries, fragments, and
destruction events for the Chaos physics destruction subsystem.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class GeometryFragmentDef:
    """Definition of a single geometry fragment within a collection."""

    fragment_id: str
    collection_id: str
    volume: float = 0.0
    mass: float = 0.0
    is_kinematic: bool = False

    @property
    def has_mass(self) -> bool:
        return self.mass > 0.0

    @property
    def is_large(self) -> bool:
        return self.volume > 1000.0


@dataclass
class DestructionEventDef:
    """Definition of a destruction event recorded for a geometry collection."""

    event_id: str
    collection_id: str
    damage_amount: float = 0.0
    impact_velocity: float = 0.0
    time_step: float = 0.0

    @property
    def is_lethal(self) -> bool:
        return self.damage_amount > 100.0

    @property
    def has_impact(self) -> bool:
        return self.impact_velocity > 0.0


@dataclass
class GeometryCollectionEntry:
    """Entry representing a full geometry collection definition."""

    collection_id: str
    collection_name: str
    fragments: list = field(default_factory=list)
    events: list = field(default_factory=list)
    enabled: bool = True

    @property
    def is_empty(self) -> bool:
        return not self.fragments

    @property
    def fragment_count(self) -> int:
        return len(self.fragments)

    @property
    def has_events(self) -> bool:
        return bool(self.events)

    @property
    def is_enabled(self) -> bool:
        return self.enabled


class ChaosDestructionPipeline:
    """Pipeline for managing geometry collection destruction entries."""

    def __init__(self) -> None:
        self._collections: Dict[str, GeometryCollectionEntry] = {}
        self._fragments: Dict[str, Dict[str, GeometryFragmentDef]] = {}
        self._events: Dict[str, Dict[str, DestructionEventDef]] = {}

    def add_collection(self, collection: GeometryCollectionEntry) -> None:
        """Register a geometry collection."""
        self._collections[collection.collection_id] = collection
        self._fragments.setdefault(collection.collection_id, {})
        self._events.setdefault(collection.collection_id, {})

    def get_collection(self, collection_id: str) -> Optional[GeometryCollectionEntry]:
        """Retrieve a collection by ID."""
        return self._collections.get(collection_id)

    def remove_collection(self, collection_id: str) -> bool:
        """Remove a collection by ID."""
        if collection_id in self._collections:
            del self._collections[collection_id]
            self._fragments.pop(collection_id, None)
            self._events.pop(collection_id, None)
            return True
        return False

    def get_all_collections(self) -> List[GeometryCollectionEntry]:
        """Return all registered collections."""
        return list(self._collections.values())

    def add_fragment(self, collection_id: str, fragment: GeometryFragmentDef) -> bool:
        """Add a fragment to a collection."""
        if collection_id not in self._collections:
            return False
        self._fragments.setdefault(collection_id, {})[fragment.fragment_id] = fragment
        collection = self._collections[collection_id]
        if fragment.fragment_id not in collection.fragments:
            collection.fragments.append(fragment.fragment_id)
        return True

    def remove_fragment(self, collection_id: str, fragment_id: str) -> bool:
        """Remove a fragment from a collection."""
        fragments = self._fragments.get(collection_id, {})
        if fragment_id in fragments:
            del fragments[fragment_id]
            collection = self._collections.get(collection_id)
            if collection and fragment_id in collection.fragments:
                collection.fragments.remove(fragment_id)
            return True
        return False

    def get_fragments_for_collection(self, collection_id: str) -> List[GeometryFragmentDef]:
        """Return all fragments for a given collection."""
        return list(self._fragments.get(collection_id, {}).values())

    def add_event(self, collection_id: str, event: DestructionEventDef) -> bool:
        """Add a destruction event to a collection."""
        if collection_id not in self._collections:
            return False
        self._events.setdefault(collection_id, {})[event.event_id] = event
        collection = self._collections[collection_id]
        if event.event_id not in collection.events:
            collection.events.append(event.event_id)
        return True

    def remove_event(self, collection_id: str, event_id: str) -> bool:
        """Remove an event from a collection."""
        events = self._events.get(collection_id, {})
        if event_id in events:
            del events[event_id]
            collection = self._collections.get(collection_id)
            if collection and event_id in collection.events:
                collection.events.remove(event_id)
            return True
        return False

    def get_events_for_collection(self, collection_id: str) -> List[DestructionEventDef]:
        """Return all events for a given collection."""
        return list(self._events.get(collection_id, {}).values())

    def get_lethal_events(self) -> List[DestructionEventDef]:
        """Return all lethal destruction events across all collections."""
        result = []
        for event_map in self._events.values():
            for event in event_map.values():
                if event.is_lethal:
                    result.append(event)
        return result

    def set_enabled(self, collection_id: str, enabled: bool) -> bool:
        """Enable or disable a collection."""
        collection = self._collections.get(collection_id)
        if collection is None:
            return False
        collection.enabled = enabled
        return True

    def get_enabled_collections(self) -> List[GeometryCollectionEntry]:
        """Return all enabled collections."""
        return [c for c in self._collections.values() if c.is_enabled]

    def get_disabled_collections(self) -> List[GeometryCollectionEntry]:
        """Return all disabled collections."""
        return [c for c in self._collections.values() if not c.is_enabled]

    def validate(self, entry: GeometryCollectionEntry) -> bool:
        """Validate a collection entry has required fields."""
        return bool(entry.collection_id) and bool(entry.collection_name)

    def clear(self) -> None:
        """Clear all pipeline data."""
        self._collections.clear()
        self._fragments.clear()
        self._events.clear()

    @property
    def collection_count(self) -> int:
        return len(self._collections)

    @property
    def is_empty(self) -> bool:
        return len(self._collections) == 0
