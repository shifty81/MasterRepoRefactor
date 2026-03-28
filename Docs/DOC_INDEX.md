# Documentation Index

> **Purpose:** Central navigation map for all documentation in this repository.  
> For the overall project vision see [`Docs/Design/MASTER_DESIGN_DOCUMENT.md`](Design/MASTER_DESIGN_DOCUMENT.md).  
> For the full implementation task list see [`New Implementations that need addressed/MASTER_IMPLEMENTATION_CHECKLIST.md`](../New%20Implementations%20that%20need%20addressed/MASTER_IMPLEMENTATION_CHECKLIST.md).

---

## Architecture

Foundational rules that govern the structure of the monorepo. These documents are authoritative — all code placement and dependency decisions must comply with them.

| Document | Description |
|---|---|
| [repo_boundaries.md](Architecture/repo_boundaries.md) | Defines each top-level ownership zone (Atlas, NovaForge, Arbiter, Shared, Docs), what each zone owns, and what is explicitly forbidden across zone boundaries. |
| [monorepo_layout.md](Architecture/monorepo_layout.md) | Describes the physical directory layout of the monorepo, including the purpose of every top-level folder and key sub-folders. |
| [dependency_rules.md](Architecture/dependency_rules.md) | Enumerates the hard dependency direction rules: which zones may depend on which, and which dependencies are permanently forbidden. |
| [shipping_separation.md](Architecture/shipping_separation.md) | Documents the rules that prevent AtlasAI tooling code from leaking into shipping client/server builds. Covers editor-only guards and build configuration isolation. |

---

## Integration

Documents that describe how the major components communicate across zone boundaries via the Atlas Bridge.

| Document | Description |
|---|---|
| [atlasai_bridge.md](Integration/atlasai_bridge.md) | End-to-end description of the AtlasAI bridge: transport model (REST + WebSocket), request/response envelopes, session handshake, whitelisted tool actions, and trust/approval rules. |
| [project_manifest_spec.md](Integration/project_manifest_spec.md) | Specification for the project manifest file — the single source of truth for how AtlasAI discovers and connects to a project. |
| [tool_protocol.md](Integration/tool_protocol.md) | Quick-reference for the Tool Protocol JSON message format. Full spec lives in `Shared/ToolProtocol/`. See also the JSON schemas in `Shared/ToolProtocol/schemas/`. |

---

## Design

High-level design vision and canon documents.

| Document | Description |
|---|---|
| [MASTER_DESIGN_DOCUMENT.md](Design/MASTER_DESIGN_DOCUMENT.md) | Authoritative unified design document covering all systems, features, and architecture decisions. All work should be evaluated against this document. |
| [MISSING_SYSTEMS_ADDENDUM.md](Design/MISSING_SYSTEMS_ADDENDUM.md) | Extension to the master design that makes explicit the major systems needed for stability, scalability, and long-term cohesion that were not fully elaborated in the main document. |
| [MASTER_REPO_DIRECTIVE.md](Design/MASTER_REPO_DIRECTIVE.md) | Converted from the original planning chat: unified refactor blueprint — project identity, pillars, non-negotiable rules, target structure, and launch strategy. |

---

## Atlas — Engine & Editor

Docs for Atlas engine subsystems. Each sub-folder will contain module-level documentation as subsystems are documented.

| Sub-folder | Scope |
|---|---|
| [Atlas/editor/](Atlas/editor/) | Atlas editor framework — editor shell, panels, tools, and editor-side integration points. |
| [Atlas/rendering/](Atlas/rendering/) | Rendering subsystem — render pipeline, materials, lighting, and viewport management. |
| [Atlas/runtime/](Atlas/runtime/) | Runtime foundation — core systems, asset loading, world/scene management, and engine lifecycle. |
| [Atlas/ui/](Atlas/ui/) | Custom UI framework — widget system, layout engine, and theme/style management. |

---

## NovaForge — Game Project

Docs for NovaForge game systems. Each sub-folder will contain module-level documentation as subsystems are documented.

| Sub-folder | Scope |
|---|---|
| [NovaForge/builder/](NovaForge/builder/) | Builder system — procedural world building, PCG hooks, and builder entity lifecycle. |
| [NovaForge/data/](NovaForge/data/) | Data layer — data tables, schemas, asset definitions, and data validation. |
| [NovaForge/factions/](NovaForge/factions/) | Faction systems — faction definitions, relationships, and faction-driven gameplay logic. |
| [NovaForge/gameplay/](NovaForge/gameplay/) | Core gameplay systems — game loop, player controller, abilities, and game rules. |
| [NovaForge/world/](NovaForge/world/) | World systems — maps, streaming, world state, and environment configuration. |

---

## Arbiter — AI Tooling Shell

Docs for Arbiter tooling modules. Each sub-folder will contain module-level documentation as modules are documented.

| Sub-folder | Scope |
|---|---|
| [Arbiter/hostapp/](Arbiter/hostapp/) | Host application — WPF shell, workspace loading, window management, and UI composition. |
| [Arbiter/ai_engine/](Arbiter/ai_engine/) | AI engine — prompt handling, context management, response parsing, and AI session lifecycle. |
| [Arbiter/automation/](Arbiter/automation/) | Automation layer — scripted workflows, task runner, and CI/CD integration hooks. |
| [Arbiter/adapters/](Arbiter/adapters/) | Project adapters — NovaForge adapter and the generic adapter interface that bridges Arbiter to any project. |

---

## Archive

| Location | Description |
|---|---|
| [Archive/Chats/](Archive/Chats/) | Raw chat session transcripts used as source material for architecture and design decisions. Superseded by `Docs/Design/MASTER_REPO_DIRECTIVE.md`. |
| [Archive/ZipFiles/](Archive/ZipFiles/) | All migrated source zip archives — fully processed into the live repo tree. Retained for reference. |
| [Archive/Planning/](Archive/Planning/) | Legacy planning documents (checklist, migration sheets, execution plans). Superseded by the live roadmap. |

---

## Launching & Running

| Document | Description |
|---|---|
| [LAUNCHING.md](LAUNCHING.md) | Build instructions, launch flags, boot sequence overview, and playtest / CI smoke-test guide. |

---

## Roadmaps

| Document | Description |
|---|---|
| [Roadmaps/roadmap.md](Roadmaps/roadmap.md) | High-level project roadmap summarising completed epics, current status, near-term goals, and long-term vision. |
