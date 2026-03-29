"""AtlasAI Phase 17A — Dev AI Phase 3: In-Editor Overlay Manager.

Coordinates the four overlay panels (AIPromptPanel, AISuggestionPanel,
AIBuildLogPanel, AIContextPanel) from the Python bridge side, routing
agent output to the appropriate panel via the WebSocket event relay.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, Optional

logger = logging.getLogger(__name__)


@dataclass
class OverlayState:
    """Current state snapshot for all overlay panels."""
    active_file: str = ""
    model_status: str = "idle"
    build_log_lines: list = field(default_factory=list)
    symbols: list = field(default_factory=list)
    pending_diff: str = ""


class OverlayManager:
    """Routes Dev AI agent output to the correct IDE overlay panel.

    Example::

        mgr = OverlayManager()
        mgr.push_build_line("CMake: -- Build files written to /build")
        mgr.push_suggestion("--- a/foo.cpp\\n+++ b/foo.cpp\\n@@ -1 +1 @@ ...")
        mgr.approve_suggestion()  # returns True
    """

    def __init__(self) -> None:
        self._state = OverlayState()
        self._on_state_change: Optional[Callable[[OverlayState], None]] = None

    # ── build log ─────────────────────────────────────────────────────────

    def push_build_line(self, line: str) -> None:
        """Append a line to the build log panel."""
        self._state.build_log_lines.append(line)
        logger.debug("BuildLog: %s", line)
        self._notify()

    def clear_build_log(self) -> None:
        """Clear all build log lines."""
        self._state.build_log_lines.clear()
        self._notify()

    # ── suggestion / diff ─────────────────────────────────────────────────

    def push_suggestion(self, diff_text: str) -> None:
        """Surface a unified diff as a pending suggestion."""
        self._state.pending_diff = diff_text
        logger.info("OverlayManager: new suggestion (%d chars)", len(diff_text))
        self._notify()

    def approve_suggestion(self) -> bool:
        """Approve the pending suggestion. Returns True if there was one."""
        if not self._state.pending_diff:
            return False
        logger.info("OverlayManager: suggestion approved")
        self._state.pending_diff = ""
        self._notify()
        return True

    def reject_suggestion(self) -> bool:
        """Reject the pending suggestion. Returns True if there was one."""
        if not self._state.pending_diff:
            return False
        logger.info("OverlayManager: suggestion rejected")
        self._state.pending_diff = ""
        self._notify()
        return True

    # ── context ───────────────────────────────────────────────────────────

    def set_active_file(self, file_path: str) -> None:
        """Update the active file shown in the context panel."""
        self._state.active_file = file_path
        self._notify()

    def set_model_status(self, status: str) -> None:
        """Update the model backend status (e.g. 'idle', 'generating', 'error')."""
        self._state.model_status = status
        self._notify()

    def add_symbol(self, symbol: str) -> None:
        """Add a symbol to the context panel's in-scope list."""
        if symbol not in self._state.symbols:
            self._state.symbols.append(symbol)
        self._notify()

    def clear_symbols(self) -> None:
        """Clear all symbols from the context panel."""
        self._state.symbols.clear()
        self._notify()

    # ── state ─────────────────────────────────────────────────────────────

    def get_state(self) -> OverlayState:
        """Return a copy of the current overlay state."""
        return self._state

    def set_on_state_change(self, cb: Callable[[OverlayState], None]) -> None:
        """Register a callback invoked whenever overlay state changes."""
        self._on_state_change = cb

    def _notify(self) -> None:
        if self._on_state_change:
            self._on_state_change(self._state)
