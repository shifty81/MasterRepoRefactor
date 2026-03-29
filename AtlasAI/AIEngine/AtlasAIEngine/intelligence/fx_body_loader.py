"""AtlasAI Phase 32D — FX Body Loader.

Discovers and manages VFX body manifests, mirroring the C++
FXBodyRegistry for cross-language particle and visual effects setup.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class FXEmitSettingsDef:
    """Emission configuration for a VFX body manifest."""

    spawn_rate: float = 100.0
    burst_count: int = 0
    lifetime: float = 2.0
    start_size: float = 10.0
    end_size: float = 0.0
    start_speed: float = 100.0
    end_speed: float = 50.0
    inherit_velocity: float = 0.0

    @property
    def has_burst(self) -> bool:
        return self.burst_count > 0

    @property
    def is_fading(self) -> bool:
        return self.end_size < self.start_size


@dataclass
class FXSimSettingsDef:
    """Simulation configuration for a VFX body manifest."""

    target: str = "GPU"     # CPU/GPU/GPUCompute/Hybrid
    max_particles: int = 1000
    local_space: bool = False
    seed: int = 0
    warmup_time: float = 0.0
    fixed_timestep: float = 0.0

    @property
    def is_gpu(self) -> bool:
        return self.target in ["GPU", "GPUCompute", "Hybrid"]

    @property
    def has_warmup(self) -> bool:
        return self.warmup_time > 0.0


@dataclass
class FXBodyManifest:
    """Parsed VFX body manifest for a single effect in a scene."""

    body_id: str
    name: str
    fx_type: str = "Particle"       # Particle/Ribbon/Mesh/Trail/Beam/Volume/Sprite/Decal
    mobility: str = "Movable"       # Static/Stationary/Movable
    range: float = 5000.0
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    enabled: bool = True
    looping: bool = True
    auto_destroy: bool = False
    visible: bool = True
    body_state: str = "Inactive"
    emit_settings: FXEmitSettingsDef = field(default_factory=FXEmitSettingsDef)
    sim_settings: FXSimSettingsDef = field(default_factory=FXSimSettingsDef)

    @property
    def is_visible(self) -> bool:
        return self.visible and self.enabled

    @property
    def is_movable(self) -> bool:
        return self.mobility == "Movable"

    @property
    def is_looping(self) -> bool:
        return self.looping


class FXBodyLoader:
    """Loader for VFX body manifests from dict or file."""

    def __init__(self) -> None:
        self._loaded: List[FXBodyManifest] = []

    def load_manifest(self, data: dict) -> FXBodyManifest:
        """Parse a dict into an FXBodyManifest."""
        emit_data = data.get("emit_settings", {})
        emit = FXEmitSettingsDef(
            spawn_rate=float(emit_data.get("spawn_rate", 100.0)),
            burst_count=int(emit_data.get("burst_count", 0)),
            lifetime=float(emit_data.get("lifetime", 2.0)),
            start_size=float(emit_data.get("start_size", 10.0)),
            end_size=float(emit_data.get("end_size", 0.0)),
            start_speed=float(emit_data.get("start_speed", 100.0)),
            end_speed=float(emit_data.get("end_speed", 50.0)),
            inherit_velocity=float(emit_data.get("inherit_velocity", 0.0)),
        )
        sim_data = data.get("sim_settings", {})
        sim = FXSimSettingsDef(
            target=sim_data.get("target", "GPU"),
            max_particles=int(sim_data.get("max_particles", 1000)),
            local_space=bool(sim_data.get("local_space", False)),
            seed=int(sim_data.get("seed", 0)),
            warmup_time=float(sim_data.get("warmup_time", 0.0)),
            fixed_timestep=float(sim_data.get("fixed_timestep", 0.0)),
        )
        manifest = FXBodyManifest(
            body_id=data["body_id"],
            name=data["name"],
            fx_type=data.get("fx_type", "Particle"),
            mobility=data.get("mobility", "Movable"),
            range=float(data.get("range", 5000.0)),
            pos_x=float(data.get("pos_x", 0.0)),
            pos_y=float(data.get("pos_y", 0.0)),
            pos_z=float(data.get("pos_z", 0.0)),
            enabled=bool(data.get("enabled", True)),
            looping=bool(data.get("looping", True)),
            auto_destroy=bool(data.get("auto_destroy", False)),
            visible=bool(data.get("visible", True)),
            body_state=data.get("body_state", "Inactive"),
            emit_settings=emit,
            sim_settings=sim,
        )
        self._loaded.append(manifest)
        return manifest

    def load_from_file(self, path) -> FXBodyManifest:
        """Load a manifest from a JSON file."""
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def load_batch(self, data_list: list) -> List[FXBodyManifest]:
        """Load multiple manifests from a list of dicts."""
        return [self.load_manifest(d) for d in data_list]

    def save_manifest(self, manifest: FXBodyManifest, path) -> None:
        """Serialize and save a manifest to a JSON file."""
        p = Path(path)
        data = {
            "body_id": manifest.body_id,
            "name": manifest.name,
            "fx_type": manifest.fx_type,
            "mobility": manifest.mobility,
            "range": manifest.range,
            "pos_x": manifest.pos_x,
            "pos_y": manifest.pos_y,
            "pos_z": manifest.pos_z,
            "enabled": manifest.enabled,
            "looping": manifest.looping,
            "auto_destroy": manifest.auto_destroy,
            "visible": manifest.visible,
            "body_state": manifest.body_state,
            "emit_settings": {
                "spawn_rate": manifest.emit_settings.spawn_rate,
                "burst_count": manifest.emit_settings.burst_count,
                "lifetime": manifest.emit_settings.lifetime,
                "start_size": manifest.emit_settings.start_size,
                "end_size": manifest.emit_settings.end_size,
                "start_speed": manifest.emit_settings.start_speed,
                "end_speed": manifest.emit_settings.end_speed,
                "inherit_velocity": manifest.emit_settings.inherit_velocity,
            },
            "sim_settings": {
                "target": manifest.sim_settings.target,
                "max_particles": manifest.sim_settings.max_particles,
                "local_space": manifest.sim_settings.local_space,
                "seed": manifest.sim_settings.seed,
                "warmup_time": manifest.sim_settings.warmup_time,
                "fixed_timestep": manifest.sim_settings.fixed_timestep,
            },
        }
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: FXBodyManifest) -> bool:
        """Validate a manifest has required fields."""
        return bool(manifest.body_id) and bool(manifest.name)

    def clear(self) -> None:
        """Clear all loaded manifests."""
        self._loaded.clear()

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)
