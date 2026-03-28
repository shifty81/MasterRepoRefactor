#!/usr/bin/env bash
# setup.sh — One-time project configuration.
# Creates Build/ directory and runs CMake configure step.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BUILD_DIR="${REPO_ROOT}/Build"

# shellcheck source=Scripts/Logging/log_helper.sh
source "${REPO_ROOT}/Scripts/Logging/log_helper.sh"
log_init "setup"

die() {
    echo "ERROR: $*" >&2
    exit 1
}

command -v cmake &>/dev/null || die "cmake not found. Run Scripts/Bootstrap/bootstrap.sh first."

echo "================================================================"
echo "  MasterRepo Setup"
echo "  Repo     : $REPO_ROOT"
echo "  Build dir: $BUILD_DIR"
echo "================================================================"
echo ""

if [[ -d "$BUILD_DIR" ]]; then
    echo "[setup] Build directory already exists: $BUILD_DIR"
else
    log_section "Create Build Directory"
    echo "[setup] Creating build directory: $BUILD_DIR"
    mkdir -p "$BUILD_DIR"
fi

cd "$BUILD_DIR"

log_section "CMake Configure"
echo "[setup] Running CMake configure (Debug, tests enabled) ..."
cmake .. \
    -DCMAKE_BUILD_TYPE=Debug \
    -DMASTERREPO_BUILD_TESTS=ON \
    -DNOVAFORGE_ENABLE_ATLASAI_INTEGRATION=OFF

echo ""
echo "================================================================"
echo "  Setup complete."
echo ""
echo "  To build:      ./Scripts/Build/build.sh"
echo "  To test:       ./Scripts/Build/test.sh"
echo "  To clean:      ./Scripts/Build/clean.sh"
echo "  To build+test: ./Scripts/CI/ci_build.sh"
echo "================================================================"
