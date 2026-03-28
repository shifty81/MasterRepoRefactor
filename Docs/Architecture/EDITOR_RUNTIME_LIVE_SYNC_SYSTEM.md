# EDITOR_RUNTIME_LIVE_SYNC_SYSTEM.md

## Purpose

This document defines the live sync model between:

- **AtlasAI WPF tooling**
- **Atlas editor/backend services**
- **live Atlas runtime/simulation**

The goal is to support a modern workflow where the editor and runtime can interact without requiring constant full reloads, while preserving simulation integrity and authority.

This system must support:
- live scene/entity inspection
- live edits where safe
- paused-step-edit workflows
- runtime preview
- diagnostics and diff visibility
- future AtlasAI-assisted editing flows

---

# 1. Core Direction

The recommended model is:

## **Command-based editor/runtime sync with authoritative runtime state and explicit edit modes**

This means:

- the runtime remains authoritative over live simulation state
- the editor does not directly mutate arbitrary memory
- editor actions become validated commands
- runtime returns authoritative results and events
- some edits are immediate
- some edits require pause/step/apply
- some edits require rebuild/reload

This is the safest path to a powerful live workflow.

---

# 2. Why this model

A direct “editor just pokes runtime memory” approach creates:
- hard-to-debug corruption
- no audit trail
- bad multiplayer assumptions
- poor undo/redo support
- fragile tool/runtime coupling

A command-based live sync model gives:
- validation
- traceability
- undo support
- replayability
- authority clarity
- compatibility with services and multiplayer-hosted runtime scenarios

---

# 3. Authority Rules

## 3.1 Runtime authority
The live runtime/simulation is authoritative for:
- active entity state
- tick progression
- physics truth
- combat/resource state
- mission/faction state
- authoritative ECS world state

## 3.2 Editor authority
The editor is authoritative for:
- authoring intent
- edit request generation
- selection state
- inspector UI state
- undo/redo stacks at the tool layer
- preview orchestration

## 3.3 Asset authority
The asset pipeline is authoritative for:
- source asset registration
- import/cook outputs
- asset metadata and validation

---

# 4. Sync Modes

## 4.1 Authoring-only mode
Editor changes affect authored data only, not a live runtime.

Used for:
- offline content editing
- schema-heavy changes
- major prefab restructuring
- changes that need recook or rebuild

## 4.2 Live preview mode
Changes are applied to a preview runtime instance that is not the primary gameplay session.

Used for:
- material/mesh previews
- prefab test scenes
- encounter previews
- local simulation trials

## 4.3 Live simulation edit mode
Changes are applied to the active simulation with validation and restrictions.

Used for:
- transform edits
- selected property edits
- debug spawning
- mission trigger testing
- balance tuning
- environment state tweaks

## 4.4 Paused-step-edit mode
Simulation is paused or stepped, and edits are applied between ticks or controlled step points.

Used for:
- structural edits
- debugging collisions
- event trigger testing
- deterministic reproduction work
- complex state inspection

---

# 5. Edit Categories

## 5.1 Safe immediate edits
Can usually apply live without pause:
- debug visualization toggles
- inspector labels/tags
- non-authoritative editor annotations
- some balance values
- some mission tuning data
- some material/lighting preview values
- telemetry filters

## 5.2 Conditional live edits
Allowed live if validation passes:
- entity transform adjustments
- NPC spawn/despawn for testing
- inventory test injection in debug mode
- mission state override in debug mode
- door state changes
- room ownership debug swaps
- market tuning in debug simulation

## 5.3 Pause-required edits
Should require paused-step-edit mode:
- structural prefab graph changes
- interior topology changes
- collision-critical changes
- component add/remove on active critical entities
- docking topology changes
- major power-network rewires
- boarding breach topology edits

## 5.4 Reload/rebuild-required edits
Must not be live-applied directly:
- incompatible asset schema changes
- importer-setting changes needing recook
- deep animation skeleton changes
- package format changes
- network-critical schema layout changes

---

# 6. Sync Flow

Recommended high-level flow:

```text
Editor action in WPF
    ↓
Editor command object
    ↓
AtlasAI.Bridge / Editor client
    ↓
AtlasEditorService / runtime edit service
    ↓
Validation against runtime and edit policy
    ↓
Apply at safe boundary
    ↓
Authoritative result event
    ↓
Inspector/viewport/log update
```

---

# 7. Command Model

## 7.1 All live edits should be command-based

Examples:
- `MoveEntity`
- `RotateEntity`
- `SetComponentProperty`
- `SpawnDebugEntity`
- `DespawnEntity`
- `ToggleDoorState`
- `SetMissionStage`
- `InjectMarketEvent`
- `PauseSimulation`
- `StepSimulation`
- `ApplyPrefabOverride`
- `ReloadAssetPreview`

## 7.2 Command requirements
Each command should include:
- target runtime/session ID
- editor user/session identity
- target entity/asset ID
- intended change payload
- edit mode requirement
- validation context
- timestamp/sequence ID

---

# 8. Safe Application Boundaries

Edits should apply only at explicit safe boundaries.

Examples:
- between simulation ticks
- while paused
- at system-defined pre/post-update phases
- in preview-only worlds
- in editor-owned sandbox sessions

Avoid arbitrary mid-system mutation.

---

# 9. Undo / Redo Model

## 9.1 Tool-side undo/redo
The WPF editor should maintain user-facing undo/redo history for edit commands.

## 9.2 Runtime-aware reversibility
Not every live edit is safely reversible by simply restoring old values.

For each command, define whether it is:
- reversible
- partially reversible
- not reversible live

Examples:
- transform move: reversible
- debug spawn: reversible if spawned entity tracked cleanly
- mission consequence trigger: may not be fully reversible
- economy transaction simulation: may require explicit rollback support

---

# 10. Selection and Inspection

## 10.1 Selection lives in tooling
Selected entity/asset/component state belongs to the editor/tooling layer.

## 10.2 Inspection reads authoritative data
Inspector panels should query authoritative runtime state through service APIs.

Inspector views should support:
- current values
- pending local edits
- last authoritative ack
- validation warnings
- diff from authored defaults
- diff from previous snapshot/tick if useful

---

# 11. Entity and Component Editing

## 11.1 Property editing
Component properties should be editable through typed, validated editors.

Avoid generic blind reflection editing for critical systems.

## 11.2 Component add/remove
Adding or removing components live should be tightly restricted.

Allowed only when:
- the entity supports dynamic reconfiguration
- the target mode allows it
- validation ensures systems remain coherent
- replication/networking safety is considered if in multiplayer preview or server mode

---

# 12. Prefab and Asset Overrides

## 12.1 Live instance override vs authored asset change
These must be distinct.

### Live instance override
Change one runtime instance only.

### Authored asset change
Change the source/prefab/asset definition, which may later propagate to instances.

This distinction is essential.

## 12.2 Propagation model
When an authored prefab changes:
- some preview/runtime instances may be refreshable
- some must be flagged stale
- some must be recreated

Do not silently force deep live migrations on active runtime entities unless explicitly supported.

---

# 13. Pause / Step / Resume Model

## 13.1 Required controls
Editor/runtime sync must support:
- pause simulation
- single-step tick
- step N ticks
- set slow-motion/debug rate
- resume

## 13.2 Use cases
- debugging combat outcomes
- validating mission trigger chains
- testing boarding transitions
- adjusting power/fuel tuning
- inspecting faction/security response timing

---

# 14. Event and Diff Visibility

## 14.1 Event visibility
The editor should receive:
- command accepted/rejected
- validation diagnostics
- entity state changed
- asset reload required
- runtime stale-state warnings
- simulation paused/resumed
- sync mode changes

## 14.2 Diff visibility
Useful diff views:
- authored vs live instance
- previous tick vs current tick
- pre-command vs post-command
- prefab default vs overridden value

These are especially valuable for debugging.

---

# 15. Multiplayer-Aware Editing

## 15.1 Editing in server-hosted worlds
If a live runtime is a networked/server-hosted session, editing must respect authority and permissions.

Rules:
- editor commands still go to the authoritative runtime/server
- changes may need admin/debug permissions
- other connected clients may need replicated update notifications
- some edits should be blocked in non-debug public sessions

## 15.2 Debug realms / sandbox instances
Highly recommended:
- sandbox preview worlds
- dev-only test sectors
- isolated editor-owned runtime sessions

This avoids contaminating real persistent sessions during development.

---

# 16. Asset Reload and Runtime Sync

## 16.1 Asset change path
When an asset changes:
1. source asset updated
2. asset pipeline imports/validates/cooks
3. runtime receives asset reload availability notice
4. runtime evaluates live reload policy
5. runtime applies safe reload or marks reload required

## 16.2 Runtime reload categories
- immediate safe reload
- deferred until pause
- deferred until entity recreation
- full scene/session reload required

---

# 17. Editor Service Responsibilities

`AtlasEditorService` should own the runtime-facing editing API.

Responsibilities:
- command validation
- edit policy enforcement
- safe apply timing
- entity/component inspection APIs
- selection query support
- diff generation support
- runtime edit event emission
- pause/step/resume control
- sandbox session support

---

# 18. WPF Tooling Responsibilities

AtlasAI WPF tooling should own:
- panel UX
- inspector UX
- selection state
- gizmo/tool state
- undo/redo history
- user-facing change review
- edit-mode display
- command submission UI
- error/report presentation

WPF tooling should not own:
- actual simulation state mutation logic
- raw runtime memory editing
- asset pipeline truth
- authoritative world state

---

# 19. Recommended Initial Live Sync Features

Start with:
1. entity selection
2. inspector readback
3. transform edit command
4. pause/resume
5. single-step tick
6. spawn/despawn debug entities
7. simple property edits for safe components
8. log/validation event stream
9. asset reload notifications
10. authored-vs-live diff basics

Then add:
- prefab instance override tools
- mission/faction debug editors
- room/interior graph editing
- power/resource network visualization
- multi-entity batch edits

---

# 20. Common Pitfalls to Avoid

- letting the editor directly poke runtime memory
- no distinction between live instance edits and authored asset edits
- editing active simulation mid-system with no safe boundary
- no permissions model for server-hosted runtime editing
- no diff visibility
- assuming every asset change can hot reload safely
- trying to force undo for irreversible world consequences without a real rollback model

---

# 21. Bottom Line

The right live sync model is:

- **command-based**
- **runtime-authoritative**
- **safe-boundary applied**
- **mode-aware**
- **diff-visible**
- **undo-friendly where realistic**
- **service-driven for WPF tooling**

That gives Atlas a modern editor/runtime workflow without sacrificing simulation integrity.
