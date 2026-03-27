# MASTERREPO_MIGRATION_MAPPING_SHEET

## Purpose
This document is the **bridge between the current MasterRepo layout and the target monorepo layout**.

Use it to move code in a controlled way, one area at a time, without losing ownership clarity or creating dependency drift.

This file is designed to work alongside:

- `MASTER_IMPLEMENTATION_CHECKLIST.md`
- `MASTERREPO_TARGET_TREE_BLUEPRINT.md`
- `MASTERREPO_CMAKE_AND_TARGET_WIRING_PLAN.md`
- `masterrepo_second_pass_cmake_templates.zip`

---

# How to use this mapping sheet

For each current folder or subsystem:

1. identify what it actually owns
2. decide the new ownership zone
3. move it only if the dependency direction remains valid
4. update include paths / CMake after each move
5. keep the repo building after every migration slice

Use the **Notes / Refactor Required** column aggressively.  
Not everything should be moved as-is.

---

# Ownership rules refresher

## Move to Atlas when it is:
- reusable engine code
- reusable editor framework
- custom UI foundation
- runtime framework
- renderer / asset / ECS / platform systems
- not game-specific

## Move to NovaForge when it is:
- gameplay logic
- game data
- world generation specific to NovaForge
- project-specific tools
- client/server game code
- factions, economy, builder behavior, mission content, recipes, parts

## Move to Arbiter when it is:
- AI tooling shell
- chat/workspace UX
- archive/memory
- automation/workflow logic
- Visual Studio extension
- project adapter logic

## Move to Shared when it is:
- bridge contracts
- protocol schemas
- project manifests
- naming / build conventions
- truly neutral interop artifacts only

---

# Top-level migration map

| Current Area | Current Role | Target Location | Target Module / Target | Move As-Is? | Notes / Refactor Required |
|---|---|---|---|---|---|
| `Core/` | foundational engine systems | `Atlas/Core/` | `AtlasCore` | Usually yes | Move reusable code only. Split out any game-specific helpers. |
| `Engine/` | engine runtime systems | `Atlas/Engine/` | `AtlasEngine` | Usually yes | Keep ECS, rendering, assets, world runtime abstractions here. |
| `Runtime/` | app/runtime services | `Atlas/Runtime/` and `NovaForge/App/` | `AtlasRuntime` / project app modules | Partial | Reusable runtime stays in Atlas. NovaForge startup/bootstrap pieces should move to NovaForge. |
| `UI/` | custom UI framework | `Atlas/UI/` | `AtlasUI` | Yes | Keep generic; do not let gameplay HUD specifics pollute it. |
| `Editor/` | editor framework + project/editor specifics mixed together | `Atlas/Editor/` and `NovaForge/Tools/` | `AtlasEditor` / `NovaForgeTools` | No | Split generic editor framework from project-specific tools and panels. |
| `AI/` | mixed AI systems | `Arbiter/AIEngine/` or remain in `Atlas` only if generic runtime-safe | `ArbiterAIEngine` or none | No | Anything chat/workflow/model/tooling related belongs in Arbiter, not Atlas/NovaForge runtime. |
| `Agents/` | agent orchestration / tools | `Arbiter/AIEngine/Tools/` or `Arbiter/Automation/` | Arbiter-side | No | Treat as tooling/orchestration unless truly runtime gameplay AI. |
| `Builder/` | build/builder systems | `NovaForge/Gameplay/Builder/` and possibly `NovaForge/Tools/` | `NovaForgeGameplay` / `NovaForgeTools` | Partial | Runtime builder logic stays gameplay-side; authoring/editor helpers go to project tools. |
| `PCG/` | procedural generation systems | `NovaForge/Gameplay/PCG/`, `NovaForge/World/`, maybe `NovaForge/Tools/` | `NovaForgeGameplay` / `NovaForgeWorld` | Partial | Split runtime PCG, world generation, and editor preview utilities. |
| `IDE/` | chat panel / dev shell / assistant UI | `Arbiter/HostApp/` | `ArbiterHost` | No | This is tooling-side. Do not leave it inside Atlas/NovaForge runtime graph. |
| `Tools/` | repo-wide or mixed tools | `Tools/`, `Arbiter/`, or `NovaForge/Tools/` | depends | No | Needs audit. Separate repo tools from project tools from AI tools. |
| `Projects/NovaForge/` | game project layer | `NovaForge/` | multiple NovaForge targets | No | This should be the main source for gameplay/content migration. |
| `Config/` | mixed config | `Atlas/Config/`, `NovaForge/Data/Config/`, `Arbiter/Config/`, `Shared/ProjectManifests/` | depends | No | Split by ownership. |
| `Docs/` | mixed docs | `Docs/` | n/a | Partial | Reclassify by architecture, integration, Atlas, NovaForge, Arbiter. |

---

# Detailed current-to-target mapping

## 1. Core

| Current Path | Target Path | Target | Move As-Is? | Notes |
|---|---|---|---|---|
| `Core/Logging` | `Atlas/Core/Logging` | `AtlasCore` | Yes | Good Atlas ownership. |
| `Core/Config` | `Atlas/Core/Config` | `AtlasCore` | Usually | Only generic config. Project manifests should move to `Shared/ProjectManifests` or project config folders. |
| `Core/Serialization` | `Atlas/Core/Serialization` | `AtlasCore` | Yes | Good reusable base. |
| `Core/Diagnostics` | `Atlas/Core/Diagnostics` | `AtlasCore` | Yes | Keep reusable. |
| `Core/Platform` | `Atlas/Core/Platform` | `AtlasCore` | Yes | Good reusable base. |
| `Core/*` with NovaForge-specific assumptions | `NovaForge/App/ProjectContext` or `NovaForge/Data/*` | project-side | No | Remove game-specific leakage from Core. |

## 2. Engine

| Current Path | Target Path | Target | Move As-Is? | Notes |
|---|---|---|---|---|
| `Engine/ECS` | `Atlas/Engine/ECS` | `AtlasEngine` | Yes | Reusable. |
| `Engine/Rendering` | `Atlas/Engine/Rendering` | `AtlasEngine` | Yes | Reusable. |
| `Engine/Assets` | `Atlas/Engine/Assets` | `AtlasEngine` | Yes | Reusable. |
| `Engine/Scene` | `Atlas/Engine/Scene` | `AtlasEngine` | Usually | Keep only generic scene systems. |
| `Engine/Input` | `Atlas/Engine/Input` | `AtlasEngine` | Yes | Reusable. |
| `Engine/*` with game-specific world assumptions | `NovaForge/Gameplay` or `NovaForge/World` | NovaForge targets | No | Strip game semantics out of Atlas. |

## 3. Runtime

| Current Path | Target Path | Target | Move As-Is? | Notes |
|---|---|---|---|---|
| `Runtime/AppFramework` | `Atlas/Runtime/AppFramework` | `AtlasRuntime` | Usually | Keep generic framework only. |
| `Runtime/Simulation` | `Atlas/Runtime/Simulation` | `AtlasRuntime` | Usually | Generic simulation services only. |
| `Runtime/BuilderRuntime/NovaForgeBuilderIntegration.*` | `NovaForge/Integrations/Arbiter/` or `NovaForge/Tools/Builder/` depending purpose | `NovaForgeTools` / integration | No | Strong reusable bridge concept, but it is project-specific and should not stay in generic runtime. |
| `Runtime/*` with NovaForge-specific boot logic | `NovaForge/App/Bootstrap` | project-side | No | Split out into app/session/bootstrap services. |

## 4. UI

| Current Path | Target Path | Target | Move As-Is? | Notes |
|---|---|---|---|---|
| generic custom controls | `Atlas/UI/Controls` | `AtlasUI` | Yes | Good candidate. |
| layout/styling/theming base | `Atlas/UI/Layout`, `Atlas/UI/Styling`, `Atlas/UI/Themes` | `AtlasUI` | Yes | Keep generic. |
| NovaForge HUD widgets | `NovaForge/Client/HUD` or `NovaForge/Content/UI` | project-side | No | Not part of Atlas UI foundation. |
| Arbiter shell UI | `Arbiter/HostApp/*` | Arbiter | No | Keep outside native engine UI. |

## 5. Editor

| Current Path | Target Path | Target | Move As-Is? | Notes |
|---|---|---|---|---|
| generic editor framework | `Atlas/Editor/Framework` | `AtlasEditor` | Yes | Core editor ownership. |
| generic selection / inspectors / commands | `Atlas/Editor/*` | `AtlasEditor` | Usually | Keep only reusable editor systems. |
| NovaForge-specific panels/tools | `NovaForge/Tools/` | `NovaForgeTools` | No | Project tooling belongs with the project. |
| AI chat/editor assistants embedded in editor | `Arbiter/HostApp/` or editor bridge hooks in `NovaForge/Integrations/Arbiter` | Arbiter / integration | No | Separate shell from in-editor bridge. |

## 6. AI / Agents / IDE

| Current Path | Target Path | Target | Move As-Is? | Notes |
|---|---|---|---|---|
| `AI/Arbiter/` | `Arbiter/AIEngine/` or `Arbiter/HostApp/` depending content | Arbiter | No | Split core orchestration from UI shell responsibilities. |
| `AI/OllamaClient/` | `Arbiter/AIEngine/Providers/` | Arbiter | Yes | Good provider-side ownership. |
| `AI/KnowledgeIngestion/` | `Arbiter/Archive/Ingestion/` or `Arbiter/AIEngine/Memory/` | Arbiter | No | Depends on whether it is archive indexing or live memory. |
| `AI/SessionMemory/` | `Arbiter/AIEngine/Memory/` | Arbiter | Yes | Good fit. |
| `Agents/` | `Arbiter/Automation/` and `Arbiter/AIEngine/Tools/` | Arbiter | No | Split tool registry vs automation workflows. |
| `IDE/AIChat` | `Arbiter/HostApp/Chat/` | Arbiter | Yes | Tooling shell. |
| `IDE/NLAssistant` | `Arbiter/HostApp/Chat/` or `Arbiter/AIEngine/Planning/` | Arbiter | No | Split presentation from planning/orchestration. |

## 7. Projects/NovaForge

| Current Path | Target Path | Target | Move As-Is? | Notes |
|---|---|---|---|---|
| `Projects/NovaForge/Assets` | `NovaForge/Content/` | project-side | Usually | Reclassify into UI/audio/materials/prefabs/etc. |
| `Projects/NovaForge/Config` | `NovaForge/Data/Config/` | project-side | Yes | Good fit. |
| `Projects/NovaForge/Data` | `NovaForge/Data/Definitions`, `Tables`, `Validation`, etc. | project-side | No | Split by data type. |
| `Projects/NovaForge/Modules` | `NovaForge/Data/Modules/` or gameplay-side if logic-heavy | project-side | Partial | Separate definitions from runtime code. |
| `Projects/NovaForge/Parts` | `NovaForge/Data/Parts/` | project-side | Yes | Good fit. |
| `Projects/NovaForge/Prefabs` | `NovaForge/Content/Prefabs/` | project-side | Yes | Good fit. |
| `Projects/NovaForge/Recipes` | `NovaForge/Data/Recipes/` | project-side | Yes | Good fit. |
| `Projects/NovaForge/Scenes` | `NovaForge/Content/Scenes/` | project-side | Yes | Good fit. |
| `Projects/NovaForge/Ships` | `NovaForge/World/Ships/` or `NovaForge/Data/Definitions/Ships/` | project-side | Partial | Depends on whether they are data defs or world templates. |
| `Projects/NovaForge/UI` | `NovaForge/Client/HUD/` or `NovaForge/Content/UI/` | project-side | No | Split runtime HUD/UI code from pure UI assets. |
| `Projects/NovaForge/main.cpp` | `NovaForge/App/NovaForgeApp/` + `Bootstrap/` + `Session/` | multiple | No | Must be split. This is one of the highest-value refactors. |

---

# High-priority refactor-before-move areas

These are the places most likely to cause trouble if moved blindly.

## A. `Projects/NovaForge/main.cpp`
### Problem
It likely mixes:
- engine startup
- world init
- player init
- builder init
- input
- HUD
- update loop
- game boot decisions

### Target split
- `NovaForge/App/NovaForgeApp/`
- `NovaForge/App/Bootstrap/`
- `NovaForge/App/Session/`
- `NovaForge/Client/Input/`
- `NovaForge/Client/HUD/`
- `NovaForge/Tools/` where editor-only helper logic belongs

### Migration action
Do not move as one file. Split responsibilities first.

---

## B. `Runtime/BuilderRuntime/NovaForgeBuilderIntegration.*`
### Problem
It sounds reusable at first, but it is actually project-specific glue.

### Target split
- runtime builder behavior → `NovaForge/Gameplay/Builder/`
- editor/builder authoring helpers → `NovaForge/Tools/`
- Arbiter-facing callable hooks → `NovaForge/Integrations/Arbiter/` only if needed for bridge actions

### Migration action
Treat it as a seam, not as a generic runtime layer.

---

## C. `AI/Arbiter`, `IDE/*`, `Agents/*`
### Problem
These often get tangled together as one “AI” zone, but they are not the same thing.

### Target split
- shell/UI → `Arbiter/HostApp/`
- LLM/model/provider logic → `Arbiter/AIEngine/Providers/`
- planning/orchestration → `Arbiter/AIEngine/Planning/`
- memory/archive → `Arbiter/Archive/` and `Arbiter/AIEngine/Memory/`
- project-specific support → `Arbiter/ProjectAdapters/NovaForge/`
- workflow jobs → `Arbiter/Automation/`

### Migration action
Do not move as one block. Reclassify by function.

---

## D. `Editor/`
### Problem
This usually contains both generic editor foundation and project/editor customizations.

### Target split
- generic framework → `Atlas/Editor/`
- NovaForge project tools → `NovaForge/Tools/`
- Arbiter/editor bridge hooks → `NovaForge/Integrations/Arbiter/` or Arbiter-side project adapter if purely external

### Migration action
Audit file-by-file. This is not a safe bulk move.

---

# Migration waves

## Wave 1 — Safe structural moves
These are the easiest and lowest-risk.

- generic `Core/*` → `Atlas/Core/*`
- generic `Engine/*` → `Atlas/Engine/*`
- generic `UI/*` → `Atlas/UI/*`
- data/content folders from `Projects/NovaForge/*` → `NovaForge/Data/*` and `NovaForge/Content/*`
- create `Shared/ProjectManifests/`
- create `Shared/ArbiterBridgeContract/`

## Wave 2 — Split mixed zones
Do these after the target folders exist.

- split `Editor/`
- split `Runtime/*` generic vs project-specific
- split `Tools/` repo-wide vs project-specific vs AI-specific
- split `AI/*` and `Agents/*` into real Arbiter ownership zones

## Wave 3 — App/bootstrap cleanup
- split `Projects/NovaForge/main.cpp`
- create `NovaForge/App/*`
- move startup and project context logic

## Wave 4 — Integration seam
- move bridge contract into `Shared/`
- move bridge service into `NovaForge/Integrations/Arbiter/`
- move project adapter into `Arbiter/ProjectAdapters/NovaForge/`

## Wave 5 — Build cleanup
- map old CMake targets to new module targets
- add guards for editor/tooling/shipping separation
- verify no forbidden dependencies exist

---

# Current folder audit checklist

Use this per folder before moving it.

## Questions to ask
- Is this reusable across projects?
- Is this game-specific?
- Is this tooling-specific?
- Is this just a contract/protocol?
- Does it reference gameplay data types?
- Does it reference editor framework types?
- Does it reference WPF/.NET/VSIX/tooling shells?
- Would shipping client/server still want this?

## Decision guide
- If reusable and native/runtime/editor foundation → `Atlas`
- If game-specific → `NovaForge`
- If AI/workflow/tooling shell → `Arbiter`
- If contract-only → `Shared`

---

# First real file move recommendations

These are the first concrete moves I’d make.

## Move first
1. create `Shared/ProjectManifests/novaforge.project.json`
2. create `Shared/ArbiterBridgeContract/include/ArbiterBridgeTypes.h`
3. move generic `Core/` content into `Atlas/Core/`
4. move generic `Engine/` content into `Atlas/Engine/`
5. move `Projects/NovaForge/Data`, `Parts`, `Recipes`, `Prefabs`, `Scenes` into `NovaForge/`
6. create `NovaForge/Integrations/Arbiter/`
7. create `Arbiter/ProjectAdapters/NovaForge/`

## Do not move yet
- `Projects/NovaForge/main.cpp`
- mixed `Editor/`
- mixed `Runtime/`
- mixed `AI/Arbiter`, `IDE`, `Agents`
- any file that already violates the desired dependency direction

---

# Example mapping decisions

## Example 1
Current file: `Projects/NovaForge/Recipes/laser_mk1.json`  
Target: `NovaForge/Data/Recipes/laser_mk1.json`  
Reason: pure project data definition

## Example 2
Current file: `Runtime/BuilderRuntime/NovaForgeBuilderIntegration.cpp`  
Target: split between `NovaForge/Gameplay/Builder/`, `NovaForge/Tools/`, and `NovaForge/Integrations/Arbiter/`  
Reason: mixed runtime/project/integration responsibilities

## Example 3
Current file: `IDE/AIChat/ChatPanel.*`  
Target: `Arbiter/HostApp/Chat/`  
Reason: tooling shell UI, not engine/game runtime

## Example 4
Current file: `Editor/Selection/ObjectInspector.*`  
Target: `Atlas/Editor/Inspectors/` if generic, otherwise `NovaForge/Tools/Inspectors/`  
Reason: depends on whether it is project-agnostic

---

# Definition of migration success

This mapping process is working when:

- each moved folder has a clear owner
- moved code matches target dependency direction
- game-specific logic steadily leaves Atlas
- tooling-specific logic steadily leaves engine/game modules
- Shared stays extremely small
- the build still works after each migration slice
- no one has to guess where new code should live

---

# Practical summary

The safest migration path is:

1. move the obviously reusable engine pieces into `Atlas`
2. move the obviously game-specific data/content pieces into `NovaForge`
3. create `Shared` early for contracts and manifests
4. split mixed zones instead of bulk-moving them
5. move Arbiter into true tooling ownership zones
6. only then tighten the build graph and bridge layer

This keeps the monorepo becoming cleaner with every pass instead of just changing folder names.
