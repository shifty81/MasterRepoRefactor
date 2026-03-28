#!/usr/bin/env bash
# build.sh — Configure and build MasterRepo using CMake.
#
# Usage:
#   ./Scripts/Build/build.sh [options]
#
# Options:
#   -c, --config <Debug|Release|Shipping>  Build configuration (default: Debug)
#   -j, --jobs <N>                         Parallel jobs (default: auto-detected)
#   -t, --tests                            Enable test build
#   -b, --bridge                           Enable AtlasAI bridge integration
#   --clean                                Clean before building
#   -h, --help                             Show this help

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BUILD_DIR="${REPO_ROOT}/Build"

CONFIG="Debug"
JOBS=""
ENABLE_TESTS="OFF"
ENABLE_BRIDGE="OFF"
CLEAN=false

usage() {
    sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
    exit 0
}

die() {
    echo "ERROR: $*" >&2
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -c|--config)
            CONFIG="${2:?'--config requires an argument'}"
            shift 2
            ;;
        -j|--jobs)
            JOBS="${2:?'--jobs requires an argument'}"
            shift 2
            ;;
        -t|--tests)
            ENABLE_TESTS="ON"
            shift
            ;;
        -b|--bridge)
            ENABLE_BRIDGE="ON"
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            die "Unknown option: $1"
            ;;
    esac
done

case "$CONFIG" in
    Debug|Release|Shipping) ;;
    *) die "Invalid config '$CONFIG'. Must be Debug, Release, or Shipping." ;;
esac

if [[ -z "$JOBS" ]]; then
    if command -v nproc &>/dev/null; then
        JOBS="$(nproc)"
    elif command -v sysctl &>/dev/null; then
        JOBS="$(sysctl -n hw.logicalcpu 2>/dev/null || echo 4)"
    else
        JOBS=4
    fi
fi

command -v cmake &>/dev/null || die "cmake not found. Run Scripts/Bootstrap/bootstrap.sh first."

echo "================================================================"
echo "  MasterRepo Build"
echo "  Config  : $CONFIG"
echo "  Jobs    : $JOBS"
echo "  Tests   : $ENABLE_TESTS"
echo "  Bridge  : $ENABLE_BRIDGE"
echo "  BuildDir: $BUILD_DIR"
echo "================================================================"

if $CLEAN && [[ -d "$BUILD_DIR" ]]; then
    echo "[clean] Removing $BUILD_DIR ..."
    rm -rf "$BUILD_DIR"
fi

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

echo ""
echo "[cmake] Configuring ..."
cmake .. \
    -DCMAKE_BUILD_TYPE="$CONFIG" \
    -DMASTERREPO_BUILD_TESTS="$ENABLE_TESTS" \
    -DNOVAFORGE_ENABLE_ATLASAI_INTEGRATION="$ENABLE_BRIDGE"

echo ""
echo "[cmake] Building with $JOBS jobs ..."
cmake --build . --parallel "$JOBS"

echo ""
echo "================================================================"
echo "  Build complete: $CONFIG"
echo "================================================================"
