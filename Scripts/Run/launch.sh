#!/usr/bin/env bash
# launch.sh — Build (if needed) and run MasterRepoRuntime.
#
# Usage:
#   ./Scripts/Run/launch.sh [options]
#
# Options:
#   -m, --mode <game|editor|server|playtest>  Launch mode (default: game)
#   -c, --config <Debug|Release|Shipping>     Build config to run (default: Debug)
#   --build                                   Rebuild before launching
#   --headless                                Suppress window creation (playtest/CI)
#   --bridge [--bridge-port <port>]           Enable AtlasAI bridge on launch
#   --dev                                     Enable dev overlay (F12) at start
#   --save <name>                             Load a named save on boot
#   -h, --help                                Show this help

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BUILD_DIR="${REPO_ROOT}/Build"
source "${REPO_ROOT}/Scripts/Logging/log_helper.sh"
log_init "launch"

# ---- Defaults -------------------------------------------------------------
MODE="game"
BUILD_CONFIG="Debug"
DO_BUILD=false
HEADLESS=false
BRIDGE=false
BRIDGE_PORT=8765
DEV=false
SAVE=""
EXTRA_ARGS=()

# ---- Argument parsing -----------------------------------------------------
usage() {
    sed -n '2,20p' "$0"
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -m|--mode)        MODE="$2";         shift 2 ;;
        -c|--config)      BUILD_CONFIG="$2"; shift 2 ;;
        --build)          DO_BUILD=true;     shift   ;;
        --headless)       HEADLESS=true;     shift   ;;
        --bridge)         BRIDGE=true;       shift   ;;
        --bridge-port)    BRIDGE_PORT="$2";  shift 2 ;;
        --dev)            DEV=true;          shift   ;;
        --save)           SAVE="$2";         shift 2 ;;
        -h|--help)        usage ;;
        *)                EXTRA_ARGS+=("$1"); shift  ;;
    esac
done

# ---- Optional rebuild -----------------------------------------------------
if [[ "$DO_BUILD" == true ]]; then
    log_info "Building (config=${BUILD_CONFIG}) before launch …"
    "${REPO_ROOT}/Scripts/Build/build.sh" --config "${BUILD_CONFIG}"
fi

# ---- Locate executable ----------------------------------------------------
EXE="${BUILD_DIR}/NovaForge/App/MasterRepoRuntime"
if [[ ! -f "$EXE" ]]; then
    log_error "Executable not found: ${EXE}"
    log_error "Run with --build first, or build manually with Scripts/Build/build.sh"
    exit 1
fi

# ---- Assemble args --------------------------------------------------------
LAUNCH_ARGS=("--mode" "${MODE}")

[[ -n "$SAVE" ]] && LAUNCH_ARGS+=("--save" "${SAVE}")
[[ "$HEADLESS" == true ]] && LAUNCH_ARGS+=("--headless")
[[ "$BRIDGE"   == true ]] && LAUNCH_ARGS+=("--bridge" "--bridge-port" "${BRIDGE_PORT}")
[[ "$DEV"      == true ]] && LAUNCH_ARGS+=("--dev")
LAUNCH_ARGS+=("${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"}")

# ---- Launch ---------------------------------------------------------------
log_info "Launching MasterRepoRuntime: ${EXE} ${LAUNCH_ARGS[*]}"
exec "${EXE}" "${LAUNCH_ARGS[@]}"
