# Documentation Index

This index covers all documentation in MasterRepoRefactor.

---

## Design Documents

High-level vision, architecture laws, gameplay design, and system specifications.

| Document | Description |
|----------|-------------|
| [Master Design Document](Design/MASTER_DESIGN_DOCUMENT.md) | The unified project vision — all pillars, systems, gameplay design, implementation order, and canon rules |
| [Missing Systems Addendum](Design/MISSING_SYSTEMS_ADDENDUM.md) | Extension to the canon covering governance, validation, telemetry, and scaling systems |

---

## Architecture

Module boundaries, dependency rules, and repo structure specifications.

| Document | Description |
|----------|-------------|
| [Monorepo Layout](Architecture/monorepo_layout.md) | Top-level folder structure and module targets for Atlas, NovaForge, AtlasAI, and Shared |
| [Repo Boundaries](Architecture/repo_boundaries.md) | Zone ownership, forbidden dependencies, and cross-boundary rules |
| [Dependency Rules](Architecture/dependency_rules.md) | Dependency direction rules, allowed/forbidden module dependencies |
| [Shipping Separation](Architecture/shipping_separation.md) | CMake flags and rules for editor/tooling-free shipping builds |

---

## Integration

Bridge contracts, protocol specifications, and manifest schemas.

| Document | Description |
|----------|-------------|
| [AtlasAI Bridge](Integration/atlasai_bridge.md) | Transport model, request/response protocol, whitelisted tool actions |
| [Project Manifest Spec](Integration/project_manifest_spec.md) | Schema for `novaforge.project.json` — capabilities, build targets, bridge config |
| [Tool Protocol](Integration/tool_protocol.md) | REST/WebSocket endpoint reference and event type reference |

---

## Archive

Original chat sessions and raw directive sources before conversion to design documents.

| File | Description |
|------|-------------|
| [Chats/repodirective2](Archive/Chats/repodirective2) | Raw source chat (directive 1 + addendum + constitution session) |
| [Chats/RepoDirective1.txt](Archive/Chats/RepoDirective1.txt) | Raw source chat (directive 1 session) |

---

## Folder Structure

```
Docs/
├── Design/
│   ├── MASTER_DESIGN_DOCUMENT.md        core vision and canon
│   └── MISSING_SYSTEMS_ADDENDUM.md      governance and scaling additions
├── Architecture/
│   ├── monorepo_layout.md
│   ├── repo_boundaries.md
│   ├── dependency_rules.md
│   └── shipping_separation.md
├── Integration/
│   ├── arbiter_bridge.md
│   ├── project_manifest_spec.md
│   └── tool_protocol.md
├── Roadmaps/                            (planned)
├── Atlas/                               (planned — engine, editor, UI, rendering docs)
├── NovaForge/                           (planned — world, gameplay, faction, builder docs)
├── AtlasAI/                             (planned — AI engine, automation, hostapp docs)
└── Archive/
    └── Chats/                           original source directives
```
