# MASTERREPO CONSOLIDATION + WPF TOOLING PLAN (ATLASAI VERSION)

## 1. Canonical Direction

MasterRepo is the **destination repo**.

All useful systems from the other repos should be absorbed into MasterRepo in a controlled way:

- **MasterRepo** = canonical engine/game/platform repository
- **AtlasAI** = AI + tooling + orchestration layer (renamed from Arbiter)
- **AtlasAI Core** = agent/runtime/service layer (renamed from ArbiterAI)
- **NovaForge** = game content, gameplay systems, progression, economy, factions, and editor-backend concepts

The target outcome is:

- **C++ core for engine/runtime/editor-backend systems**
- **WPF desktop shell for tooling/workspace UX**
- **Stable bridge/API between WPF and native systems**
- **One naming model across the whole ecosystem**

---

## 2. Naming Lock

### Approved naming model

- `Atlas.*` = engine/runtime/editor/backend systems
- `AtlasAI.*` = tooling, AI, orchestration, workspace, automation
- `NovaForge.*` = game-specific systems/content/data

### Rename map

- `Arbiter` -> `AtlasAI`
- `ArbiterAI` -> `AtlasAI.Core`
- `ArbiterBridge` -> `AtlasAI.Bridge` or `AtlasBridge`
- `Arbiter.UI` -> `AtlasAI.UI`
- `Arbiter.Services` -> `AtlasAI.Services`
- `Arbiter.Agents` -> `AtlasAI.Agents`

### Rule

Do not allow mixed naming long-term. New work should use only:

- `Atlas`
- `AtlasAI`
- `NovaForge`

---

## 3. Architecture Target

## 3.1 MasterRepo role

MasterRepo should own:

- engine core
- runtime
- rendering
- ECS/simulation
- world systems
- gameplay systems
- asset/content pipeline
- native editor-backend services
- dedicated server/client separation
- data schemas and serialization

## 3.2 AtlasAI role

AtlasAI should own:

- WPF tooling shell
- chat-first workspace UI
- archive/library UX
- docs/design viewing
- task/build/log panels
- AI orchestration
- repo indexing and assistance
- Visual Studio workflow integration
- user workspace/session management
- automation surfaces for project operations

## 3.3 NovaForge role

NovaForge should contribute:

- game design systems
- faction/standing/economy concepts
- PVE loops and mission structure
- modular ship/interior concepts
- on-foot/boarding/station interactions
- sector/galaxy progression logic
- PCG/worldbuilding rules
- content authoring requirements for tools/editor

---

## 4. Preferred Physical Structure

```text
/MasterRepo
  /Engine
    /AtlasCore
    /AtlasRuntime
    /AtlasEditorBackend
    /AtlasRender
    /AtlasToolsNative

  /AI
    /AtlasAI.Core
    /AtlasAI.Agents
    /AtlasAI.Pipelines
    /AtlasAI.Memory
    /AtlasAI.Indexing

  /Tools
    /AtlasAI.WpfHost
    /AtlasAI.Shell
    /AtlasAI.UI
    /AtlasAI.Bridge
    /AtlasAI.Workspace
    /AtlasAI.Archive
    /AtlasAI.Chat

  /Game
    /NovaForge
    /NovaForge.Content
    /NovaForge.Data
    /NovaForge.Systems

  /Services
    /BuildService
    /AssetService
    /WorldService
    /TestService
    /AIService

  /Docs
    /Architecture
    /Migration
    /Design
```

---

## 5. WPF Strategy

WPF is a good fit **for the tooling shell**, not for replacing the native runtime/editor core.

### WPF should handle

- shell window
- docking/panel layout
- chat interface
- asset browser
- archive browser
- docs/tasks/build panels
- settings/workspace management
- project navigation
- embedded web content when useful

### Native C++ side should handle

- rendering viewport
- scene/world state
- high-frequency editor operations
- simulation inspection
- asset transforms
- content compilation/cooking
- deterministic gameplay/runtime logic

### Integration pattern

Use WPF as the outer shell and connect it to native services via:

- local REST endpoints
- WebSocket event streams
- named pipes for command/control
- optional direct DLL interop only where justified

---

## 6. Migration Principles

1. **Do not merge raw repos file-for-file**.
2. **Port by subsystem ownership**.
3. **Bridge first, then migrate features**.
4. **Rename early at the boundary level** so new code stops reintroducing old identities.
5. **Prefer adapters over rewrites** for proven systems.
6. **Keep the engine/runtime isolated from the tooling shell**.

---

## 7. Consolidation by Donor Repo

## 7.1 From Arbiter -> AtlasAI

Absorb and refactor:

- WPF shell patterns
- project/workspace UX
- tray/menu workflow
- archive panel model
- AI chat integration surfaces
- WebView2 tooling where helpful
- visual layout concepts for multi-panel tooling
- background service/controller patterns

## 7.2 From ArbiterAI -> AtlasAI.Core

Absorb and refactor:

- AI service layer concepts
- orchestration patterns
- memory/index/archive interfaces
- agent task routing
- local AI server workflows
- prompt/task abstraction concepts

## 7.3 From NovaForge -> MasterRepo + Game layer

Absorb and refactor:

- gameplay/data systems
- economy/faction/mission rules
- modular ship and station content concepts
- interior/on-foot systems requirements
- PCG and builder requirements
- editor feature requirements driven by gameplay needs

---

## 8. Suggested Execution Phases

## Phase 0 - Naming lock

- freeze naming model
- rename Arbiter -> AtlasAI in docs and plans first
- create namespace/project mapping list
- stop adding new `Arbiter*` identifiers

## Phase 1 - Shell foundation

Build AtlasAI WPF shell with:

- main workspace window
- docking system
- chat panel
- project explorer
- output/log panel
- task/build panel
- archive panel
- settings panel

## Phase 2 - Bridge/API foundation

Implement bridge contracts for:

- build/run/stop
- logs/events streaming
- asset queries
- world/scene commands
- editor backend requests
- AI requests/responses
- test execution

## Phase 3 - Service extraction in MasterRepo

Expose backend services behind clean interfaces:

- asset service
- build service
- world service
- simulation inspection service
- content pipeline service
- test service

## Phase 4 - AtlasAI workflow migration

Port tooling features from old Arbiter/ArbiterAI into AtlasAI by workflow:

- chat workflow
- archive workflow
- repo assistance workflow
- build workflow
- design/doc workflow
- VS/tool integration workflow

## Phase 5 - NovaForge subsystem migration

Port game systems in this order:

1. data definitions
2. content schema
3. faction/economy/progression systems
4. modular ship/interior systems
5. mission/PVE loop systems
6. station/on-foot interactions
7. PCG and world-generation integration

## Phase 6 - Cleanup and hard rename

- remove all remaining `Arbiter` references
- consolidate configs/scripts/docs
- delete duplicate legacy layers
- enforce dependency boundaries

---

## 9. Dependency Rules

### Allowed

- `AtlasAI.*` -> bridge/service contracts -> `Atlas.* backend services`
- `NovaForge.*` -> `Atlas.*`
- `AtlasEditorBackend` -> `AtlasRuntime/AtlasCore`

### Not allowed

- WPF UI reaching directly into random low-level engine internals
- game content systems depending on WPF assemblies
- duplicated logic in both native and tooling layers
- multiple competing editors for the same authority domain

---

## 10. Immediate Next Deliverables

1. Module ownership matrix
2. Rename execution plan
3. Dependency rules document
4. Bridge contract draft
5. Folder/solution restructuring plan
6. Legacy deprecation list

---

## 11. Final Direction Statement

MasterRepo will become the single consolidated repository.

AtlasAI will be the official AI + tooling identity for the platform, replacing Arbiter and ArbiterAI.

WPF will be used as the professional desktop tooling shell around MasterRepo-native services, while engine/runtime/editor-backend logic remains primarily native.

NovaForge systems will be ported into MasterRepo as gameplay and data subsystems, not bolted on as a separate competing architecture.
