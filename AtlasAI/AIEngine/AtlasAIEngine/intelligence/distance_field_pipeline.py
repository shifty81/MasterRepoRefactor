"""AtlasAI Phase 42B — Distance Field Pipeline.

Manages distance field entries, shadow configurations, and blend operations
for the DistanceFieldTool cross-language pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class DistanceFieldEntry:
    """A distance field definition."""
    field_id: str
    field_name: str
    shape: str = "Sphere"
    resolution: str = "Medium"
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    scale_z: float = 1.0
    blend_radius: float = 0.0
    self_shadow: bool = True
    enabled: bool = True

    @property
    def is_sphere(self) -> bool:
        return self.shape == "Sphere"

    @property
    def is_box(self) -> bool:
        return self.shape == "Box"

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_high_res(self) -> bool:
        return self.resolution in ("High", "Ultra")

    @property
    def has_blend(self) -> bool:
        return self.blend_radius > 0.0

    @property
    def is_at_origin(self) -> bool:
        return self.pos_x == 0.0 and self.pos_y == 0.0 and self.pos_z == 0.0

    @property
    def uniform_scale(self) -> bool:
        return self.scale_x == self.scale_y == self.scale_z


@dataclass
class ShadowConfigEntry:
    """A shadow configuration for a distance field."""
    shadow_config_id: str
    field_id: str
    shadow_type: str = "Soft"
    penumbra_angle: float = 3.0
    shadow_bias: float = 0.01
    max_distance: float = 5000.0
    softness_factor: float = 1.0
    cast_shadow: bool = True

    @property
    def is_soft(self) -> bool:
        return self.shadow_type == "Soft"

    @property
    def is_hard(self) -> bool:
        return self.shadow_type == "Hard"

    @property
    def is_ray_traced(self) -> bool:
        return self.shadow_type == "RayTraced"

    @property
    def casts_shadow(self) -> bool:
        return self.cast_shadow

    @property
    def is_wide_penumbra(self) -> bool:
        return self.penumbra_angle > 10.0


@dataclass
class FieldBlendOpEntry:
    """A blend operation between two distance fields."""
    blend_op_id: str
    field_a_id: str
    field_b_id: str
    blend_mode: str = "Union"
    smooth_k: float = 0.1
    enabled: bool = True

    @property
    def is_union(self) -> bool:
        return self.blend_mode == "Union"

    @property
    def is_intersection(self) -> bool:
        return self.blend_mode == "Intersection"

    @property
    def is_subtraction(self) -> bool:
        return self.blend_mode == "Subtraction"

    @property
    def is_smooth(self) -> bool:
        return self.blend_mode == "SmoothUnion"

    @property
    def is_enabled(self) -> bool:
        return self.enabled


class DistanceFieldPipeline:
    """Pipeline managing distance field entries, shadow configs, and blend ops."""

    def __init__(self) -> None:
        self._fields: Dict[str, DistanceFieldEntry] = {}
        self._shadow_configs: Dict[str, Dict[str, ShadowConfigEntry]] = {}
        self._blend_ops: Dict[str, FieldBlendOpEntry] = {}

    def add_field(self, entry: DistanceFieldEntry) -> bool:
        if not entry.field_id:
            return False
        self._fields[entry.field_id] = entry
        if entry.field_id not in self._shadow_configs:
            self._shadow_configs[entry.field_id] = {}
        return True

    def get_field(self, field_id: str) -> Optional[DistanceFieldEntry]:
        return self._fields.get(field_id)

    def remove_field(self, field_id: str) -> bool:
        if field_id not in self._fields:
            return False
        del self._fields[field_id]
        self._shadow_configs.pop(field_id, None)
        return True

    def get_all_fields(self) -> List[DistanceFieldEntry]:
        return list(self._fields.values())

    def get_fields_by_shape(self, shape: str) -> List[DistanceFieldEntry]:
        return [f for f in self._fields.values() if f.shape == shape]

    def get_enabled_fields(self) -> List[DistanceFieldEntry]:
        return [f for f in self._fields.values() if f.enabled]

    def add_shadow_config(self, field_id: str, config: ShadowConfigEntry) -> bool:
        if field_id not in self._fields:
            return False
        if field_id not in self._shadow_configs:
            self._shadow_configs[field_id] = {}
        self._shadow_configs[field_id][config.shadow_config_id] = config
        return True

    def remove_shadow_config(self, field_id: str, shadow_config_id: str) -> bool:
        if field_id not in self._shadow_configs:
            return False
        if shadow_config_id not in self._shadow_configs[field_id]:
            return False
        del self._shadow_configs[field_id][shadow_config_id]
        return True

    def get_shadow_configs_for_field(self, field_id: str) -> List[ShadowConfigEntry]:
        return list(self._shadow_configs.get(field_id, {}).values())

    def add_blend_op(self, entry: FieldBlendOpEntry) -> bool:
        if not entry.blend_op_id:
            return False
        self._blend_ops[entry.blend_op_id] = entry
        return True

    def remove_blend_op(self, blend_op_id: str) -> bool:
        if blend_op_id not in self._blend_ops:
            return False
        del self._blend_ops[blend_op_id]
        return True

    def get_blend_op(self, blend_op_id: str) -> Optional[FieldBlendOpEntry]:
        return self._blend_ops.get(blend_op_id)

    def get_all_blend_ops(self) -> List[FieldBlendOpEntry]:
        return list(self._blend_ops.values())

    def get_blend_ops_by_mode(self, mode: str) -> List[FieldBlendOpEntry]:
        return [op for op in self._blend_ops.values() if op.blend_mode == mode]

    def validate(self, entry: DistanceFieldEntry) -> bool:
        return bool(entry.field_id) and bool(entry.field_name)

    @property
    def field_count(self) -> int:
        return len(self._fields)

    @property
    def is_empty(self) -> bool:
        return len(self._fields) == 0

    def clear(self) -> None:
        self._fields.clear()
        self._shadow_configs.clear()
        self._blend_ops.clear()
