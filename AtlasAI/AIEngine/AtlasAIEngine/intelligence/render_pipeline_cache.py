"""AtlasAI Phase 30B — Render Pipeline Cache.

Manages cached render pipeline configurations including pass definitions,
pipeline entries, and cache statistics for efficient render pipeline lookups.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class RenderPassDef:
    """Definition for a single render pass in a pipeline."""

    pass_id: str
    pass_name: str
    pass_type: str = "Opaque"       # Opaque, Transparent, Shadow, PostProcess, UI, Compute
    render_target: str = "MainRT"
    priority: int = 0
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_postprocess(self) -> bool:
        return self.pass_type == "PostProcess"


@dataclass
class RenderPipelineEntry:
    """A cached render pipeline entry containing ordered passes."""

    entry_id: str
    pipeline_name: str
    passes: list = field(default_factory=list)
    version: int = 1
    platform: str = "PC"
    last_modified: float = field(default_factory=lambda: 0.0)

    @property
    def pass_count(self) -> int:
        return len(self.passes)

    @property
    def is_empty(self) -> bool:
        return len(self.passes) == 0


@dataclass
class PipelineCacheStats:
    """Statistics for the render pipeline cache."""

    total_entries: int = 0
    total_passes: int = 0
    cache_hits: int = 0
    cache_misses: int = 0

    @property
    def hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total

    @property
    def total_lookups(self) -> int:
        return self.cache_hits + self.cache_misses


class RenderPipelineCache:
    """Cache for render pipeline configurations supporting lookup by name."""

    def __init__(self) -> None:
        self._entries: dict[str, RenderPipelineEntry] = {}
        self._invalidated: set[str] = set()
        self._stats = PipelineCacheStats()

    def add_entry(self, entry: RenderPipelineEntry) -> None:
        """Add or replace a pipeline entry in the cache."""
        self._entries[entry.entry_id] = entry
        self._invalidated.discard(entry.entry_id)
        self._stats.total_entries = len(self._entries)
        self._stats.total_passes = sum(e.pass_count for e in self._entries.values())
        logger.debug("Added pipeline entry %s: %s", entry.entry_id, entry.pipeline_name)

    def remove_entry(self, entry_id: str) -> bool:
        """Remove an entry from the cache by ID."""
        if entry_id not in self._entries:
            return False
        del self._entries[entry_id]
        self._invalidated.discard(entry_id)
        self._stats.total_entries = len(self._entries)
        self._stats.total_passes = sum(e.pass_count for e in self._entries.values())
        return True

    def get_entry(self, entry_id: str) -> Optional[RenderPipelineEntry]:
        """Retrieve an entry by its ID."""
        entry = self._entries.get(entry_id)
        if entry is not None and entry_id not in self._invalidated:
            self._stats.cache_hits += 1
        else:
            self._stats.cache_misses += 1
        return entry if entry_id not in self._invalidated else None

    def get_all_entries(self) -> list:
        """Return all non-invalidated entries."""
        return [e for eid, e in self._entries.items() if eid not in self._invalidated]

    def lookup(self, pipeline_name: str) -> Optional[RenderPipelineEntry]:
        """Lookup an entry by pipeline name."""
        for entry_id, entry in self._entries.items():
            if entry.pipeline_name == pipeline_name and entry_id not in self._invalidated:
                self._stats.cache_hits += 1
                return entry
        self._stats.cache_misses += 1
        return None

    def invalidate(self, entry_id: str) -> bool:
        """Mark a specific entry as invalid."""
        if entry_id not in self._entries:
            return False
        self._invalidated.add(entry_id)
        return True

    def invalidate_all(self) -> None:
        """Mark all entries as invalid."""
        self._invalidated = set(self._entries.keys())

    def get_stats(self) -> PipelineCacheStats:
        """Return current cache statistics."""
        self._stats.total_entries = len(self._entries)
        self._stats.total_passes = sum(e.pass_count for e in self._entries.values())
        return self._stats

    def save_cache(self, path: Path) -> None:
        """Serialize the cache to a JSON file."""
        data = {
            "entries": [
                {
                    "entry_id": e.entry_id,
                    "pipeline_name": e.pipeline_name,
                    "version": e.version,
                    "platform": e.platform,
                    "passes": [
                        {
                            "pass_id": p.pass_id,
                            "pass_name": p.pass_name,
                            "pass_type": p.pass_type,
                            "render_target": p.render_target,
                            "priority": p.priority,
                            "enabled": p.enabled,
                        }
                        for p in e.passes
                    ],
                }
                for e in self._entries.values()
            ]
        }
        Path(path).write_text(json.dumps(data, indent=2))

    def load_cache(self, path: Path) -> None:
        """Deserialize the cache from a JSON file."""
        raw = json.loads(Path(path).read_text())
        for e_data in raw.get("entries", []):
            passes = [
                RenderPassDef(
                    pass_id=p["pass_id"],
                    pass_name=p["pass_name"],
                    pass_type=p.get("pass_type", "Opaque"),
                    render_target=p.get("render_target", "MainRT"),
                    priority=p.get("priority", 0),
                    enabled=p.get("enabled", True),
                )
                for p in e_data.get("passes", [])
            ]
            entry = RenderPipelineEntry(
                entry_id=e_data["entry_id"],
                pipeline_name=e_data["pipeline_name"],
                passes=passes,
                version=e_data.get("version", 1),
                platform=e_data.get("platform", "PC"),
            )
            self.add_entry(entry)

    def clear(self) -> None:
        """Clear all entries and reset stats."""
        self._entries.clear()
        self._invalidated.clear()
        self._stats = PipelineCacheStats()

    @property
    def entry_count(self) -> int:
        return len(self._entries)

    @property
    def is_empty(self) -> bool:
        return len(self._entries) == 0
