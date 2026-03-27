# MASTERREPO_POST_CONSOLIDATION_FOLDER_LAYOUT.md

## Purpose

This document defines the recommended **post-consolidation folder and module layout** for **MasterRepo** after absorbing systems, patterns, and features from:

- **MasterRepo** as the canonical destination
- **Arbiter** renamed to **AtlasAI**
- **ArbiterAI** renamed to **AtlasAI.Core**
- **NovaForge** as the gameplay/content/system donor repo

The goal is to produce a clean, scalable repository structure that supports:

- native C++ engine/runtime/editor systems
- WPF-based tooling and workspace UX
- AtlasAI orchestration and agent workflows
- gameplay/content/data systems
- asset and build pipelines
- clean subsystem ownership boundaries

---

# 1. Top-Level Repository Layout

```text
/MasterRepo
│
├── /Engine
├── /Game
├── /AI
├── /Tools
├── /Services
├── /Shared
├── /Content
├── /Data
├── /Config
├── /Scripts
├── /Docs
├── /Tests
├── /ThirdParty
├── /Build
├── /Deploy
└── /Archive
```

---

# 2. Top-Level Folder Responsibilities

## `/Engine`
Native engine, runtime, renderer, ECS, simulation, editor backend, asset runtime interfaces, and low-level systems.

## `/Game`
All game-specific logic and gameplay for **NovaForge** and future game modules built on Atlas.

## `/AI`
All AtlasAI orchestration, agent systems, memory, planning, indexing, inference integration, and training/data preparation components.

## `/Tools`
Desktop tooling shell, WPF workspace, editor-facing UX, panels, dashboards, archive views, build interfaces, and chat-first workflow surfaces.

## `/Services`
Executable or hostable service processes used by tools and runtime systems, such as AI service, world service, build service, asset service, and indexing service.

## `/Shared`
Schemas, contracts, DTOs, protocol definitions, common utility code, cross-language interoperability assets, and generated bridge contracts.

## `/Content`
Game-ready authored content and templates: prefabs, archetypes, blueprints, stations, ship parts, missions, dialogue, economy templates, and PCG seeds.

## `/Data`
Structured data for tuning, balance, definitions, rulesets, progression, localization, economy, factions, and simulation tables.

## `/Config`
Default configuration files, environment templates, workspace configuration, tool profiles, runtime config, and per-service settings.

## `/Scripts`
Build scripts, repo tooling, bootstrap scripts, migration scripts, codegen, validation, packaging, and automation helpers.

## `/Docs`
All architecture docs, design docs, migration plans, implementation plans, coding standards, subsystem contracts, and roadmap files.

## `/Tests`
Unit, integration, deterministic simulation, tool bridge, asset pipeline, and end-to-end test projects.

## `/ThirdParty`
Vendored external dependencies, source drops, pinned libraries, wrappers, licenses, and integration notes.

## `/Build`
Intermediate build orchestration files, generator outputs, CI inputs, packaging metadata, and solution generation artifacts.

## `/Deploy`
Deployment assets for local services, internal tools, dedicated server outputs, packaging profiles, and installer-related content.

## `/Archive`
Knowledge archive, learning inputs, indexed references, project snapshots, design captures, imported notes, and long-term project memory artifacts.

---

# 3. Recommended Detailed Structure

## `/Engine`

```text
/Engine
├── /AtlasCore
├── /AtlasRuntime
├── /AtlasRenderer
├── /AtlasPhysics
├── /AtlasAudio
├── /AtlasInput
├── /AtlasNetworking
├── /AtlasSimulation
├── /AtlasVoxel
├── /AtlasWorld
├── /AtlasAssets
├── /AtlasScripting
├── /AtlasEditorBackend
├── /AtlasToolsRuntime
└── /AtlasPlatform
```

### Responsibilities

- **AtlasCore**  
  Core primitives, memory, containers, logging, IDs, threading, job system, math, reflection helpers, and base module contracts.

- **AtlasRuntime**  
  Runtime bootstrap, application lifecycle, subsystem registration, frame orchestration, and host environment setup.

- **AtlasRenderer**  
  Rendering backend, scene rendering, materials, shaders, viewport integration, debug rendering, and tooling overlays.

- **AtlasPhysics**  
  Rigid body, collision, spatial queries, damage interactions, docking/attachment physics, and gameplay-facing integration points.

- **AtlasAudio**  
  Audio engine integration, sound emitters, environmental audio, and tooling previews.

- **AtlasInput**  
  Input abstraction for player, editor, tools, remapping, and simulation command routing.

- **AtlasNetworking**  
  Replication, authority layers, deterministic sync support, dedicated server integration, prediction/interpolation groundwork.

- **AtlasSimulation**  
  Deterministic simulation core, tick model, world progression, system scheduling, fixed-step orchestration.

- **AtlasVoxel**  
  Voxel terrain, planet surfaces, destruction, streaming, clipmaps, and voxel editing support.

- **AtlasWorld**  
  Sector streaming, galaxy/world topology, spatial partitioning, star systems, planets, stations, and traversal data.

- **AtlasAssets**  
  Asset loading, metadata, import pipeline runtime hooks, asset registry, dependency tracking, and runtime asset handles.

- **AtlasScripting**  
  Data-driven behavior support, script runtime abstractions, event-driven gameplay bindings, and future scripting extensibility.

- **AtlasEditorBackend**  
  Native editor operations: scene manipulation, asset manipulation, transform tools, selection, inspection, viewport editing, and save/load editor state.

- **AtlasToolsRuntime**  
  Runtime hooks specifically exposed to tooling: diagnostics, live state query, profiling streams, and editor-runtime bridge endpoints.

- **AtlasPlatform**  
  OS abstraction, file system services, process control, windowing integration, IPC plumbing, and platform-specific support.

---

## `/Game`

```text
/Game
├── /NovaForge
│   ├── /Core
│   ├── /Gameplay
│   ├── /Economy
│   ├── /Factions
│   ├── /Missions
│   ├── /Ships
│   ├── /Stations
│   ├── /Interiors
│   ├── /Characters
│   ├── /Combat
│   ├── /Mining
│   ├── /Exploration
│   ├── /Construction
│   ├── /PCG
│   ├── /UIRuntime
│   └── /Server
└── /CommonGameFramework
```

### Responsibilities

- **NovaForge/Core**  
  Game bootstrap, game rules, mode registration, progression entry points, and project-specific composition.

- **NovaForge/Gameplay**  
  Shared gameplay systems, state machines, player loops, interaction rules, and common game orchestration.

- **NovaForge/Economy**  
  Trade, market behavior, resources, pricing logic, logistics rules, scarcity, station economy, and simulation-linked market updates.

- **NovaForge/Factions**  
  Reputation, standings, security layers, diplomatic state, NPC hostility, lawful zone logic, and war declaration systems.

- **NovaForge/Missions**  
  Contract generation, mission templates, reward tables, mission chains, procedural tasks, and event-driven mission triggers.

- **NovaForge/Ships**  
  Ship modules, mass, thrust, fuel, hardpoints, docking, ship archetypes, player ships, and NPC ship composition.

- **NovaForge/Stations**  
  Station generation, services, ownership, trade hubs, orbital logic, defense systems, and station lifecycle.

- **NovaForge/Interiors**  
  Ship/station interior generation, room systems, walkable spaces, boarding flow, shop interiors, and NPC interior placement.

- **NovaForge/Characters**  
  Player/NPC characters, on-foot systems, EVA, mech integration, equipment, interaction, and animation-facing gameplay state.

- **NovaForge/Combat**  
  Space combat, on-foot combat, PVE, consensual PVP, duels, boarding, crime response, and security force response logic.

- **NovaForge/Mining**  
  Resource scanning, extraction systems, salvage, asteroid/resource nodes, and mining progression.

- **NovaForge/Exploration**  
  scanning, probes, ruins, caches, discovery systems, mapping, sensor gameplay, and planetary survey flow.

- **NovaForge/Construction**  
  Modular building, voxel/block assembly, upgrade systems, station/ship construction, sockets, weld logic, and salvage rebuild paths.

- **NovaForge/PCG**  
  Procedural world generation, interiors, factions, economy seeding, encounter generation, sectors, planetary data, and prefab composition.

- **NovaForge/UIRuntime**  
  In-game runtime UI only. This must remain distinct from WPF tooling UI.

- **NovaForge/Server**  
  Dedicated server and simulation host integration for game-specific rules.

- **CommonGameFramework**  
  Shared game-facing patterns if future Atlas-based games are added.

---

## `/AI`

```text
/AI
├── /AtlasAI.Core
├── /AtlasAI.Agents
├── /AtlasAI.Planning
├── /AtlasAI.Memory
├── /AtlasAI.Indexing
├── /AtlasAI.Training
├── /AtlasAI.Inference
├── /AtlasAI.Archive
├── /AtlasAI.Codegen
├── /AtlasAI.Design
└── /AtlasAI.Automation
```

### Responsibilities

- **AtlasAI.Core**  
  Core AI orchestration contracts, session model, command routing, task lifecycle, and agent framework base classes.

- **AtlasAI.Agents**  
  Specialized agents for code, design, worldbuilding, balance, documentation, testing, and implementation planning.

- **AtlasAI.Planning**  
  Multi-step plan generation, dependency analysis, task decomposition, and execution graph support.

- **AtlasAI.Memory**  
  Working memory, project memory, indexed context links, retrieval policies, and long-term reference management.

- **AtlasAI.Indexing**  
  Repo indexing, archive indexing, semantic search preparation, embeddings pipelines, and structured retrieval metadata.

- **AtlasAI.Training**  
  Dataset preparation, labeling flows, replay capture, learning inputs, tuning pipelines, and evaluation harnesses.

- **AtlasAI.Inference**  
  Local model adapters, provider abstraction, inference orchestration, request/response normalization, and safety/runtime policy hooks.

- **AtlasAI.Archive**  
  Archive ingestion, document classification, knowledge capture, project note preservation, and asset-linked memory.

- **AtlasAI.Codegen**  
  Code assistance, patch proposal generation, diff planning, refactor suggestions, and code-quality analysis.

- **AtlasAI.Design**  
  Game design support, system planning, balance reasoning, implementation breakdowns, and design-doc generation.

- **AtlasAI.Automation**  
  Background workflows, scripted tasks, environment setup, CI helpers, tool triggers, and user-approved automation flows.

---

## `/Tools`

```text
/Tools
├── /AtlasAI.WpfHost
├── /AtlasAI.Shell
├── /AtlasAI.Panels
├── /AtlasAI.Workspace
├── /AtlasAI.ProjectExplorer
├── /AtlasAI.Chat
├── /AtlasAI.ArchiveUI
├── /AtlasAI.BuildUI
├── /AtlasAI.LogsUI
├── /AtlasAI.AssetUI
├── /AtlasAI.DesignUI
├── /AtlasAI.SettingsUI
├── /AtlasAI.VisualStudio
├── /AtlasAI.BlenderBridge
└── /AtlasAI.Bridge
```

### Responsibilities

- **AtlasAI.WpfHost**  
  The top-level WPF application entry point and desktop shell host.

- **AtlasAI.Shell**  
  Docking, layout management, window chrome, theming, command routing, menus, tray behavior, workspace lifecycle.

- **AtlasAI.Panels**  
  Shared panel framework for all dockable, pinnable, and tool panels.

- **AtlasAI.Workspace**  
  Workspace profiles, session restore, multi-project contexts, tab/panel persistence, and active environment state.

- **AtlasAI.ProjectExplorer**  
  Repo tree, solution context, content browser links, generated items, and quick-action workflows.

- **AtlasAI.Chat**  
  ChatGPT-style assistant surface, threaded sessions, prompt history, tool invocation UX, and task/action bridging.

- **AtlasAI.ArchiveUI**  
  Archive ingestion interface, document browsing, indexing status, tagging, and research support panels.

- **AtlasAI.BuildUI**  
  Build controls, run profiles, compile logs, test execution, packaging actions, and environment launch controls.

- **AtlasAI.LogsUI**  
  Runtime logs, tool logs, simulation traces, warnings/errors, diagnostics, and filter/search views.

- **AtlasAI.AssetUI**  
  Asset browser, metadata inspector, import queues, dependencies, and preview workflow.

- **AtlasAI.DesignUI**  
  Design docs, roadmaps, design graphs, spec panels, task planning, and implementation note surfaces.

- **AtlasAI.SettingsUI**  
  Global settings, theme profiles, AI provider settings, workspace defaults, service config editors.

- **AtlasAI.VisualStudio**  
  IDE integration, file opening, change review workflows, jump-to-code actions, and code assistant handoff surfaces.

- **AtlasAI.BlenderBridge**  
  Integration points for Blender-based content workflows where needed.

- **AtlasAI.Bridge**  
  WPF-side implementation of the bridge contract used to communicate with native Atlas services.

---

## `/Services`

```text
/Services
├── /AtlasAI.ServiceHost
├── /AtlasBuildService
├── /AtlasAssetService
├── /AtlasWorldService
├── /AtlasSimulationService
├── /AtlasIndexService
├── /AtlasEditorService
├── /AtlasTelemetryService
└── /AtlasSessionService
```

### Responsibilities

- **AtlasAI.ServiceHost**  
  Process host for AtlasAI orchestration and model-facing tasks.

- **AtlasBuildService**  
  Build/run/test orchestration and compile task execution.

- **AtlasAssetService**  
  Asset import/export, conversion, metadata generation, and asset pipeline tasks.

- **AtlasWorldService**  
  World queries, save/load operations, content generation hooks, and map/sector inspection endpoints.

- **AtlasSimulationService**  
  Simulation control, pause/resume/tick/debug stepping, scenario execution, and deterministic replay support.

- **AtlasIndexService**  
  Repo and archive indexing service for AtlasAI retrieval.

- **AtlasEditorService**  
  Native editor command endpoints exposed to tooling.

- **AtlasTelemetryService**  
  Logging, diagnostics streaming, profiling sessions, and metrics/event broadcast.

- **AtlasSessionService**  
  Workspace session state, active project state, locks, and tool-runtime session coordination.

---

## `/Shared`

```text
/Shared
├── /Contracts
├── /Schemas
├── /Protocols
├── /Generated
├── /Interop
└── /Utilities
```

### Responsibilities

- **Contracts**  
  Bridge contracts, service APIs, command definitions, event types, and response models.

- **Schemas**  
  JSON/YAML/XML schemas and validation definitions.

- **Protocols**  
  Versioning, handshake rules, transport protocols, IPC message conventions.

- **Generated**  
  Auto-generated DTOs, bindings, codegen outputs, and synchronized protocol types.

- **Interop**  
  Native/managed interop definitions, marshalling helpers, binary compatibility wrappers.

- **Utilities**  
  Shared helpers that are safe to reuse cross-module.

---

## `/Content`

```text
/Content
├── /Prefabs
├── /Ships
├── /Stations
├── /Interiors
├── /Props
├── /Characters
├── /Missions
├── /Dialogue
├── /Economy
├── /PCGSeeds
├── /Biomes
├── /Planets
└── /Templates
```

---

## `/Data`

```text
/Data
├── /Balance
├── /Factions
├── /Security
├── /Resources
├── /Progression
├── /Loot
├── /Crafting
├── /Localization
├── /Encounters
├── /Rules
└── /Tables
```

---

## `/Config`

```text
/Config
├── /Default
├── /Workspace
├── /Services
├── /Editor
├── /Runtime
├── /Server
└── /AI
```

---

## `/Scripts`

```text
/Scripts
├── /Bootstrap
├── /Build
├── /RepoMaintenance
├── /Migration
├── /Validation
├── /Codegen
└── /Packaging
```

---

## `/Docs`

```text
/Docs
├── /Architecture
├── /Design
├── /Roadmaps
├── /Migration
├── /Bridge
├── /Implementation
├── /Standards
├── /Subsystems
└── /ArchiveGuides
```

---

## `/Tests`

```text
/Tests
├── /Unit
├── /Integration
├── /Simulation
├── /Bridge
├── /Services
├── /Assets
├── /Game
└── /EndToEnd
```

---

# 4. Solution Layout Recommendation

Use multiple solutions, but one repo.

## Native / C++ solutions
- `AtlasEngine.sln`
- `NovaForge.sln`
- `AtlasServices.sln`

## Managed / .NET solutions
- `AtlasAI.Tools.sln`
- `AtlasAI.Services.sln`

## Optional umbrella generation
- generated workspace/solution files for convenience only, not as the primary long-term dependency structure

This avoids one gigantic fragile solution.

---

# 5. Ownership Rules

## WPF owns
- workspace shell
- docking UI
- chat UX
- logs/build/archive/design panels
- project/session workflow
- settings and desktop experience

## Native Atlas owns
- rendering
- simulation
- world state
- editor backend operations
- asset runtime systems
- gameplay execution
- performance-critical systems

## Shared owns
- contracts
- DTOs
- schemas
- transport protocols
- generated bridge bindings

## AtlasAI owns
- orchestration
- indexing
- memory
- code/design support
- task planning
- archive intelligence
- automation support

## NovaForge owns
- game rules
- progression
- faction/economy systems
- missions
- ship/station/interior gameplay
- player loops
- runtime HUD/UI only

---

# 6. Hard Separation Rules

## Never mix these
- WPF tooling UI with runtime in-game UI
- AtlasAI orchestration logic with low-level renderer code
- game-specific code inside core engine modules
- transport contracts directly inside UI-only assemblies
- archive/reference data inside live game runtime modules

## Keep boundaries strict
- `/Engine` must remain reusable beyond NovaForge
- `/Game/NovaForge` must not own engine primitives
- `/Tools` must call into services/contracts, not random native internals
- `/AI` must interact through contracts and indexed data, not ad hoc direct coupling

---

# 7. Migration Mapping from Current Repos

## MasterRepo → keep and reorganize into
- `/Engine`
- `/AI`
- `/Services`
- `/Docs`
- `/Config`
- `/Scripts`

## Arbiter → absorb into
- `/Tools/AtlasAI.WpfHost`
- `/Tools/AtlasAI.Shell`
- `/Tools/AtlasAI.Chat`
- `/Tools/AtlasAI.ArchiveUI`
- `/Tools/AtlasAI.BuildUI`
- `/Tools/AtlasAI.LogsUI`

## ArbiterAI → absorb into
- `/AI/AtlasAI.Core`
- `/AI/AtlasAI.Agents`
- `/AI/AtlasAI.Memory`
- `/AI/AtlasAI.Indexing`
- `/AI/AtlasAI.Codegen`

## NovaForge → absorb into
- `/Game/NovaForge/*`
- selective engine/editor-support pieces into `/Engine/*`
- content/data definitions into `/Content` and `/Data`

---

# 8. Suggested First Physical Moves

## Step 1
Create the new folder skeleton only.

## Step 2
Move docs first:
- architecture
- consolidation plans
- rename plans
- bridge specs
- design docs

## Step 3
Establish `/Shared/Contracts` and `/Tools/AtlasAI.Bridge`

## Step 4
Stand up `AtlasAI.WpfHost` shell in the new layout

## Step 5
Move Atlas-native service interfaces into `/Services`

## Step 6
Begin subsystem-by-subsystem migration from donor repos

---

# 9. Final Recommended Naming Standard

Use these prefixes consistently:

- `Atlas*` for engine/runtime/native platform systems
- `AtlasAI*` for AI/tooling/orchestration systems
- `NovaForge*` for game-specific systems

Examples:

- `AtlasRenderer`
- `AtlasWorldService`
- `AtlasAI.WpfHost`
- `AtlasAI.Chat`
- `NovaForge.Factions`
- `NovaForge.Missions`

This keeps ownership obvious at a glance.

---

# 10. Bottom Line

This structure gives you:

- a clean destination for every subsystem
- proper separation between tooling and runtime
- a strong WPF shell without polluting engine code
- a clear home for AtlasAI after the Arbiter rename
- a scalable architecture for future games or tools built on Atlas

It is the right layout for turning the current multi-repo ideas into one coherent long-term platform.
