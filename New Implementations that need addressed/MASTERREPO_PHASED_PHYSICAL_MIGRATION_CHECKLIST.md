# MASTERREPO_PHASED_PHYSICAL_MIGRATION_CHECKLIST.md

## Purpose

This checklist turns the consolidation plans into a **real execution sequence** for physically migrating code, docs, modules, and workflows into **MasterRepo**.

It assumes:

- **MasterRepo** is the destination repo
- **Arbiter** is being renamed to **AtlasAI**
- **ArbiterAI** is being renamed to **AtlasAI.Core**
- **NovaForge** is being merged as the main gameplay/content donor
- **WPF** is the desktop tooling shell
- **Atlas** native systems remain the engine/runtime/editor backend

This is a **phased, low-risk migration order**, not a giant one-shot merge.

---

# 1. Migration Principles

## 1.1 Core rules

- Do **not** merge all repos at once.
- Do **not** do blind folder copy/paste integration.
- Do **not** rename everything in one pass.
- Move **structure first**, then **contracts**, then **services**, then **tooling**, then **game systems**.
- Keep the repo building as often as possible.
- Preserve docs and donor repo history wherever practical.

## 1.2 Success criteria

By the end of migration:

- MasterRepo has the final folder/module structure
- AtlasAI replaces Arbiter naming
- WPF tooling lives in `Tools/AtlasAI.*`
- services and bridge layers are in place
- donor systems are absorbed into the correct ownership zones
- dependency boundaries are preserved
- duplicate/obsolete code is retired cleanly

---

# 2. Pre-Migration Snapshot Phase

## Phase 0 — Freeze and inventory

### Goal
Capture the current state before physical moves begin.

### Checklist
- [ ] Create a fresh backup/archive of all current zip contents
- [ ] Extract all donor repos into a temporary comparison workspace
- [ ] Create a simple inventory spreadsheet or markdown list of:
  - [ ] repo names
  - [ ] major modules
  - [ ] build systems
  - [ ] docs/design files
  - [ ] tooling apps
  - [ ] services
  - [ ] config files
- [ ] Mark each major module as:
  - [ ] keep
  - [ ] refactor
  - [ ] merge
  - [ ] replace
  - [ ] archive
- [ ] Preserve original donor repo names in migration notes for traceability
- [ ] Save a clean copy of all generated planning docs into `/Docs/Migration`

### Deliverable
A full migration inventory and backup snapshot.

---

# 3. Repo Skeleton Phase

## Phase 1 — Create final destination skeleton

### Goal
Create the final folder structure in MasterRepo before moving code.

### Checklist
- [ ] Create top-level folders:
  - [ ] `/Engine`
  - [ ] `/Game`
  - [ ] `/AI`
  - [ ] `/Tools`
  - [ ] `/Services`
  - [ ] `/Shared`
  - [ ] `/Content`
  - [ ] `/Data`
  - [ ] `/Config`
  - [ ] `/Scripts`
  - [ ] `/Docs`
  - [ ] `/Tests`
  - [ ] `/ThirdParty`
  - [ ] `/Build`
  - [ ] `/Deploy`
  - [ ] `/Archive`
- [ ] Create initial subfolders from the post-consolidation layout
- [ ] Add placeholder README files in each major directory
- [ ] Add ownership notes to each major folder
- [ ] Add a root architecture README describing the layer model

### Deliverable
MasterRepo has the final skeleton, even if most folders are still mostly empty.

---

# 4. Docs-First Migration Phase

## Phase 2 — Move and normalize documentation first

### Goal
Get planning, design, and architecture docs consolidated before code moves.

### Checklist
- [ ] Create doc categories:
  - [ ] `/Docs/Architecture`
  - [ ] `/Docs/Design`
  - [ ] `/Docs/Roadmaps`
  - [ ] `/Docs/Migration`
  - [ ] `/Docs/Bridge`
  - [ ] `/Docs/Implementation`
  - [ ] `/Docs/Standards`
  - [ ] `/Docs/Subsystems`
- [ ] Move generated consolidation docs into their final locations
- [ ] Move relevant NovaForge design docs into `/Docs/Design`
- [ ] Move donor repo implementation notes into `/Docs/Migration`
- [ ] Rename old Arbiter references in docs to AtlasAI where appropriate
- [ ] Keep an archive copy of original donor docs in `/Archive` if needed
- [ ] Add a `DOC_INDEX.md` linking the important documents
- [ ] Mark outdated docs as `ARCHIVED` instead of deleting immediately

### Deliverable
One centralized documentation system inside MasterRepo.

---

# 5. Naming and Identity Phase

## Phase 3 — Soft rename Arbiter to AtlasAI

### Goal
Lock the new naming system before major code moves.

### Checklist
- [ ] Rename documentation references:
  - [ ] Arbiter → AtlasAI
  - [ ] ArbiterAI → AtlasAI.Core
- [ ] Define final namespace prefix rules:
  - [ ] `Atlas*`
  - [ ] `AtlasAI*`
  - [ ] `NovaForge*`
- [ ] Rename solution and project names in the planning docs
- [ ] Rename UI-facing labels and branding in donor WPF tooling plans
- [ ] Create a rename map markdown file if not already present
- [ ] Delay deep namespace/file rename in code until the project lands in its final ownership area

### Deliverable
Naming is standardized in plans and migration targets before code churn starts.

---

# 6. Shared Boundary Phase

## Phase 4 — Establish Shared contracts and protocols

### Goal
Create the cross-boundary core before moving live tooling and services.

### Checklist
- [ ] Create `/Shared/Contracts`
- [ ] Create `/Shared/Schemas`
- [ ] Create `/Shared/Protocols`
- [ ] Create `/Shared/Generated`
- [ ] Create `/Shared/Interop`
- [ ] Add the first version of:
  - [ ] command envelopes
  - [ ] event envelopes
  - [ ] error model
  - [ ] handshake/versioning schema
  - [ ] session model
- [ ] Add bridge DTOs for:
  - [ ] build commands
  - [ ] log events
  - [ ] asset operations
  - [ ] simulation queries
  - [ ] editor commands
  - [ ] AI task commands
- [ ] Ensure these modules stay free of WPF/UI code
- [ ] Add validation tests for schema versioning

### Deliverable
A stable contract layer that the rest of the system can build against.

---

# 7. Service Layer Phase

## Phase 5 — Stand up Services before UI migration

### Goal
Make services the stable execution surface before WPF panels arrive.

### Checklist
- [ ] Create:
  - [ ] `/Services/AtlasBuildService`
  - [ ] `/Services/AtlasAssetService`
  - [ ] `/Services/AtlasWorldService`
  - [ ] `/Services/AtlasSimulationService`
  - [ ] `/Services/AtlasEditorService`
  - [ ] `/Services/AtlasTelemetryService`
  - [ ] `/Services/AtlasSessionService`
  - [ ] `/Services/AtlasAI.ServiceHost`
- [ ] Define minimal startup/lifecycle for each service
- [ ] Implement basic health check endpoint or equivalent status probe
- [ ] Implement logging and structured error output
- [ ] Connect each service to shared contracts
- [ ] Create a local service startup script
- [ ] Add integration test harness for service boot

### MVP targets
- [ ] Build service can launch compile/test commands
- [ ] Telemetry service can stream logs/events
- [ ] Editor service can accept simple editor command requests
- [ ] AI service host can accept a simple task request
- [ ] Session service can track the active workspace/project

### Deliverable
Service surfaces exist before the desktop shell tries to consume them.

---

# 8. Native Atlas Alignment Phase

## Phase 6 — Reorganize native engine/backend ownership inside MasterRepo

### Goal
Normalize the native side before game and WPF donor features are merged deeply.

### Checklist
- [ ] Reorganize existing native code into:
  - [ ] `/Engine/AtlasCore`
  - [ ] `/Engine/AtlasRuntime`
  - [ ] `/Engine/AtlasRenderer`
  - [ ] `/Engine/AtlasPhysics`
  - [ ] `/Engine/AtlasAudio`
  - [ ] `/Engine/AtlasInput`
  - [ ] `/Engine/AtlasNetworking`
  - [ ] `/Engine/AtlasSimulation`
  - [ ] `/Engine/AtlasVoxel`
  - [ ] `/Engine/AtlasWorld`
  - [ ] `/Engine/AtlasAssets`
  - [ ] `/Engine/AtlasScripting`
  - [ ] `/Engine/AtlasEditorBackend`
  - [ ] `/Engine/AtlasToolsRuntime`
  - [ ] `/Engine/AtlasPlatform`
- [ ] Move only the files already owned by native runtime/backend layers
- [ ] Avoid moving NovaForge-specific gameplay logic into Engine
- [ ] Add folder-level readmes describing ownership
- [ ] Verify include paths after each major move
- [ ] Fix build errors module by module, not globally all at once

### Deliverable
Atlas native code has a coherent engine/editor/runtime backend structure.

---

# 9. WPF Tooling Shell Phase

## Phase 7 — Move Arbiter WPF concepts into AtlasAI.Tools shell

### Goal
Stand up the desktop shell in its final location.

### Checklist
- [ ] Create:
  - [ ] `/Tools/AtlasAI.WpfHost`
  - [ ] `/Tools/AtlasAI.Shell`
  - [ ] `/Tools/AtlasAI.Panels`
  - [ ] `/Tools/AtlasAI.Workspace`
  - [ ] `/Tools/AtlasAI.ProjectExplorer`
  - [ ] `/Tools/AtlasAI.Chat`
  - [ ] `/Tools/AtlasAI.ArchiveUI`
  - [ ] `/Tools/AtlasAI.BuildUI`
  - [ ] `/Tools/AtlasAI.LogsUI`
  - [ ] `/Tools/AtlasAI.AssetUI`
  - [ ] `/Tools/AtlasAI.DesignUI`
  - [ ] `/Tools/AtlasAI.SettingsUI`
  - [ ] `/Tools/AtlasAI.VisualStudio`
  - [ ] `/Tools/AtlasAI.BlenderBridge`
  - [ ] `/Tools/AtlasAI.Bridge`
- [ ] Port donor WPF shell code into these destinations
- [ ] Rename UI branding to AtlasAI
- [ ] Keep any donor code that is too tightly coupled in a temporary `Legacy` subfolder during cleanup
- [ ] Wire the shell to services, not direct engine internals
- [ ] Restore basic app startup
- [ ] Restore docking/layout
- [ ] Restore theme system
- [ ] Restore workspace/session persistence

### MVP targets
- [ ] WPF host launches cleanly
- [ ] shell loads
- [ ] a chat panel opens
- [ ] a logs panel can display telemetry stream
- [ ] a build panel can call the build service

### Deliverable
AtlasAI WPF shell exists in MasterRepo and is alive.

---

# 10. AtlasAI Core Migration Phase

## Phase 8 — Move AI/orchestration modules into `/AI`

### Goal
Land AtlasAI core logic into final ownership zones without mixing it into WPF UI.

### Checklist
- [ ] Create:
  - [ ] `/AI/AtlasAI.Core`
  - [ ] `/AI/AtlasAI.Agents`
  - [ ] `/AI/AtlasAI.Planning`
  - [ ] `/AI/AtlasAI.Memory`
  - [ ] `/AI/AtlasAI.Indexing`
  - [ ] `/AI/AtlasAI.Training`
  - [ ] `/AI/AtlasAI.Inference`
  - [ ] `/AI/AtlasAI.Archive`
  - [ ] `/AI/AtlasAI.Codegen`
  - [ ] `/AI/AtlasAI.Design`
  - [ ] `/AI/AtlasAI.Automation`
- [ ] Move ArbiterAI donor code into the correct target areas
- [ ] Strip any UI-specific classes out of non-UI AI modules
- [ ] Replace old names with AtlasAI naming gradually
- [ ] Connect AtlasAI modules to:
  - [ ] Shared contracts
  - [ ] Index service
  - [ ] AI service host
  - [ ] archive systems
- [ ] Add smoke tests for the AI task flow

### Deliverable
AtlasAI exists as a real subsystem family inside MasterRepo, separate from UI.

---

# 11. Bridge Integration Phase

## Phase 9 — Implement the WPF ↔ Atlas bridge

### Goal
Make WPF and native/services communicate through the formal bridge contract.

### Checklist
- [ ] Implement bridge client in `/Tools/AtlasAI.Bridge`
- [ ] Implement service-facing adapters using the shared contracts
- [ ] Wire:
  - [ ] log subscriptions
  - [ ] build commands
  - [ ] asset operations
  - [ ] editor requests
  - [ ] simulation queries
  - [ ] AI task requests
- [ ] Add reconnect handling
- [ ] Add session handshake/version checks
- [ ] Add bridge integration tests
- [ ] Add failure-mode behavior in UI for offline services

### Deliverable
WPF no longer needs direct coupling to engine internals to function.

---

# 12. NovaForge Gameplay Migration Phase

## Phase 10 — Move game systems into `/Game/NovaForge`

### Goal
Bring in gameplay/content logic after engine/services/tooling boundaries are already defined.

### Checklist
- [ ] Create `/Game/NovaForge`
- [ ] Add subfolders:
  - [ ] `/Core`
  - [ ] `/Gameplay`
  - [ ] `/Economy`
  - [ ] `/Factions`
  - [ ] `/Missions`
  - [ ] `/Ships`
  - [ ] `/Stations`
  - [ ] `/Interiors`
  - [ ] `/Characters`
  - [ ] `/Combat`
  - [ ] `/Mining`
  - [ ] `/Exploration`
  - [ ] `/Construction`
  - [ ] `/PCG`
  - [ ] `/UIRuntime`
  - [ ] `/Server`
- [ ] Move NovaForge modules subsystem by subsystem
- [ ] Keep in-game runtime UI isolated in `UIRuntime`
- [ ] Move only reusable backend pieces into `/Engine` if they truly belong there
- [ ] Move content definitions into `/Content`
- [ ] Move data tables and tuning into `/Data`
- [ ] Update build files for each migrated subsystem
- [ ] Validate dependency rules after each subsystem lands

### Recommended subsystem order
1. [ ] Core
2. [ ] Gameplay
3. [ ] Ships
4. [ ] Stations
5. [ ] Interiors
6. [ ] Factions
7. [ ] Economy
8. [ ] Missions
9. [ ] Mining
10. [ ] Exploration
11. [ ] Construction
12. [ ] Combat
13. [ ] PCG
14. [ ] Characters
15. [ ] Server
16. [ ] UIRuntime

### Deliverable
NovaForge gameplay is absorbed into MasterRepo under the correct ownership model.

---

# 13. Content and Data Phase

## Phase 11 — Normalize content, data, and configs

### Goal
Separate authored content from code cleanly.

### Checklist
- [ ] Populate `/Content` with:
  - [ ] prefabs
  - [ ] ships
  - [ ] stations
  - [ ] interiors
  - [ ] dialogue
  - [ ] templates
  - [ ] PCG seeds
- [ ] Populate `/Data` with:
  - [ ] factions
  - [ ] balance
  - [ ] resources
  - [ ] progression
  - [ ] loot
  - [ ] crafting
  - [ ] encounters
  - [ ] localization
  - [ ] security
  - [ ] rules
- [ ] Move config files into `/Config`
- [ ] Separate runtime configs, editor configs, server configs, and AI configs
- [ ] Add validation scripts for malformed content/data
- [ ] Ensure code no longer depends on donor repo file layouts

### Deliverable
Content/data/config are no longer scattered across donor layouts.

---

# 14. Build and Solution Phase

## Phase 12 — Normalize solutions, scripts, and build orchestration

### Goal
Make the repo build and launch in a clean, intentional way.

### Checklist
- [ ] Create or normalize:
  - [ ] `AtlasEngine.sln`
  - [ ] `NovaForge.sln`
  - [ ] `AtlasServices.sln`
  - [ ] `AtlasAI.Tools.sln`
  - [ ] `AtlasAI.Services.sln`
- [ ] Move scripts into `/Scripts`
- [ ] Add bootstrap scripts
- [ ] Add build scripts
- [ ] Add migration scripts if needed
- [ ] Add validation scripts
- [ ] Add packaging scripts
- [ ] Add service startup script
- [ ] Add WPF host startup script
- [ ] Add local developer setup doc

### Deliverable
The repo has a sane build/orchestration entry path.

---

# 15. Test and Validation Phase

## Phase 13 — Add confidence checks during migration

### Goal
Prevent silent architectural decay.

### Checklist
- [ ] Create `/Tests/Unit`
- [ ] Create `/Tests/Integration`
- [ ] Create `/Tests/Simulation`
- [ ] Create `/Tests/Bridge`
- [ ] Create `/Tests/Services`
- [ ] Create `/Tests/Assets`
- [ ] Create `/Tests/Game`
- [ ] Create `/Tests/EndToEnd`
- [ ] Add basic smoke tests for:
  - [ ] service startup
  - [ ] WPF shell startup
  - [ ] bridge handshake
  - [ ] log streaming
  - [ ] build request flow
  - [ ] AI task request flow
- [ ] Add dependency audits
- [ ] Add include/reference validation if possible in CI
- [ ] Add a migration-progress checklist to CI or docs

### Deliverable
Migration progress is measurable and guarded.

---

# 16. Cleanup and Retirement Phase

## Phase 14 — Retire duplicates and legacy layout remnants

### Goal
Remove transitional clutter once the final structure is stable.

### Checklist
- [ ] Remove temporary legacy folders after replacement is confirmed
- [ ] Delete duplicate donor modules once new ownership copy is validated
- [ ] Remove obsolete config files
- [ ] Remove dead namespace aliases once safe
- [ ] Remove old Arbiter labels from code/comments/resources
- [ ] Clean obsolete scripts
- [ ] Archive legacy docs that are no longer source of truth
- [ ] Update all readmes to the final naming and folder model

### Deliverable
MasterRepo becomes the only real working repo layout.

---

# 17. Final Hardening Phase

## Phase 15 — Lock architecture and operating rules

### Goal
Prevent the repo from sliding back into entropy after migration.

### Checklist
- [ ] Add per-folder README ownership docs
- [ ] Add dependency rule doc links to root README
- [ ] Add architecture review checklist for new modules
- [ ] Add pull request checklist items:
  - [ ] correct ownership area
  - [ ] dependency rule compliance
  - [ ] no direct WPF → engine internals coupling
  - [ ] no game logic in engine core
  - [ ] no UI logic in AI core modules
- [ ] Add naming standard doc
- [ ] Add code review rules for layer violations
- [ ] Add “where should this file live?” guidance doc

### Deliverable
The consolidated repo stays clean after the merge.

---

# 18. Recommended Execution Order Summary

## Best order
1. [ ] Phase 0 — inventory and backup
2. [ ] Phase 1 — create repo skeleton
3. [ ] Phase 2 — migrate docs
4. [ ] Phase 3 — soft rename to AtlasAI
5. [ ] Phase 4 — establish shared contracts
6. [ ] Phase 5 — stand up services
7. [ ] Phase 6 — align native Atlas modules
8. [ ] Phase 7 — stand up WPF shell
9. [ ] Phase 8 — move AtlasAI core modules
10. [ ] Phase 9 — wire bridge integration
11. [ ] Phase 10 — migrate NovaForge gameplay modules
12. [ ] Phase 11 — normalize content/data/config
13. [ ] Phase 12 — normalize build/solutions/scripts
14. [ ] Phase 13 — add tests and validation
15. [ ] Phase 14 — cleanup legacy duplicates
16. [ ] Phase 15 — harden architecture rules

This is the safest order because it builds the destination structure before heavy subsystem absorption.

---

# 19. High-Risk Areas to Watch Carefully

## Watch list
- [ ] accidental direct WPF references into native engine code
- [ ] NovaForge systems slipping into reusable engine modules
- [ ] UI-specific logic leaking into AtlasAI core modules
- [ ] contract drift between bridge, services, and native backends
- [ ] duplicated config/data file formats
- [ ] giant utility modules becoming a dumping ground
- [ ] one-shot rename attempts causing broken builds everywhere
- [ ] temporary legacy folders becoming permanent

---

# 20. Bottom Line

This checklist gives you a **real physical migration path** for turning multiple repos into one coherent platform.

The safest strategy is:

- **structure first**
- **contracts second**
- **services third**
- **tooling fourth**
- **AI/core fifth**
- **game systems after boundaries exist**
- **cleanup last**

That keeps MasterRepo stable while Atlas, AtlasAI, and NovaForge are consolidated into a single long-term architecture.
