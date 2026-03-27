# ECS_AND_SIMULATION_ARCHITECTURE.md

## Purpose

This document defines the recommended **ECS and simulation architecture** for Atlas and NovaForge inside MasterRepo.

The design must support:

- large-scale world simulation
- deterministic or near-deterministic authoritative simulation
- tooling introspection
- multiplayer server authority
- modular ships/stations/interiors
- on-foot and ship gameplay
- scalable AI and faction/economy systems
- editor/runtime integration

---

# 1. Architectural Direction

The recommended model is a **hybrid data-oriented ECS with deterministic simulation discipline**.

That means:

- core simulation state is ECS-driven
- systems operate over stable component data
- behavior orchestration may still use higher-level helper objects where useful
- runtime/editor bridges observe ECS state through controlled APIs
- game features are built on ECS-backed world state, not giant inheritance trees

This is not pure dogmatic ECS everywhere. It is **ECS at the simulation core**, with practical wrappers around it.

---

# 2. Why this model

This project needs all of the following at once:

- ships composed of modular systems
- interiors and boarding spaces
- faction/policing/security logic
- economy simulation
- mining/construction/destruction
- server authority
- editor inspection and live manipulation
- future AI-assisted tooling

A traditional OOP object model becomes hard to scale here because:
- cross-system queries get expensive and messy
- save/load becomes more fragile
- networking state ownership becomes muddy
- editor introspection becomes inconsistent

A data-oriented ECS gives:
- clearer ownership
- better cache behavior
- better queryability
- more reliable serialization patterns
- easier deterministic stepping

---

# 3. Core Simulation Principles

## 3.1 The simulation runs on ticks

The authoritative simulation runs on fixed ticks.

Examples:
- 20 Hz, 30 Hz, or 60 Hz depending on mode
- render/update interpolation happens separately from authoritative simulation

The tick is the source of truth for:
- movement authority
- combat resolution
- economy updates
- faction standing changes
- mission progression
- construction/mining state
- AI decision commits

---

## 3.2 Render time is not simulation time

Rendering may interpolate between authoritative tick states.

Tools and runtime visuals may preview smooth motion, but gameplay truth lives on simulation ticks.

This keeps:
- replay/debugging cleaner
- networking more manageable
- deterministic simulation more realistic

---

## 3.3 ECS state is authoritative

Simulation truth lives in ECS component state and related authoritative data stores.

Avoid storing critical gameplay truth only in:
- visual scene graph nodes
- WPF UI state
- temporary runtime objects
- animation systems
- ad hoc singleton managers

---

# 4. Entity Model

## 4.1 Entity definition

An entity is a stable identity with component attachments.

Examples:
- ship
- ship thruster
- station
- cargo crate
- asteroid
- mining beam emitter
- player avatar
- NPC guard
- door
- interior room trigger
- projectile
- faction patrol waypoint
- market node
- mission marker

Entities should use compact IDs, not heavyweight class identities.

---

## 4.2 Entity categories

### World entities
Planets, asteroids, stations, fields, gates, anomalies.

### Actor entities
Players, NPCs, drones, mechs, creatures if added later.

### Structure entities
Ships, station modules, doors, rooms, docking points.

### Simulation helper entities
Spawn points, mission triggers, sensor volumes, nav markers.

### Transient entities
Projectiles, temporary effects, timed hazards.

---

# 5. Component Model

## 5.1 Components are data first

Components should be primarily state containers, not behavior objects.

Examples:
- `TransformComponent`
- `VelocityComponent`
- `HealthComponent`
- `PowerComponent`
- `FuelComponent`
- `FactionAffiliationComponent`
- `CargoInventoryComponent`
- `DockingPortComponent`
- `RoomMembershipComponent`
- `InteriorAccessComponent`
- `MissionParticipantComponent`
- `SensorSignatureComponent`

Behavior belongs in systems.

---

## 5.2 Component granularity

Components should be:
- meaningful
- composable
- not excessively tiny
- not giant “god components”

Bad:
- one `ShipEverythingComponent`

Bad:
- twenty microscopic components that always appear together with no value

Good:
- components organized by simulation responsibility

---

## 5.3 Suggested component families

### Spatial and motion
- Transform
- Velocity
- AngularVelocity
- GridAnchor
- OrbitState
- DockedState

### Physics and damage
- CollisionShape
- Mass
- Inertia
- Health
- Armor
- Shield
- DamageReceiver
- DamageEmitter

### Power and resources
- Reactor
- Battery
- FuelTank
- ResourceStorage
- ConsumptionProfile

### Ships and structures
- ShipCore
- ThrusterArray
- HardpointSet
- DockingPort
- InteriorRoot
- RoomMembership
- StructuralIntegrity
- ConstructionState

### Actors and NPCs
- CharacterState
- Inventory
- Equipment
- MovementMode
- CombatIntent
- DialogueState
- EVAState
- MechLink

### World systems
- FactionAffiliation
- SecurityZonePresence
- TradeNode
- MarketState
- MiningNode
- Salvageable
- ScanTarget
- DiscoveryState

### Missions and progression
- MissionState
- ObjectiveTracker
- RewardPending
- ReputationModifier
- TriggerBinding

---

# 6. System Model

## 6.1 Systems own behavior

Systems iterate over relevant component sets and update state.

Examples:
- physics system
- thruster system
- power distribution system
- shield recharge system
- cargo transfer system
- faction law enforcement system
- mission progression system
- economy pricing system
- mining extraction system
- construction assembly system

---

## 6.2 Systems should be ordered explicitly

A simulation phase graph is required. Do not rely on accidental ordering.

### Example high-level order
1. input command application
2. AI decision commit
3. movement intent / control resolution
4. physics integration
5. resource and power updates
6. collision/contact resolution
7. damage/combat resolution
8. mission/progression updates
9. faction/law/security updates
10. economy and world-state updates
11. cleanup / despawn
12. event emission for observers

Not every subsystem runs every tick at full frequency.

---

## 6.3 Variable-frequency simulation within fixed ticks

Some systems can run at lower frequencies:
- economy updates
- strategic faction behavior
- market repricing
- long-range NPC route planning
- slow planetary scans

Use tick scheduling or sub-rate execution, but keep the authoritative timeline coherent.

---

# 7. Determinism Strategy

## 7.1 Recommended target
Use **deterministic simulation discipline for core gameplay**, even if full cross-platform bit-perfect determinism is not achieved immediately.

Why:
- replays/debugging improve
- multiplayer architecture is cleaner
- system boundaries become healthier
- rollback or correction strategies become more realistic later

---

## 7.2 Determinism-sensitive areas
- movement authority
- combat resolution
- inventory transfer
- economy transactions
- mission progression
- construction state
- faction standing changes
- crime/security flags

## 7.3 Less sensitive areas
- cosmetic effects
- local-only particles
- audio timing nuance
- editor-only preview overlays

---

## 7.4 Practical rules
- fixed tick timestep
- stable system order
- stable random seeds by context
- avoid depending on render delta time
- isolate non-deterministic APIs
- keep floating-point risk visible
- consider deterministic math wrappers for critical systems over time

---

# 8. World Partition and Simulation Scope

## 8.1 Simulation scope must be partitioned

Not everything in the galaxy runs at full fidelity at all times.

Recommended layers:
- **Loaded high-fidelity simulation**
- **Regional medium-fidelity simulation**
- **Background strategic simulation**

### High fidelity
For nearby sectors, players, combat zones, boarding interiors, active mining/construction.

### Medium fidelity
For adjacent or relevant sectors with simplified but still explicit state progression.

### Background strategic
For distant economy/faction/world events at abstracted update rates.

---

## 8.2 Entity activation states
Entities may be:
- fully active
- partially simulated
- background-simulated
- dormant
- unloaded but persisted

This matters for performance and persistence.

---

# 9. Ship / Station / Interior Composition

## 9.1 Composition model
Ships and stations should be represented as compositions of:
- root entity
- structural/module entities
- interior graph entities
- hardpoints / sockets
- service nodes
- attachment relationships

Do not treat a ship as one opaque mega-object.

---

## 9.2 Interior integration
Interior spaces can be attached to ship/station entities as subgraphs.

Required support:
- room membership
- door/access state
- atmosphere or hazard state if later added
- boarding ownership changes
- EVA transition points
- dock/cut/breach entry points

---

# 10. Input and Command Model

## 10.1 Inputs should become commands
Player input and networked player actions should be converted into simulation commands.

Examples:
- apply thrust intent
- activate mining beam
- dock request
- open door
- fire weapon
- transfer cargo
- accept mission
- declare duel
- breach hull section

Commands are then applied on tick boundaries.

---

## 10.2 Tooling commands are separate from gameplay commands
Editor/runtime tooling commands must not be confused with player/gameplay commands.

Examples:
- spawn entity for preview
- inspect component set
- move selected entity in paused simulation
- apply prefab change

These need separate authority and validation paths.

---

# 11. Event Model

## 11.1 Systems emit events, but events are not the source of truth
Events are for:
- observers
- logs
- UI updates
- replay markers
- telemetry
- tooling

The ECS state remains authoritative.

---

## 11.2 Event categories
- gameplay events
- simulation diagnostics
- editor events
- replication events
- mission events
- asset/runtime reload events

---

# 12. Save / Load Model Interaction

ECS must be serializable in a stable way.

Recommended approach:
- component-wise serialization
- versioned component schemas
- chunk/region persistence
- archetype-aware snapshots where useful
- migration hooks for schema evolution

Do not serialize raw runtime pointers or UI assumptions.

---

# 13. Networking Interaction

The ECS authoritative state should be replication-friendly.

Recommended design:
- replication built around entity/component authority
- filtered state replication by interest management
- command-based client input submission
- server-authoritative correction

This will be expanded in the networking spec, but the ECS model must support it from the start.

---

# 14. Tooling and Introspection

## 14.1 AtlasAI and WPF tooling need introspection-friendly ECS
The ECS layer should expose:
- entity inspection
- component inspection
- archetype summaries
- filtered queries
- diff views between ticks/snapshots
- debug visualization hooks

## 14.2 Required tooling capabilities
- inspect selected entity
- inspect ship composition
- inspect room graph
- inspect power/resource flow
- inspect mission/faction state links
- inspect pending simulation events
- step simulation while observing state changes

This requires intentional debug/query APIs, not hacky reflection into internals.

---

# 15. Scheduling and Job Model

## 15.1 Systems should be job-friendly
The simulation graph should allow:
- parallel-safe systems
- staged barriers
- read/write dependency declarations
- batch iteration
- chunk-based processing

## 15.2 Do not over-parallelize blindly
Correctness, determinism, and debuggability matter more than theoretical thread usage.

Start with:
- explicit system dependencies
- safe parallel islands
- clear read/write rules

---

# 16. Recommended World Data Split

Use three major categories:

## 16.1 Authoritative simulation state
Lives in ECS/component stores and authoritative simulation services.

## 16.2 Derived presentation state
Used for visuals, interpolation, animation, and local-only presentation helpers.

## 16.3 Tooling/editor state
Selection, inspector filters, bookmarks, previews, edit commands.

These must not be mixed carelessly.

---

# 17. Initial Implementation Order

1. entity ID system
2. component storage model
3. base query model
4. fixed tick scheduler
5. command ingestion model
6. explicit phase ordering
7. serialization hooks
8. introspection/debug APIs
9. world partition activation model
10. replication-friendly change tracking

---

# 18. Recommended Hybrid ECS Boundaries

Use ECS for:
- simulation state
- authoritative world state
- combat/resource/economy logic
- entity composition
- replication-relevant state

Use wrappers/services/helpers for:
- complex editor UX
- pathfinding authoring tools
- design-time graph editing
- AI planning layer integration
- some content authoring abstractions

This avoids forcing every single concept into raw ECS syntax.

---

# 19. Common Pitfalls to Avoid

- giant entity classes disguised as ECS
- behavior-heavy components
- hidden global managers owning real gameplay truth
- no clear system ordering
- mixing render interpolation with simulation truth
- trying to full-fidelity simulate the entire galaxy at once
- storing authoritative state in UI/editor structures
- ignoring save/load and networking needs until late

---

# 20. Bottom Line

Atlas should use a **hybrid data-oriented ECS with fixed-tick authoritative simulation**.

That gives you:

- scalable simulation
- better multiplayer readiness
- better save/load patterns
- better tooling introspection
- better composition for ships/stations/interiors
- cleaner integration with AtlasAI and WPF tooling

It is the strongest fit for the project’s actual needs.
