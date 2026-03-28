#!/usr/bin/env bash
# bootstrap.sh — Set up the development environment for MasterRepo.
# Run once after cloning.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { printf "  ${GREEN}[OK]${NC}    %s\n" "$*"; }
warn() { printf "  ${YELLOW}[WARN]${NC}  %s\n" "$*"; }
miss() { printf "  ${RED}[MISS]${NC}  %s\n" "$*"; }

echo "================================================================"
echo "  MasterRepo Bootstrap"
echo "  Repo: $REPO_ROOT"
echo "================================================================"
echo ""

MISSING_TOOLS=()

# ── cmake ≥ 3.20 ─────────────────────────────────────────────────────────────
check_cmake() {
    if command -v cmake &>/dev/null; then
        CMAKE_VER="$(cmake --version | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
        CMAKE_MAJOR="${CMAKE_VER%%.*}"
        CMAKE_MINOR="${CMAKE_VER#*.}"; CMAKE_MINOR="${CMAKE_MINOR%%.*}"
        if [[ $CMAKE_MAJOR -gt 3 ]] || { [[ $CMAKE_MAJOR -eq 3 ]] && [[ $CMAKE_MINOR -ge 20 ]]; }; then
            ok "cmake $CMAKE_VER"
        else
            warn "cmake $CMAKE_VER found but >= 3.20 is required"
            MISSING_TOOLS+=(cmake)
        fi
    else
        miss "cmake (>= 3.20 required)"
        MISSING_TOOLS+=(cmake)
    fi
}

# ── C++ compiler ──────────────────────────────────────────────────────────────
check_cxx() {
    if command -v g++ &>/dev/null; then
        ok "g++ $(g++ --version | head -1)"
    elif command -v clang++ &>/dev/null; then
        ok "clang++ $(clang++ --version | head -1)"
    else
        miss "C++ compiler (g++ or clang++ required)"
        MISSING_TOOLS+=(g++)
    fi
}

# ── python3 ───────────────────────────────────────────────────────────────────
check_python3() {
    if command -v python3 &>/dev/null; then
        ok "python3 $(python3 --version)"
    else
        miss "python3"
        MISSING_TOOLS+=(python3)
    fi
}

# ── dotnet ────────────────────────────────────────────────────────────────────
check_dotnet() {
    if command -v dotnet &>/dev/null; then
        ok "dotnet $(dotnet --version)"
    else
        miss "dotnet SDK (required for AtlasAI C# components)"
        MISSING_TOOLS+=(dotnet)
    fi
}

check_cmake
check_cxx
check_python3
check_dotnet

echo ""

if [[ ${#MISSING_TOOLS[@]} -eq 0 ]]; then
    echo "  All required tools are present."
else
    echo "  Missing tools: ${MISSING_TOOLS[*]}"
    echo ""

    if command -v apt-get &>/dev/null; then
        echo "  Attempting to install missing packages via apt-get ..."
        APT_PACKAGES=()
        for tool in "${MISSING_TOOLS[@]}"; do
            case "$tool" in
                cmake)   APT_PACKAGES+=(cmake) ;;
                g++)     APT_PACKAGES+=(g++) ;;
                python3) APT_PACKAGES+=(python3) ;;
                dotnet)
                    warn "dotnet must be installed manually from https://dotnet.microsoft.com/download"
                    ;;
            esac
        done

        if [[ ${#APT_PACKAGES[@]} -gt 0 ]]; then
            sudo apt-get update -qq
            sudo apt-get install -y "${APT_PACKAGES[@]}"
            echo ""
            echo "  Re-checking after install ..."
            MISSING_TOOLS=()
            check_cmake
            check_cxx
            check_python3
        fi
    else
        warn "apt-get not available. Please install missing tools manually."
    fi
fi

echo ""
echo "================================================================"
echo "  Next steps:"
echo ""
echo "    1. Configure and build:"
echo "         ./Scripts/Setup/setup.sh"
echo ""
echo "    2. Or build manually:"
echo "         ./Scripts/Build/build.sh --config Debug --tests"
echo ""
echo "    3. Run tests:"
echo "         ./Scripts/Build/test.sh"
echo ""
echo "    4. Run CI validation:"
echo "         ./Scripts/CI/ci_validate.sh"
echo "================================================================"
