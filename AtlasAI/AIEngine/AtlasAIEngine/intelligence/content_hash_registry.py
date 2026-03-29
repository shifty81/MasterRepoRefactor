"""AtlasAI Phase 20B — Content Hash Registry.

Tracks SHA-256 hashes of content files so that the AI pipeline can
quickly detect which assets have changed since the last baseline was
recorded, enabling targeted re-processing and invalidation.
"""
from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ContentHashEntry:
    """A single hash record for a content file."""

    path: str
    sha256: str
    size_bytes: int
    dirty: bool = False


class ContentHashRegistry:
    """Track and compare SHA-256 hashes of content/asset files.

    Usage::

        registry = ContentHashRegistry()
        registry.register_file("/repo/NovaForge/Content/Data/layout.json")
        changed = registry.get_dirty()   # after files are modified
        registry.save("/tmp/hashes.json")
    """

    def __init__(self) -> None:
        self._entries: dict[str, ContentHashEntry] = {}

    # ------------------------------------------------------------------
    # Hash helpers
    # ------------------------------------------------------------------

    @staticmethod
    def hash_file(path: str) -> Optional[str]:
        """Compute the SHA-256 hex digest of *path*.  Returns None on error."""
        try:
            h = hashlib.sha256()
            with open(path, "rb") as fh:
                for chunk in iter(lambda: fh.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception as exc:  # pragma: no cover
            logger.error("ContentHashRegistry.hash_file failed for %s: %s", path, exc)
            return None

    @staticmethod
    def hash_string(content: str) -> str:
        """Compute the SHA-256 hex digest of a UTF-8 string."""
        return hashlib.sha256(content.encode()).hexdigest()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_file(self, path: str) -> Optional[ContentHashEntry]:
        """Hash and register a file.  Returns the entry, or None on error."""
        digest = self.hash_file(path)
        if digest is None:
            return None
        try:
            size = Path(path).stat().st_size
        except OSError:
            size = 0
        entry = ContentHashEntry(path=path, sha256=digest, size_bytes=size)
        self._entries[path] = entry
        return entry

    def register_string(self, key: str, content: str) -> ContentHashEntry:
        """Register an in-memory string content under *key*."""
        digest = self.hash_string(content)
        entry = ContentHashEntry(
            path=key,
            sha256=digest,
            size_bytes=len(content.encode()),
        )
        self._entries[key] = entry
        return entry

    def unregister(self, key: str) -> bool:
        """Remove a registry entry.  Returns True if it existed."""
        if key in self._entries:
            del self._entries[key]
            return True
        return False

    # ------------------------------------------------------------------
    # Change detection
    # ------------------------------------------------------------------

    def check_file(self, path: str) -> bool:
        """Re-hash *path* and mark dirty if changed.  Returns True if dirty."""
        current = self.hash_file(path)
        if current is None:
            return False
        entry = self._entries.get(path)
        if entry is None:
            return False
        if entry.sha256 != current:
            entry.sha256 = current
            entry.dirty = True
            return True
        return False

    def check_string(self, key: str, content: str) -> bool:
        """Re-hash *content* for *key* and mark dirty if changed."""
        current = self.hash_string(content)
        entry = self._entries.get(key)
        if entry is None:
            return False
        if entry.sha256 != current:
            entry.sha256 = current
            entry.dirty = True
            return True
        return False

    def get_dirty(self) -> list[ContentHashEntry]:
        """Return all entries marked dirty."""
        return [e for e in self._entries.values() if e.dirty]

    def clear_dirty(self) -> int:
        """Reset dirty flags on all entries.  Returns number cleared."""
        count = sum(1 for e in self._entries.values() if e.dirty)
        for e in self._entries.values():
            e.dirty = False
        return count

    def get_entry(self, key: str) -> Optional[ContentHashEntry]:
        return self._entries.get(key)

    def get_entry_count(self) -> int:
        return len(self._entries)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str) -> bool:
        """Write the registry to *path* as JSON.  Returns True on success."""
        try:
            data = {
                "entry_count": len(self._entries),
                "entries": [
                    {
                        "path": e.path,
                        "sha256": e.sha256,
                        "size_bytes": e.size_bytes,
                        "dirty": e.dirty,
                    }
                    for e in self._entries.values()
                ],
            }
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(json.dumps(data, indent=2))
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("ContentHashRegistry.save failed: %s", exc)
            return False

    def load(self, path: str) -> int:
        """Load entries from a saved JSON registry.  Returns entries loaded."""
        try:
            data = json.loads(Path(path).read_text())
            for raw in data.get("entries", []):
                entry = ContentHashEntry(
                    path=raw["path"],
                    sha256=raw["sha256"],
                    size_bytes=raw.get("size_bytes", 0),
                    dirty=raw.get("dirty", False),
                )
                self._entries[entry.path] = entry
            return len(data.get("entries", []))
        except Exception as exc:  # pragma: no cover
            logger.error("ContentHashRegistry.load failed: %s", exc)
            return 0

    def clear(self) -> None:
        self._entries.clear()
