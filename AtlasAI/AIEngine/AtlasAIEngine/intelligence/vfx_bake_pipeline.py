"""AtlasAI Phase 32B — VFX Bake Pipeline.

Manages VFX bake passes, atlas entries, and configuration for
the VFX baking subsystem used for particle, ribbon, and volumetric effects.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class VFXBakePassDef:
    """Definition for a single VFX bake pass."""

    pass_id: str
    pass_name: str
    effect_type: str = "Particle"   # Particle/Ribbon/Mesh/Trail/Beam/Volume
    resolution: int = 512
    sample_count: int = 64
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_volumetric(self) -> bool:
        return self.effect_type == "Volume"


@dataclass
class VFXBakeEntry:
    """A single VFX asset entry tracked for baking."""

    entry_id: str
    asset_path: str
    baked_path: str = ""
    pass_type: str = "Particle"
    uv_channel: int = 0
    atlas_rows: int = 4
    atlas_cols: int = 4
    version: int = 1
    baked: bool = False

    @property
    def is_baked(self) -> bool:
        return self.baked

    @property
    def needs_rebake(self) -> bool:
        return not self.baked


@dataclass
class VFXAtlasSettings:
    """Atlas configuration for a baked VFX flipbook."""

    atlas_id: str
    rows: int = 4
    cols: int = 4
    total_frames: int = 0
    frame_rate: float = 30.0
    loop: bool = True

    @property
    def frame_count(self) -> int:
        return self.rows * self.cols

    @property
    def is_looping(self) -> bool:
        return self.loop


class VFXBakePipeline:
    """Pipeline for managing and executing VFX bake jobs."""

    def __init__(self) -> None:
        self._entries: Dict[str, VFXBakeEntry] = {}
        self._passes: Dict[str, VFXBakePassDef] = {}
        self._atlas_settings: Optional[VFXAtlasSettings] = None

    def add_entry(self, entry: VFXBakeEntry) -> None:
        """Register a VFX bake entry in the pipeline."""
        self._entries[entry.entry_id] = entry

    def remove_entry(self, entry_id: str) -> bool:
        """Remove a VFX bake entry by ID."""
        if entry_id in self._entries:
            del self._entries[entry_id]
            return True
        return False

    def get_entry(self, entry_id: str) -> Optional[VFXBakeEntry]:
        """Retrieve a VFX bake entry by ID."""
        return self._entries.get(entry_id)

    def get_all_entries(self) -> List[VFXBakeEntry]:
        """Return all registered bake entries."""
        return list(self._entries.values())

    def add_pass(self, bake_pass: VFXBakePassDef) -> None:
        """Register a VFX bake pass definition."""
        self._passes[bake_pass.pass_id] = bake_pass

    def get_pass(self, pass_id: str) -> Optional[VFXBakePassDef]:
        """Retrieve a bake pass by ID."""
        return self._passes.get(pass_id)

    def bake(self, entry_id: str) -> bool:
        """Mark a single entry as baked."""
        entry = self._entries.get(entry_id)
        if entry is None:
            return False
        entry.baked = True
        logger.debug("Baked VFX entry %s", entry_id)
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

    def set_atlas_settings(self, settings: VFXAtlasSettings) -> None:
        """Set the atlas configuration for the pipeline."""
        self._atlas_settings = settings

    def get_atlas_settings(self) -> Optional[VFXAtlasSettings]:
        """Return the current atlas settings."""
        return self._atlas_settings

    def get_unbaked(self) -> List[VFXBakeEntry]:
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
