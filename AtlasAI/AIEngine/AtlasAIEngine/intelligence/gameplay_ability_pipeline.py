"""AtlasAI Phase 33B — Gameplay Ability Pipeline.

Manages gameplay ability entries, costs, effects, and compilation
for the Gameplay Ability System authoring subsystem.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class AbilityCostDef:
    """Definition for a single ability cost."""

    cost_id: str
    cost_name: str
    attribute_name: str = "Mana"
    cost_value: float = 10.0
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def has_attribute(self) -> bool:
        return bool(self.attribute_name)


@dataclass
class AbilityEffectDef:
    """Definition for a gameplay effect applied by an ability."""

    effect_id: str
    effect_name: str
    application_type: str = "Instant"   # Instant/Duration/Infinite/Periodic
    duration: float = 0.0
    period: float = 0.0
    magnitude: float = 0.0
    attribute_name: str = ""

    @property
    def is_instant(self) -> bool:
        return self.application_type == "Instant"

    @property
    def is_periodic(self) -> bool:
        return self.application_type == "Periodic"


@dataclass
class AbilityEntry:
    """A single gameplay ability entry tracked by the pipeline."""

    entry_id: str
    ability_name: str
    activation_policy: str = "OnInputAction"
    end_policy: str = "WhenCompleted"
    cooldown: float = 0.0
    costs: list = field(default_factory=list)
    effects: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    version: int = 1
    compiled: bool = False

    @property
    def is_compiled(self) -> bool:
        return self.compiled

    @property
    def has_costs(self) -> bool:
        return bool(self.costs)

    @property
    def has_effects(self) -> bool:
        return bool(self.effects)


class GameplayAbilityPipeline:
    """Pipeline for managing and compiling gameplay ability entries."""

    def __init__(self) -> None:
        self._abilities: Dict[str, AbilityEntry] = {}

    def add_ability(self, entry: AbilityEntry) -> None:
        """Register a gameplay ability entry."""
        self._abilities[entry.entry_id] = entry

    def remove_ability(self, entry_id: str) -> bool:
        """Remove an ability entry by ID."""
        if entry_id in self._abilities:
            del self._abilities[entry_id]
            return True
        return False

    def get_ability(self, entry_id: str) -> Optional[AbilityEntry]:
        """Retrieve an ability entry by ID."""
        return self._abilities.get(entry_id)

    def get_all_abilities(self) -> List[AbilityEntry]:
        """Return all registered ability entries."""
        return list(self._abilities.values())

    def add_cost(self, entry_id: str, cost: AbilityCostDef) -> bool:
        """Add a cost definition to an ability entry."""
        entry = self._abilities.get(entry_id)
        if entry is None:
            return False
        entry.costs.append(cost)
        return True

    def add_effect(self, entry_id: str, effect: AbilityEffectDef) -> bool:
        """Add an effect definition to an ability entry."""
        entry = self._abilities.get(entry_id)
        if entry is None:
            return False
        entry.effects.append(effect)
        return True

    def compile(self, entry_id: str) -> bool:
        """Mark a single ability entry as compiled."""
        entry = self._abilities.get(entry_id)
        if entry is None:
            return False
        entry.compiled = True
        logger.debug("Compiled ability entry %s", entry_id)
        return True

    def compile_all(self) -> Dict[str, bool]:
        """Compile all registered ability entries and return results by ID."""
        results = {}
        for eid in list(self._abilities):
            results[eid] = self.compile(eid)
        return results

    def invalidate(self, entry_id: str) -> bool:
        """Invalidate a single ability entry's compiled state."""
        entry = self._abilities.get(entry_id)
        if entry is None:
            return False
        entry.compiled = False
        return True

    def invalidate_all(self) -> None:
        """Invalidate all compiled ability entries."""
        for entry in self._abilities.values():
            entry.compiled = False

    def get_uncompiled(self) -> List[AbilityEntry]:
        """Return all entries that have not yet been compiled."""
        return [e for e in self._abilities.values() if not e.compiled]

    def validate(self, entry: AbilityEntry) -> bool:
        """Validate an ability entry has required fields."""
        return bool(entry.entry_id) and bool(entry.ability_name)

    def clear(self) -> None:
        """Clear all ability entries."""
        self._abilities.clear()

    @property
    def ability_count(self) -> int:
        return len(self._abilities)

    @property
    def is_empty(self) -> bool:
        return len(self._abilities) == 0
