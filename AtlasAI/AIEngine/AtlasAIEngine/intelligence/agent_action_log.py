"""AtlasAI Phase 20B — Agent Action Log.

Records every action taken by the AI agent (code suggestions, approvals,
rejections, placements, queries) as structured log entries.  The log
supports sequential replay for debugging and auditing.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class ActionEntry:
    """A single agent action record."""

    action_id: str
    action_type: str
    timestamp: str
    payload: dict = field(default_factory=dict)
    result: Optional[str] = None
    success: bool = True


class AgentActionLog:
    """Append-only structured log of AI agent actions with replay support.

    Actions are appended in order and can be replayed via ``replay()``.
    The log can be persisted to / loaded from JSON for cross-session auditing.

    Example::

        log = AgentActionLog(agent_id="atlas_ai_01")
        eid = log.record("CodeSuggest", payload={"file": "foo.cpp"})
        log.set_result(eid, result="patch_applied", success=True)
        log.save("/tmp/agent_log.json")
    """

    def __init__(self, agent_id: str = "default") -> None:
        self.agent_id = agent_id
        self._entries: list[ActionEntry] = []
        self._next_id = 0

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record(
        self,
        action_type: str,
        payload: Optional[dict] = None,
        timestamp: Optional[str] = None,
    ) -> str:
        """Append a new action entry.  Returns the action_id."""
        action_id = f"action_{self._next_id:05d}"
        self._next_id += 1
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat()
        entry = ActionEntry(
            action_id=action_id,
            action_type=action_type,
            timestamp=timestamp,
            payload=dict(payload or {}),
        )
        self._entries.append(entry)
        logger.debug("AgentActionLog[%s]: recorded %s %s", self.agent_id,
                     action_type, action_id)
        return action_id

    def set_result(self, action_id: str, result: str, success: bool = True) -> bool:
        """Update the result of an existing entry.  Returns True if found."""
        for entry in self._entries:
            if entry.action_id == action_id:
                entry.result = result
                entry.success = success
                return True
        return False

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get_entry(self, action_id: str) -> Optional[ActionEntry]:
        """Return the entry with *action_id*, or None."""
        for entry in self._entries:
            if entry.action_id == action_id:
                return entry
        return None

    def get_by_type(self, action_type: str) -> list[ActionEntry]:
        """Return all entries of the given action_type."""
        return [e for e in self._entries if e.action_type == action_type]

    def get_failures(self) -> list[ActionEntry]:
        """Return all entries where success is False."""
        return [e for e in self._entries if not e.success]

    def get_entry_count(self) -> int:
        return len(self._entries)

    # ------------------------------------------------------------------
    # Replay
    # ------------------------------------------------------------------

    def replay(self, handler=None) -> list[ActionEntry]:
        """Iterate entries in insertion order.

        If *handler* is provided, calls ``handler(entry)`` for each entry
        and returns the list.  Otherwise just returns the ordered list.
        """
        for entry in self._entries:
            if handler is not None:
                handler(entry)
        return list(self._entries)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str) -> bool:
        """Persist the log to *path* as JSON.  Returns True on success."""
        try:
            data = {
                "agent_id": self.agent_id,
                "entry_count": len(self._entries),
                "entries": [
                    {
                        "action_id": e.action_id,
                        "action_type": e.action_type,
                        "timestamp": e.timestamp,
                        "payload": e.payload,
                        "result": e.result,
                        "success": e.success,
                    }
                    for e in self._entries
                ],
            }
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(json.dumps(data, indent=2))
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("AgentActionLog.save failed: %s", exc)
            return False

    def load(self, path: str) -> int:
        """Load entries from a persisted JSON log.  Returns entries loaded."""
        try:
            data = json.loads(Path(path).read_text())
            self.agent_id = data.get("agent_id", self.agent_id)
            for raw in data.get("entries", []):
                entry = ActionEntry(
                    action_id=raw["action_id"],
                    action_type=raw["action_type"],
                    timestamp=raw["timestamp"],
                    payload=raw.get("payload", {}),
                    result=raw.get("result"),
                    success=raw.get("success", True),
                )
                self._entries.append(entry)
                # keep _next_id ahead of loaded ids
                idx = int(raw["action_id"].split("_")[-1])
                if idx >= self._next_id:
                    self._next_id = idx + 1
            return len(data.get("entries", []))
        except Exception as exc:  # pragma: no cover
            logger.error("AgentActionLog.load failed: %s", exc)
            return 0

    def clear(self) -> None:
        """Remove all entries."""
        self._entries.clear()
        self._next_id = 0
