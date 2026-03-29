"""AtlasAI Phase 36B — Landscape Spline Pipeline.

Manages landscape spline definitions, points, and segments
for the spline authoring and deformation subsystem.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class SplinePointDef:
    """Definition of a single landscape spline control point."""

    point_id: str
    position_x: float = 0.0
    position_y: float = 0.0
    position_z: float = 0.0
    tangent_weight: float = 1.0
    arrive_tangent_x: float = 0.0
    arrive_tangent_y: float = 0.0
    leave_tangent_x: float = 0.0
    leave_tangent_y: float = 0.0

    @property
    def is_at_origin(self) -> bool:
        return self.position_x == 0.0 and self.position_y == 0.0 and self.position_z == 0.0

    @property
    def has_weight(self) -> bool:
        return self.tangent_weight != 1.0


@dataclass
class SplineSegmentDef:
    """Definition of a landscape spline segment between two points."""

    segment_id: str
    start_point_id: str
    end_point_id: str
    mesh_id: str = ""
    width: float = 200.0
    side_falloff: float = 400.0
    end_falloff: float = 0.0
    layers: list = field(default_factory=list)

    @property
    def has_mesh(self) -> bool:
        return bool(self.mesh_id)

    @property
    def has_layers(self) -> bool:
        return bool(self.layers)


@dataclass
class LandscapeSplineEntry:
    """Entry representing a full landscape spline definition."""

    spline_id: str
    spline_name: str
    points: list = field(default_factory=list)
    segments: list = field(default_factory=list)
    landscape_actor_id: str = ""
    enabled: bool = True

    @property
    def is_empty(self) -> bool:
        return not self.points

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def has_segments(self) -> bool:
        return bool(self.segments)


class LandscapeSplinePipeline:
    """Pipeline for managing landscape splines, points, and segments."""

    def __init__(self) -> None:
        self._splines: Dict[str, LandscapeSplineEntry] = {}
        self._points: Dict[str, Dict[str, SplinePointDef]] = {}
        self._segments: Dict[str, Dict[str, SplineSegmentDef]] = {}

    def add_spline(self, s: LandscapeSplineEntry) -> None:
        """Register a landscape spline."""
        self._splines[s.spline_id] = s
        self._points.setdefault(s.spline_id, {})
        self._segments.setdefault(s.spline_id, {})

    def remove_spline(self, spline_id: str) -> bool:
        """Remove a spline by ID."""
        if spline_id in self._splines:
            del self._splines[spline_id]
            self._points.pop(spline_id, None)
            self._segments.pop(spline_id, None)
            return True
        return False

    def get_spline(self, spline_id: str) -> Optional[LandscapeSplineEntry]:
        """Retrieve a spline by ID."""
        return self._splines.get(spline_id)

    def get_all_splines(self) -> List[LandscapeSplineEntry]:
        """Return all registered splines."""
        return list(self._splines.values())

    def add_point(self, spline_id: str, point: SplinePointDef) -> bool:
        """Add a point to a spline."""
        if spline_id not in self._splines:
            return False
        self._points.setdefault(spline_id, {})[point.point_id] = point
        spline = self._splines[spline_id]
        if point.point_id not in spline.points:
            spline.points.append(point.point_id)
        return True

    def remove_point(self, spline_id: str, point_id: str) -> bool:
        """Remove a point from a spline."""
        points = self._points.get(spline_id, {})
        if point_id in points:
            del points[point_id]
            spline = self._splines.get(spline_id)
            if spline and point_id in spline.points:
                spline.points.remove(point_id)
            return True
        return False

    def add_segment(self, spline_id: str, segment: SplineSegmentDef) -> bool:
        """Add a segment to a spline."""
        if spline_id not in self._splines:
            return False
        self._segments.setdefault(spline_id, {})[segment.segment_id] = segment
        spline = self._splines[spline_id]
        if segment.segment_id not in spline.segments:
            spline.segments.append(segment.segment_id)
        return True

    def remove_segment(self, spline_id: str, segment_id: str) -> bool:
        """Remove a segment from a spline."""
        segments = self._segments.get(spline_id, {})
        if segment_id in segments:
            del segments[segment_id]
            spline = self._splines.get(spline_id)
            if spline and segment_id in spline.segments:
                spline.segments.remove(segment_id)
            return True
        return False

    def set_enabled(self, spline_id: str, enabled: bool) -> bool:
        """Enable or disable a spline."""
        spline = self._splines.get(spline_id)
        if spline is None:
            return False
        spline.enabled = enabled
        return True

    def get_enabled_splines(self) -> List[LandscapeSplineEntry]:
        """Return all enabled splines."""
        return [s for s in self._splines.values() if s.is_enabled]

    def get_disabled_splines(self) -> List[LandscapeSplineEntry]:
        """Return all disabled splines."""
        return [s for s in self._splines.values() if not s.is_enabled]

    def get_points_for_spline(self, spline_id: str) -> List[SplinePointDef]:
        """Return all points for a given spline."""
        return list(self._points.get(spline_id, {}).values())

    def get_segments_for_spline(self, spline_id: str) -> List[SplineSegmentDef]:
        """Return all segments for a given spline."""
        return list(self._segments.get(spline_id, {}).values())

    def validate(self, spline: LandscapeSplineEntry) -> bool:
        """Validate a spline has required fields."""
        return bool(spline.spline_id) and bool(spline.spline_name)

    def clear(self) -> None:
        """Clear all pipeline data."""
        self._splines.clear()
        self._points.clear()
        self._segments.clear()

    @property
    def spline_count(self) -> int:
        return len(self._splines)

    @property
    def is_empty(self) -> bool:
        return len(self._splines) == 0
