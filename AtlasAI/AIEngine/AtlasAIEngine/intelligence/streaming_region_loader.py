"""AtlasAI Phase 22D — Streaming Region Loader.

Discovers and manages streaming region manifests, mirrors the C++
StreamingRegionRegistry for cross-language level streaming coordination.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class RegionBounds:
    """Axis-aligned bounding box for a streaming region."""

    min_x: float = 0.0
    min_y: float = 0.0
    min_z: float = 0.0
    max_x: float = 100.0
    max_y: float = 100.0
    max_z: float = 100.0

    def contains_point(self, px: float, py: float, pz: float) -> bool:
        return (self.min_x <= px <= self.max_x and
                self.min_y <= py <= self.max_y and
                self.min_z <= pz <= self.max_z)


@dataclass
class StreamingRegionManifest:
    """Parsed streaming region manifest."""

    region_id: str
    name: str
    bounds: RegionBounds
    bundle_ids: list[str] = field(default_factory=list)
    always_loaded: bool = False
    priority: int = 0
    manifest_path: str = ""

    @property
    def bundle_count(self) -> int:
        return len(self.bundle_ids)


class StreamingRegionLoader:
    """Discover, register, and manage streaming region manifests.

    Region manifests live under *content_root* and are named
    ``region_manifest.json``.

    Example::

        loader = StreamingRegionLoader("/repo/NovaForge/Content")
        loader.discover()
        loader.load_region("region_zone_01")
        regions = loader.query_point(100.0, 0.0, 200.0)
    """

    MANIFEST_FILENAME = "region_manifest.json"

    def __init__(self, content_root: str) -> None:
        self.content_root = Path(content_root)
        self._regions: dict[str, StreamingRegionManifest] = {}
        self._loaded: set[str] = set()

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover(self) -> list[str]:
        """Walk *content_root* for all ``region_manifest.json`` files."""
        discovered: list[str] = []
        for mf in self.content_root.rglob(self.MANIFEST_FILENAME):
            try:
                data = json.loads(mf.read_text())
                manifest = self._parse(data, str(mf))
                self._regions[manifest.region_id] = manifest
                discovered.append(manifest.region_id)
            except Exception as exc:  # pragma: no cover
                logger.warning("StreamingRegionLoader: skipping %s — %s", mf, exc)
        return discovered

    def register_manifest(self, data: dict,
                           manifest_path: str = "") -> StreamingRegionManifest:
        """Manually register a manifest from a pre-parsed dict."""
        manifest = self._parse(data, manifest_path)
        self._regions[manifest.region_id] = manifest
        return manifest

    @staticmethod
    def _parse(data: dict, manifest_path: str) -> StreamingRegionManifest:
        bounds_raw = data.get("bounds", {})
        bounds = RegionBounds(
            min_x=bounds_raw.get("min_x", 0.0),
            min_y=bounds_raw.get("min_y", 0.0),
            min_z=bounds_raw.get("min_z", 0.0),
            max_x=bounds_raw.get("max_x", 100.0),
            max_y=bounds_raw.get("max_y", 100.0),
            max_z=bounds_raw.get("max_z", 100.0),
        )
        return StreamingRegionManifest(
            region_id=data["region_id"],
            name=data.get("name", data["region_id"]),
            bounds=bounds,
            bundle_ids=list(data.get("bundle_ids", [])),
            always_loaded=data.get("always_loaded", False),
            priority=data.get("priority", 0),
            manifest_path=manifest_path,
        )

    # ------------------------------------------------------------------
    # Load / unload
    # ------------------------------------------------------------------

    def load_region(self, region_id: str) -> bool:
        if region_id not in self._regions:
            return False
        self._loaded.add(region_id)
        return True

    def unload_region(self, region_id: str) -> bool:
        if region_id in self._loaded:
            self._loaded.discard(region_id)
            return True
        return False

    def is_loaded(self, region_id: str) -> bool:
        return region_id in self._loaded

    def get_loaded_count(self) -> int:
        return len(self._loaded)

    def get_loaded_region_ids(self) -> list[str]:
        return list(self._loaded)

    # ------------------------------------------------------------------
    # Spatial query
    # ------------------------------------------------------------------

    def query_point(self, px: float, py: float, pz: float) -> list[str]:
        """Return IDs of regions whose bounds contain the given point."""
        return [rid for rid, m in self._regions.items()
                if m.bounds.contains_point(px, py, pz)]

    def get_always_loaded(self) -> list[StreamingRegionManifest]:
        return [m for m in self._regions.values() if m.always_loaded]

    def get_by_priority(self, min_priority: int) -> list[StreamingRegionManifest]:
        return [m for m in self._regions.values()
                if m.priority >= min_priority]

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_manifest(self, region_id: str) -> Optional[StreamingRegionManifest]:
        return self._regions.get(region_id)

    def get_registered_count(self) -> int:
        return len(self._regions)

    def get_all_region_ids(self) -> list[str]:
        return list(self._regions.keys())

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_manifest(self, region_id: str, path: str) -> bool:
        m = self._regions.get(region_id)
        if m is None:
            return False
        try:
            data = {
                "region_id": m.region_id,
                "name": m.name,
                "bounds": {
                    "min_x": m.bounds.min_x,
                    "min_y": m.bounds.min_y,
                    "min_z": m.bounds.min_z,
                    "max_x": m.bounds.max_x,
                    "max_y": m.bounds.max_y,
                    "max_z": m.bounds.max_z,
                },
                "bundle_ids": m.bundle_ids,
                "always_loaded": m.always_loaded,
                "priority": m.priority,
            }
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(json.dumps(data, indent=2))
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("StreamingRegionLoader.export_manifest failed: %s", exc)
            return False

    def clear(self) -> None:
        self._regions.clear()
        self._loaded.clear()
