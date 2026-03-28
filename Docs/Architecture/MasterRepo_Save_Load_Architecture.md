# MasterRepo Save / Load Architecture

## Purpose
This document locks the persistence architecture for Master Repo so voxel worlds, structures, modules, simulation state, tooling sessions, AI-assisted workflows, and legacy migration all rely on one stable save/load model.

---

## 1. Decision summary

### Locked decision
Master Repo will use a **layered, versioned, domain-owned persistence model**.

This means:
- persistence is split by ownership domain
- each domain serializes only the data it owns
- save files are versioned
- migration handlers are required
- large structural data is partitioned from gameplay/session data
- runtime objects are reconstructed from persistent records, not blindly memory-dumped

This is **not** a monolithic single-file snapshot model and **not** a pure rebuild-from-seed-only model.

It is a hybrid persistence model designed for:
- voxel-heavy structural data
- modular functional graphs
- simulation continuity
- editor/tooling workflows
- AI-safe change tracking
- long-term schema evolution

---

## 2. Why this model was chosen

### Monolithic full snapshot was rejected because
- world and voxel data can become very large
- migration becomes painful
- corruption risk affects too much at once
- save diffing and audit become harder
- tooling/editor partial saves are awkward

### Rebuild-from-seed-only was rejected because
- player-made changes, damage, repairs, inventory, and mission state must persist
- simulation divergence matters
- procedural seeds do not capture player history

### Layered domain-owned persistence advantages
- cleaner ownership and migration
- easier incremental saves
- easier corruption recovery
- easier audit and diff
- better fit for streamed voxel data
- safer AI-assisted editing and refactor support

---

## 3. Persistence domains

Master Repo persistence is divided into the following domains:

### A. Save Manifest Domain
Top-level save metadata and index records.

### B. World Metadata Domain
World identity, seed, global settings, versioning, and high-level session facts.

### C. Structure Domain
Ships, stations, wrecks, habitats, rooms, structural containers, and their graph/state records.

### D. Voxel Domain
Chunked voxel material/state/damage data.

### E. Entity / Component Domain
Persisted runtime entities and their component payloads.

### F. Simulation Domain
Faction, economy, jobs, missions, seasonal state, environmental sim, and other world-level simulation records.

### G. Player Domain
Player identity, inventory, skills, equipment, progression, location, and active context.

### H. Tooling / Editor Session Domain
Panel layouts, selection state, workspace tabs, view modes, debug toggles, editor sessions where persistence is intended.

### I. AI Workspace Domain
Arbiter context caches, change proposals, patch sessions, audit logs, and approved workspace artifacts where persistence is intended.

### J. Config / Preferences Domain
User and project preferences separate from world save history.

---

## 4. Ownership rule

### Locked rule
Every serialized field must have a single authority owner.

That owner may be:
- manifest
- world
- structure
- voxel chunk
- entity/component
- simulation subsystem
- player record
- tooling session
- AI workspace session
- config/preferences system

No field should be serialized redundantly by multiple domains without an explicit cache/derived-data rule.

---

## 5. Save package structure

## 5.1 High-level save layout
A save should be stored as a **save package folder** or equivalent package abstraction, not one giant blob.

### Recommended structure
```text
/Saves/<SaveName>/
  manifest.json
  world/
    world_meta.json
    globals.json
  structures/
    <StructureId>/
      structure_meta.json
      modules.json
      power_graph.json
      resource_graph.json
      air_graph.json
      navigation_graph.json
  voxels/
    <StructureId>/
      chunk_<x>_<y>_<z>.bin
    world_chunks/
      chunk_<x>_<y>_<z>.bin
  entities/
    entities.json
  simulation/
    factions.json
    economy.json
    jobs.json
    missions.json
    seasonal_state.json
  players/
    player_<PlayerId>.json
  tooling/
    workspace_layout.json
    sessions.json
  ai/
    pending_changes.json
    approved_patches.json
    audit_log.json
  prefs/
    local_overrides.json
```

This can be represented physically as folders, archives, or package bundles later, but the logical partition must remain.

---

## 6. Versioning model

## 6.1 Global save version
Every save package must have:
- save format version
- engine version
- project data/schema version
- optional branch/build identifier

### Example
```json
{
  "save_format_version": 3,
  "engine_version": "0.2.0",
  "data_version": "2026.03.master",
  "branch": "main"
}
```

## 6.2 Domain-local versioning
Major domains may also carry their own version numbers.

Examples:
- structure schema version
- voxel chunk format version
- mission schema version
- player progression version

## 6.3 Locked rule
Migration can occur:
- at full-save manifest level
- at domain level
- at individual record level when required

Migration handlers must be explicit and testable.

---

## 7. Save manifest

The manifest is the entry point into a save package.

### Manifest responsibilities
- identify save package
- record versions
- list major included domains
- record creation and last-save timestamps
- track active player and world ID
- provide integrity metadata
- provide migration hints if needed

### Example responsibilities
- human-readable save name
- quick thumbnail reference later
- world seed
- build compatibility info
- corruption flags/recovery state if applicable

### Locked rule
The manifest must be lightweight and readable without loading the entire world.

---

## 8. World metadata domain

This domain stores:
- world ID
- world seed
- generation profile
- active rulesets
- calendar/time state
- top-level progression mode
- save-safe global toggles
- currently loaded region set metadata if needed

### Does not store
- full voxel data
- all structure internals
- every entity payload
- derived rendering caches

### Locked rule
World metadata identifies the world and the broad simulation context.  
It does not become a dumping ground for everything else.

---

## 9. Structure domain

This is one of the most important persistence layers.

### Structures include
- ships
- stations
- derelicts
- ruins
- mechs if structurally persistent
- generated installations
- room clusters if modeled as persistent structures

### Structure persistence includes
- `StructureId`
- type/classification
- transform anchor
- ownership/faction
- references to voxel sets
- module instances
- structure-local graphs
- environmental state
- docking/attachment state
- damage state summaries
- style/profile tags
- persistence references to child records

### Locked rule
A structure owns its structural graphs and references its voxel data, but does not duplicate chunk payloads inline.

### Important
Structure save should be able to load independently enough for inspection and migration without requiring every unrelated world system to be loaded.

---

## 10. Voxel domain

## 10.1 Voxel persistence model
Voxel data is stored by chunk or chunk-equivalent partition.

### Each chunk record may include
- chunk coordinates
- format version
- material IDs
- damage/deformation state
- repair state
- occupancy/compression encoding
- optional metadata for thermal/power/environment anchors if persisted at chunk level

## 10.2 Locked rule
Voxel chunks must be persisted in chunk-sized partitions, never as one giant structure-wide raw dump unless exporting for special tools.

## 10.3 Chunk ownership
Chunks belong to:
- world terrain
- a structure-local voxel set
- a streamed region package

### Chunk identity must include
- owning world or structure
- local coordinates
- chunk format version

## 10.4 Compression rule
Chunk formats may be compressed, but compression is a storage detail.  
Logical ownership and versioning remain explicit.

---

## 11. Entity / Component domain

## 11.1 Purpose
Persist runtime entities that represent meaningful state not already fully covered by structures or world simulation records.

### Examples
- loose cargo crates
- temporary mission actors intended to persist
- deployed devices
- player-adjacent helper entities
- interactables with ongoing state
- certain NPCs if persistence model requires them

## 11.2 Record contents
- `EntityId`
- archetype/type hint
- owned component payloads
- cross references by stable IDs
- load policy flags
- streaming or activation metadata if needed

## 11.3 Locked rule
Entity persistence should reference stable domain IDs where possible instead of fragile pointer-like relationships.

## 11.4 Non-goal
This domain is not for every transient runtime object.

Purely transient entities should be recreated at runtime, not persisted.

---

## 12. Simulation domain

This domain persists world-scale systems.

### Includes
- faction standings and territory control
- economy state
- production queues
- jobs and patrol assignments
- mission state
- anomaly progression
- seasonal collapse/reset timing
- regional hazards
- spawned event state when persistence matters

### Locked rule
Simulation persistence should be subsystem-partitioned.  
Do not serialize all global simulation into one giant file.

### Example partition
- `factions.json`
- `economy.json`
- `missions.json`
- `seasonal_state.json`

---

## 13. Player domain

### Persisted player data includes
- `PlayerId`
- profile metadata
- transform/context anchor
- active structure/sector/location reference
- inventory
- equipment
- skills
- progression
- active mission pointers
- unlocked knowledge/tech
- health/status
- mech/rig ownership or assignment links where needed

### Locked rule
Player data is always its own domain and should not be buried inside generic entity blobs.

This is critical for:
- migration
- profile inspection
- multiplayer evolution later
- seasonal/reset policies
- debugging progression issues

---

## 14. Tooling / editor session domain

Because Master Repo includes a built-in tooling layer, certain workspace state may be persisted intentionally.

### Examples
- panel layout
- open tabs/documents
- camera bookmarks
- selected tool mode
- debug visualization toggles
- favorite inspectors
- build/test workspace state

### Locked rule
Tooling session persistence must be explicitly opt-in by category.

Do not mix ephemeral editor noise with world save state without intent.

### Recommended split
- world-bound tooling state
- project/workspace UI state
- local user preferences

---

## 15. AI workspace domain

Because Arbiter participates in the workspace, some AI-related state may need persistence.

### Candidate records
- approved patch sessions
- pending patch proposals
- audit logs
- migration reports
- knowledge/index snapshots if intended
- task history relevant to project workflow

### Locked rule
AI persistence must be kept separate from world simulation data and must support auditability.

### Security rule
AI-generated change proposals must persist with:
- author/source metadata
- timestamp
- approval state
- affected file/domain references
- rollback references when applicable

---

## 16. Config / preferences domain

This is separate from save history.

### Includes
- local UI preferences
- keybindings
- debug defaults
- accessibility settings
- rendering preferences
- web server preferences
- user-specific tool settings

### Locked rule
Preferences are not world saves.  
World saves must remain portable without bundling every local preference unless explicitly exported.

---

## 17. Serialization format guidance

## 17.1 Human-readable vs binary
Use a mixed approach.

### Human-readable formats for
- manifests
- metadata
- module definitions
- structure metadata
- players
- missions
- settings
- AI logs and audit summaries
- lightweight entity/component payloads when practical

### Binary or compact formats for
- voxel chunks
- large dense simulation tables if needed
- derived caches that must persist
- heavy graph blobs if JSON becomes too expensive

## 17.2 Locked rule
Choose format based on data shape, size, auditability, and migration needs.  
Do not force everything into JSON and do not force everything into opaque binary.

---

## 18. Incremental save strategy

## 18.1 Save categories
Support at least:
- full save
- incremental save
- autosave
- quicksave
- domain-specific maintenance save where useful

## 18.2 Dirty tracking
Each domain should track dirtiness independently.

### Examples
- changed voxel chunks
- changed structure graph
- changed player inventory
- changed mission state
- changed tooling workspace layout

## 18.3 Locked rule
Incremental save writes only dirty domains or dirty partitions where supported.

This reduces:
- save time
- corruption blast radius
- unnecessary IO

---

## 19. Autosave policy

### Recommended autosave behavior
Autosave should:
- operate on dirty domains
- avoid interrupting high-frequency loops excessively
- keep rolling historical backups
- use safe write/replace strategy
- mark incomplete autosaves clearly if interrupted

### Locked rule
Autosave must never overwrite the only good copy without a recovery path.

---

## 20. Safe write strategy

### Required behavior
When writing any domain:
1. write to temp file/package area
2. validate written result if possible
3. swap/commit atomically where possible
4. update manifest and save journal
5. retain rollback copy when policy requires

### Locked rule
No direct destructive overwrite of critical save records without temp/commit flow.

---

## 21. Corruption handling and recovery

## 21.1 Corruption strategy
The save system must support:
- manifest validation
- missing-file detection
- domain-specific recovery attempts
- partial load with warnings when safe
- rollback to previous autosave/manual save
- migration failure reporting

## 21.2 Locked rule
Corruption in one domain should not automatically invalidate the entire save unless core manifest/world identity is unrecoverable.

### Example
A bad tooling session file should not destroy the player’s world save.

---

## 22. Load pipeline

### Recommended load stages
1. read manifest
2. validate versions and migration needs
3. load world metadata
4. mount structure registries
5. register voxel chunk ownership
6. load simulation global state
7. load player domain
8. instantiate persistent entities/components
9. reconstruct domain wrappers
10. apply tooling/AI sessions if requested and safe
11. rebuild derived caches
12. finalize runtime activation

### Locked rule
Load order follows dependency order, not file order.

---

## 23. Rebuild vs persist rules

Some runtime state should be persisted. Some should be rebuilt.

### Persist
- player progress
- voxel edits
- module placements
- structure graph truth
- mission outcomes
- economy/faction state
- approved AI workspace records where intended

### Rebuild
- render caches
- transient pathfinding caches
- temporary debug draw buffers
- short-lived effects
- derived UI state where not intentionally saved
- transient runtime-only entities

### Locked rule
Persist truth. Rebuild derivations.

---

## 24. Migration model

## 24.1 Migration triggers
Migration may be required when:
- save format version changes
- structure schema changes
- chunk format changes
- component schema changes
- player progression rules change
- legacy repo data is imported/refactored

## 24.2 Migration handler requirements
Each migration should declare:
- source version
- target version
- affected domains
- reversible or not
- validation step
- fallback behavior on failure

## 24.3 Locked rule
Migrations are explicit code/tools, not ad hoc load-time guesswork.

---

## 25. Legacy repo import relationship

Legacy zip repos are not save packages, but they may contain save-like data, configs, or serialized project state.

### Locked rule
Legacy imported data must pass through:
- audit classification
- schema mapping
- migration transform
- validation
- then persistence re-emission in Master Repo save format

Do not preserve old save shapes inside live Master Repo persistence except as archive references.

---

## 26. Networking relationship

Even before multiplayer is fully locked, persistence must prepare for authority separation.

### Locked rule
Save data should distinguish:
- portable persistent truth
- local-only preferences
- session/local cache data
- authority-sensitive state that may later be server-owned

This avoids future rewrite pain.

---

## 27. Tooling and AI safety relationship

### Tooling safety
Tooling edits that modify persistent world state must mark affected domains dirty explicitly.

### AI safety
AI-generated changes to persistent project/workspace artifacts must be:
- attributable
- auditable
- reversible where possible

### Locked rule
Persistence is part of the trust model, not just storage.

---

## 28. Proposed base interfaces

### Core persistence types
- `SaveManager`
- `SaveManifest`
- `SavePackage`
- `SaveDomain`
- `SaveJournal`
- `MigrationManager`

### Domain writers/loaders
- `WorldSaveAdapter`
- `StructureSaveAdapter`
- `VoxelChunkSerializer`
- `EntitySaveAdapter`
- `SimulationSaveAdapter`
- `PlayerSaveAdapter`
- `ToolingSessionSaveAdapter`
- `AIWorkspaceSaveAdapter`

### Dirty tracking
- `DirtyTracker`
- `DomainDirtySet`
- `ChunkDirtySet`

---

## 29. Proposed logical class diagram

```text
SaveManager
 ├─ ManifestReaderWriter
 ├─ MigrationManager
 ├─ DirtyTracker
 ├─ WorldSaveAdapter
 ├─ StructureSaveAdapter
 ├─ VoxelChunkSerializer
 ├─ EntitySaveAdapter
 ├─ SimulationSaveAdapter
 ├─ PlayerSaveAdapter
 ├─ ToolingSessionSaveAdapter
 └─ AIWorkspaceSaveAdapter
```

---

## 30. Hard rules going forward

1. **Persistence is domain-owned**
2. **Every save package is versioned**
3. **Manifest must be lightweight and readable**
4. **Voxel data is chunk-partitioned**
5. **Structure graphs persist separately from chunk payloads**
6. **Player data is its own domain**
7. **Tooling and AI persistence remain separate from core world truth**
8. **Incremental save is dirty-domain aware**
9. **Safe write/rollback behavior is mandatory**
10. **Persist truth, rebuild derivations**
11. **Legacy formats must migrate into Master Repo formats**
12. **Corruption in one domain should not destroy unrelated domains automatically**

---

## 31. Immediate follow-on implementation tasks

### Required code tasks
1. Create `SaveManifest` type
2. Create `SaveManager`
3. Create domain adapter interface
4. Create `DirtyTracker`
5. Create `VoxelChunkSerializer`
6. Create `StructureSaveAdapter`
7. Create `PlayerSaveAdapter`
8. Create migration registry
9. Create safe-write temp/commit workflow
10. Create manifest/domain validation checks

### Required design tasks
1. Save manifest schema
2. Structure save schema
3. Chunk binary format spec
4. Component persistence eligibility list
5. Corruption recovery matrix
6. Migration test plan

---

## 32. Final locked outcome

Master Repo persistence architecture is now:

**a layered, versioned, domain-owned save/load system with chunked voxel persistence, structure-partitioned state, subsystem-scoped simulation records, explicit migration handlers, and auditable tooling/AI persistence separation**

In practical terms:
- world saves are packaged as partitioned domains
- voxel data is chunked
- structures own graph truth
- players persist independently
- tooling and AI state are separated and auditable
- migration is explicit
- recovery and rollback are built into the design

This is the persistence architecture all future runtime, tooling, AI, and legacy migration work should follow.
