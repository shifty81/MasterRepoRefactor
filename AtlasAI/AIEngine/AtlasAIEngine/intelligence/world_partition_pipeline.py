"""AtlasAI Phase 34B — World Partition Pipeline.

Manages world partition streaming cells, HLOD layers, and
partition entries for the World Partition authoring subsystem.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class StreamingCellDef:
    """Definition of a single streaming cell within a world partition grid."""

    cell_id: str
    grid_id: str
    bounds_min: list = field(default_factory=lambda: [0.0, 0.0, 0.0])
    bounds_max: list = field(default_factory=lambda: [1.0, 1.0, 1.0])
    cell_state: str = "Unloaded"
    data_layers: list = field(default_factory=list)

    @property
    def is_loaded(self) -> bool:
        return self.cell_state == "Loaded"

    @property
    def has_data_layers(self) -> bool:
        return bool(self.data_layers)


@dataclass
class HLODLayerConfig:
    """Configuration for an HLOD layer within a world partition entry."""

    hlod_id: str
    layer_name: str
    hlod_type: str = "MeshMerge"    # MeshMerge/Instancing/Approximation/Custom
    min_vis_size: float = 0.01
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_approximation(self) -> bool:
        return self.hlod_type == "Approximation"


@dataclass
class WorldPartitionEntry:
    """Entry representing a world partition configuration."""

    entry_id: str
    world_name: str
    cell_size: float = 12800.0
    loading_radius: float = 25600.0
    unloading_radius: float = 30000.0
    cells: list = field(default_factory=list)
    hlod_layers: list = field(default_factory=list)
    streaming_enabled: bool = True

    @property
    def is_streaming_enabled(self) -> bool:
        return self.streaming_enabled

    @property
    def has_cells(self) -> bool:
        return bool(self.cells)

    @property
    def has_hlod(self) -> bool:
        return bool(self.hlod_layers)


class WorldPartitionPipeline:
    """Pipeline for managing world partition entries, cells, and HLOD layers."""

    def __init__(self) -> None:
        self._worlds: Dict[str, WorldPartitionEntry] = {}
        self._cells: Dict[str, Dict[str, StreamingCellDef]] = {}
        self._hlod_layers: Dict[str, List[HLODLayerConfig]] = {}

    def add_world(self, entry: WorldPartitionEntry) -> None:
        """Register a world partition entry."""
        self._worlds[entry.entry_id] = entry
        self._cells.setdefault(entry.entry_id, {})
        self._hlod_layers.setdefault(entry.entry_id, [])

    def remove_world(self, entry_id: str) -> bool:
        """Remove a world partition entry by ID."""
        if entry_id in self._worlds:
            del self._worlds[entry_id]
            self._cells.pop(entry_id, None)
            self._hlod_layers.pop(entry_id, None)
            return True
        return False

    def get_world(self, entry_id: str) -> Optional[WorldPartitionEntry]:
        """Retrieve a world partition entry by ID."""
        return self._worlds.get(entry_id)

    def get_all_worlds(self) -> List[WorldPartitionEntry]:
        """Return all registered world partition entries."""
        return list(self._worlds.values())

    def add_cell(self, entry_id: str, cell: StreamingCellDef) -> bool:
        """Add a streaming cell to a world partition entry."""
        if entry_id not in self._worlds:
            return False
        self._cells.setdefault(entry_id, {})[cell.cell_id] = cell
        entry = self._worlds[entry_id]
        if cell.cell_id not in entry.cells:
            entry.cells.append(cell.cell_id)
        return True

    def add_hlod_layer(self, entry_id: str, hlod: HLODLayerConfig) -> bool:
        """Add an HLOD layer to a world partition entry."""
        if entry_id not in self._worlds:
            return False
        self._hlod_layers.setdefault(entry_id, []).append(hlod)
        entry = self._worlds[entry_id]
        if hlod.hlod_id not in entry.hlod_layers:
            entry.hlod_layers.append(hlod.hlod_id)
        return True

    def load_cell(self, entry_id: str, cell_id: str) -> bool:
        """Set a cell state to Loaded."""
        cells = self._cells.get(entry_id, {})
        if cell_id in cells:
            cells[cell_id].cell_state = "Loaded"
            return True
        return False

    def unload_cell(self, entry_id: str, cell_id: str) -> bool:
        """Set a cell state to Unloaded."""
        cells = self._cells.get(entry_id, {})
        if cell_id in cells:
            cells[cell_id].cell_state = "Unloaded"
            return True
        return False

    def get_loaded_cells(self, entry_id: str) -> List[StreamingCellDef]:
        """Return all loaded cells for a world partition entry."""
        cells = self._cells.get(entry_id, {})
        return [c for c in cells.values() if c.is_loaded]

    def validate(self, entry: WorldPartitionEntry) -> bool:
        """Validate a world partition entry has required fields."""
        return bool(entry.entry_id) and bool(entry.world_name)

    def clear(self) -> None:
        """Clear all world partition data."""
        self._worlds.clear()
        self._cells.clear()
        self._hlod_layers.clear()

    @property
    def world_count(self) -> int:
        return len(self._worlds)

    @property
    def is_empty(self) -> bool:
        return len(self._worlds) == 0
