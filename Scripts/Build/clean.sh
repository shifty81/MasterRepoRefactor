#!/usr/bin/env bash
# clean.sh — Remove build artifacts.
#
# Usage:
#   ./Scripts/Build/clean.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BUILD_DIR="${REPO_ROOT}/Build"

# shellcheck source=Scripts/Logging/log_helper.sh
source "${REPO_ROOT}/Scripts/Logging/log_helper.sh"
log_init "build"

if [[ ! -d "$BUILD_DIR" ]]; then
    echo "[clean] Nothing to clean — '$BUILD_DIR' does not exist."
    exit 0
fi

log_section "Clean Build Artifacts"
echo "[clean] Removing build artifacts in '$BUILD_DIR' ..."
find "$BUILD_DIR" -mindepth 1 -maxdepth 1 ! -name '.gitkeep' -print -exec rm -rf {} +

echo "[clean] Done."
