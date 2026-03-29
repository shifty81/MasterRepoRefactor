"""AtlasAI Phase 29B — Particle system pipeline for emitter and module compilation."""
from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ParticleModuleDef:
    """Definition for a single particle module."""

    module_id: str
    module_type: str = "Spawn"  # Spawn, Color, Force, Velocity, Noise, Collision, Renderer
    enabled: bool = True
    priority: int = 0

    @property
    def is_active(self) -> bool:
        return self.enabled and self.module_type != ""


@dataclass
class ParticleEmitterDef:
    """Definition for a particle emitter."""

    emitter_id: str
    name: str
    shape: str = "Point"
    spawn_rate: float = 10.0
    lifetime: float = 2.0
    modules: List[ParticleModuleDef] = field(default_factory=list)
    loop: bool = True
    warmup: float = 0.0

    @property
    def is_looping(self) -> bool:
        return self.loop

    @property
    def has_modules(self) -> bool:
        return len(self.modules) > 0

    @property
    def active_module_count(self) -> int:
        return sum(1 for m in self.modules if m.is_active)


@dataclass
class ParticlePipelineResult:
    """Result of a particle pipeline compilation."""

    job_id: str
    success: bool = True
    emitter_count: int = 0
    module_count: int = 0
    errors: List[str] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def total_processed(self) -> int:
        return self.emitter_count + self.module_count


class ParticleSystemPipeline:
    """Pipeline for managing and compiling particle system emitters."""

    def __init__(self) -> None:
        self._emitters: dict[str, ParticleEmitterDef] = {}

    def add_emitter(self, emitter: ParticleEmitterDef) -> None:
        """Add an emitter to the pipeline."""
        self._emitters[emitter.emitter_id] = emitter
        logger.debug("Added emitter %s", emitter.emitter_id)

    def remove_emitter(self, emitter_id: str) -> bool:
        """Remove an emitter by ID. Returns True if removed."""
        if emitter_id in self._emitters:
            del self._emitters[emitter_id]
            return True
        return False

    def compile(self) -> ParticlePipelineResult:
        """Compile all emitters into a pipeline result."""
        errors: List[str] = []
        module_count = 0
        for emitter in self._emitters.values():
            if not self.validate_emitter(emitter):
                errors.append(f"Invalid emitter: {emitter.emitter_id}")
            module_count += len(emitter.modules)
        return ParticlePipelineResult(
            job_id=str(uuid.uuid4()),
            success=len(errors) == 0,
            emitter_count=len(self._emitters),
            module_count=module_count,
            errors=errors,
        )

    def get_emitter(self, emitter_id: str) -> Optional[ParticleEmitterDef]:
        """Retrieve an emitter by ID."""
        return self._emitters.get(emitter_id)

    def get_all_emitters(self) -> List[ParticleEmitterDef]:
        """Return all registered emitters."""
        return list(self._emitters.values())

    def validate_emitter(self, emitter: ParticleEmitterDef) -> bool:
        """Validate emitter has required fields."""
        return bool(emitter.emitter_id) and bool(emitter.name) and emitter.spawn_rate > 0

    def clear(self) -> None:
        """Clear all emitters."""
        self._emitters.clear()

    @property
    def emitter_count(self) -> int:
        return len(self._emitters)

    @property
    def is_empty(self) -> bool:
        return len(self._emitters) == 0
