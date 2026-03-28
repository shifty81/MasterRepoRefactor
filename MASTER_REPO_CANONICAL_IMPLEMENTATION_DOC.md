# Master Repo Canonical Implementation Doc

_Last updated: 2026-03-28_

## 1. Project identity

**Master Repo** is the umbrella project.

It contains three tightly connected layers:

1. **Atlas Suite** — the user-facing WPF/editor/tooling shell
2. **Engine** — the reusable engine/runtime foundation
3. **NovaForge** — the flagship game project built on top of the engine

The project is not only a game. It is a combined:
- engine
- editor/IDE
- AI-assisted development environment
- playable runtime/game

## 2. Locked project rules

These are canonical and should be treated as standards.

### Naming and terminology
- The WPF layer that connects project systems is called **Atlas Suite**.
- Avoid using `MasterRepo.exe` as the user-facing executable name.
- The player suit + backpack assembly is called a **rig** in-game.

### UI / editor direction
- No ImGui as the project-facing UI path.
- Project-facing editor and runtime UI should remain custom.
- Runtime/player UI must stay separate from editor/debug UI.

### World / progression direction
- The project direction is **hybrid voxel + low-poly**.
- Voxels define structural mass, damage, mining, repair, and PCG state.
- Low-poly assets define readability, silhouette, interactable detail, and visual upgrade language.
- Seasons should be configurable on both client and server, but generally enforced server-side.
- Default target season length is about **6 months**.

### Architectural rules
- `Engine/` remains generic enough to support multiple products.
- Project-specific gameplay belongs under `Runtime/` and `Projects/`.
- Arbiter must execute through validated command gateways, not raw unrestricted engine mutation.
- Gameplay-critical JSON/data should be treated as documented contracts.

## 3. Current architectural state

The repo already has strong structural coverage across the major domains.

### Core
Owns:
- serialization
- deterministic seed logic
- versioning
- jobs / async / tasking
- events / messaging
- profiling / telemetry / crash reporting
- shared utilities

### Engine
Owns:
- rendering
- physics
- scene systems
- input
- networking substrate
- animation
- audio
- voxel-capable runtime services

### Editor / Atlas Suite direction
Owns:
- project browser
- viewport workflows
- builder editing
- PCG editing
- scene/prefab authoring
- AI-assisted tasking and review
- debug overlays and tooling panels

### AI / Arbiter
Owns:
- orchestration
- intent routing
- memory and context
- workflow planning
- knowledge ingestion/query
- multi-agent coordination
- validation and regression support

### Tools / Agents
Own:
- build automation
- repo insight
- doc generation
- compliance checks
- code/refactor/debug/editor/PCG specialized actions

### PCG
Owns:
- deterministic generation
- structure grammar
- wreck/ruin/site generation
- universe and encounter layout
- faction style propagation
- variation rules

### Config / schemas
Own:
- model configs
- builder/editor/engine/server configs
- gameplay definitions
- scenes
- parts
- ships
- prefabs
- recipes
- universe/faction data

## 4. Project phase

The project is now in:

# Pre-Vertical-Slice Integration Phase

This means:
- the high-level architecture is strong
- the direction is mostly locked
- many systems exist or are scaffolded
- the next critical work is to connect them into a playable, testable runtime loop

The main risk now is over-design without integrating.

## 5. Primary next-phase objective

Build a real playable vertical slice that proves the runtime stack.

### Target loop
Boot into a controlled scenario and allow the player to:
1. spawn in a starter ship interior
2. inspect rig and equipment
3. cycle an airlock
4. EVA with tether active
5. travel to a nearby wreck/derelict
6. scan and salvage one required component
7. survive at least one hazard
8. repair one subsystem or mission-critical target
9. return to ship
10. complete mission
11. receive mission/economy/faction outcome
12. save and reload with state preserved

If this loop works end-to-end, the repo becomes a real integrated foundation rather than an architectural shell.

## 6. Vertical slice implementation order

### Phase A — Runtime foundation
Purpose: boot, spawn, controlled scenario loading.

Deliver:
- `Runtime/Gameplay/VerticalSliceGameMode`
- `Runtime/Session/SessionBootstrap`
- `Runtime/Player/RigController`
- `Runtime/Scene/StarterScenarioLoader`
- `Projects/NovaForge/Scenes/vertical_slice_scene.json`
- `Projects/NovaForge/Prefabs/vertical_slice_starter_ship.json`

Required state:
- one starter ship interior
- one nearby salvage target or wreck
- one mission objective
- one repairable subsystem
- one extraction return point

### Phase B — Builder + Salvage loop
Purpose: first core gameplay pillar.

Player flow:
- move inside ship
- airlock transition
- EVA
- tether connection
- wreck scan
- cut/detach salvageable component
- collect materials or part
- return to ship

Key runtime contracts:
- `IRigLifeSupportSource`
- `ISalvageTarget`
- `IDetachableAssembly`
- `IRepairableSubsystem`

Minimal tools:
- cutter
- scanner
- tether tool
- repair tool
- cargo interface

### Phase C — Mission + Economy + Faction loop
Purpose: attach purpose, reward, progression.

Slice missions:
- recover black box
- restore relay
- retrieve regulator
- scan hazard zone and return

Small starting economy:
- credits
- scrap metal
- circuitry
- oxygen tanks
- repair kits

Faction slice:
- faction ID
- standing delta
- mission availability tags

### Phase D — Combat + Repair + Fire/Breach
Purpose: add failure states and environmental tension.

Initial hazards:
- hull breach
- electrical fire

Optional:
- hostile maintenance drone

Repair loop must support:
- detection
- diagnosis
- required part/tool check
- repair action
- restored ship/system state propagation

### Phase E — Save/Load + persistence
Purpose: lock the slice as a reusable runtime foundation.

Persist at minimum:
- rig state
- inventory
- equipped tools
- mission progress
- faction standing
- ship subsystem damage
- airlock state
- wreck state
- detached nodes
- encounter/world seed plus state deltas

## 7. Recommended runtime scaffold layout

```text
Runtime/
├── Gameplay/
│   ├── VerticalSliceGameMode.h/.cpp
│   ├── VerticalSliceState.h/.cpp
│   ├── VerticalSliceRules.h/.cpp
│   └── GameplayBootstrap.h/.cpp
│
├── Session/
│   ├── SessionBootstrap.h/.cpp
│   ├── SessionFlowController.h/.cpp
│   └── CheckpointService.h/.cpp
│
├── Player/
│   ├── RigController.h/.cpp
│   ├── RigVitalsComponent.h/.cpp
│   ├── RigEquipmentComponent.h/.cpp
│   ├── RigInventoryComponent.h/.cpp
│   ├── RigMovementZeroGComponent.h/.cpp
│   └── RigInteractionComponent.h/.cpp
│
├── BuilderRuntime/
│   ├── AssemblyRuntimeComponent.h/.cpp
│   ├── SnapGraphRuntime.h/.cpp
│   ├── DetachRuntimeService.h/.cpp
│   └── StructuralIntegrityRuntime.h/.cpp
│
├── Equipment/
│   ├── ToolItemDef.h/.cpp
│   ├── CutterToolRuntime.h/.cpp
│   ├── ScannerToolRuntime.h/.cpp
│   ├── RepairToolRuntime.h/.cpp
│   └── TetherToolRuntime.h/.cpp
│
├── Inventory/
│   ├── InventoryComponent.h/.cpp
│   ├── CargoContainerComponent.h/.cpp
│   ├── ItemStack.h
│   └── LootResolver.h/.cpp
│
├── Crafting/
│   ├── PortableAssemblerRuntime.h/.cpp
│   ├── RecipeResolver.h/.cpp
│   └── CraftingQueueRuntime.h/.cpp
│
├── Damage/
│   ├── DamageableComponent.h/.cpp
│   ├── BreachComponent.h/.cpp
│   ├── FirePropagationComponent.h/.cpp
│   └── RepairStateComponent.h/.cpp
│
├── Combat/
│   ├── DroneEnemyController.h/.cpp
│   ├── HitResolver.h/.cpp
│   └── ThreatEncounterRuntime.h/.cpp
│
├── Hazards/
│   ├── AtmosphereVolume.h/.cpp
│   ├── OxygenSimulation.h/.cpp
│   ├── PressureLeakRuntime.h/.cpp
│   └── HazardAlertService.h/.cpp
│
├── Quest/
│   ├── MissionRuntimeComponent.h/.cpp
│   ├── ObjectiveTracker.h/.cpp
│   └── MissionRewardResolver.h/.cpp
│
├── Economy/
│   ├── WalletComponent.h/.cpp
│   ├── EconomyLedger.h/.cpp
│   └── SalvageValueResolver.h/.cpp
│
├── Faction/
│   ├── FactionStandingComponent.h/.cpp
│   ├── FactionReactionResolver.h/.cpp
│   └── ContractIssuerResolver.h/.cpp
│
├── SaveLoad/
│   ├── SaveCoordinator.h/.cpp
│   ├── SaveMappers/
│   ├── WorldStateSerializer.h/.cpp
│   └── DeterministicRestoreService.h/.cpp
│
└── UI/
    ├── HudRuntimeController.h/.cpp
    ├── TabRigMenuController.h/.cpp
    ├── AirlockPanelController.h/.cpp
    ├── MissionPanelController.h/.cpp
    └── SalvageReticleController.h/.cpp
```

## 8. Atlas Suite integration plan

Atlas Suite should host distinct modes rather than blending editor and gameplay concepts together.

### Recommended top-level modes
- Project mode
- Scene / Prefab mode
- Builder mode
- PCG mode
- Runtime Debug mode
- Arbiter mode

### Immediate focus: Runtime Debug mode
This mode should accelerate vertical slice testing.

Recommended panels:
- session boot config
- spawn / checkpoint loader
- mission override panel
- faction standing debugger
- inventory injector
- salvage target inspector
- subsystem damage toggles
- atmosphere / fire / breach controls
- save/load inspector
- deterministic seed view

## 9. Arbiter → Engine execution model

Arbiter should not directly mutate engine/runtime systems through unrestricted calls.

Use a validated action pipeline.

```text
User / Atlas Suite / Web UI
            │
            ▼
      ArbiterOrchestrator
            │
            ▼
        Intent Router
            │
   ┌────────┼────────┐
   ▼        ▼        ▼
Knowledge  Planning  Execution Request
Query      Graph     Builder
                     │
                     ▼
             Validated Action Plan
                     │
                     ▼
               Tool / Agent Bus
                     │
     ┌───────────────┼────────────────┐
     ▼               ▼                ▼
 EditorAgent      CodeAgent       PCGAgent
     │               │                │
     └──────► Engine Command Gateway ◄┘
                         │
                         ▼
               Runtime / Editor Services
```

### Arbiter layers

#### Layer 1 — conversational intelligence
- intent recognition
- memory/context use
- explanation
- planning support
- schema lookup

#### Layer 2 — action planning
- structured task plan
- permission determination
- dependency requirements
- rollback/checkpoint generation
- validation path

#### Layer 3 — execution gateway
Converts AI intent into explicit commands only.

#### Layer 4 — result capture
- success/failure
- diffs
- logs
- reports
- generated assets
- test outcomes

## 10. Engine command gateway specification

Arbiter needs a strict command interface.

### Editor command family
- `OpenProject`
- `OpenScene`
- `FocusActor`
- `CreatePrefab`
- `CreateBuilderAssembly`
- `GenerateMaterialStub`
- `RunRuntimePreview`
- `ToggleDebugOverlay`

### Runtime debug command family
- `SpawnRigAt`
- `GiveItem`
- `SetMissionState`
- `DamageSubsystem`
- `TriggerBreach`
- `IgniteNode`
- `CompleteObjective`
- `SaveCheckpoint`
- `LoadCheckpoint`

### PCG command family
- `GenerateSector`
- `GenerateWreck`
- `ValidateSeed`
- `RebuildEncounter`
- `ExportPCGReport`

### Build/test command family
- `CompileModule`
- `RunUnitTests`
- `RunIntegrationSlice`
- `RunComplianceScan`
- `GenerateSchemaDocs`

### Every command should contain
- command ID
- origin
- target subsystem
- parameters
- dry-run flag
- validation rules
- rollback token
- telemetry tag

## 11. Builder ↔ voxel ↔ low-poly propagation model

This is a canonical project rule.

### Voxels own
- structural mass
- hull volume
- destruction state
- mining depletion
- repair fill state
- pressure containment
- durability/integrity substrate

### Builder graph owns
- modules
- snap rules
- sockets
- subsystem connectivity
- functional tags
- room/interior logic
- upgrade eligibility

### Low-poly layer owns
- visible silhouettes
- panels
- pipes/conduits
- terminals/displays
- readable attachments
- tier expression
- exposed damage dressing

### Upgrade propagation chain
```text
Functional upgrade installed
        │
        ▼
Subsystem stats change
        │
        ▼
Builder graph tags updated
        │
        ├── PCG style propagation updates dressing/layout detail
        ├── low-poly detail set swaps to higher-tier visuals
        └── voxel metadata updates if durability/resistance should change
```

### Example
Upgrading a reactor can:
- increase power budget
- unlock additional support modules
- update conduit/room dressing choices
- change internal/external visual language
- alter thermal or durability metadata on associated structures

## 12. Rig system target

The game should remain first person.

### Rig requirements
- always first person
- visible body when looking down
- visible feet movement/body awareness
- animated hands, wrists, forearms, fingers
- idle motion
- zero-G locomotion
- tether awareness
- tool socket system
- later mech compatibility via control transfer

### Rig component split
- `RigViewComponent`
- `RigBodyAwarenessComponent`
- `RigHandPoseComponent`
- `RigVitalsComponent`
- `RigEquipmentComponent`
- `RigLocomotionComponent`
- `RigInteractionComponent`

### Runtime rig menu (TAB)
Should remain in-game only and support:
- equipment
- inventory
- portable crafting if assembler installed
- rig vitals
- quick repair materials
- mission items

## 13. Save/load architecture

Use a coordinator model rather than several disconnected save concepts.

### Recommended structure
- `Runtime/SaveLoad/SaveCoordinator`
- `Runtime/Save/DomainModels`
- `Runtime/SaveGame/ProfileState`
- `Runtime/SaveLoad/Mappers`

### Persistence domains

#### ProfileState
- user settings
- unlocked cosmetics/account-level data

#### CampaignState
- season record
- long-term faction progression
- meta economy state

#### SessionState
- current ship
- rig state
- current inventory
- current mission progression

#### WorldState
- encounter seed
- scene seed
- wreck modifications
- breaches
- fire state
- loot depletion
- subsystem status

### Determinism rule
For PCG-heavy world states, prefer:
- world seed
- encounter seed
- explicit state deltas

over serializing giant reconstructed blobs when the world can be reproduced deterministically.

## 14. Networking stance for this phase

Networking-aware design should remain in mind, but multiplayer should not lead the first vertical slice.

### Current recommendation
Build the slice as:
- authoritative single-session runtime
- replication-aware state shapes
- serializer-friendly event flows
- no hard multiplayer dependency for first slice delivery

This helps avoid later rework while keeping scope contained.

## 15. Documentation tasks that should happen alongside implementation

Add the following docs as canonical runtime references:
- `Docs/Runtime/VERTICAL_SLICE.md`
- `Docs/Runtime/RIG_SYSTEM.md`
- `Docs/Runtime/SALVAGE_LOOP.md`
- `Docs/Runtime/MISSION_ECONOMY_FACTION.md`
- `Docs/Runtime/DAMAGE_REPAIR_BREACH.md`
- `Docs/Runtime/SAVELOAD_CONTRACTS.md`
- `Docs/AI/ARBITER_EXECUTION_GATEWAY.md`
- `Docs/Editor/ATLAS_SUITE_RUNTIME_DEBUG.md`

Also continue using:
- schema doc generation
- compliance scanning
- per-system docs updates whenever contracts change

## 16. Concrete sprint order

### Sprint 1
- session bootstrap
- starter scene
- rig spawn
- interior movement
- airlock state machine
- EVA transition
- tether basics

### Sprint 2
- salvage target interaction
- detach/cut flow
- inventory pickup
- cargo return
- mission objective completion hook

### Sprint 3
- repairable subsystem
- breach simulation
- oxygen drain
- repair flow
- restored system state propagation

### Sprint 4
- mission rewards
- wallet
- faction standing updates
- debrief screen
- save/load checkpoint flow

### Sprint 5
- Atlas Suite runtime debug mode
- Arbiter execution gateway
- command bus
- doc/compliance automation hooks

### Sprint 6
- optional hostile drone layer
- polish
- telemetry
- deterministic replay validation
- integration testing

## 17. Definition of done for the first true slice

The first integrated slice is done when the following all work in sequence:
- launch Atlas Suite or the runtime
- load the vertical slice scenario
- spawn in starter ship interior
- inspect rig/loadout
- cycle the airlock
- EVA to wreck
- scan and salvage one needed component
- survive at least one hazard
- repair one system or mission-critical target
- return and complete mission
- receive reward and faction update
- save
- reload and confirm world state persists accurately

## 18. Immediate implementation priority

The correct priority is:
1. runtime foundation
2. salvage loop
3. mission/economy/faction loop
4. damage/repair/breach loop
5. persistence
6. Atlas Suite runtime debug integration
7. Arbiter execution gateway

Avoid adding broad new systems until this loop exists and is stable.

## 19. Summary

The project already has the architecture needed to become a serious integrated engine/editor/runtime platform.

The next success condition is no longer more planning. It is proving one playable loop that joins:
- Core
- Engine
- Runtime
- PCG
- Builder
- Atlas Suite
- Arbiter
- Save/load

This document should act as the canonical implementation direction for the next development phase.
