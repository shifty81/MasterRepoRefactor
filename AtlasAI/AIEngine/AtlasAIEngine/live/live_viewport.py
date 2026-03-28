"""AtlasAI Phase 13 — Live Viewport Client.

Implements the ``supportsViewportAttach`` capability: establishes a
connection to a running IDE viewport so AtlasAI can push live snapshots
(e.g. rendered UI frames, diagnostic overlays) without a full reload.
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class LiveViewportConfig:
    host: str
    port: int
    capability: str = "supportsViewportAttach"


class LiveViewportClient:
    """Client that attaches to a live IDE viewport over an async channel.

    All network calls are stubbed — real transport is wired up by the
    host process that embeds this engine.
    """

    def __init__(self, config: LiveViewportConfig) -> None:
        self._config = config
        self._connected: bool = False
        self._loop: asyncio.AbstractEventLoop | None = None

    # ── connection lifecycle ───────────────────────────────────────────────

    def connect(self) -> bool:
        """Attempt to attach to the viewport.  Returns ``True`` on success."""
        logger.debug(
            "LiveViewportClient: connecting to %s:%d (capability=%s)",
            self._config.host,
            self._config.port,
            self._config.capability,
        )
        # Stub: a real implementation would open a WebSocket / named-pipe here.
        self._connected = True
        self._loop = asyncio.new_event_loop()
        logger.info(
            "LiveViewportClient: attached to %s:%d",
            self._config.host,
            self._config.port,
        )
        return self._connected

    def disconnect(self) -> None:
        """Detach from the viewport and release resources."""
        if not self._connected:
            return
        logger.debug("LiveViewportClient: disconnecting")
        self._connected = False
        if self._loop is not None:
            self._loop.close()
            self._loop = None

    # ── data transfer ──────────────────────────────────────────────────────

    def send_snapshot(self, data: dict) -> bool:
        """Push a snapshot payload to the viewport.

        Args:
            data: Arbitrary dict describing the snapshot (frame id, pixels,
                  diagnostics, etc.).

        Returns:
            ``True`` if the snapshot was accepted, ``False`` otherwise.
        """
        if not self._connected:
            logger.warning("LiveViewportClient.send_snapshot: not connected")
            return False
        # Stub: serialize and dispatch over the transport channel.
        logger.debug("LiveViewportClient: sending snapshot keys=%s", list(data.keys()))
        return True

    # ── status ─────────────────────────────────────────────────────────────

    def is_connected(self) -> bool:
        """Return ``True`` when the viewport channel is active."""
        return self._connected
