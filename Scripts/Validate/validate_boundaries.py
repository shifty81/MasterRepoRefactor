#!/usr/bin/env python3
"""validate_boundaries.py — Check that module dependency rules are respected.

Rules enforced:
- Atlas/ must not import from AtlasAI/ or NovaForge/
  (exception: files under Atlas/Integrations/ may cross those boundaries)
- Shared/ must not import from AtlasAI/, AtlasEditor/, or NovaForge/
- AtlasAI/HostApp and AtlasAI/VisualStudioExtension (C#) must not import
  game-runtime or engine-internal namespaces directly

Exit codes:
  0 — all rules pass
  1 — one or more violations found
  2 — usage error
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# ── Helpers ───────────────────────────────────────────────────────────────────

def iter_files(directory: Path, extensions: tuple[str, ...]):
    """Yield all files with the given extensions under *directory*."""
    if not directory.is_dir():
        return
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix in extensions:
            yield path


def check_cpp_includes(
    source_file: Path,
    forbidden_patterns: list[re.Pattern],
    exempt_substrings: list[str],
) -> list[tuple[int, str]]:
    """Return a list of (line_number, line_text) for forbidden #include lines."""
    # Check whether this file itself is in an exempt sub-path
    file_str = source_file.as_posix()
    for exempt in exempt_substrings:
        if exempt in file_str:
            return []

    violations = []
    try:
        lines = source_file.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped.startswith("#include"):
            continue
        for pat in forbidden_patterns:
            if pat.search(stripped):
                violations.append((lineno, line.rstrip()))
                break
    return violations


def check_csharp_usings(
    source_file: Path,
    forbidden_patterns: list[re.Pattern],
) -> list[tuple[int, str]]:
    """Return (line_number, line_text) for forbidden `using` directives."""
    violations = []
    try:
        lines = source_file.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped.startswith("using "):
            continue
        for pat in forbidden_patterns:
            if pat.search(stripped):
                violations.append((lineno, line.rstrip()))
                break
    return violations


def report(violations: dict[Path, list[tuple[int, str]]], rule_name: str) -> int:
    """Print violations for a rule. Returns number of violations."""
    count = 0
    for path, hits in sorted(violations.items()):
        for lineno, text in hits:
            print(f"  {path.relative_to(REPO_ROOT)}:{lineno}: {text.strip()}")
            count += 1
    return count


# ── Rules ─────────────────────────────────────────────────────────────────────

CPP_EXTS = (".h", ".hpp", ".hxx", ".cpp", ".cxx", ".cc", ".c")
CS_EXTS  = (".cs",)

ATLAS_DIR   = REPO_ROOT / "Atlas"
SHARED_DIR  = REPO_ROOT / "Shared"
ATLASAI_DIR = REPO_ROOT / "AtlasAI"

# Atlas/ must not include AtlasAI/ or NovaForge/ headers
ATLAS_FORBIDDEN_PATTERNS = [
    re.compile(r'#include\s+[<"].*AtlasAI/', re.IGNORECASE),
    re.compile(r'#include\s+[<"].*NovaForge/', re.IGNORECASE),
]
ATLAS_EXEMPT_SUBSTRINGS = ["/Integrations/"]

# Shared/ must not include AtlasAI/, AtlasEditor/, or NovaForge/ headers
SHARED_FORBIDDEN_PATTERNS = [
    re.compile(r'#include\s+[<"].*AtlasAI/', re.IGNORECASE),
    re.compile(r'#include\s+[<"].*AtlasEditor/', re.IGNORECASE),
    re.compile(r'#include\s+[<"].*NovaForge/', re.IGNORECASE),
]
SHARED_EXEMPT_SUBSTRINGS: list[str] = []

# AtlasAI HostApp / VSExtension must not reference game-runtime or engine internals
# Allowed: AtlasAI.*, Shared.*
# Forbidden: NovaForge.*, Atlas.Engine.*, Atlas.Runtime.*
ATLASAI_CS_FORBIDDEN_PATTERNS = [
    re.compile(r'\busing\s+NovaForge\b'),
    re.compile(r'\busing\s+Atlas\.Engine\b'),
    re.compile(r'\busing\s+Atlas\.Runtime\b'),
]
ATLASAI_CS_DIRS = [
    ATLASAI_DIR / "HostApp",
    ATLASAI_DIR / "VisualStudioExtension",
]


def run_atlas_boundary_check() -> int:
    violations: dict[Path, list[tuple[int, str]]] = {}
    for f in iter_files(ATLAS_DIR, CPP_EXTS):
        hits = check_cpp_includes(f, ATLAS_FORBIDDEN_PATTERNS, ATLAS_EXEMPT_SUBSTRINGS)
        if hits:
            violations[f] = hits
    if violations:
        print("[FAIL] Atlas/ boundary violations (must not include AtlasAI/ or NovaForge/):")
        return report(violations, "Atlas boundaries")
    print("[PASS] Atlas/ boundary check")
    return 0


def run_shared_boundary_check() -> int:
    violations: dict[Path, list[tuple[int, str]]] = {}
    for f in iter_files(SHARED_DIR, CPP_EXTS):
        hits = check_cpp_includes(f, SHARED_FORBIDDEN_PATTERNS, SHARED_EXEMPT_SUBSTRINGS)
        if hits:
            violations[f] = hits
    if violations:
        print("[FAIL] Shared/ boundary violations (must not include AtlasAI/, AtlasEditor/, or NovaForge/):")
        return report(violations, "Shared boundaries")
    print("[PASS] Shared/ boundary check")
    return 0


def run_atlasai_csharp_check() -> int:
    violations: dict[Path, list[tuple[int, str]]] = {}
    for cs_dir in ATLASAI_CS_DIRS:
        for f in iter_files(cs_dir, CS_EXTS):
            hits = check_csharp_usings(f, ATLASAI_CS_FORBIDDEN_PATTERNS)
            if hits:
                violations[f] = hits
    if violations:
        print("[FAIL] AtlasAI C# boundary violations (direct game-runtime/engine imports forbidden):")
        return report(violations, "AtlasAI C# boundaries")
    print("[PASS] AtlasAI C# boundary check")
    return 0


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> int:
    print("=" * 64)
    print("  Boundary Validation")
    print(f"  Repo: {REPO_ROOT}")
    print("=" * 64)
    print()

    total_violations = 0
    total_violations += run_atlas_boundary_check()
    print()
    total_violations += run_shared_boundary_check()
    print()
    total_violations += run_atlasai_csharp_check()

    print()
    print("=" * 64)
    if total_violations == 0:
        print("  Result: PASS — no boundary violations found.")
    else:
        print(f"  Result: FAIL — {total_violations} violation(s) found.")
    print("=" * 64)

    return 0 if total_violations == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
