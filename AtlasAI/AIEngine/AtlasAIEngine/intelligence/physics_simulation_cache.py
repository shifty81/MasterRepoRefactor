"""AtlasAI Phase 26B — Physics Simulation Cache.

Stores and replays deterministic physics simulation frames, reducing
re-simulation cost for baked cloth, fluid, and rigid-body sequences during
content authoring.
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class PhysicsFrameData:
    """Serialised state of a single simulation frame."""

    frame_index: int
    simulation_id: str
    timestamp_ms: float = 0.0
    body_count: int = 0
    kinetic_energy: float = 0.0
    potential_energy: float = 0.0
    contact_count: int = 0
    is_sleeping: bool = False
    checksum: str = ""

    @property
    def total_energy(self) -> float:
        return self.kinetic_energy + self.potential_energy


@dataclass
class PhysicsSimulationEntry:
    """A cached simulation run with associated frame data."""

    simulation_id: str
    name: str
    scene_id: str = ""
    frame_count: int = 0
    frame_rate: float = 60.0
    duration_seconds: float = 0.0
    body_count: int = 0
    created_at: float = field(default_factory=time.time)
    frames: list[PhysicsFrameData] = field(default_factory=list)
    is_deterministic: bool = True
    cache_size_bytes: int = 0

    @property
    def stored_frame_count(self) -> int:
        return len(self.frames)

    @property
    def is_complete(self) -> bool:
        return self.stored_frame_count >= self.frame_count and self.frame_count > 0

    @property
    def cache_size_kb(self) -> float:
        return self.cache_size_bytes / 1024.0


@dataclass
class CachePolicy:
    """Policy for cache eviction and storage limits."""

    policy_id: str
    max_entries: int = 100
    max_total_size_mb: float = 512.0
    ttl_seconds: float = 3600.0        # time-to-live
    eviction_strategy: str = "LRU"    # LRU, LFU, FIFO
    compress_frames: bool = True
    deduplicate_frames: bool = False


class PhysicsSimulationCache:
    """Cache for deterministic physics simulation results used during baking."""

    def __init__(self) -> None:
        self._entries: dict[str, PhysicsSimulationEntry] = {}
        self._access_order: list[str] = []
        self._policy: CachePolicy = CachePolicy(policy_id="default")
        self._next_sim: int = 0
        self._hit_count: int = 0
        self._miss_count: int = 0

    # ------------------------------------------------------------------
    # Policy
    # ------------------------------------------------------------------

    def set_policy(self, policy: CachePolicy) -> None:
        self._policy = policy
        logger.debug("Cache policy set: %s", policy.policy_id)

    def get_policy(self) -> CachePolicy:
        return self._policy

    # ------------------------------------------------------------------
    # Entry management
    # ------------------------------------------------------------------

    def create_entry(
        self,
        name: str,
        scene_id: str = "",
        frame_count: int = 0,
        frame_rate: float = 60.0,
        body_count: int = 0,
    ) -> PhysicsSimulationEntry:
        sim_id = f"sim_{self._next_sim:04d}"
        self._next_sim += 1
        entry = PhysicsSimulationEntry(
            simulation_id=sim_id,
            name=name,
            scene_id=scene_id,
            frame_count=frame_count,
            frame_rate=frame_rate,
            body_count=body_count,
            duration_seconds=frame_count / max(1.0, frame_rate),
        )
        self._entries[sim_id] = entry
        self._access_order.append(sim_id)
        self._evict_if_needed()
        logger.debug("Created simulation entry %s", sim_id)
        return entry

    def get_entry(self, simulation_id: str) -> Optional[PhysicsSimulationEntry]:
        entry = self._entries.get(simulation_id)
        if entry is not None:
            self._hit_count += 1
            self._touch(simulation_id)
        else:
            self._miss_count += 1
        return entry

    def has_entry(self, simulation_id: str) -> bool:
        return simulation_id in self._entries

    def remove_entry(self, simulation_id: str) -> bool:
        if simulation_id not in self._entries:
            return False
        del self._entries[simulation_id]
        if simulation_id in self._access_order:
            self._access_order.remove(simulation_id)
        return True

    def get_entry_count(self) -> int:
        return len(self._entries)

    def get_all_simulation_ids(self) -> list[str]:
        return list(self._entries.keys())

    def get_entries_for_scene(self, scene_id: str) -> list[str]:
        return [
            sid for sid, e in self._entries.items()
            if e.scene_id == scene_id
        ]

    # ------------------------------------------------------------------
    # Frame storage
    # ------------------------------------------------------------------

    def store_frame(
        self,
        simulation_id: str,
        frame_index: int,
        kinetic_energy: float = 0.0,
        potential_energy: float = 0.0,
        contact_count: int = 0,
        is_sleeping: bool = False,
    ) -> Optional[PhysicsFrameData]:
        entry = self._entries.get(simulation_id)
        if entry is None:
            return None
        frame = PhysicsFrameData(
            frame_index=frame_index,
            simulation_id=simulation_id,
            timestamp_ms=frame_index * (1000.0 / max(1.0, entry.frame_rate)),
            body_count=entry.body_count,
            kinetic_energy=kinetic_energy,
            potential_energy=potential_energy,
            contact_count=contact_count,
            is_sleeping=is_sleeping,
            checksum=f"crc_{frame_index:08x}",
        )
        entry.frames.append(frame)
        entry.cache_size_bytes += 64
        return frame

    def get_frame(
        self, simulation_id: str, frame_index: int
    ) -> Optional[PhysicsFrameData]:
        entry = self._entries.get(simulation_id)
        if entry is None:
            return None
        for f in entry.frames:
            if f.frame_index == frame_index:
                return f
        return None

    def get_frame_count(self, simulation_id: str) -> int:
        entry = self._entries.get(simulation_id)
        return entry.stored_frame_count if entry else 0

    def clear_frames(self, simulation_id: str) -> bool:
        entry = self._entries.get(simulation_id)
        if entry is None:
            return False
        entry.frames.clear()
        entry.cache_size_bytes = 0
        return True

    # ------------------------------------------------------------------
    # Cache statistics
    # ------------------------------------------------------------------

    def get_hit_count(self) -> int:
        return self._hit_count

    def get_miss_count(self) -> int:
        return self._miss_count

    def get_hit_rate(self) -> float:
        total = self._hit_count + self._miss_count
        if total == 0:
            return 0.0
        return self._hit_count / total

    def get_total_cache_size_bytes(self) -> int:
        return sum(e.cache_size_bytes for e in self._entries.values())

    def get_total_cache_size_mb(self) -> float:
        return self.get_total_cache_size_bytes() / (1024 * 1024)

    def reset_stats(self) -> None:
        self._hit_count = 0
        self._miss_count = 0

    # ------------------------------------------------------------------
    # Eviction
    # ------------------------------------------------------------------

    def _touch(self, simulation_id: str) -> None:
        if simulation_id in self._access_order:
            self._access_order.remove(simulation_id)
            self._access_order.append(simulation_id)

    def _evict_if_needed(self) -> int:
        evicted = 0
        while (
            len(self._entries) > self._policy.max_entries
            and self._access_order
        ):
            oldest = self._access_order.pop(0)
            if oldest in self._entries:
                del self._entries[oldest]
                evicted += 1
        return evicted

    def evict_oldest(self, count: int = 1) -> int:
        evicted = 0
        for _ in range(count):
            if not self._access_order:
                break
            oldest = self._access_order.pop(0)
            if oldest in self._entries:
                del self._entries[oldest]
                evicted += 1
        return evicted

    def evict_by_scene(self, scene_id: str) -> int:
        ids = self.get_entries_for_scene(scene_id)
        for sid in ids:
            self.remove_entry(sid)
        return len(ids)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_index(self, output_path: str) -> bool:
        data = {
            "entry_count": self.get_entry_count(),
            "total_size_bytes": self.get_total_cache_size_bytes(),
            "hit_count": self._hit_count,
            "miss_count": self._miss_count,
            "entries": [
                {
                    "simulation_id": e.simulation_id,
                    "name": e.name,
                    "scene_id": e.scene_id,
                    "frame_count": e.frame_count,
                    "stored_frame_count": e.stored_frame_count,
                    "is_complete": e.is_complete,
                    "cache_size_kb": e.cache_size_kb,
                }
                for e in self._entries.values()
            ],
        }
        try:
            Path(output_path).write_text(json.dumps(data, indent=2))
            return True
        except OSError as exc:
            logger.error("Failed to save cache index: %s", exc)
            return False

    def clear(self) -> None:
        self._entries.clear()
        self._access_order.clear()
        self._hit_count = 0
        self._miss_count = 0
        self._next_sim = 0
