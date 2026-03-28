#!/usr/bin/env bash
# clear_logs.sh — Remove all log files from every log folder in the repository.
#
# Run this locally once a debugging session is resolved and the logs are no
# longer needed.  .gitkeep files are preserved so the folder structure stays
# intact in git.
#
# Usage:
#   bash Scripts/Logging/clear_logs.sh            # interactive (prompts first)
#   bash Scripts/Logging/clear_logs.sh --yes      # skip confirmation prompt
#   bash Scripts/Logging/clear_logs.sh --dry-run  # show what would be deleted

set -euo pipefail

# ── Resolve repo root ─────────────────────────────────────────────────────────
# Uses LICENSE as the sentinel (consistent with Python log_utils.py / logger.py)
# because CMakeLists.txt exists in multiple sub-library directories.
_find_repo_root() {
    local dir
    dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    for _ in $(seq 1 8); do
        [[ -f "$dir/LICENSE" ]] && { echo "$dir"; return 0; }
        dir="$(dirname "$dir")"
    done
    # Fallback: two levels above Scripts/Logging/
    echo "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
}

REPO_ROOT="$(_find_repo_root)"

# ── Parse flags ───────────────────────────────────────────────────────────────
AUTO_YES=0
DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        --yes|-y)   AUTO_YES=1 ;;
        --dry-run)  DRY_RUN=1  ;;
        *)
            echo "Usage: $0 [--yes] [--dry-run]" >&2
            exit 2
            ;;
    esac
done

# ── Log directories to clear ──────────────────────────────────────────────────
# AtlasAI subsystem names shared between Logs/ (Python tools/shell) and
# logs/ (AtlasAI engine).  Add new subsystem names here once only.
ATLASAI_SUBSYSTEMS=(
    arbiter_engine
    python_bridge
    host_app
    vs_extension
    self_build
    steam_server_admin
)

LOG_DIRS=()

# Root Logs/ — tool/script subsystems
for sub in "${ATLASAI_SUBSYSTEMS[@]}"; do
    LOG_DIRS+=("${REPO_ROOT}/Logs/${sub}")
done
LOG_DIRS+=(
    "${REPO_ROOT}/Logs/intake"
    "${REPO_ROOT}/Logs/validate"
    "${REPO_ROOT}/Logs/build"
    "${REPO_ROOT}/Logs/tools"
    "${REPO_ROOT}/Logs/ci"
    "${REPO_ROOT}/Logs/setup"
    "${REPO_ROOT}/Logs/run"
)

# Root logs/ — AtlasAI engine (same subsystem names, lowercase parent)
for sub in "${ATLASAI_SUBSYSTEMS[@]}"; do
    LOG_DIRS+=("${REPO_ROOT}/logs/${sub}")
done

# Subsystem-local log directories
LOG_DIRS+=(
    "${REPO_ROOT}/AtlasAI/AIEngine/AtlasAIEngine/logs"
    "${REPO_ROOT}/AtlasAI/HostApp/Logs"
    "${REPO_ROOT}/AtlasAI/AIEngine/Memory/ConversationLogs"
    "${REPO_ROOT}/NovaForge/Integrations/AtlasAI/Logs"
    "${REPO_ROOT}/NovaForge/Server/logs"
    "${REPO_ROOT}/NovaForge/Client/logs"
    "${REPO_ROOT}/Atlas/Core/Logging"
)

# ── Collect files that would be deleted ───────────────────────────────────────
FILES_TO_DELETE=()
for dir in "${LOG_DIRS[@]}"; do
    [[ -d "$dir" ]] || continue
    while IFS= read -r -d '' f; do
        FILES_TO_DELETE+=("$f")
    done < <(find "$dir" -maxdepth 5 -type f ! -name ".gitkeep" \( -name "*.log" -o -name "*.log.*" -o -name "*.jsonl" \) -print0 2>/dev/null)
done

if [[ ${#FILES_TO_DELETE[@]} -eq 0 ]]; then
    echo "  [OK] No log files found — nothing to clear."
    exit 0
fi

# ── Print summary ─────────────────────────────────────────────────────────────
echo ""
echo "  Log files to be cleared (${#FILES_TO_DELETE[@]} file(s)):"
for f in "${FILES_TO_DELETE[@]}"; do
    echo "    ${f#"${REPO_ROOT}/"}"
done
echo ""

if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "  [DRY-RUN] No files were deleted."
    exit 0
fi

# ── Confirm ───────────────────────────────────────────────────────────────────
if [[ "$AUTO_YES" -eq 0 ]]; then
    read -r -p "  Delete these ${#FILES_TO_DELETE[@]} file(s)? [y/N] " response
    [[ "$response" =~ ^[Yy]$ ]] || { echo "  Aborted."; exit 0; }
fi

# ── Delete ────────────────────────────────────────────────────────────────────
deleted=0
for f in "${FILES_TO_DELETE[@]}"; do
    rm -f -- "$f" && (( deleted++ )) || true
done

echo "  [OK] Cleared ${deleted} log file(s). Folder structure preserved."
