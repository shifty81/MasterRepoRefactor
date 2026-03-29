"""AtlasAI Phase 22B — Build Cache Manager.

Stores and retrieves cached build artefact fingerprints so that incremental
builds can skip unchanged targets.  Plugs into AIBuildMonitor's summaries
to automatically mark targets as stale when dependencies change.
"""
from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """A single cached build artefact record."""

    target_id: str
    source_hash: str
    output_hash: str
    build_time: float
    extra: dict = field(default_factory=dict)

    @property
    def age_seconds(self) -> float:
        return time.time() - self.build_time


class BuildCacheManager:
    """Lightweight, JSON-backed build cache for incremental build support.

    Typical usage::

        cache = BuildCacheManager("/tmp/build_cache.json")
        cache.load()                              # restore from disk
        if not cache.is_valid("target_a", new_hash):
            build("target_a")
            cache.store("target_a", new_hash, output_hash)
        cache.save()                              # persist

    The cache is also queryable by partial hash prefix and supports bulk
    invalidation by tag.
    """

    def __init__(self, cache_path: str = "") -> None:
        self.cache_path = cache_path
        self._entries: dict[str, CacheEntry] = {}

    # ------------------------------------------------------------------
    # Core cache operations
    # ------------------------------------------------------------------

    def store(self, target_id: str, source_hash: str,
              output_hash: str, extra: Optional[dict] = None) -> CacheEntry:
        """Store (or overwrite) a cache entry for *target_id*."""
        entry = CacheEntry(
            target_id=target_id,
            source_hash=source_hash,
            output_hash=output_hash,
            build_time=time.time(),
            extra=dict(extra or {}),
        )
        self._entries[target_id] = entry
        logger.debug("BuildCacheManager: stored %s", target_id)
        return entry

    def retrieve(self, target_id: str) -> Optional[CacheEntry]:
        return self._entries.get(target_id)

    def invalidate(self, target_id: str) -> bool:
        return self._entries.pop(target_id, None) is not None

    def invalidate_many(self, target_ids: list[str]) -> int:
        return sum(1 for tid in target_ids if self.invalidate(tid))

    def is_valid(self, target_id: str, source_hash: str) -> bool:
        """Return True if the target's cached source hash matches *source_hash*."""
        entry = self._entries.get(target_id)
        return entry is not None and entry.source_hash == source_hash

    def is_cached(self, target_id: str) -> bool:
        return target_id in self._entries

    def get_entry_count(self) -> int:
        return len(self._entries)

    def get_all_target_ids(self) -> list[str]:
        return list(self._entries.keys())

    # ------------------------------------------------------------------
    # Hash utilities
    # ------------------------------------------------------------------

    @staticmethod
    def hash_string(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

    @staticmethod
    def hash_file(path: str) -> Optional[str]:
        try:
            data = Path(path).read_bytes()
            return hashlib.sha256(data).hexdigest()
        except OSError:
            return None

    def hash_prefix_lookup(self, prefix: str) -> list[str]:
        """Find target IDs whose source_hash starts with *prefix*."""
        return [tid for tid, e in self._entries.items()
                if e.source_hash.startswith(prefix)]

    # ------------------------------------------------------------------
    # Stale detection
    # ------------------------------------------------------------------

    def get_stale_entries(self, max_age_seconds: float) -> list[CacheEntry]:
        """Return entries older than *max_age_seconds*."""
        now = time.time()
        return [e for e in self._entries.values()
                if (now - e.build_time) > max_age_seconds]

    def evict_stale(self, max_age_seconds: float) -> int:
        stale = self.get_stale_entries(max_age_seconds)
        for e in stale:
            del self._entries[e.target_id]
        return len(stale)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: Optional[str] = None) -> bool:
        dest = path or self.cache_path
        if not dest:
            logger.warning("BuildCacheManager.save: no path specified")
            return False
        try:
            data = {
                target_id: {
                    "source_hash": e.source_hash,
                    "output_hash": e.output_hash,
                    "build_time": e.build_time,
                    "extra": e.extra,
                }
                for target_id, e in self._entries.items()
            }
            Path(dest).parent.mkdir(parents=True, exist_ok=True)
            Path(dest).write_text(json.dumps(data, indent=2))
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("BuildCacheManager.save failed: %s", exc)
            return False

    def load(self, path: Optional[str] = None) -> bool:
        src = path or self.cache_path
        if not src or not Path(src).exists():
            return False
        try:
            data = json.loads(Path(src).read_text())
            self._entries.clear()
            for tid, raw in data.items():
                self._entries[tid] = CacheEntry(
                    target_id=tid,
                    source_hash=raw["source_hash"],
                    output_hash=raw["output_hash"],
                    build_time=raw.get("build_time", 0.0),
                    extra=raw.get("extra", {}),
                )
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("BuildCacheManager.load failed: %s", exc)
            return False

    def clear(self) -> None:
        self._entries.clear()
