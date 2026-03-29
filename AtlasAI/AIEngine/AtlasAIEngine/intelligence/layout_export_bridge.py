"""AtlasAI Phase 19B — Layout Export Bridge.

Converts in-memory PCG layouts (lists of PlacementRecord objects or raw
position dicts) into runtime-consumable JSON formats that can be loaded
directly by the NovaForge content pipeline.
"""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class LayoutEntry:
    """A single entity entry in an exported layout."""

    entity_id: str
    entity_type: str
    x: float
    y: float
    z: float
    rotation_y: float = 0.0
    pcg_seed: Optional[int] = None
    metadata: Optional[dict] = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


class LayoutExportBridge:
    """Accumulate layout entries and export to runtime JSON.

    Designed to sit at the boundary between the editor placement layer and
    the NovaForge content loader.  The exported format mirrors the structure
    expected by ``NovaForge/Content`` scene descriptors.

    Example::

        bridge = LayoutExportBridge("layout_001", version="1.0")
        bridge.add_entry("ent_01", "Planet", 0.0, 0.0, 1.0)
        bridge.add_entry("ent_02", "Station", 0.0, 0.0, 1.2)
        bridge.export("/repo/NovaForge/Content/Data/Layouts/layout_001.json")
    """

    def __init__(self, layout_id: str, version: str = "1.0") -> None:
        self.layout_id = layout_id
        self.version = version
        self._entries: list[LayoutEntry] = []

    # ------------------------------------------------------------------
    # Entry management
    # ------------------------------------------------------------------

    def add_entry(
        self,
        entity_id: str,
        entity_type: str,
        x: float,
        y: float,
        z: float,
        rotation_y: float = 0.0,
        pcg_seed: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> LayoutEntry:
        """Add a new entity entry to the layout."""
        entry = LayoutEntry(
            entity_id=entity_id,
            entity_type=entity_type,
            x=x,
            y=y,
            z=z,
            rotation_y=rotation_y,
            pcg_seed=pcg_seed,
            metadata=dict(metadata or {}),
        )
        self._entries.append(entry)
        logger.debug("LayoutExportBridge: added entry %s (%s)", entity_id, entity_type)
        return entry

    def remove_entry(self, entity_id: str) -> bool:
        """Remove the entry with the given entity_id.  Returns True if found."""
        before = len(self._entries)
        self._entries = [e for e in self._entries if e.entity_id != entity_id]
        return len(self._entries) < before

    def get_entry_count(self) -> int:
        """Return the number of entries in this layout."""
        return len(self._entries)

    def get_entries_by_type(self, entity_type: str) -> list[LayoutEntry]:
        """Return all entries of the given entity type."""
        return [e for e in self._entries if e.entity_type == entity_type]

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Return the layout as a plain Python dict (exportable to JSON)."""
        return {
            "layout_id": self.layout_id,
            "version": self.version,
            "entry_count": len(self._entries),
            "entries": [
                {
                    "entity_id": e.entity_id,
                    "entity_type": e.entity_type,
                    "position": {"x": e.x, "y": e.y, "z": e.z},
                    "rotation_y": e.rotation_y,
                    "pcg_seed": e.pcg_seed,
                    "metadata": e.metadata,
                }
                for e in self._entries
            ],
        }

    def export(self, path: str) -> bool:
        """Write the layout to *path* as a JSON file.  Returns True on success."""
        try:
            out = Path(path)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(self.to_dict(), indent=2))
            logger.info("LayoutExportBridge: exported %d entries to %s",
                        len(self._entries), path)
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("LayoutExportBridge export failed: %s", exc)
            return False

    def load(self, path: str) -> int:
        """Load entries from a previously exported JSON file.
        Returns the number of entries loaded, or 0 on failure."""
        try:
            data = json.loads(Path(path).read_text())
            entries = data.get("entries", [])
            for raw in entries:
                pos = raw.get("position", {})
                self.add_entry(
                    entity_id=raw["entity_id"],
                    entity_type=raw["entity_type"],
                    x=pos.get("x", 0.0),
                    y=pos.get("y", 0.0),
                    z=pos.get("z", 0.0),
                    rotation_y=raw.get("rotation_y", 0.0),
                    pcg_seed=raw.get("pcg_seed"),
                    metadata=raw.get("metadata", {}),
                )
            return len(entries)
        except Exception as exc:  # pragma: no cover
            logger.error("LayoutExportBridge load failed: %s", exc)
            return 0

    def clear(self) -> None:
        """Remove all entries."""
        self._entries.clear()
