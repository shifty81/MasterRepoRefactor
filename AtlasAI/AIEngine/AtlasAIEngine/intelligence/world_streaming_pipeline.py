"""AtlasAI Phase 30B — World Streaming Pipeline.

Manages world zone definitions, LOD rules, and streaming operations
for dynamic large-world content loading and unloading.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class StreamingZoneDef:
    """Definition for a streamable world zone."""

    zone_id: str
    zone_name: str
    zone_type: str = "Static"       # Static, Dynamic, Procedural, Underground, Sky
    center_x: float = 0.0
    center_y: float = 0.0
    center_z: float = 0.0
    radius: float = 500.0
    load_distance: float = 1000.0
    unload_distance: float = 1500.0
    priority: int = 0

    @property
    def is_dynamic(self) -> bool:
        return self.zone_type == "Dynamic"

    @property
    def is_in_range(self) -> bool:
        # Placeholder — always returns True; real impl would compare against camera distance
        return True


@dataclass
class StreamingLODRule:
    """LOD distance rule associated with a streaming zone."""

    rule_id: str
    zone_id: str
    lod_level: int = 0
    distance_threshold: float = 200.0
    cull_distance: float = 2000.0

    @property
    def is_culled_at_threshold(self) -> bool:
        # Placeholder — always False; real impl compares object distance
        return False


@dataclass
class WorldStreamingResult:
    """Result of a streaming in/out operation."""

    job_id: str
    zones_loaded: int = 0
    zones_unloaded: int = 0
    errors: list = field(default_factory=list)
    elapsed_ms: float = 0.0

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def total_operations(self) -> int:
        return self.zones_loaded + self.zones_unloaded


class WorldStreamingPipeline:
    """Pipeline for managing world zone streaming with LOD and priority support."""

    def __init__(self) -> None:
        self._zones: dict[str, StreamingZoneDef] = {}
        self._lod_rules: dict[str, StreamingLODRule] = {}
        self._active_zones: set[str] = set()
        self._job_counter: int = 0

    def register_zone(self, zone: StreamingZoneDef) -> None:
        """Register a zone for streaming management."""
        self._zones[zone.zone_id] = zone
        logger.debug("Registered zone %s: %s", zone.zone_id, zone.zone_name)

    def unregister_zone(self, zone_id: str) -> bool:
        """Unregister a zone by ID."""
        if zone_id not in self._zones:
            return False
        del self._zones[zone_id]
        self._active_zones.discard(zone_id)
        return True

    def add_lod_rule(self, rule: StreamingLODRule) -> None:
        """Add an LOD rule for a zone."""
        self._lod_rules[rule.rule_id] = rule
        logger.debug("Added LOD rule %s for zone %s", rule.rule_id, rule.zone_id)

    def get_zone(self, zone_id: str) -> Optional[StreamingZoneDef]:
        """Retrieve a registered zone by ID."""
        return self._zones.get(zone_id)

    def get_all_zones(self) -> list:
        """Return all registered zones."""
        return list(self._zones.values())

    def stream_in(self, zone_id: str) -> WorldStreamingResult:
        """Stream a zone into active memory."""
        self._job_counter += 1
        job_id = f"job_{self._job_counter:04d}"
        start = time.monotonic()
        errors = []
        loaded = 0

        if zone_id not in self._zones:
            errors.append(f"Zone {zone_id} not registered")
        else:
            self._active_zones.add(zone_id)
            loaded = 1
            logger.debug("Streamed in zone %s", zone_id)

        elapsed = (time.monotonic() - start) * 1000.0
        return WorldStreamingResult(
            job_id=job_id,
            zones_loaded=loaded,
            zones_unloaded=0,
            errors=errors,
            elapsed_ms=elapsed,
        )

    def stream_out(self, zone_id: str) -> WorldStreamingResult:
        """Stream a zone out of active memory."""
        self._job_counter += 1
        job_id = f"job_{self._job_counter:04d}"
        start = time.monotonic()
        errors = []
        unloaded = 0

        if zone_id not in self._active_zones:
            errors.append(f"Zone {zone_id} not active")
        else:
            self._active_zones.discard(zone_id)
            unloaded = 1
            logger.debug("Streamed out zone %s", zone_id)

        elapsed = (time.monotonic() - start) * 1000.0
        return WorldStreamingResult(
            job_id=job_id,
            zones_loaded=0,
            zones_unloaded=unloaded,
            errors=errors,
            elapsed_ms=elapsed,
        )

    def get_active_zones(self) -> list:
        """Return currently active zone definitions."""
        return [self._zones[zid] for zid in self._active_zones if zid in self._zones]

    def validate_zone(self, zone: StreamingZoneDef) -> bool:
        """Validate that a zone definition has required fields."""
        return bool(zone.zone_id) and bool(zone.zone_name) and zone.radius > 0

    def clear(self) -> None:
        """Clear all zones, rules, and active state."""
        self._zones.clear()
        self._lod_rules.clear()
        self._active_zones.clear()
        self._job_counter = 0

    @property
    def zone_count(self) -> int:
        return len(self._zones)

    @property
    def active_zone_count(self) -> int:
        return len(self._active_zones)
