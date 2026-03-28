"""Shared logging utilities for MasterRepo tools and scripts.

Provides a lightweight ``get_tool_logger()`` factory that any Python tool in
the repository can import without depending on the AtlasAI engine packages.
Output goes simultaneously to the console (stdout) and a rotating log file
under ``<repo_root>/Logs/<subsystem>/``.

Usage::

    from Shared.Logging.log_utils import get_tool_logger
    logger = get_tool_logger(__name__)
    logger.info("Starting validation …")

Or, when running a script directly from any directory::

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[N]))  # N = depth to repo root
    from Shared.Logging.log_utils import get_tool_logger
"""
from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path

_LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
_LOG_DATE_FMT = "%Y-%m-%d %H:%M:%S"
_LOG_MAX_BYTES = 5 * 1024 * 1024   # 5 MB
_LOG_BACKUP_COUNT = 5

_MAX_REPO_TRAVERSAL_DEPTH = 8

# Track which subsystems have already been initialised to avoid duplicate handlers
_initialised: set[str] = set()


def _find_repo_root(start: Path | None = None) -> Path:
    """Walk upward from *start* to find the repository root.

    The root is identified by the presence of a ``LICENSE`` file, which exists
    only at the repository root (not in any sub-library directories that also
    carry their own ``CMakeLists.txt``).  Falls back to the explicit relative
    path from this file's known location if not found.
    """
    candidate = (start or Path(__file__).resolve()).parent
    for _ in range(_MAX_REPO_TRAVERSAL_DEPTH):
        if (candidate / "LICENSE").exists():
            return candidate
        parent = candidate.parent
        if parent == candidate:
            break
        candidate = parent
    # Fallback: three levels above Shared/Logging/log_utils.py → repo root
    return Path(__file__).resolve().parents[2]


def get_tool_logger(
    name: str,
    subsystem: str = "tools",
    level: int = logging.DEBUG,
) -> logging.Logger:
    """Return a logger that writes to console, a rotating subsystem file, and a root debug log.

    Parameters
    ----------
    name:
        Logger name — typically ``__name__`` of the calling module.
    subsystem:
        Subdirectory under ``<repo_root>/Logs/`` where the log file is placed.
        Defaults to ``"tools"``.
    level:
        Minimum logging level (default: ``logging.DEBUG``).

    Returns
    -------
    logging.Logger
        Configured logger instance.

    Notes
    -----
    Handlers are attached directly to the named logger (not a separate
    subsystem root logger) so that output is always captured regardless of
    whether the caller's module name is a child of *subsystem* in the
    logging hierarchy.  The guard key is ``name`` so multiple callers inside
    the same module never duplicate handlers.

    In addition to the per-subsystem rotating log file, a flat ``debug.log``
    is written directly to the repository root for convenient debugging
    (e.g., ``cat debug.log`` at the root to see all tool output at once).
    """
    logger = logging.getLogger(name)
    # Only add handlers once per unique logger name
    if name not in _initialised:
        _initialised.add(name)
        logger.setLevel(level)
        # Prevent messages from propagating to the root logger (avoids
        # duplicate console output if the root logger has its own handler).
        logger.propagate = False

        formatter = logging.Formatter(_LOG_FORMAT, datefmt=_LOG_DATE_FMT)

        # ── Console handler ───────────────────────────────────────────────────
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        try:
            repo_root = _find_repo_root()

            # ── Subsystem file handler (rotating) ────────────────────────────
            log_dir = repo_root / "Logs" / subsystem
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f"{subsystem}.log"
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=_LOG_MAX_BYTES,
                backupCount=_LOG_BACKUP_COUNT,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            # ── Root debug log (flat, append-mode) ────────────────────────────
            # Written to <repo_root>/debug.log so all Python tool output is
            # visible in one place without navigating into Logs/ subdirectories.
            root_log_file = repo_root / "debug.log"
            root_handler = logging.FileHandler(
                root_log_file,
                mode="a",
                encoding="utf-8",
            )
            root_handler.setFormatter(formatter)
            logger.addHandler(root_handler)

        except OSError:
            # If we can't write the log file (e.g. read-only filesystem in CI),
            # continue with console-only logging.
            pass

    logger.setLevel(level)
    return logger
