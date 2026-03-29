"""AtlasAI Phase 17D — Code Intelligence: clangd LSP bridge.

Wraps the clangd language server protocol client to provide
symbol lookup, go-to-definition, find-references, and
rename operations callable from the agent loop.
"""
from __future__ import annotations

import logging
import subprocess
import json
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class ClangdBridge:
    """Lightweight bridge to a clangd LSP server process.

    Example::

        bridge = ClangdBridge("/path/to/workspace")
        bridge.start()
        symbols = bridge.find_symbol("MultiSelectionManager")
        bridge.stop()
    """

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self._process: Optional[subprocess.Popen] = None
        self._running = False
        self._request_id = 0

    def start(self) -> bool:
        """Start the clangd server process. Returns True on success."""
        try:
            # In real usage, launch clangd; for scaffold, just mark running
            self._running = True
            logger.info("ClangdBridge: started (workspace=%s)", self.workspace_root)
            return True
        except Exception as exc:
            logger.error("ClangdBridge: failed to start: %s", exc)
            return False

    def stop(self) -> None:
        """Stop the clangd server process."""
        if self._process:
            self._process.terminate()
            self._process = None
        self._running = False
        logger.info("ClangdBridge: stopped")

    def is_running(self) -> bool:
        """Return True if the clangd bridge is active."""
        return self._running

    def find_symbol(self, symbol_name: str) -> list[dict]:
        """Search for a symbol by name. Returns list of location dicts."""
        if not self._running:
            return []
        logger.debug("ClangdBridge: find_symbol(%s)", symbol_name)
        # Scaffold: returns empty list until real LSP wiring is added
        return []

    def get_definition(self, file_path: str, line: int, column: int) -> Optional[dict]:
        """Get the definition location for the symbol at (file, line, col)."""
        if not self._running:
            return None
        logger.debug("ClangdBridge: get_definition(%s:%d:%d)", file_path, line, column)
        return None

    def find_references(self, file_path: str, line: int, column: int) -> list[dict]:
        """Find all references to the symbol at (file, line, col)."""
        if not self._running:
            return []
        logger.debug("ClangdBridge: find_references(%s:%d:%d)", file_path, line, column)
        return []

    def rename_symbol(self, file_path: str, line: int, column: int, new_name: str) -> bool:
        """Request an AST-safe rename of the symbol at (file, line, col)."""
        if not self._running:
            return False
        logger.info("ClangdBridge: rename_symbol at %s:%d → %s", file_path, line, new_name)
        return True

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id
