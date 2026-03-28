# Master Repo — Unified Refactor & Integration Directive

> **Status:** Authoritative  
> **Source:** Converted from `Docs/Archive/Chats/RepoDirective1.txt` (original planning chat)  
> **See also:** [MASTER_DESIGN_DOCUMENT.md](MASTER_DESIGN_DOCUMENT.md) · [MISSING_SYSTEMS_ADDENDUM.md](MISSING_SYSTEMS_ADDENDUM.md)

---

## Purpose

This document is the single cohesive project direction for **MasterRepo**. It defines the identity, pillars, non-negotiable rules, and structure of the entire platform — covering Atlas (engine/editor), NovaForge (game), AtlasAI (tooling/AI), and the unified content pipeline.

The goal is a single ecosystem that supports:

- A custom engine/editor/tool suite
- A game development platform
- A runtime in-game tooling layer
- A fully integrated AI development assistant
- A unified content pipeline
- A single project architecture that can build games, tools, and software from the same foundation

---

## 1. Master Repo Identity

**MasterRepo is the umbrella platform containing:**

| Layer | Description |
|---|---|
| Core Engine Layer | Physics, rendering, ECS, audio, animation, input, scene graph |
| Editor / IDE Layer | Custom dockable editor, asset browser, scene editor, inspector |
| Tooling Layer | Runtime/editor hybrid overlay tools, PCG debug, inspection |
| AtlasAI Layer | Workspace-aware AI assistant, code generation, patch planning |
| Game Framework Layer | Reusable gameplay primitives: inventory, progression, factions |
| NovaForge Game Layer | The flagship playable product (FPS, ship gameplay, EVA, economy) |
| PCG / Simulation Layer | Sectors, stations, missions, economy regions, fauna/flora |
| Asset / Data Pipeline | Import rules, naming conventions, schema validation |

MasterRepo is simultaneously:
- A **game engine**
- A **development environment**
- A **project-aware AI operating layer**
- A **runtime world simulation framework**
- A **content authoring platform**

---

## 2. High-Level Pillars

### A. Engine (Atlas)

Custom engine foundation handling:

- Rendering (custom pipeline, no third-party render frameworks as a hard dependency)
- Scene graph + ECS
- Input (context-aware, remappable)
- Physics, audio, animation
- Materials / shaders
- Save / load
- Asset streaming
- Gameplay framework
- Networking / server support
- Tooling hooks

### B. Editor / IDE (Atlas Editor)

A custom editor with:

- Dockable panels
- Integrated code editor
- Asset browser + project browser
- Scene / world editor
- Property inspector + outliner
- Log console
- Build / deploy tools
- AI chat and task orchestration
- Documentation / PDF / web viewer
- Diff preview / code patch preview
- Repo map and index views

### C. AtlasAI (formerly Arbiter)

The embedded assistant layer that:

- Learns the workspace
- Indexes code and assets
- Generates / refactors code
- Explains systems
- Plans features
- Audits repos
- Compares implementation against project rules
- Proposes patches through safe delta/diff workflows
- Operates from project architecture rules
- Supports correction/reinforcement workflows

### D. Tooling Layer

A runtime/editor hybrid tool system that allows:

- Overlay tools (F12/dev mode)
- Object placement
- PCG debugging
- Prefab editing
- Ship / station assembly
- Mission / economy inspection
- NPC / faction debugging
- Build / repair / dev commands
- Live game-state inspection

### E. NovaForge Game Framework

The flagship playable product inside MasterRepo:

- FPS / first-person always where player embodiment exists
- Ship gameplay, station gameplay, EVA
- Mech suit use
- Salvage, mining, scanning, repair, crafting
- Progression, factions, missions, fleet systems, economy
- Seasonal universe progression, titan endgame loop

### F. PCG Framework

A unified procedural system driving:

- Sectors, stations, derelicts, ships, rooms, caves/ruins
- Loot, mission generation, economy regions
- Faction spread, visual style propagation from part tiers/upgrades

---

## 3. Non-Negotiable Rules

### UI Rules

- **No ImGui** in any shipping or production system
- All final UI uses the custom Atlas UI framework
- Editor and runtime UI share a consistent style language
- Temporary debug overlays may not become shipping dependencies

### Gameplay Rules

- First-person wherever player embodiment exists
- Ship interiors are explorable; airlocks, life support, and gravity are real systems
- EVA is systemic: tethers, oxygen, power, damage, and repair are modelled
- Tooling input must be clearly separated from gameplay input
- Overlay mode (F12/dev) must be deterministic and clean; cannot corrupt gameplay control state

### AI Rules

- AtlasAI must be workspace-aware and follow repo conventions
- AI suggestions must be **previewable before apply** — no blind overwrites
- AI operates through safe patch/delta systems
- AtlasAI is a project "arbiter" governing code quality, not just a chatbot

### Data Rules

- Data-driven wherever possible
- JSON/spec-driven formats for gameplay systems
- Versioned data schemas with migration paths
- Asset metadata and procedural metadata are first-class
- Save formats and generation seeds must be structured and inspectable

### Repo Rules

- Existing legacy repos are imported, audited, stripped, renamed, and normalised
- Legacy naming conflicts must be removed
- Documentation must be rewritten to MasterRepo standards
- Docs/Archive/ holds planning artefacts only; active docs live in Docs/

---

## 4. What Each Legacy Repo Becomes

| Legacy Repo | Contribution Role |
|---|---|
| **Atlas** | Engine/editor/tooling architecture, custom GUI direction, editor framework concepts |
| **NovaForge** | Gameplay systems, survival/resource loops, ship/station/interior concepts, progression, faction/season/titan design |
| **Arbiter / ArbiterAI** | AI orchestration, workspace indexing, repo awareness, patch generation, planning mode, assistant UX |
| **Pioneer / builder repos** | Ship builder logic, snapping systems, modular construction, assembly UI, part hierarchy |
| **All other archived repos** | Donor archives — feature mines, patterns to salvage, code to normalise |

---

## 5. Target Structure

The canonical directory layout established for MasterRepo:

```
MasterRepo/
  Atlas/                     # Engine, editor, runtime foundations
    Engine/                  # Core, ECS, rendering, physics, audio, input …
    Editor/                  # Editor shell, panels, tools, gizmos …
    Runtime/                 # Runtime bootstrap, lifecycle
    UI/                      # Custom UI framework
    Config/                  # Engine/editor config schemas
    CMake/
  NovaForge/                 # Game project
    Gameplay/                # All gameplay systems
    World/                   # World streaming, map, environment
    Save/                    # Save/load
    UI/                      # Game HUD and menus
    App/                     # Bootstrap, orchestration, main entry point
    Data/                    # Data definitions and tables
    Server/                  # Dedicated server target
    Client/                  # Client-specific app entry
  AtlasAI/                   # AI tooling shell
    AIEngine/                # Python AI engine core
    HostApp/                 # C# WPF host application
    VisualStudioExtension/   # VSIX integration
    ProjectAdapters/         # Per-project adapters
    WebhookIntegration/      # TypeScript webhook relay
  Shared/                    # Bridge contracts, protocol types only
    AtlasBridgeContract/
    ToolProtocol/
  Docs/                      # All active documentation
    Architecture/
    Design/
    Integration/
    Roadmaps/
    ExpectedResults/
    Archive/                 # Archived planning artefacts and chat exports
  Scripts/                   # Build, run, validate, CI scripts
  Tests/                     # Integration and cross-system tests
  Services/                  # Optional backend services
  ThirdParty/                # Third-party libraries
```

---

## 6. Executable / Launch Strategy

The primary goal of all engine and tooling work is to produce a **bootable executable** that exercises all systems in an integrated vertical slice. See [Docs/LAUNCHING.md](../LAUNCHING.md) for build and launch instructions.

The boot sequence is:

1. `LaunchConfig` parsed from CLI args / config file
2. `RuntimeBootstrap::Initialize(mode)` — loads core engine systems
3. `GameSystemsRegistry` registers all gameplay subsystems
4. `WorldBootstrap::RunAll()` — phases through config → data → world → UI → editor
5. Engine main loop (`Engine::Run()`)
6. Graceful shutdown

Modes supported:

| Mode | Description |
|---|---|
| `editor` | Full Atlas editor shell with all panels and AtlasAI integration |
| `game` | NovaForge game client, HUD active, no editor panels |
| `server` | NovaForge headless dedicated server |
| `playtest` | Automated `PlaytestSession` smoke-test run (headless, returns exit code) |

---

## 7. Implementation Status

See the live roadmap at [Docs/Roadmaps/roadmap.md](../Roadmaps/roadmap.md) for current phase status.

Key milestones:

| Milestone | Status |
|---|---|
| Epics 1–10: Monorepo foundation, bridge backbone, AtlasAI rename | ✅ Complete |
| Zip file migration (all 7 source zips) | ✅ Complete |
| G/H/I series: Physics, Audio, Networking, Scripting, Season, Anomaly, WarSector | ✅ Complete |
| J series: GameplayConnector, ContractReward, Keybind, SaveLoad, AssetImport, PCGDeterminism, MarketBridge, Schema | ✅ Complete |
| K series: LaunchConfig, GameSystemsRegistry, PlaytestSession, RuntimeDiagnostics, EditorLaunchBridge, TestHarness | ✅ Complete |
| Phase 11–15: CMake wiring, client/server integration, live AI, CI hardening, character hookup | 🔄 In progress |

---

*This document supersedes all individual planning chat exports in `Docs/Archive/Chats/`.*
