# Master Repo Missing Systems + Priority Closure Checklist

## Purpose
This checklist converts the current remaining gaps into a practical closure plan, focused on moving from broad scaffolding to a unified, playable, editable project.

---

## Status Key
- **Critical**: blocks real playability or integration
- **High**: strongly needed for productive development
- **Medium**: important, but can follow core closure
- **Later**: valuable after major consolidation

---

# A. Consolidation / Integration Gaps

## A1. Unified source tree and build
**Priority:** Critical

### Missing
- one consolidated repo layout
- one canonical set of runtime types
- one compile path for all subsystems
- duplicate placeholder removal across packs

### Done when
- all current packs are merged into one live repo
- duplicate class/type definitions are resolved
- project compiles from one root

### Closure checklist
- [ ] merge all phase packs into one source tree
- [ ] identify duplicated types and systems
- [ ] choose canonical ownership for each subsystem
- [ ] remove obsolete placeholder duplicates
- [ ] create one main build target

---

## A2. World/bootstrap orchestration
**Priority:** Critical

### Missing
- one authoritative startup flow for:
  - config
  - data loading
  - save loading
  - world generation
  - player spawn
  - UI bootstrap
  - editor/dev state bootstrap

### Done when
- one boot path starts the full vertical slice coherently

### Closure checklist
- [ ] finalize one boot sequence
- [ ] load config before world/runtime init
- [ ] load data registry before gameplay systems
- [ ] choose save vs new-world startup path
- [ ] register UI/debug/editor state in one place
- [ ] make orchestrator the true root owner

---

## A3. Data registry unification
**Priority:** Critical

### Missing
- one authoritative loader model
- unified record model set
- cross-reference validation
- hot reload/writeback plan

### Done when
- every gameplay/editor system reads through one canonical data layer

### Closure checklist
- [ ] unify item/recipe/mission/faction/module/player models
- [ ] centralize ID lookup
- [ ] add missing-reference validation
- [ ] add schema version checks
- [ ] define editor writeback path
- [ ] define hot reload rules

---

# B. Core Playability Gaps

## B1. Real input/context system
**Priority:** Critical

### Missing
- real input binding layer
- game/editor context switching
- mouse capture/release policy
- remapping support
- gameplay action dispatch

### Done when
- runtime and editor can both be controlled reliably without conflicts

### Closure checklist
- [ ] unify gameplay input and editor input contexts
- [ ] implement context switching rules
- [ ] finalize mouse capture/release behavior
- [ ] add remappable keybind config
- [ ] route actions into gameplay systems
- [ ] route editor-only input into editor layer

---

## B2. Real rendering backend / viewport
**Priority:** Critical

### Missing
- actual scene rendering
- voxel chunk rendering
- module rendering
- debug draw
- HUD/editor overlays

### Done when
- user can see live world state, not just logs/scaffolds

### Closure checklist
- [ ] implement viewport rendering shell
- [ ] render voxel chunks
- [ ] render modules/entities
- [ ] render debug overlays
- [ ] render runtime HUD
- [ ] render editor overlays and selection highlights

---

## B3. Save/load implementation
**Priority:** Critical

### Missing
- actual persistence across gameplay/editor systems

### Done when
- a session can be saved and restored accurately

### Closure checklist
- [ ] save/load player state
- [ ] save/load voxel chunks
- [ ] save/load structures/modules
- [ ] save/load contracts/factions/economy
- [ ] save/load fleet/meta/titan/season
- [ ] validate restored world matches expected state

---

## B4. UI framework implementation
**Priority:** Critical

### Missing
- actual working UI layer rather than UI state/controller scaffolds

### Done when
- player and editor workflows can be used through real panels/screens

### Closure checklist
- [ ] implement runtime HUD widgets
- [ ] implement inventory screen
- [ ] implement contract board UI
- [ ] implement station terminal UI
- [ ] implement ship/fleet progression panels
- [ ] implement editor panel docking basics

---

# C. Editor / Tooling Gaps

## C1. Voxel editor workflow
**Priority:** Critical

### Missing
- usable voxel authoring workflow

### Done when
- voxels can be added/removed/painted live and saved

### Closure checklist
- [ ] implement chunk editing
- [ ] implement add/remove/paint tools
- [ ] implement brush shapes
- [ ] mark chunks dirty
- [ ] rebuild mesh after edit
- [ ] persist edits through save/load
- [ ] connect tool UI to editor mode

---

## C2. Outliner + inspector completion
**Priority:** High

### Missing
- deeper object hierarchy
- editable properties
- component/state visibility

### Done when
- selecting any major object gives a useful, editable detail panel

### Closure checklist
- [ ] add hierarchy grouping
- [ ] expose transform editing
- [ ] expose IDs and ownership
- [ ] expose component summary
- [ ] expose module/structure/faction links
- [ ] support edit callbacks into runtime/data

---

## C3. Gizmo + placement completion
**Priority:** High

### Missing
- real transform application
- snapping rules
- module placement preview

### Done when
- world and module editing feels spatial and reliable

### Closure checklist
- [ ] apply move/rotate/scale to selected targets
- [ ] add grid snap
- [ ] add socket snap
- [ ] add local/world toggle behavior
- [ ] add placement preview ghost
- [ ] add validity feedback

---

## C4. PCG editor/debug mode
**Priority:** High

### Missing
- seed controls
- regenerate selected content
- spatial debug for generated content

### Done when
- procedural content can be inspected and controlled directly

### Closure checklist
- [ ] add seed panel
- [ ] add regenerate selected/world buttons
- [ ] visualize spawn points and bounds
- [ ] inspect generation rules in context
- [ ] allow override/lock generated content

---

## C5. Validation toolkit
**Priority:** High

### Missing
- one-click correctness checks

### Done when
- broken references and bad data are caught before runtime

### Closure checklist
- [ ] validate item/recipe references
- [ ] validate loot references
- [ ] validate module/structure references
- [ ] validate config conflicts
- [ ] validate season/server settings
- [ ] expose validation results in WPF + editor

---

## C6. Undo/redo
**Priority:** High

### Missing
- safe editing iteration

### Done when
- edits can be reverted consistently

### Closure checklist
- [ ] define command stack
- [ ] support transform edits
- [ ] support voxel edits
- [ ] support module placement/removal
- [ ] support property edits
- [ ] expose undo/redo commands in UI

---

## C7. Prefab/template authoring
**Priority:** Medium

### Missing
- reusable authored building blocks

### Done when
- rooms/modules/layouts can be saved and reused

### Closure checklist
- [ ] define prefab data shape
- [ ] save prefab from selection
- [ ] load/place prefab
- [ ] categorize prefab library
- [ ] add prefab preview/metadata support

---

# D. Gameplay Loop Hookup Gaps

## D1. Salvage/mining to rewards/inventory
**Priority:** Critical

### Missing
- real payout path into gameplay state

### Done when
- completing actions yields real items/resources visibly

### Closure checklist
- [ ] connect salvage completion to loot table resolution
- [ ] connect mining completion to resource payout
- [ ] add inventory insertion
- [ ] add HUD feedback
- [ ] add mission progress hooks

---

## D2. Station/home-base loop hookup
**Priority:** High

### Missing
- storage, manufacturing, services fully connected to player flow

### Done when
- return-to-station loop feels meaningful

### Closure checklist
- [ ] deposit to storage from inventory
- [ ] withdraw from storage
- [ ] queue manufacturing jobs from recipe data
- [ ] complete jobs into inventory/storage
- [ ] connect repair/resupply terminals
- [ ] connect credits/economy to services

---

## D3. Contracts/progression/economy linkage
**Priority:** High

### Missing
- actions need to drive broader progression

### Done when
- jobs pay out credits, reputation, XP, and unlock better opportunities

### Closure checklist
- [ ] reward credits on contract completion
- [ ] reward faction standing
- [ ] reward skill XP
- [ ] gate better contracts by standing/skill
- [ ] feed trade/market data into contract generation

---

## D4. Fleet/meta/world-sim linkage
**Priority:** Medium

### Missing
- larger systems still need stronger gameplay feedback

### Done when
- fleet and world sim matter in player decisions

### Closure checklist
- [ ] connect contracts to fleet assignments
- [ ] connect fleet roles to income/risk
- [ ] connect war/sectors to opportunity levels
- [ ] connect anomalies to resource/encounter changes
- [ ] connect titan race to long-term pressure

---

# E. AI / Workflow Gaps

## E1. Arbiter editor workflow
**Priority:** High

### Missing
- full AI-assisted review/edit loop

### Done when
- AI suggestions can be reviewed, applied, rejected, and rolled back cleanly

### Closure checklist
- [ ] add diff review panel
- [ ] add file impact preview
- [ ] add accept/reject flow
- [ ] add rollback history
- [ ] connect AI context to selected objects/files
- [ ] expose architecture rule warnings

---

## E2. Documentation/design workflow
**Priority:** Medium

### Missing
- docs integrated tightly with editor/host workflow

### Done when
- design, implementation, and validation are visible in one workspace

### Closure checklist
- [ ] add design doc panel
- [ ] add feature checklist panel
- [ ] add architecture decision log view
- [ ] add link from docs to systems/data where possible

---

# F. Content / Pipeline / QA Gaps

## F1. Asset pipeline standards
**Priority:** High

### Missing
- actual import/content workflow rules

### Done when
- assets can be brought in consistently without repo chaos

### Closure checklist
- [ ] lock naming rules
- [ ] define import destinations
- [ ] define low-poly kit standards
- [ ] define voxel material standards
- [ ] define icon/preview generation rules
- [ ] add import validation checks

---

## F2. Testing and QA tools
**Priority:** High

### Missing
- systemic validation and regression coverage

### Done when
- core loops and data can be checked repeatably

### Closure checklist
- [ ] add data validation tests
- [ ] add save/load smoke tests
- [ ] add PCG determinism tests
- [ ] add economy/world-sim smoke tests
- [ ] add UI sanity tests
- [ ] add integration regression checklist

---

# Highest-priority closure order

## Immediate Top 12
1. [ ] Unified source tree/build
2. [ ] World/bootstrap orchestration
3. [ ] Data registry unification
4. [ ] Real input/context system
5. [ ] Real rendering backend/viewport
6. [ ] Save/load implementation
7. [ ] UI framework implementation
8. [ ] Voxel editor workflow
9. [ ] Salvage/mining reward hookup
10. [ ] Station/home-base hookup
11. [ ] Outliner/inspector/gizmo completion
12. [ ] Validation toolkit

---

# Recommended work tracks

## Track A — Consolidation
- unified source tree
- one build
- one orchestrator
- one data layer

## Track B — Core playability
- input
- rendering
- save/load
- runtime UI

## Track C — Editor usefulness
- voxel editor
- outliner
- inspector
- gizmos
- validation
- undo/redo

## Track D — Loop completion
- salvage/mining payout
- contracts/rewards/progression
- stations/manufacturing/storage
- fleet/world-sim/titan linkage

---

# Final takeaway

What’s missing now is not the project’s identity.

What’s missing is:
- **consolidation**
- **real subsystem hookups**
- **usable editor workflows**
- **actual runtime presentation**
- **production-grade persistence and validation**

Once those are closed, the project stops feeling like a large structured prototype and starts feeling like a real buildable game/editor platform.
