# Arbiter Command Gateway — Deep Expansion

## Purpose

The command gateway is the only approved path for Arbiter-driven mutations of editor/runtime state.
Arbiter may reason broadly, but execution must be narrowed into validated, auditable commands.

## Non-negotiable rules

- Arbiter never directly mutates runtime or editor objects.
- Every mutating action becomes an explicit command.
- Commands must be validateable before execution.
- Commands must be loggable and attributable.
- Commands should support dry-run where practical.
- Unsafe commands require explicit capability tags.
- Results must flow back as structured execution reports.

## High-level flow

```text
User / Atlas Suite / Web UI
            │
            ▼
      ArbiterOrchestrator
            │
            ▼
        Intent Router
            │
            ▼
      Action Plan Builder
            │
            ▼
     Command Gateway Validator
            │
            ▼
      Command Dispatcher
            │
   ┌────────┼─────────┬──────────┐
   ▼        ▼         ▼          ▼
 Editor   Runtime     PCG      Tools/CI
 Service  Service   Service      Service
```

## Command envelope

Every command should include:

- `CommandId`
- `CorrelationId`
- `Origin`
- `RequestedBy`
- `TargetSubsystem`
- `Verb`
- `Parameters`
- `DryRun`
- `CapabilityTags[]`
- `ValidationRules[]`
- `RollbackToken`
- `Timestamp`
- `ExpectedArtifacts[]`

## Command families

### Runtime Debug Commands
- SpawnRigAt
- GiveItem
- SetMissionState
- TriggerBreach
- IgniteFire
- FaultSubsystem
- RepairSubsystem
- SaveCheckpoint
- LoadCheckpoint
- ToggleTetherFailover

### Builder/Salvage Commands
- MaterializeAssembly
- DetachNode
- RepairNode
- InspectSnapGraph
- ExportAssemblyDelta
- InjectHazardAtNode
- OverrideLootTable
- MarkNodeMissionCritical

### Save/Load Commands
- CreateSaveSlot
- CreateCheckpoint
- ListSaveSlots
- ValidateRestore
- ExportSaveDiff
- MigrateSaveSlot

### Documentation/Tooling Commands
- GenerateSchemaDocs
- RunComplianceScan
- CreateSpecStub
- OpenRuntimeDebugPanel

## Validation layers

### Static validation
- schema completeness
- parameter type validation
- allowed target subsystem
- required capability tags

### Context validation
- active scene loaded
- target node exists
- mission state allows mutation
- user/session permission level allows action

### Safety validation
- cannot break protected content in unsafe mode
- cannot overwrite save slots unless allowed
- cannot detach hard-locked mission nodes without override capability

## Result envelope

Every command returns structured result data:

- `CommandId`
- `Status`
- `Warnings[]`
- `Errors[]`
- `Artifacts[]`
- `StateChanges[]`
- `TelemetryEvents[]`
- `DurationMs`
- `RollbackAvailable`

## Capability model

Suggested capability tags:
- `runtime.debug`
- `runtime.hazard`
- `runtime.save`
- `builder.inspect`
- `builder.mutate`
- `mission.override`
- `docs.generate`
- `compliance.scan`

## Audit / traceability

Each executed command should be recorded with:
- who initiated it
- what plan generated it
- what validation ran
- what changed
- what artifacts resulted
- whether rollback was available or used

## Definition of done

The gateway is ready when Arbiter can:
- request runtime debug mutations through command objects
- inspect builder assemblies safely
- request save/load operations through explicit commands
- generate docs/compliance actions without bypassing validation
- receive structured execution reports for every action
