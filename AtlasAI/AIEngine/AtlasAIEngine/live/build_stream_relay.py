"""Phase 13 — Build Stream Relay.

Relays real-time build events from the PythonBridge to connected WebSocket
clients so the Atlas IDE can stream build output without polling.
"""
from __future__ import annotations

import logging
import threading
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import Callable

logger = logging.getLogger(__name__)


@dataclass
class BuildEvent:
    event_type: str
    message: str
    severity: str = "info"
    timestamp: float = field(default_factory=time.time)


class BuildStreamRelay:
    """Relays build events to registered subscriber callbacks.

    Subscribers receive every :class:`BuildEvent` published after they
    subscribe.  A bounded history ring-buffer lets late-joiners catch up.

    Usage::

        relay = BuildStreamRelay(max_history=200)

        def on_event(evt: BuildEvent) -> None:
            print(evt.event_type, evt.message)

        sub_id = relay.subscribe(on_event)
        relay.publish("compile", "Building foo.py …")
        relay.unsubscribe(sub_id)
    """

    def __init__(self, max_history: int = 200) -> None:
        self._max_history = max_history
        self._history: deque[BuildEvent] = deque(maxlen=max_history)
        self._subscribers: dict[str, Callable[[BuildEvent], None]] = {}
        self._lock = threading.Lock()

    # ── publishing ─────────────────────────────────────────────────────────

    def publish(
        self, event_type: str, message: str, severity: str = "info"
    ) -> BuildEvent:
        """Create a :class:`BuildEvent`, store it in history, and fan out to subscribers.

        Args:
            event_type: Short label for the event category (e.g. ``"compile"``,
                        ``"error"``, ``"success"``).
            message:    Human-readable description of the build event.
            severity:   One of ``"info"``, ``"warning"``, or ``"error"``.

        Returns:
            The newly created :class:`BuildEvent`.
        """
        event = BuildEvent(event_type=event_type, message=message, severity=severity)
        with self._lock:
            self._history.append(event)
            callbacks = list(self._subscribers.values())

        logger.debug(
            "BuildStreamRelay: publish event_type=%s severity=%s subscribers=%d",
            event_type,
            severity,
            len(callbacks),
        )
        for callback in callbacks:
            try:
                callback(event)
            except Exception:
                logger.exception(
                    "BuildStreamRelay: subscriber callback raised an exception"
                )
        return event

    # ── subscription management ────────────────────────────────────────────

    def subscribe(self, callback: Callable[[BuildEvent], None]) -> str:
        """Register *callback* to receive future :class:`BuildEvent` objects.

        Args:
            callback: Callable that accepts a single :class:`BuildEvent`.

        Returns:
            A unique ``subscriber_id`` string used to unsubscribe later.
        """
        subscriber_id = str(uuid.uuid4())
        with self._lock:
            self._subscribers[subscriber_id] = callback
        logger.debug(
            "BuildStreamRelay: registered subscriber id=%s total=%d",
            subscriber_id,
            len(self._subscribers),
        )
        return subscriber_id

    def unsubscribe(self, subscriber_id: str) -> bool:
        """Remove the subscriber identified by *subscriber_id*.

        Args:
            subscriber_id: ID returned by a previous :meth:`subscribe` call.

        Returns:
            ``True`` if the subscriber was found and removed, ``False`` if the
            ID was unknown.
        """
        with self._lock:
            if subscriber_id not in self._subscribers:
                return False
            del self._subscribers[subscriber_id]
        logger.debug(
            "BuildStreamRelay: unregistered subscriber id=%s", subscriber_id
        )
        return True

    # ── history ────────────────────────────────────────────────────────────

    def get_history(self, limit: int = 50) -> list[BuildEvent]:
        """Return the most recent build events from the history buffer.

        Args:
            limit: Maximum number of events to return (capped at
                   ``max_history``).

        Returns:
            List of :class:`BuildEvent` objects, oldest first.
        """
        with self._lock:
            events = list(self._history)
        return events[-limit:] if limit < len(events) else events

    def clear_history(self) -> None:
        """Discard all events from the history buffer."""
        with self._lock:
            self._history.clear()
        logger.debug("BuildStreamRelay: history cleared")

    # ── status ─────────────────────────────────────────────────────────────

    def subscriber_count(self) -> int:
        """Return the number of currently registered subscribers."""
        with self._lock:
            return len(self._subscribers)
