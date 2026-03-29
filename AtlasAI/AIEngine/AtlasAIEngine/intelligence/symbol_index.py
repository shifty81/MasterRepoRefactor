"""AtlasAI Phase 17D — Code Intelligence: in-memory symbol index.

Builds and queries a flat symbol table from C++ header files,
providing fast name-to-location lookup without requiring a running
language server.
"""
from __future__ import annotations

import re
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

# Regex patterns for common C++ declarations
_CLASS_RE = re.compile(r'\bclass\s+(\w+)')
_STRUCT_RE = re.compile(r'\bstruct\s+(\w+)')
_FUNC_RE = re.compile(r'\b(\w+)\s*\(')
_ENUM_RE = re.compile(r'\benum(?:\s+class)?\s+(\w+)')


@dataclass
class SymbolEntry:
    """A single indexed symbol."""
    name: str
    kind: str  # "class", "struct", "function", "enum"
    file_path: str
    line: int


class SymbolIndex:
    """Scans C++ headers and builds a searchable symbol table.

    Example::

        idx = SymbolIndex("/path/to/repo/Atlas")
        idx.build()
        results = idx.search("MultiSelection")
        print(results)  # [SymbolEntry(name="MultiSelectionManager", ...)]
    """

    def __init__(self, root_path: str) -> None:
        self.root_path = Path(root_path)
        self._entries: list[SymbolEntry] = []

    def build(self, extensions: tuple = (".h", ".hpp")) -> int:
        """Scan all header files under root_path and index symbols.

        Returns:
            Number of symbols indexed.
        """
        self._entries.clear()
        for ext in extensions:
            for header in self.root_path.rglob(f"*{ext}"):
                self._index_file(header)
        logger.info("SymbolIndex: indexed %d symbols from %s", len(self._entries), self.root_path)
        return len(self._entries)

    def search(self, query: str, kind: Optional[str] = None) -> list[SymbolEntry]:
        """Return entries whose name contains query (case-insensitive).

        Args:
            query: Substring to search for.
            kind:  If provided, filter by symbol kind ("class", "function", etc.).
        """
        q = query.lower()
        results = [e for e in self._entries if q in e.name.lower()]
        if kind:
            results = [e for e in results if e.kind == kind]
        return results

    def get_by_name(self, name: str) -> Optional[SymbolEntry]:
        """Return the first entry with an exact name match, or None."""
        for entry in self._entries:
            if entry.name == name:
                return entry
        return None

    def get_all(self) -> list[SymbolEntry]:
        """Return all indexed symbol entries."""
        return list(self._entries)

    def clear(self) -> None:
        """Remove all indexed entries."""
        self._entries.clear()

    def _index_file(self, path: Path) -> None:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return
        for line_no, line in enumerate(text.splitlines(), start=1):
            for pattern, kind in [
                (_CLASS_RE, "class"),
                (_STRUCT_RE, "struct"),
                (_ENUM_RE, "enum"),
            ]:
                for m in pattern.finditer(line):
                    name = m.group(1)
                    if name not in ("override", "final", "default", "delete"):
                        self._entries.append(
                            SymbolEntry(name=name, kind=kind, file_path=str(path), line=line_no)
                        )
