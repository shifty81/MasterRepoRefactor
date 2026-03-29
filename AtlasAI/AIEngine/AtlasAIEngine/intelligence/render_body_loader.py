"""AtlasAI Phase 30D — Render Body Loader.

Discovers and manages render body manifests, mirroring the C++
RenderBodyRegistry for cross-language rendering scene setup.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class MaterialSlotDef:
    """Definition for a single material slot on a render body."""

    slot_index: int = 0
    material_path: str = ""
    param_overrides: dict = field(default_factory=dict)

    @property
    def has_material(self) -> bool:
        return bool(self.material_path)

    @property
    def override_count(self) -> int:
        return len(self.param_overrides)


@dataclass
class LODEntryDef:
    """LOD entry definition for a render body."""

    lod_level: int = 0
    mesh_path: str = ""
    screen_size_threshold: float = 1.0

    @property
    def is_highest_lod(self) -> bool:
        return self.lod_level == 0


@dataclass
class RenderBodyManifest:
    """Parsed render body manifest for a single mesh body in a scene."""

    body_id: str
    name: str
    mesh_path: str = ""
    primitive: str = "Triangle"         # Triangle, Line, Point, Patch, Billboard, InstancedMesh
    render_layer: str = "World"         # Background, World, Characters, VFX, UI, Debug, Overlay
    shading_model: str = "Lit"          # Lit, Unlit, Toon, Subsurface, ClearCoat, Custom
    cull_mode: str = "Back"             # None, Front, Back, Both
    material_slots: List[MaterialSlotDef] = field(default_factory=list)
    lod_entries: List[LODEntryDef] = field(default_factory=list)
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    visible: bool = True
    enabled: bool = True
    cast_shadow: bool = True
    receive_shadow: bool = True
    body_state: str = "Inactive"

    @property
    def is_visible(self) -> bool:
        return self.visible and self.enabled

    @property
    def has_lods(self) -> bool:
        return len(self.lod_entries) > 0

    @property
    def lod_count(self) -> int:
        return len(self.lod_entries)

    @property
    def material_count(self) -> int:
        return len(self.material_slots)


class RenderBodyLoader:
    """Loader for render body manifests from dict or file."""

    def __init__(self) -> None:
        self._loaded: List[RenderBodyManifest] = []

    def load_manifest(self, data: dict) -> RenderBodyManifest:
        """Parse a dict into a RenderBodyManifest."""
        material_slots = [
            MaterialSlotDef(
                slot_index=int(s.get("slot_index", 0)),
                material_path=s.get("material_path", ""),
                param_overrides=dict(s.get("param_overrides", {})),
            )
            for s in data.get("material_slots", [])
        ]
        lod_entries = [
            LODEntryDef(
                lod_level=int(l.get("lod_level", 0)),
                mesh_path=l.get("mesh_path", ""),
                screen_size_threshold=float(l.get("screen_size_threshold", 1.0)),
            )
            for l in data.get("lod_entries", [])
        ]
        manifest = RenderBodyManifest(
            body_id=data["body_id"],
            name=data["name"],
            mesh_path=data.get("mesh_path", ""),
            primitive=data.get("primitive", "Triangle"),
            render_layer=data.get("render_layer", "World"),
            shading_model=data.get("shading_model", "Lit"),
            cull_mode=data.get("cull_mode", "Back"),
            material_slots=material_slots,
            lod_entries=lod_entries,
            pos_x=float(data.get("pos_x", 0.0)),
            pos_y=float(data.get("pos_y", 0.0)),
            pos_z=float(data.get("pos_z", 0.0)),
            visible=bool(data.get("visible", True)),
            enabled=bool(data.get("enabled", True)),
            cast_shadow=bool(data.get("cast_shadow", True)),
            receive_shadow=bool(data.get("receive_shadow", True)),
            body_state=data.get("body_state", "Inactive"),
        )
        self._loaded.append(manifest)
        return manifest

    def load_from_file(self, path) -> RenderBodyManifest:
        """Load a manifest from a JSON file."""
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def load_batch(self, data_list: list) -> List[RenderBodyManifest]:
        """Load multiple manifests from a list of dicts."""
        return [self.load_manifest(d) for d in data_list]

    def save_manifest(self, manifest: RenderBodyManifest, path) -> None:
        """Serialize and save a manifest to a JSON file."""
        p = Path(path)
        data = {
            "body_id": manifest.body_id,
            "name": manifest.name,
            "mesh_path": manifest.mesh_path,
            "primitive": manifest.primitive,
            "render_layer": manifest.render_layer,
            "shading_model": manifest.shading_model,
            "cull_mode": manifest.cull_mode,
            "pos_x": manifest.pos_x,
            "pos_y": manifest.pos_y,
            "pos_z": manifest.pos_z,
            "visible": manifest.visible,
            "enabled": manifest.enabled,
            "cast_shadow": manifest.cast_shadow,
            "receive_shadow": manifest.receive_shadow,
            "body_state": manifest.body_state,
            "material_slots": [
                {
                    "slot_index": s.slot_index,
                    "material_path": s.material_path,
                    "param_overrides": s.param_overrides,
                }
                for s in manifest.material_slots
            ],
            "lod_entries": [
                {
                    "lod_level": l.lod_level,
                    "mesh_path": l.mesh_path,
                    "screen_size_threshold": l.screen_size_threshold,
                }
                for l in manifest.lod_entries
            ],
        }
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: RenderBodyManifest) -> bool:
        """Validate a manifest has required fields."""
        return bool(manifest.body_id) and bool(manifest.name)

    def clear(self) -> None:
        """Clear all loaded manifests."""
        self._loaded.clear()

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)
