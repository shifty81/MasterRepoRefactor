# Master Repo — Unified Design Document

> **Status:** Authoritative canon. All systems, features, and architecture decisions should be evaluated against this document.
>
> **Source:** Derived from `RepoDirective1` chat session. Original chat archived at `Docs/Archive/Chats/`.

---

## Preamble

This is the single cohesive Master Repo design direction covering Atlas, NovaForge, Arbiter, tooling, PCG, in-game systems, editor systems, AI systems, and repo consolidation.

The goal is to turn existing scattered efforts into a single ecosystem that supports:

- A custom engine / editor / tool suite
- A game development platform
- A runtime in-game tooling layer
- A fully integrated AI development assistant
- A unified content pipeline
- A single project architecture that can build games, tools, and software from the same foundation

### Core Truths (Non-Negotiable)

| Rule | Detail |
|------|--------|
| No ImGui | All UI is custom |
| Custom UI only | Low poly art direction across the project |
| First-person always | Where player embodiment exists |
| Tooling works in-editor and in-game | Where intended |
| AI is first-class | Not a bolt-on |
| Master Repo is source of truth | Existing repos are feature archives / donor repos |

---

## 1. Master Repo Identity

### Project Purpose

Master Repo is the umbrella platform containing:

- Core Engine Layer
- Editor / IDE Layer
- Tooling Layer
- AI / Arbiter Layer
- Game Framework Layer
- NovaForge Game Layer
- PCG / Simulation / Worldgen Layer
- Runtime Build / Asset / Data Pipeline
- Remote / Web / Multiuser Collaboration Layer

This is not "just a game repo" or "just an AI coding tool." It is:

- A game engine
- A development environment
- A project-aware AI operating layer
- A runtime world simulation framework
- A content authoring platform

---

## 2. High-Level Pillars

### A. Engine

Custom engine foundation handling:

- Rendering
- Scene graph
- ECS or object/component framework
- Input
- Physics, audio, animation, materials/shaders
- Save/load, asset streaming
- Gameplay framework, networking/server support
- Tooling hooks

### B. Editor / IDE

A custom editor with:

- Dockable panels
- Integrated code editor
- Asset browser, project browser
- Scene/world editor
- Property inspector, outliner
- Log console
- Build/deploy tools
- AI chat and task orchestration
- Documentation / PDF / web viewer
- Diff preview / code patch preview
- Repo map and index views

### C. Arbiter AI

The embedded assistant layer that:

- Learns the workspace
- Indexes code and assets
- Generates/refactors code
- Explains systems, plans features
- Audits repos against architecture rules
- Proposes patches through safe preview/delta workflows
- Operates from project architecture rules

### D. Tooling Layer

A runtime/editor hybrid tool system allowing:

- Overlay tools, object placement, PCG debugging
- Prefab editing, ship/station assembly
- Mission/economy inspection, NPC/faction debugging
- Build/repair/dev commands, live game-state inspection

### E. NovaForge Game Framework

The flagship playable product inside Master Repo:

- FPS / first-person
- Ship gameplay, station gameplay, EVA
- Mech suit use, salvage, mining, scanning, repair
- Crafting, progression, factions, missions, fleet systems
- Economy, seasonal universe progression, titan endgame loop

### F. PCG Framework

A unified procedural system driving:

- Sectors, stations, derelicts, ships, rooms, caves/ruins
- Loot, mission generation, economy regions, faction spread
- Visual style propagation from part tiers/upgrades

---

## 3. Non-Negotiable Rules

### UI Rules

- No ImGui
- No temporary debug GUI dependence for shipping systems
- All final UI uses the custom project UI framework
- Editor and runtime UI share style language where sensible
- Chat UI can mimic modern assistant layout, but remains custom

### Gameplay Rules

- First-person wherever player embodiment exists
- Ship interiors are explorable
- Airlocks matter; life support matters
- Gravity can differ by area
- EVA is systemic, not scripted fluff
- Tethers, oxygen, power, damage, and repairs are real systems

### Tooling Rules

- Tooling input must be clearly separated from gameplay input
- Overlay mode cannot corrupt gameplay control state
- Tooling layer must be able to inspect, manipulate, and visualize runtime systems
- F12/dev overlay behavior must be deterministic and clean

### AI Rules

- AI must be workspace-aware
- AI must follow repo conventions and architecture law
- AI suggestions must be previewable before apply
- AI should operate through safe patch/delta systems, not blind overwrite
- AI must become a project "Arbiter," not just a chatbot

### Data Rules

- Data-driven where possible
- JSON/spec-driven formats for gameplay systems
- Versioned data schemas
- Asset metadata and procedural metadata must be first-class
- Save formats and generation seeds must be structured and inspectable

### Repo Rules

- Existing repos are imported, audited, stripped, renamed, normalized
- Legacy naming conflicts must be removed
- Any old EVE-derived naming or borrowed identifiers must be audited out
- Documentation must be rewritten to Master Repo standards

---

## 4. Legacy Repo Strategy

### Atlas

Contributes to engine/editor/tooling architecture, custom GUI direction, editor framework concepts, and project architecture constraints. Atlas uses no ImGui and should remain all custom UI.

### NovaForge

Main donor for gameplay systems, survival/resource loops, ship/station/interior concepts, progression systems, worldbuilding, faction/season/titan design, in-game tooling concepts, and low-poly survival-space style direction.

### Arbiter / AI Concepts

Donor source for AI orchestration, workspace indexing, repo awareness, patch generation, planning mode, assistant UX, web/chat/remote access concepts, and autonomous but governed tooling direction.

### Builder / Pioneer Work

Contributes ship builder logic, snapping systems, modular construction, assembly UI, part hierarchy, and possibly station/module construction workflow.

### All Other Archived Repos

Treated as donor archives, feature mines, patterns to salvage, code to normalize or rewrite into Master standards.

---

## 5. Target Repo Structure

```
MasterRepo/
  apps/
    Editor/        game editor / IDE
    Game/          game client
    Server/        dedicated server
    WebPortal/     optional remote web portal
    Tools/         standalone dev tools

  engine/
    Core/          platform abstraction, main loop, memory, logging, config, events
    Math/          math types, utilities
    Memory/        allocators
    ECS/           entity component system
    Scene/         scene management
    Asset/         asset registry, streaming, serialization
    Render/        renderer, shaders, materials, lighting
    Physics/       collision, simulation
    Audio/
    Animation/
    Navigation/
    Networking/
    SaveSystem/
    Scripting/
    UI/            custom UI framework
    Tooling/       tooling overlay hooks

  editor/
    Framework/     docking, panels, commands
    Panels/        all panel implementations
    AssetBrowser/
    SceneEditor/
    PropertyInspector/
    Outliner/
    Console/
    BuildTools/
    DocViewer/     markdown, PDF, web viewer host
    DiffPreview/   split-diff code preview
    RepoMap/
    AI/            Arbiter chat integration

  ai/
    ArbiterCore/   orchestration core
    WorkspaceIndexer/
    Embeddings/
    Retrieval/
    PatchPlanner/
    DiffEngine/
    CommandRouter/
    ModelProviders/ local/remote model abstraction
    Conversation/
    Memory/
    Policies/
    Automation/

  game/
    Core/
    Player/
    Inventory/
    Items/
    Crafting/
    BuildSystem/
    Ships/
    Stations/
    EVA/
    Mechs/
    Survival/
    Missions/
    Factions/
    Economy/
    Combat/
    Loot/
    Progression/
    Skills/
    TechTree/
    Titans/
    Seasons/
    World/
    PCG/
    UI/

  data/
    configs/
    items/
    recipes/
    loot/
    missions/
    factions/
    ships/
    stations/
    sectors/
    anomalies/
    storms/
    tech/
    skills/
    economy/

  content/
    meshes/
    materials/
    textures/
    animations/
    sounds/
    music/
    prefabs/
    modular_parts/
    characters/
    ships/
    stations/
    ruins/

  docs/
    architecture/
    design/
    engine/
    editor/
    tooling/
    ai/
    gameplay/
    pipelines/
    schemas/
    migration/
    audits/
    archive/

  scripts/
    bootstrap/
    migration/
    build/
    validation/
    indexing/
    packaging/
```

---

## 6. Core Systems

### 6.1 Engine Core

Must provide:

- Platform abstraction, main loop
- Memory allocators, logging, config loading
- Task/job system, event bus
- Scene management, asset registry
- Serialization, plugin/module registration

### 6.2 Rendering

Needs to support:

- Low poly aesthetic pipeline
- Stylized but scalable rendering
- Material instances, decals, lighting, shadowing
- Transparency, controlled post-process for readability
- Debug draw and tooling overlays
- Preview scenes for assets/characters/items

### 6.3 UI Framework

Custom UI system supporting:

- Windows, tabs, docking
- Lists, trees, property grids
- Markdown-like text blocks, code blocks, text input
- Chat layout, graph views
- Inventory grids, radial menus
- In-game HUD widgets, editor widgets
- Theme/styling system

This single UI framework powers: game HUD, pause/inventory screens, editor panels, AI chat, build menus, ship builder, station management, document viewers.

### 6.4 Input Architecture

Separate input layers:

- Gameplay input
- UI input
- Tooling overlay input
- Editor viewport input
- Text/chat input

**Required behavior when tooling overlay is active:**

- Gameplay camera should not drift
- Cursor visible when intended; ghost cursor bugs must not occur
- Middle mouse drag for freelook in tooling layer is acceptable
- Movement and camera interaction states cleanly gated
- Overlay activation must not break WASD state or pointer lock

Built around an **Input Routing Stack** with: active context, focused widget, captured pointer owner, camera control owner, and action maps by mode.

---

## 7. Editor / IDE Plan

The editor is not just a code window — it is a full project cockpit.

### Required Panels

| Panel | Purpose |
|-------|---------|
| Project Explorer | Navigate repo structure |
| Asset Browser | Browse all assets |
| Scene Hierarchy / Outliner | Manage scene objects |
| Inspector / Details | Inspect and edit properties |
| Console / Logs | Build, runtime, and AI logs |
| Build / Run / Package | Build pipeline management |
| AI Chat | Arbiter interaction |
| Repo Map | Visualize repo structure and dependencies |
| Knowledge Index | Arbiter's workspace awareness |
| Doc / PDF / Web Viewer | Read docs, PDFs, and web resources |
| Diff / Patch Preview | AI patch staging and review |
| Search Everywhere | Global search across code, docs, assets |
| Task / Roadmap | Planning and progress |
| Data/Schema Editor | Edit JSON schemas inline |
| PCG Preview | Visualize and debug PCG output |
| World Generation | Sector and world tools |
| Ship/Station Builder | Modular construction |
| Design Document System | Author and browse design docs |

### Code Editing

- Syntax highlighting, split view, diff preview
- AI patch preview in split window (side-by-side staged form)
- Symbol navigation, search/replace, diagnostics
- Jump to definition, references, inline explain/fix tools
- Multi-file patch staging

### Document / Web Support

The internal IDE displays:

- Source files, markdown, project docs, PDFs, web pages, reference docs, internal design docs

---

## 8. Arbiter AI Role

Arbiter is not "a chatbot tab." It is the project intelligence layer.

### Arbiter Modes

| Mode | Description |
|------|-------------|
| Conversation | Brainstorming, planning, design work |
| Workspace Analysis | Reads repo and answers from actual project state |
| Patch/Refactor | Generates code edits, proposes diffs, explains impact |
| Audit | Scans project against architecture rules, highlights drift |
| Builder | Scaffolds modules, classes, schemas, configs, UI skeletons |
| Documentation | Writes/re-writes docs in project format |
| Runtime Debug | Understands logs, runtime state, content pipelines, build failures |

### Knowledge Sources

- Repo files, schema files, docs
- Asset metadata, code index, symbol graph
- Build logs, runtime logs, generation history
- Project memory/rules

### Arbiter Rules

- Never overwrite blindly
- Always show intent and scope
- Operate through delta/patch system
- Keep architecture alignment visible
- Prioritize local project truth over generic guesses

### Long-Term

- Correction reinforcement
- Learning from the workspace
- Ability to improve output from feedback
- Multiple models/providers via AI Provider Abstraction layer

---

## 9. Web Server / Remote Access

An optional hosted web portal exposing remote functionality.

### Goals

- Remote dashboard, login/auth, permission levels
- Remote AI chat
- Project overview, logs/build status
- Remote control of allowed tools
- Documentation access
- Collaboration/session status

### Roles

- Owner, Admin, Developer, Viewer, AI-only restricted

### Modes

- **Local-only mode** — Safe local LAN access
- **Authenticated remote mode** — Optional if exposed beyond LAN

Should remain **optional and disabled by default** unless intentionally enabled.

---

## 10. Multiuser Collaboration

Future-facing feature designed into data ownership and change-tracking systems early.

- Shared sessions, multiuser editing
- Shared comments/annotations, task assignment
- AI-assisted collaborative planning
- Presence indicators in editor/world
- Review/approval workflow for patches

---

## 11. NovaForge Game Design

### Core Fantasy

A low-poly first-person systemic sci-fi survival / salvage / build / exploration experience:

- Ship interior living, airlocks, EVA, tethered survival
- Resource extraction, modular building, salvage
- Ruins/anomalies, faction conflict, economy
- Tech progression, fleet development, titan-scale endgame
- Seasonal reset loop

---

## 12. Player Modes

| Mode | Description |
|------|-------------|
| On Foot | First-person, survival, crafting, repair, scanning, inventory, combat |
| Ship Pilot | First-person cockpit, ship systems control, docking, power/fuel/life support |
| EVA | First-person spacewalk, tether logic, oxygen/power routing, salvage/repair |
| Mech Suit | First-person transfer into mech, utility/salvage/mining/combat, socketed tools |

---

## 13. Ship Interior + Airlock + EVA System

A major foundational gameplay loop and signature system.

### Ship Interior

A systemic habitat with: rooms, pressure zones, powered devices, gravity-enabled interior zones, storage, crafting/refining, airlock, suit prep area, modular upgrades.

### Airlock Logic

Handles: inner door, chamber state, outer door, pressurize/depressurize, safety locks, player transition between interior and EVA space.

### Life Support

Per ship/station: oxygen supply, power requirement, damage/failure states, room/zone support, refill logic.

### Gravity

Per interior or room zone: active when generator functional, can fail or be disabled. EVA/exterior always zero-G unless special zones.

### Tether

When leaving ship: auto deploys, routes oxygen/power, retracts on return. Has max length, may snag — becomes a critical risk/reward mechanic.

---

## 14. Salvage / Derelict / Mech / EVA Loop

One of the strongest identity loops in the project.

### Loop

1. Leave ship through airlock
2. Tether connects to main ship
3. EVA to derelict or ruin
4. Scan target
5. Cut/open/extract modules/materials
6. Fight hazards or environmental risks
7. Haul resources back
8. Process/refine/craft upgrades
9. Improve ship, mech, station, gear
10. Access harder locations

### Salvage Content Types

- Intact containers, damaged machinery, hull panels, wiring/conduit
- Reactors, computers/data cores, abandoned drones
- Faction wrecks, ancient ruins/anomaly debris

### Mech Use

Primarily for: EVA utility, exterior ship repairs, salvage, mining, cargo handling, limited combat, ground utility.

---

## 15. Building — Ship Builder / Station Builder

Two parallel systems:

### Easy Build

- Snapping modules, large pieces, accessible construction
- Quick ship/station creation

### Advanced Build

- Detailed part placement, weld logic
- Pipe/conduit/cable routing
- Structural parts, modules and subsystems
- Surface/detail propagation
- Part health and durability, system-dependent visual upgrades

### System Propagation

When the player upgrades system tiers:

- Reactor upgrade changes visual complexity
- Armor upgrade changes room/exterior detail
- Conduits/pipes/panels improve visually
- Interiors gain richer details
- Exteriors reflect tech tier

This is part of the PCG style inheritance layer.

---

## 16. Crafting / Survival / Progression

### Survival Base Loop

- Oxygen, fuel, power, raw materials
- Storage, manufacturing, mobility
- Damage/repair

### Crafting Complexity

Chained crafting through multiple machines:

- Assemblers, refiners, chemical processors
- Fabricators, electronics benches, module assembly
- On-person portable crafting (if backpack assembler installed)

### Player Rig UI (Tab)

- Equipment, upgrades, inventory
- Crafting (if portable assembler installed)
- Suit stats: power/oxygen/damage readouts

Separate from editor tooling.

---

## 17. Economy / Factions / Fleets / Seasons

### Economy

- Resources, supply/demand, production chains, trade routes
- Mining zones, station demand, scarcity regions, pricing logic

### Factions

- Identity, relationship states, territory
- Fleet styles, tech/style differences
- Procedural mission influence

### Fleets

- Patrol fleets, station defense, system defense
- War fleets, titan support fleets, job/behavior profiles

### Seasons

Universe reset/wipe around titan race progression:

- Universe cycle escalating toward titan objective
- Monthslong arc, end-of-season collapse/reset
- Legacy reward for successful titan jump

---

## 18. Skills / Tech Tree / Progression

Skills train over time, accelerated by relevant actions:

- Mining skill advances faster while actively mining
- Engineering skill accelerates through repairs/building
- Scanning through exploration/scanning activity
- Piloting through flight and docking practice

### Parallel Trees

- Personal skills (suit/mech proficiency, piloting, industrial, science/scanning, combat)
- Faction unlocks
- Blueprint/tech unlock tree

---

## 19. PCG Master Plan

PCG is not just terrain — it drives almost everything.

### PCG Domains

- Sectors, star systems, ruins, derelicts
- Mission targets, ship variants, station layouts, interior details
- Loot placement, hazards, storms/anomalies
- Faction presence, economy nodes, room dressing, style propagation

### PCG Style Rules

Low-poly style consistency enforced by:

- Modular kit rules, silhouette rules
- Density budgets, detail tier rules
- Color/material family rules, part inheritance rules

### Upgrade Propagation

As system tiers increase:

- Structural visuals change
- Interior props shift
- Exterior modules evolve
- Pipeline/conduit density changes
- UI and interaction affordances reflect tech growth

---

## 20. Data-Driven Formats

Every schema should be: **versioned, documented, validated, editor-readable, AI-readable**.

### Schemas to Define

- Items, inventory, modules, recipes, loot tables
- Factions, AI states, missions, contracts
- Anomaly/storm definitions, fleet jobs, economy routes
- War/sector control, titan construction, season settings
- UI definitions, debug overlay definitions, console commands
- Input/actions, camera modes, audio/music, VFX/particles
- Animation rigs, collision/hitboxes, projectiles, vehicle/ship physics
- Saves

---

## 21. Tooling Layer Design

A tooling overlay available in-game without turning the game into a full editor mess.

### Goals

- Inspect runtime objects, place/test content
- Preview PCG, gizmos (move/rotate/scale)
- Inspect systems, spawn/debug, tune gameplay values
- Manage generation seeds, access live diagnostics
- Author specific runtime-facing content

### Input Modes

- Gameplay mode, tooling mode, cursor mode
- Freelook mode, gizmo drag mode, panel interaction mode

### Tool Panels

- Object inspector, world tools, generation tools
- Entity spawner, debug stats
- Mission/economy/faction visualizers
- Ship/station builder
- Live data editor

---

## 22. Design Document System

### Design Document System

A structured documentation system for:

- Feature specs, implementation plans
- Schema docs, architecture docs
- Art/style docs, gameplay pillar docs
- Migration/audit records

### Design Panel System

An editor-facing panel framework for:

- Displaying docs
- Linking docs to systems/assets/modules
- AI-assisted drafting/refactoring
- Turning design docs into scaffolds/tasks

Connects: planning → implementation → AI generation → architecture enforcement.

---

## 23. Migration Strategy

### Phase 0 — Archive and Classify

For each donor repo:

- Capture repo tree
- Identify core systems
- Label code as: keep / rewrite / extract concept / delete
- Identify naming conflicts, dead code, external dependencies, UI assumptions, engine assumptions

### Phase 1 — Feature Extraction Map

Create matrix: source repo → feature → current quality → dependencies → migration target module → rewrite needed? → priority.

### Phase 2 — Naming and Law Audit

- Remove legacy borrowed names
- Normalize terminology
- Rename to Master Repo canon
- Rewrite docs accordingly

### Phase 3 — Skeleton Merge

Create empty clean Master Repo module tree first. Then import features deliberately into correct homes.

### Phase 4 — Rewrite Around Interfaces

Keep: useful logic, useful data, useful concepts, useful assets/tools.

Replace: bad module boundaries, legacy hacks, inconsistent naming, UI shortcuts, one-off project assumptions.

---

## 24. Refactor vs Preserve

### Preserve

- Strong system concepts, gameplay loops
- Builder/salvage ideas, AI integration concepts
- Useful data formats, reusable utility code
- Content pipelines that can generalize

### Refactor Hard

- Naming, module boundaries, UI implementation
- Duplicated systems, ad hoc file layouts
- Inconsistent config handling, old one-project assumptions
- Ungoverned AI/codegen behavior
- Any debug-only interface pretending to be final UI

### Delete

- Abandoned duplicate experiments
- Conflicting architecture branches
- Legacy naming contamination
- Placeholder patterns that would poison future scaling

---

## 25. Implementation Order

### Phase A — Foundation

- Repo restructure, module registration/build system
- Logging/config/events, asset registry, serialization basics
- Custom UI foundation, input routing foundation
- App shell for Editor/Game/Server

### Phase B — Editor Core

- Docking layout, file/project browser
- Outliner, inspector, console
- Document viewer host, code editor integration
- Split diff preview, AI panel shell

### Phase C — Arbiter Core

- Workspace indexing, repo map
- Retrieval/search, chat memory scoped to workspace
- Patch planning, diff proposal flow
- Documentation assistant flow

### Phase D — Gameplay Vertical Slice

- Player controller first-person
- Ship interior prototype, gravity zones, life support stub
- Airlock system, EVA controls, tether system
- Simple derelict salvage target
- Inventory and pickup loop

### Phase E — Builder / Tooling

- Tooling overlay input routing, gizmos
- Object inspect/manipulate, ship modular placement
- Simple snapping, runtime debug panels

### Phase F — Crafting / Progression

- Item schema, recipe schema, machine chains
- Rig/equipment UI, skill progression skeleton
- Tech unlock framework

### Phase G — World / PCG

- Sector generation, derelict generator
- Interior room generator, loot placement
- Faction/economy seed data, storm/anomaly system shells

### Phase H — Web / Remote / Collaboration

- Local web panel, login/auth, remote chat
- Remote dashboards, safe action permissions

### Phase I — Endgame Systems

- Fleets, war/territory, titans, season cycle
- Advanced economy, advanced missions

---

## 26. Fastest Playable Vertical Slice

**Target:** "Ship–Airlock–EVA–Derelict–Salvage–Return"

### Required Elements

- First-person player in interior ship room
- Functioning airlock
- Gravity inside, zero-G outside
- Tether auto deploy/retract
- Oxygen/power dependency
- Derelict target
- Salvage interaction, carry/extract loot
- Return to ship
- Process/craft one upgrade

### What This Proves

- First-person framework
- Interior/exterior state transition
- Life support concepts
- EVA controls
- Salvage identity
- Crafting and progression foundation
- NovaForge identity
- Master Repo architecture viability

---

## 27. Tool / AI UX Vision

The final editor/app should feel like:

- A modern custom IDE
- A project command center
- A design/wiki browser
- A live debug console
- An AI engineering assistant
- A content workstation
- A remote-capable control hub

Users should be able to do all of the following from a single environment: chat with Arbiter, inspect code and docs, read PDFs, browse project web resources, preview AI changes, manipulate worlds, debug systems, build content, launch/test runtime, and manage game/server/tool states.

---

## 28. Gaps to Cover Explicitly

### Engine / Tooling

- Plugin/module lifecycle, schema validation tools
- Command console + command registry, settings/profile system
- Project templates, automated migration scripts
- Build verification and audit tools

### Editor

- Global search, symbol/index search
- Content references, dependency graph views
- Undo/redo architecture, tab/session restore

### AI

- Patch safety model, workspace scoping rules
- Approval workflow, architecture constraints engine
- Prompt policy templates by task type
- Local model/provider abstraction

### Gameplay

- Damage propagation, power network simulation
- Room/zone graph logic, item mass/transport logic
- Door/airlock permission state, hazard feedback/readability
- Progression pacing tools

### Content Pipeline

- Prefab versioning, modular kit validation
- Generation metadata tagging, art style conformance checks
- Asset dependency tracking

---

## 29. Definition of Done

Master Repo is "cohesive" when:

- [ ] All active systems live in one clean repo tree
- [ ] Old repos are donor archives, not competing sources of truth
- [ ] UI is custom throughout
- [ ] Arbiter can reason about the workspace
- [ ] The editor can browse code/docs/web/PDF
- [ ] AI changes appear in safe split-preview flows
- [ ] Gameplay and tooling input are cleanly separated
- [ ] NovaForge vertical slice works inside Master architecture
- [ ] PCG, data schemas, and docs are standardized
- [ ] Naming and documentation are normalized
- [ ] The project can scale without re-architecting again

---

## 30. Final Canon Summary

### What This Project Is

A unified custom platform merging: engine, editor, IDE, AI assistant, runtime tooling, world generation, survival/salvage game framework, remote/web access, and future collaboration tools.

### What Each Component Becomes

| Component | Role |
|-----------|------|
| **NovaForge** | The flagship game and proving ground for the platform |
| **Arbiter** | The project-aware intelligence layer embedded throughout |
| **Atlas** | Custom UI/editor standards and architecture direction |
| **Legacy Repos** | Harvested, audited, renamed, normalized, and absorbed or archived |

### What Must Happen First

Build clean foundations, then prove the ship–airlock–EVA–salvage loop inside the new architecture.

---

## 31. Executive Roadmap

Immediate next actions:

1. Freeze Master Repo laws and naming canon
2. Build target repo structure
3. Audit donor repos into keep/rewrite/delete matrix
4. Stand up custom UI foundation
5. Stand up editor shell + document host + AI shell
6. Stand up Arbiter indexing/retrieval core
7. Build first-person ship interior + airlock + EVA vertical slice
8. Add salvage loop
9. Layer builder/tooling systems on top
10. Expand toward economy/factions/PCG/endgame

---

## 32. Final Single-Chat Directive

> From this point onward, everything in the project should be interpreted through this rule:
>
> **Master Repo is the unified destination architecture.**
>
> All prior ideas, systems, repos, and experiments are to be:
> - aligned to it,
> - refactored for it,
> - renamed for it,
> - or discarded if they fight it.
>
> This is the cohesive master direction.
