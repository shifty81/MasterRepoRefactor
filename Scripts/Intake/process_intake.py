#!/usr/bin/env python3
"""process_intake.py — Classify and route files from Intake/ to canonical destinations.

Usage:
    python3 Scripts/Intake/process_intake.py [--dry-run] [--verbose]

Options:
    --dry-run    Print routing decisions without moving any files.
    --verbose    Print a line for every file examined (including skipped ones).
    --classify   Alias for --dry-run (explicit classify-only mode).

Exit codes:
    0  All items classified and routed (or dry-run complete with no unclassified items).
    1  One or more items could not be confidently classified.
    2  Usage error.

Rules are documented in: Docs/Architecture/intake_policy.md
"""

import sys
import shutil
import json
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

REPO_ROOT  = Path(__file__).resolve().parents[2]
INTAKE_DIR = REPO_ROOT / "Intake"
LOG_DIR    = REPO_ROOT / "Logs" / "intake"

sys.path.insert(0, str(REPO_ROOT))
from Shared.Logging.log_utils import get_tool_logger
logger = get_tool_logger(__name__, subsystem="intake")


# ---------------------------------------------------------------------------
# Classification result
# ---------------------------------------------------------------------------

class ClassificationResult:
    def __init__(self, source: Path, destination: Path, label: str,
                 confident: bool = True, note: str = ""):
        self.source:      Path = source
        self.destination: Path = destination
        self.label:       str  = label       # e.g. "zip_archive", "design_doc"
        self.confident:   bool = confident
        self.note:        str  = note

    def __repr__(self) -> str:
        marker = "✓" if self.confident else "?"
        rel_src = self.source.relative_to(REPO_ROOT)
        rel_dst = self.destination.relative_to(REPO_ROOT)
        return f"[{marker}] {rel_src} → {rel_dst}  ({self.label})"


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------

# Filename signals for documentation routing (checked against uppercased filename stem)
_DOC_SIGNALS: list[tuple[list[str], Path, str]] = [
    (["DESIGN", "DIRECTIVE", "VISION", "CANON", "MASTER_DESIGN",
      "MASTER_REPO"],                             REPO_ROOT / "Docs" / "Design",
     "design_doc"),
    (["ARCHITECTURE", "BOUNDAR", "DEPENDENCY", "LAYOUT",
      "MONOREPO", "SHIPPING", "INTAKE"],          REPO_ROOT / "Docs" / "Architecture",
     "architecture_doc"),
    (["ROADMAP", "PHASE_EXECUTION"],              REPO_ROOT / "Docs" / "Roadmaps",
     "roadmap_doc"),
    (["ROADMAP_", "SPRINT", "CHECKLIST", "MIGRATION", "EXECUTION",
      "PHASE_", "DAY_BY_DAY", "MOVE_CHECKLIST",
      "MODULE_OWNERSHIP", "POST_CONSOLIDATION",
      "FIRST_REAL", "GITHUB_ISSUES"],             REPO_ROOT / "Docs" / "Archive" / "Planning",
     "planning_doc"),
    (["CROSSPLATFORM", "GUI", "LAUNCHING",
      "SETUP", "CONTRIBUTING"],                   REPO_ROOT / "Docs",
     "top_level_doc"),
]


def _classify_file(path: Path) -> ClassificationResult:
    """Return the routing decision for a single file."""
    name_upper = path.stem.upper()
    suffix     = path.suffix.lower()

    # ---- Archives ---------------------------------------------------------
    if suffix in (".zip", ".tar", ".gz", ".7z", ".rar"):
        return ClassificationResult(
            path,
            REPO_ROOT / "Docs" / "Archive" / "ZipFiles" / path.name,
            "zip_archive",
        )

    # ---- Documentation ----------------------------------------------------
    if suffix in (".md", ".rst"):
        for signals, dest_dir, label in _DOC_SIGNALS:
            if any(sig in name_upper for sig in signals):
                return ClassificationResult(path, dest_dir / path.name, label)
        # Default docs go to Docs/Design
        return ClassificationResult(
            path, REPO_ROOT / "Docs" / "Design" / path.name, "design_doc_default")

    # ---- CMake (before .txt to avoid CMakeLists.txt being misclassified) -----
    if suffix == ".cmake" or path.name == "CMakeLists.txt":
        return ClassificationResult(
            path, REPO_ROOT / "cmake" / path.name, "cmake_module")

    if suffix == ".txt":
        # Assume chat export → archive chats, suggest structured doc
        return ClassificationResult(
            path,
            REPO_ROOT / "Docs" / "Archive" / "Chats" / path.name,
            "chat_export",
            confident=True,
            note="Convert to structured .md in Docs/Design/ after routing.",
        )

    # ---- C++ / C source ---------------------------------------------------
    if suffix in (".h", ".hpp", ".hxx", ".cpp", ".cxx", ".cc", ".c"):
        dest = _classify_cpp(path)
        if dest:
            return dest

    # ---- Python -----------------------------------------------------------
    if suffix == ".py":
        if path.stem.startswith("test_"):
            return ClassificationResult(
                path, REPO_ROOT / "AtlasAI" / "Tests" / path.name, "python_test")
        # Heuristic: check for build/validate keywords in stem
        stem_lower = path.stem.lower()
        if any(k in stem_lower for k in ("validate", "check", "lint")):
            return ClassificationResult(
                path, REPO_ROOT / "Scripts" / "Validate" / path.name, "validate_script")
        if any(k in stem_lower for k in ("build", "clean", "compile")):
            return ClassificationResult(
                path, REPO_ROOT / "Scripts" / "Build" / path.name, "build_script")
        if any(k in stem_lower for k in ("ci", "workflow", "pipeline")):
            return ClassificationResult(
                path, REPO_ROOT / "Scripts" / "CI" / path.name, "ci_script")
        # Default Python → AtlasAI engine
        return ClassificationResult(
            path, REPO_ROOT / "AtlasAI" / "AIEngine" / "AtlasAIEngine" / path.name,
            "ai_engine_python",
            confident=False,
            note="Default Python route — verify subsystem manually.",
        )

    # ---- C# ---------------------------------------------------------------
    if suffix in (".cs", ".csproj", ".sln"):
        return ClassificationResult(
            path, REPO_ROOT / "AtlasAI" / "HostApp" / path.name,
            "csharp_hostapp",
            confident=False,
            note="Default C# route — verify HostApp vs ProjectAdapters vs VSIX.",
        )

    # ---- JSON / YAML / data -----------------------------------------------
    if suffix in (".json", ".yaml", ".yml", ".toml", ".ini"):
        return ClassificationResult(
            path, REPO_ROOT / "NovaForge" / "Data" / path.name,
            "data_config",
            confident=False,
            note="Default data route — verify NovaForge/Data vs Atlas/Config vs Shared.",
        )

    # ---- Unknown ----------------------------------------------------------
    return ClassificationResult(
        path,
        REPO_ROOT / "Docs" / "Archive" / "Planning" / "UNCLASSIFIED" / path.name,
        "unclassified",
        confident=False,
        note="Could not determine routing — manual review required.",
    )


def _classify_cpp(path: Path) -> Optional[ClassificationResult]:
    """Read the first 60 lines of a C++ file and route by namespace / include signals."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            head = "".join(fh.readline() for _ in range(60))
    except OSError:
        return None

    head_lower = head.lower()

    # Detect boundary violations (Atlas including NovaForge)
    if re.search(r'namespace\s+(atlas|atlas::)', head_lower):
        if re.search(r'#include\s+".*novaforge', head_lower):
            return ClassificationResult(
                path,
                REPO_ROOT / "Docs" / "Archive" / "Planning" / "UNCLASSIFIED" / path.name,
                "boundary_violation",
                confident=False,
                note="Atlas file with NovaForge include — boundary violation.",
            )

    # Routing by namespace declaration
    if re.search(r'namespace\s+atlas\b', head_lower):
        stem = path.stem.lower()
        if any(k in stem for k in ("render", "viewport", "shader", "material")):
            zone = "Rendering"
        elif any(k in stem for k in ("physics", "collid")):
            zone = "Physics"
        elif any(k in stem for k in ("audio", "sound")):
            zone = "Audio"
        elif any(k in stem for k in ("input", "keybind", "action")):
            zone = "Input"
        elif any(k in stem for k in ("editor", "panel", "dock", "outliner",
                                      "inspector", "gizmo", "command")):
            return ClassificationResult(
                path,
                REPO_ROOT / "Atlas" / "Editor" / "Core" / path.name,
                "atlas_editor_cpp",
            )
        elif any(k in stem for k in ("launch", "config", "schema", "settings")):
            zone = "Config"
        elif any(k in stem for k in ("save", "load", "serializ")):
            zone = "SaveLoad"
        elif any(k in stem for k in ("pcg", "procedural")):
            zone = "PCG"
        elif any(k in stem for k in ("script", "vm", "lua")):
            zone = "Scripting"
        elif any(k in stem for k in ("net", "session", "packet")):
            zone = "Networking"
        elif any(k in stem for k in ("anim")):
            zone = "Animation"
        elif any(k in stem for k in ("ecs", "entity", "component")):
            zone = "ECS"
        else:
            zone = "Core"
        return ClassificationResult(
            path, REPO_ROOT / "Atlas" / "Engine" / zone / path.name, "atlas_engine_cpp")

    if re.search(r'namespace\s+novaforge\b', head_lower):
        stem = path.stem.lower()
        if any(k in stem for k in ("inventory", "loot", "item")):
            zone = "Inventory"
        elif any(k in stem for k in ("mission", "contract")):
            zone = "Missions"
        elif any(k in stem for k in ("fleet", "ship")):
            zone = "Fleet"
        elif any(k in stem for k in ("save", "load")):
            return ClassificationResult(
                path, REPO_ROOT / "NovaForge" / "Save" / "include" / path.name,
                "novaforge_save_cpp")
        elif any(k in stem for k in ("bootstrap", "app", "session", "orchestrat")):
            return ClassificationResult(
                path, REPO_ROOT / "NovaForge" / "App" / "src" / path.name,
                "novaforge_app_cpp")
        elif any(k in stem for k in ("world", "sector", "galaxy")):
            zone = "World"
        elif any(k in stem for k in ("progression", "reward", "xp", "skill")):
            zone = "Progression"
        elif any(k in stem for k in ("faction", "relation")):
            zone = "Factions"
        elif any(k in stem for k in ("economy", "market", "trade")):
            zone = "Economy"
        elif any(k in stem for k in ("station", "service")):
            zone = "Station"
        elif any(k in stem for k in ("salvage", "mine", "extract")):
            zone = "Salvage"
        elif any(k in stem for k in ("pcg", "procedural")):
            zone = "PCG"
        elif any(k in stem for k in ("season", "titan", "endgame")):
            zone = "Season"
        elif any(k in stem for k in ("anomaly", "event")):
            zone = "Anomaly"
        elif any(k in stem for k in ("war", "sector")):
            zone = "WarSector"
        elif any(k in stem for k in ("manufactur", "craft")):
            zone = "Manufacturing"
        else:
            zone = "Gameplay"
        return ClassificationResult(
            path, REPO_ROOT / "NovaForge" / "Gameplay" / zone / path.name,
            "novaforge_gameplay_cpp")

    return None


# ---------------------------------------------------------------------------
# Directory intake
# ---------------------------------------------------------------------------

def _classify_directory(path: Path) -> list[ClassificationResult]:
    """Classify all files inside a directory recursively."""
    results = []
    for child in sorted(path.rglob("*")):
        if child.is_file() and child.name != "README.md":
            results.append(_classify_file(child))
    return results


# ---------------------------------------------------------------------------
# Routing (move)
# ---------------------------------------------------------------------------

def _route(result: ClassificationResult, dry_run: bool) -> bool:
    """Move the file to its destination.  Returns True on success."""
    dest = result.destination
    if dest == result.source:
        logger.info("SKIP (already in place): %s", result.source.name)
        return True
    if dry_run:
        logger.info("DRY-RUN: %s", result)
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        logger.warning("SKIP (destination exists): %s", dest)
        return True
    shutil.move(str(result.source), str(dest))
    logger.info("MOVED: %s → %s", result.source.relative_to(REPO_ROOT),
                dest.relative_to(REPO_ROOT))
    return True


# ---------------------------------------------------------------------------
# Audit log
# ---------------------------------------------------------------------------

def _write_audit(results: list[ClassificationResult], dry_run: bool):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "intake_log.jsonl"
    ts = datetime.now(tz=timezone.utc).isoformat()
    with open(log_file, "a", encoding="utf-8") as fh:
        for r in results:
            record = {
                "timestamp":      ts,
                "source":         str(r.source.relative_to(REPO_ROOT)),
                "destination":    str(r.destination.relative_to(REPO_ROOT)),
                "classification": r.label,
                "confident":      r.confident,
                "note":           r.note,
                "dry_run":        dry_run,
            }
            fh.write(json.dumps(record) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify and route files from Intake/ to canonical destinations.")
    parser.add_argument("--dry-run", "--classify", action="store_true",
                        help="Print routing decisions without moving files.")
    parser.add_argument("--verbose", action="store_true",
                        help="Print a line for every examined file.")
    args = parser.parse_args()

    if not INTAKE_DIR.is_dir():
        logger.error("Intake/ directory not found at: %s", INTAKE_DIR)
        return 2

    # Gather all items (files and directories) directly inside Intake/
    items = sorted(INTAKE_DIR.iterdir())
    # Filter out the README and hidden files
    items = [p for p in items
             if p.name != "README.md" and not p.name.startswith(".")]

    if not items:
        logger.info("Intake/ is empty — nothing to process.")
        return 0

    all_results: list[ClassificationResult] = []

    for item in items:
        if item.is_dir():
            dir_results = _classify_directory(item)
            all_results.extend(dir_results)
        else:
            all_results.append(_classify_file(item))

    # Print summary
    unclassified = [r for r in all_results if not r.confident]
    for r in all_results:
        if args.verbose or not r.confident:
            print(repr(r))
            if r.note:
                print(f"    NOTE: {r.note}")

    if not args.verbose:
        classified = [r for r in all_results if r.confident]
        print(f"\n{len(all_results)} item(s): "
              f"{len(classified)} classified, {len(unclassified)} unclassified")

    # Route
    if not args.dry_run:
        for r in all_results:
            _route(r, dry_run=False)

    # Audit log
    _write_audit(all_results, dry_run=args.dry_run)

    if unclassified:
        logger.warning("%d item(s) could not be confidently classified", len(unclassified))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
