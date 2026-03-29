"""AtlasAI Phase 18D — DeltaEdits persistence store.

Records, stores, and queries delta edits — incremental changes made to
scene entities — enabling propagation, merging, and rollback.
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class DeltaEdit:
    """A single incremental edit to a scene entity property."""
    edit_id: str
    entity_id: str
    property_name: str
    old_value: object
    new_value: object
    timestamp: float = field(default_factory=time.time)
    session_id: str = "default"
    committed: bool = False


class DeltaEditStore:
    """In-memory (+ optional JSON persistence) store for DeltaEdits.

    Example::

        store = DeltaEditStore()
        eid = store.record("ent_001", "position.x", 0.0, 100.0)
        store.commit(eid)
        edits = store.get_committed()
        store.save("/tmp/delta_edits.json")
    """

    def __init__(self) -> None:
        self._edits: dict[str, DeltaEdit] = {}
        self._next_id = 0

    def record(self, entity_id: str, property_name: str,
               old_value: object, new_value: object,
               session_id: str = "default") -> str:
        """Record a new delta edit. Returns the edit ID."""
        eid = f"edit_{self._next_id:05d}"
        self._next_id += 1
        self._edits[eid] = DeltaEdit(
            edit_id=eid,
            entity_id=entity_id,
            property_name=property_name,
            old_value=old_value,
            new_value=new_value,
            session_id=session_id,
        )
        logger.debug("DeltaEditStore: recorded %s → %s.%s", eid, entity_id, property_name)
        return eid

    def commit(self, edit_id: str) -> bool:
        """Mark an edit as committed. Returns True if found."""
        edit = self._edits.get(edit_id)
        if edit is None:
            return False
        edit.committed = True
        logger.info("DeltaEditStore: committed %s", edit_id)
        return True

    def rollback(self, edit_id: str) -> bool:
        """Remove an uncommitted edit. Returns True if removed."""
        edit = self._edits.get(edit_id)
        if edit is None or edit.committed:
            return False
        del self._edits[edit_id]
        logger.info("DeltaEditStore: rolled back %s", edit_id)
        return True

    def get_committed(self) -> list[DeltaEdit]:
        """Return all committed edits."""
        return [e for e in self._edits.values() if e.committed]

    def get_pending(self) -> list[DeltaEdit]:
        """Return all uncommitted (pending) edits."""
        return [e for e in self._edits.values() if not e.committed]

    def get_by_entity(self, entity_id: str) -> list[DeltaEdit]:
        """Return all edits for a specific entity ID."""
        return [e for e in self._edits.values() if e.entity_id == entity_id]

    def save(self, path: str) -> bool:
        """Persist all edits to a JSON file. Returns True on success."""
        try:
            data = [
                {
                    "edit_id": e.edit_id,
                    "entity_id": e.entity_id,
                    "property_name": e.property_name,
                    "old_value": e.old_value,
                    "new_value": e.new_value,
                    "timestamp": e.timestamp,
                    "session_id": e.session_id,
                    "committed": e.committed,
                }
                for e in self._edits.values()
            ]
            Path(path).write_text(json.dumps(data, indent=2))
            logger.info("DeltaEditStore: saved %d edits → %s", len(data), path)
            return True
        except OSError as exc:
            logger.error("DeltaEditStore: save failed: %s", exc)
            return False

    def load(self, path: str) -> int:
        """Load edits from a JSON file. Returns number loaded."""
        try:
            raw = json.loads(Path(path).read_text())
        except (OSError, json.JSONDecodeError) as exc:
            logger.error("DeltaEditStore: load failed: %s", exc)
            return 0
        for item in raw:
            edit = DeltaEdit(
                edit_id=item["edit_id"],
                entity_id=item["entity_id"],
                property_name=item["property_name"],
                old_value=item["old_value"],
                new_value=item["new_value"],
                timestamp=item.get("timestamp", 0.0),
                session_id=item.get("session_id", "default"),
                committed=item.get("committed", False),
            )
            self._edits[edit.edit_id] = edit
        logger.info("DeltaEditStore: loaded %d edits from %s", len(raw), path)
        return len(raw)

    def clear(self) -> None:
        """Remove all edits."""
        self._edits.clear()

    def get_stats(self) -> dict:
        """Return summary statistics."""
        total = len(self._edits)
        committed = sum(1 for e in self._edits.values() if e.committed)
        return {
            "total": total,
            "committed": committed,
            "pending": total - committed,
        }
