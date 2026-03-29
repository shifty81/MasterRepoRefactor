"""AtlasAI Phase 37B — Hair Groom Pipeline.

Manages groom asset entries, strands, and LOD definitions
for the hair groom simulation and rendering subsystem.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class GroomStrandDef:
    """Definition of a single hair strand within a groom asset."""

    strand_id: str
    groom_id: str
    strand_type: str = "Guide"
    width: float = 0.5
    length: float = 10.0

    @property
    def is_guide(self) -> bool:
        return self.strand_type == "Guide"

    @property
    def is_long(self) -> bool:
        return self.length > 20.0


@dataclass
class GroomLODEntry:
    """LOD entry for a groom asset."""

    lod_id: str
    groom_id: str
    lod_level: int = 0
    screen_size: float = 1.0
    strand_ratio: float = 1.0

    @property
    def is_highest_lod(self) -> bool:
        return self.lod_level == 0

    @property
    def is_culled(self) -> bool:
        return self.strand_ratio == 0.0


@dataclass
class GroomAssetEntry:
    """Entry representing a full groom asset definition."""

    groom_id: str
    groom_name: str
    sim_mode: str = "Disabled"
    strands: list = field(default_factory=list)
    lods: list = field(default_factory=list)
    enabled: bool = True

    @property
    def is_empty(self) -> bool:
        return not self.strands

    @property
    def has_lods(self) -> bool:
        return bool(self.lods)

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_simulated(self) -> bool:
        return self.sim_mode != "Disabled"


class HairGroomPipeline:
    """Pipeline for managing groom assets and simulation entries."""

    def __init__(self) -> None:
        self._grooms: Dict[str, GroomAssetEntry] = {}
        self._strands: Dict[str, Dict[str, GroomStrandDef]] = {}
        self._lods: Dict[str, Dict[str, GroomLODEntry]] = {}

    def add_groom(self, groom: GroomAssetEntry) -> None:
        """Register a groom asset."""
        self._grooms[groom.groom_id] = groom
        self._strands.setdefault(groom.groom_id, {})
        self._lods.setdefault(groom.groom_id, {})

    def get_groom(self, groom_id: str) -> Optional[GroomAssetEntry]:
        """Retrieve a groom by ID."""
        return self._grooms.get(groom_id)

    def remove_groom(self, groom_id: str) -> bool:
        """Remove a groom by ID."""
        if groom_id in self._grooms:
            del self._grooms[groom_id]
            self._strands.pop(groom_id, None)
            self._lods.pop(groom_id, None)
            return True
        return False

    def get_all_grooms(self) -> List[GroomAssetEntry]:
        """Return all registered grooms."""
        return list(self._grooms.values())

    def add_strand(self, groom_id: str, strand: GroomStrandDef) -> bool:
        """Add a strand to a groom."""
        if groom_id not in self._grooms:
            return False
        self._strands.setdefault(groom_id, {})[strand.strand_id] = strand
        groom = self._grooms[groom_id]
        if strand.strand_id not in groom.strands:
            groom.strands.append(strand.strand_id)
        return True

    def remove_strand(self, groom_id: str, strand_id: str) -> bool:
        """Remove a strand from a groom."""
        strands = self._strands.get(groom_id, {})
        if strand_id in strands:
            del strands[strand_id]
            groom = self._grooms.get(groom_id)
            if groom and strand_id in groom.strands:
                groom.strands.remove(strand_id)
            return True
        return False

    def get_strands_for_groom(self, groom_id: str) -> List[GroomStrandDef]:
        """Return all strands for a given groom."""
        return list(self._strands.get(groom_id, {}).values())

    def add_lod(self, groom_id: str, lod: GroomLODEntry) -> bool:
        """Add a LOD entry to a groom."""
        if groom_id not in self._grooms:
            return False
        self._lods.setdefault(groom_id, {})[lod.lod_id] = lod
        groom = self._grooms[groom_id]
        if lod.lod_id not in groom.lods:
            groom.lods.append(lod.lod_id)
        return True

    def remove_lod(self, groom_id: str, lod_id: str) -> bool:
        """Remove a LOD entry from a groom."""
        lods = self._lods.get(groom_id, {})
        if lod_id in lods:
            del lods[lod_id]
            groom = self._grooms.get(groom_id)
            if groom and lod_id in groom.lods:
                groom.lods.remove(lod_id)
            return True
        return False

    def get_lods_for_groom(self, groom_id: str) -> List[GroomLODEntry]:
        """Return all LOD entries for a given groom."""
        return list(self._lods.get(groom_id, {}).values())

    def get_simulated_grooms(self) -> List[GroomAssetEntry]:
        """Return all grooms with simulation enabled."""
        return [g for g in self._grooms.values() if g.is_simulated]

    def get_guide_strands(self, groom_id: str) -> List[GroomStrandDef]:
        """Return all guide strands for a given groom."""
        return [s for s in self._strands.get(groom_id, {}).values() if s.is_guide]

    def set_enabled(self, groom_id: str, enabled: bool) -> bool:
        """Enable or disable a groom."""
        groom = self._grooms.get(groom_id)
        if groom is None:
            return False
        groom.enabled = enabled
        return True

    def get_enabled_grooms(self) -> List[GroomAssetEntry]:
        """Return all enabled grooms."""
        return [g for g in self._grooms.values() if g.is_enabled]

    def get_disabled_grooms(self) -> List[GroomAssetEntry]:
        """Return all disabled grooms."""
        return [g for g in self._grooms.values() if not g.is_enabled]

    def validate(self, entry: GroomAssetEntry) -> bool:
        """Validate a groom entry has required fields."""
        return bool(entry.groom_id) and bool(entry.groom_name)

    def clear(self) -> None:
        """Clear all pipeline data."""
        self._grooms.clear()
        self._strands.clear()
        self._lods.clear()

    @property
    def groom_count(self) -> int:
        return len(self._grooms)

    @property
    def is_empty(self) -> bool:
        return len(self._grooms) == 0
