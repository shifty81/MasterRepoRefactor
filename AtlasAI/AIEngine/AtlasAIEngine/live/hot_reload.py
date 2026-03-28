"""AtlasAI Phase 13 — Hot-Reload Coordinator.

Implements the ``supportsLivePatch`` capability: watches source paths for
changes and queues patches that can be applied to a running process without
a full restart.
"""
from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class HotReloadConfig:
    watch_paths: list[str]
    debounce_ms: int = 200


@dataclass
class _PendingPatch:
    path: str
    content: str
    queued_at: float = field(default_factory=time.monotonic)


class HotReloadCoordinator:
    """Coordinates live-patch delivery for the ``supportsLivePatch`` capability.

    Usage::

        config = HotReloadConfig(watch_paths=["src/", "lib/"])
        coordinator = HotReloadCoordinator(config)
        coordinator.start()

        # Engine pushes a patch when it detects a change:
        coordinator.add_patch("src/foo.py", new_source)

        patches = coordinator.get_pending_patches()
        # … apply patches …

        coordinator.stop()
    """

    def __init__(self, config: HotReloadConfig) -> None:
        self._config = config
        self._patches: list[_PendingPatch] = []
        self._lock = threading.Lock()
        self._running = False
        self._watcher_thread: threading.Thread | None = None

    # ── lifecycle ──────────────────────────────────────────────────────────

    def start(self) -> None:
        """Begin watching ``config.watch_paths`` for changes."""
        if self._running:
            return
        self._running = True
        self._watcher_thread = threading.Thread(
            target=self._watch_loop, daemon=True, name="hot-reload-watcher"
        )
        self._watcher_thread.start()
        logger.info(
            "HotReloadCoordinator: started watching %s (debounce=%dms)",
            self._config.watch_paths,
            self._config.debounce_ms,
        )

    def stop(self) -> None:
        """Stop the watcher and discard any pending patches."""
        if not self._running:
            return
        self._running = False
        if self._watcher_thread is not None:
            self._watcher_thread.join(timeout=2.0)
            self._watcher_thread = None
        with self._lock:
            self._patches.clear()
        logger.info("HotReloadCoordinator: stopped")

    # ── patch management ───────────────────────────────────────────────────

    def add_patch(self, path: str, content: str) -> bool:
        """Queue a live patch for *path* with the given *content*.

        Duplicate patches for the same path replace the previous entry so only
        the latest content is applied after the debounce window.

        Args:
            path:    Path of the file being patched (relative or absolute).
            content: New source content to apply.

        Returns:
            ``True`` if the patch was queued successfully.
        """
        if not path or not self._running:
            return False
        with self._lock:
            # Replace any existing pending patch for the same path.
            self._patches = [p for p in self._patches if p.path != path]
            self._patches.append(_PendingPatch(path=path, content=content))
        logger.debug("HotReloadCoordinator: queued patch for %s", path)
        return True

    def get_pending_patches(self) -> list[dict]:
        """Return all patches that have passed the debounce window.

        Consumed patches are removed from the queue.

        Returns:
            List of ``{"path": str, "content": str}`` dicts ready to apply.
        """
        debounce_s = self._config.debounce_ms / 1000.0
        cutoff = time.monotonic() - debounce_s
        ready: list[_PendingPatch] = []
        with self._lock:
            still_pending: list[_PendingPatch] = []
            for patch in self._patches:
                if patch.queued_at <= cutoff:
                    ready.append(patch)
                else:
                    still_pending.append(patch)
            self._patches = still_pending
        return [{"path": p.path, "content": p.content} for p in ready]

    # ── internal ───────────────────────────────────────────────────────────

    def _watch_loop(self) -> None:
        """Background thread stub — a real implementation would use inotify /
        FSEvents / ReadDirectoryChangesW to detect file-system events and call
        :meth:`add_patch` automatically."""
        while self._running:
            time.sleep(self._config.debounce_ms / 1000.0)
