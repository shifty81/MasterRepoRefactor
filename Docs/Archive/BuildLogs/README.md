# Build Logs Archive

This directory contains build and CI log files uploaded via the `Intake/` pipeline for debugging reference.

## Contents

| File | Type | Date |
|------|------|------|
| `build_20260328_152344.log` | Debug build (no tests) | 2026-03-28 |
| `build_20260328_152447.log` | Release build (with tests) | 2026-03-28 |
| `ci_20260328_152447.log` | CI validation run | 2026-03-28 |
| `setup_20260328_152310.log` | Dependency check | 2026-03-28 |
| `setup_20260328_152559.log` | CMake configure | 2026-03-28 |
| `test_20260328_152440.log` | CTest run | 2026-03-28 |
| `launch_20260328_152628.log` | Runtime launch attempt | 2026-03-28 |

## Errors Identified and Fixed

The 2026-03-28 build logs identified the following errors, all of which have been corrected:

### C++ Source Fixes
- **`AudioSystem.h`** — Added `#include <array>` (std::array used without the header, causing C2109/C2582)
- **`World.h` / `World.cpp`** — Added `const` overloads for `GetVoxelSubsystem()` and `GetModuleSubsystem()` (C2662 const violation called from `Renderer::Render(const World&)`)
- **`PCGDeterminismEngine.h`** — Marked `AutoAssignSeed()` as `const` to match the `.cpp` implementation (C2511 overload mismatch)
- **`GameOrchestrator.h`** — Replaced forward declaration of `IntegrationCoordinator` with full include (C2027 / C2338 incomplete type in `unique_ptr`)
- **`DataRegistry.h` / `.cpp`** — Added `RecipeIngredient`, `RecipeDefinition` structs and `FindRecipeDefinition()` method (C2039 member not found in `CraftingSystem.cpp`)
- **`PhysicsExtensions.cpp`** — Added `(void)count` to suppress C4189 (unused variable treated as error)
- **`file_logger.cpp`** — Replaced `std::localtime` with a platform-safe `safe_localtime()` helper (C4996 unsafe function on MSVC)
- **`session_manager.cpp`** — Cast `strlen()` result to `int` for `sendto()` (C4267); replaced `inet_ntoa` with `inet_ntop` (C4996)
- **`atlas_console.cpp`** — Added `static_cast<char>` in `std::transform` lambda (C4244 int→char)
- **`atlas_hud.cpp`** — Removed unused `r` variable in `drawSystemInfo()` (C4189)
- **`atlas_renderer.cpp`** — Removed unused `atlasH` variable (C4189)
- **`atlas_widgets_hud.cpp`** — Removed unused `totalH` variable (C4189)
- **`atlas_widgets_panels.cpp`** — Renamed inner `leftEdge` to `sidebarLeft` to eliminate C4456 shadowing
- **`radial_menu.cpp`** — Removed unused `pi2` variable (C4189)

### Build System Fixes
- **`NovaForge/Server/CMakeLists.txt`** — Added `target_link_libraries(NovaForgeServer PRIVATE MasterLogger)` to make `Shared/Logging/MasterLogger.h` findable (C1083)
- **`NovaForge/Client/CMakeLists.txt`** — Fixed nlohmann/json include path from `App/external/nlohmann` to `App/external` so that `#include <nlohmann/json.hpp>` resolves correctly (C1083)
- **`CMakeLists.txt`** — Added FetchContent for `glm`, `glfw`, and `glew` so that the required OpenGL/math headers are available without requiring system-level installation (C1083 for glm.hpp, glew.h, glfw3.h)
