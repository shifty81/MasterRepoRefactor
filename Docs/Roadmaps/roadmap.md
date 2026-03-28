# Project Roadmap

> **Design canon:** [Docs/Design/MASTER_DESIGN_DOCUMENT.md](../Design/MASTER_DESIGN_DOCUMENT.md)
> **Architecture:** [Docs/Architecture/monorepo_layout.md](../Architecture/monorepo_layout.md)

---

## Completed Phases

### Foundation Epics (Epics 1–10) ✅

All ten foundation epics have been executed and are stable.

| Epic | Title | Key Outcomes |
|------|-------|--------------|
| 1 | Lock the monorepo architecture | Ownership zones defined; boundary, dependency, and shipping-separation rules documented |
| 2 | Restructure the repo physically | Atlas, NovaForge, AtlasAI, Shared directories established; code migrated to correct zones |
| 3 | Stand up the bridge backbone | `AtlasBridgeContract` shared types; bridge transport model documented; NovaForge integration scaffolded |
| 4 | Wire the first usable endpoints | `/project/info`, `/editor/selection`, `/build/run`, `/editor/tools/run` operational |
| 5 | Refactor NovaForge into callable modules | Monolithic startup split; project context isolated; editor tool hooks separated |
| 6 | Refactor Arbiter → AtlasAI | Folder rename complete; all C++/C#/CMake/docs updated |
| 7 | Build system cleanup | CMake structure updated; AtlasAI optional; editor/tooling separated from shipping |
| 8 | Safety, logging, and operational controls | Action allowlist; dry-run defaulted true; audit logging; local trust guard |
| 9 | First real workflow milestone | AtlasAI reads project info, queries editor state, launches safe build, runs safe editor tool |
| 10 | Second-wave improvements | Search roots; richer editor snapshots; codegen proposal workflow; workspace dashboard |

---

### Zip File Migration ✅ COMPLETE

All 7 source zips committed to `New Implementations that need addressed/` have been fully processed.

| Zip File | Size | Status | Content Migrated To |
|----------|------|--------|---------------------|
| `ArbiterAI-main.zip` | 397 KB | ✅ Done | `AtlasAI/AIEngine/PythonBridge/`, `AtlasAI/AIEngine/Memory/`, `AtlasAI/Projects/`, `AtlasAI/WebhookIntegration/` |
| `Arbiter-main.zip` | 12.2 MB | ✅ Done | `AtlasAI/Installer/`, `AtlasAI/VisualStudioExtension/`, `Docs/` |
| `NovaForge-main.zip` | 73.6 MB | ✅ Done | `Atlas/Engine/`, `Atlas/Editor/`, `NovaForge/Client/`, `NovaForge/Server/`, `NovaForge/Tests/AtlasTests/`, `NovaForge/Data/`, `NovaForge/Docs/`, `NovaForge/Tools/AIDev/` |
| `MasterRepo-main.zip` | 30.2 MB | ✅ Done | `.github/ISSUE_TEMPLATE/` |
| `arbiter_novaforge_starter_files.zip` | 5 KB | ✅ Done | `AtlasAI/ProjectAdapters/NovaForge/`, `NovaForge/Integrations/AtlasAI/` |
| `masterrepo_first_pass_monorepo_files.zip` | 3.6 KB | ✅ Done | CMake skeleton, `Shared/`, `NovaForge/Integrations/` stubs |
| `masterrepo_second_pass_cmake_templates.zip` | 8.3 KB | ✅ Done | CMake templates, `Docs/SECOND_PASS_NOTES.md`, expanded NovaForge CMakeLists |

**Files migrated:** ~2,750+ across all zips. **All Arbiter→AtlasAI renames applied.**

---

### Additional Infrastructure Added ✅

| Component | Status | Notes |
|-----------|--------|-------|
| AtlasAI PythonBridge | ✅ Done | FastAPI server — chat, LLM, TTS/STT, model downloader, web UI |
| AtlasAI Installer | ✅ Done | Inno Setup script + PowerShell build helper for Windows |
| AtlasAI WebhookIntegration | ✅ Done | TypeScript Express bridge: Jira / Azure Boards / Linear |
| Atlas/Engine C++ sources | ✅ Done | 88 files: animation, assets, audio, camera, core, ecs, graphvm, input, net, physics, plugin, sim, world |
| Atlas/Editor C++ sources | ✅ Done | 73 files: AI backends, panels, tools, UI framework |
| NovaForge/Server tests | ✅ Done | 529 gameplay test `.cpp` files |
| NovaForge/Client | ✅ Done | Shaders, assets, tests, external libs, build scripts |
| NovaForge Blender Generator | ✅ Done | 45-module procedural ship/asteroid/character generator |
| GitHub Issue Templates | ✅ Done | Build failure template |
| Professional README | ✅ Done | SVG logos, architecture diagram, full feature showcase |

---

## New Zip Packs Integrated ✅ COMPLETE

All 19 root-level zip packs audited and fully committed.  The duplicate
`MasterRepo_Gameplay_Foundation_Pack (1).zip` was skipped.  All zips moved to
`Docs/Archive/ZipFiles/`.

| Zip Pack | Contents Migrated To |
|----------|----------------------|
| `MasterRepo_Phase2_Runtime_Pack.zip` | `NovaForge/Server/Source/` — Core, World, Entity, Voxel, Modules, Rendering, Tooling |
| `MasterRepo_Phase3_1_Integration_Pack.zip` | `NovaForge/Server/Source/` — Core + World integration; `NovaForge/Data/Definitions/` items/recipes/missions/factions |
| `MasterRepo_Phase3_Full_Pack.zip` | `NovaForge/Server/Source/` — Input, HUD UI, Gameplay session, ShipInterior |
| `MasterRepo_Phase4_EVA_Airlock_Tether_Foundation_Pack.zip` | `NovaForge/Server/Source/Gameplay/EVA` + Airlock + Tether + Environment |
| `MasterRepo_Phase5_Salvage_Mining_Pack.zip` | `NovaForge/Server/Source/Gameplay/Salvage` + Mining |
| `MasterRepo_Phase6_PCG_Pack.zip` | `NovaForge/Server/Source/PCG/` + `NovaForge/Data/PCG/` |
| `MasterRepo_Phase7_Economy_Progression_Pack.zip` | `NovaForge/Server/Source/Gameplay/Economy` + Progression + Upgrades |
| `MasterRepo_Phase8_Factions_Contracts_Trade_Pack.zip` | `NovaForge/Server/Source/Gameplay/Factions` + Contracts + Trade + WorldSim |
| `MasterRepo_Phase9_Stations_Manufacturing_Storage_Pack.zip` | `NovaForge/Server/Source/Gameplay/Stations` + Manufacturing + Storage + Services |
| `MasterRepo_Phase10_Fleet_Ship_Progression_Meta_Pack.zip` | `NovaForge/Server/Source/Gameplay/Fleet` + Ships + Meta |
| `MasterRepo_Phase11_Sector_War_Anomaly_Pack.zip` | `NovaForge/Server/Source/Gameplay/Sectors` + War + Anomalies |
| `MasterRepo_Phase12_Titan_Endgame_Season_Pack.zip` | `NovaForge/Server/Source/Gameplay/Titan` + Endgame + Season |
| `MasterRepo_Phase12_1_Season_Config_Patch_Pack.zip` | `NovaForge/Server/Source/Config` + Season patch; `NovaForge/Data/Config/` |
| `MasterRepo_Phase13_Vertical_Slice_Pack.zip` | `NovaForge/Server/Source/Core/GameOrchestrator`, UI, Save, Integration, Debug |
| `MasterRepo_Legacy_Adapter_Pack.zip` | `NovaForge/Server/Source/LegacyAdapters/` — full legacy migration layer |
| `MasterRepo_NovaForge_First_Live_Ingestion_Pass.zip` | `NovaForge/Data/LegacyIngested/` + ingestion manifest |
| `MasterRepo_DataRegistry_Expansion_Pack.zip` | `NovaForge/Server/Source/Data/DataRegistry.cpp` + DataRecordModels |
| `MasterRepo_Gameplay_Foundation_Pack.zip` | `NovaForge/Server/Source/Gameplay/` — PlayerController, Inventory, Crafting, Mission, GameplayManager, UI hooks |
| `MasterRepo_Master_Delivery_Bundle.zip` | `Docs/Architecture/` — 6 architectural design docs (Entity/Component, Rendering, Save/Load, Networking, Security, Gap Closure) |

**Root directory cleanup:** `docs/` (architecture specs) → `Docs/Architecture/`; empty `src/` and `tests/` placeholders removed.

---

## Logging Infrastructure ✅ COMPLETE

Proper logging wired into every executable and runnable component across the project.

### Shared Logging Utilities

| File | Purpose |
|------|---------|
| `Scripts/Logging/log_helper.sh` | Bash library sourced by all shell scripts — `log_init` creates a timestamped log file and tees all stdout+stderr; `log_section` emits labelled dividers |
| `Shared/Logging/MasterLogger.h` | C++17 header-only singleton — dual console+file output, five severity levels (DEBUG/INFO/WARN/ERROR/FATAL), thread-safe, ISO 8601 timestamps, convenience macros `MR_LOG_*` |
| `Shared/Logging/log_utils.py` | Python utility for tools outside AtlasAI — `get_tool_logger(name, subsystem)` creates rotating file + console handler under `Logs/<subsystem>/` |

### Log Directory Layout

```
<repo_root>/
├── Logs/                      ← top-level runtime log tree (git-ignored)
│   ├── build/                 ← Scripts/Build/build.sh, clean.sh, test.sh
│   ├── ci/                    ← Scripts/CI/ci_build.sh, ci_validate.sh
│   ├── setup/                 ← Scripts/Setup/setup.sh, Scripts/Bootstrap/bootstrap.sh
│   ├── validate/              ← validate_naming.py, validate_boundaries.py
│   ├── game_tools/            ← contract_scan.py, validate_json.py
│   ├── ai_dev/                ← agent_loop.py
│   └── tools/                 ← generic tool default
├── AtlasAI/AIEngine/AtlasAIEngine/logs/
│   ├── arbiter_engine/        ← server.py
│   ├── python_bridge/         ← fastapi_bridge.py  ← NOW LOGGING
│   ├── host_app/
│   ├── vs_extension/
│   └── self_build/
├── NovaForge/Server/logs/     ← server build + test shell scripts
└── NovaForge/Client/logs/     ← client build scripts
```

### Components Hooked

| Component | Type | Logging Method |
|-----------|------|----------------|
| `Scripts/Build/build.sh` | Bash | `log_helper.sh` → `Logs/build/build_<ts>.log` |
| `Scripts/Build/clean.sh` | Bash | `log_helper.sh` → `Logs/build/build_<ts>.log` |
| `Scripts/Build/test.sh` | Bash | `log_helper.sh` → `Logs/test/test_<ts>.log` |
| `Scripts/CI/ci_build.sh` | Bash | `log_helper.sh` → `Logs/ci/ci_<ts>.log` |
| `Scripts/CI/ci_validate.sh` | Bash | `log_helper.sh` → `Logs/ci/ci_<ts>.log` |
| `Scripts/Setup/setup.sh` | Bash | `log_helper.sh` → `Logs/setup/setup_<ts>.log` |
| `Scripts/Bootstrap/bootstrap.sh` | Bash | `log_helper.sh` → `Logs/setup/setup_<ts>.log` |
| `Scripts/Validate/validate_naming.py` | Python | `log_utils.py` → `Logs/validate/validate.log` |
| `Scripts/Validate/validate_boundaries.py` | Python | `log_utils.py` → `Logs/validate/validate.log` |
| `NovaForge/Tools/GameTools/contract_scan.py` | Python | `log_utils.py` → `Logs/game_tools/game_tools.log` |
| `NovaForge/Tools/GameTools/validate_json.py` | Python | `log_utils.py` → `Logs/game_tools/game_tools.log` |
| `NovaForge/Tools/AIDev/core/agent_loop.py` | Python | `log_utils.py` → `Logs/ai_dev/ai_dev.log` |
| `AtlasAI/AIEngine/PythonBridge/fastapi_bridge.py` | Python | Inline rotating handler → `Logs/python_bridge/python_bridge.log` |
| `AtlasAI/AIEngine/AtlasAIEngine/server.py` | Python | `core/logger.py` → `logs/arbiter_engine/arbiter_engine.log` (existing) |
| `NovaForge/Server/Source/main.cpp` | C++ | `MasterLogger.h` → `Logs/server/masterrepo_server.log` |
| `NovaForge/Server/Source/Core/App.cpp` | C++ | `MasterLogger.h` (via Init in main) |
| `NovaForge/Server/Source/Core/EngineKernel.cpp` | C++ | `MasterLogger.h` (via Init in main) |
| `NovaForge/Server/build.sh` | Bash | Existing tee → `logs/server_build_<ts>.log` |
| `NovaForge/Server/run_tests.sh` | Bash | Existing tee → `logs/server_tests_<ts>.log` |
| `NovaForge/Client/build_test*.sh` | Bash | Existing tee → `logs/` |

---

## Current Status

```
Tests passing:  7 C++ integration tests · 352 Python unit tests
Source files:  ~2,650 C++ · 215 Python · 35 C# · 23 TypeScript
Architecture:  Stable — all 10 foundation epics complete
Bridge:        REST + WebSocket endpoints operational
AI Engine:     41 modules · 12 LLM backends · agentic self-build loop
Logging:       Unified across all shell scripts, Python tools, and C++ runtime
Character:     Phase 1 + Phase 2 character systems migrated (Equipment, Animation, IK, FPS, Mech)
Editor:        T1-T3 foundation migrated (Core, Input, Camera, Selection, Outliner, Inspector, Gizmos)
Orchestration: Unified repo consolidation migrated (App, GameOrchestrator, World, Renderer, Save, UI)
```

---

### Root-Level Zip Migration ✅ COMPLETE (Session 8)

All 4 root-level zip packs migrated:

| Zip File | Status | Content Migrated To |
|----------|--------|---------------------|
| `MasterRepo_Unified_Repo_Consolidation_Pack.zip` | ✅ Done | `NovaForge/App/` (App, GameOrchestrator, DataRegistry), `NovaForge/World/`, `NovaForge/Save/`, `NovaForge/UI/`, `Atlas/Engine/Rendering/`, `Atlas/Editor/EditorShell`, `NovaForge/Data/Config/`, `Docs/Architecture/` |
| `MasterRepo_T1_T3_Editor_Foundation_Pack.zip` | ✅ Done | `Atlas/Editor/Core/`, `Atlas/Editor/Input/`, `Atlas/Editor/Camera/`, `Atlas/Editor/Selection/`, `Atlas/Editor/Outliner/`, `Atlas/Editor/Inspector/`, `Atlas/Editor/Gizmos/`, `Atlas/Config/Editor/` |
| `MasterRepo_Character_System_Pack.zip` | ✅ Done | `NovaForge/Gameplay/Characters/` (CharacterSystem, CharacterControllerShell, Animation, Equipment, Mech), `NovaForge/Data/Definitions/Characters,Equipment,Animation/` |
| `MasterRepo_Character_Phase2_Pack.zip` | ✅ Done | `NovaForge/Gameplay/Characters/Core/` (StateAuthority, TransitionRules), `Characters/IK/`, `Characters/FPS/`, `Characters/Editor/`, `Characters/Tools/`, `NovaForge/Data/Definitions/IK,Tools/` |

---

## Near-Term Goals (Active)

### Phase 11 — Engine C++ Subsystem Expansion

The C++ source files are now in place. The next step is wiring them into the CMake build graph and verifying each subsystem compiles and links correctly.

- [x] Wire `Atlas/Engine/Rendering/` into `AtlasEngine` CMake target
- [ ] Wire `Atlas/Engine/Scene/` + `Atlas/Engine/Scripting/` into target
- [x] Wire `Atlas/Editor/Core/`, `Input/`, `Camera/`, `Selection/`, `Outliner/`, `Inspector/`, `Gizmos/` into `AtlasEditor` target
- [ ] Wire `Atlas/Editor/Panels/` + `Atlas/Editor/EditorServices/AI/` into `AtlasEditor` target
- [ ] Add `Atlas/Editor/Framework/UI/` to `AtlasUI` target
- [ ] Resolve any missing includes from external deps (glm, stb, etc.)
- [ ] Run full engine build smoke test

### Phase 12 — NovaForge Client/Server CMake Wiring

The server and client source trees are populated. Next: integrate with the CMake build.

- [ ] Wire `NovaForge/Client/App/` into `NovaForgeApp` CMake target
- [ ] Wire `NovaForge/Client/App/shaders/` into shader compile step
- [ ] Wire `NovaForge/Server/tests/` test suite into CTest
- [ ] Verify `NovaForge/Client/App/external/` (tinygltf, nlohmann/json, sol2) links correctly
- [ ] Add server config/whitelist validation test

### Phase 13 — AtlasAI Live Integration

- [ ] Live viewport attachment (`supportsViewportAttach` capability)
- [ ] Hot-reload / live patch workflow (`supportsLivePatch`)
- [ ] Multi-workspace support (parallel bridge sessions)
- [ ] Expand codegen loop to accept diffs from AI-proposed changes
- [ ] PythonBridge → WebSocket event relay for real-time build streaming

### Phase 14 — Testing & CI Hardening

- [ ] Add unit tests for all bridge endpoint handlers (ProjectService, EditorService, BuildService)
- [ ] Add integration tests that spin up the FastAPI bridge and exercise each endpoint
- [ ] Add TypeScript Jest coverage for WebhookIntegration
- [ ] Set up GitHub Actions CI: CMake build → CTest → Python pytest → TypeScript Jest
- [ ] Add schema validation tests (JSON round-trip against `Shared/ToolProtocol/schemas/`)
- [ ] Automate audit log rotation and workspace snapshot exports

### Phase 15 — Character + Gameplay Loop Hookup

- [ ] Connect `CharacterSystem` to `PlayerController` (movement mode dispatch)
- [ ] Connect `EquipmentSystem` to mining tool interaction (`ToolInteractionShell`)
- [ ] Wire `IKSystem` into character animation pipeline
- [ ] Wire `FPSPresentationSystem` into runtime rendering
- [ ] Connect `CharacterEditorSystem` to editor mode controller
- [ ] Add `MechPossessionSystem` vehicle entry/exit events to gameplay loop
- [ ] Connect `GameOrchestrator` boot path to `NovaForgeBootstrap`
- [ ] Wire `SaveManager` into world serialization
- [ ] Wire `RuntimeUIShell` into HUD display path

---

## Long-Term Vision

### Full Codegen Workflow

Human-in-the-loop AI code generation: AtlasAI proposes a change → diff is shown in the IDE → user approves → patch is applied. The codegen planner (Epic 10) is the foundation; Phases 13–14 complete the loop.

### Multi-Workspace & Multi-Project Support

A single AtlasAI instance managing multiple concurrent project workspaces, each with an independent bridge session. Atlas engine work and NovaForge game work managed from one shell.

### Expanded PCG & Builder Tooling

The `BuilderToolActionId` second-wave actions provide scaffolding for deep PCG integration — preview mesh generation, builder entity validation, diagnostics — all accessible from AtlasAI without leaving the workspace.

### Shipping & Distribution

The Inno Setup installer (`AtlasAI/Installer/atlasai_setup.iss`) bundles the full AtlasAI stack into a single Windows `.exe`. Long-term: automated CI build of the installer on every tagged release.

### NovaForge Public Release

Once the engine, editor, and game systems are production-ready, NovaForge ships as a standalone title. The Atlas engine and AtlasAI tooling remain open source; the game content follows a separate distribution model.

---

## Document Index

| Document | Path |
|----------|------|
| Master Design Document | [Docs/Design/MASTER_DESIGN_DOCUMENT.md](../Design/MASTER_DESIGN_DOCUMENT.md) |
| Missing Systems Addendum | [Docs/Design/MISSING_SYSTEMS_ADDENDUM.md](../Design/MISSING_SYSTEMS_ADDENDUM.md) |
| Monorepo Layout | [Docs/Architecture/monorepo_layout.md](../Architecture/monorepo_layout.md) |
| Dependency Rules | [Docs/Architecture/dependency_rules.md](../Architecture/dependency_rules.md) |
| Repo Boundaries | [Docs/Architecture/repo_boundaries.md](../Architecture/repo_boundaries.md) |
| Shipping Separation | [Docs/Architecture/shipping_separation.md](../Architecture/shipping_separation.md) |
| AtlasAI Bridge | [Docs/Integration/atlasai_bridge.md](../Integration/atlasai_bridge.md) |
| Tool Protocol | [Docs/Integration/tool_protocol.md](../Integration/tool_protocol.md) |
| Project Manifest Spec | [Docs/Integration/project_manifest_spec.md](../Integration/project_manifest_spec.md) |
| CROSSPLATFORM | [Docs/CROSSPLATFORM.md](../CROSSPLATFORM.md) |
| GUI Architecture | [Docs/GUI.md](../GUI.md) |
