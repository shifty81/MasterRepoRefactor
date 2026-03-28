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
    """Walk upward from *start* to find the repository root (contains CMakeLists.txt)."""
    candidate = (start or Path(__file__).resolve()).parent
    for _ in range(_MAX_REPO_TRAVERSAL_DEPTH):
        if (candidate / "CMakeLists.txt").exists():
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
    """Return a logger that writes to console and a rotating file.

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
    """
    logger = logging.getLogger(name)
    # Only add handlers the first time this subsystem is configured
    if subsystem not in _initialised:
        _initialised.add(subsystem)
        root_logger = logging.getLogger(subsystem)
        root_logger.setLevel(level)

        formatter = logging.Formatter(_LOG_FORMAT, datefmt=_LOG_DATE_FMT)

        # ── Console handler ───────────────────────────────────────────────────
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # ── File handler (rotating) ───────────────────────────────────────────
        try:
            repo_root = _find_repo_root()
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
            root_logger.addHandler(file_handler)
        except OSError:
            # If we can't write the log file (e.g. read-only filesystem in CI),
            # continue with console-only logging.
            pass

    logger.setLevel(level)
    return logger
