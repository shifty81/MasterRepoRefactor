"""AtlasAI Phase 31D — Light Body Loader.

Discovers and manages light body manifests, mirroring the C++
LightBodyRegistry for cross-language lighting scene setup.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class LightColorDef:
    """Color and temperature definition for a light body."""

    r: float = 1.0
    g: float = 1.0
    b: float = 1.0
    temperature: float = 6500.0
    intensity: float = 1.0
    use_temperature: bool = False

    @property
    def is_warm(self) -> bool:
        return self.temperature < 5000

    @property
    def is_daylight(self) -> bool:
        return 5500 <= self.temperature <= 7000


@dataclass
class ShadowSettingsDef:
    """Shadow configuration for a light body manifest."""

    resolution: str = "Medium"      # Off/Low/Medium/High/Ultra/Cinematic
    bias: float = 0.01
    near_plane: float = 0.1
    contact_shadow: bool = False
    cascades: int = 4
    soft_shadow: bool = True

    @property
    def has_contact_shadow(self) -> bool:
        return self.contact_shadow

    @property
    def is_high_res(self) -> bool:
        return self.resolution in ["High", "Ultra", "Cinematic"]


@dataclass
class LightBodyManifest:
    """Parsed light body manifest for a single light in a scene."""

    body_id: str
    name: str
    light_type: str = "Point"           # Directional/Point/Spot/Area/SkyLight/EmissiveMesh/VolumetricFog/IES
    mobility: str = "Stationary"        # Static/Stationary/Movable
    range: float = 1000.0
    inner_angle: float = 0.0
    outer_angle: float = 45.0
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    enabled: bool = True
    cast_shadow: bool = True
    affects_world: bool = True
    visible: bool = True
    body_state: str = "Inactive"
    color: LightColorDef = field(default_factory=LightColorDef)

    @property
    def is_visible(self) -> bool:
        return self.visible and self.enabled

    @property
    def is_static(self) -> bool:
        return self.mobility == "Static"

    @property
    def is_shadow_caster(self) -> bool:
        return self.cast_shadow


class LightBodyLoader:
    """Loader for light body manifests from dict or file."""

    def __init__(self) -> None:
        self._loaded: List[LightBodyManifest] = []

    def load_manifest(self, data: dict) -> LightBodyManifest:
        """Parse a dict into a LightBodyManifest."""
        color_data = data.get("color", {})
        color = LightColorDef(
            r=float(color_data.get("r", 1.0)),
            g=float(color_data.get("g", 1.0)),
            b=float(color_data.get("b", 1.0)),
            temperature=float(color_data.get("temperature", 6500.0)),
            intensity=float(color_data.get("intensity", 1.0)),
            use_temperature=bool(color_data.get("use_temperature", False)),
        )
        manifest = LightBodyManifest(
            body_id=data["body_id"],
            name=data["name"],
            light_type=data.get("light_type", "Point"),
            mobility=data.get("mobility", "Stationary"),
            range=float(data.get("range", 1000.0)),
            inner_angle=float(data.get("inner_angle", 0.0)),
            outer_angle=float(data.get("outer_angle", 45.0)),
            pos_x=float(data.get("pos_x", 0.0)),
            pos_y=float(data.get("pos_y", 0.0)),
            pos_z=float(data.get("pos_z", 0.0)),
            enabled=bool(data.get("enabled", True)),
            cast_shadow=bool(data.get("cast_shadow", True)),
            affects_world=bool(data.get("affects_world", True)),
            visible=bool(data.get("visible", True)),
            body_state=data.get("body_state", "Inactive"),
            color=color,
        )
        self._loaded.append(manifest)
        return manifest

    def load_from_file(self, path) -> LightBodyManifest:
        """Load a manifest from a JSON file."""
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def load_batch(self, data_list: list) -> List[LightBodyManifest]:
        """Load multiple manifests from a list of dicts."""
        return [self.load_manifest(d) for d in data_list]

    def save_manifest(self, manifest: LightBodyManifest, path) -> None:
        """Serialize and save a manifest to a JSON file."""
        p = Path(path)
        data = {
            "body_id": manifest.body_id,
            "name": manifest.name,
            "light_type": manifest.light_type,
            "mobility": manifest.mobility,
            "range": manifest.range,
            "inner_angle": manifest.inner_angle,
            "outer_angle": manifest.outer_angle,
            "pos_x": manifest.pos_x,
            "pos_y": manifest.pos_y,
            "pos_z": manifest.pos_z,
            "enabled": manifest.enabled,
            "cast_shadow": manifest.cast_shadow,
            "affects_world": manifest.affects_world,
            "visible": manifest.visible,
            "body_state": manifest.body_state,
            "color": {
                "r": manifest.color.r,
                "g": manifest.color.g,
                "b": manifest.color.b,
                "temperature": manifest.color.temperature,
                "intensity": manifest.color.intensity,
                "use_temperature": manifest.color.use_temperature,
            },
        }
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: LightBodyManifest) -> bool:
        """Validate a manifest has required fields."""
        return bool(manifest.body_id) and bool(manifest.name)

    def clear(self) -> None:
        """Clear all loaded manifests."""
        self._loaded.clear()

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)
