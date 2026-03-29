"""AtlasAI Phase 24D — Scene Partition Loader.

Discovers and manages scene partition manifests, mirroring the C++
ScenePartitionRegistry for cross-language spatial streaming coordination.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class PartitionBounds:
    """Axis-aligned bounding box for a scene partition."""

    min_x: float = 0.0
    min_y: float = 0.0
    min_z: float = 0.0
    max_x: float = 100.0
    max_y: float = 100.0
    max_z: float = 100.0

    def contains_point(self, px: float, py: float, pz: float) -> bool:
        return (self.min_x <= px <= self.max_x
                and self.min_y <= py <= self.max_y
                and self.min_z <= pz <= self.max_z)

    def intersects(self, other: "PartitionBounds") -> bool:
        return (self.min_x <= other.max_x and self.max_x >= other.min_x
                and self.min_y <= other.max_y and self.max_y >= other.min_y
                and self.min_z <= other.max_z and self.max_z >= other.min_z)

    @property
    def volume(self) -> float:
        return (max(0.0, self.max_x - self.min_x)
                * max(0.0, self.max_y - self.min_y)
                * max(0.0, self.max_z - self.min_z))


@dataclass
class PartitionPortal:
    """A portal connection between two partitions."""

    portal_id: str
    from_partition_id: str
    to_partition_id: str
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    width: float = 3.0
    height: float = 3.0
    bidirectional: bool = True


@dataclass
class ScenePartitionManifest:
    """Parsed scene partition manifest."""

    partition_id: str
    name: str
    partition_type: str = "Sector"
    bounds: PartitionBounds = field(default_factory=PartitionBounds)
    bundle_ids: list[str] = field(default_factory=list)
    neighbour_ids: list[str] = field(default_factory=list)
    always_loaded: bool = False
    priority: int = 0
    parent_partition_id: str = ""
    scene_asset_path: str = ""
    manifest_path: str = ""

    @property
    def bundle_count(self) -> int:
        return len(self.bundle_ids)

    @property
    def neighbour_count(self) -> int:
        return len(self.neighbour_ids)


class ScenePartitionLoader:
    """Discover, register, and manage scene partition manifests.

    Partition manifests live under *content_root* and are named
    ``partition_manifest.json``.

    Example::

        loader = ScenePartitionLoader("/repo/NovaForge/Content")
        loader.discover()
        loader.load_partition("sector_01")
        nearby = loader.query_point(50.0, 0.0, 50.0)
    """

    MANIFEST_FILENAME = "partition_manifest.json"

    def __init__(self, content_root: str) -> None:
        self.content_root = Path(content_root)
        self._partitions: dict[str, ScenePartitionManifest] = {}
        self._portals: dict[str, PartitionPortal] = {}
        self._loaded: set[str] = set()
        self._next_portal = 0

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover(self) -> list[str]:
        """Walk *content_root* for all ``partition_manifest.json`` files."""
        discovered: list[str] = []
        for mf in self.content_root.rglob(self.MANIFEST_FILENAME):
            try:
                data = json.loads(mf.read_text(encoding="utf-8"))
                bounds_data = data.get("bounds", {})
                bounds = PartitionBounds(
                    min_x=bounds_data.get("min_x", 0.0),
                    min_y=bounds_data.get("min_y", 0.0),
                    min_z=bounds_data.get("min_z", 0.0),
                    max_x=bounds_data.get("max_x", 100.0),
                    max_y=bounds_data.get("max_y", 100.0),
                    max_z=bounds_data.get("max_z", 100.0),
                )
                manifest = ScenePartitionManifest(
                    partition_id=data["partition_id"],
                    name=data.get("name", ""),
                    partition_type=data.get("partition_type", "Sector"),
                    bounds=bounds,
                    bundle_ids=data.get("bundle_ids", []),
                    neighbour_ids=data.get("neighbour_ids", []),
                    always_loaded=data.get("always_loaded", False),
                    priority=data.get("priority", 0),
                    parent_partition_id=data.get("parent_partition_id", ""),
                    scene_asset_path=data.get("scene_asset_path", ""),
                    manifest_path=str(mf),
                )
                self._partitions[manifest.partition_id] = manifest
                discovered.append(manifest.partition_id)
                logger.debug("ScenePartitionLoader: discovered %s", manifest.partition_id)
            except Exception as exc:
                logger.warning("ScenePartitionLoader: failed to parse %s — %s", mf, exc)
        return discovered

    def register_from_dict(self, data: dict) -> Optional[ScenePartitionManifest]:
        """Register a partition from a dictionary."""
        try:
            bounds_data = data.get("bounds", {})
            bounds = PartitionBounds(
                min_x=bounds_data.get("min_x", 0.0),
                min_y=bounds_data.get("min_y", 0.0),
                min_z=bounds_data.get("min_z", 0.0),
                max_x=bounds_data.get("max_x", 100.0),
                max_y=bounds_data.get("max_y", 100.0),
                max_z=bounds_data.get("max_z", 100.0),
            )
            manifest = ScenePartitionManifest(
                partition_id=data["partition_id"],
                name=data.get("name", ""),
                partition_type=data.get("partition_type", "Sector"),
                bounds=bounds,
                bundle_ids=data.get("bundle_ids", []),
                neighbour_ids=data.get("neighbour_ids", []),
                always_loaded=data.get("always_loaded", False),
                priority=data.get("priority", 0),
                parent_partition_id=data.get("parent_partition_id", ""),
                scene_asset_path=data.get("scene_asset_path", ""),
            )
            self._partitions[manifest.partition_id] = manifest
            return manifest
        except Exception as exc:
            logger.error("ScenePartitionLoader.register_from_dict error: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Portal management
    # ------------------------------------------------------------------

    def register_portal(
        self,
        from_id: str,
        to_id: str,
        pos_x: float = 0.0,
        pos_y: float = 0.0,
        pos_z: float = 0.0,
        width: float = 3.0,
        height: float = 3.0,
        bidirectional: bool = True,
    ) -> Optional[PartitionPortal]:
        if from_id not in self._partitions or to_id not in self._partitions:
            return None
        pid = f"portal_{self._next_portal:05d}"
        self._next_portal += 1
        portal = PartitionPortal(
            portal_id=pid,
            from_partition_id=from_id,
            to_partition_id=to_id,
            pos_x=pos_x,
            pos_y=pos_y,
            pos_z=pos_z,
            width=width,
            height=height,
            bidirectional=bidirectional,
        )
        self._portals[pid] = portal
        # Update neighbour lists
        if to_id not in self._partitions[from_id].neighbour_ids:
            self._partitions[from_id].neighbour_ids.append(to_id)
        if bidirectional and from_id not in self._partitions[to_id].neighbour_ids:
            self._partitions[to_id].neighbour_ids.append(from_id)
        return portal

    def unregister_portal(self, portal_id: str) -> bool:
        if portal_id not in self._portals:
            return False
        del self._portals[portal_id]
        return True

    def get_portal(self, portal_id: str) -> Optional[PartitionPortal]:
        return self._portals.get(portal_id)

    def get_portal_count(self) -> int:
        return len(self._portals)

    def get_portals_for_partition(self, partition_id: str) -> list[PartitionPortal]:
        return [
            p for p in self._portals.values()
            if p.from_partition_id == partition_id
            or (p.bidirectional and p.to_partition_id == partition_id)
        ]

    # ------------------------------------------------------------------
    # Load / unload
    # ------------------------------------------------------------------

    def load_partition(self, partition_id: str) -> bool:
        if partition_id not in self._partitions:
            return False
        self._loaded.add(partition_id)
        return True

    def unload_partition(self, partition_id: str) -> bool:
        if partition_id not in self._loaded:
            return False
        self._loaded.discard(partition_id)
        return True

    def is_loaded(self, partition_id: str) -> bool:
        return partition_id in self._loaded

    def get_loaded_partition_ids(self) -> list[str]:
        return list(self._loaded)

    def get_loaded_count(self) -> int:
        return len(self._loaded)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_partition(self, partition_id: str) -> Optional[ScenePartitionManifest]:
        return self._partitions.get(partition_id)

    def get_all_partition_ids(self) -> list[str]:
        return list(self._partitions.keys())

    def get_partition_count(self) -> int:
        return len(self._partitions)

    def query_point(self, px: float, py: float, pz: float) -> list[ScenePartitionManifest]:
        return [p for p in self._partitions.values() if p.bounds.contains_point(px, py, pz)]

    def get_always_loaded_partitions(self) -> list[ScenePartitionManifest]:
        return [p for p in self._partitions.values() if p.always_loaded]

    def get_partitions_by_type(self, partition_type: str) -> list[ScenePartitionManifest]:
        return [p for p in self._partitions.values() if p.partition_type == partition_type]

    def get_partitions_by_priority(self, min_priority: int) -> list[ScenePartitionManifest]:
        return [p for p in self._partitions.values() if p.priority >= min_priority]

    def get_neighbours(self, partition_id: str) -> list[str]:
        p = self._partitions.get(partition_id)
        return list(p.neighbour_ids) if p else []

    def get_children(self, parent_id: str) -> list[ScenePartitionManifest]:
        return [p for p in self._partitions.values()
                if p.parent_partition_id == parent_id]

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def unregister(self, partition_id: str) -> bool:
        if partition_id not in self._partitions:
            return False
        del self._partitions[partition_id]
        self._loaded.discard(partition_id)
        return True

    def clear(self) -> None:
        self._partitions.clear()
        self._portals.clear()
        self._loaded.clear()
