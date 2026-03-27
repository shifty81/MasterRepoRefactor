# MASTERREPO_TARGET_TREE_BLUEPRINT

## Purpose
This document defines the **target folder structure** for **MasterRepo** after the Arbiter + NovaForge refactor.
It is intended to be the practical companion to:

- `MASTER_IMPLEMENTATION_CHECKLIST.md`
- `Arbiter_NovaForge_Integration_Plan.md`

The goal is a **single monorepo** with **hard internal boundaries**.

---

# Top-level target layout

```text
MasterRepo/
├── Atlas/
├── NovaForge/
├── Arbiter/
├── Shared/
├── Docs/
├── ThirdParty/
├── Tools/
├── Scripts/
├── Tests/
└── Build/
```

---

# Ownership summary

## Atlas
Owns reusable engine and editor foundations.

## NovaForge
Owns the actual game project and all game-specific systems/content.

## Arbiter
Owns AI tooling, workflow orchestration, workspace shell, archive, automation, and IDE integration.

## Shared
Owns only neutral contracts and shared protocol/manifests.

## Docs
Owns architecture, design, integration, and implementation documents.

## ThirdParty
Owns vendored external dependencies and clearly isolated third-party source.

## Tools
Owns repo-wide developer tools that are not specific to Arbiter or NovaForge.

## Scripts
Owns automation scripts, setup scripts, and build helpers.

## Tests
Owns repo-level integration and system verification.

## Build
Owns generated build output or build orchestration metadata if you choose to keep it in-repo.

---

# Atlas target structure

```text
Atlas/
├── Core/
│   ├── Containers/
│   ├── Memory/
│   ├── Math/
│   ├── IO/
│   ├── Serialization/
│   ├── Config/
│   ├── Logging/
│   ├── Diagnostics/
│   ├── Jobs/
│   └── Platform/
├── Engine/
│   ├── ECS/
│   ├── World/
│   ├── Scene/
│   ├── Assets/
│   ├── Rendering/
│   ├── Physics/
│   ├── Audio/
│   ├── Animation/
│   ├── Networking/
│   ├── Input/
│   └── Scripting/
├── Runtime/
│   ├── AppFramework/
│   ├── GameLoop/
│   ├── Simulation/
│   ├── SaveLoad/
│   └── RuntimeServices/
├── Editor/
│   ├── Framework/
│   ├── Panels/
│   ├── Commands/
│   ├── Selection/
│   ├── Inspectors/
│   ├── SceneTools/
│   ├── AssetTools/
│   └── EditorServices/
├── UI/
│   ├── Core/
│   ├── Layout/
│   ├── Controls/
│   ├── Styling/
│   ├── Rendering/
│   └── Themes/
├── Assets/
├── Config/
└── CMake/
```

## Atlas rules
- Atlas must stay reusable.
- Atlas must not depend on Arbiter.
- Atlas should not contain NovaForge gameplay logic.
- Atlas UI is the native/custom editor UI foundation.

---

# NovaForge target structure

```text
NovaForge/
├── Client/
│   ├── App/
│   ├── Presentation/
│   ├── HUD/
│   ├── Input/
│   └── ClientServices/
├── Server/
│   ├── App/
│   ├── Simulation/
│   ├── Authority/
│   ├── Persistence/
│   └── ServerServices/
├── Gameplay/
│   ├── Factions/
│   ├── Economy/
│   ├── Mining/
│   ├── Combat/
│   ├── Builder/
│   ├── PCG/
│   ├── Exploration/
│   ├── Missions/
│   ├── Progression/
│   └── PlayerSystems/
├── World/
│   ├── Galaxy/
│   ├── Sectors/
│   ├── Planets/
│   ├── Stations/
│   ├── Ships/
│   └── Encounters/
├── Data/
│   ├── Config/
│   ├── Definitions/
│   ├── Tables/
│   ├── Recipes/
│   ├── Modules/
│   ├── Parts/
│   ├── Factions/
│   └── Validation/
├── Content/
│   ├── Prefabs/
│   ├── Scenes/
│   ├── UI/
│   ├── Audio/
│   ├── Materials/
│   └── VFX/
├── Tools/
│   ├── Importers/
│   ├── Validators/
│   ├── Authoring/
│   └── Generators/
├── Integrations/
│   └── Arbiter/
│       ├── include/
│       ├── src/
│       ├── Config/
│       └── Logs/
├── App/
│   ├── NovaForgeApp/
│   ├── Bootstrap/
│   ├── Session/
│   └── ProjectContext/
├── Tests/
├── Docs/
└── CMake/
```

## NovaForge rules
- NovaForge owns all project-specific gameplay and content.
- Arbiter-facing code must live under `NovaForge/Integrations/Arbiter/`.
- NovaForge must not depend on Arbiter host UI/chat/archive internals.
- Shipping builds must work without Arbiter.

---

# Arbiter target structure

```text
Arbiter/
├── HostApp/
│   ├── Shell/
│   ├── Workspace/
│   ├── Chat/
│   ├── Logs/
│   ├── Build/
│   ├── FileExplorer/
│   ├── Actions/
│   ├── Notifications/
│   ├── Theming/
│   └── DocumentViewer/
├── AIEngine/
│   ├── Core/
│   ├── Models/
│   ├── Providers/
│   ├── Tools/
│   ├── Memory/
│   ├── Sessions/
│   ├── Planning/
│   └── Orchestration/
├── ProjectAdapters/
│   └── NovaForge/
│       ├── Manifest/
│       ├── Bridge/
│       ├── ToolCatalog/
│       ├── BuildMapping/
│       └── SearchRoots/
├── Archive/
│   ├── Ingestion/
│   ├── Indexing/
│   ├── Retrieval/
│   └── Storage/
├── Automation/
│   ├── Workflows/
│   ├── Jobs/
│   ├── Triggers/
│   └── Audit/
├── VisualStudioExtension/
│   ├── ToolWindow/
│   ├── Commands/
│   ├── InlineAssist/
│   └── ProjectBridge/
├── Tests/
└── Config/
```

## Arbiter rules
- Arbiter shell modules should stay generic.
- NovaForge-specific logic belongs in `ProjectAdapters/NovaForge/`.
- Arbiter may use project manifests and bridge contracts, but should not own gameplay code.
- The Visual Studio extension should prefer project-adapter-driven behavior.

---

# Shared target structure

```text
Shared/
├── ArbiterBridgeContract/
│   ├── include/
│   ├── docs/
│   └── schemas/
├── ProjectManifests/
│   ├── novaforge.project.json
│   └── README.md
├── ToolProtocol/
│   ├── docs/
│   ├── schemas/
│   └── README.md
├── BuildMetadata/
└── Conventions/
```

## Shared rules
- Shared must remain small and stable.
- Shared may contain contracts, schemas, manifests, conventions, and protocol docs.
- Shared must not become a dumping ground for gameplay, editor logic, or Arbiter shell code.

---

# Docs target structure

```text
Docs/
├── Architecture/
│   ├── repo_boundaries.md
│   ├── monorepo_layout.md
│   ├── dependency_rules.md
│   └── shipping_separation.md
├── Integration/
│   ├── arbiter_bridge.md
│   ├── project_manifest_spec.md
│   └── tool_protocol.md
├── NovaForge/
│   ├── gameplay/
│   ├── world/
│   ├── builder/
│   ├── factions/
│   └── data/
├── Arbiter/
│   ├── hostapp/
│   ├── ai_engine/
│   ├── adapters/
│   └── automation/
├── Atlas/
│   ├── editor/
│   ├── ui/
│   ├── rendering/
│   └── runtime/
└── Roadmaps/
```

---

# Repo-wide support structure

```text
ThirdParty/
├── README.md
└── VendorPackages/

Tools/
├── RepoTools/
├── DataTools/
├── ValidationTools/
└── DevUtilities/

Scripts/
├── Setup/
├── Build/
├── Validate/
├── Bootstrap/
└── CI/

Tests/
├── Integration/
├── Functional/
├── BuildVerification/
└── Tooling/

Build/
├── Generated/
├── Artifacts/
└── Logs/
```

---

# Initial bridge file placement

These are the first files that should exist in the target structure.

```text
Shared/
└── ProjectManifests/
    └── novaforge.project.json

Shared/
└── ArbiterBridgeContract/
    └── include/
        └── ArbiterBridgeTypes.h

NovaForge/
└── Integrations/
    └── Arbiter/
        ├── include/
        │   └── ArbiterBridgeService.h
        └── src/
            └── ArbiterBridgeService.cpp

Arbiter/
└── ProjectAdapters/
    └── NovaForge/
        ├── NovaForgeProjectManifest.cs
        └── NovaForgeProjectAdapter.cs
```

---

# Initial module targets to introduce

## Atlas
- `AtlasCore`
- `AtlasEngine`
- `AtlasRuntime`
- `AtlasEditor`
- `AtlasUI`

## NovaForge
- `NovaForgeGameplay`
- `NovaForgeWorld`
- `NovaForgeClient`
- `NovaForgeServer`
- `NovaForgeTools`
- `NovaForgeIntegrationArbiter`

## Arbiter
- `ArbiterHost`
- `ArbiterAIEngine`
- `ArbiterArchive`
- `ArbiterAutomation`
- `ArbiterVSIX`
- `ArbiterProjectAdapterNovaForge`

## Shared
- `ArbiterBridgeContract`

---

# Example dependency direction

```text
Shared ─────────────► Atlas
Shared ─────────────► NovaForge
Shared ─────────────► Arbiter

Atlas ──────────────► NovaForge
Atlas ──────────────X Arbiter

NovaForge ──────────X Arbiter internals
NovaForge ──────────► Shared contracts

Arbiter ────────────► Shared contracts
Arbiter ────────────► ProjectAdapters/NovaForge
Arbiter ────────────► NovaForge only through bridge/protocol
```

Legend:
- `►` = allowed dependency direction
- `X` = forbidden direct dependency

---

# Suggested first migration order

1. Create the new top-level zones.
2. Create `Docs/Architecture/` and `Docs/Integration/`.
3. Create `Shared/ProjectManifests/` and `Shared/ArbiterBridgeContract/`.
4. Move or mirror the starter bridge files into target locations.
5. Split NovaForge app/bootstrap code into `NovaForge/App/`.
6. Split Arbiter project-specific code into `Arbiter/ProjectAdapters/NovaForge/`.
7. Update build targets to reflect the new physical layout.
8. Verify shipping builds remain isolated from Arbiter.

---

# Practical notes

## Keep separate-process thinking
Even though everything lives in one monorepo, Arbiter should still be treated as an external-style tooling process when interacting with NovaForge.

## Keep Shared tiny
If a file feels like “maybe Shared,” it probably belongs elsewhere unless it is a true contract, schema, or protocol artifact.

## Avoid UI overlap
- Arbiter UI = outer workflow shell
- Atlas/NovaForge UI = native editor and runtime UI

## Avoid direct write-first AI actions
Prefer:
- inspect
- propose
- diff
- approve
- apply

---

# Definition of structural success

The target tree is correct when:

- every major subsystem has a clear home
- Atlas stays reusable
- NovaForge stays game-specific
- Arbiter stays tooling-specific
- Shared stays narrow
- build targets map cleanly to ownership zones
- no forbidden dependency direction is required to make the repo work
