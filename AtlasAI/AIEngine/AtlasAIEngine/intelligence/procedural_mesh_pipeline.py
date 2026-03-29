"""AtlasAI Phase 29B — Procedural mesh generation pipeline."""
from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)

_SUPPORTED_TYPES = ["Plane", "Sphere", "Box", "Cylinder", "Cone", "Custom"]


@dataclass
class MeshGenerationParams:
    """Parameters for procedural mesh generation."""

    param_id: str
    mesh_type: str = "Plane"  # Plane, Sphere, Box, Cylinder, Cone, Custom
    resolution_u: int = 8
    resolution_v: int = 8
    scale_x: float = 1.0
    scale_y: float = 1.0
    scale_z: float = 1.0
    use_uv: bool = True
    use_normals: bool = True

    @property
    def vertex_estimate(self) -> int:
        return (self.resolution_u + 1) * (self.resolution_v + 1)

    @property
    def is_subdivided(self) -> bool:
        return self.resolution_u > 1 and self.resolution_v > 1


@dataclass
class MeshGenerationResult:
    """Result of a single mesh generation."""

    result_id: str
    success: bool = True
    vertex_count: int = 0
    triangle_count: int = 0
    has_uvs: bool = True
    has_normals: bool = True
    errors: List[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.success and self.vertex_count >= 0 and len(self.errors) == 0

    @property
    def total_primitives(self) -> int:
        return self.vertex_count + self.triangle_count


@dataclass
class ProceduralMeshBatch:
    """A batch of mesh generation parameter sets."""

    batch_id: str
    params: List[MeshGenerationParams] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.params)

    @property
    def is_empty(self) -> bool:
        return len(self.params) == 0


class ProceduralMeshPipeline:
    """Pipeline for generating procedural meshes."""

    def __init__(self) -> None:
        self._cache: dict[str, MeshGenerationResult] = {}

    def generate(self, params: MeshGenerationParams) -> MeshGenerationResult:
        """Generate a mesh from the given parameters."""
        if not self.validate(params):
            result = MeshGenerationResult(
                result_id=str(uuid.uuid4()),
                success=False,
                errors=[f"Invalid params: {params.param_id}"],
            )
            return result
        vertex_count = params.vertex_estimate
        triangle_count = params.resolution_u * params.resolution_v * 2
        result = MeshGenerationResult(
            result_id=str(uuid.uuid4()),
            success=True,
            vertex_count=vertex_count,
            triangle_count=triangle_count,
            has_uvs=params.use_uv,
            has_normals=params.use_normals,
        )
        self._cache[params.param_id] = result
        return result

    def generate_batch(self, batch: ProceduralMeshBatch) -> List[MeshGenerationResult]:
        """Generate meshes for all params in a batch."""
        return [self.generate(p) for p in batch.params]

    def validate(self, params: MeshGenerationParams) -> bool:
        """Validate mesh generation parameters."""
        return (
            bool(params.param_id)
            and params.mesh_type in _SUPPORTED_TYPES
            and params.resolution_u >= 1
            and params.resolution_v >= 1
        )

    def get_supported_types(self) -> List[str]:
        """Return list of supported mesh types."""
        return list(_SUPPORTED_TYPES)

    def clear_cache(self) -> None:
        """Clear the result cache."""
        self._cache.clear()

    @property
    def cache_size(self) -> int:
        return len(self._cache)
