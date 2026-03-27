# MasterRepo Consolidation + WPF Tooling Plan

## Purpose

Use **MasterRepo** as the canonical destination repository and consolidate the strongest pieces of:

- **Arbiter**
- **ArbiterAI**
- **NovaForge**

into a single architecture that keeps the runtime/engine side native where it belongs while adding a **WPF-based tooling shell** for workspace UX, chat, archive, build flow, and editor orchestration.

---

## Source Repo Roles

### MasterRepo
Best candidate for the destination repo because it already contains broad engine and platform structure:

- `AI/`
- `Agents/`
- `Archive/`
- `Builder/`
- `Core/`
- `Editor/`
- `Engine/`
- `PCG/`
- `Runtime/`
- `Tools/`
- `UI/`
- `WorkspaceState/`

This should remain the primary home for:

- runtime systems
- engine and simulation
- editor backend services
- AI orchestration
- archive/learning systems
- build pipeline
- content pipeline
- project-wide docs and migration tracking

### Arbiter / ArbiterAI
Best source for **tooling-shell patterns** and workflow UX:

- `HostApp/`
- `VisualStudioExtension/`
- `AIEngine/`
- `Memory/`
- `archive/`
- workflow/docs around GUI and repo directives

These repos should be treated as the strongest source for:

- WPF shell structure
- chat-first workspace ideas
- tool host UX
- archive ingestion workflow
- AI-facing desktop experience
- IDE integration concepts

### NovaForge
Best source for **game-side systems and data-driven design**:

- `cpp_client/`
- `cpp_server/`
- `cpp_common/`
- `engine/`
- `editor/`
- `data/`
- `schemas/`
- `tools/`
- `docs/`
- `specs/`

This repo should be mined for:

- gameplay architecture concepts
- engine/editor split ideas
- client/server boundaries
- schema-driven content setup
- editor support patterns
- modular world/system implementation ideas

---

## Final Direction

## Core Rule

**MasterRepo is the source of truth.**

The other repos are not merged blindly. Their systems are:

- evaluated
- mapped by responsibility
- rewritten or adapted
- integrated into MasterRepo behind clear interfaces

---

## Target Architecture

```text
+-----------------------------------------------------------+
|                    WPF Tooling Shell                      |
|-----------------------------------------------------------|
| Workspace | Chat | Archive | Logs | Builds | Docs | Tasks |
| Project Browser | Asset Views | VS Integration | Settings |
+--------------------------|--------------------------------+
                           |
                    Command / Event Bridge
          (WebSocket / Named Pipes / REST / Native DLL API)
                           |
+-----------------------------------------------------------+
|                MasterRepo Native Backend                  |
|-----------------------------------------------------------|
| Engine | Runtime | Editor Services | AI Orchestration     |
| Content Pipeline | Builder | Archive Indexing | PCG       |
| Game Systems | Data Schemas | Tests | Automation          |
+-----------------------------------------------------------+
                           |
+-----------------------------------------------------------+
|        Optional External Services / Local AI Server       |
|-----------------------------------------------------------|
| LLM host | embeddings/indexing | repo analysis | agents   |
+-----------------------------------------------------------+
```

---

## WPF Role vs Native Role

### WPF should own

- workspace shell
- docking layout
- chat interface
- archive browser and upload/download UX
- logs, jobs, build output, notifications
- document/spec viewer
- project/file explorer
- task board / execution dashboard
- settings and workspace profiles
- embedded web surfaces where useful
- Visual Studio integration front-end

### Native MasterRepo should own

- engine runtime
- rendering
- world/editor core logic
- simulation and deterministic systems
- gameplay subsystems
- asset import/processing backends
- save/load logic
- content compilation/baking
- performance-critical tools
- viewport/editor backend
- plugin execution
- AI-assisted backend tasks that need repo/runtime access

### Shared boundary should own

- command schema
- event schema
- state sync contracts
- job/task execution protocol
- build/run/test commands
- editor open/save/select/focus requests
- asset inspection and mutation requests
- AI request/response transport

---

## Integration Principles

1. **Do not directly fuse UI code across repos.**
2. **Do not copy entire folders unless they are self-contained and still fit the target architecture.**
3. **Every imported system gets a destination owner in MasterRepo first.**
4. **WPF remains a host and orchestration layer, not the entire engine/editor implementation.**
5. **All cross-boundary communication must go through a stable bridge.**
6. **Prefer incremental subsystem migration over massive repo-wide rewrites.**
7. **Keep release/client builds separated from tooling/editor builds.**
8. **Keep Atlas rule locked: no ImGui, custom UI direction only.**

---

## Recommended MasterRepo Structure After Consolidation

```text
MasterRepo/
  AI/
  Agents/
  Archive/
  Builder/
  Core/
  Docs/
  Editor/
  Engine/
  PCG/
  Runtime/
  Tools/
    WpfHost/
    Bridge/
    VSIntegration/
    ArchiveTools/
    DesignTools/
  UI/
  Projects/
  Tests/
  WorkspaceState/
```

### Proposed new or expanded folders

#### `Tools/WpfHost/`
The desktop shell application.

Suggested contents:

- main window
- docking layout manager
- chat panel
- archive panel
- logs/output panel
- build tasks panel
- project browser
- document/design viewer
- settings/workspace profile system
- notification center
- WebView2 host surfaces where needed

#### `Tools/Bridge/`
Contract layer between WPF and native MasterRepo services.

Suggested contents:

- command definitions
- event definitions
- request/response types
- serialization helpers
- transport adapters
- session/workspace state sync

#### `Tools/VSIntegration/`
Visual Studio extension and editor-side integration.

Suggested contents:

- file diff preview support
- task/codegen request bridge
- project awareness
- change application workflow
- command palette hooks

#### `Tools/ArchiveTools/`
Shared archive ingestion and indexing UX/backend helpers.

#### `Tools/DesignTools/`
Spec viewing, design documents, implementation plans, roadmap tooling.

---

## Consolidation Ownership Matrix

| Domain | Destination | Primary Source | Notes |
|---|---|---|---|
| Workspace shell | `Tools/WpfHost` | Arbiter / ArbiterAI | Port patterns, not raw app assumptions |
| Chat UX | `Tools/WpfHost/Chat` | Arbiter / ArbiterAI | Central workflow surface |
| Archive UX | `Tools/WpfHost/Archive` + `Archive/` | Arbiter / ArbiterAI + MasterRepo | Split front-end and backend clearly |
| AI orchestration | `AI/` + `Agents/` | MasterRepo + Arbiter AIEngine ideas | Keep backend native/service-oriented |
| Build dashboard | `Tools/WpfHost/Builds` + `Builder/` | MasterRepo + Arbiter patterns | UI reads backend jobs/events |
| VS integration | `Tools/VSIntegration` | Arbiter | Keep optional and isolated |
| Editor backend | `Editor/` | MasterRepo + NovaForge ideas | Native side only |
| Viewport/render tools | `Editor/` + `Engine/` | MasterRepo / NovaForge | Do not push this into WPF core |
| Gameplay systems | `Runtime/`, `Projects/`, `PCG/` | NovaForge + current MasterRepo | Port subsystem by subsystem |
| Data schemas | `Projects/`, `Docs/`, `Config/` | NovaForge | Normalize naming and schema versioning |
| Client/server split | `Runtime/`, `Projects/`, network modules | NovaForge | Integrate only after architecture mapping |
| Workspace persistence | `WorkspaceState/` | MasterRepo + Arbiter patterns | Shared with WPF shell |

---

## What to Refactor In, What to Avoid

### Refactor in from Arbiter / ArbiterAI

Refactor in:

- WPF host patterns
- panel/workspace concepts
- chat-centric workflow design
- archive ingestion UX
- Visual Studio integration concepts
- AI engine workflow ideas
- memory/session interaction patterns

Avoid importing directly:

- repo-specific assumptions tied to Arbiter naming
- duplicate AI engine layers if MasterRepo already has equivalent ownership
- narrow HostApp wiring that bypasses a clean bridge

### Refactor in from NovaForge

Refactor in:

- schema-driven content organization
- useful client/server/common separation ideas
- gameplay system structures
- data-driven editor support concepts
- engine/editor patterns that improve MasterRepo
- specs and docs that clarify runtime requirements

Avoid importing directly:

- conflicting engine abstractions without remapping ownership
- redundant editor front-end assumptions
- whole-folder copy of client/server code before dependency cleanup

---

## Bridge Contract Recommendation

Use a layered bridge model.

### Transport priority

1. **Named pipes** for local desktop command/control
2. **WebSocket** for live event streams and panel updates
3. **REST/HTTP** for simple request/response services
4. **Native DLL boundary** only where performance or direct editor integration really needs it

### Minimum command groups

- `workspace.*`
- `build.*`
- `archive.*`
- `project.*`
- `asset.*`
- `editor.*`
- `runtime.*`
- `ai.*`
- `tasks.*`
- `logs.*`
- `tests.*`

### Example event groups

- `workspace.changed`
- `build.started`
- `build.progress`
- `build.completed`
- `archive.ingest.progress`
- `asset.updated`
- `editor.selection.changed`
- `runtime.state.changed`
- `ai.response.delta`
- `job.failed`
- `notification.raised`

---

## Migration Waves

## Wave 0 — Freeze the architecture

Deliverables:

- destination ownership map
- dependency rules
- naming rules
- bridge contract draft
- tooling vs runtime separation policy
- build target matrix

Exit condition:

- no subsystem is “homeless”
- no duplicated ownership remains undefined

## Wave 1 — Build the WPF shell skeleton

Deliverables:

- `Tools/WpfHost` solution
- shell window
- workspace layout system
- chat panel shell
- logs/output panel shell
- build panel shell
- archive panel shell
- settings panel shell
- project tree shell
- theme system with dark-first support

Exit condition:

- app launches and panel layout persists
- shell can connect to a mock bridge backend

## Wave 2 — Implement the bridge

Deliverables:

- command bus
- event bus
- transport layer
- serialization contracts
- backend service host adapters
- diagnostics and reconnection logic

Exit condition:

- WPF can issue commands and receive live state/events from MasterRepo services

## Wave 3 — Connect core workflows

Deliverables:

- build/run/stop workflow
- log stream integration
- chat-to-task workflow
- archive upload/index/search workflow
- docs/spec viewer workflow
- workspace save/restore workflow

Exit condition:

- WPF becomes operational as the daily driver tooling shell

## Wave 4 — Port Arbiter workflow features

Deliverables:

- refined chat UX
- archive and knowledge UX
- VS integration hooks
- roadmap/tasks dashboard
- file/diff/change-review workflow

Exit condition:

- key Arbiter productivity loops function inside MasterRepo tooling

## Wave 5 — Port NovaForge systems into native MasterRepo

Suggested order:

1. schemas/data organization
2. editor-support abstractions
3. gameplay data definitions
4. modular systems / PCG hooks
5. client/server shared logic
6. network/service layers where still valid

Exit condition:

- imported systems compile cleanly under MasterRepo ownership
- no direct repo-identity leakage remains

## Wave 6 — Hardening and cleanup

Deliverables:

- obsolete code removal
- deprecation pass
- test coverage pass
- build matrix pass
- performance pass
- docs pass

Exit condition:

- MasterRepo is the only active repo required for ongoing development

---

## Immediate Refactor Backlog

### Highest priority

- create the consolidation map docs in `Docs/`
- create `Tools/WpfHost/`
- create `Tools/Bridge/`
- define bridge commands/events JSON schema
- define build targets: runtime, editor, tooling, server, release
- define workspace state model
- define theme and docking system architecture

### Next priority

- port Arbiter chat workflow into WPF shell
- port archive panel behavior into WPF shell
- connect build/log stream into WPF
- define embedded document/browser strategy
- define Visual Studio extension boundaries

### Then

- audit NovaForge modules for direct portability
- map data/schema structures into MasterRepo format
- port gameplay/editor backend ideas into native subsystems
- deprecate duplicate code paths

---

## Build Target Rules

At minimum, formalize these targets:

- **RuntimeClient**
- **DedicatedServer**
- **EditorBackend**
- **ToolingShellWpf**
- **AIToolingServices**
- **Tests**
- **ReleaseClient**
- **ReleaseServer**

### Separation rule

Tooling must be removable from release client builds.

That means:

- no mandatory WPF dependency in shipped runtime client
- no editor-only code in release runtime path
- AI/tooling layers behind compile-time and packaging boundaries
- server builds may optionally retain selected AI/admin integrations if explicitly desired

---

## UI/UX Direction

### WPF shell style

- dark-first theme
- crisp professional layout
- dockable panel workspace
- fast keyboard-centric workflow
- persistent workspace presets
- integrated chat panel as first-class feature
- integrated archive drag/drop and progress bars
- notification/event center
- bottom-right archive access option if desired

### Keep native where it matters

- viewport
- rendering overlays
- scene/world editing internals
- simulation inspection overlays tightly coupled to engine state

---

## Risk Register

### Risk 1 — Hybrid editor confusion
If both WPF and native editor compete for ownership, the system becomes inconsistent.

Mitigation:

- WPF owns shell/workflow
- native backend owns editor core and viewport logic

### Risk 2 — Dependency sprawl
If WPF reaches deep into engine internals directly, maintenance cost explodes.

Mitigation:

- all calls go through bridge/services
- no random direct DLL calls without review

### Risk 3 — Copy-paste architecture drift
Large folder imports can preserve old assumptions and break the destination repo.

Mitigation:

- import by feature
- rewrite identifiers and ownership at import time
- require destination module for every migration item

### Risk 4 — Release contamination
Tooling dependencies leaking into game runtime builds.

Mitigation:

- strict build target separation
- packaging audits
- editor/tooling compile guards

### Risk 5 — Too much refactor at once
Trying to migrate everything in one pass can stall the repo.

Mitigation:

- work system by system
- keep a shippable working baseline after each wave

---

## Definition of Done

The consolidation is considered successful when:

- MasterRepo is the only active destination repo needed for development
- WPF tooling shell launches and is usable as the main workspace
- chat, archive, logs, docs, builds, and tasks work from one shell
- native MasterRepo services back the tooling reliably
- NovaForge-derived systems live under MasterRepo ownership cleanly
- Arbiter-derived tooling workflows live in WPF cleanly
- release builds exclude editor/tooling dependencies correctly
- migration status is documented and testable

---

## Recommended First Implementation Sequence

1. Add `Docs/MASTERREPO_CONSOLIDATION_PLAN.md`
2. Add `Docs/MASTERREPO_MODULE_OWNERSHIP_MATRIX.md`
3. Create `Tools/WpfHost/` skeleton
4. Create `Tools/Bridge/` contracts
5. Stand up a mock backend and connect WPF shell
6. Wire build/log/chat/archive workflows first
7. Port Arbiter UX patterns next
8. Port NovaForge native systems after bridge and shell are stable

---

## Bottom Line

Yes, this can be done, and **WPF is a good fit** as long as it is used for the **tooling shell and workflow experience**, not as a forced replacement for every native editor/runtime responsibility.

The safest and strongest direction is:

- **MasterRepo = canonical platform**
- **WPF = tooling host**
- **Arbiter/ArbiterAI = workflow UX donor repos**
- **NovaForge = gameplay/data/editor-backend donor repo**
- **Bridge layer = mandatory contract between tooling and native backend**

That gives you a scalable path to one consolidated repo without turning the project into a brittle hybrid mess.
