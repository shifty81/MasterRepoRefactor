# MASTER IMPLEMENTATION CHECKLIST

## Purpose
This checklist defines the execution order for restructuring **MasterRepo** into a clean monorepo with strict internal boundaries between:

- **Atlas** — engine, editor framework, runtime foundations, custom UI framework
- **NovaForge** — game project, gameplay systems, data, content, project-specific tools
- **Arbiter** — AI tooling shell, automation, archive, workflow host, Visual Studio integration
- **Shared** — bridge contracts, manifests, protocol types only
- **Docs** — architecture, integration, implementation references

---

# EPIC 1 — Lock the monorepo architecture

## Goal
Define the structure and rules before moving code.

### Task 1.1 — Create top-level ownership zones
Create or align these roots:

- `Atlas/`
- `NovaForge/`
- `Arbiter/`
- `Shared/`
- `Docs/`

### Task 1.2 — Write boundary document
Create:

- `Docs/Architecture/repo_boundaries.md`

Document:

- what Atlas owns
- what NovaForge owns
- what Arbiter owns
- what Shared owns
- what is forbidden across boundaries

### Task 1.3 — Write Arbiter bridge document
Create:

- `Docs/Integration/arbiter_bridge.md`

Document:

- transport model
- request / response model
- whitelisted tool actions
- read-only vs write actions
- editor-only vs runtime-safe behavior
- trust / local approval rules

### Task 1.4 — Freeze dependency rules
Establish these as hard rules:

- Atlas cannot depend on Arbiter
- NovaForge cannot depend on Arbiter host, chat, archive, UI, or automation internals
- Arbiter may depend on Shared contracts and project adapters
- Shared must stay minimal and stable
- Atlas and NovaForge may consume Shared, but may not place project logic into Shared

### Task 1.5 — Define shipping separation rules
Document that:

- shipping client / server builds cannot pull Arbiter UI or tooling code
- editor-only integrations must be guarded
- development-only tooling paths must not leak into runtime binaries

---

# EPIC 2 — Restructure the repo physically

## Goal
Move code into the correct ownership zones.

### Task 2.1 — Move engine and editor foundations into Atlas
Place reusable engine-side systems under Atlas, including:

- core
- engine
- editor framework
- runtime foundation
- UI framework
- renderer abstractions
- reusable asset pipeline foundations

### Task 2.2 — Move game-specific code into NovaForge
Place project-specific systems under NovaForge, including:

- client
- server
- data
- content
- gameplay systems
- project configs
- project tools
- project-specific asset definitions

### Task 2.3 — Move AI tooling shell into Arbiter
Place tooling-specific systems under Arbiter, including:

- HostApp
- AIEngine
- Archive
- Automation
- VisualStudioExtension
- ProjectAdapters
- workspace shell modules

### Task 2.4 — Create Shared for neutral contracts only
Create:

- `Shared/ArbiterBridgeContract/`
- `Shared/ProjectManifests/`
- `Shared/ToolProtocol/`

### Task 2.5 — Add monorepo layout documentation
Create:

- `Docs/Architecture/monorepo_layout.md`

Map where every major subsystem now belongs.

---

# EPIC 3 — Stand up the bridge backbone

## Goal
Create the safe handshake between Arbiter and NovaForge.

### Task 3.1 — Create the project manifest
Create:

- `Shared/ProjectManifests/novaforge.project.json`

Include:

- repo paths
- build targets
- capabilities
- bridge transport
- timeout
- safety settings
- whitelisted tool actions
- project root references for monorepo layout

### Task 3.2 — Create shared bridge types
Create:

- `Shared/ArbiterBridgeContract/include/ArbiterBridgeTypes.h`

This should define:

- project info
- build request / result
- open file request
- editor selection snapshot
- tool action request / result
- common result / error codes

### Task 3.3 — Create NovaForge bridge implementation
Create:

- `NovaForge/Integrations/Arbiter/include/ArbiterBridgeService.h`
- `NovaForge/Integrations/Arbiter/src/ArbiterBridgeService.cpp`

Start with:

- start / stop service
- get project info
- run build stub
- open file stub
- editor selection stub
- tool action stub

### Task 3.4 — Create Arbiter NovaForge adapter
Create:

- `Arbiter/ProjectAdapters/NovaForge/NovaForgeProjectManifest.cs`
- `Arbiter/ProjectAdapters/NovaForge/NovaForgeProjectAdapter.cs`

Responsibilities:

- load manifest
- connect to bridge
- query project info
- request builds
- query editor selection
- run whitelisted tool actions

### Task 3.5 — Add bridge protocol notes
Create:

- `Shared/ToolProtocol/README.md`

Define:

- request transport assumptions
- local loopback / named pipe options
- payload format
- dry-run behavior
- error surface

---

# EPIC 4 — Wire the first usable endpoints

## Goal
Get a minimal end-to-end integration working.

### Task 4.1 — Implement `/project/info`
Arbiter should be able to read:

- project id
- display name
- version
- supported build targets
- capabilities

### Task 4.2 — Implement `/editor/selection`
Arbiter should be able to query:

- active scene
- selected object
- selected type
- selected id

### Task 4.3 — Implement `/build/run`
Start with these target classes:

- editor target
- client target
- server target
- tests target

All execution should be:

- logged
- bounded
- routed through safe task execution

### Task 4.4 — Implement `/editor/tools/run`
Only allow a whitelist initially, such as:

- `validate_data`
- `run_pcg_preview`
- `open_scene`
- `focus_entity`
- `regenerate_schemas`

All tool actions should default to dry-run unless explicitly approved.

### Task 4.5 — Add log routing
Create a path for bridge-visible logs so Arbiter can surface:

- build results
- tool execution results
- validation summaries
- bridge errors

---

# EPIC 5 — Refactor NovaForge into callable modules

## Goal
Make NovaForge clean enough for bridge integration and long-term growth.

### Task 5.1 — Split monolithic startup and bootstrap
Break large startup flow into modules such as:

- `NovaForgeApp`
- `NovaForgeBootstrap`
- `NovaForgeWorldBootstrap`
- `NovaForgeBuilderBootstrap`
- `NovaForgeHUDController`
- `NovaForgeInputRouter`
- `NovaForgeSession`

### Task 5.2 — Isolate project context
Create a project context layer, for example:

- `NovaForgeProjectContext`

This should own:

- paths
- manifests and config
- data roots
- scene roots
- content roots
- environment flags

### Task 5.3 — Move Arbiter-specific code into integrations
Any Arbiter-facing support should live under:

- `NovaForge/Integrations/Arbiter/`

Not inside core gameplay or runtime modules.

### Task 5.4 — Replace hardcoded path assumptions
Move startup and content discovery to:

- manifest-driven paths
- config-driven roots
- environment-driven resolution

### Task 5.5 — Refactor builder hooks into services
Expose builder integration through clean service calls instead of deep startup coupling.

### Task 5.6 — Separate editor-facing tool hooks from game runtime
Anything callable by Arbiter should be:

- editor-safe
- permissioned
- isolated from shipping runtime logic

---

# EPIC 6 — Refactor Arbiter into a real host shell

## Goal
Make Arbiter reusable and adapter-driven instead of NovaForge-hardcoded.

### Task 6.1 — Split generic modules from project-specific ones
Keep generic:

- chat
- workspace
- logs
- build
- archive
- automation
- theme
- file navigation
- document viewing

### Task 6.2 — Move NovaForge logic into a project adapter
NovaForge-specific behavior should live under:

- `Arbiter/ProjectAdapters/NovaForge/`

This adapter should define:

- supported tools
- relevant paths
- build target mapping
- docs / data search roots
- bridge endpoint mapping

### Task 6.3 — Keep AI engine generic
Ensure these stay project-agnostic:

- tool registry
- memory
- model backend selection
- workflow execution
- archive ingestion
- orchestration logic

### Task 6.4 — Keep Visual Studio integration generic where possible
The extension should speak to project adapters, not hardcode NovaForge everywhere.

### Task 6.5 — Standardize workspace loading
Arbiter should load project manifests and activate a project adapter at startup.

---

# EPIC 7 — Build system cleanup

## Goal
Make the monorepo compile cleanly and keep tooling optional.

### Task 7.1 — Update CMake structure
Reflect the monorepo layout for:

- Atlas targets
- NovaForge targets
- Shared contracts
- integration layers

### Task 7.2 — Keep Arbiter optional
Atlas and NovaForge should remain buildable even if Arbiter is not built.

### Task 7.3 — Separate editor and tooling from shipping builds
Ensure:

- shipping game binaries do not pull Arbiter UI or tooling assemblies
- editor-only integrations are guarded
- tooling dependencies do not leak into runtime targets

### Task 7.4 — Standardize target naming
Use consistent target naming, for example:

- `AtlasEditor`
- `NovaForgeClient`
- `NovaForgeServer`
- `NovaForgeTests`
- `ArbiterHost`

### Task 7.5 — Add compile-time feature guards
Introduce flags or target guards for:

- editor-only bridge support
- dev-only automation
- shipping-safe exclusion of tooling systems

---

# EPIC 8 — Safety, logging, and operational controls

## Goal
Keep AI and tooling actions safe and auditable.

### Task 8.1 — Add action allowlist
Every bridge-callable tool action must be whitelisted.

### Task 8.2 — Add dry-run default
Any action that can modify code, assets, or project state should default to dry-run.

### Task 8.3 — Add audit logging
Log:

- who or what triggered the action
- timestamp
- request payload
- result
- failure reason

### Task 8.4 — Add local trust or auth guard
Before enabling write actions, require:

- local-only transport, or
- trusted session token, or
- editor-side approval gate

### Task 8.5 — Add failure and rollback expectations
Document behavior for:

- rejected tool actions
- partial failure
- build failure
- stale editor state
- unsafe action denial

---

# EPIC 9 — First real workflow milestone

## Goal
Prove the architecture works in practice.

### Task 9.1 — Arbiter reads project info
Working end-to-end.

### Task 9.2 — Arbiter queries active editor selection
Working end-to-end.

### Task 9.3 — Arbiter launches a safe build target
Working end-to-end.

### Task 9.4 — Arbiter runs one safe editor tool
Working end-to-end.

### Task 9.5 — Verify shipping isolation
Confirm that:

- shipping builds compile without Arbiter
- no tooling-only dependencies leak into runtime outputs

Once these are working, the backbone is real.

---

# EPIC 10 — Second-wave improvements

## Goal
Expand only after the backbone is stable.

### Task 10.1 — Add code, doc, and data search roots
Let Arbiter understand:

- docs
- configs
- data tables
- content definitions
- source folders

### Task 10.2 — Add builder and PCG tool hooks
Expose safe actions for:

- preview generation
- validation
- diagnostics
- scene open and focus
- builder inspection

### Task 10.3 — Add richer editor snapshots
Expose more context, such as:

- active map
- active mode
- loaded world state
- selected components
- simulation state

### Task 10.4 — Add proposed codegen workflow
Do not use direct write-first.
Use:

- proposal
- diff preview
- approval
- apply

### Task 10.5 — Add better workspace dashboards
Surface:

- build health
- recent actions
- docs / data roots
- last tool execution
- current project status

---

# Recommended implementation order

## Sprint 1
- Epic 1
- Epic 2
- Task 3.1
- Task 3.2

## Sprint 2
- Task 3.3
- Task 3.4
- Task 4.1
- Task 4.2

## Sprint 3
- Task 4.3
- Task 4.4
- Task 4.5
- Epic 7
- Epic 8

## Sprint 4
- Epic 5
- Epic 6

## Sprint 5
- Epic 9
- Epic 10

---

# Definition of done

The backbone is considered done when:

- MasterRepo is cleanly partitioned
- Shared contracts are the only handshake layer
- NovaForge exposes bridge-backed editor and build services
- Arbiter talks through a NovaForge adapter
- shipping builds remain free of Arbiter dependencies
- at least one safe tool action works end-to-end
- repo boundaries are documented and enforced

---

# Practical summary

What this plan asks you to do is:

- organize the repo
- enforce boundaries
- build the bridge
- modularize NovaForge
- adapter-ize Arbiter
- clean the build system
- prove it with a few safe workflows first

That is the real path from the current state to a clean MasterRepo architecture.
