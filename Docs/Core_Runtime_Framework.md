# Core Runtime Framework

See also:
- [Compliance Rules](Compliance_Rules.md)
- [Implementation Roadmap](Implementation_Roadmap.md)
- [Global State Input Interaction](systems/Global_State_Input_Interaction.md)

## Purpose

Defines startup order, ownership boundaries, config hierarchy, event routing, save orchestration, and validation authority.

## Runtime layering

```text
Core
 -> Runtime Services
   -> Domain Systems
     -> Presentation and Tooling
```

## Core subsystems

- `UCoreRuntimeSubsystem`
- `UConfigSubsystem`
- `ULoggingSubsystem`
- `UEventBusSubsystem`
- `USaveGameSubsystem`
- `UComplianceValidationSubsystem`

## Startup order

```text
1. Config
2. Logging
3. Event Bus
4. Save System
5. Compliance Validation
6. State / Input / Interaction
7. Runtime Assembly / Streaming
8. Gameplay Systems
9. UI / Debug
10. Arbiter / Tooling
```

## Ownership rules

- Core owns config, logging, events, persistence orchestration, compliance.
- Runtime services own transitions, input routing, assembly, streaming, mission orchestration.
- Domain systems own local behavior and actor state.
- Tooling owns authoring, generation, and validation UI.

## Save fragment rule

Subsystems contribute save fragments; the save subsystem orchestrates serialization.

## Logging categories

Core, Config, Input, Interaction, Transition, Character, Rig, Ship, Mech, EVA, Salvage, Derelict, Progression, Mission, Sector, Titan, Tooling, Blender, SaveLoad, Validation.
