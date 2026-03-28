#!/usr/bin/env bash
# ci_build.sh — CI build runner. Builds and tests in one step.
# Called by CI pipelines. Exits non-zero on failure.

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_SCRIPT="${SCRIPTS_DIR}/../Build/build.sh"
TEST_SCRIPT="${SCRIPTS_DIR}/../Build/test.sh"

CI_CONFIG="${CI_BUILD_CONFIG:-Release}"
CI_JOBS="${CI_BUILD_JOBS:-}"

die() {
    echo "ERROR: $*" >&2
    exit 1
}

[[ -f "$BUILD_SCRIPT" ]] || die "build.sh not found at $BUILD_SCRIPT"
[[ -f "$TEST_SCRIPT"  ]] || die "test.sh not found at $TEST_SCRIPT"

START_TIME=$(date +%s)

echo "================================================================"
echo "  CI Build — $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "  Config : $CI_CONFIG"
echo "================================================================"
echo ""

BUILD_ARGS=(--config "$CI_CONFIG" --tests)
if [[ -n "$CI_JOBS" ]]; then
    BUILD_ARGS+=(--jobs "$CI_JOBS")
fi

BUILD_STATUS=0
bash "$BUILD_SCRIPT" "${BUILD_ARGS[@]}" || BUILD_STATUS=$?

TEST_STATUS=0
if [[ $BUILD_STATUS -eq 0 ]]; then
    bash "$TEST_SCRIPT" --config "$CI_CONFIG" || TEST_STATUS=$?
else
    echo ""
    echo "[ci] Skipping tests because build failed."
fi

END_TIME=$(date +%s)
DURATION=$(( END_TIME - START_TIME ))
MINUTES=$(( DURATION / 60 ))
SECONDS=$(( DURATION % 60 ))

echo ""
echo "================================================================"
echo "  CI Summary"
echo "  Duration : ${MINUTES}m ${SECONDS}s"
printf "  Build    : %s\n" "$([ $BUILD_STATUS -eq 0 ] && echo 'PASS' || echo 'FAIL')"
printf "  Tests    : %s\n" "$([ $TEST_STATUS  -eq 0 ] && echo 'PASS' || echo 'FAIL')"

OVERALL=0
if [[ $BUILD_STATUS -ne 0 || $TEST_STATUS -ne 0 ]]; then
    OVERALL=1
fi

printf "  Result   : %s\n" "$([ $OVERALL -eq 0 ] && echo 'PASS' || echo 'FAIL')"
echo "================================================================"

exit $OVERALL
