# Builder + Salvage Spec — Deep Expansion

## Purpose

`Runtime/BuilderRuntime` and `Runtime/Salvage` convert modular authored structures into live gameplay systems.
They are the bridge between:
- authored builder assemblies
- voxel structural state
- low-poly readable interaction surfaces
- salvage, repair, and upgrade loops

This system must support:
- snap-graph-driven structures
- detachable assemblies
- cut / release workflows
- mission-tagged salvage
- repairable subsystems
- deterministic state deltas for save/load and PCG reconstruction

## Design rules

- Builder owns functional assembly topology.
- Voxels own structural mass, destruction, repair fill, and containment relevance.
- Low-poly owns readable surfaces, props, panels, conduit, interactable expression, and tier visuals.
- Salvage never directly rewrites authored prefab source; it produces runtime deltas.
- Detached state must be saveable and replayable from deterministic seed plus deltas.
- Runtime debug mode must be able to inspect and override builder and salvage states.

## Relationship model

```text
Prefab / Scene Authoring
        │
        ▼
Builder Assembly Definition
        │
        ├── Snap Graph
        ├── Module Definitions
        ├── Structural Links
        ├── Socket Rules
        └── Upgrade Metadata
        │
        ▼
Runtime Assembly Materialization
        │
        ├── Interactive Part Nodes
        ├── Salvage Targets
        ├── Repairable Subsystems
        ├── Hazard Links
        └── Saveable Delta State
```

## Core runtime objects

### AssemblyRuntimeComponent
Owns the live representation of a builder-authored object.

Responsibilities:
- create live node registry from authored assembly data
- expose attachment and dependency relationships
- resolve structural integrity state
- mark runtime deltas when parts detach, break, repair, or upgrade
- bridge to hazard, mission, and save/load systems

### SnapGraphRuntime
Owns:
- node adjacency
- socket compatibility
- supported detach routes
- dependency tracing
- propagation of failure or upgrade effects

### StructuralIntegrityRuntime
Owns:
- structural support validation
- dependent-node collapse/release logic
- breach risk tagging from missing pieces
- detachment legality based on remaining support

### SalvageTargetComponent
Owns:
- scan metadata
- required tool class
- detach progress
- loot output
- mission tags
- hazard tags
- salvage completion events

### RepairableSubsystemComponent
Owns:
- functional subsystem identity
- fault state
- required parts and tools
- staged repair progress
- post-repair restoration events
- downstream functional propagation

## Assembly taxonomy

```text
Assembly
├── Hull Segment
├── Structural Frame
├── Functional Module
│   ├── reactor
│   ├── conduit node
│   ├── life support node
│   ├── terminal
│   └── door / airlock component
├── Visual Module
│   ├── paneling
│   ├── conduit dressing
│   ├── pipes
│   ├── display units
│   └── aesthetic overlays
└── Salvage Node
    ├── scrap source
    ├── mission item housing
    ├── detachable subsystem
    └── optional loot pocket
```

## Salvage loop

1. Player scans target.
2. Runtime validates scanable state and reveals metadata.
3. Required tool and salvage tier are checked.
4. Structural dependency trace runs.
5. If legal, player begins cut / detach process.
6. Runtime updates detach progress.
7. On completion:
   - node detaches
   - loot is resolved
   - mission hooks fire if tagged
   - structural integrity recalculates
   - world delta is recorded
8. UI and telemetry update.

## Target metadata contract

Each salvage target should expose:

- `TargetId`
- `AssemblyId`
- `NodeId`
- `SalvageClass`
- `Tier`
- `RequiredTool`
- `RequiredToolTier`
- `DetachMode`
- `Integrity`
- `MissionTags[]`
- `HazardTags[]`
- `LootTableId`
- `IsCriticalStructuralNode`
- `CanScan`
- `CanDetach`
- `CanHarvestInPlace`

## Detach modes

- `CutFree`
- `Unbolt`
- `Unsocket`
- `ExtractCore`
- `HarvestMaterial`
- `MissionRetrieve`

The mode determines:
- tool usage
- animation prompts
- time to completion
- resulting item form
- hazard chance
- whether a new world actor is spawned or inventory item is granted directly

## Structural dependency rules

A node may be:
- free
- supported
- critical
- locked by mission state
- locked by pressure or hazard state
- locked by power state
- locked by neighboring integrity thresholds

Detachment must fail gracefully with a readable reason if:
- it would invalidate a protected objective
- it would collapse a required route before player reaches safety
- the node is still powered in a dangerous way
- the correct tool tier is not equipped

## Repair system relationship

Repair uses the same topology as salvage, but inversely.

Repairable subsystem flow:
1. identify faulted subsystem
2. inspect node requirements
3. provide missing part or patch state
4. complete repair stage
5. restore subsystem function
6. propagate restored state to dependent systems

Example:
- conduit regulator repaired
- linked door control regains power
- route to mission terminal reopens

## Hazard integration

BuilderRuntime and Salvage must react to:
- breach
- fire
- electrical discharge
- unstable mass release

Each target can carry hazard probabilities or explicit hazard links.

Example:
Removing a damaged panel may:
- reveal breach
- ignite sparking conduit
- disable gravity in a room
- release a mission item from containment

## Upgrade propagation

Installed upgrades should propagate through three layers:

```text
Functional Change
        │
        ▼
Builder Graph Tags Update
        │
        ├── subsystem limits change
        ├── new sockets become valid
        ├── room capability tags expand
        └── mission/PCG eligibility shifts
        │
        ▼
Visual Propagation
        ├── low-poly detail tier changes
        ├── conduit/panel dressing updates
        └── status indicators improve
        │
        ▼
Voxel/Durability Metadata
        ├── resistance shifts
        ├── thermal tolerance changes
        └── containment integrity changes
```

## Save/load requirements

Builder/salvage state must save:
- assembly id
- encounter seed
- detached node ids
- integrity deltas
- repaired node ids
- installed upgrade ids
- spawned loose salvage actors
- depleted loot tables
- active hazard states
- runtime-only lock states

## Runtime debug requirements

Atlas Suite Runtime Debug Mode should expose:
- assembly tree inspector
- snap graph viewer
- node detach toggle
- subsystem fault injector
- integrity recalculation button
- loot preview
- mission tag preview
- hazard injection by node
- delta export preview

## Telemetry events

Minimum events:
- assembly_materialized
- salvage_target_scanned
- salvage_detach_started
- salvage_detach_completed
- salvage_detach_failed
- subsystem_fault_detected
- subsystem_repair_started
- subsystem_repair_completed
- integrity_recalculated
- builder_delta_recorded

## Definition of done

This system is ready when the player can:
- scan a live assembly node
- detach one mission-critical object
- trigger a structural recalculation
- repair one subsystem on a ship or derelict
- save and reload all resulting deltas correctly
