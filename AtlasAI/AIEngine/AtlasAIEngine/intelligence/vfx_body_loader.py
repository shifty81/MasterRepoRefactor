"""AtlasAI Phase 28D — VFX Body Loader.

Discovers and manages VFX emitter body manifests, mirroring the C++
VFXBodyRegistry for cross-language visual effects scene setup.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class EmitterBoundsDef:
    """Bounding volume for a VFX emitter body."""

    shape: str = "Sphere"    # Sphere, Box, Cone, Mesh
    extent_x: float = 1.0
    extent_y: float = 1.0
    extent_z: float = 1.0
    radius: float = 1.0
    use_mesh_bounds: bool = False

    @property
    def volume(self) -> float:
        if self.shape == "Sphere":
            import math
            return (4.0 / 3.0) * math.pi * self.radius ** 3
        return self.extent_x * self.extent_y * self.extent_z

    @property
    def is_bounded(self) -> bool:
        return self.radius > 0.0 or (self.extent_x > 0.0 and self.extent_y > 0.0)


@dataclass
class SimulationSettingsDef:
    """Runtime simulation settings for a VFX emitter."""

    simulation_space: str = "World"    # World, Local, Custom
    max_particles: int = 1000
    fixed_time_step: bool = False
    time_step: float = 0.016
    gravity_scale: float = 1.0
    collision_enabled: bool = False
    use_gpu_simulation: bool = False

    @property
    def is_gpu_simulated(self) -> bool:
        return self.use_gpu_simulation

    @property
    def effective_time_step(self) -> float:
        return self.time_step if self.fixed_time_step else 0.0


@dataclass
class VFXBodyManifest:
    """Parsed VFX body manifest for a single emitter in a scene."""

    body_id: str
    name: str
    emitter_type: str = "Point"         # Point, Sphere, Box, Cone, Mesh, Trail
    body_state: str = "Inactive"        # Inactive, Active, Playing, Paused, Stopped
    vfx_layer: str = "World"            # World, UI, Overlay, Debug
    blend_mode: str = "Additive"        # Additive, AlphaBlend, Multiply, Screen
    bounds: EmitterBoundsDef = field(default_factory=EmitterBoundsDef)
    simulation: SimulationSettingsDef = field(default_factory=SimulationSettingsDef)
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    spawn_rate: float = 10.0
    lifetime: float = 2.0
    start_speed: float = 1.0
    start_size: float = 0.1
    loop: bool = False
    play_on_activate: bool = False
    prewarm: bool = False
    effect_asset_id: str = ""
    linked_entity_id: str = ""
    scene_id: str = ""
    priority: int = 0
    lod_level: int = 0
    always_play: bool = False
    manifest_path: str = ""

    @property
    def position(self) -> tuple[float, float, float]:
        return (self.pos_x, self.pos_y, self.pos_z)

    @property
    def is_active(self) -> bool:
        return self.body_state in ("Active", "Playing")

    @property
    def is_playing(self) -> bool:
        return self.body_state == "Playing"

    @property
    def is_looping(self) -> bool:
        return self.loop


class VFXBodyLoader:
    """Discovers and manages VFX emitter body manifests for scene setup."""

    def __init__(self) -> None:
        self._bodies: dict[str, VFXBodyManifest] = {}
        self._active: set[str] = set()
        self._playing: set[str] = set()
        self._next_body: int = 0

    # ------------------------------------------------------------------
    # Manifest registration
    # ------------------------------------------------------------------

    def load_manifest(
        self,
        body_id: str,
        name: str,
        emitter_type: str = "Point",
        scene_id: str = "",
        vfx_layer: str = "World",
        priority: int = 0,
        always_play: bool = False,
    ) -> VFXBodyManifest:
        manifest = VFXBodyManifest(
            body_id=body_id,
            name=name,
            emitter_type=emitter_type,
            scene_id=scene_id,
            vfx_layer=vfx_layer,
            priority=priority,
            always_play=always_play,
        )
        self._bodies[body_id] = manifest
        logger.debug("Loaded VFX body manifest %s: %s", body_id, name)
        return manifest

    def load_manifest_from_dict(self, data: dict) -> Optional[VFXBodyManifest]:
        try:
            body_id = data["body_id"]
            name = data["name"]
            manifest = self.load_manifest(
                body_id=body_id,
                name=name,
                emitter_type=data.get("emitter_type", "Point"),
                scene_id=data.get("scene_id", ""),
                vfx_layer=data.get("vfx_layer", "World"),
                priority=data.get("priority", 0),
                always_play=data.get("always_play", False),
            )
            manifest.spawn_rate = data.get("spawn_rate", 10.0)
            manifest.lifetime = data.get("lifetime", 2.0)
            manifest.loop = data.get("loop", False)
            manifest.play_on_activate = data.get("play_on_activate", False)
            manifest.effect_asset_id = data.get("effect_asset_id", "")
            manifest.linked_entity_id = data.get("linked_entity_id", "")
            manifest.pos_x = data.get("pos_x", 0.0)
            manifest.pos_y = data.get("pos_y", 0.0)
            manifest.pos_z = data.get("pos_z", 0.0)
            bounds_data = data.get("bounds", {})
            if bounds_data:
                manifest.bounds = EmitterBoundsDef(
                    shape=bounds_data.get("shape", "Sphere"),
                    extent_x=bounds_data.get("extent_x", 1.0),
                    extent_y=bounds_data.get("extent_y", 1.0),
                    extent_z=bounds_data.get("extent_z", 1.0),
                    radius=bounds_data.get("radius", 1.0),
                )
            sim_data = data.get("simulation", {})
            if sim_data:
                manifest.simulation = SimulationSettingsDef(
                    simulation_space=sim_data.get("simulation_space", "World"),
                    max_particles=sim_data.get("max_particles", 1000),
                    gravity_scale=sim_data.get("gravity_scale", 1.0),
                    use_gpu_simulation=sim_data.get("use_gpu_simulation", False),
                )
            return manifest
        except (KeyError, TypeError) as exc:
            logger.error("load_manifest_from_dict failed: %s", exc)
            return None

    def save_manifest(self, body_id: str, output_path: str) -> bool:
        manifest = self._bodies.get(body_id)
        if manifest is None:
            return False
        data = {
            "body_id": manifest.body_id,
            "name": manifest.name,
            "emitter_type": manifest.emitter_type,
            "body_state": manifest.body_state,
            "vfx_layer": manifest.vfx_layer,
            "scene_id": manifest.scene_id,
            "pos_x": manifest.pos_x,
            "pos_y": manifest.pos_y,
            "pos_z": manifest.pos_z,
            "spawn_rate": manifest.spawn_rate,
            "lifetime": manifest.lifetime,
            "loop": manifest.loop,
            "effect_asset_id": manifest.effect_asset_id,
            "bounds": {
                "shape": manifest.bounds.shape,
                "radius": manifest.bounds.radius,
            },
        }
        try:
            manifest.manifest_path = output_path
            Path(output_path).write_text(json.dumps(data, indent=2))
            return True
        except OSError as exc:
            logger.error("Failed to save VFX manifest %s: %s", body_id, exc)
            return False

    def remove_manifest(self, body_id: str) -> bool:
        if body_id not in self._bodies:
            return False
        del self._bodies[body_id]
        self._active.discard(body_id)
        self._playing.discard(body_id)
        return True

    def get_manifest(self, body_id: str) -> Optional[VFXBodyManifest]:
        return self._bodies.get(body_id)

    def list_manifests(self) -> list[str]:
        return list(self._bodies.keys())

    def count(self) -> int:
        return len(self._bodies)

    # ------------------------------------------------------------------
    # Activation
    # ------------------------------------------------------------------

    def activate(self, body_id: str) -> bool:
        if body_id not in self._bodies:
            return False
        self._active.add(body_id)
        self._bodies[body_id].body_state = "Active"
        return True

    def deactivate(self, body_id: str) -> bool:
        if body_id not in self._active:
            return False
        self._active.discard(body_id)
        self._playing.discard(body_id)
        m = self._bodies.get(body_id)
        if m:
            m.body_state = "Inactive"
        return True

    def play(self, body_id: str) -> bool:
        if body_id not in self._bodies:
            return False
        self.activate(body_id)
        self._playing.add(body_id)
        self._bodies[body_id].body_state = "Playing"
        return True

    def stop(self, body_id: str) -> bool:
        if body_id not in self._active and body_id not in self._playing:
            return False
        self._playing.discard(body_id)
        m = self._bodies.get(body_id)
        if m:
            m.body_state = "Stopped"
        return True

    def is_active(self, body_id: str) -> bool:
        return body_id in self._active

    def is_playing(self, body_id: str) -> bool:
        return body_id in self._playing

    def get_bodies_by_scene(self, scene_id: str) -> list[str]:
        return [bid for bid, m in self._bodies.items() if m.scene_id == scene_id]

    def get_bodies_by_layer(self, vfx_layer: str) -> list[str]:
        return [bid for bid, m in self._bodies.items() if m.vfx_layer == vfx_layer]

    def get_bodies_by_type(self, emitter_type: str) -> list[str]:
        return [bid for bid, m in self._bodies.items() if m.emitter_type == emitter_type]

    def get_active_ids(self) -> list[str]:
        return list(self._active)

    def get_playing_ids(self) -> list[str]:
        return list(self._playing)

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_registry_json(self, output_path: str) -> bool:
        data = {
            "vfx_body_count": self.count(),
            "active_count": len(self._active),
            "playing_count": len(self._playing),
            "bodies": [
                {
                    "body_id": m.body_id,
                    "name": m.name,
                    "emitter_type": m.emitter_type,
                    "body_state": m.body_state,
                    "vfx_layer": m.vfx_layer,
                    "scene_id": m.scene_id,
                    "loop": m.loop,
                    "spawn_rate": m.spawn_rate,
                    "lifetime": m.lifetime,
                    "effect_asset_id": m.effect_asset_id,
                    "bounds_shape": m.bounds.shape,
                    "sim_space": m.simulation.simulation_space,
                }
                for m in self._bodies.values()
            ],
        }
        try:
            Path(output_path).write_text(json.dumps(data, indent=2))
            return True
        except OSError as exc:
            logger.error("Failed to export VFX registry: %s", exc)
            return False

    def clear(self) -> None:
        self._bodies.clear()
        self._active.clear()
        self._playing.clear()
        self._next_body = 0
