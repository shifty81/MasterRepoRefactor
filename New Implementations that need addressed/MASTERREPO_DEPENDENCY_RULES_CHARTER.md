# MASTERREPO_DEPENDENCY_RULES_CHARTER

## Purpose
This charter defines the **allowed and forbidden dependency directions** inside **MasterRepo**.

It exists to stop architectural drift while Atlas, NovaForge, Arbiter, and Shared are being refactored into a clean monorepo.

This document should be treated as a **hard engineering policy**, not a suggestion.

It is intended to work alongside:

- `MASTER_IMPLEMENTATION_CHECKLIST.md`
- `MASTERREPO_TARGET_TREE_BLUEPRINT.md`
- `MASTERREPO_CMAKE_AND_TARGET_WIRING_PLAN.md`
- `MASTERREPO_MIGRATION_MAPPING_SHEET.md`

---

# Core principle

**Ownership must match dependency direction.**

If a module depends on another module, then the depended-on module must be:
- more foundational,
- more stable,
- less project-specific,
- less tool-shell-specific.

This means:

- reusable foundations sit lower
- project logic sits above foundations
- tooling shells sit outside runtime foundations
- shared contracts stay tiny and neutral

---

# The four ownership zones

## 1. Atlas
Atlas owns:
- reusable engine code
- reusable editor framework
- reusable runtime framework
- custom native UI framework
- renderer, ECS, asset, platform, config, diagnostics, core systems

Atlas must remain reusable across multiple projects.

## 2. NovaForge
NovaForge owns:
- gameplay systems
- game client/server code
- world rules
- factions, economy, builder, PCG, missions, progression
- project-specific tools
- project-specific data/content
- project-specific integration shims

NovaForge is the flagship game project built on Atlas.

## 3. Arbiter
Arbiter owns:
- AI tooling shell
- chat/workspace UX
- archive and memory
- workflow orchestration
- automation jobs
- Visual Studio integration
- project adapters
- external-style control of the project through a safe bridge

Arbiter is not part of shipping runtime gameplay.

## 4. Shared
Shared owns:
- bridge contracts
- schemas
- project manifests
- protocol definitions
- narrow conventions needed by more than one zone

Shared is not an implementation layer.

---

# Allowed dependency matrix

## Summary matrix

| From \ To | Shared | Atlas | NovaForge | Arbiter |
|---|---:|---:|---:|---:|
| Shared | No | No | No | No |
| Atlas | Yes | Internal only | No | No |
| NovaForge | Yes | Yes | Internal only | No |
| Arbiter | Yes | Usually no direct runtime dependency | Through bridge/contracts, not by linking gameplay internals | Internal only |

### Read this carefully
- “Yes” means allowed in principle, still subject to ownership sanity.
- “No” means forbidden as an architectural rule.
- “Internal only” means dependencies within the same ownership zone are allowed when layered correctly.
- Arbiter interacting with NovaForge should happen through bridge/protocol/adapters, not by pulling in gameplay internals directly.

---

# High-level rules by zone

## Rule A — Atlas may depend only on Shared and Atlas
Atlas may:
- depend on `Shared` contracts if truly needed
- depend on other Atlas modules in the approved layering order

Atlas may not:
- depend on NovaForge gameplay/content modules
- depend on Arbiter host/UI/archive/workflow modules
- contain NovaForge semantics
- contain Arbiter shell logic

## Rule B — NovaForge may depend on Atlas and Shared
NovaForge may:
- build on Atlas foundations
- consume Shared contracts/manifests/protocols
- create project-specific integrations under `NovaForge/Integrations/`

NovaForge may not:
- depend on Arbiter host app code
- depend on Arbiter chat, memory, automation, or VS integration internals
- force shipping runtime targets to include tooling-only integrations

## Rule C — Arbiter may depend on Shared and its own adapters
Arbiter may:
- depend on Shared contracts
- load project manifests
- use project adapters
- talk to NovaForge through bridge endpoints or bridge contracts
- use external process boundaries

Arbiter may not:
- become a direct runtime dependency of Atlas
- become a direct shipping dependency of NovaForge client/server
- own gameplay logic
- force engine/editor internals to import WPF/.NET/tool-shell code

## Rule D — Shared must not depend on implementation zones
Shared may not:
- depend on Atlas
- depend on NovaForge
- depend on Arbiter
- contain gameplay logic
- contain editor framework logic
- contain host shell logic

Shared is definitions only.

---

# Include-direction rules

These rules apply to `#include`, source references, module imports, and similar code-level dependency edges.

## Allowed include directions

### Atlas
Allowed:
- `Atlas/* -> Atlas/*` when following internal layering
- `Atlas/* -> Shared/*` only for narrow contract use

Forbidden:
- `Atlas/* -> NovaForge/*`
- `Atlas/* -> Arbiter/*`

### NovaForge
Allowed:
- `NovaForge/* -> Atlas/*`
- `NovaForge/* -> Shared/*`
- `NovaForge/* -> NovaForge/*` when following internal layering

Forbidden:
- `NovaForge/* -> Arbiter/*`

### Arbiter
Allowed:
- `Arbiter/* -> Shared/*`
- `Arbiter/* -> Arbiter/*`
- bridge/protocol interaction with NovaForge through contract-facing types

Forbidden:
- `Arbiter/*` should not require native gameplay source includes from `NovaForge/*` as a normal pattern
- `Arbiter/* -> Atlas/*` should be avoided unless there is a very narrow, clearly justified native helper dependency

### Shared
Allowed:
- internal Shared references only

Forbidden:
- `Shared/* -> Atlas/*`
- `Shared/* -> NovaForge/*`
- `Shared/* -> Arbiter/*`

---

# Link-direction rules

These rules apply to CMake target linkage, native libraries, assemblies, and build references.

## Allowed target linkage

### Atlas
Allowed:
- Atlas targets linking other lower/foundation Atlas targets
- Atlas targets linking `ArbiterBridgeContract` only if truly necessary

Forbidden:
- `Atlas* -> NovaForge*`
- `Atlas* -> ArbiterHost`
- `Atlas* -> ArbiterAIEngine`
- `Atlas* -> ArbiterArchive`
- `Atlas* -> ArbiterAutomation`

### NovaForge
Allowed:
- `NovaForge* -> Atlas*`
- `NovaForge* -> ArbiterBridgeContract`
- `NovaForgeTools -> AtlasEditor`
- `NovaForgeIntegrationArbiter -> ArbiterBridgeContract`
- optional editor-only linkage to project tooling modules

Forbidden:
- `NovaForgeClient -> Arbiter*`
- `NovaForgeServer -> Arbiter*`
- `NovaForgeGameplay -> Arbiter*`
- `NovaForgeWorld -> Arbiter*`

### Arbiter
Allowed:
- `ArbiterProjectAdapterNovaForge -> Shared contracts`
- convenience or external process interaction with NovaForge
- build orchestration via shell commands or bridge endpoints

Forbidden:
- direct hard link from Arbiter shell assemblies to NovaForge gameplay internals as a normal design
- direct hard dependency that makes shipping game builds require Arbiter

### Shared
Allowed:
- no outward implementation linkage

Forbidden:
- linking Shared to any implementation zone

---

# Internal layering rules within each zone

## Atlas internal layering
Recommended order:

```text
AtlasCore
AtlasUI -> AtlasCore
AtlasEngine -> AtlasCore
AtlasRuntime -> AtlasCore + AtlasEngine
AtlasEditor -> AtlasCore + AtlasUI + AtlasEngine + AtlasRuntime
```

Rules:
- `AtlasCore` should be the lowest layer.
- `AtlasEditor` may sit at the highest Atlas layer.
- lower Atlas layers must not depend on higher Atlas layers.
- engine/runtime code must not depend on editor-only modules unless explicitly editor-gated.

## NovaForge internal layering
Recommended order:

```text
NovaForgeGameplay
NovaForgeWorld -> NovaForgeGameplay
NovaForgeTools -> NovaForgeGameplay + NovaForgeWorld + AtlasEditor
NovaForgeIntegrationArbiter -> NovaForgeTools + ArbiterBridgeContract + AtlasEditor
NovaForgeClient -> NovaForgeGameplay + NovaForgeWorld + AtlasRuntime
NovaForgeServer -> NovaForgeGameplay + NovaForgeWorld + AtlasRuntime
```

Rules:
- gameplay/world are the project runtime base
- tools sit above project runtime and editor foundations
- Arbiter integration sits above tools and bridge contracts
- client/server must not require project tooling integration

## Arbiter internal layering
Suggested order:

```text
ArbiterAIEngine.Core
ArbiterAIEngine.Providers
ArbiterAIEngine.Tools
ArbiterArchive
ArbiterAutomation
ArbiterProjectAdapters
ArbiterHostApp
ArbiterVSIX
```

Rules:
- providers/tools/planning should stay below shell UX
- project adapters should not absorb shell responsibilities
- VS integration should sit near the edge, not at the foundation

## Shared internal layering
Suggested order:

```text
ProjectManifests
BridgeContract
ToolProtocol
Conventions
```

Rules:
- keep all of Shared definition-only
- avoid helper implementations unless absolutely necessary
- do not allow Shared to become a utility dumping ground

---

# Explicit forbidden dependencies

These are the ones most likely to creep in and must be rejected.

## Forbidden category 1 — Engine to game
- `Atlas/Core -> NovaForge/*`
- `Atlas/Engine -> NovaForge/*`
- `Atlas/Runtime -> NovaForge/*`
- `Atlas/UI -> NovaForge/*`
- `Atlas/Editor -> NovaForge/*` unless through generic plugin/project-loading mechanisms, not direct project coupling

## Forbidden category 2 — Game to tooling shell
- `NovaForge/Gameplay -> Arbiter/*`
- `NovaForge/World -> Arbiter/*`
- `NovaForge/Client -> Arbiter/*`
- `NovaForge/Server -> Arbiter/*`

## Forbidden category 3 — Tooling shell to runtime internals as core design
- `Arbiter/HostApp` directly linking native gameplay modules as a normal integration path
- `Arbiter/Automation` directly embedding game runtime logic
- `Arbiter/Archive` depending on Atlas editor internals

## Forbidden category 4 — Shared becoming implementation soup
- putting builder runtime code in Shared
- putting WPF/.NET adapter logic in Shared
- putting gameplay enums/data tables in Shared
- putting editor framework helper implementations in Shared

## Forbidden category 5 — Shipping leakage
- `NovaForgeClient` linking `NovaForgeIntegrationArbiter`
- `NovaForgeServer` linking `NovaForgeIntegrationArbiter`
- shipping build configs enabling Arbiter integration by default
- runtime packaging containing Arbiter host binaries unless intentionally packaged as separate dev tooling

---

# Allowed bridge patterns

The architecture still needs communication. These patterns are allowed and preferred.

## Pattern 1 — Shared contract + separate process
- Shared defines request/response types
- NovaForge exposes safe local bridge endpoints
- Arbiter calls those endpoints
- no direct host-shell dependency leaks into runtime

This is the preferred model.

## Pattern 2 — Editor-only integration shim
- `NovaForge/Integrations/Arbiter` compiles only in editor/dev builds
- it links to `ArbiterBridgeContract`
- it exposes safe query/action endpoints internally
- it does not leak into shipping client/server

This is also allowed.

## Pattern 3 — Project manifest activation
- Arbiter loads `Shared/ProjectManifests/novaforge.project.json`
- project adapter decides how to communicate with NovaForge
- no direct gameplay import is needed

This is strongly recommended.

---

# Rules for code reviews and PRs

Any PR affecting architecture should be checked against this charter.

## A PR must be blocked if it:
- introduces a forbidden dependency edge
- adds Arbiter shell code into Atlas or NovaForge runtime layers
- adds NovaForge gameplay assumptions into Atlas
- places non-contract implementation code into Shared
- links shipping targets against editor/tooling integration
- makes a lower-level module depend on a higher-level module

## A PR is acceptable if it:
- moves code toward its rightful ownership zone
- reduces coupling between zones
- replaces direct coupling with bridge/protocol contracts
- improves shipping/editor separation
- simplifies the target graph without violating ownership

---

# Dependency exceptions policy

Exceptions should be rare.

## An exception is allowed only if:
1. the dependency is temporary,
2. the reason is documented,
3. a removal plan exists,
4. it does not contaminate shipping runtime builds,
5. it does not break the core ownership model.

## Required documentation for an exception
Every exception must include:
- what depends on what
- why it is temporary
- what the exit/refactor plan is
- which milestone removes it

Document exceptions in:
- `Docs/Architecture/dependency_exceptions.md`

---

# Enforcement suggestions

## Build-time enforcement
- keep target graph narrow in CMake
- do not expose broad include directories unnecessarily
- use compile definitions to gate editor/dev-only code
- add CI checks for forbidden target link edges

## Review-time enforcement
- require ownership-zone labels in PRs
- require dependency justification for cross-zone changes
- review includes and target linkage, not just behavior

## Repo structure enforcement
- prefer directories that reveal ownership
- avoid ambiguous catch-all folders
- do not add new top-level zones casually

---

# Quick decision guide

When adding a new file, ask:

## Question 1
Is this reusable across multiple projects?
- yes → likely `Atlas`
- no → continue

## Question 2
Is this gameplay/content/project-specific?
- yes → `NovaForge`
- no → continue

## Question 3
Is this AI shell/chat/workflow/archive/IDE tooling?
- yes → `Arbiter`
- no → continue

## Question 4
Is this only a contract/schema/manifest?
- yes → `Shared`
- no → it likely needs refactoring before placement

---

# Practical examples

## Good
- `NovaForgeGameplay -> AtlasEngine`
- `NovaForgeIntegrationArbiter -> ArbiterBridgeContract`
- `ArbiterProjectAdapterNovaForge -> Shared/ProjectManifests`
- `AtlasEditor -> AtlasRuntime`

## Bad
- `AtlasEngine -> NovaForgeGameplay`
- `NovaForgeClient -> ArbiterHost`
- `Shared -> NovaForgeWorld`
- `NovaForgeGameplay -> ArbiterAIEngine`
- `AtlasCore -> ArbiterArchive`

---

# Definition of dependency success

Dependency discipline is working when:
- Atlas stays reusable and project-agnostic
- NovaForge stays project-specific without importing tooling shell internals
- Arbiter remains external-style and optional
- Shared stays tiny and neutral
- shipping builds stay free of tooling contamination
- most new code has an obvious home without debate

---

# Final policy statement

**MasterRepo is a monorepo, not a monolith.**

Being in one repository does **not** mean everything may depend on everything else.

The correct model is:

- **Atlas** provides foundations
- **NovaForge** builds the game on those foundations
- **Arbiter** operates as the tooling and orchestration shell
- **Shared** defines the narrow handshake

Any change that weakens that model should be treated as architectural debt and blocked unless explicitly documented as a temporary exception.
