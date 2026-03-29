"""AtlasAI Phase 23D — Terrain Chunk Loader.

Discovers and manages terrain chunk manifests, mirroring the C++
TerrainChunkRegistry for cross-language heightmap/voxel streaming.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ChunkCoord:
    """Grid coordinate for a terrain chunk."""

    x: int = 0
    z: int = 0

    def __hash__(self) -> int:
        return hash((self.x, self.z))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ChunkCoord):
            return self.x == other.x and self.z == other.z
        return NotImplemented

    def distance_to(self, other: "ChunkCoord") -> float:
        return ((self.x - other.x) ** 2 + (self.z - other.z) ** 2) ** 0.5


@dataclass
class TerrainChunkManifest:
    """Parsed terrain chunk manifest."""

    chunk_id: str
    coord: ChunkCoord
    resolution: int = 16
    chunk_size: float = 100.0
    bundle_ids: list[str] = field(default_factory=list)
    material_id: str = ""
    generator_seed: str = ""
    always_loaded: bool = False
    priority: int = 0
    manifest_path: str = ""

    @property
    def bundle_count(self) -> int:
        return len(self.bundle_ids)

    @property
    def world_origin_x(self) -> float:
        return self.coord.x * self.chunk_size

    @property
    def world_origin_z(self) -> float:
        return self.coord.z * self.chunk_size


class TerrainChunkLoader:
    """Discover, register, and manage terrain chunk manifests.

    Chunk manifests live under *content_root* and are named
    ``chunk_manifest.json``.

    Example::

        loader = TerrainChunkLoader("/repo/NovaForge/Content")
        loader.discover()
        loader.load_chunk("chunk_0_0")
        nearby = loader.get_chunks_in_range(ChunkCoord(0, 0), radius=2)
    """

    MANIFEST_FILENAME = "chunk_manifest.json"

    def __init__(self, content_root: str) -> None:
        self.content_root = Path(content_root)
        self._chunks: dict[str, TerrainChunkManifest] = {}
        self._loaded: set[str] = set()

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover(self) -> list[str]:
        """Walk *content_root* for all ``chunk_manifest.json`` files."""
        discovered: list[str] = []
        for mf in self.content_root.rglob(self.MANIFEST_FILENAME):
            try:
                data = json.loads(mf.read_text(encoding="utf-8"))
                coord = ChunkCoord(
                    x=data.get("coord_x", 0),
                    z=data.get("coord_z", 0),
                )
                manifest = TerrainChunkManifest(
                    chunk_id=data["chunk_id"],
                    coord=coord,
                    resolution=data.get("resolution", 16),
                    chunk_size=data.get("chunk_size", 100.0),
                    bundle_ids=data.get("bundle_ids", []),
                    material_id=data.get("material_id", ""),
                    generator_seed=data.get("generator_seed", ""),
                    always_loaded=data.get("always_loaded", False),
                    priority=data.get("priority", 0),
                    manifest_path=str(mf),
                )
                self._chunks[manifest.chunk_id] = manifest
                discovered.append(manifest.chunk_id)
                logger.debug("TerrainChunkLoader: discovered %s", manifest.chunk_id)
            except Exception as exc:
                logger.warning("TerrainChunkLoader: failed to parse %s — %s", mf, exc)
        return discovered

    def register_from_dict(self, data: dict) -> Optional[TerrainChunkManifest]:
        """Register a chunk from a dictionary (e.g. for testing)."""
        try:
            coord = ChunkCoord(
                x=data.get("coord_x", 0),
                z=data.get("coord_z", 0),
            )
            manifest = TerrainChunkManifest(
                chunk_id=data["chunk_id"],
                coord=coord,
                resolution=data.get("resolution", 16),
                chunk_size=data.get("chunk_size", 100.0),
                bundle_ids=data.get("bundle_ids", []),
                material_id=data.get("material_id", ""),
                generator_seed=data.get("generator_seed", ""),
                always_loaded=data.get("always_loaded", False),
                priority=data.get("priority", 0),
            )
            self._chunks[manifest.chunk_id] = manifest
            return manifest
        except Exception as exc:
            logger.error("TerrainChunkLoader.register_from_dict error: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Load / unload
    # ------------------------------------------------------------------

    def load_chunk(self, chunk_id: str) -> bool:
        if chunk_id not in self._chunks:
            return False
        self._loaded.add(chunk_id)
        logger.debug("TerrainChunkLoader: loaded %s", chunk_id)
        return True

    def unload_chunk(self, chunk_id: str) -> bool:
        if chunk_id not in self._loaded:
            return False
        self._loaded.discard(chunk_id)
        logger.debug("TerrainChunkLoader: unloaded %s", chunk_id)
        return True

    def is_loaded(self, chunk_id: str) -> bool:
        return chunk_id in self._loaded

    def get_loaded_chunk_ids(self) -> list[str]:
        return list(self._loaded)

    def get_loaded_count(self) -> int:
        return len(self._loaded)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_chunk(self, chunk_id: str) -> Optional[TerrainChunkManifest]:
        return self._chunks.get(chunk_id)

    def get_chunk_at_coord(self, cx: int, cz: int) -> Optional[TerrainChunkManifest]:
        target = ChunkCoord(cx, cz)
        for chunk in self._chunks.values():
            if chunk.coord == target:
                return chunk
        return None

    def get_chunks_in_range(
        self, center: ChunkCoord, radius: int = 1
    ) -> list[TerrainChunkManifest]:
        result = []
        for chunk in self._chunks.values():
            if (abs(chunk.coord.x - center.x) <= radius
                    and abs(chunk.coord.z - center.z) <= radius):
                result.append(chunk)
        return result

    def get_all_chunk_ids(self) -> list[str]:
        return list(self._chunks.keys())

    def get_chunk_count(self) -> int:
        return len(self._chunks)

    def get_always_loaded_chunks(self) -> list[TerrainChunkManifest]:
        return [c for c in self._chunks.values() if c.always_loaded]

    def get_chunks_by_priority(self, min_priority: int) -> list[TerrainChunkManifest]:
        return [c for c in self._chunks.values() if c.priority >= min_priority]

    def get_chunks_by_material(self, material_id: str) -> list[TerrainChunkManifest]:
        return [c for c in self._chunks.values() if c.material_id == material_id]

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def unregister(self, chunk_id: str) -> bool:
        if chunk_id not in self._chunks:
            return False
        self._chunks.pop(chunk_id)
        self._loaded.discard(chunk_id)
        return True

    def clear(self) -> None:
        self._chunks.clear()
        self._loaded.clear()
