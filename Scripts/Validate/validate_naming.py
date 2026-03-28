#!/usr/bin/env python3
"""validate_naming.py — Check that naming conventions are respected.

Rules enforced:
- No source files should contain the legacy "Arbiter" name in their content
  (case-insensitive).
  Exceptions: files under 'New Implementations that need addressed/' and
  Docs/Archive/
- C++ files in Atlas/ should declare at least one of the allowed namespaces:
  Atlas::, NovaForge::, or Atlas::Bridge
- C# files in AtlasAI/ should use the AtlasAI.* namespace

Exit codes:
  0 — all rules pass
  1 — one or more violations found
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# ── Logging setup ─────────────────────────────────────────────────────────────
sys.path.insert(0, str(REPO_ROOT))
from Shared.Logging.log_utils import get_tool_logger
logger = get_tool_logger(__name__, subsystem="validate")

# ── Helpers ───────────────────────────────────────────────────────────────────

CPP_EXTS = (".h", ".hpp", ".hxx", ".cpp", ".cxx", ".cc")
CS_EXTS  = (".cs",)
ALL_SRC_EXTS = CPP_EXTS + CS_EXTS + (".c",)

LEGACY_NAME_RE = re.compile(r'\barbiter\b', re.IGNORECASE)

# Paths that are explicitly exempt from the legacy-name check
LEGACY_EXEMPT_SUBSTRINGS = [
    "New Implementations that need addressed",
    "Docs/Archive",
    "Docs\\Archive",
]

# Allowed namespace declarations in C++ Atlas/ files (accepts both Atlas:: and
# atlas:: conventions since source files use lowercase namespace identifiers)
ATLAS_NAMESPACE_RE = re.compile(
    r'\bnamespace\s+(atlas\b|Atlas\b|novaforge\b|NovaForge\b|atlas::Bridge\b|Atlas::Bridge\b)',
    re.IGNORECASE
)

# Allowed namespace in AtlasAI C# files
ATLASAI_CS_NAMESPACE_RE = re.compile(r'\bnamespace\s+AtlasAI\b')


def iter_files(directory: Path, extensions: tuple[str, ...]):
    if not directory.is_dir():
        return
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix in extensions:
            yield path


def is_exempt_from_legacy(path: Path) -> bool:
    path_str = path.as_posix()
    for substr in LEGACY_EXEMPT_SUBSTRINGS:
        if substr in path_str:
            return True
    return False


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []


def report_hits(violations: dict[Path, list[tuple[int, str]]], label: str) -> int:
    count = 0
    for path, hits in sorted(violations.items()):
        for lineno, text in hits:
            print(f"  {path.relative_to(REPO_ROOT)}:{lineno}: {text.strip()}")
            count += 1
    return count


# ── Rule 1: legacy "Arbiter" name check ──────────────────────────────────────

SCAN_DIRS = [
    REPO_ROOT / "Atlas",
    REPO_ROOT / "AtlasAI",
    REPO_ROOT / "NovaForge",
    REPO_ROOT / "Shared",
    REPO_ROOT / "src",
    REPO_ROOT / "tests",
    REPO_ROOT / "Tests",
]


def run_legacy_name_check() -> int:
    violations: dict[Path, list[tuple[int, str]]] = {}

    for scan_dir in SCAN_DIRS:
        for f in iter_files(scan_dir, ALL_SRC_EXTS):
            if is_exempt_from_legacy(f):
                continue
            lines = read_lines(f)
            hits = [
                (i + 1, line)
                for i, line in enumerate(lines)
                if LEGACY_NAME_RE.search(line)
            ]
            if hits:
                violations[f] = hits

    if violations:
        print("[FAIL] Legacy 'Arbiter' name found in source files:")
        return report_hits(violations, "legacy name")
    print("[PASS] Legacy name check (no 'Arbiter' references)")
    return 0


# ── Rule 2: Atlas/ C++ namespace check ───────────────────────────────────────

ATLAS_DIR = REPO_ROOT / "Atlas"


def run_atlas_namespace_check() -> int:
    bad_files: list[Path] = []

    for f in iter_files(ATLAS_DIR, CPP_EXTS):
        content = f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""
        if not content.strip():
            continue  # skip empty files
        # Skip stub files (placeholder compilation units without real namespaces)
        if "_stub" in f.name or f.name == "main.cpp":
            continue
        if not ATLAS_NAMESPACE_RE.search(content):
            bad_files.append(f)

    if bad_files:
        print("[FAIL] Atlas/ C++ files missing required namespace (Atlas::, NovaForge::, or Atlas::Bridge):")
        for f in sorted(bad_files):
            print(f"  {f.relative_to(REPO_ROOT)}")
        return len(bad_files)
    print("[PASS] Atlas/ C++ namespace check")
    return 0


# ── Rule 3: AtlasAI C# namespace check ───────────────────────────────────────

ATLASAI_DIR = REPO_ROOT / "AtlasAI"


def run_atlasai_namespace_check() -> int:
    bad_files: list[Path] = []

    for f in iter_files(ATLASAI_DIR, CS_EXTS):
        content = f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""
        if not content.strip():
            continue  # skip empty files
        # Look for a namespace *declaration* line; it should be AtlasAI.*
        # Use multiline match anchored at start-of-line to avoid false matches
        # in inline comments like "// ... from the parent namespace\nusing ..."
        ns_match = re.search(r'^namespace\s+([\w.]+)', content, re.MULTILINE)
        if ns_match and not ns_match.group(1).startswith("AtlasAI"):
            bad_files.append(f)

    if bad_files:
        print("[FAIL] AtlasAI/ C# files with non-AtlasAI.* namespace:")
        for f in sorted(bad_files):
            print(f"  {f.relative_to(REPO_ROOT)}")
        return len(bad_files)
    print("[PASS] AtlasAI C# namespace check")
    return 0


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> int:
    logger.info("Naming convention validation started — repo: %s", REPO_ROOT)
    print("=" * 64)
    print("  Naming Convention Validation")
    print(f"  Repo: {REPO_ROOT}")
    print("=" * 64)
    print()

    total_violations = 0
    logger.info("Running legacy name check …")
    total_violations += run_legacy_name_check()
    print()
    logger.info("Running Atlas namespace check …")
    total_violations += run_atlas_namespace_check()
    print()
    logger.info("Running AtlasAI C# namespace check …")
    total_violations += run_atlasai_namespace_check()

    print()
    print("=" * 64)
    if total_violations == 0:
        logger.info("Result: PASS — no naming violations found")
        print("  Result: PASS — no naming violations found.")
    else:
        logger.warning("Result: FAIL — %d violation(s) found", total_violations)
        print(f"  Result: FAIL — {total_violations} violation(s) found.")
    print("=" * 64)

    return 0 if total_violations == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
