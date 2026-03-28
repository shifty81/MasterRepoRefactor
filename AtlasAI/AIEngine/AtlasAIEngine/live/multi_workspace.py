"""AtlasAI Phase 13 — Multi-Workspace Session Manager.

Tracks multiple concurrent project workspaces, each with its own bridge
port and lifecycle state, so AtlasAI can serve several IDE windows
simultaneously.
"""
from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class WorkspaceSession:
    session_id: str
    project_path: str
    bridge_port: int
    active: bool = True


class MultiWorkspaceManager:
    """Manages a pool of :class:`WorkspaceSession` objects.

    Each session represents one open project.  Session IDs are random
    UUID4 strings so they are safe to use as dict keys or URL path segments.

    Example::

        manager = MultiWorkspaceManager()
        session = manager.create_session("/home/user/myproject", port=8765)
        print(session.session_id)

        same = manager.get_session(session.session_id)
        manager.close_session(session.session_id)
    """

    def __init__(self) -> None:
        self._sessions: dict[str, WorkspaceSession] = {}

    # ── session lifecycle ──────────────────────────────────────────────────

    def create_session(self, project_path: str, port: int) -> WorkspaceSession:
        """Create and register a new workspace session.

        Args:
            project_path: Absolute path of the project root.
            port:         Bridge port this session will listen on.

        Returns:
            The newly created :class:`WorkspaceSession`.
        """
        session_id = str(uuid.uuid4())
        session = WorkspaceSession(
            session_id=session_id,
            project_path=project_path,
            bridge_port=port,
        )
        self._sessions[session_id] = session
        logger.info(
            "MultiWorkspaceManager: created session %s for %s on port %d",
            session_id,
            project_path,
            port,
        )
        return session

    def get_session(self, session_id: str) -> Optional[WorkspaceSession]:
        """Look up a session by its ID.

        Returns:
            The :class:`WorkspaceSession` if found, otherwise ``None``.
        """
        return self._sessions.get(session_id)

    def list_sessions(self) -> list[WorkspaceSession]:
        """Return all registered sessions (active and inactive)."""
        return list(self._sessions.values())

    def close_session(self, session_id: str) -> bool:
        """Mark a session as inactive and remove it from the pool.

        Args:
            session_id: ID of the session to close.

        Returns:
            ``True`` if the session existed and was closed, ``False`` if the
            session ID was not found.
        """
        session = self._sessions.pop(session_id, None)
        if session is None:
            logger.warning(
                "MultiWorkspaceManager.close_session: unknown session %s", session_id
            )
            return False
        session.active = False
        logger.info("MultiWorkspaceManager: closed session %s", session_id)
        return True
