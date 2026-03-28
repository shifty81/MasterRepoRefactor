#!/usr/bin/env bash
# test.sh — Run MasterRepo CTest suite.
#
# Usage:
#   ./Scripts/Build/test.sh [options]
#
# Options:
#   -c, --config <Debug|Release>  Build configuration (default: Debug)
#   -v, --verbose                 Verbose test output
#   -f, --filter <pattern>        Run only tests matching pattern
#   -h, --help                    Show this help

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BUILD_DIR="${REPO_ROOT}/Build"

# shellcheck source=Scripts/Logging/log_helper.sh
source "${REPO_ROOT}/Scripts/Logging/log_helper.sh"
log_init "test"

CONFIG="Debug"
VERBOSE=false
FILTER=""

usage() {
    sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'
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
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--filter)
            FILTER="${2:?'--filter requires an argument'}"
            shift 2
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
    Debug|Release) ;;
    *) die "Invalid config '$CONFIG'. Must be Debug or Release." ;;
esac

command -v ctest &>/dev/null || die "ctest not found. Run Scripts/Bootstrap/bootstrap.sh first."

[[ -d "$BUILD_DIR" ]] || die "Build directory '$BUILD_DIR' not found. Run build.sh first."

cd "$BUILD_DIR"

CTEST_ARGS=(--output-on-failure --build-config "$CONFIG")

if $VERBOSE; then
    CTEST_ARGS+=(--verbose)
fi

if [[ -n "$FILTER" ]]; then
    CTEST_ARGS+=(--tests-regex "$FILTER")
fi

echo "================================================================"
echo "  MasterRepo Test Run"
echo "  Config : $CONFIG"
echo "  Verbose: $VERBOSE"
echo "  Filter : ${FILTER:-'(all)'}"
echo "================================================================"
echo ""

log_section "CTest"
ctest "${CTEST_ARGS[@]}"

echo ""
echo "================================================================"
echo "  All tests passed."
echo "================================================================"
