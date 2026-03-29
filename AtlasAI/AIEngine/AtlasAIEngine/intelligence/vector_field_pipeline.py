"""AtlasAI Phase 43B — Vector Field Pipeline.

Manages vector field volumes, flow visualizations, and particle coupling
for the VectorFieldEditorTool cross-language pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class VectorFieldEntry:
    """A vector field volume definition."""
    field_id: str
    field_name: str
    field_type: str = "Uniform"
    dimension: str = "ThreeD"
    data_type: str = "Float16"
    resolution_x: int = 32
    resolution_y: int = 32
    resolution_z: int = 32
    bounds_x: float = 100.0
    bounds_y: float = 100.0
    bounds_z: float = 100.0
    intensity: float = 1.0
    enabled: bool = True

    @property
    def is_uniform(self) -> bool:
        return self.field_type == "Uniform"

    @property
    def is_vortex(self) -> bool:
        return self.field_type == "Vortex"

    @property
    def is_turbulent(self) -> bool:
        return self.field_type == "Turbulent"

    @property
    def is_wind(self) -> bool:
        return self.field_type == "Wind"

    @property
    def is_3d(self) -> bool:
        return self.dimension == "ThreeD"

    @property
    def is_2d(self) -> bool:
        return self.dimension == "TwoD"

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def voxel_count(self) -> int:
        if self.is_3d:
            return self.resolution_x * self.resolution_y * self.resolution_z
        return self.resolution_x * self.resolution_y

    @property
    def is_high_res(self) -> bool:
        return self.resolution_x >= 64 and self.resolution_y >= 64

    @property
    def is_float32(self) -> bool:
        return self.data_type == "Float32"

    @property
    def is_float16(self) -> bool:
        return self.data_type == "Float16"

    @property
    def volume(self) -> float:
        return self.bounds_x * self.bounds_y * self.bounds_z


@dataclass
class FlowVisualizationEntry:
    """Flow visualization for a vector field."""
    vis_id: str
    field_id: str
    streamline_count: int = 64
    step_size: float = 0.5
    max_length: float = 50.0
    line_width: float = 1.0
    show_arrows: bool = True
    use_heat_map: bool = False
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def shows_arrows(self) -> bool:
        return self.show_arrows

    @property
    def uses_heat_map(self) -> bool:
        return self.use_heat_map

    @property
    def is_dense(self) -> bool:
        return self.streamline_count >= 128

    @property
    def is_fine_step(self) -> bool:
        return self.step_size <= 0.1


@dataclass
class ParticleCouplingEntry:
    """Particle system coupling to a vector field."""
    coupling_id: str
    field_id: str
    particle_system_id: str = ""
    coupling_type: str = "OneWay"
    influence_radius: float = 10.0
    strength_scale: float = 1.0
    drag_coefficient: float = 0.1
    enabled: bool = True

    @property
    def is_one_way(self) -> bool:
        return self.coupling_type == "OneWay"

    @property
    def is_two_way(self) -> bool:
        return self.coupling_type == "TwoWay"

    @property
    def is_disabled_coupling(self) -> bool:
        return self.coupling_type == "None"

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def has_particle_system(self) -> bool:
        return bool(self.particle_system_id)

    @property
    def is_strong(self) -> bool:
        return self.strength_scale > 2.0

    @property
    def is_high_drag(self) -> bool:
        return self.drag_coefficient > 0.5


class VectorFieldPipeline:
    """Pipeline managing vector field entries, flow visualizations, and particle couplings."""

    def __init__(self) -> None:
        self._fields: Dict[str, VectorFieldEntry] = {}
        self._visualizations: Dict[str, Dict[str, FlowVisualizationEntry]] = {}
        self._couplings: Dict[str, Dict[str, ParticleCouplingEntry]] = {}

    def add_field(self, entry: VectorFieldEntry) -> bool:
        if not entry.field_id:
            return False
        self._fields[entry.field_id] = entry
        self._visualizations.setdefault(entry.field_id, {})
        self._couplings.setdefault(entry.field_id, {})
        return True

    def get_field(self, field_id: str) -> Optional[VectorFieldEntry]:
        return self._fields.get(field_id)

    def remove_field(self, field_id: str) -> bool:
        if field_id not in self._fields:
            return False
        del self._fields[field_id]
        self._visualizations.pop(field_id, None)
        self._couplings.pop(field_id, None)
        return True

    def get_all_fields(self) -> List[VectorFieldEntry]:
        return list(self._fields.values())

    def get_fields_by_type(self, field_type: str) -> List[VectorFieldEntry]:
        return [f for f in self._fields.values() if f.field_type == field_type]

    def get_fields_by_dimension(self, dimension: str) -> List[VectorFieldEntry]:
        return [f for f in self._fields.values() if f.dimension == dimension]

    def get_enabled_fields(self) -> List[VectorFieldEntry]:
        return [f for f in self._fields.values() if f.enabled]

    def add_visualization(self, field_id: str, entry: FlowVisualizationEntry) -> bool:
        if field_id not in self._fields:
            return False
        self._visualizations.setdefault(field_id, {})[entry.vis_id] = entry
        return True

    def remove_visualization(self, field_id: str, vis_id: str) -> bool:
        if field_id not in self._visualizations:
            return False
        if vis_id not in self._visualizations[field_id]:
            return False
        del self._visualizations[field_id][vis_id]
        return True

    def get_visualizations_for_field(self, field_id: str) -> List[FlowVisualizationEntry]:
        return list(self._visualizations.get(field_id, {}).values())

    def add_coupling(self, field_id: str, entry: ParticleCouplingEntry) -> bool:
        if field_id not in self._fields:
            return False
        self._couplings.setdefault(field_id, {})[entry.coupling_id] = entry
        return True

    def remove_coupling(self, field_id: str, coupling_id: str) -> bool:
        if field_id not in self._couplings:
            return False
        if coupling_id not in self._couplings[field_id]:
            return False
        del self._couplings[field_id][coupling_id]
        return True

    def get_couplings_for_field(self, field_id: str) -> List[ParticleCouplingEntry]:
        return list(self._couplings.get(field_id, {}).values())

    def get_couplings_by_type(self, coupling_type: str) -> List[ParticleCouplingEntry]:
        result = []
        for couplings in self._couplings.values():
            result.extend(c for c in couplings.values() if c.coupling_type == coupling_type)
        return result

    def validate(self, entry: VectorFieldEntry) -> bool:
        return bool(entry.field_id) and bool(entry.field_name)

    @property
    def field_count(self) -> int:
        return len(self._fields)

    @property
    def is_empty(self) -> bool:
        return len(self._fields) == 0

    def clear(self) -> None:
        self._fields.clear()
        self._visualizations.clear()
        self._couplings.clear()
