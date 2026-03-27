# MASTERREPO_DEPENDENCY_RULES_AND_MODULE_REFERENCE_MATRIX.md

## Purpose

This document defines the **dependency rules**, **allowed module references**, and **forbidden coupling patterns** for the consolidated **MasterRepo** architecture.

It exists to keep the repo clean while combining:

- **Atlas** native engine/runtime/editor backend
- **AtlasAI** WPF tooling and orchestration
- **NovaForge** gameplay/content systems
- shared contracts, services, and data layers

Without strict dependency rules, the repo will drift into circular references, duplicated abstractions, and tooling/runtime coupling that becomes painful to maintain. This file is intended to prevent that.

---

# 1. Core Architectural Principle

Dependencies must flow **downward** toward more stable, reusable layers.

The intended direction is:

```text
Tools/UI
   ↓
Services / Bridge
   ↓
Shared Contracts / Schemas
   ↓
Engine / Runtime / Editor Backend
   ↓
Core Platform / Utilities

Game-specific modules depend on Engine modules.
AI modules depend on Shared contracts, Services, indexed project data, and approved integration surfaces.
```

The key idea is:

- higher-level systems may depend on lower-level systems
- lower-level systems must not depend on higher-level systems
- tooling must not directly reach into arbitrary engine internals
- game-specific code must not leak into reusable engine modules

---

# 2. Layer Model

## Layer A — Foundation
Most stable, lowest-level modules.

Examples:
- `Engine/AtlasCore`
- `Engine/AtlasPlatform`
- `Shared/Utilities`

## Layer B — Engine Systems
Reusable engine/runtime systems.

Examples:
- `Engine/AtlasRuntime`
- `Engine/AtlasRenderer`
- `Engine/AtlasPhysics`
- `Engine/AtlasAssets`
- `Engine/AtlasSimulation`
- `Engine/AtlasWorld`
- `Engine/AtlasVoxel`
- `Engine/AtlasNetworking`
- `Engine/AtlasEditorBackend`
- `Engine/AtlasToolsRuntime`

## Layer C — Shared Contracts and Protocols
Cross-boundary interface definitions.

Examples:
- `Shared/Contracts`
- `Shared/Schemas`
- `Shared/Protocols`
- `Shared/Interop`
- `Shared/Generated`

## Layer D — Services
Host processes and bridge implementations.

Examples:
- `Services/AtlasBuildService`
- `Services/AtlasAssetService`
- `Services/AtlasWorldService`
- `Services/AtlasSimulationService`
- `Services/AtlasEditorService`
- `Services/AtlasTelemetryService`
- `Services/AtlasSessionService`
- `Services/AtlasAI.ServiceHost`

## Layer E — Game Modules
Game-specific systems built on Atlas.

Examples:
- `Game/NovaForge/Core`
- `Game/NovaForge/Gameplay`
- `Game/NovaForge/Factions`
- `Game/NovaForge/Economy`
- `Game/NovaForge/Missions`
- `Game/NovaForge/Ships`
- `Game/NovaForge/Stations`
- `Game/NovaForge/Interiors`
- `Game/NovaForge/Characters`
- `Game/NovaForge/Combat`
- `Game/NovaForge/Mining`
- `Game/NovaForge/Exploration`
- `Game/NovaForge/Construction`
- `Game/NovaForge/PCG`
- `Game/NovaForge/UIRuntime`
- `Game/NovaForge/Server`

## Layer F — AI / Tooling
AtlasAI orchestration, WPF host, and UX modules.

Examples:
- `AI/AtlasAI.Core`
- `AI/AtlasAI.Agents`
- `AI/AtlasAI.Planning`
- `AI/AtlasAI.Memory`
- `AI/AtlasAI.Indexing`
- `AI/AtlasAI.Codegen`
- `AI/AtlasAI.Design`
- `AI/AtlasAI.Automation`
- `Tools/AtlasAI.WpfHost`
- `Tools/AtlasAI.Shell`
- `Tools/AtlasAI.Chat`
- `Tools/AtlasAI.Panels`
- `Tools/AtlasAI.ProjectExplorer`
- `Tools/AtlasAI.ArchiveUI`
- `Tools/AtlasAI.BuildUI`
- `Tools/AtlasAI.LogsUI`
- `Tools/AtlasAI.AssetUI`
- `Tools/AtlasAI.DesignUI`
- `Tools/AtlasAI.SettingsUI`
- `Tools/AtlasAI.VisualStudio`
- `Tools/AtlasAI.BlenderBridge`
- `Tools/AtlasAI.Bridge`

---

# 3. High-Level Dependency Rules

## Allowed direction
- Tools → Services / Bridge / Shared
- AI → Shared / Services / indexed data / approved engine-facing APIs
- Game → Engine / Shared
- Services → Engine / Shared / selected AI modules where explicitly approved
- Engine → Foundation / selected Shared utility abstractions only

## Forbidden direction
- Engine → Tools
- Engine → WPF
- Engine → NovaForge-specific gameplay modules
- Shared Contracts → Tools / Game / concrete Engine modules
- Foundation → anything above it
- Runtime UI → WPF tooling assemblies
- Game systems → direct references to WPF or desktop tooling
- AI modules → direct arbitrary references into renderer or platform code unless exposed via service/contract boundary

---

# 4. Module Dependency Matrix

Legend:

- **A** = Allowed
- **L** = Limited / only through narrow approved interfaces
- **N** = Not allowed

| From \ To | Foundation | Engine | Shared | Services | Game | AI | Tools |
|---|---:|---:|---:|---:|---:|---:|---:|
| Foundation | A | N | L | N | N | N | N |
| Engine | A | A | L | N | N | N | N |
| Shared | A | N | A | N | N | N | N |
| Services | A | A | A | A | L | L | N |
| Game | A | A | A | L | A | N | N |
| AI | A | L | A | A | L | A | N |
| Tools | A | N | A | A | L | L | A |

### Notes

- **Foundation → Shared** is limited to generic utilities only. Foundation must not grow feature awareness.
- **Engine → Shared** is limited to contracts, schemas, and protocol-safe abstractions. Engine should not depend on UI-driven or workflow-driven definitions.
- **Services → Game** is limited to game host/service modules that intentionally expose game-specific operations.
- **Services → AI** is limited to service host orchestration and approved automation or indexing workflows.
- **Game → Services** is limited and should generally be avoided at runtime except for explicit server/service boundaries.
- **AI → Engine** must occur only through approved APIs, contracts, indexing hooks, editor services, or telemetry surfaces.
- **Tools → Game** is limited to reading/manipulating game data through services or shared contracts, not direct deep coupling.
- **Tools → AI** is allowed because tooling is a consumer of AtlasAI features, but tooling should still prefer stable public APIs or service boundaries.

---

# 5. Allowed References by Area

## 5.1 Foundation

### Modules
- `AtlasCore`
- `AtlasPlatform`
- `Shared/Utilities` (carefully controlled)

### May reference
- C++ standard libraries / platform wrappers
- internal low-level utilities
- carefully selected generic utility code

### Must not reference
- WPF
- game rules
- AI orchestration
- services
- transport-specific business workflows
- NovaForge-specific data types

### Design rule
Foundation code must remain portable and reusable.

---

## 5.2 Engine

### Modules
- renderer
- physics
- simulation
- world
- voxel
- assets
- scripting
- runtime
- editor backend
- tools runtime

### May reference
- `AtlasCore`
- `AtlasPlatform`
- generic `Shared/Contracts` or `Shared/Protocols`
- other engine modules that sit at the same or lower abstraction level

### Must not reference
- WPF tooling
- `NovaForge/*`
- `AtlasAI.*`
- desktop-only workflows
- archive UI concepts
- chat concepts
- design-doc concepts

### Design rule
Engine should be reusable even if NovaForge disappeared tomorrow.

---

## 5.3 Shared

### Modules
- contracts
- schemas
- protocols
- generated DTOs
- interop definitions

### May reference
- foundation-safe utilities only

### Must not reference
- engine implementations
- game implementations
- UI assemblies
- service-specific logic
- model provider logic
- WPF types
- gameplay systems

### Design rule
Shared defines boundaries. It must not know who consumes them.

---

## 5.4 Services

### Modules
- build
- asset
- world
- simulation
- editor
- telemetry
- session
- AI service host

### May reference
- engine modules
- shared contracts
- approved AI modules
- selected game modules when the service is intentionally game-aware

### Must not reference
- WPF-specific UI code
- desktop controls
- visual theme logic
- in-game runtime UI

### Design rule
Services are executable adapters and orchestration layers. They expose capabilities; they do not own desktop UI.

---

## 5.5 Game / NovaForge

### Modules
- all NovaForge gameplay and runtime modules

### May reference
- engine modules
- shared contracts
- shared schemas
- game-common helper modules

### Must not reference
- WPF tooling
- AtlasAI desktop UI assemblies
- direct renderer internals unless via engine-facing abstractions
- arbitrary editor shell classes
- archive ingestion UI

### Design rule
NovaForge is a game built on Atlas, not a modifier of Atlas architecture.

---

## 5.6 AI / AtlasAI

### Modules
- orchestration
- agents
- planning
- memory
- indexing
- training
- inference
- archive
- codegen
- design
- automation

### May reference
- shared contracts
- service APIs
- indexing data
- structured project metadata
- approved editor/telemetry/build interfaces
- selected engine-facing APIs through contracts or adapters

### Must not reference directly
- WPF controls from non-UI AI assemblies
- raw renderer internals
- arbitrary gameplay internals
- platform window handles except in explicit bridge/integration modules

### Design rule
AtlasAI should reason over stable surfaces, not dig through unstable concrete implementations.

---

## 5.7 Tools / AtlasAI WPF

### Modules
- WPF host
- shell
- chat
- panels
- archive UI
- build UI
- logs UI
- settings UI
- project explorer
- bridge

### May reference
- services
- shared contracts
- approved AI public APIs
- controlled bridge implementations
- IDE integrations

### Must not reference
- arbitrary engine internals
- direct renderer implementation details
- raw simulation internals
- game runtime state structures except via bridge/service contracts

### Design rule
WPF is the workspace shell, not the owner of engine internals.

---

# 6. Special Boundary Rules

## 6.1 WPF Tooling Boundary
All WPF modules must treat native Atlas and NovaForge systems as remote or service-backed dependencies.

Preferred access patterns:
- service calls
- named pipes
- WebSocket / local IPC
- generated contract clients
- bridge adapters

Avoid:
- direct in-process grabs into native subsystem internals
- UI code calling renderer internals directly
- gameplay logic embedded into panel code

---

## 6.2 Editor Backend Boundary
`Engine/AtlasEditorBackend` is the native editor operation layer.

It may expose:
- scene operations
- transform/edit commands
- asset mutation endpoints
- debug draw hooks
- selection/inspection data
- save/load operations

It must not expose:
- WPF-specific view models
- desktop theme logic
- panel lifecycle logic
- chat workflow logic

---

## 6.3 Runtime UI vs Tooling UI
`Game/NovaForge/UIRuntime` is for:
- HUD
- menus
- in-game overlays
- gameplay screens

`Tools/AtlasAI/*` is for:
- desktop shell
- workspace
- archive
- chat
- logs
- build tools
- design/document panels

These two UI worlds must remain separate.

---

## 6.4 AI Read/Write Access Rule
AtlasAI may:
- read indexed repo data
- read docs, design plans, logs, diagnostics
- propose code changes
- trigger approved services
- operate on structured data through stable contracts

AtlasAI must not:
- mutate arbitrary engine state directly
- bypass service validation
- modify live runtime state without an explicit command surface
- embed itself into low-level engine systems through ad hoc calls

---

# 7. Dependency Rules by Common Scenario

## Scenario A — WPF panel wants to show live simulation data
Allowed path:

`AtlasAI.LogsUI`  
→ `AtlasAI.Bridge`  
→ `AtlasSimulationService`  
→ `AtlasSimulation` / `AtlasToolsRuntime`

Not allowed:

`AtlasAI.LogsUI`  
→ direct reference into `AtlasSimulation` internals

---

## Scenario B — Game faction system needs world queries
Allowed path:

`NovaForge/Factions`  
→ `AtlasWorld`

This is normal.

Not allowed:

`NovaForge/Factions`  
→ `AtlasAI.Chat`

---

## Scenario C — AtlasAI wants repo context for code assistance
Allowed path:

`AtlasAI.Codegen`  
→ `AtlasIndexService` or indexed repository database  
→ shared contract models

Not allowed:

`AtlasAI.Codegen`  
→ direct UI project tree state as source of truth

---

## Scenario D — Build panel wants to compile the game
Allowed path:

`AtlasAI.BuildUI`  
→ `AtlasBuildService`

Not allowed:

`AtlasAI.BuildUI`  
→ shelling into random scripts with no service boundary as the permanent architecture

---

## Scenario E — Engine wants to log telemetry
Allowed path:

`AtlasRenderer`  
→ `AtlasCore` logging interfaces  
or  
`AtlasRenderer`  
→ telemetry event sink abstraction in shared/foundation-safe layer

Not allowed:

`AtlasRenderer`  
→ `AtlasAI.LogsUI`

---

# 8. Friend Modules and Narrow Exceptions

Some exceptions are acceptable, but only as documented, narrow cases.

## Allowed narrow exceptions
- `AtlasToolsRuntime` may expose tooling-friendly telemetry and inspection APIs over engine systems
- `AtlasEditorBackend` may use selected renderer/editor integration hooks
- `AtlasAI.Bridge` may contain native interop or transport code that is otherwise not used by general WPF modules
- `AtlasAI.VisualStudio` and `AtlasAI.BlenderBridge` may interact with external tool APIs directly

## Process rule
Any exception should be documented in:
- this file
- the module README
- the build/solution config if enforcement is automated

---

# 9. Circular Dependency Prevention Rules

## Hard rules
- No engine module may depend on a game module
- No shared contract module may depend on an implementation module
- No WPF module may become the hidden owner of service business logic
- No AI module may require UI assemblies to function
- No service should require WPF to be running

## Recommended enforcement
- separate solutions by layer
- static analysis checks
- include path restrictions
- project reference audits
- CI rule that blocks new forbidden references

---

# 10. Build-Time Enforcement Strategy

## C++ side
- restrict include directories
- use module-private headers
- ban upward includes in review
- keep public/private include trees separate
- consider dependency graph generation in CI

## .NET side
- use explicit project references only
- do not allow transitive “just because it compiles” reference growth
- separate contracts from implementations
- avoid giant utility assemblies that become dependency magnets

## Repo policy
Every new module should answer:
1. What layer is it in?
2. What lower layers may it reference?
3. What public API does it expose?
4. What is explicitly forbidden?

---

# 11. Recommended Allowed Reference Summary

## Engine may reference
- Foundation
- selected Shared contracts/protocols
- lower-level Engine modules

## Game may reference
- Engine
- Shared
- selected Service contracts only when intentional

## Services may reference
- Engine
- Shared
- selected Game modules
- selected AI modules

## AI may reference
- Shared
- Services
- indexed data stores
- approved Engine-facing APIs via contracts

## Tools may reference
- Shared
- Services
- AI public APIs
- bridge/client adapters

## Nothing may reference upward into WPF from lower layers

That one rule alone will save a lot of pain.

---

# 12. Red Flags to Watch For

If any of these start showing up, the architecture is drifting:

- WPF view models containing gameplay logic
- Engine modules importing NovaForge headers
- Shared contract assemblies importing service code
- AI orchestration modules coupled to visual controls
- build logic duplicated in UI and services
- multiple “utility” libraries becoming unowned dumping grounds
- editor/runtime concerns mixed into desktop shell code
- data schemas duplicated between services and game runtime

---

# 13. Final Bottom Line

The dependency model should remain:

- **Atlas** owns reusable engine/runtime/editor-backend systems
- **NovaForge** owns game-specific logic
- **AtlasAI** owns orchestration, intelligence, and tooling UX
- **Shared** owns boundaries and schemas
- **Services** own execution surfaces and process boundaries

If this is enforced, MasterRepo can absorb the other repos cleanly.

If this is not enforced, the consolidation will slowly turn into one giant coupled codebase that is hard to test, hard to refactor, and hard to scale.
