#!/usr/bin/env python3
"""Engine build smoke test — validates that all CMake targets and key source files
are present before attempting a real CMake configure/build."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(REPO_ROOT))
from Shared.Logging.log_utils import get_tool_logger

logger = get_tool_logger(__name__, subsystem="build")

PASS = 0
FAIL = 0
FAILURES: list[str] = []


def check(condition: bool, label: str) -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        logger.info("  [PASS] %s", label)
    else:
        FAIL += 1
        FAILURES.append(label)
        logger.warning("  [FAIL] %s", label)


# ---------------------------------------------------------------------------
# 1. CMakeLists.txt targets
# ---------------------------------------------------------------------------
CMAKE_TARGETS = [
    "Atlas/Engine/CMakeLists.txt",
    "Atlas/Editor/CMakeLists.txt",
    "NovaForge/CMakeLists.txt",
    "NovaForge/Client/CMakeLists.txt",
    "NovaForge/Server/CMakeLists.txt",
]


def check_cmake_targets() -> None:
    print("\n--- CMakeLists.txt targets ---")
    for rel in CMAKE_TARGETS:
        check((REPO_ROOT / rel).exists(), rel)


# ---------------------------------------------------------------------------
# 2. Key C++ headers — spot-check per subsystem
# ---------------------------------------------------------------------------
KEY_HEADERS = [
    # Rendering
    "Atlas/Engine/Rendering/Renderer.h",
    "Atlas/Engine/Rendering/RenderViewport.h",
    # Input
    "Atlas/Engine/Input/InputManager.h",
    # Physics
    "Atlas/Engine/Physics/PhysicsWorld.h",
    "Atlas/Engine/Physics/PhysicsTypes.h",
    # Audio
    "Atlas/Engine/Audio/AudioEngine.h",
    # ECS
    "Atlas/Engine/ECS/ECS.h",
    "Atlas/Engine/ECS/ComponentRegistry.h",
    # Scene (Phase 11)
    "Atlas/Engine/Scene/SceneNode.h",
    "Atlas/Engine/Scene/SceneGraph.h",
    "Atlas/Engine/Scene/SceneManager.h",
    "Atlas/Engine/Scene/SceneTypes.h",
    # Config
    "Atlas/Engine/Config/KeybindConfig.h",
    "Atlas/Engine/Config/SchemaVersionRegistry.h",
]


def check_key_headers() -> None:
    print("\n--- Key C++ headers ---")
    for rel in KEY_HEADERS:
        check((REPO_ROOT / rel).exists(), rel)


# ---------------------------------------------------------------------------
# 3. External dependency include dirs
# ---------------------------------------------------------------------------
EXTERNAL_BASE = "NovaForge/Client/App/external"
EXTERNAL_DEPS = ["stb", "nlohmann", "tinygltf", "tinyobjloader"]


def check_external_deps() -> None:
    print("\n--- External dependency include dirs ---")
    for dep in EXTERNAL_DEPS:
        rel = f"{EXTERNAL_BASE}/{dep}"
        check((REPO_ROOT / rel).is_dir(), rel)


# ---------------------------------------------------------------------------
# 4. Phase 11 wired subsystem headers
# ---------------------------------------------------------------------------
PHASE11_HEADERS = [
    "Atlas/Engine/Scene/SceneNode.h",
    "Atlas/Engine/Scene/SceneGraph.h",
    "Atlas/Engine/Scene/SceneManager.h",
]


def check_phase11_headers() -> None:
    print("\n--- Phase 11 wired subsystem headers ---")
    for rel in PHASE11_HEADERS:
        check((REPO_ROOT / rel).exists(), rel)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> int:
    logger.info("=" * 60)
    logger.info("  Engine Build Smoke Test")
    logger.info("=" * 60)

    check_cmake_targets()
    check_key_headers()
    check_external_deps()
    check_phase11_headers()

    logger.info("\n" + "=" * 60)
    total = PASS + FAIL
    logger.info("  Results: %d/%d passed, %d failed", PASS, total, FAIL)
    if FAILURES:
        logger.warning("\n  Failed checks:")
        for f in FAILURES:
            logger.warning("    - %s", f)
    logger.info("=" * 60)

    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
