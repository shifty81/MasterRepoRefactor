"""indexer.py — Lightweight project/archive indexer for AtlasAI context retrieval."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Optional
from core.logger import get_logger

logger = get_logger(__name__)


class IndexEntry:
    """Single entry in the project index."""

    def __init__(self, path: str, kind: str, size: int, content_hash: str = "") -> None:
        self.path         = path
        self.kind         = kind        # e.g. "source", "doc", "data", "config"
        self.size         = size
        self.content_hash = content_hash
        self.tags: list[str] = []

    def to_dict(self) -> dict:
        return {
            "path":         self.path,
            "kind":         self.kind,
            "size":         self.size,
            "content_hash": self.content_hash,
            "tags":         self.tags,
        }


class ProjectIndexer:
    """Indexes a project root for AI context retrieval."""

    # Extensions → kind mapping
    _KIND_MAP: dict[str, str] = {
        ".cpp": "source", ".h": "source", ".hpp": "source",
        ".cs":  "source", ".py": "source",
        ".md":  "doc",    ".txt": "doc",  ".rst": "doc",
        ".json": "data",  ".yaml": "data", ".yml": "data", ".toml": "config",
        ".cmake": "config", ".sh": "script", ".ps1": "script",
    }

    def __init__(self) -> None:
        self._entries: dict[str, IndexEntry] = {}  # path → entry
        self._root: Optional[Path] = None

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    def index_directory(self, root: str | Path, max_depth: int = 10) -> int:
        """Index all files under *root* up to *max_depth*. Returns count added."""
        root = Path(root)
        if not root.is_dir():
            logger.warning("Indexer: root is not a directory: %s", root)
            return 0
        self._root = root
        added = 0
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            # Respect max depth
            try:
                rel = path.relative_to(root)
            except ValueError:
                continue
            if len(rel.parts) > max_depth:
                continue
            added += self._add_file(path, root)
        logger.debug("Indexer: indexed %d files from %s", added, root)
        return added

    def index_file(self, path: str | Path) -> bool:
        """Index a single file. Returns True if added."""
        path = Path(path)
        root = self._root or path.parent
        return bool(self._add_file(path, root))

    def _add_file(self, path: Path, root: Path) -> int:
        try:
            rel_path = str(path.relative_to(root))
        except ValueError:
            rel_path = str(path)
        kind = self._KIND_MAP.get(path.suffix.lower(), "other")
        try:
            size = path.stat().st_size
            content_hash = self._hash_file(path)
        except OSError:
            size = 0
            content_hash = ""
        entry = IndexEntry(rel_path, kind, size, content_hash)
        self._entries[rel_path] = entry
        return 1

    @staticmethod
    def _hash_file(path: Path) -> str:
        h = hashlib.sha256()
        try:
            with path.open("rb") as f:
                while chunk := f.read(8192):
                    h.update(chunk)
        except OSError:
            return ""
        return h.hexdigest()[:16]

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def search(self, query: str, kind: Optional[str] = None) -> list[IndexEntry]:
        """Return entries whose path contains *query* (case-insensitive)."""
        q = query.lower()
        results = []
        for entry in self._entries.values():
            if kind and entry.kind != kind:
                continue
            if q in entry.path.lower():
                results.append(entry)
        return results

    def get(self, path: str) -> Optional[IndexEntry]:
        return self._entries.get(path)

    def list_by_kind(self, kind: str) -> list[IndexEntry]:
        return [e for e in self._entries.values() if e.kind == kind]

    def list_all(self) -> list[IndexEntry]:
        return list(self._entries.values())

    def count(self) -> int:
        return len(self._entries)

    def clear(self) -> None:
        self._entries.clear()
        self._root = None
