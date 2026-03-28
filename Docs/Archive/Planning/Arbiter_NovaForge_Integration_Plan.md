# Arbiter ↔ NovaForge Integration & Refactor Plan

## Purpose
This document defines a repo-ready plan for integrating **Arbiter-main** with **NovaForge-main** without tangling AI tooling, editor/runtime code, or shipping gameplay binaries.

The target model is:

- **Arbiter** = external AI tooling cockpit, workflow host, IDE shell, archive/memory, VS integration
- **NovaForge** = game project, Atlas engine/editor/client/server/data
- **Bridge** = thin interop boundary between them

---

## 1. Grounded repository observations

### Arbiter-main currently contains
- `HostApp/` WPF shell and windows:
  - `MainWindow.xaml`
  - `IdeWindow.xaml`
  - `LauncherWindow.xaml`
  - `ProjectWindow.xaml`
  - `WorkspaceWindow.xaml`
  - `PdfViewerWindow.xaml`
  - `SettingsWindow.xaml`
- `AIEngine/ArbiterEngine/`
- `AIEngine/PythonBridge/`
- `Memory/ConversationLogs/`
- `Projects/Novaforge/`
- `Projects/SteamServerAdmin/`
- `VisualStudioExtension/ArbiterVSIX/`
- `archive/`
- `docs/design/`
- `docs/wiki/`

### NovaForge-main currently contains
- `engine/`
- `editor/`
  - `editor/ai/`
  - `editor/panels/`
  - `editor/tools/`
  - `editor/ui/`
- `cpp_client/`
- `cpp_server/`
- `cpp_common/`
- `data/`
- `schemas/`
- `tools/`
- `docs/`
- `ai_dev/`
- `atlas_tests/`

### Existing NovaForge signs that already support this direction
- `docs/ATLAS_INTEGRATION.md`
- `docs/GUI_ARCHITECTURE.md`
- `docs/EDITOR_TOOLS.md`
- `schemas/atlas.project.v1.json`
- `schemas/atlas.build.v1.json`
- strong test coverage in `atlas_tests/`
- editor AI area already exists in `editor/ai/`

---

## 2. Integration principles

1. **NovaForge must build and run without Arbiter installed.**
2. **Arbiter must never be a hard runtime dependency of client or server binaries.**
3. **Editor/runtime/gameplay code stays in NovaForge.**
4. **Chat, archive, planning, orchestration, project shell, and automation stay in Arbiter.**
5. **Only a narrow bridge layer may connect the two.**
6. **All AI-driven file/code modifications must go through reviewable actions.**
7. **No WPF code inside Atlas/NovaForge engine/editor runtime.**
8. **Shipping builds must be able to compile with bridge support disabled.**

---

## 3. Target architecture

### 3.1 Responsibility split

#### Arbiter owns
- AI chat UX
- workspace/project selection
- archives and memory
- document viewing
- build orchestration
- IDE/VS integration
- task execution and tool routing
- developer automation
- design/doc/code search and summarization

#### NovaForge owns
- Atlas engine code
- custom editor UI and viewport tooling
- gameplay systems
- project data and schemas
- client/server networking and simulation
- PCG/game asset systems
- game-facing AI/editor tools

#### Bridge owns
- command schemas
- project capability metadata
- action/result envelopes
- safe editor tool invocation
- build and analysis request transport
- state snapshots for selection, logs, and tool discovery

---

## 4. Required refactor: repo boundaries

### 4.1 Arbiter refactor target
Refactor Arbiter from project-specific shell code into a reusable host plus project adapters.

#### New target structure
```text
Arbiter-main/
  HostApp/
    Modules/
      Chat/
      Workspace/
      ProjectShell/
      Logs/
      Build/
      Git/
      Documents/
      Settings/
      Theme/
      Actions/
  AIEngine/
    ArbiterEngine/
      core/
      llm/
      tools/
      memory/
      planning/
  ProjectAdapters/
    NovaForge/
      NovaForgeProjectAdapter.cs
      NovaForgeManifest.cs
      NovaForgeCapabilityMap.cs
      NovaForgeBridgeClient.cs
      NovaForgeToolCatalog.cs
  VisualStudioExtension/
    ArbiterVSIX/
```

### 4.2 NovaForge refactor target
Create an isolated Arbiter integration zone.

#### New target structure
```text
NovaForge-main/
  engine/
  editor/
  cpp_client/
  cpp_server/
  cpp_common/
  data/
  docs/
  schemas/
  tools/
  integrations/
    arbiter/
      include/
        ArbiterBridge/
          ArbiterBridgeTypes.h
          ArbiterCapabilityRegistry.h
          ArbiterCommandRouter.h
          ArbiterEditorHooks.h
          ArbiterProjectContext.h
      src/
        ArbiterCapabilityRegistry.cpp
        ArbiterCommandRouter.cpp
        ArbiterEditorHooks.cpp
        ArbiterProjectContext.cpp
      config/
        arbiter_bridge.json
      tests/
        test_arbiter_bridge.cpp
```

---

## 5. Bridge contract

Create a shared bridge contract first. Do not move feature code before this exists.

### 5.1 Command categories
- project info
- capability discovery
- build requests
- analysis/lint/validation
- file open/navigation
- editor selection snapshots
- editor tool discovery
- editor tool execution
- asset generation requests
- structured log streaming

### 5.2 Initial command set

#### Requests
- `GetProjectInfo`
- `GetCapabilities`
- `GetBuildTargets`
- `BuildTarget`
- `AnalyzeFile`
- `ValidateData`
- `OpenFile`
- `SearchDocs`
- `GetEditorSelection`
- `ListEditorTools`
- `RunEditorTool`
- `RequestAssetGeneration`
- `GetRecentLogs`

#### Responses
- `ProjectInfoResponse`
- `CapabilityListResponse`
- `BuildResultResponse`
- `AnalysisResultResponse`
- `ValidationResultResponse`
- `OpenFileResultResponse`
- `EditorSelectionResponse`
- `EditorToolListResponse`
- `EditorToolRunResultResponse`
- `AssetGenerationResultResponse`
- `RecentLogsResponse`

### 5.3 Suggested C++ types in NovaForge
```cpp
struct ArbiterRequestHeader;
struct ArbiterResponseHeader;
struct ArbiterProjectInfo;
struct ArbiterCapabilityDescriptor;
struct ArbiterBuildRequest;
struct ArbiterBuildResult;
struct ArbiterAnalysisRequest;
struct ArbiterAnalysisResult;
struct ArbiterEditorSelectionSnapshot;
struct ArbiterToolInvocation;
struct ArbiterToolResult;
```

### 5.4 Suggested C# types in Arbiter
```csharp
public sealed class ArbiterBridgeEnvelope;
public sealed class NovaForgeProjectInfo;
public sealed class NovaForgeCapabilityDescriptor;
public sealed class NovaForgeBuildRequest;
public sealed class NovaForgeBuildResult;
public sealed class NovaForgeEditorSelectionSnapshot;
public sealed class NovaForgeToolInvocation;
public sealed class NovaForgeToolResult;
```

---

## 6. Transport recommendation

### Phase 1 transport
Use **local HTTP** or **named pipes**.

### Recommendation
- Use **HTTP localhost** first for easier debugging.
- Move to named pipes later only if needed for tighter local integration.

### Initial endpoint layout
- `GET /project/info`
- `GET /project/capabilities`
- `GET /build/targets`
- `POST /build/run`
- `POST /analysis/file`
- `POST /validation/data`
- `POST /files/open`
- `GET /editor/selection`
- `GET /editor/tools`
- `POST /editor/tools/run`
- `POST /assets/request`
- `GET /logs/recent`

### Constraints
- bind to `127.0.0.1` only by default
- disabled by default in shipping builds
- explicit config toggle in editor/dev builds
- request auth token in local config if remote access is ever added

---

## 7. Project manifest system

NovaForge already has schema direction. Expand it so Arbiter can treat NovaForge as a managed workspace instead of a hardcoded project.

### 7.1 Add or extend manifest file
Create:
- `NovaForge-main/integrations/arbiter/config/novaforge.project.json`

### 7.2 Suggested contents
```json
{
  "projectId": "novaforge",
  "displayName": "NovaForge",
  "repoRoot": ".",
  "engineRoot": "engine",
  "editorRoot": "editor",
  "clientRoot": "cpp_client",
  "serverRoot": "cpp_server",
  "docsRoot": "docs",
  "dataRoot": "data",
  "schemasRoot": "schemas",
  "buildTargets": [
    "editor",
    "client",
    "server",
    "tests"
  ],
  "bridge": {
    "transport": "http",
    "endpoint": "http://127.0.0.1:8005"
  },
  "capabilities": [
    "chat",
    "build",
    "analyze_file",
    "validate_data",
    "open_file",
    "query_editor_selection",
    "list_editor_tools",
    "run_editor_tool",
    "request_asset_generation",
    "read_recent_logs"
  ]
}
```

### 7.3 Arbiter side adapter classes
Implement:
- `NovaForgeManifest.cs`
- `NovaForgeProjectAdapter.cs`
- `NovaForgeBridgeClient.cs`
- `NovaForgeCapabilityMap.cs`

---

## 8. Editor integration strategy

### 8.1 Arbiter UI should handle
- chat threads
- archive browsing
- project switching
- design doc reading
- build/analysis dashboards
- code navigation launch actions
- file/document preview
- high-level automation actions

### 8.2 Atlas/NovaForge editor UI should handle
- viewport
- world editing
- ship building
- PCG previews
- entity/component inspection
- editor panels and toolbars
- live simulation overlays
- custom runtime/debug visualization

### 8.3 Non-goal
Do **not** attempt to make Arbiter’s WPF shell the primary in-engine editor viewport environment.

---

## 9. Exact first-pass class plan

## 9.1 Arbiter classes

### Host shell
- `WorkspaceModule`
- `ProjectShellModule`
- `ChatModule`
- `BuildModule`
- `LogsModule`
- `DocumentModule`
- `ActionCenterModule`

### NovaForge adapter
- `NovaForgeProjectAdapter`
- `NovaForgeManifest`
- `NovaForgeBridgeClient`
- `NovaForgeCapabilityMap`
- `NovaForgeToolCatalog`
- `NovaForgeBuildService`
- `NovaForgeEditorToolService`
- `NovaForgeAnalysisService`

### VS extension alignment
- `NovaForgeSolutionContext`
- `NovaForgeCommandRouter`
- `NovaForgeToolWindowBridge`

## 9.2 NovaForge classes

### Bridge core
- `ArbiterProjectContext`
- `ArbiterCapabilityRegistry`
- `ArbiterCommandRouter`
- `ArbiterBridgeServer`
- `ArbiterBridgeTypes`

### Editor hook layer
- `ArbiterEditorHooks`
- `ArbiterSelectionExporter`
- `ArbiterToolAdapterRegistry`
- `ArbiterLogExporter`

### Action handlers
- `BuildTargetHandler`
- `AnalyzeFileHandler`
- `ValidateDataHandler`
- `OpenFileHandler`
- `GetEditorSelectionHandler`
- `ListEditorToolsHandler`
- `RunEditorToolHandler`
- `RequestAssetGenerationHandler`

---

## 10. Candidate NovaForge editor tools to expose first

Based on the repo structure and tests already present, the safest first exposed tools are editor/data/test oriented rather than gameplay mutation.

### First wave
- data validator
- schema validator
- map editor preview
- PCG preview trigger
- ship module editor opener
- station editor opener
- mission editor opener
- visual diff opener
- camera view tool opener
- lighting control tool opener

### Second wave
- asset palette actions
- NPC spawner tool
- environment control tool
- trade route panel actions
- event timeline tool
- live scene snapshot export

### Third wave
- batch edit proposals
- safe content generation workflows
- AI-suggested changes as patch previews

---

## 11. Safe review workflow for AI-generated changes

All Arbiter-initiated changes must produce one of these outcomes:
- no-op informational response
- file patch proposal
- editor action preview
- explicit build/test report

### Never allow directly by default
- silent code rewrites in core engine
- arbitrary file deletion
- gameplay database mutation without preview
- runtime memory patching
- automatic commits to git main branch

### Required gates
- preview diff
- target file list
- impacted subsystem summary
- optional test/build command before apply
- human approval before write

---

## 12. Build system integration

NovaForge has `CMakeLists.txt`, `CMakePresets.json`, and build scripts already. Use those as the source of truth.

### Arbiter should call
- `scripts/build.sh`
- `scripts/build_all.sh`
- `scripts/build_vs.bat`
- preset-based CMake invocations

### Build target abstraction in Arbiter
Expose these logical build targets:
- `editor`
- `client`
- `server`
- `tests`
- `all`

### Do not do
- duplicate build logic in Arbiter
- create separate unofficial compile pipelines unless strictly for local experiments

---

## 13. Documentation tasks

Create these docs in NovaForge:
- `docs/integrations/ARBITER_BRIDGE.md`
- `docs/architecture/TOOLING_BOUNDARIES.md`
- `docs/architecture/AI_ASSIST_WORKFLOW.md`

Create these docs in Arbiter:
- `docs/design/NOVAFORGE_ADAPTER.md`
- `docs/design/PROJECT_ADAPTER_MODEL.md`
- `docs/design/SAFE_ACTION_PIPELINE.md`

---

## 14. Repo task tickets

## Epic A — Establish boundaries

### A1. Create boundary documentation
**Deliverables**
- NovaForge: `docs/architecture/TOOLING_BOUNDARIES.md`
- Arbiter: `docs/design/PROJECT_ADAPTER_MODEL.md`

**Acceptance criteria**
- defines ownership of chat, editor, runtime, gameplay, AI tooling, and transport
- documents forbidden dependency directions

### A2. Create integration folder in NovaForge
**Deliverables**
- `integrations/arbiter/include/ArbiterBridge/`
- `integrations/arbiter/src/`
- `integrations/arbiter/config/`
- `integrations/arbiter/tests/`

**Acceptance criteria**
- compiles as optional dev-only target
- no effect on shipping builds when disabled

---

## Epic B — Project manifest and capability discovery

### B1. Implement NovaForge manifest
**Deliverables**
- `integrations/arbiter/config/novaforge.project.json`
- schema alignment with `schemas/atlas.project.v1.json`

**Acceptance criteria**
- Arbiter can load project metadata without hardcoding paths

### B2. Implement Arbiter project adapter
**Deliverables**
- `ProjectAdapters/NovaForge/NovaForgeProjectAdapter.cs`
- `ProjectAdapters/NovaForge/NovaForgeManifest.cs`

**Acceptance criteria**
- Arbiter launcher can discover and open NovaForge workspace profile

---

## Epic C — Basic bridge service

### C1. Implement bridge server in NovaForge
**Deliverables**
- `ArbiterBridgeServer`
- `ArbiterCommandRouter`
- config-backed localhost endpoint

**Acceptance criteria**
- responds to `/project/info`, `/project/capabilities`, `/build/targets`

### C2. Implement bridge client in Arbiter
**Deliverables**
- `NovaForgeBridgeClient.cs`

**Acceptance criteria**
- Arbiter can query project info and capabilities from live NovaForge dev session

---

## Epic D — Read-only workflow integration

### D1. File open and navigation
**Deliverables**
- `OpenFileHandler`
- Arbiter command mapping for open/navigate

**Acceptance criteria**
- clicking a file in Arbiter opens correct file/path in the configured editor workflow

### D2. Editor selection snapshots
**Deliverables**
- `ArbiterSelectionExporter`
- `/editor/selection`

**Acceptance criteria**
- Arbiter can display current editor selection context safely

### D3. Tool discovery
**Deliverables**
- `ArbiterToolAdapterRegistry`
- `/editor/tools`

**Acceptance criteria**
- Arbiter lists available editor tools exposed by NovaForge

---

## Epic E — Safe action execution

### E1. Build trigger support
**Deliverables**
- `BuildTargetHandler`
- Arbiter build panel integration

**Acceptance criteria**
- Arbiter can trigger editor/client/server/tests build and capture result

### E2. Validation support
**Deliverables**
- `ValidateDataHandler`
- schema/data validation routing

**Acceptance criteria**
- Arbiter can request validation of data files under `data/` and `schemas/`

### E3. Editor tool execution
**Deliverables**
- `RunEditorToolHandler`
- `NovaForgeEditorToolService`

**Acceptance criteria**
- Arbiter can invoke whitelisted editor tools with structured args

---

## Epic F — AI-assisted content workflows

### F1. Asset generation request pipeline
**Deliverables**
- `RequestAssetGenerationHandler`
- queue/preview response model

**Acceptance criteria**
- Arbiter can request generation tasks without directly mutating runtime state

### F2. Patch preview workflow
**Deliverables**
- diff proposal flow in Arbiter
- NovaForge file targets exposed only via explicit request

**Acceptance criteria**
- proposed edits show diff, impacted files, and optional validation/test action

---

## 15. Suggested milestone sequence

### Milestone 1 — Foundations
- A1
- A2
- B1
- B2

### Milestone 2 — Bridge online
- C1
- C2

### Milestone 3 — Read-only useful workflows
- D1
- D2
- D3

### Milestone 4 — Safe actions
- E1
- E2
- E3

### Milestone 5 — Advanced AI workflows
- F1
- F2

---

## 16. Risks and mitigations

### Risk: WPF shell tries to absorb editor responsibilities
**Mitigation:** keep all viewport/simulation/editor-native interaction inside NovaForge editor.

### Risk: Arbiter becomes required for build/runtime
**Mitigation:** compile-time optional integration target and manifest-driven discovery only.

### Risk: AI writes directly into unstable core systems
**Mitigation:** diff-only workflow, test/build gate, human approval.

### Risk: duplicate project metadata across repos
**Mitigation:** NovaForge manifest is source of truth; Arbiter reads it.

### Risk: transport becomes security hole
**Mitigation:** localhost only, disabled in shipping, token for any non-local extension later.

---

## 17. Immediate next implementation tasks

### NovaForge immediate tasks
1. Create `integrations/arbiter/` folder tree.
2. Add `novaforge.project.json`.
3. Add `ArbiterBridgeTypes.h` and `ArbiterProjectContext.h`.
4. Add `ArbiterCapabilityRegistry` and return static capabilities first.
5. Add minimal bridge server with `/project/info` and `/project/capabilities`.

### Arbiter immediate tasks
1. Create `ProjectAdapters/NovaForge/`.
2. Implement `NovaForgeManifest.cs`.
3. Implement `NovaForgeProjectAdapter.cs`.
4. Implement `NovaForgeBridgeClient.cs`.
5. Add a simple Project Overview panel showing project info, capabilities, and build targets.

---

## 18. Final recommendation

The cleanest path is not “merge Arbiter into NovaForge.”
It is:

- **adapter-ize Arbiter**
- **modularize NovaForge integration**
- **establish a strict bridge contract**
- **keep Atlas/NovaForge editor native and custom**
- **keep Arbiter as the external AI development cockpit**

That gets you the universal tooling layer you want without wrecking the engine/game architecture.
