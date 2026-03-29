"""AtlasAI Phase 38B — Curve Linear Color Pipeline.

Manages color curve entries, keyframe data, and gradient bake definitions
for the CurveLinearColorTool cross-language pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ColorKeyframeEntry:
    """A single color keyframe in a curve."""
    keyframe_id: str
    curve_id: str
    time: float = 0.0
    r: float = 1.0
    g: float = 1.0
    b: float = 1.0
    a: float = 1.0

    @property
    def is_at_start(self) -> bool:
        return self.time == 0.0

    @property
    def is_opaque(self) -> bool:
        return self.a >= 1.0

    @property
    def is_transparent(self) -> bool:
        return self.a < 1.0


@dataclass
class GradientBakeDef:
    """Definition for a gradient bake result."""
    bake_id: str
    curve_id: str
    resolution: int = 256
    output_path: str = ""
    success: bool = False

    @property
    def is_hd(self) -> bool:
        return self.resolution >= 512

    @property
    def has_output(self) -> bool:
        return bool(self.output_path)

    @property
    def is_complete(self) -> bool:
        return self.success


@dataclass
class ColorCurveEntry:
    """A color curve with keyframes and bake results."""
    curve_id: str
    curve_name: str
    interpolation: str = "Linear"
    channel: str = "All"
    keyframes: list = field(default_factory=list)
    bakes: list = field(default_factory=list)
    enabled: bool = True

    @property
    def is_empty(self) -> bool:
        return not bool(self.keyframes)

    @property
    def has_bakes(self) -> bool:
        return bool(self.bakes)

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def keyframe_count(self) -> int:
        return len(self.keyframes)


class CurveLinearColorPipeline:
    """Pipeline for managing color curve entries, keyframes, and gradient bakes."""

    def __init__(self) -> None:
        self._curves: Dict[str, ColorCurveEntry] = {}

    # Curve CRUD
    def add_curve(self, entry: ColorCurveEntry) -> bool:
        if not entry.curve_id:
            return False
        self._curves[entry.curve_id] = entry
        return True

    def get_curve(self, curve_id: str) -> Optional[ColorCurveEntry]:
        return self._curves.get(curve_id)

    def remove_curve(self, curve_id: str) -> bool:
        if curve_id not in self._curves:
            return False
        del self._curves[curve_id]
        return True

    def get_all_curves(self) -> List[ColorCurveEntry]:
        return list(self._curves.values())

    # Keyframe management
    def add_keyframe(self, curve_id: str, keyframe: ColorKeyframeEntry) -> bool:
        curve = self._curves.get(curve_id)
        if curve is None:
            return False
        curve.keyframes.append(keyframe)
        return True

    def remove_keyframe(self, curve_id: str, keyframe_id: str) -> bool:
        curve = self._curves.get(curve_id)
        if curve is None:
            return False
        before = len(curve.keyframes)
        curve.keyframes = [k for k in curve.keyframes if k.keyframe_id != keyframe_id]
        return len(curve.keyframes) < before

    def get_keyframes_for_curve(self, curve_id: str) -> list:
        curve = self._curves.get(curve_id)
        if curve is None:
            return []
        return list(curve.keyframes)

    # Bake management
    def add_bake(self, curve_id: str, bake: GradientBakeDef) -> bool:
        curve = self._curves.get(curve_id)
        if curve is None:
            return False
        curve.bakes.append(bake)
        return True

    def remove_bake(self, curve_id: str, bake_id: str) -> bool:
        curve = self._curves.get(curve_id)
        if curve is None:
            return False
        before = len(curve.bakes)
        curve.bakes = [b for b in curve.bakes if b.bake_id != bake_id]
        return len(curve.bakes) < before

    def get_bakes_for_curve(self, curve_id: str) -> list:
        curve = self._curves.get(curve_id)
        if curve is None:
            return []
        return list(curve.bakes)

    def get_completed_bakes(self) -> list:
        result = []
        for curve in self._curves.values():
            result.extend(b for b in curve.bakes if b.success)
        return result

    # Enable/disable
    def set_enabled(self, curve_id: str, enabled: bool) -> bool:
        curve = self._curves.get(curve_id)
        if curve is None:
            return False
        curve.enabled = enabled
        return True

    def get_enabled_curves(self) -> List[ColorCurveEntry]:
        return [c for c in self._curves.values() if c.enabled]

    def get_disabled_curves(self) -> List[ColorCurveEntry]:
        return [c for c in self._curves.values() if not c.enabled]

    # Validation
    def validate(self, entry: ColorCurveEntry) -> bool:
        return bool(entry.curve_id) and bool(entry.curve_name)

    # Properties
    @property
    def curve_count(self) -> int:
        return len(self._curves)

    @property
    def is_empty(self) -> bool:
        return len(self._curves) == 0

    def clear(self) -> None:
        self._curves.clear()
