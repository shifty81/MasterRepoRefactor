"""AtlasAI Phase 26D — Physics Body Loader.

Discovers and manages physics body manifests, mirroring the C++
PhysicsBodyRegistry for cross-language physics scene setup coordination.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class PhysicsMaterialDef:
    """Physics surface material properties."""

    material_id: str
    name: str
    static_friction: float = 0.6
    dynamic_friction: float = 0.4
    restitution: float = 0.1
    density: float = 1000.0
    is_trigger: bool = False

    @property
    def friction_ratio(self) -> float:
        """dynamic / static friction ratio — values < 1.0 are physically realistic."""
        if self.static_friction == 0.0:
            return 0.0
        return self.dynamic_friction / self.static_friction


@dataclass
class ColliderDef:
    """Defines a single collider shape within a physics body."""

    collider_id: str
    shape: str = "Box"
    extent_x: float = 0.5
    extent_y: float = 0.5
    extent_z: float = 0.5
    radius: float = 0.5
    height: float = 2.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    offset_z: float = 0.0
    physics_material_id: str = ""
    is_trigger: bool = False
    enabled: bool = True

    @property
    def offset(self) -> tuple[float, float, float]:
        return (self.offset_x, self.offset_y, self.offset_z)


@dataclass
class PhysicsBodyManifest:
    """Parsed physics body manifest for a single rigidbody."""

    body_id: str
    name: str
    body_type: str = "Dynamic"
    body_state: str = "Inactive"
    physics_layer: str = "Default"
    mass: float = 1.0
    linear_drag: float = 0.0
    angular_drag: float = 0.05
    gravity_scale: float = 1.0
    use_gravity: bool = True
    freeze_pos_x: bool = False
    freeze_pos_y: bool = False
    freeze_pos_z: bool = False
    freeze_rot_x: bool = False
    freeze_rot_y: bool = False
    freeze_rot_z: bool = False
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    colliders: list[ColliderDef] = field(default_factory=list)
    linked_entity_id: str = ""
    scene_id: str = ""
    manifest_path: str = ""
    priority: int = 0
    always_active: bool = False

    @property
    def collider_count(self) -> int:
        return len(self.colliders)

    @property
    def position(self) -> tuple[float, float, float]:
        return (self.pos_x, self.pos_y, self.pos_z)

    @property
    def is_dynamic(self) -> bool:
        return self.body_type == "Dynamic"

    @property
    def is_active(self) -> bool:
        return self.body_state == "Active"

    def get_collider(self, collider_id: str) -> Optional[ColliderDef]:
        for c in self.colliders:
            if c.collider_id == collider_id:
                return c
        return None


class PhysicsBodyLoader:
    """Discovers and manages physics body manifests for scene setup."""

    def __init__(self) -> None:
        self._bodies: dict[str, PhysicsBodyManifest] = {}
        self._materials: dict[str, PhysicsMaterialDef] = {}
        self._active: set[str] = set()
        self._next_body: int = 0
        self._next_collider: int = 0
        self._next_material: int = 0

    # ------------------------------------------------------------------
    # Body registration
    # ------------------------------------------------------------------

    def register(
        self,
        body_id: str,
        name: str,
        body_type: str = "Dynamic",
        scene_id: str = "",
        mass: float = 1.0,
        always_active: bool = False,
        priority: int = 0,
    ) -> PhysicsBodyManifest:
        manifest = PhysicsBodyManifest(
            body_id=body_id,
            name=name,
            body_type=body_type,
            scene_id=scene_id,
            mass=mass,
            always_active=always_active,
            priority=priority,
        )
        self._bodies[body_id] = manifest
        logger.debug("Registered physics body %s", body_id)
        return manifest

    def register_from_dict(self, data: dict) -> Optional[PhysicsBodyManifest]:
        try:
            body_id = data["body_id"]
            name = data["name"]
            manifest = self.register(
                body_id=body_id,
                name=name,
                body_type=data.get("body_type", "Dynamic"),
                scene_id=data.get("scene_id", ""),
                mass=data.get("mass", 1.0),
                always_active=data.get("always_active", False),
                priority=data.get("priority", 0),
            )
            manifest.physics_layer = data.get("physics_layer", "Default")
            manifest.linear_drag = data.get("linear_drag", 0.0)
            manifest.angular_drag = data.get("angular_drag", 0.05)
            manifest.gravity_scale = data.get("gravity_scale", 1.0)
            manifest.use_gravity = data.get("use_gravity", True)
            manifest.linked_entity_id = data.get("linked_entity_id", "")
            manifest.pos_x = data.get("pos_x", 0.0)
            manifest.pos_y = data.get("pos_y", 0.0)
            manifest.pos_z = data.get("pos_z", 0.0)
            for cd in data.get("colliders", []):
                collider = ColliderDef(
                    collider_id=cd.get("collider_id", f"col_{self._next_collider:04d}"),
                    shape=cd.get("shape", "Box"),
                    extent_x=cd.get("extent_x", 0.5),
                    extent_y=cd.get("extent_y", 0.5),
                    extent_z=cd.get("extent_z", 0.5),
                    is_trigger=cd.get("is_trigger", False),
                )
                self._next_collider += 1
                manifest.colliders.append(collider)
            return manifest
        except (KeyError, TypeError) as exc:
            logger.error("register_from_dict failed: %s", exc)
            return None

    def unregister(self, body_id: str) -> bool:
        if body_id not in self._bodies:
            return False
        del self._bodies[body_id]
        self._active.discard(body_id)
        return True

    def get_manifest(self, body_id: str) -> Optional[PhysicsBodyManifest]:
        return self._bodies.get(body_id)

    def get_registered_count(self) -> int:
        return len(self._bodies)

    def get_all_body_ids(self) -> list[str]:
        return list(self._bodies.keys())

    def get_bodies_by_scene(self, scene_id: str) -> list[str]:
        return [
            bid for bid, m in self._bodies.items()
            if m.scene_id == scene_id
        ]

    def get_bodies_by_type(self, body_type: str) -> list[str]:
        return [
            bid for bid, m in self._bodies.items()
            if m.body_type == body_type
        ]

    # ------------------------------------------------------------------
    # Activation
    # ------------------------------------------------------------------

    def activate(self, body_id: str) -> bool:
        if body_id not in self._bodies:
            logger.warning("Cannot activate unknown body %s", body_id)
            return False
        self._active.add(body_id)
        m = self._bodies[body_id]
        m.body_state = "Active"
        return True

    def deactivate(self, body_id: str) -> bool:
        if body_id not in self._active:
            return False
        self._active.discard(body_id)
        m = self._bodies.get(body_id)
        if m:
            m.body_state = "Inactive"
        return True

    def is_active(self, body_id: str) -> bool:
        return body_id in self._active

    def get_active_count(self) -> int:
        return len(self._active)

    def get_active_ids(self) -> list[str]:
        return list(self._active)

    def activate_all_in_scene(self, scene_id: str) -> int:
        activated = 0
        for body_id, m in self._bodies.items():
            if m.scene_id == scene_id and body_id not in self._active:
                self.activate(body_id)
                activated += 1
        return activated

    def deactivate_all_in_scene(self, scene_id: str) -> int:
        deactivated = 0
        ids = self.get_bodies_by_scene(scene_id)
        for body_id in ids:
            if self.deactivate(body_id):
                deactivated += 1
        return deactivated

    def activate_always_active(self) -> int:
        activated = 0
        for body_id, m in self._bodies.items():
            if m.always_active and body_id not in self._active:
                self.activate(body_id)
                activated += 1
        return activated

    # ------------------------------------------------------------------
    # Collider management
    # ------------------------------------------------------------------

    def add_collider(
        self,
        body_id: str,
        shape: str = "Box",
        extent_x: float = 0.5,
        extent_y: float = 0.5,
        extent_z: float = 0.5,
        is_trigger: bool = False,
        material_id: str = "",
    ) -> Optional[ColliderDef]:
        manifest = self._bodies.get(body_id)
        if manifest is None:
            return None
        collider_id = f"col_{self._next_collider:04d}"
        self._next_collider += 1
        collider = ColliderDef(
            collider_id=collider_id,
            shape=shape,
            extent_x=extent_x,
            extent_y=extent_y,
            extent_z=extent_z,
            is_trigger=is_trigger,
            physics_material_id=material_id,
        )
        manifest.colliders.append(collider)
        return collider

    def remove_collider(self, body_id: str, collider_id: str) -> bool:
        manifest = self._bodies.get(body_id)
        if manifest is None:
            return False
        before = len(manifest.colliders)
        manifest.colliders = [c for c in manifest.colliders if c.collider_id != collider_id]
        return len(manifest.colliders) < before

    def get_collider_count(self, body_id: str) -> int:
        manifest = self._bodies.get(body_id)
        return manifest.collider_count if manifest else 0

    # ------------------------------------------------------------------
    # Physics materials
    # ------------------------------------------------------------------

    def register_material(
        self,
        name: str,
        static_friction: float = 0.6,
        dynamic_friction: float = 0.4,
        restitution: float = 0.1,
        density: float = 1000.0,
    ) -> PhysicsMaterialDef:
        material_id = f"mat_{self._next_material:04d}"
        self._next_material += 1
        mat = PhysicsMaterialDef(
            material_id=material_id,
            name=name,
            static_friction=static_friction,
            dynamic_friction=dynamic_friction,
            restitution=restitution,
            density=density,
        )
        self._materials[material_id] = mat
        return mat

    def unregister_material(self, material_id: str) -> bool:
        if material_id not in self._materials:
            return False
        del self._materials[material_id]
        return True

    def get_material(self, material_id: str) -> Optional[PhysicsMaterialDef]:
        return self._materials.get(material_id)

    def get_material_count(self) -> int:
        return len(self._materials)

    def get_all_material_ids(self) -> list[str]:
        return list(self._materials.keys())

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_registry(self, output_path: str) -> bool:
        data = {
            "bodies": [
                {
                    "body_id": m.body_id,
                    "name": m.name,
                    "body_type": m.body_type,
                    "scene_id": m.scene_id,
                    "mass": m.mass,
                    "always_active": m.always_active,
                    "priority": m.priority,
                    "physics_layer": m.physics_layer,
                    "collider_count": m.collider_count,
                    "colliders": [
                        {
                            "collider_id": c.collider_id,
                            "shape": c.shape,
                            "is_trigger": c.is_trigger,
                        }
                        for c in m.colliders
                    ],
                }
                for m in self._bodies.values()
            ],
            "materials": [
                {
                    "material_id": mat.material_id,
                    "name": mat.name,
                    "static_friction": mat.static_friction,
                    "dynamic_friction": mat.dynamic_friction,
                    "restitution": mat.restitution,
                }
                for mat in self._materials.values()
            ],
        }
        try:
            Path(output_path).write_text(json.dumps(data, indent=2))
            return True
        except OSError as exc:
            logger.error("Failed to save physics registry: %s", exc)
            return False

    def load_registry(self, input_path: str) -> int:
        try:
            data = json.loads(Path(input_path).read_text())
            loaded = 0
            for entry in data.get("bodies", []):
                if self.register_from_dict(entry) is not None:
                    loaded += 1
            for mat_data in data.get("materials", []):
                try:
                    mat = PhysicsMaterialDef(
                        material_id=mat_data["material_id"],
                        name=mat_data["name"],
                        static_friction=mat_data.get("static_friction", 0.6),
                        dynamic_friction=mat_data.get("dynamic_friction", 0.4),
                        restitution=mat_data.get("restitution", 0.1),
                    )
                    self._materials[mat.material_id] = mat
                except (KeyError, TypeError):
                    pass
            return loaded
        except (OSError, json.JSONDecodeError) as exc:
            logger.error("Failed to load physics registry: %s", exc)
            return 0

    def clear(self) -> None:
        self._bodies.clear()
        self._materials.clear()
        self._active.clear()
        self._next_body = 0
        self._next_collider = 0
        self._next_material = 0
