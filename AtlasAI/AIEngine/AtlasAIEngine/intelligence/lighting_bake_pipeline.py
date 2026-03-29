"""AtlasAI Phase 31B — Lighting Bake Pipeline.

Manages lightmap bake passes, entries, and budget configuration for
the lighting baking subsystem used in static and semi-static scenes.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class BakePassDef:
    """Definition for a single lighting bake pass."""

    pass_id: str
    pass_name: str
    pass_type: str = "Direct"   # Direct/Indirect/Ambient/Emissive/Shadow/Combined
    resolution: int = 512
    samples: int = 64
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_high_res(self) -> bool:
        return self.resolution >= 1024


@dataclass
class LightmapEntry:
    """A single mesh entry tracked for lightmap baking."""

    entry_id: str
    mesh_path: str
    lightmap_path: str = ""
    bake_pass: str = "Direct"
    uv_channel: int = 1
    padding: int = 2
    version: int = 1
    baked: bool = False

    @property
    def is_baked(self) -> bool:
        return self.baked

    @property
    def needs_rebake(self) -> bool:
        return not self.baked


@dataclass
class BakeBudget:
    """Budget constraints for the lighting bake pipeline."""

    max_resolution: int = 2048
    max_samples: int = 512
    time_limit_sec: float = 3600.0
    memory_limit_mb: int = 4096

    @property
    def is_high_budget(self) -> bool:
        return self.max_samples >= 256


class LightingBakePipeline:
    """Pipeline for managing and executing lightmap bake jobs."""

    def __init__(self) -> None:
        self._entries: Dict[str, LightmapEntry] = {}
        self._passes: Dict[str, BakePassDef] = {}
        self._budget: BakeBudget = BakeBudget()

    def add_entry(self, entry: LightmapEntry) -> None:
        """Register a lightmap entry in the pipeline."""
        self._entries[entry.entry_id] = entry

    def remove_entry(self, entry_id: str) -> bool:
        """Remove a lightmap entry by ID."""
        if entry_id in self._entries:
            del self._entries[entry_id]
            return True
        return False

    def get_entry(self, entry_id: str) -> Optional[LightmapEntry]:
        """Retrieve a lightmap entry by ID."""
        return self._entries.get(entry_id)

    def get_all_entries(self) -> List[LightmapEntry]:
        """Return all registered lightmap entries."""
        return list(self._entries.values())

    def add_pass(self, bake_pass: BakePassDef) -> None:
        """Register a bake pass definition."""
        self._passes[bake_pass.pass_id] = bake_pass

    def get_pass(self, pass_id: str) -> Optional[BakePassDef]:
        """Retrieve a bake pass by ID."""
        return self._passes.get(pass_id)

    def bake(self, entry_id: str) -> bool:
        """Mark a single entry as baked."""
        entry = self._entries.get(entry_id)
        if entry is None:
            return False
        entry.baked = True
        logger.debug("Baked entry %s", entry_id)
        return True

    def bake_all(self) -> Dict[str, bool]:
        """Bake all registered entries and return results by ID."""
        results = {}
        for eid in list(self._entries):
            results[eid] = self.bake(eid)
        return results

    def invalidate(self, entry_id: str) -> bool:
        """Invalidate a single entry's baked state."""
        entry = self._entries.get(entry_id)
        if entry is None:
            return False
        entry.baked = False
        return True

    def invalidate_all(self) -> None:
        """Invalidate all baked entries."""
        for entry in self._entries.values():
            entry.baked = False

    def set_budget(self, budget: BakeBudget) -> None:
        """Set the bake budget constraints."""
        self._budget = budget

    def get_budget(self) -> BakeBudget:
        """Return the current bake budget."""
        return self._budget

    def get_unbaked(self) -> List[LightmapEntry]:
        """Return all entries that have not yet been baked."""
        return [e for e in self._entries.values() if not e.baked]

    def clear(self) -> None:
        """Clear all entries and passes."""
        self._entries.clear()
        self._passes.clear()

    @property
    def entry_count(self) -> int:
        return len(self._entries)

    @property
    def pass_count(self) -> int:
        return len(self._passes)

    @property
    def is_empty(self) -> bool:
        return len(self._entries) == 0
