"""AtlasAI Phase 19D — Scene Graph Snapshot Utility.

Reads a scene snapshot JSON file (exported by the C++ SceneQueryBridge)
and surfaces it as a queryable in-memory representation via SceneQueryEngine.
Also supports diffing two snapshots to detect entity additions/removals/moves.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .scene_query_engine import SceneQueryEngine, SceneEntityRecord

logger = logging.getLogger(__name__)


@dataclass
class SnapshotDiff:
    """Difference between two scene graph snapshots."""

    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    moved: list[str] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not (self.added or self.removed or self.moved)

    def total_changes(self) -> int:
        return len(self.added) + len(self.removed) + len(self.moved)


class SceneGraphSnapshot:
    """Load, query and diff scene graph snapshots.

    A snapshot is a JSON file produced by ``SceneQueryBridge::ExportToFile()``
    on the C++ side.  This class parses that file and feeds the entities into
    a ``SceneQueryEngine`` instance so that the full query API is available
    without a live engine connection.

    Example::

        snap = SceneGraphSnapshot.from_file("/tmp/scene_snap.json")
        planets = snap.engine.query_by_type("Planet")
        diff = SceneGraphSnapshot.diff(snap_before, snap_after)
        print(diff.added)
    """

    def __init__(self, system_id: str = "") -> None:
        self.system_id: str = system_id
        self.engine: SceneQueryEngine = SceneQueryEngine()
        self._raw: list[dict] = []

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    @classmethod
    def from_file(cls, path: str) -> "SceneGraphSnapshot":
        """Load a snapshot from a JSON file.  Returns an empty snapshot on error."""
        snap = cls()
        try:
            data = json.loads(Path(path).read_text())
            snap.system_id = data.get("system_id", "")
            snap._load_entities(data.get("entities", []))
        except Exception as exc:  # pragma: no cover
            logger.error("SceneGraphSnapshot.from_file failed: %s", exc)
        return snap

    @classmethod
    def from_dict(cls, data: dict) -> "SceneGraphSnapshot":
        """Construct a snapshot from a pre-parsed dict."""
        snap = cls()
        snap.system_id = data.get("system_id", "")
        snap._load_entities(data.get("entities", []))
        return snap

    def _load_entities(self, entities: list[dict]) -> None:
        self._raw = list(entities)
        for raw in entities:
            self.engine.register(
                entity_id=raw["entity_id"],
                entity_type=raw["entity_type"],
                x=raw.get("x", 0.0),
                y=raw.get("y", 0.0),
                z=raw.get("z", 0.0),
                tags=raw.get("tags", []),
                properties=raw.get("properties", {}),
            )
        logger.debug(
            "SceneGraphSnapshot: loaded %d entities for system '%s'",
            len(entities),
            self.system_id,
        )

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Serialise snapshot back to a dict (round-trippable)."""
        return {
            "system_id": self.system_id,
            "entity_count": self.engine.get_entity_count(),
            "entities": self._raw,
        }

    def save(self, path: str) -> bool:
        """Write the snapshot to *path*.  Returns True on success."""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(json.dumps(self.to_dict(), indent=2))
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("SceneGraphSnapshot.save failed: %s", exc)
            return False

    # ------------------------------------------------------------------
    # Diffing
    # ------------------------------------------------------------------

    @staticmethod
    def diff(before: "SceneGraphSnapshot",
             after: "SceneGraphSnapshot") -> SnapshotDiff:
        """Compute the entity-level diff between two snapshots."""
        before_ids = {
            e.entity_id: e
            for e in before.engine.query(lambda _: True)
        }
        after_ids = {
            e.entity_id: e
            for e in after.engine.query(lambda _: True)
        }

        added = [eid for eid in after_ids if eid not in before_ids]
        removed = [eid for eid in before_ids if eid not in after_ids]

        _EPSILON = 1e-4
        moved = []
        for eid in before_ids:
            if eid not in after_ids:
                continue
            b = before_ids[eid]
            a = after_ids[eid]
            if (abs(a.x - b.x) > _EPSILON or
                    abs(a.y - b.y) > _EPSILON or
                    abs(a.z - b.z) > _EPSILON):
                moved.append(eid)

        return SnapshotDiff(added=added, removed=removed, moved=moved)

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def get_entity_count(self) -> int:
        return self.engine.get_entity_count()
