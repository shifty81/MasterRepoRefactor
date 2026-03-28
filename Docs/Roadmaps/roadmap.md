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

## Current Status

```
Tests passing: 7 C++ integration tests · 263 Python unit tests
Source files:  ~2,370 C++ · 210 Python · 35 C# · 23 TypeScript
Architecture:  Stable — all 10 foundation epics complete
Bridge:        REST + WebSocket endpoints operational
AI Engine:     41 modules · 12 LLM backends · agentic self-build loop
```

---

## Near-Term Goals (Active)

### Phase 11 — Engine C++ Subsystem Expansion

The C++ source files are now in place. The next step is wiring them into the CMake build graph and verifying each subsystem compiles and links correctly.

- [ ] Wire `Atlas/Engine/Rendering/` into `AtlasEngine` CMake target
- [ ] Wire `Atlas/Engine/Scene/` + `Atlas/Engine/Scripting/` into target
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
