"""AtlasAI Phase 29D — Animation body loader for manifest parsing and validation."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class AnimationClipDef:
    """Definition for a single animation clip."""

    clip_id: str
    name: str
    clip_type: str = "Skeletal"
    duration: float = 1.0
    loop: bool = False
    blend_in: float = 0.1
    blend_out: float = 0.1

    @property
    def is_looping(self) -> bool:
        return self.loop

    @property
    def total_blend_time(self) -> float:
        return self.blend_in + self.blend_out


@dataclass
class AnimationBlendWeightDef:
    """Definition for animation blend weights on a layer."""

    layer: str
    weight: float = 1.0
    mask_bones: List[str] = field(default_factory=list)

    @property
    def is_additive(self) -> bool:
        return self.layer.lower() == "additive"

    @property
    def bone_count(self) -> int:
        return len(self.mask_bones)


@dataclass
class AnimationBodyManifest:
    """Parsed manifest for a single animation body."""

    body_id: str
    name: str
    clip_type: str = "Skeletal"
    body_state: str = "Inactive"
    animation_layer: str = "Base"
    clips: List[AnimationClipDef] = field(default_factory=list)
    blend_weights: List[AnimationBlendWeightDef] = field(default_factory=list)
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    animation_speed: float = 1.0
    current_time: float = 0.0
    loop: bool = False
    root_motion: bool = False

    @property
    def is_playing(self) -> bool:
        return self.body_state.lower() == "playing"

    @property
    def has_clips(self) -> bool:
        return len(self.clips) > 0

    @property
    def clip_count(self) -> int:
        return len(self.clips)


class AnimationBodyLoader:
    """Loader for animation body manifests from dict or file."""

    def __init__(self) -> None:
        self._loaded: List[AnimationBodyManifest] = []

    def load_manifest(self, data: dict) -> AnimationBodyManifest:
        """Parse a dict into an AnimationBodyManifest."""
        clips = [
            AnimationClipDef(
                clip_id=c.get("clip_id", ""),
                name=c.get("name", ""),
                clip_type=c.get("clip_type", "Skeletal"),
                duration=float(c.get("duration", 1.0)),
                loop=bool(c.get("loop", False)),
                blend_in=float(c.get("blend_in", 0.1)),
                blend_out=float(c.get("blend_out", 0.1)),
            )
            for c in data.get("clips", [])
        ]
        blend_weights = [
            AnimationBlendWeightDef(
                layer=bw.get("layer", "Base"),
                weight=float(bw.get("weight", 1.0)),
                mask_bones=list(bw.get("mask_bones", [])),
            )
            for bw in data.get("blend_weights", [])
        ]
        manifest = AnimationBodyManifest(
            body_id=data["body_id"],
            name=data["name"],
            clip_type=data.get("clip_type", "Skeletal"),
            body_state=data.get("body_state", "Inactive"),
            animation_layer=data.get("animation_layer", "Base"),
            clips=clips,
            blend_weights=blend_weights,
            pos_x=float(data.get("pos_x", 0.0)),
            pos_y=float(data.get("pos_y", 0.0)),
            pos_z=float(data.get("pos_z", 0.0)),
            animation_speed=float(data.get("animation_speed", 1.0)),
            current_time=float(data.get("current_time", 0.0)),
            loop=bool(data.get("loop", False)),
            root_motion=bool(data.get("root_motion", False)),
        )
        self._loaded.append(manifest)
        return manifest

    def load_from_file(self, path) -> AnimationBodyManifest:
        """Load manifest from a JSON file."""
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def load_batch(self, data_list: list) -> List[AnimationBodyManifest]:
        """Load multiple manifests from a list of dicts."""
        return [self.load_manifest(d) for d in data_list]

    def save_manifest(self, manifest: AnimationBodyManifest, path) -> None:
        """Serialize and save a manifest to a JSON file."""
        p = Path(path)
        data = {
            "body_id": manifest.body_id,
            "name": manifest.name,
            "clip_type": manifest.clip_type,
            "body_state": manifest.body_state,
            "animation_layer": manifest.animation_layer,
            "pos_x": manifest.pos_x,
            "pos_y": manifest.pos_y,
            "pos_z": manifest.pos_z,
            "animation_speed": manifest.animation_speed,
            "current_time": manifest.current_time,
            "loop": manifest.loop,
            "root_motion": manifest.root_motion,
            "clips": [
                {
                    "clip_id": c.clip_id,
                    "name": c.name,
                    "clip_type": c.clip_type,
                    "duration": c.duration,
                    "loop": c.loop,
                    "blend_in": c.blend_in,
                    "blend_out": c.blend_out,
                }
                for c in manifest.clips
            ],
            "blend_weights": [
                {
                    "layer": bw.layer,
                    "weight": bw.weight,
                    "mask_bones": bw.mask_bones,
                }
                for bw in manifest.blend_weights
            ],
        }
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: AnimationBodyManifest) -> bool:
        """Validate a manifest has required fields."""
        return bool(manifest.body_id) and bool(manifest.name)

    def clear(self) -> None:
        """Clear all loaded manifests."""
        self._loaded.clear()

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)
