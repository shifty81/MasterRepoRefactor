# MASTERREPO_CMAKE_AND_TARGET_WIRING_PLAN

## Purpose
This document defines the **build-system strategy** for the MasterRepo monorepo after the Atlas + NovaForge + Arbiter refactor.

It is meant to align with:

- `MASTER_IMPLEMENTATION_CHECKLIST.md`
- `MASTERREPO_TARGET_TREE_BLUEPRINT.md`
- `Arbiter_NovaForge_Integration_Plan.md`

The goal is to make the **physical monorepo layout** and the **logical dependency graph** match cleanly in CMake and related build targets.

---

# Build-system goals

1. Keep **Atlas** reusable and independent of Arbiter.
2. Keep **NovaForge** buildable without Arbiter.
3. Keep **Arbiter** optional from the game/runtime perspective.
4. Keep **Shared** small and stable.
5. Prevent tooling/editor code from leaking into shipping runtime binaries.
6. Make target naming predictable and ownership-driven.
7. Support editor-only integrations safely.
8. Make future CI and packaging straightforward.

---

# Recommended top-level build layout

## Top-level structure
At the root of `MasterRepo`, use a root `CMakeLists.txt` that orchestrates repo-wide targets.

Example logical layout:

```text
MasterRepo/
├── CMakeLists.txt
├── cmake/
│   ├── Options.cmake
│   ├── CompilerWarnings.cmake
│   ├── PlatformConfig.cmake
│   ├── AtlasTargets.cmake
│   ├── NovaForgeTargets.cmake
│   ├── SharedTargets.cmake
│   ├── TestingConfig.cmake
│   └── PackagingConfig.cmake
├── Atlas/
├── NovaForge/
├── Arbiter/
├── Shared/
├── Docs/
├── ThirdParty/
├── Tools/
├── Scripts/
├── Tests/
└── Build/
```

---

# Root CMake responsibilities

The root `CMakeLists.txt` should do only these jobs:

- define the project
- define global options
- configure compiler/platform settings
- include common CMake modules
- add subdirectories in dependency order
- register tests
- avoid project-specific deep logic

## Recommended root subdirectory order

```cmake
add_subdirectory(Shared)
add_subdirectory(Atlas)
add_subdirectory(NovaForge)
```

Only add Arbiter-related build integration if you are bridging it through CMake-compatible native components.

If Arbiter is mostly C# / WPF / VSIX, do **not** force it into the main CMake graph unless you have a thin helper target strategy. Keep it build-adjacent, not build-entangled.

---

# Repo-wide build options

## Recommended root options

```cmake
option(MASTERREPO_BUILD_TESTS "Build repo tests" ON)
option(MASTERREPO_BUILD_TOOLS "Build developer tools" ON)
option(MASTERREPO_BUILD_EDITOR "Build editor targets" ON)
option(MASTERREPO_BUILD_CLIENT "Build client targets" ON)
option(MASTERREPO_BUILD_SERVER "Build server targets" ON)

option(ATLAS_ENABLE_EDITOR "Enable Atlas editor systems" ON)
option(NOVAFORGE_ENABLE_ARBETER_INTEGRATION "Enable NovaForge Arbiter bridge integration" ON)
option(NOVAFORGE_ENABLE_SHIPPING_SAFE_MODE "Disable dev-only integration paths for shipping" ON)
```

## Note
Use a corrected internal option name in actual code:

- `NOVAFORGE_ENABLE_ARBITER_INTEGRATION`

The typo above should not be used in the real file.

---

# Ownership-driven target model

## Shared targets
Shared should expose only neutral target(s), for example:

- `ArbiterBridgeContract`

This target should contain:
- shared bridge headers
- protocol schemas if applicable
- include directories
- no gameplay logic
- no editor logic
- no WPF/C# host logic

### Example
```text
Shared/
├── CMakeLists.txt
└── ArbiterBridgeContract/
    ├── include/
    ├── src/           # only if needed
    └── CMakeLists.txt
```

### Suggested target shape
```cmake
add_library(ArbiterBridgeContract INTERFACE)
target_include_directories(ArbiterBridgeContract INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/ArbiterBridgeContract/include
)
```

Use `INTERFACE` unless you truly need compiled native code.

---

## Atlas targets
Recommended native target grouping:

- `AtlasCore`
- `AtlasUI`
- `AtlasEngine`
- `AtlasRuntime`
- `AtlasEditor`

### Recommended dependency flow
```text
AtlasCore -> AtlasUI -> AtlasEngine -> AtlasRuntime -> AtlasEditor
```

A more practical version may be:

```text
AtlasCore
AtlasUI depends on AtlasCore
AtlasEngine depends on AtlasCore
AtlasRuntime depends on AtlasCore + AtlasEngine
AtlasEditor depends on AtlasCore + AtlasEngine + AtlasRuntime + AtlasUI
```

### Important rule
None of these may depend on Arbiter host/app code.

---

## NovaForge targets
Recommended target grouping:

- `NovaForgeGameplay`
- `NovaForgeWorld`
- `NovaForgeTools`
- `NovaForgeIntegrationArbiter`
- `NovaForgeClient`
- `NovaForgeServer`
- `NovaForgeTests`

### Recommended dependency flow
```text
NovaForgeGameplay depends on AtlasEngine + AtlasRuntime
NovaForgeWorld depends on AtlasEngine + NovaForgeGameplay
NovaForgeTools depends on AtlasEditor + NovaForgeGameplay + NovaForgeWorld
NovaForgeIntegrationArbiter depends on ArbiterBridgeContract + AtlasEditor/NovaForgeTools as needed
NovaForgeClient depends on NovaForgeGameplay + NovaForgeWorld + AtlasRuntime
NovaForgeServer depends on NovaForgeGameplay + NovaForgeWorld + AtlasRuntime
NovaForgeTests depends on the targets under test
```

### Important rule
`NovaForgeIntegrationArbiter` must remain optional and editor/developer-facing.

---

## Arbiter targets
If Arbiter remains mostly .NET / WPF / VSIX:

- do **not** try to make it a normal CMake-owned core target
- instead document its build in `Docs/Integration` and in the manifest
- optionally expose helper custom targets from CMake for convenience only

Example convenience targets:
- `ArbiterHostBuild`
- `ArbiterVSIXBuild`

These would shell out to `dotnet build` or MSBuild, but they should not become dependencies of Atlas or NovaForge native targets.

---

# Target ownership map

## Shared
- `ArbiterBridgeContract`

## Atlas
- `AtlasCore`
- `AtlasUI`
- `AtlasEngine`
- `AtlasRuntime`
- `AtlasEditor`

## NovaForge
- `NovaForgeGameplay`
- `NovaForgeWorld`
- `NovaForgeTools`
- `NovaForgeIntegrationArbiter`
- `NovaForgeClient`
- `NovaForgeServer`
- `NovaForgeTests`

## Optional convenience targets
- `ArbiterHostBuild`
- `ArbiterVSIXBuild`

---

# Suggested folder-level CMake layout

```text
MasterRepo/
├── CMakeLists.txt
├── Shared/
│   ├── CMakeLists.txt
│   └── ArbiterBridgeContract/
│       └── CMakeLists.txt
├── Atlas/
│   ├── CMakeLists.txt
│   ├── Core/CMakeLists.txt
│   ├── UI/CMakeLists.txt
│   ├── Engine/CMakeLists.txt
│   ├── Runtime/CMakeLists.txt
│   └── Editor/CMakeLists.txt
├── NovaForge/
│   ├── CMakeLists.txt
│   ├── Gameplay/CMakeLists.txt
│   ├── World/CMakeLists.txt
│   ├── Tools/CMakeLists.txt
│   ├── Integrations/Arbiter/CMakeLists.txt
│   ├── Client/CMakeLists.txt
│   ├── Server/CMakeLists.txt
│   └── Tests/CMakeLists.txt
└── cmake/
    ├── Options.cmake
    ├── CompilerWarnings.cmake
    ├── PlatformConfig.cmake
    └── TestingConfig.cmake
```

---

# Recommended top-level CMakeLists template

```cmake
cmake_minimum_required(VERSION 3.28)

project(MasterRepo LANGUAGES CXX)

include(cmake/Options.cmake)
include(cmake/PlatformConfig.cmake)
include(cmake/CompilerWarnings.cmake)

add_subdirectory(Shared)
add_subdirectory(Atlas)
add_subdirectory(NovaForge)

if(MASTERREPO_BUILD_TESTS)
    include(CTest)
    enable_testing()
endif()
```

Keep it small. Avoid embedding project-specific conditions directly in the root file.

---

# Shared CMake plan

## `Shared/CMakeLists.txt`
```cmake
add_subdirectory(ArbiterBridgeContract)
```

## `Shared/ArbiterBridgeContract/CMakeLists.txt`
```cmake
add_library(ArbiterBridgeContract INTERFACE)

target_include_directories(ArbiterBridgeContract
    INTERFACE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_features(ArbiterBridgeContract INTERFACE cxx_std_20)
```

### When to keep this as INTERFACE
Use `INTERFACE` if the contract is just:
- headers
- enums
- structs
- docs/schemas

### When to switch to STATIC
Switch only if you add:
- serialization helpers
- protocol validation code
- compiled adapters

Keep that pressure low.

---

# Atlas CMake plan

## `Atlas/CMakeLists.txt`
```cmake
add_subdirectory(Core)
add_subdirectory(UI)
add_subdirectory(Engine)
add_subdirectory(Runtime)

if(ATLAS_ENABLE_EDITOR AND MASTERREPO_BUILD_EDITOR)
    add_subdirectory(Editor)
endif()
```

## Example target wiring

### `Atlas/Core/CMakeLists.txt`
```cmake
add_library(AtlasCore STATIC
    # source files
)

target_include_directories(AtlasCore PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_features(AtlasCore PUBLIC cxx_std_20)
```

### `Atlas/UI/CMakeLists.txt`
```cmake
add_library(AtlasUI STATIC
    # source files
)

target_link_libraries(AtlasUI
    PUBLIC
        AtlasCore
)
```

### `Atlas/Engine/CMakeLists.txt`
```cmake
add_library(AtlasEngine STATIC
    # source files
)

target_link_libraries(AtlasEngine
    PUBLIC
        AtlasCore
)
```

### `Atlas/Runtime/CMakeLists.txt`
```cmake
add_library(AtlasRuntime STATIC
    # source files
)

target_link_libraries(AtlasRuntime
    PUBLIC
        AtlasCore
        AtlasEngine
)
```

### `Atlas/Editor/CMakeLists.txt`
```cmake
add_library(AtlasEditor STATIC
    # source files
)

target_link_libraries(AtlasEditor
    PUBLIC
        AtlasCore
        AtlasUI
        AtlasEngine
        AtlasRuntime
)
```

---

# NovaForge CMake plan

## `NovaForge/CMakeLists.txt`
```cmake
add_subdirectory(Gameplay)
add_subdirectory(World)

if(MASTERREPO_BUILD_TOOLS AND MASTERREPO_BUILD_EDITOR)
    add_subdirectory(Tools)
endif()

if(NOVAFORGE_ENABLE_ARBITER_INTEGRATION AND MASTERREPO_BUILD_EDITOR)
    add_subdirectory(Integrations/Arbiter)
endif()

if(MASTERREPO_BUILD_CLIENT)
    add_subdirectory(Client)
endif()

if(MASTERREPO_BUILD_SERVER)
    add_subdirectory(Server)
endif()

if(MASTERREPO_BUILD_TESTS)
    add_subdirectory(Tests)
endif()
```

## Example target wiring

### `NovaForge/Gameplay/CMakeLists.txt`
```cmake
add_library(NovaForgeGameplay STATIC
    # source files
)

target_link_libraries(NovaForgeGameplay
    PUBLIC
        AtlasCore
        AtlasEngine
        AtlasRuntime
)
```

### `NovaForge/World/CMakeLists.txt`
```cmake
add_library(NovaForgeWorld STATIC
    # source files
)

target_link_libraries(NovaForgeWorld
    PUBLIC
        NovaForgeGameplay
        AtlasEngine
)
```

### `NovaForge/Tools/CMakeLists.txt`
```cmake
add_library(NovaForgeTools STATIC
    # source files
)

target_link_libraries(NovaForgeTools
    PUBLIC
        NovaForgeGameplay
        NovaForgeWorld
        AtlasEditor
)
```

### `NovaForge/Integrations/Arbiter/CMakeLists.txt`
```cmake
add_library(NovaForgeIntegrationArbiter STATIC
    include/ArbiterBridgeService.h
    src/ArbiterBridgeService.cpp
)

target_include_directories(NovaForgeIntegrationArbiter
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(NovaForgeIntegrationArbiter
    PUBLIC
        ArbiterBridgeContract
        AtlasEditor
        NovaForgeTools
)
```

### Important integration guard
Only compile `NovaForgeIntegrationArbiter` when:
- editor build is enabled
- Arbiter integration is enabled
- shipping-safe exclusion rules permit it

Add compile definitions such as:

```cmake
target_compile_definitions(NovaForgeIntegrationArbiter
    PUBLIC
        NOVAFORGE_WITH_ARBITER_BRIDGE=1
)
```

---

# Client and server executable plan

## `NovaForge/Client/CMakeLists.txt`
```cmake
add_executable(NovaForgeClient
    # client entry / source files
)

target_link_libraries(NovaForgeClient
    PRIVATE
        NovaForgeGameplay
        NovaForgeWorld
        AtlasRuntime
)
```

## `NovaForge/Server/CMakeLists.txt`
```cmake
add_executable(NovaForgeServer
    # server entry / source files
)

target_link_libraries(NovaForgeServer
    PRIVATE
        NovaForgeGameplay
        NovaForgeWorld
        AtlasRuntime
)
```

## Shipping rule
Do **not** link `NovaForgeIntegrationArbiter` into:
- `NovaForgeClient`
- `NovaForgeServer`

If you need editor-side integration, wire it into:
- editor tooling modules
- dev utilities
- editor-only builds

---

# Editor-side composition plan

There are two good patterns here.

## Pattern A — AtlasEditor hosts NovaForge editor tooling
Use `AtlasEditor` plus `NovaForgeTools` and optional `NovaForgeIntegrationArbiter`.

Example:
```cmake
add_executable(NovaForgeEditor
    # editor app entry point
)

target_link_libraries(NovaForgeEditor
    PRIVATE
        AtlasEditor
        NovaForgeGameplay
        NovaForgeWorld
        NovaForgeTools
)
```

Optionally:
```cmake
if(NOVAFORGE_ENABLE_ARBITER_INTEGRATION)
    target_link_libraries(NovaForgeEditor
        PRIVATE
            NovaForgeIntegrationArbiter
    )
endif()
```

## Pattern B — AtlasEditor remains generic, NovaForgeTools loaded by configuration
This is better if you want Atlas to stay very reusable.
The editor stays generic, and NovaForge project tooling is loaded on project open.

That is the stronger long-term direction.

---

# Build option guards and compile definitions

## Recommended option names

```cmake
option(MASTERREPO_BUILD_EDITOR "Build editor components" ON)
option(MASTERREPO_BUILD_CLIENT "Build game client" ON)
option(MASTERREPO_BUILD_SERVER "Build game server" ON)
option(MASTERREPO_BUILD_TESTS "Build tests" ON)
option(MASTERREPO_BUILD_TOOLS "Build developer tools" ON)

option(ATLAS_ENABLE_EDITOR "Enable Atlas editor systems" ON)
option(NOVAFORGE_ENABLE_ARBITER_INTEGRATION "Enable NovaForge Arbiter bridge integration" ON)
option(NOVAFORGE_SHIPPING_BUILD "Configure NovaForge as a shipping build" OFF)
```

## Shipping-safe control example
```cmake
if(NOVAFORGE_SHIPPING_BUILD)
    set(NOVAFORGE_ENABLE_ARBITER_INTEGRATION OFF CACHE BOOL "" FORCE)
endif()
```

---

# Test target plan

## Repo-level testing
Use:
- unit tests near the owning module
- integration tests at the repo/test layer
- build verification for shipping separation

### Suggested tests
- `NovaForgeBridgeContractTests`
- `NovaForgeIntegrationArbiterTests`
- `BuildIsolationTests`
- `TargetDependencyTests`

## Example
```cmake
add_executable(NovaForgeIntegrationArbiterTests
    # test source files
)

target_link_libraries(NovaForgeIntegrationArbiterTests
    PRIVATE
        NovaForgeIntegrationArbiter
)
```

### Important test case
Add a test or CI validation that confirms:
- shipping client/server targets do not link Arbiter integration code

---

# Convenience targets for Arbiter

If Arbiter is built outside CMake, you can still provide convenience targets.

## Example
```cmake
add_custom_target(ArbiterHostBuild
    COMMAND dotnet build ${CMAKE_SOURCE_DIR}/Arbiter/HostApp/HostApp.csproj
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)

add_custom_target(ArbiterVSIXBuild
    COMMAND dotnet build ${CMAKE_SOURCE_DIR}/Arbiter/VisualStudioExtension/YourVsixProject.csproj
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)
```

## Rule
These custom targets must not be linked as dependencies of Atlas or NovaForge shipping targets.

They are developer conveniences only.

---

# CI pipeline implications

## Recommended CI lanes
1. **Native core lane**
   - Shared
   - Atlas
   - NovaForge gameplay/world/client/server
2. **Editor lane**
   - AtlasEditor
   - NovaForgeTools
   - optional NovaForgeIntegrationArbiter
3. **Shipping isolation lane**
   - verify shipping config disables Arbiter integration
4. **Arbiter lane**
   - HostApp build
   - VSIX build
5. **Integration lane**
   - project manifest validation
   - bridge contract validation
   - end-to-end bridge smoke tests

---

# Target naming conventions

Use names that reveal ownership and scope.

## Good examples
- `AtlasCore`
- `AtlasEditor`
- `NovaForgeGameplay`
- `NovaForgeClient`
- `NovaForgeIntegrationArbiter`
- `ArbiterBridgeContract`

## Avoid
- generic names like `CoreLib`
- cross-domain names like `EditorGameToolsLib`
- names that hide ownership

---

# Recommended immediate implementation sequence

1. Create `Shared/CMakeLists.txt`
2. Add `ArbiterBridgeContract` as an `INTERFACE` target
3. Create `Atlas/CMakeLists.txt` with module subdirectories
4. Create `NovaForge/CMakeLists.txt` with guarded subdirectories
5. Add `NovaForgeIntegrationArbiter` behind editor + integration flags
6. Ensure client/server targets do not link integration targets
7. Add a convenience custom target for Arbiter host build
8. Add CI validation for shipping isolation

---

# Minimal example target graph

```text
ArbiterBridgeContract

AtlasCore
AtlasUI --------------------► AtlasCore
AtlasEngine ----------------► AtlasCore
AtlasRuntime ---------------> AtlasCore, AtlasEngine
AtlasEditor ----------------► AtlasCore, AtlasUI, AtlasEngine, AtlasRuntime

NovaForgeGameplay ----------> AtlasCore, AtlasEngine, AtlasRuntime
NovaForgeWorld -------------> NovaForgeGameplay, AtlasEngine
NovaForgeTools -------------> NovaForgeGameplay, NovaForgeWorld, AtlasEditor
NovaForgeIntegrationArbiter -> ArbiterBridgeContract, NovaForgeTools, AtlasEditor

NovaForgeClient ------------> NovaForgeGameplay, NovaForgeWorld, AtlasRuntime
NovaForgeServer ------------> NovaForgeGameplay, NovaForgeWorld, AtlasRuntime
```

### Forbidden graph edges
- `Atlas* -> ArbiterHost`
- `NovaForgeClient -> NovaForgeIntegrationArbiter`
- `NovaForgeServer -> NovaForgeIntegrationArbiter`
- `Atlas* -> Arbiter UI/chat/archive code`
- `Shared -> NovaForge gameplay`

---

# Definition of build-system success

The build plan is successful when:

- target ownership mirrors repo ownership
- Atlas builds independently
- NovaForge builds independently of Arbiter
- Arbiter integration is optional and guarded
- shipping client/server builds exclude Arbiter integration
- Shared remains a tiny, stable contract layer
- CI can validate build isolation cleanly

---

# Practical summary

The build graph should express the architecture directly:

- **Shared** defines the contract
- **Atlas** provides reusable foundations
- **NovaForge** builds the game on Atlas
- **Arbiter** stays optional and external-style
- **NovaForgeIntegrationArbiter** is the only bridge-facing native seam on the NovaForge side

That is the cleanest way to keep the monorepo maintainable while still making Arbiter deeply useful.
