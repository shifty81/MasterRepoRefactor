#!/usr/bin/env python3
"""validate_root.py — Enforce the root-level file contract.

Any file or directory at repository root that is not in the ALLOWLIST causes
this script to fail.  This is the CI gate that enforces the intake policy.

Rules documented in: Docs/Architecture/intake_policy.md

Exit codes:
  0 — root is clean
  1 — one or more violations found
  2 — usage error
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(REPO_ROOT))
from Shared.Logging.log_utils import get_tool_logger
logger = get_tool_logger(__name__, subsystem="validate")

# ---------------------------------------------------------------------------
# Allowlist — the ONLY items permitted at repository root.
# To add a new top-level item: update this set AND Docs/Architecture/monorepo_layout.md
# AND Docs/Architecture/intake_policy.md, then open a PR for review.
# ---------------------------------------------------------------------------

ALLOWLIST: set[str] = {
    # Zone directories
    "Atlas",
    "AtlasAI",
    "NovaForge",
    "Shared",
    "Services",
    "Tools",
    "ThirdParty",
    "Tests",
    "Scripts",
    "Docs",
    "cmake",
    # Staging / intake
    "Intake",
    "DropBox",
    # Build output (git-ignored, but may appear locally)
    "Build",
    # Log directories (tracked in git for debugging; cleared via Scripts/Logging/clear_logs.sh)
    "Logs",
    "logs",
    # Essential root files
    "CMakeLists.txt",
    "README.md",
    "LICENSE",
    ".gitignore",
    # Hidden / tool directories (not directly managed by this script)
    ".git",
    ".github",
    ".pytest_cache",
    ".venv",
    "venv",
    "env",
    # CI / editor config files (common additions)
    ".editorconfig",
    ".clang-format",
    ".clang-tidy",
    "pyproject.toml",
    "setup.cfg",
    "setup.py",
    # Debug log written by Python tools (local debugging aid; gitignored)
    "debug.log",
}


def main() -> int:
    violations: list[str] = []

    for item in sorted(REPO_ROOT.iterdir()):
        name = item.name
        # Skip hidden items not in allowlist (they are typically tool-managed)
        if name.startswith(".") and name not in ALLOWLIST:
            continue
        if name not in ALLOWLIST:
            rel = item.relative_to(REPO_ROOT)
            violations.append(str(rel))
            logger.error("Root violation: '%s' is not in the root allowlist", rel)

    if violations:
        logger.error(
            "%d root-level violation(s) found. "
            "Move items through Intake/ and run Scripts/Intake/process_intake.py.",
            len(violations),
        )
        print("\nRoot violations:")
        for v in violations:
            print(f"  {v}")
        print(
            "\nFix: move the file/folder into Intake/ then run:\n"
            "  python3 Scripts/Intake/process_intake.py"
        )
        return 1

    logger.info("validate_root: root is clean (%d item(s) checked)", len(list(REPO_ROOT.iterdir())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
