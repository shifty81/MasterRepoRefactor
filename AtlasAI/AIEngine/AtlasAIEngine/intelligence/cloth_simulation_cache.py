"""AtlasAI Phase 27B — Cloth Simulation Cache.

Caches deterministic cloth simulation frames for rapid playback during
content authoring, avoiding full re-simulation on every scene reload.
Supports per-layer cache management and configurable eviction policies.
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
class ClothFrameSnapshot:
    """Serialised vertex-level snapshot for a single cloth simulation frame."""

    frame_index: int
    layer_id: str
    simulation_id: str
    timestamp_ms: float = 0.0
    vertex_count: int = 0
    kinetic_energy: float = 0.0
    potential_energy: float = 0.0
    max_stretch: float = 0.0
    is_torn: bool = False
    checksum: str = ""

    @property
    def total_energy(self) -> float:
        return self.kinetic_energy + self.potential_energy

    @property
    def is_sleeping(self) -> bool:
        return self.kinetic_energy < 1e-5


@dataclass
class ClothSimEntry:
    """A cached cloth simulation run for a single layer."""

    simulation_id: str
    layer_id: str
    layer_name: str
    cloth_type: str = "Fabric"
    frame_count: int = 0
    frame_rate: float = 60.0
    duration_seconds: float = 0.0
    vertex_count: int = 0
    created_at: float = field(default_factory=time.time)
    frames: list[ClothFrameSnapshot] = field(default_factory=list)
    cache_size_bytes: int = 0
    is_baked: bool = False

    @property
    def stored_frame_count(self) -> int:
        return len(self.frames)

    @property
    def is_complete(self) -> bool:
        return self.stored_frame_count >= self.frame_count and self.frame_count > 0

    @property
    def cache_size_kb(self) -> float:
        return self.cache_size_bytes / 1024.0

    @property
    def fill_ratio(self) -> float:
        if self.frame_count == 0:
            return 0.0
        return self.stored_frame_count / self.frame_count


@dataclass
class ClothCachePolicy:
    """Policy for cloth simulation cache eviction and storage."""

    policy_id: str
    max_entries: int = 50
    max_total_size_mb: float = 256.0
    ttl_seconds: float = 1800.0
    eviction_strategy: str = "LRU"
    compress_frames: bool = True
    store_only_baked: bool = False


class ClothSimulationCache:
    """Per-layer cache for deterministic cloth simulation results."""

    def __init__(self) -> None:
        self._entries: dict[str, ClothSimEntry] = {}
        self._access_order: list[str] = []
        self._policy: ClothCachePolicy = ClothCachePolicy(policy_id="default")
        self._next_sim: int = 0
        self._hit_count: int = 0
        self._miss_count: int = 0

    # ------------------------------------------------------------------
    # Policy
    # ------------------------------------------------------------------

    def set_policy(self, policy: ClothCachePolicy) -> None:
        self._policy = policy
        logger.debug("Cloth cache policy set: %s", policy.policy_id)

    def get_policy(self) -> ClothCachePolicy:
        return self._policy

    # ------------------------------------------------------------------
    # Entry management
    # ------------------------------------------------------------------

    def create_entry(
        self,
        layer_id: str,
        layer_name: str,
        cloth_type: str = "Fabric",
        frame_count: int = 0,
        frame_rate: float = 60.0,
        vertex_count: int = 0,
    ) -> ClothSimEntry:
        sim_id = f"cloth_{self._next_sim:04d}"
        self._next_sim += 1
        entry = ClothSimEntry(
            simulation_id=sim_id,
            layer_id=layer_id,
            layer_name=layer_name,
            cloth_type=cloth_type,
            frame_count=frame_count,
            frame_rate=frame_rate,
            duration_seconds=frame_count / max(1.0, frame_rate),
            vertex_count=vertex_count,
        )
        self._entries[sim_id] = entry
        self._access_order.append(sim_id)
        self._evict_if_needed()
        logger.debug("Created cloth entry %s for layer %s", sim_id, layer_id)
        return entry

    def get_entry(self, simulation_id: str) -> Optional[ClothSimEntry]:
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

    def get_entries_for_layer(self, layer_id: str) -> list[str]:
        return [
            sid for sid, e in self._entries.items()
            if e.layer_id == layer_id
        ]

    def get_baked_entries(self) -> list[str]:
        return [sid for sid, e in self._entries.items() if e.is_baked]

    def mark_baked(self, simulation_id: str) -> bool:
        entry = self._entries.get(simulation_id)
        if entry is None:
            return False
        entry.is_baked = True
        return True

    # ------------------------------------------------------------------
    # Frame storage
    # ------------------------------------------------------------------

    def store_frame(
        self,
        simulation_id: str,
        frame_index: int,
        kinetic_energy: float = 0.0,
        potential_energy: float = 0.0,
        max_stretch: float = 0.0,
        is_torn: bool = False,
        vertex_count: int = 0,
    ) -> Optional[ClothFrameSnapshot]:
        entry = self._entries.get(simulation_id)
        if entry is None:
            return None
        snapshot = ClothFrameSnapshot(
            frame_index=frame_index,
            layer_id=entry.layer_id,
            simulation_id=simulation_id,
            timestamp_ms=frame_index * (1000.0 / max(1.0, entry.frame_rate)),
            vertex_count=vertex_count or entry.vertex_count,
            kinetic_energy=kinetic_energy,
            potential_energy=potential_energy,
            max_stretch=max_stretch,
            is_torn=is_torn,
            checksum=f"cloth_crc_{frame_index:08x}",
        )
        entry.frames.append(snapshot)
        entry.cache_size_bytes += snapshot.vertex_count * 12 + 64
        return snapshot

    def get_frame(
        self, simulation_id: str, frame_index: int
    ) -> Optional[ClothFrameSnapshot]:
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
        entry.is_baked = False
        return True

    # ------------------------------------------------------------------
    # Statistics
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
                if self._policy.store_only_baked and not self._entries[oldest].is_baked:
                    del self._entries[oldest]
                    evicted += 1
                elif not self._policy.store_only_baked:
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

    def evict_by_layer(self, layer_id: str) -> int:
        ids = self.get_entries_for_layer(layer_id)
        for sid in ids:
            self.remove_entry(sid)
        return len(ids)

    def evict_unbaked(self) -> int:
        unbaked = [sid for sid, e in self._entries.items() if not e.is_baked]
        for sid in unbaked:
            self.remove_entry(sid)
        return len(unbaked)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_index(self, output_path: str) -> bool:
        data = {
            "entry_count": self.get_entry_count(),
            "total_size_bytes": self.get_total_cache_size_bytes(),
            "hit_count": self._hit_count,
            "miss_count": self._miss_count,
            "baked_count": len(self.get_baked_entries()),
            "entries": [
                {
                    "simulation_id": e.simulation_id,
                    "layer_id": e.layer_id,
                    "layer_name": e.layer_name,
                    "cloth_type": e.cloth_type,
                    "frame_count": e.frame_count,
                    "stored_frame_count": e.stored_frame_count,
                    "is_complete": e.is_complete,
                    "is_baked": e.is_baked,
                    "fill_ratio": e.fill_ratio,
                    "cache_size_kb": e.cache_size_kb,
                }
                for e in self._entries.values()
            ],
        }
        try:
            Path(output_path).write_text(json.dumps(data, indent=2))
            return True
        except OSError as exc:
            logger.error("Failed to save cloth cache index: %s", exc)
            return False

    def clear(self) -> None:
        self._entries.clear()
        self._access_order.clear()
        self._hit_count = 0
        self._miss_count = 0
        self._next_sim = 0
