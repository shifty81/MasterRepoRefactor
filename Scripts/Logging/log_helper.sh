#!/usr/bin/env bash
# log_helper.sh — Shared logging utilities for MasterRepo shell scripts.
#
# Usage (in any script):
#   source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../../Scripts/Logging/log_helper.sh"
#   log_init "build"          # creates Logs/build/<timestamp>.log, tees all output
#   log_section "My Step"     # prints a timestamped section header
#
# All output (stdout + stderr) is automatically teed to the log file once
# log_init is called.  The resolved log path is exported as LOG_FILE.

# Guard against double-sourcing
[[ -n "${_MR_LOG_HELPER_LOADED:-}" ]] && return 0
_MR_LOG_HELPER_LOADED=1

# Resolve repo root: walk up from this file until we find CMakeLists.txt
_log_find_repo_root() {
    local dir
    dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    for _ in $(seq 1 8); do
        [[ -f "$dir/CMakeLists.txt" ]] && { echo "$dir"; return 0; }
        dir="$(dirname "$dir")"
    done
    # Fallback: two levels above Scripts/Logging/
    echo "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
}

# log_init <subsystem>
#   Creates Logs/<subsystem>/<subsystem>_<YYYYMMDD_HHMMSS>.log and redirects
#   all subsequent stdout/stderr output through tee so the console still shows
#   output while it is also written to the log file.
log_init() {
    local subsystem="${1:-script}"
    local repo_root
    repo_root="$(_log_find_repo_root)"
    local log_dir="${repo_root}/Logs/${subsystem}"
    mkdir -p "$log_dir"
    LOG_FILE="${log_dir}/${subsystem}_$(date '+%Y%m%d_%H%M%S').log"
    export LOG_FILE
    # Redirect stdout and stderr through tee (-a appends; using process sub)
    exec > >(tee -a "$LOG_FILE") 2>&1
    echo "[log] Session started — $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    echo "[log] Log file: $LOG_FILE"
}

# log_section <title>
#   Prints a timestamped section divider that shows clearly in both the console
#   and the log file.
log_section() {
    local title="${1:-}"
    local ts
    ts="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    echo ""
    echo "──────────────────────────────────────────────────────────────"
    echo "  [${ts}] ${title}"
    echo "──────────────────────────────────────────────────────────────"
}

# log_ok / log_warn / log_error — convenience wrappers for consistent prefix
log_ok()    { echo "  [OK]    $*"; }
log_warn()  { echo "  [WARN]  $*"; }
log_error() { echo "  [ERROR] $*" >&2; }
