#!/usr/bin/env bash
# ci_validate.sh — CI validation runner.
# Runs boundary and naming validation checks.
# Exits non-zero if any check fails.

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATE_DIR="${SCRIPTS_DIR}/../Validate"

BOUNDARY_SCRIPT="${VALIDATE_DIR}/validate_boundaries.py"
NAMING_SCRIPT="${VALIDATE_DIR}/validate_naming.py"

die() {
    echo "ERROR: $*" >&2
    exit 1
}

command -v python3 &>/dev/null || die "python3 not found. Run Scripts/Bootstrap/bootstrap.sh first."

[[ -f "$BOUNDARY_SCRIPT" ]] || die "validate_boundaries.py not found at $BOUNDARY_SCRIPT"
[[ -f "$NAMING_SCRIPT"   ]] || die "validate_naming.py not found at $NAMING_SCRIPT"

START_TIME=$(date +%s)

echo "================================================================"
echo "  CI Validation — $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "================================================================"
echo ""

BOUNDARY_STATUS=0
echo "[validate] Running boundary checks ..."
python3 "$BOUNDARY_SCRIPT" || BOUNDARY_STATUS=$?

echo ""
NAMING_STATUS=0
echo "[validate] Running naming convention checks ..."
python3 "$NAMING_SCRIPT" || NAMING_STATUS=$?

END_TIME=$(date +%s)
DURATION=$(( END_TIME - START_TIME ))
MINUTES=$(( DURATION / 60 ))
SECONDS=$(( DURATION % 60 ))

echo ""
echo "================================================================"
echo "  Validation Summary"
echo "  Duration   : ${MINUTES}m ${SECONDS}s"
printf "  Boundaries : %s\n" "$([ $BOUNDARY_STATUS -eq 0 ] && echo 'PASS' || echo 'FAIL')"
printf "  Naming     : %s\n" "$([ $NAMING_STATUS    -eq 0 ] && echo 'PASS' || echo 'FAIL')"

OVERALL=0
if [[ $BOUNDARY_STATUS -ne 0 || $NAMING_STATUS -ne 0 ]]; then
    OVERALL=1
fi

printf "  Result     : %s\n" "$([ $OVERALL -eq 0 ] && echo 'PASS' || echo 'FAIL')"
echo "================================================================"

exit $OVERALL
