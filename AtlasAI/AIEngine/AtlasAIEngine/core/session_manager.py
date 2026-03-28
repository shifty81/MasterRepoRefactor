"""session_manager.py — Workspace session lifecycle management for AtlasAI."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from core.logger import get_logger

logger = get_logger(__name__)


class SessionState(str, Enum):
    DISCONNECTED = "disconnected"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class Session:
    """Represents a single AtlasAI workspace session."""

    def __init__(self, session_id: str, project_id: str, client_id: str) -> None:
        self.session_id   = session_id
        self.project_id   = project_id
        self.client_id    = client_id
        self.state        = SessionState.ACTIVE
        self.created_at   = datetime.now(timezone.utc).isoformat()
        self.last_active  = self.created_at

    def touch(self) -> None:
        """Update last-active timestamp."""
        self.last_active = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return {
            "session_id":  self.session_id,
            "project_id":  self.project_id,
            "client_id":   self.client_id,
            "state":       self.state.value,
            "created_at":  self.created_at,
            "last_active": self.last_active,
        }


class SessionManager:
    """Manages lifecycle of AtlasAI workspace sessions."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    # ------------------------------------------------------------------
    # Creation / termination
    # ------------------------------------------------------------------

    def create_session(self, project_id: str, client_id: str) -> Session:
        """Create and register a new active session."""
        session_id = str(uuid.uuid4())
        session = Session(session_id, project_id, client_id)
        self._sessions[session_id] = session
        logger.debug("Session created: %s (project=%s)", session_id, project_id)
        return session

    def terminate_session(self, session_id: str) -> bool:
        """Terminate a session by ID. Returns True if found."""
        session = self._sessions.get(session_id)
        if session is None:
            return False
        session.state = SessionState.TERMINATED
        logger.debug("Session terminated: %s", session_id)
        return True

    def suspend_session(self, session_id: str) -> bool:
        """Suspend an active session. Returns True if transition succeeded."""
        session = self._sessions.get(session_id)
        if session is None or session.state != SessionState.ACTIVE:
            return False
        session.state = SessionState.SUSPENDED
        return True

    def resume_session(self, session_id: str) -> bool:
        """Resume a suspended session. Returns True if transition succeeded."""
        session = self._sessions.get(session_id)
        if session is None or session.state != SessionState.SUSPENDED:
            return False
        session.state = SessionState.ACTIVE
        session.touch()
        return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_session(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)

    def list_active(self) -> list[Session]:
        return [s for s in self._sessions.values() if s.state == SessionState.ACTIVE]

    def list_all(self) -> list[Session]:
        return list(self._sessions.values())

    def count_active(self) -> int:
        return sum(1 for s in self._sessions.values() if s.state == SessionState.ACTIVE)
