# MasterRepo Entity / Component Architecture

## Purpose
This document locks the runtime object model for Master Repo so gameplay, tooling, AI workflows, persistence, and migration can all converge on one coherent structure.

---

## 1. Decision summary

### Locked decision
Master Repo will use a **hybrid entity/component architecture**.

That means:
- **Entities** provide stable identity, ownership anchoring, and system registration
- **Components** provide modular runtime data and behavior attachment
- **High-level domain objects** provide readable orchestration for complex concepts like ships, stations, players, voxel structures, editor selections, and AI-facing workspace objects

This is **not** a pure ECS and **not** a classic deep inheritance object tree.

It is a hybrid model designed for:
- simulation-heavy runtime work
- editor/tooling integration
- save/load clarity
- AI inspection/edit workflows
- voxel + modular system interaction

---

## 2. Why this model was chosen

### Pure ECS was rejected because
- editor/tooling readability becomes worse
- AI and human inspection of high-level systems becomes harder
- save/load ownership becomes less obvious
- gameplay concepts like ships, stations, and player rigs benefit from named wrapper objects

### Pure object/inheritance architecture was rejected because
- it becomes rigid as systems expand
- feature mixing gets messy
- data-oriented updates become harder
- sim/networking/runtime system grouping becomes less efficient

### Hybrid model advantages
- stable high-level concepts remain understandable
- lower-level systems remain modular
- data can still be externalized cleanly
- voxel structures and module graphs can have clear ownership boundaries
- runtime/editor/AI views of the same object can stay aligned

---

## 3. Core architecture model

Master Repo runtime identity is built in four layers:

### Layer 1 — World
A world is the top-level runtime container.

It owns:
- world metadata
- entity registry
- chunk managers
- subsystem managers
- persistence domains
- simulation clocks
- editor session overlays

### Layer 2 — Entity
An entity is the **smallest stable identity-bearing runtime unit**.

An entity:
- has a unique ID
- belongs to one world
- can have components
- can be referenced by other entities, tools, saves, and AI
- does not need to map 1:1 with visual scene objects

### Layer 3 — Component
A component is a typed attachment storing data and system-facing state.

Examples:
- TransformComponent
- VoxelStructureRefComponent
- ModuleContainerComponent
- HealthComponent
- InventoryComponent
- AirVolumeComponent
- InputContextComponent
- EditorSelectableComponent

### Layer 4 — Domain Object Wrapper
A domain object wrapper is a high-level orchestrator that presents a meaningful concept.

Examples:
- Ship
- Station
- PlayerCharacter
- EVAActor
- MechRig
- ToolOverlaySession
- AIWorkspaceContext

A wrapper may own or coordinate:
- one root entity
- several supporting entities
- associated voxel chunks
- graph/network data
- editor projections
- save/load helpers

---

## 4. Locked terminology

### World
A runtime or editor-executing simulation space.

### Entity
A stable identity anchor for runtime state.

### Component
A modular typed state unit attached to an entity.

### Domain Object
A higher-level gameplay/editor/AI concept composed from entities + components + associated subsystem state.

### Structure
A large construct such as a ship, station, wreck, room cluster, or generated habitat. Usually backed by voxel data plus module graphs.

### Actor
A runtime-present, behaviorally active domain object or entity grouping. The term may be used informally, but engine internals should prefer **Entity** and **Domain Object**.

### Handle
A lightweight reference to an object, entity, component, graph, or structure that can survive subsystem boundaries safely.

---

## 5. Identity model

## 5.1 Global identity rules
Every entity must have a **world-unique EntityID**.

EntityID requirements:
- deterministic enough for save/load remap
- safe for references
- not reused during a world session
- serializable to string or integer form
- usable across runtime, tooling, save data, and AI logs

### Locked format
Use a 64-bit or 128-bit engine ID abstraction internally, exposed through a typed wrapper.

Recommended wrapper:
- `EntityId`
- invalid/null sentinel supported
- string conversion helpers for logs and save files

## 5.2 Domain object identity
High-level objects have a separate stable identifier when needed.

Examples:
- `StructureId`
- `ModuleInstanceId`
- `PlayerId`
- `SessionToolId`
- `MissionId`

These are not replacements for EntityId.  
They exist when a domain concept must survive entity rearrangement.

## 5.3 Save identity rule
Save/load references must prefer:
1. domain-level IDs for major persistent objects
2. entity IDs for runtime-owned object references
3. component-local keys only inside serialized component payloads

---

## 6. Ownership model

## 6.1 Ownership principles
Ownership must always answer:
- who creates this state
- who updates it
- who serializes it
- who destroys it
- who exposes it to tooling and AI

## 6.2 Ownership levels

### World-owned
Examples:
- global registries
- chunk managers
- faction sim state
- active editor session manager
- weather/space environment simulation

### Entity-owned
Examples:
- transform
- health
- inventory
- input context
- local tags
- selection flags

### Structure-owned
Examples:
- voxel chunk assignment for a ship/station
- structure power graph
- structure air network
- structure navigation graph
- module placement registry

### Domain-wrapper-owned
Examples:
- PlayerCharacter orchestration
- Ship gameplay API
- Station district access helpers
- Tool overlay session mode state
- AI workspace task context

## 6.3 Destruction rule
If an entity is destroyed:
- its entity-owned components are removed
- cross-references must be invalidated safely
- wrapper/domain objects depending on it must reconcile immediately
- structure/global systems must be notified through explicit events or queues

Entity destruction must never silently orphan graph state.

---

## 7. Component model

## 7.1 Component rules
A component:
- is typed
- belongs to exactly one entity
- stores state, not broad world ownership
- should remain focused in scope
- may be read by multiple systems
- should not directly own massive cross-world resources

## 7.2 Component categories

### Core runtime components
- TransformComponent
- NameComponent
- TagComponent
- LifetimeComponent

### Simulation components
- HealthComponent
- DamageReceiverComponent
- PowerNodeComponent
- ResourceNodeComponent
- AirSealComponent
- GravityAffectableComponent

### Gameplay components
- InventoryComponent
- EquipmentComponent
- InteractionComponent
- QuestStateComponent
- FactionAffinityComponent

### Structure integration components
- VoxelStructureRefComponent
- ModuleContainerRefComponent
- BuildSocketComponent
- StructuralAnchorComponent

### Tool/editor components
- EditorSelectableComponent
- InspectorMetadataComponent
- GizmoTargetComponent
- DebugLabelComponent

### AI-facing components
- AINamedContextComponent
- SemanticRoleComponent
- ChangeTrackingComponent
- DocumentationLinkComponent

## 7.3 Anti-bloat rule
If a component becomes a bag of unrelated state, split it.

## 7.4 Behavior rule
Components store state.  
Systems execute behavior.  
Wrappers orchestrate high-level intent.

---

## 8. System model

A system is a world-level processor that:
- iterates relevant entities/components
- updates state
- coordinates with domain objects and structure registries
- emits events or queues follow-up work

### Example systems
- TransformSystem
- DamageSystem
- ModulePlacementSystem
- PowerNetworkSystem
- AirPressureSystem
- SelectionSystem
- InputRoutingSystem
- SavePrepSystem

### Locked rule
Systems may query wrappers or structure registries when needed, but component iteration remains the standard path for repeated runtime processing.

---

## 9. Domain object wrappers

## 9.1 Purpose
Wrappers exist to provide understandable ownership and APIs for complex objects.

### Example: Ship wrapper
A Ship wrapper may coordinate:
- root entity
- voxel structure handle
- module registry handle
- power graph handle
- air network handle
- docking state
- crew assignments
- current flight state

### Example: PlayerCharacter wrapper
A PlayerCharacter wrapper may coordinate:
- root entity
- inventory entity or components
- equipment loadout
- rig/mech possession state
- camera mode
- current input context
- mission interaction hooks

## 9.2 Wrapper rules
A wrapper:
- may not replace the entity registry
- must keep references explicit
- must not hide ownership ambiguities
- must expose serialization boundaries clearly
- should provide readable APIs for gameplay/editor/AI

---

## 10. Voxel architecture relationship

## 10.1 Voxel truth rule
Voxel data is not a component on every voxel cell.  
Voxel data belongs to structure/chunk systems.

### Locked rule
Voxel chunks are owned by chunk/structure subsystems, not by individual entities.

Entities reference voxel-backed structures through components or wrappers:
- `VoxelStructureRefComponent`
- `StructuralAnchorComponent`

## 10.2 Why
A ship hull with millions of cells cannot be modeled as millions of entities.

## 10.3 Result
The entity/component layer references voxel systems.  
It does not replace them.

---

## 11. Module architecture relationship

Modules are domain-level functional objects with persistent identity.

### Locked rule
Modules are not anonymous components.
A placed module is represented by:
- a `ModuleInstanceId`
- structure/module registry membership
- optional supporting entity when interaction, visuals, damage targeting, or tooling benefit from one

### Module representation options
A module may exist as:
1. registry-only data plus graph nodes
2. registry data plus one entity with components
3. registry data plus multiple helper entities for interaction/collision/ui

The chosen form depends on runtime needs, but the persistent truth is the **module registry instance**, not a scene mesh.

---

## 12. Editor and tooling integration

## 12.1 Tool-facing identity
Tooling must be able to select:
- entities
- structures
- modules
- chunks
- graph nodes
- domains like mission objects or AI task results

### Locked rule
Selection is represented by a **SelectionHandle** abstraction, not only raw entity IDs.

### SelectionHandle may target:
- Entity
- Structure
- ModuleInstance
- VoxelChunk
- GraphNode
- ToolSessionObject

## 12.2 Inspector rule
The inspector must be able to show:
- domain object overview
- entity details
- component list
- associated structure/network links
- save identity references

This is one reason the hybrid model is required.

---

## 13. AI integration

Arbiter and future AI tools must not rely on scraping arbitrary scene data.

### Locked rule
AI-facing systems access the runtime model through:
- world registries
- entity/component query APIs
- domain wrapper APIs
- semantic/documentation metadata components
- audit/change-tracking systems

### Benefits
- deterministic inspection
- easier diff generation
- safer refactor targeting
- better save/runtime/tool consistency

---

## 14. Serialization model

## 14.1 Serialization layers
Serialization is split by ownership domain:

### World serialization
- world seed
- global sim state
- registry metadata
- active sessions

### Structure serialization
- voxel chunk references
- module instances
- power/resource/air graphs
- structure-local metadata

### Entity serialization
- entity ID
- component payloads
- local links
- runtime state intended to persist

### Domain wrapper serialization
Wrappers do not always serialize directly.
Often they serialize by delegating to:
- structure data
- entity data
- specific domain records

## 14.2 Locked rule
Serialization authority follows ownership.  
No system should serialize data it does not own.

## 14.3 Versioning rule
Every serialized domain must support version tagging and migration hooks.

---

## 15. Lifetime model

## 15.1 Entity lifetime states
Recommended states:
- Created
- Registered
- Active
- Disabled
- PendingDestroy
- Destroyed

## 15.2 Component lifetime
Components are valid only while attached and registered.

## 15.3 Wrapper lifetime
Wrappers may outlive a temporary entity remap if they own stable domain IDs, but they must reconcile references on load or rebuild.

## 15.4 Streaming rule
World streaming may unload chunks, structures, and support entities.  
Persistent domain identities must survive unload/reload.

---

## 16. Event and dependency rules

### Event use
Use events/messages for:
- entity destruction
- module placement/removal
- structure seal breaches
- selection changes
- save/load transitions

### Dependency rule
Components should avoid hard coupling to unrelated systems.

### Wrapper dependency rule
Wrappers may coordinate many systems, but dependencies must be visible and documented.

---

## 17. Proposed base types

## 17.1 Core IDs
- `WorldId`
- `EntityId`
- `StructureId`
- `ModuleInstanceId`
- `PlayerId`
- `SessionId`

## 17.2 Core handles
- `EntityHandle`
- `StructureHandle`
- `ModuleHandle`
- `SelectionHandle`

## 17.3 Core registries
- `EntityRegistry`
- `ComponentRegistry`
- `StructureRegistry`
- `ModuleRegistry`
- `SelectionRegistry`
- `DomainObjectRegistry`

---

## 18. Proposed minimal class layout

```text
World
 ├─ EntityRegistry
 ├─ ComponentRegistry
 ├─ StructureRegistry
 ├─ DomainObjectRegistry
 ├─ SystemScheduler
 ├─ ChunkManager
 ├─ SaveManager
 └─ ToolSessionManager

DomainObjectRegistry
 ├─ ShipRegistry
 ├─ StationRegistry
 ├─ PlayerRegistry
 ├─ ToolSessionRegistry
 └─ AIContextRegistry
```

### Minimal runtime types
- `Entity`
- `IComponent`
- `World`
- `ISystem`
- `Ship`
- `Station`
- `PlayerCharacter`
- `VoxelStructure`
- `ModuleInstance`

---

## 19. What is an entity vs not an entity

### Usually an entity
- player body
- NPC body
- interactable tool object
- door if direct interaction/damage is needed
- loose cargo crate
- turret if behaviorally active
- editor gizmo target
- camera proxy
- mission marker object

### Usually not an entity
- individual voxel cells
- every graph edge
- static metadata rows
- every UI widget
- every save file record
- every power packet or resource tick

### Sometimes an entity
- module root
- room volume
- docking port
- build preview ghost
- hazard volume
- mech occupancy point

Use runtime behavior, interaction needs, and tooling needs to decide.

---

## 20. Migration guidance for legacy repos

When auditing old code:
- convert inheritance-heavy gameplay objects into domain wrappers + components
- move giant data blobs out of classes into data definitions or focused components
- preserve meaningful top-level concepts like Ship or Station as wrappers
- do not convert voxel internals into entities
- do not assume old folder naming matches new ownership rules

### Adopt / refactor examples
- Old `ShipActor` class -> Ship wrapper + root entity + ship components + structure registry entry
- Old `InventoryManager` singleton -> world system plus InventoryComponent ownership per entity
- Old `PlacedModule` object -> Module registry instance + optional entity for interaction

---

## 21. Hard rules going forward

1. **Every persistent gameplay object must have a clear identity owner**
2. **Every serialized field must have a clear serialization owner**
3. **Voxels stay in voxel systems, not entity explosion**
4. **Modules persist through module registries, not scene meshes**
5. **Systems process state, components store state, wrappers orchestrate concepts**
6. **Tooling and AI access must use registries/handles, not ad hoc traversal**
7. **Entity deletion must never orphan graph or structure data**
8. **Selection and inspection must support more than entity IDs**
9. **Streaming must preserve stable domain identities**
10. **Legacy repo migration must conform to this model, not reshape this model**

---

## 22. Immediate follow-on implementation tasks

### Required code tasks
1. Create typed ID wrappers
2. Create EntityRegistry
3. Create ComponentRegistry
4. Create SelectionHandle abstraction
5. Create StructureRegistry
6. Create Module registry with persistent instance IDs
7. Define base wrapper classes for Ship, Station, PlayerCharacter
8. Define serialization ownership map
9. Add debug inspector output for entity/component/domain views

### Required design tasks
1. Component catalog v1
2. System scheduler/update order document
3. Structure registry spec
4. Selection/inspector architecture doc
5. Save ownership matrix

---

## 23. Final locked outcome

Master Repo runtime architecture is now:

**hybrid entity/component + domain wrapper + structure registry**

In practical terms:
- entities give stable identity
- components provide modular state
- systems do repeated processing
- domain wrappers make major concepts readable
- voxel and module registries hold large structural truth
- tooling and AI operate through handles and registries

This is the architecture all future gameplay, tooling, AI, save/load, and migration work should follow.
