"""AtlasAI Phase 41B — Procedural Terrain Pipeline.

Manages terrain generation entries, biome layers, and erosion simulation configs
for the ProceduralTerrainTool cross-language pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class TerrainGenEntry:
    """A procedural terrain generation definition."""
    gen_id: str
    gen_name: str
    mode: str = "Noise"
    seed: int = 0
    width: float = 1024.0
    height: float = 1024.0
    max_elevation: float = 500.0
    resolution: int = 512
    seamless: bool = False
    generated: bool = False

    @property
    def is_noise(self) -> bool:
        return self.mode == "Noise"

    @property
    def is_heightmap(self) -> bool:
        return self.mode == "Heightmap"

    @property
    def is_generated(self) -> bool:
        return self.generated

    @property
    def is_seamless(self) -> bool:
        return self.seamless

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def aspect_ratio(self) -> float:
        if self.height == 0:
            return 0.0
        return self.width / self.height


@dataclass
class BiomeLayerEntry:
    """A biome layer definition for a terrain."""
    biome_layer_id: str
    gen_id: str
    biome_type: str = "Grassland"
    layer: str = "Base"
    min_elevation: float = 0.0
    max_elevation: float = 1000.0
    blend_weight: float = 1.0
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_base_layer(self) -> bool:
        return self.layer == "Base"

    @property
    def elevation_range(self) -> float:
        return self.max_elevation - self.min_elevation

    @property
    def is_grassland(self) -> bool:
        return self.biome_type == "Grassland"

    @property
    def is_desert(self) -> bool:
        return self.biome_type == "Desert"


@dataclass
class ErosionSimEntry:
    """An erosion simulation configuration."""
    erosion_id: str
    gen_id: str
    erosion_type: str = "Hydraulic"
    iterations: int = 100
    intensity: float = 0.5
    sediment_capacity: float = 1.0
    apply_to_mesh: bool = True
    completed: bool = False

    @property
    def is_hydraulic(self) -> bool:
        return self.erosion_type == "Hydraulic"

    @property
    def is_thermal(self) -> bool:
        return self.erosion_type == "Thermal"

    @property
    def is_completed(self) -> bool:
        return self.completed

    @property
    def is_intensive(self) -> bool:
        return self.iterations > 500

    @property
    def is_high_intensity(self) -> bool:
        return self.intensity > 0.75


class ProceduralTerrainPipeline:
    """Pipeline managing procedural terrain entries, biome layers, and erosion sims."""

    def __init__(self) -> None:
        self._terrains: Dict[str, TerrainGenEntry] = {}
        self._biome_layers: Dict[str, Dict[str, BiomeLayerEntry]] = {}
        self._erosion_sims: Dict[str, Dict[str, ErosionSimEntry]] = {}

    def add_terrain(self, entry: TerrainGenEntry) -> bool:
        if not entry.gen_id:
            return False
        self._terrains[entry.gen_id] = entry
        if entry.gen_id not in self._biome_layers:
            self._biome_layers[entry.gen_id] = {}
        if entry.gen_id not in self._erosion_sims:
            self._erosion_sims[entry.gen_id] = {}
        return True

    def get_terrain(self, gen_id: str) -> Optional[TerrainGenEntry]:
        return self._terrains.get(gen_id)

    def remove_terrain(self, gen_id: str) -> bool:
        if gen_id not in self._terrains:
            return False
        del self._terrains[gen_id]
        self._biome_layers.pop(gen_id, None)
        self._erosion_sims.pop(gen_id, None)
        return True

    def get_all_terrains(self) -> List[TerrainGenEntry]:
        return list(self._terrains.values())

    def get_terrains_by_mode(self, mode: str) -> List[TerrainGenEntry]:
        return [t for t in self._terrains.values() if t.mode == mode]

    def get_generated_terrains(self) -> List[TerrainGenEntry]:
        return [t for t in self._terrains.values() if t.generated]

    def add_biome_layer(self, gen_id: str, layer: BiomeLayerEntry) -> bool:
        if gen_id not in self._terrains:
            return False
        if gen_id not in self._biome_layers:
            self._biome_layers[gen_id] = {}
        self._biome_layers[gen_id][layer.biome_layer_id] = layer
        return True

    def remove_biome_layer(self, gen_id: str, biome_layer_id: str) -> bool:
        if gen_id not in self._biome_layers:
            return False
        if biome_layer_id not in self._biome_layers[gen_id]:
            return False
        del self._biome_layers[gen_id][biome_layer_id]
        return True

    def get_biome_layers_for_terrain(self, gen_id: str) -> List[BiomeLayerEntry]:
        return list(self._biome_layers.get(gen_id, {}).values())

    def get_biome_layers_by_type(self, biome_type: str) -> List[BiomeLayerEntry]:
        result = []
        for layers in self._biome_layers.values():
            result.extend(l for l in layers.values() if l.biome_type == biome_type)
        return result

    def add_erosion_sim(self, gen_id: str, sim: ErosionSimEntry) -> bool:
        if gen_id not in self._terrains:
            return False
        if gen_id not in self._erosion_sims:
            self._erosion_sims[gen_id] = {}
        self._erosion_sims[gen_id][sim.erosion_id] = sim
        return True

    def remove_erosion_sim(self, gen_id: str, erosion_id: str) -> bool:
        if gen_id not in self._erosion_sims:
            return False
        if erosion_id not in self._erosion_sims[gen_id]:
            return False
        del self._erosion_sims[gen_id][erosion_id]
        return True

    def get_erosion_sims_for_terrain(self, gen_id: str) -> List[ErosionSimEntry]:
        return list(self._erosion_sims.get(gen_id, {}).values())

    def run_erosion(self, gen_id: str, erosion_id: str) -> bool:
        sims = self._erosion_sims.get(gen_id, {})
        if erosion_id not in sims:
            return False
        sims[erosion_id].completed = True
        return True

    def validate(self, entry: TerrainGenEntry) -> bool:
        return bool(entry.gen_id) and bool(entry.gen_name)

    @property
    def terrain_count(self) -> int:
        return len(self._terrains)

    @property
    def is_empty(self) -> bool:
        return len(self._terrains) == 0

    def clear(self) -> None:
        self._terrains.clear()
        self._biome_layers.clear()
        self._erosion_sims.clear()
