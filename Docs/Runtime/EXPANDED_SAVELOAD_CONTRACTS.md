# Save/Load Contracts — Deep Expansion

## Purpose

Save/load is the persistence spine of the vertical slice.
It must preserve deterministic runtime state without serializing unnecessary whole-world blobs.

The save/load system must support:
- profile persistence
- campaign progression
- session continuity
- deterministic reconstruction of encounter state
- version-safe migration
- ordered subsystem serialization
- clear runtime error reporting

## Save domains

### ProfileSave
Owns:
- control bindings
- accessibility settings
- graphics/audio preferences
- preferred UI layout where applicable

### CampaignSave
Owns:
- season/campaign identity
- long-term faction standing
- tech unlock flags
- account-level progression hooks
- campaign statistics

### SessionSave
Owns:
- current active mission
- rig vitals and inventory
- equipped tools
- current ship state
- current sector/system context
- checkpoint location

### WorldInstanceSave
Owns:
- encounter seed
- spawned scenario id
- wreck deltas
- detached node state
- repaired subsystem state
- hazard state
- depleted loot state
- mission object state

## Architecture

```text
SaveCoordinator
├── DomainRegistry
│   ├── ProfileSaveMapper
│   ├── CampaignSaveMapper
│   ├── SessionSaveMapper
│   └── WorldInstanceSaveMapper
├── VersionStampService
├── SerializationGateway
├── DeterministicRestoreService
└── SaveErrorReporter
```

## Core classes

### SaveCoordinator
Responsibilities:
- orchestrate save order
- coordinate domain mappers
- write metadata and version stamps
- perform integrity checks
- initiate restore sequence
- surface recoverable vs non-recoverable failures

### SaveSlotMetadata
Fields:
- slot id
- display name
- build version
- schema version
- timestamp
- scenario id
- campaign id
- playtime
- corruption status
- last successful restore hash

### WorldStateSerializer
Responsibilities:
- serialize world-instance deltas only
- avoid duplication of source prefab / seed content
- write compact delta payloads
- feed restore service

### DeterministicRestoreService
Responsibilities:
- rebuild encounter from seed
- apply runtime deltas in stable order
- validate missing content references
- report restore drift

## Serialization rules

- Prefer stable ids over raw pointers or transient memory references.
- Save authored content references by id/path.
- Save dynamic runtime changes as deltas.
- Store order-sensitive reconstruction lists where dependency matters.
- Include schema version at every domain root.
- Separate optional cosmetic state from gameplay-critical state.

## Ordered save sequence

1. freeze critical mutation points
2. flush mission/economy pending writes
3. serialize rig and inventory
4. serialize session and ship state
5. serialize world-instance deltas
6. write metadata
7. finalize slot
8. release freeze

## Ordered restore sequence

1. read slot metadata
2. validate versions
3. load scenario and authored content
4. inject deterministic seed
5. rebuild baseline encounter
6. restore rig/session state
7. apply world-instance deltas
8. restore mission/economy/faction state
9. validate post-restore integrity
10. release player control

## Required save payload shapes

### RigState
- oxygen
- power
- suit integrity
- current movement mode
- current location transform or logical location id
- equipped tool ids
- quick slot mapping

### InventoryState
- item stacks
- mission items
- capacity modifiers
- container bindings

### ShipState
- subsystem statuses
- damage states
- door/airlock states
- power routing summary
- atmosphere state summary

### WorldDeltaState
- detached assembly nodes
- repaired nodes
- destroyed nodes
- hazard nodes
- depleted loot nodes
- spawned loose salvage actors
- mission interaction flags

## Versioning requirements

Every save must include:
- engine build version
- gameplay schema version
- content manifest version if available
- migration notes or compatibility flags

Migration must support:
- additive fields
- deprecated fields with fallbacks
- missing optional domains
- hard failure on incompatible critical graph references

## Failure model

### Recoverable failures
- missing optional cosmetic payload
- stale UI state payload
- deprecated non-critical analytics data

### Non-recoverable failures
- corrupted slot header
- missing required scenario content
- invalid deterministic seed data
- unresolved critical assembly reference

## Runtime debug requirements

- create named checkpoint
- list slots with metadata
- inspect serialized domain summaries
- force restore drift validation
- compare active state vs save state
- export readable save diff report

## Telemetry events

- save_requested
- save_started
- save_completed
- save_failed
- load_requested
- load_completed
- load_failed
- restore_drift_detected
- migration_applied

## Definition of done

Save/load is ready when:
- the player can save during or after salvage
- detached/repaired builder nodes restore correctly
- mission progress persists
- hazards persist
- rig vitals and inventory restore exactly
- version metadata is written and readable
