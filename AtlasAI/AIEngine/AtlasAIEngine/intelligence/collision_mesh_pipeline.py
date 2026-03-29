"""AtlasAI Phase 31B — Collision Mesh Pipeline.

Manages collision shape definitions, mesh entries, and build results for
the physics collision mesh generation subsystem.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class CollisionShapeDef:
    """Definition for a single collision shape."""

    shape_id: str
    shape_name: str
    shape_type: str = "Box"     # Box/Sphere/Capsule/ConvexHull/TriangleMesh/Compound
    scale_x: float = 1.0
    scale_y: float = 1.0
    scale_z: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    offset_z: float = 0.0
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_simple(self) -> bool:
        return self.shape_type in ["Box", "Sphere", "Capsule"]


@dataclass
class CollisionMeshEntry:
    """A single mesh entry with associated collision shapes."""

    entry_id: str
    mesh_path: str
    shapes: list = field(default_factory=list)
    physics_material: str = "Default"
    generate_from_mesh: bool = False
    simplification_ratio: float = 1.0

    @property
    def shape_count(self) -> int:
        return len(self.shapes)

    @property
    def has_shapes(self) -> bool:
        return len(self.shapes) > 0


@dataclass
class CollisionBuildResult:
    """Result of a collision mesh build job."""

    job_id: str
    entry_id: str
    shapes_generated: int = 0
    errors: list = field(default_factory=list)
    elapsed_ms: float = 0.0

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def success(self) -> bool:
        return not self.has_errors


class CollisionMeshPipeline:
    """Pipeline for generating and validating collision meshes."""

    def __init__(self) -> None:
        self._entries: Dict[str, CollisionMeshEntry] = {}
        self._job_counter: int = 0

    def add_entry(self, entry: CollisionMeshEntry) -> None:
        """Register a collision mesh entry."""
        self._entries[entry.entry_id] = entry

    def remove_entry(self, entry_id: str) -> bool:
        """Remove a collision mesh entry by ID."""
        if entry_id in self._entries:
            del self._entries[entry_id]
            return True
        return False

    def get_entry(self, entry_id: str) -> Optional[CollisionMeshEntry]:
        """Retrieve a collision mesh entry by ID."""
        return self._entries.get(entry_id)

    def get_all_entries(self) -> List[CollisionMeshEntry]:
        """Return all registered collision mesh entries."""
        return list(self._entries.values())

    def add_shape(self, entry_id: str, shape: CollisionShapeDef) -> bool:
        """Add a collision shape to an existing entry."""
        entry = self._entries.get(entry_id)
        if entry is None:
            return False
        entry.shapes.append(shape)
        return True

    def build(self, entry_id: str) -> CollisionBuildResult:
        """Build collision shapes for a single entry."""
        self._job_counter += 1
        job_id = f"job_{self._job_counter:04d}"
        entry = self._entries.get(entry_id)
        if entry is None:
            return CollisionBuildResult(
                job_id=job_id,
                entry_id=entry_id,
                errors=[f"Entry '{entry_id}' not found"],
            )
        start = time.perf_counter()
        shapes_generated = len(entry.shapes)
        elapsed = (time.perf_counter() - start) * 1000.0
        logger.debug("Built collision for entry %s: %d shapes", entry_id, shapes_generated)
        return CollisionBuildResult(
            job_id=job_id,
            entry_id=entry_id,
            shapes_generated=shapes_generated,
            elapsed_ms=elapsed,
        )

    def build_all(self) -> List[CollisionBuildResult]:
        """Build collision shapes for all registered entries."""
        return [self.build(eid) for eid in list(self._entries)]

    def validate(self, entry: CollisionMeshEntry) -> bool:
        """Validate that a collision mesh entry is well-formed."""
        return bool(entry.entry_id) and bool(entry.mesh_path)

    def clear(self) -> None:
        """Clear all registered entries."""
        self._entries.clear()

    @property
    def entry_count(self) -> int:
        return len(self._entries)

    @property
    def is_empty(self) -> bool:
        return len(self._entries) == 0
