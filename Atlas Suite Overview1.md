


the Atlas Suite lets  plan and develop it  and  what it does

Oh this is where things get really exciting—because Atlas Suite is the backbone of your entire ecosystem. If we get this right, everything else (engine, editor, AI, game runtime) becomes dramatically easier to build, debug, and scale.

Let’s design this like a AAA-grade internal platform, not just a launcher.

🚀 Atlas Suite — Master Plan
Purpose:
Atlas Suite is the central command layer that connects:

Engine (runtime)

Editor (content creation)

AI (Arbiter)

Tooling (build, sync, validation)

Servers (optional backend/web access)

Think:
👉 Unreal Editor + Visual Studio + GitHub Desktop + AI Copilot + DevOps dashboard
👉 All in one cohesive environment tailored to NovaForge

🧠 Core Philosophy
Atlas Suite should be:

Modular → everything is a panel/module

AI-first → Arbiter is deeply integrated everywhere

Data-aware → understands your repo structure + schemas

Workflow-driven → guides development, not just tools

Offline-first capable → but enhanced with cloud sync

🧩 Core System Architecture
1. 🧱 Shell (WPF Application)
This is the main executable:

AtlasSuite.exe

Responsibilities:
Window + layout system

Panel docking (like Unreal / Visual Studio)

Plugin/module loading

Theme + UI framework (custom, no ImGui per your rule)

2. 🧠 Arbiter AI Core (Integrated Brain)
This is HUGE for your vision.

What it does:
Reads entire repo (code + assets + schemas)

Generates:

Code

Systems

Docs

Fixes

Understands:

Voxel system

Low-poly modular system

Game rules

Acts as:

Assistant

Validator

Automation agent

Modes:
Chat Mode (like this)

Action Mode (executes tasks)

Audit Mode (scans repo)

Generate Mode (builds systems)

🗂️ 3. Workspace System (Project Awareness)
Atlas Suite should “understand” your project.

Features:
Repo Map (visual graph)

File indexing (AI-readable)

Schema registry (Arbiter-readable)

Dependency tracking

🛠️ 4. Tooling Layer (DevOps Inside the App)
Includes:
🔹 Build System
Compile engine/editor

Package game

Hot reload

🔹 Git + Archive System
GitHub integration

Google Drive sync (your idea 👇)

Asset recovery system

👉 YES — your idea is solid:

Git = code

Google Drive = assets + gitignored + archives

Atlas Suite syncs both

🎨 5. Editor Integration Layer
Atlas Suite launches and controls:

Voxel Editor

Modular Asset Editor

Character Editor

Ship Builder

PCG Designer

👉 These are tools inside the ecosystem, not separate apps

🧪 6. Runtime Debug Layer (THIS IS HUGE)
You wanted:

“gameplay to be tested in executable”

This layer enables that.

Features:
Launch game in debug mode

Inject tools into runtime

Toggle systems:

Economy

Factions

Combat

Damage

Spawn anything

Simulate events

🌐 7. Web Server + Remote Access
You mentioned this—great call.

Capabilities:
Run local web server

Access Atlas Suite from:

Tablet

Phone

Browser

Features:
Remote dashboard

AI chat access

Build controls

Monitoring

🧱 8. Panel System (Core UX)
Everything = panels

Example Panels:
🧠 AI Chat Panel
Full-screen mode option

Context-aware (file, system, repo)

📁 Repo Explorer
Smart + AI-enhanced

🧬 System Graph
Visual relationships:

Systems

Entities

Dependencies

🧪 Debug Panel
Live runtime control

🏗️ Builder Panels
Ships

Structures

Characters

Mechs

⚙️ Feature Breakdown (What It DOES)
🔹 Development
Create systems via AI

Edit code inside IDE panel

Compile + run instantly

🔹 Content Creation
Build ships, rigs, mechs

Edit voxel structures

Generate PCG worlds

🔹 Testing
Launch runtime

Simulate gameplay systems

Debug live

🔹 AI Automation
“Build me a salvage system”

“Fix economy imbalance”

“Generate faction logic”

🔹 Validation
Detect missing systems

Enforce your Master Repo rules

Compare repo vs spec

🧠 Arbiter Superpowers (Game-Changer)
Atlas Suite becomes insane when Arbiter is fully integrated:

Example Commands:
“Create tiered reactor system”

“Generate voxel mining loop”

“Fix save/load bugs”

“Scan repo for missing combat logic”

It can:
Write code

Update files

Create assets

Generate docs

Run tests

🧬 Integration With YOUR Project Rules
This is important:

✔ No ImGui
→ WPF + custom rendering UI

✔ Hybrid Voxel + Low Poly
→ Editors support BOTH systems seamlessly

✔ Rig System (player suit)
→ Dedicated rig editor + upgrade system

✔ Seasonal System
→ Config panel in Atlas Suite (client/server control)

🗺️ Development Roadmap (REALISTIC BUILD ORDER)
🟢 Phase 1 — Foundation (CRITICAL)
WPF shell

Panel system

Basic file explorer

AI chat panel (Arbiter basic)

🟡 Phase 2 — Project Awareness
Repo indexing

Schema system

AI context awareness

🔵 Phase 3 — Tooling Integration
Build system

Git integration

Google Drive sync

🟣 Phase 4 — Editor Layer
Voxel editor integration

Modular asset editor

Character/rig editor

🔴 Phase 5 — Runtime + Debug
Launch game from Suite

Debug overlays

Simulation controls

⚫ Phase 6 — Advanced AI
Code generation pipelines

Auto-refactor system

Compliance scanner

Auto-doc generator

💥 What Makes Atlas Suite SPECIAL
This is not just a tool.

It becomes:

A game engine controller

A development AI

A live simulation environment

A content creation hub

A DevOps system

👉 Most studios have 5–10 tools to do this
👉 You’re building ONE unified system

🔥 Next Step (Highly Recommended)
We should now do one of these:

1. 👉 Generate FULL SYSTEM ARCHITECTURE DOC (AAA spec)
Class structures

Module interfaces

Data flow

Plugin system

2. 👉 Generate CODE SCAFFOLD
WPF shell

Panel system

AI integration hooks

3. 👉 Design UI/UX Layout (like Unreal Editor)
Docking system

Panel layout

Interaction flows

4. 👉 Arbiter Integration Spec (CRITICAL)
How it reads repo

How it modifies code safely

Action pipeline

If you want to move fast and actually build this, I’d go:

👉 “generate code scaffolding” next

and we start turning this into a real executable immediately.


what gaps do we have here?

Oh this is the right question—this is how you turn Atlas Suite from a cool idea into something that actually works at scale without collapsing later.

You’ve got a very strong vision already. What we need now is to identify the hidden gaps—the stuff that usually kills projects later if not designed now.

I’m going to break this into:

🚨 Critical Missing Systems (must solve early)

⚠️ Structural Risks (design weaknesses)

🧠 AI / Arbiter Gaps (biggest opportunity + danger)

🛠 Tooling Gaps

🎮 Gameplay Pipeline Gaps

🔒 Stability / Production Gaps

🧭 Final “Reality Check” Gaps

🚨 1. CRITICAL MISSING SYSTEMS
These are non-optional. Without these, Atlas Suite will eventually break.

🔹 A. Plugin / Module System (HUGE GAP)
Right now everything is “panels + features”
But you need:

👉 A true module system:
Load/unload tools dynamically

Version modules

Dependency resolution

Without this:
Atlas becomes monolithic

Impossible to maintain long-term

🔹 B. Command Bus / Action System
You said:

“AI can do things”

But how exactly?

You need a central execution layer:

Example:
AI → Request → Command Bus → Validated → Executed → Logged → Undoable
This enables:
Safe AI actions

Undo/redo

Logging

Multiplayer tooling later

👉 Without this = AI becomes dangerous and inconsistent

🔹 C. State Management System (Editor + Runtime)
You need a unified way to track:

Open files

Active systems

Runtime state

Editor state

Otherwise:
Debugging becomes chaos

AI loses context

Panels desync

🔹 D. Data Schema Authority (Arbiter Backbone)
You mentioned schemas—but not fully enforced.

You need:

Single source of truth for:

Items

rigs

ships

voxels

factions

Arbiter MUST rely on this
👉 Without this:

Systems drift apart

AI generates incompatible logic

⚠️ 2. STRUCTURAL RISKS
These won’t break immediately—but they will later.

🔸 A. Atlas Suite vs Engine Boundary
Right now it’s blurry.

You need strict separation:

Atlas Suite:
Tools

UI

AI

orchestration

Engine:
Rendering

physics

runtime simulation

👉 If not:

You’ll entangle editor + engine → nightmare

🔸 B. Panel System Complexity
Docking UI sounds simple… it’s not.

Missing:

Layout persistence

Panel lifecycle management

Memory control

🔸 C. Performance Strategy
No plan yet for:

Large repos

Massive assets

Real-time indexing

👉 This WILL hit hard later

🧠 3. ARBITER AI GAPS (BIGGEST ONE)
This is where most projects fail.

🔥 A. No “Action Safety Layer”
If AI can:

Modify files

Generate systems

You NEED:

Guardrails:
Dry run mode

Diff preview

Approval system

Rollback system

🔥 B. No Context Segmentation
Right now:

“AI reads everything”

That’s dangerous + inefficient.

You need:

Scoped context:

file-level

system-level

task-level

🔥 C. No Learning Pipeline
You said:

“learn from repo”

But missing:

Indexing pipeline

Embeddings / retrieval

Update strategy

🔥 D. No Task Planning System
AI needs to break work into steps:

Example:

Goal → Plan → Steps → Execute → Validate
Without this:

Outputs become messy

Hard to scale complexity

🛠 4. TOOLING GAPS
🔹 A. No Asset Pipeline Definition
You mentioned Google Drive sync (great)

But missing:

Asset versioning

Asset validation

Asset dependency tracking

🔹 B. No Build Profiles
You need:

Dev build

Test build

Release build

Dedicated server build

🔹 C. No Error/Log Aggregation System
You NEED:

Central logging panel

Error tracking

AI-assisted debugging

🎮 5. GAMEPLAY PIPELINE GAPS
This is a big one.

🔸 A. No “Gameplay Injection Layer”
You said:

test gameplay in executable

But missing:

A system that allows:
Injecting systems into runtime

Enabling/disabling features

Simulating scenarios

🔸 B. No System Lifecycle Definition
Every system needs:

Init → Update → Shutdown → Serialize
Not defined yet.

🔸 C. No Cross-System Communication Model
How do:

economy

factions

combat

PCG

talk to each other?

👉 Needs event/messaging system

🔒 6. STABILITY / PRODUCTION GAPS
🔹 A. No Versioning Strategy
For:

systems

assets

schemas

🔹 B. No Backup / Recovery System (beyond idea)
Needs:

automated snapshots

rollback points

🔹 C. No Testing Framework
You NEED:

Unit tests

Simulation tests

AI validation tests

🔹 D. No Permissions System (for future multi-user)
You mentioned collaboration → missing:

roles

access control

edit locks

🧭 7. FINAL REALITY CHECK GAPS
These are the “make or break long-term” ones.

💥 1. No Defined “Vertical Slice Pipeline”
You need a way to go:

Idea → System → Assets → Runtime → Test → Iterate
Atlas Suite should GUIDE this.

💥 2. No “Golden Path Workflow”
New user (you in 3 months) should be able to:

Open Atlas

Load project

Ask AI for system

Run it

Test it

Right now → not fully defined

💥 3. No “Failure Handling Philosophy”
What happens when:

AI breaks something

build fails

asset corrupts

🧠 THE BIGGEST GAP (TL;DR)
If I had to pick ONE:

👉 You don’t yet have a SAFE EXECUTION MODEL for AI + tools

Fix that, and everything becomes stable.

✅ What You Actually Have (Strong)
You’re VERY solid on:

Vision

System scope

Integration mindset

Hybrid voxel + modular pipeline

AI-first approach

🔥 What We Should Do Next (Critical Move)
We lock down the core foundation layer:

👉 Next Step:
Design these 4 systems in detail:

Command Bus (AI + tool execution)

Module/Plugin System

Schema Authority System

Arbiter Task Pipeline

If you want, I can:

👉 Build the full architecture spec for these (AAA-level)
👉 OR generate code scaffolding for them immediately

Both paths move you from vision → real system fast.


do both

Absolutely — here’s both:

AAA-level architecture spec for the missing foundation systems

repo-ready code scaffolding plan for Atlas Suite so it can start becoming real immediately

Atlas Suite — Foundation Lockdown Pack
This covers the 4 highest-priority systems:

Command Bus

Module / Plugin System

Schema Authority System

Arbiter Task Pipeline

These are the pieces that turn Atlas Suite from “tool shell” into a safe development operating system for the whole project.

1. Command Bus — Architecture Spec
Purpose
The Command Bus is the single controlled execution path for all meaningful actions in Atlas Suite.

Nothing important should happen outside this path:

AI file edits

project generation

build actions

asset sync

runtime launch

schema updates

editor actions

recovery / restore operations

This gives you:

safety

validation

logging

rollback

permissions later

undo/redo

deterministic execution

Core Rule
Every meaningful action is represented as a command object.

Examples:

CreateFileCommand

ModifyFileCommand

RunBuildCommand

LaunchRuntimeCommand

SyncAssetsCommand

RegisterSchemaCommand

GenerateSystemCommand

Execution Flow
User / Arbiter / UI
        ↓
   Command Request
        ↓
  Command Bus Router
        ↓
Pre-Validation Layer
        ↓
 Safety / Policy Layer
        ↓
  Handler Resolution
        ↓
  Execution Transaction
        ↓
 Post-Validation Layer
        ↓
 Result + Log + Event
        ↓
 Undo Snapshot / Rollback Record
Required Subsystems
A. Command Registry
Maps command types to handlers.

B. Validator Pipeline
Checks:

schema compliance

repo path safety

file lock collisions

runtime state conflicts

missing dependencies

C. Policy Layer
Determines whether the command is allowed.
Later this supports:

role permissions

AI restrictions

dangerous operation escalation

environment gating

D. Execution Context
Provides:

active workspace

project root

loaded module state

current user / source

active branch

task correlation id

E. Transaction / Snapshot Layer
Before destructive ops:

record old file contents

capture metadata

store rollback token

F. Event Publisher
Emits:

command started

command succeeded

command failed

rollback available

follow-up action required

G. Audit Log
Persistent operation history:

command source

timestamp

scope

affected files

status

diffs

rollback token

Command Types
Safe Local Commands
Low risk:

open panel

refresh repo tree

read file

switch tab

Mutating Commands
Medium risk:

edit file

move file

delete temp files

modify schema

update config

Critical Commands
High risk:

bulk refactor

overwrite directories

asset recovery

runtime data migration

destructive cleanup

branch rewrite

These should support:

preview

approval gate

snapshot

rollback

Result Model
Every command should return a structured result.

public sealed class CommandResult
{
    public bool Success { get; init; }
    public string Message { get; init; } = "";
    public string CommandId { get; init; } = "";
    public string? RollbackId { get; init; }
    public IReadOnlyList<string> AffectedPaths { get; init; } = Array.Empty<string>();
    public IReadOnlyList<string> Warnings { get; init; } = Array.Empty<string>();
    public IReadOnlyList<DomainEvent> Events { get; init; } = Array.Empty<DomainEvent>();
}
Atlas-Specific Requirements
For your project, Command Bus must support:

Arbiter-generated work plans

repo-safe file operations

Google Drive asset sync actions

schema-backed game data generation

runtime test launch and instrumentation

compliance scanner actions

auto-doc generation actions

2. Module / Plugin System — Architecture Spec
Purpose
Atlas Suite cannot become one giant executable blob.
It needs to be a host shell with loadable modules.

This allows:

editor tools to remain isolated

Arbiter tools to evolve separately

optional systems to be enabled later

cleaner repo boundaries

faster refactors

Module Boundaries
Atlas Host
Owns:

window shell

panel framework

command bus

module loader

event hub

workspace context

theme/layout persistence

Modules
Provide:

panels

services

commands

schemas

menus

tools

workflows

Required Module Categories
Core Modules
Always loaded:

Shell

Workspace

Commanding

Logging

Settings

Arbiter Core

Schema Authority

Tool Modules
Optional but first-class:

Build Tools

Git Integration

Cloud Sync

Runtime Launcher

Asset Browser

Compliance Scanner

Auto Doc Generator

Editor Modules
Project-specific:

Voxel Editor

Modular Asset Editor

Rig Editor

Character Editor

Ship Builder

PCG Graph Editor

Module Contract
Each module should declare:

name

id

version

dependencies

startup priority

provided services

contributed panels

contributed commands

contributed schema providers

Module Lifecycle
Discover
→ Validate Manifest
→ Resolve Dependencies
→ Load Assembly
→ Register Services
→ Register Panels
→ Register Commands
→ Start
→ Active
→ Stop
→ Unload
Module Safety Rules
A module must not:

directly mutate global state without service access

bypass command bus for meaningful writes

write into arbitrary repo locations

register duplicate command ids

shadow core schema authorities

Versioning
Each module gets:

semantic version

compatible host version range

compatible schema version range

This matters later when tools evolve faster than the engine.

Recommended Initial Modules
Core
Atlas.Shell

Atlas.Workspace

Atlas.Commanding

Atlas.Logging

Atlas.Schemas

Atlas.Arbiter

Tooling
Atlas.Build

Atlas.Git

Atlas.CloudSync

Atlas.Runtime

Atlas.DocGen

Atlas.Compliance

Editors
Atlas.Editor.Voxel

Atlas.Editor.Modular

Atlas.Editor.Rig

Atlas.Editor.Character

Atlas.Editor.PCG

3. Schema Authority System — Architecture Spec
Purpose
This is the truth layer.

Arbiter, tools, editor panels, runtime generators, and validators must all rely on the same authoritative data rules.

Without this, the project drifts:

AI generates invalid data

editors save incompatible definitions

runtime breaks on mismatched fields

docs stop matching reality

What Needs Authority
At minimum:

Items

Resource definitions

Factions

Missions

Structures

Voxels

Modular parts

Ships

Rigs

Mechs

NPC archetypes

Crafting recipes

Skill definitions

Damage types

Repair rules

Salvage data

Season configuration

Worldgen parameters

Schema Layers
A. Schema Definitions
Formal type rules.

B. Validation Rules
Required fields, allowed ranges, references, enum constraints.

C. Migration Rules
Upgrade old schema versions forward.

D. Registry
Central discoverable catalog.

E. Documentation Generator
Human-readable output from schemas.

F. Runtime Adapters
Translate schema objects into engine/runtime usable data.

Registry Structure
Schema Registry
 ├── domain/item
 ├── domain/faction
 ├── domain/rig
 ├── domain/ship
 ├── domain/voxel-material
 ├── domain/modular-part
 ├── domain/mission
 ├── domain/season-config
 └── domain/worldgen
Schema Versioning
Each schema must include:

SchemaId

Version

DisplayName

OwnerModule

MigrationChain

Example:

domain.rig v1

domain.rig v2

migration v1 → v2

Arbiter Dependency
Arbiter should never generate freeform game data without schema context.

Instead:

ask schema registry for target type

build from contract

validate against authority

emit only valid assets/config/data

Schema Validation Pipeline
Load Candidate Data
→ Parse
→ Schema Lookup
→ Structural Validation
→ Rule Validation
→ Reference Validation
→ Migration Check
→ Final Validated Object
Output Benefits
This system feeds:

editor forms

auto docs

compliance scanner

AI generation constraints

runtime loading

import/export

patch migrations

4. Arbiter Task Pipeline — Architecture Spec
Purpose
This is the AI execution brain model.

Arbiter should not go:
“user asked for feature → write files randomly”

It needs a structured pipeline.

Core Model
Intent
→ Scope
→ Plan
→ Validate Plan
→ Execute Step
→ Verify Result
→ Continue / Roll Back / Escalate
→ Summarize Outcome
Arbiter Modes
A. Chat Mode
Discussion only. No mutations.

B. Plan Mode
Produces step plan and target files.

C. Dry Run Mode
Generates proposed diffs without applying.

D. Execute Mode
Applies approved steps through command bus.

E. Audit Mode
Scans repo and reports mismatches.

F. Repair Mode
Attempts targeted fixes with validation.

Task Model
Each task should contain:

Task Id

Request source

Goal

Scope

Constraints

Referenced schemas

Candidate files

Planned steps

Execution status

Generated commands

Validation results

Rollback tokens

Step Types
read repo map

inspect schema

inspect existing code

generate design draft

generate diff

run validation

apply command

build/test

summarize

Hard Safety Rules
Arbiter must not:

bypass command bus

mass rewrite without scope

generate data without schema

alter unrelated files without justification

perform destructive actions silently

Validation Stages
Pre-plan validation
Is goal understood? Is scope clear enough?

Pre-execution validation
Are target files real? Are schemas available?

Post-step validation
Did the edit compile? Did the asset still validate?

Final validation
Does output match request and not break standards?

Atlas-Specific Arbiter Features
You want Arbiter to become the in-suite developer assistant. For that it needs:

repo map awareness

schema-awareness

module-awareness

command bus integration

diff previews

design + code dual mode

compliance checking

doc generation

runtime test launch hooks

Recommended Foundation Dependency Order
Build in this order:

Command Bus

Module Loader

Schema Authority

Arbiter Pipeline

logging + snapshots

build/runtime integration

cloud sync

higher-level editors

That gives you a real spine.

Repo-Ready Code Scaffolding
Now the second half: the actual structure to build.

Recommended Solution Layout
AtlasSuite/
├── src/
│   ├── AtlasSuite.Host/
│   ├── AtlasSuite.Shell/
│   ├── AtlasSuite.Core/
│   ├── AtlasSuite.Commanding/
│   ├── AtlasSuite.Modules/
│   ├── AtlasSuite.Schemas/
│   ├── AtlasSuite.Arbiter/
│   ├── AtlasSuite.Logging/
│   ├── AtlasSuite.Workspace/
│   ├── AtlasSuite.Runtime/
│   ├── AtlasSuite.Build/
│   ├── AtlasSuite.CloudSync/
│   ├── AtlasSuite.Compliance/
│   ├── AtlasSuite.DocGen/
│   ├── AtlasSuite.Editor.Voxel/
│   ├── AtlasSuite.Editor.Modular/
│   ├── AtlasSuite.Editor.Rig/
│   ├── AtlasSuite.Editor.Character/
│   └── AtlasSuite.Editor.PCG/
├── tests/
│   ├── AtlasSuite.Commanding.Tests/
│   ├── AtlasSuite.Modules.Tests/
│   ├── AtlasSuite.Schemas.Tests/
│   ├── AtlasSuite.Arbiter.Tests/
│   └── AtlasSuite.Integration.Tests/
└── docs/
Core Project Responsibilities
AtlasSuite.Host
App bootstrapper.

startup

DI container

module discovery

shell launch

AtlasSuite.Shell
WPF windowing and layout.

main window

docking host

panel lifecycle

theme/layout persistence

AtlasSuite.Core
Shared primitives.

result types

IDs

domain events

interfaces

app constants

AtlasSuite.Commanding
Command bus implementation.

commands

handlers

validators

policies

transactions

history

AtlasSuite.Modules
Plugin loader and module contracts.

manifests

dependency resolution

load/unload lifecycle

AtlasSuite.Schemas
Registry + validation + migration.

schema definitions

schema validator

migrations

schema docs

AtlasSuite.Arbiter
AI task pipeline.

task planner

task executor

context providers

dry run generator

command translator

AtlasSuite.Logging
Logs + audit trail.

event store

operation history

UI log feeds

AtlasSuite.Workspace
Project awareness.

repo map

project root

index

file inventory

workspace settings

Minimal Interfaces to Create First
Command Bus
public interface ICommand
{
    string CommandId { get; }
    string Name { get; }
}

public interface ICommandHandler<in TCommand> where TCommand : ICommand
{
    Task<CommandResult> HandleAsync(TCommand command, CommandExecutionContext context, CancellationToken ct);
}

public interface ICommandValidator<in TCommand> where TCommand : ICommand
{
    Task<ValidationResult> ValidateAsync(TCommand command, CommandExecutionContext context, CancellationToken ct);
}

public interface ICommandBus
{
    Task<CommandResult> ExecuteAsync(ICommand command, CommandExecutionContext context, CancellationToken ct = default);
}
Execution Context
public sealed class CommandExecutionContext
{
    public string WorkspaceRoot { get; init; } = "";
    public string Initiator { get; init; } = "";
    public string CorrelationId { get; init; } = Guid.NewGuid().ToString("N");
    public bool IsDryRun { get; init; }
    public IServiceProvider Services { get; init; } = default!;
}
Validation Result
public sealed class ValidationResult
{
    public bool IsValid { get; init; }
    public IReadOnlyList<string> Errors { get; init; } = Array.Empty<string>();
    public IReadOnlyList<string> Warnings { get; init; } = Array.Empty<string>();

    public static ValidationResult Success() => new() { IsValid = true };
    public static ValidationResult Failure(params string[] errors) =>
        new() { IsValid = false, Errors = errors };
}
Module Contract
public interface IAtlasModule
{
    AtlasModuleManifest Manifest { get; }
    Task InitializeAsync(IModuleContext context, CancellationToken ct);
    Task StartAsync(IModuleContext context, CancellationToken ct);
    Task StopAsync(IModuleContext context, CancellationToken ct);
}
public sealed class AtlasModuleManifest
{
    public string Id { get; init; } = "";
    public string Name { get; init; } = "";
    public string Version { get; init; } = "";
    public IReadOnlyList<string> Dependencies { get; init; } = Array.Empty<string>();
}
Schema Registry
public interface ISchemaDefinition
{
    string SchemaId { get; }
    int Version { get; }
    Type ClrType { get; }
}

public interface ISchemaRegistry
{
    void Register(ISchemaDefinition schema);
    ISchemaDefinition? Find(string schemaId, int? version = null);
    IReadOnlyList<ISchemaDefinition> GetAll();
}
public interface ISchemaValidator
{
    Task<ValidationResult> ValidateAsync(string schemaId, object instance, CancellationToken ct = default);
}
Arbiter Pipeline
public interface IArbiterTaskPlanner
{
    Task<ArbiterPlan> BuildPlanAsync(ArbiterRequest request, CancellationToken ct);
}

public interface IArbiterTaskExecutor
{
    Task<ArbiterExecutionResult> ExecuteAsync(ArbiterPlan plan, CancellationToken ct);
}
public sealed class ArbiterRequest
{
    public string Goal { get; init; } = "";
    public string Scope { get; init; } = "";
    public bool DryRun { get; init; }
    public IReadOnlyList<string> Constraints { get; init; } = Array.Empty<string>();
}
First Concrete Commands to Scaffold
These are the best starter commands:

File / Repo
ReadFileCommand

CreateFileCommand

ModifyFileCommand

MoveFileCommand

DeleteFileCommand

Workspace
RefreshWorkspaceIndexCommand

OpenProjectCommand

Build / Runtime
RunBuildCommand

LaunchRuntimeCommand

StopRuntimeCommand

Schemas
RegisterSchemaCommand

ValidateSchemaAssetCommand

Arbiter
CreateArbiterPlanCommand

ExecuteArbiterPlanCommand

PreviewArbiterDiffCommand

Tooling
RunComplianceScanCommand

GenerateDocsCommand

SyncCloudAssetsCommand

First Concrete Panels to Scaffold
These should exist very early:

1. Workspace Explorer Panel
file tree

indexed project view

filters

2. Arbiter Chat Panel
chat

task mode switch

dry run toggle

plan preview

3. Command Log Panel
all command history

statuses

errors

rollback availability

4. Schema Registry Panel
list schemas

versions

validation status

docs preview

5. Build / Runtime Panel
build buttons

runtime launch

test status

logs

6. Module Manager Panel
loaded modules

versions

dependency health

enable/disable

Example Command Bus Skeleton
public sealed class CommandBus : ICommandBus
{
    private readonly IServiceProvider _services;
    private readonly ICommandAuditLogger _auditLogger;

    public CommandBus(IServiceProvider services, ICommandAuditLogger auditLogger)
    {
        _services = services;
        _auditLogger = auditLogger;
    }

    public async Task<CommandResult> ExecuteAsync(
        ICommand command,
        CommandExecutionContext context,
        CancellationToken ct = default)
    {
        var commandType = command.GetType();

        var validatorType = typeof(ICommandValidator<>).MakeGenericType(commandType);
        var handlerType = typeof(ICommandHandler<>).MakeGenericType(commandType);

        var validators = _services.GetServices(validatorType).Cast<object>().ToArray();
        foreach (var validator in validators)
        {
            var validateMethod = validatorType.GetMethod("ValidateAsync")!;
            var validationTask = (Task<ValidationResult>)validateMethod.Invoke(validator, new object[] { command, context, ct })!;
            var result = await validationTask;
            if (!result.IsValid)
            {
                var failed = new CommandResult
                {
                    Success = false,
                    CommandId = command.CommandId,
                    Message = string.Join(Environment.NewLine, result.Errors),
                    Warnings = result.Warnings
                };

                await _auditLogger.RecordAsync(command, context, failed, ct);
                return failed;
            }
        }

        var handler = _services.GetRequiredService(handlerType);
        var handleMethod = handlerType.GetMethod("HandleAsync")!;
        var task = (Task<CommandResult>)handleMethod.Invoke(handler, new object[] { command, context, ct })!;
        var commandResult = await task;

        await _auditLogger.RecordAsync(command, context, commandResult, ct);
        return commandResult;
    }
}
Example Module Loader Skeleton
public interface IModuleLoader
{
    Task<IReadOnlyList<IAtlasModule>> DiscoverAndLoadAsync(string modulesPath, CancellationToken ct);
}
public sealed class ModuleLoader : IModuleLoader
{
    public async Task<IReadOnlyList<IAtlasModule>> DiscoverAndLoadAsync(string modulesPath, CancellationToken ct)
    {
        var modules = new List<IAtlasModule>();

        if (!Directory.Exists(modulesPath))
            return modules;

        foreach (var dll in Directory.EnumerateFiles(modulesPath, "*.dll", SearchOption.TopDirectoryOnly))
        {
            var assembly = Assembly.LoadFrom(dll);
            var moduleTypes = assembly.GetTypes()
                .Where(t => typeof(IAtlasModule).IsAssignableFrom(t) && !t.IsAbstract && !t.IsInterface);

            foreach (var type in moduleTypes)
            {
                if (Activator.CreateInstance(type) is IAtlasModule module)
                    modules.Add(module);
            }
        }

        return modules;
    }
}
Example Schema Registry Skeleton
public sealed class SchemaRegistry : ISchemaRegistry
{
    private readonly Dictionary<string, List<ISchemaDefinition>> _schemas = new();

    public void Register(ISchemaDefinition schema)
    {
        if (!_schemas.TryGetValue(schema.SchemaId, out var versions))
        {
            versions = new List<ISchemaDefinition>();
            _schemas[schema.SchemaId] = versions;
        }

        if (versions.Any(x => x.Version == schema.Version))
            throw new InvalidOperationException($"Schema already registered: {schema.SchemaId} v{schema.Version}");

        versions.Add(schema);
        versions.Sort((a, b) => a.Version.CompareTo(b.Version));
    }

    public ISchemaDefinition? Find(string schemaId, int? version = null)
    {
        if (!_schemas.TryGetValue(schemaId, out var versions))
            return null;

        return version is null
            ? versions.LastOrDefault()
            : versions.FirstOrDefault(x => x.Version == version.Value);
    }

    public IReadOnlyList<ISchemaDefinition> GetAll() =>
        _schemas.Values.SelectMany(x => x).ToArray();
}
Example Arbiter Plan Models
public sealed class ArbiterPlan
{
    public string PlanId { get; init; } = Guid.NewGuid().ToString("N");
    public string Goal { get; init; } = "";
    public string Scope { get; init; } = "";
    public bool DryRun { get; init; }
    public IReadOnlyList<ArbiterStep> Steps { get; init; } = Array.Empty<ArbiterStep>();
}
public sealed class ArbiterStep
{
    public int Order { get; init; }
    public string Kind { get; init; } = "";
    public string Description { get; init; } = "";
    public IReadOnlyList<string> TargetPaths { get; init; } = Array.Empty<string>();
}
public sealed class ArbiterExecutionResult
{
    public bool Success { get; init; }
    public IReadOnlyList<CommandResult> StepResults { get; init; } = Array.Empty<CommandResult>();
    public IReadOnlyList<string> Notes { get; init; } = Array.Empty<string>();
}
Immediate Build Order for Actual Implementation
Sprint 1 — Core Spine
AtlasSuite.Core

AtlasSuite.Commanding

AtlasSuite.Logging

AtlasSuite.Workspace

AtlasSuite.Host

AtlasSuite.Shell

Goal:

launch Atlas Suite

open shell

show workspace panel

execute test commands

display command log

Sprint 2 — Module Backbone
AtlasSuite.Modules

AtlasSuite.ModuleManagerPanel

module manifest validation

dependency resolution

startup ordering

Goal:

load modules safely

register panels and services

Sprint 3 — Schema Authority
AtlasSuite.Schemas

registry panel

JSON schema support or custom type rules

validation pipeline

migration hooks

Goal:

define authoritative game data contracts

Sprint 4 — Arbiter Safe Pipeline
AtlasSuite.Arbiter

task planner

dry-run output

command generation

scoped execution

Goal:

Arbiter can inspect, plan, preview, and apply through command bus only

Sprint 5 — Tooling & Runtime
build runner

runtime launcher

compliance scanner

doc generator

cloud sync service

Goal:

useful daily development suite

Biggest Remaining Gaps Even After This Pack
After these are in place, next missing systems will be:

layout persistence and advanced docking

repo indexer / semantic project map

diff viewer

rollback UI

asset manifest system

cloud sync resolver

runtime instrumentation bridge

test orchestration

user roles / permissions

multi-user collaboration

integrated editor surfaces for voxel/rig/PCG

These become much easier once this foundation exists.

Strong Recommendation
The smartest next move is to build these first actual source files:

ICommand.cs

ICommandBus.cs

CommandBus.cs

CommandResult.cs

CommandExecutionContext.cs

IAtlasModule.cs

AtlasModuleManifest.cs

ModuleLoader.cs

ISchemaDefinition.cs

ISchemaRegistry.cs

SchemaRegistry.cs

ArbiterRequest.cs

ArbiterPlan.cs

IArbiterTaskPlanner.cs

IArbiterTaskExecutor.cs

That gives you the first true backbone.

Next after that, create a simple WPF shell with:

left: workspace tree

center: Arbiter panel

bottom: command log

right: module/schema inspector

That would already feel like Atlas Suite has started existing.

I can do the next layer and generate a full repo folder/file scaffold with exact filenames and starter class contents.


any gaps in tooling  that need addressed as well? also Arbiter has been renamed in master repo to AtlasAI

Updated saved memory

Thought for 6s
Yes — there are still important tooling gaps to address, and the rename is locked in now: Arbiter → AtlasAI.

That rename actually helps, because it makes the stack read cleaner:

Atlas Suite = the WPF tooling shell / platform

AtlasAI = the integrated AI system inside it

Biggest tooling gaps still open
1. Tool orchestration layer
Right now we’ve defined commands and modules, but tooling still needs a higher-level coordinator.

You need a layer that answers:

which tool runs first

what prerequisites are required

what outputs feed the next tool

how failures are handled mid-pipeline

Example:

repo scan

schema validation

code generation

build

launch runtime

collect logs

summarize issues

Without orchestration, Atlas Suite becomes a box of disconnected tools.

2. Workspace indexer
AtlasAI cannot really function at a high level without a strong project index.

You still need:

repo tree cache

symbol/file relationships

schema-to-file mapping

module ownership mapping

asset manifest indexing

change detection

This is one of the biggest missing tooling pieces because it powers:

search

AI context

compliance scans

doc generation

dependency tracing

3. Diff / patch review tooling
If AtlasAI is going to generate or refactor code, you need first-class tooling for:

file diffs

patch previews

accept/reject at hunk level

rollback from prior state

compare generated output vs current implementation

Without this, AI-assisted editing is too risky.

4. Snapshot / recovery tooling
You already want archive behavior and strong recovery. The tooling side still needs:

pre-action snapshots

repo state restore points

restore selected files only

restore generated config only

restore ignored/cloud-backed content

compare current vs snapshot

This is especially important because you want cloud sync for assets and gitignored material.

5. Asset pipeline tooling
This is still underdefined.

You need tooling for:

asset manifest generation

asset dependency validation

missing asset detection

duplicate asset detection

naming compliance

import rules

archive indexing

cloud recovery mapping

Because your project uses both voxel and low-poly modular content, asset tooling has to understand both pipelines cleanly.

6. Build matrix tooling
You mentioned build/run tools, but not enough detail yet.

You should have tooling for:

engine build

editor build

Atlas Suite build

client build

server build

tools-only build

test build

packaging build

Also:

cached build profiles

build history

failed build diagnostics

one-click rebuild of affected layers only

7. Runtime instrumentation tooling
This is a major one.

You want to test systems from the executable, but tooling still needs:

live stat overlays

entity inspectors

economy/faction state views

damage/fire/breach simulation controls

mission debug injection

PCG seed replay

save/load test hooks

event stream viewer

Without this, runtime testing stays shallow.

8. Validation tooling stack
You’ve got the idea of compliance scanning, but it needs to be broader.

You need multiple validator classes:

repo structure validator

naming validator

schema validator

asset validator

code convention validator

config validator

cross-reference validator

broken link/path validator

AtlasAI should be able to call these directly and summarize results.

9. Documentation tooling
Still a gap.

You want Atlas Suite to help maintain project truth, so tooling should generate:

system docs

schema docs

repo maps

module docs

API/interface docs

missing-doc reports

stale-doc reports

This is especially useful for keeping the source pack aligned with the real repo.

10. Task queue / job tooling
Some tooling operations are bigger than a single command.

You need a jobs layer for:

long repo scans

large doc generation

asset reindexing

cloud sync

compliance scans

multi-step AtlasAI plans

That means:

queued jobs

progress reporting

cancel support

retry support

result summaries

11. External tool bridge
A big tooling gap.

Atlas Suite should eventually bridge to external tools in a clean way:

git

GitHub workflows

compiler/build tools

local scripts

asset processors

archive tools

cloud sync providers

optional IDE/editor integration

This needs a standard adapter layer, not ad hoc process launching everywhere.

12. Settings / profile tooling
This sounds small, but it matters a lot.

You need settings support for:

per-user settings

per-project settings

per-workspace settings

client/server seasonal configs

AtlasAI behavior modes

tool permissions

sync roots

archive paths

build targets

Without strong settings tooling, the suite gets messy fast.

13. Error intelligence tooling
AtlasAI will be much stronger if errors are normalized.

You need tooling that:

collects logs from all modules

categorizes errors

groups duplicate failures

links errors to files/modules/systems

suggests likely causes

tracks recurring failures

This becomes your internal “diagnostic brain.”

14. Test harness tooling
Still a very important gap.

You need tooling for:

unit test runs

schema test runs

integration test runs

content validation test runs

simulated gameplay test runs

regression packs

baseline comparison

This is how Atlas Suite moves from “smart editor shell” to real development platform.

15. Permission / safety tooling
Especially important for AtlasAI.

You need tooling controls for:

read-only mode

dry-run only mode

guarded write mode

full trusted mode

restricted path lists

protected files

confirmation thresholds for destructive actions

That gives AtlasAI safe boundaries.

The biggest tooling gaps, in priority order
If I had to rank them:

Workspace indexer

Diff / patch review

Validation tooling stack

Runtime instrumentation tooling

Snapshot / recovery tooling

Asset pipeline tooling

Task queue / job tooling

Documentation tooling

External tool bridge

Test harness tooling

Those are the big ones that still need deliberate design.

AtlasAI rename impact
Now that the rename is official, these naming shifts should happen everywhere in planning:

Arbiter Panel → AtlasAI Panel

ArbiterRequest → AtlasAIRequest

ArbiterPlan → AtlasAIPlan

IArbiterTaskPlanner → IAtlasAITaskPlanner

IArbiterTaskExecutor → IAtlasAITaskExecutor

AtlasSuite.Arbiter → AtlasSuite.AtlasAI

That should be treated as the canonical naming going forward.

One more hidden tooling gap
There is also a tool capability registry gap.

Atlas Suite should know:

what tools exist

what each tool can do

which commands each tool exposes

which modules own them

what input/output contracts they have

That lets AtlasAI intelligently pick tools instead of hardcoding assumptions.

Best next move
The smartest next step is to build the Tooling Architecture Pack for Atlas Suite with AtlasAI naming baked in:

Workspace Indexer

Diff/Patch System

Validation Stack

Snapshot/Recovery

Job Queue

External Tool Adapter

Runtime Instrumentation Bridge

That would close most of the real tooling holes in one pass.


what about blender as well? and the integration of it into tooling?


Thought for 9s
Yes — Blender should absolutely be part of the tooling plan, but as a connected DCC pipeline tool, not as the place where project truth lives.

The clean model is:

Atlas Suite = orchestration, validation, indexing, pipeline control

AtlasAI = planning, automation, generation, repair, validation assistance

Blender = mesh/rig/animation/material authoring and conversion

Engine/Editor = final runtime truth and in-engine validation

Blender is a strong fit here because it supports automation from the command line, can run in background mode for headless jobs, exposes a Python API for scripting and add-ons, and supports standard import/export pipelines like glTF and USD. 

Where Blender fits in your stack
Blender should handle:

low-poly mesh authoring

rig creation and animation prep

collision/helper object setup

socket / attach point authoring

LOD authoring

material slot preparation

export packaging for engine ingest

It should not be the authority for:

gameplay schema

item/faction/mission data

final runtime metadata contracts

project-wide dependency truth

That authority should still stay in Atlas Suite + schema registry. That separation keeps your repo stable.

Best integration model
1. External tool adapter
Atlas Suite should treat Blender as a registered external capability, not a random executable launch.

Blender integration should expose actions like:

Open asset in Blender

Export selected asset preset

Run headless conversion

Validate a .blend

Bake/export animations

Rebuild collision helpers

Generate socket metadata

Batch process a folder

This belongs in an External Tool Bridge plus a Blender Adapter Module.

Suggested module name:

AtlasSuite.Tooling.Blender

2. Blender add-on + Atlas-side adapter
The strongest setup is two-sided:

Atlas side

launches Blender

passes job payloads

receives results/logs

validates outputs

updates index

Blender side

custom add-on

standard export presets

naming validation

object tagging

metadata extraction

one-click “Export to Atlas”

Blender’s API and add-on system are designed for extension, which makes this a solid route. 

Tooling gaps specific to Blender integration
This is where the real missing pieces are.

A. No DCC pipeline contract yet
You need a formal definition for:

supported source formats

supported export targets

file naming rules

scale/orientation conventions

armature/bone naming conventions

socket marker conventions

collision mesh conventions

animation split conventions

material/export restrictions

Without this, Blender integration becomes inconsistent fast.

B. No asset metadata bridge
You need Atlas Suite to understand Blender-authored assets beyond “there is a file.”

You want metadata such as:

source .blend

exported outputs

skeleton used

animation clips included

sockets/helpers found

collision objects found

material slots

export preset version

last validation status

This should go into an asset manifest system.

C. No export preset governance
You do not want artists or future-you exporting with arbitrary settings.

You need locked presets for:

static mesh

skeletal mesh

animation-only

modular part

rig component

prop kit piece

ship interior piece

character clothing/gear piece

Given Blender’s exporter support and scripting hooks, Atlas Suite can enforce or trigger standardized exports rather than relying on manual setup. 

D. No headless batch pipeline yet
This is a major gap.

Because Blender supports command-line operation and background mode, Atlas Suite should be able to do jobs like:

re-export all modular ship parts

validate all skeleton assets

batch bake/convert

rebuild generated preview files

run nightly asset compliance scans

That’s one of the best reasons to integrate Blender deeply. 

E. No safe scripting policy yet
This matters a lot. Blender supports embedded and external Python, and Blender’s own docs call out scripting security risks. 

So Atlas Suite needs rules like:

only trusted add-ons

signed/approved internal scripts

no arbitrary script execution from imported .blend files

sandboxed batch jobs where possible

explicit trust mode for automation

This is a real tooling/safety gap.

F. No scene-authoring conventions for your project
For NovaForge-style production, you need Blender scene standards for:

collection organization

object prefixes

export collections

collision naming

socket empties

rig controls vs deform bones

proxy vs final mesh separation

modular snapping pivots

voxel-conversion marker objects where relevant

Blender’s collection system and export tooling can support disciplined scene organization, but you need to define your house rules. 

G. No round-trip workflow
You still need to define:

asset created in Blender

Atlas export preset applied

Atlas Suite validates/export indexes it

engine/editor ingests it

changes are detected later

re-export updates downstream safely

Without this, asset iteration gets messy.

What Blender should do for your specific project
Because your project is hybrid voxel + low-poly, Blender is especially useful for the low-poly authored side:

ships and interiors

rig/mech hard-surface parts

modular environment kits

props

character body/gear meshes

hand/weapon/viewmodel components

animated interactables

For the voxel side, Blender should be a support tool, not the main source of truth:

concept/blockout meshes

proxy forms

conversion helpers

presentation meshes

damage-state overlays

baked visual shells over voxel-driven structure

That pairing is strong.

Recommended Atlas Suite tooling for Blender
You should add a dedicated feature cluster:

Blender Integration Pack
Blender executable locator

version/profile manager

Atlas Blender add-on deployment

export preset manager

asset manifest bridge

headless batch runner

import/export job queue

validation rules

scene compliance scanner

socket/collision/rig inspector

one-click “open source asset”

one-click “re-export selected asset”

log capture and error surfacing into Atlas Suite

Suggested module breakdown
AtlasSuite.Tooling.Blender

AtlasSuite.Tooling.Blender.Jobs

AtlasSuite.Tooling.Blender.Validation

AtlasSuite.Tooling.Blender.Export

AtlasSuite.Tooling.Blender.Manifest

And on the Blender side:

atlas_blender_addon

The biggest Blender-related gaps, in order
No asset pipeline contract

No export preset system

No asset manifest bridge

No headless batch automation

No scene compliance rules

No safe scripting policy

No round-trip reimport workflow

No Blender-specific validation panel in Atlas Suite

Best practical direction
The right move is:

keep Atlas Suite in charge

integrate Blender as a managed authoring tool

build a custom Blender add-on

standardize export/validation through Atlas Suite jobs

let AtlasAI plan and automate Blender-related work, but only through approved commands and presets

That gives you a professional pipeline instead of a loose tool hookup.

I can map out the full Blender Integration Architecture Pack next using AtlasAI naming, including module layout, job flow, export contracts, validation rules, and the Blender add-on structure.


is there any other oopen source tools we can integrate into our suite to make it more powerful tooling layer  for the specific project?

Oh this is where Atlas Suite can really level up into something insanely powerful. You’re basically building your own studio-grade dev platform, so pulling in the right open-source tools (in the right way) will save you YEARS.

I’m going to give you high-value integrations only—things that actually fit your project (voxel + modular + AI + tooling suite), not random fluff.

🧠 Core Principle for Integrations
Every tool must fit one of these roles:

Authoring (create content)

Processing (convert/optimize)

Validation (enforce rules)

Automation (pipeline execution)

Insight (debug/visualize/analyze)

And ALL of them must:
👉 plug into Command Bus + AtlasAI + Module System

🔥 HIGH-IMPACT OPEN SOURCE TOOLS TO INTEGRATE
🧱 1. Asset Processing / Pipeline
🔹 Assimp
Why it’s huge:
Universal model importer

Supports tons of formats (FBX, OBJ, glTF, etc.)

Lets you normalize everything into your pipeline

Use in Atlas Suite:
Convert Blender exports → engine format

Validate mesh structure

Extract:

bones

meshes

materials

animations

👉 Works perfectly with your Blender pipeline

🔹 Open3D
Use cases:
mesh analysis

voxelization helpers

geometry processing

collision simplification

👉 VERY useful for your voxel ↔ mesh bridge

🔹 MeshLab
Use for:
mesh cleanup

decimation

repair

optimization pipelines

👉 Can be run headless for batch jobs

🧠 2. AI / Code Intelligence Layer
🔹 tree-sitter
This is CRITICAL
What it gives you:
fast code parsing

syntax trees

language-agnostic analysis

Use in AtlasAI:
understand code structure

detect functions/classes

map dependencies

power repo indexer

👉 This is your code intelligence backbone

🔹 ripgrep
Why:
insanely fast search across repo

Use:
AtlasAI context search

validation scans

dependency lookups

🔹 sqlite
Use:
workspace index storage

schema registry cache

asset manifest DB

command history

AI memory layer

👉 Lightweight + perfect for your suite

🧪 3. Validation / Quality / Debug
🔹 clang-tidy
Use:
engine code validation

enforce standards

detect bugs early

🔹 Cppcheck
Use:
deeper analysis

catch memory issues

detect unsafe code

🔹 Valgrind
Use:
runtime memory debugging

leak detection

👉 Hook into Atlas runtime testing

🎮 4. Voxel / Geometry Systems
🔹 OpenVDB
This is MASSIVE for your project
Use:
voxel storage

damage systems

procedural generation

LOD voxel streaming

👉 Industry-grade voxel backend

🔹 FastNoiseLite
Use:
terrain generation

asteroid fields

anomalies

procedural content

👉 Lightweight + perfect for PCG

🧰 5. Build / DevOps / Automation
🔹 CMake
Use:
engine builds

cross-platform support

dependency management

🔹 Ninja
Use:
super fast builds

integrates with CMake

🔹 Taskfile
Use:
define build pipelines

automation scripts

job orchestration

👉 Can tie directly into Command Bus

🌐 6. Networking / Backend Tools
🔹 FastAPI
Use:
Atlas web server

remote control dashboard

API layer

🔹 WebSocket
Use:
live updates

runtime telemetry

remote control

📊 7. Visualization / Debug UI
🔹 Dear ImGui
⚠️ You said NO ImGui → skip for UI
BUT…

👉 You could still embed it for:

debug overlays

dev-only tools (optional)

If you want strict consistency → ignore it.

🔹 Graphviz
Use:
system graphs

dependency maps

AI plan visualization

faction/economy flows

🎨 8. Texture / Material / Asset Tools
🔹 ImageMagick
Use:
texture conversion

compression

batch processing

🔹 OpenImageIO
Use:
advanced texture pipeline

mip generation

format normalization

🎧 9. Audio (future-proofing)
🔹 FMOD (free tier)
Use:
advanced audio system

spatial audio

event-driven sound

🧠 10. AtlasAI SUPERCHARGE STACK
If you want AtlasAI to feel insane:

🔹 FAISS
Use:
semantic search over repo

memory retrieval

context matching

🔹 LangChain
Use:
task planning pipelines

tool selection logic

multi-step execution

🔹 LlamaIndex
Use:
index repo

connect schemas + code + docs

🧠 MOST IMPORTANT COMBINATIONS
These combos are where magic happens:

🔥 AtlasAI Brain Stack
tree-sitter

ripgrep

SQLite

FAISS

👉 gives you:

repo understanding

semantic memory

fast search

structured reasoning

🔥 Asset Pipeline Stack
Blender (with add-on)

Assimp

OpenImageIO

MeshLab

👉 gives you:

full asset pipeline

validation + conversion

batch processing

🔥 Voxel + PCG Stack
OpenVDB

FastNoiseLite

👉 gives you:

scalable voxel system

procedural worlds

🔥 DevOps Stack
CMake

Ninja

Taskfile

👉 gives you:

fast builds

automation

reproducible pipelines

🚨 What NOT to integrate (important)
Avoid:

heavy monolithic engines (Unity tools, etc.)

overly complex enterprise frameworks

tools that bypass your command bus

tools that don’t support automation

🧭 FINAL RECOMMENDATION (PRIORITY)
If I had to pick the top 8 to integrate FIRST:

tree-sitter

SQLite

Assimp

OpenVDB

FastNoiseLite

ripgrep

CMake + Ninja

FAISS

These give you:
👉 AI + pipeline + voxel + build backbone

🚀 Next Step (this would be huge)
We can now build:

👉 “Atlas Suite Integration Architecture Pack”

That defines:

how each tool plugs into Command Bus

module structure per tool

data flow

job execution model

AtlasAI tool usage layer

This would basically turn Atlas Suite into a real production-grade dev platform blueprint.

If you want to push forward hard, I’d do that next.


yes


Thought for 20s
Yes — and now we can tighten this into a real integration architecture for Atlas Suite with AtlasAI as the orchestration brain.

The strongest additions are the ones that give you four things at once: repo intelligence, asset pipeline power, voxel/PCG support, and validation/test automation.

Best open-source integrations for this project
Tier 1 — should be part of the core tooling backbone
tree-sitter for code intelligence. It is an incremental parsing library that can build syntax trees and update them efficiently as code changes, which makes it a strong fit for AtlasAI’s repo map, symbol graph, refactor targeting, and language-aware inspection. 

ripgrep for ultra-fast workspace search. It recursively searches directories, respects .gitignore by default, and is a great low-level search engine for AtlasAI context gathering, compliance scans, and “find all related files” tooling. 

SQLite for local tooling storage. SQLite is self-contained, serverless, zero-configuration, and transactional, which makes it ideal for Atlas Suite’s local index, asset manifest store, command history, job queue state, and validation cache. 

CMake + Ninja for build orchestration. CMake generates native build systems including Ninja and IDE project files, while Ninja is designed to run builds as fast as possible from generated build inputs. That pairing is a very good fit for your engine/editor/tools build matrix. 

Tier 2 — asset and DCC pipeline power
Blender as the managed authoring tool. Blender supports background mode and command-line Python execution, which makes it suitable for Atlas-driven batch export, validation, and conversion jobs instead of just manual art work. It also has a full add-on system for custom pipeline tooling. 

Assimp as the interchange/import normalization layer. Assimp loads many 3D formats into a shared in-memory format and supports more than 40 file formats for import, which is useful for validating and normalizing external geometry entering your pipeline. 

OpenImageIO for texture and image processing. It provides format-agnostic APIs for reading, writing, and processing many image formats and is aimed at production pipelines, making it a strong fit for texture normalization, mip prep, preview generation, and batch asset QA. 

Tier 3 — voxel / PCG / worldbuilding support
OpenVDB for sparse volumetric and voxel-adjacent data work. OpenVDB is built around efficient sparse volumetric data structures and tools, which makes it a strong candidate for higher-end voxel processing, sparse damage fields, destruction data prep, and conversion utilities around your hybrid voxel pipeline. 

FastNoiseLite for procedural generation. It is a fast, portable open-source noise library with multiple noise algorithms, making it a clean fit for terrain fields, asteroid fields, anomaly distribution, resource masks, and procedural shaping tools. 

Tier 4 — visualization, testing, and dev diagnostics
Graphviz for system graphs. Graphviz is open-source graph visualization software and supports DOT plus multiple layout/rendering paths, which is perfect for repo dependency maps, schema graphs, AI plan graphs, faction relationship diagrams, and build pipeline visualizations inside Atlas Suite. 

GoogleTest for C++ test infrastructure. GoogleTest is Google’s C++ testing and mocking framework, so it is a strong fit for engine tests, subsystem tests, validator tests, and automated regression harnesses surfaced inside Atlas Suite. 

What I would not prioritize right now
I would not make Atlas Suite depend early on:

heavyweight general-purpose orchestration frameworks

tools that bypass your command bus

anything UI-centric that conflicts with your no-ImGui rule

tools that become the new “source of truth” outside Atlas Suite

That last one is important. Blender, Assimp, OpenImageIO, and OpenVDB should be connected capabilities, not authority holders.

Recommended Atlas Suite module map
This is the cleanest architecture path.

Core intelligence

AtlasSuite.Tooling.Search → ripgrep adapter

AtlasSuite.Tooling.Parse → tree-sitter adapter

AtlasSuite.Storage → SQLite index + manifests + jobs

Build layer

AtlasSuite.Tooling.Build → CMake/Ninja profiles, logs, artifact tracking

Art pipeline

AtlasSuite.Tooling.Blender → Blender launch, add-on bridge, headless jobs

AtlasSuite.Tooling.AssetImport → Assimp-based inspection/conversion

AtlasSuite.Tooling.Images → OpenImageIO-based texture utilities

Voxel / PCG

AtlasSuite.Tooling.VDB → OpenVDB conversion and sparse volume tooling

AtlasSuite.Tooling.PCG → FastNoiseLite jobs and graph presets

Debug / quality

AtlasSuite.Tooling.Graphs → Graphviz diagrams

AtlasSuite.Tooling.Tests → GoogleTest discovery, run, and result surfacing

How AtlasAI should use them
AtlasAI should never call these tools “raw.” It should go through Atlas Suite commands like:

IndexWorkspaceCommand

SearchWorkspaceCommand

ParseFileSymbolsCommand

RunBuildProfileCommand

RunBlenderExportJobCommand

InspectMeshAssetCommand

NormalizeTextureSetCommand

GeneratePCGMaskCommand

RenderDependencyGraphCommand

RunTestSuiteCommand

That keeps the integration safe, logged, undo-aware where appropriate, and consistent with the suite architecture.

Best first-wave integration order
If the goal is maximum gain with minimum chaos, I’d do this in order:

SQLite

ripgrep

tree-sitter

CMake/Ninja

Blender integration

Assimp

GoogleTest

Graphviz

OpenImageIO

FastNoiseLite

OpenVDB

That sequence gives you:

immediate repo intelligence

strong build tooling

controlled DCC integration

reliable testing

then deeper asset/PCG/voxel power

Biggest hidden gap even after adding these
The tools themselves are not the hard part anymore. The real gap is the adapter contract:

For every external tool, Atlas Suite still needs:

capability registration

version detection

settings/profile management

command wrappers

structured outputs

log normalization

failure handling

result caching

AtlasAI-safe invocation rules

That adapter layer is what turns “a pile of tools” into a unified tooling platform.

My strongest recommendation
The best next deliverable is an Open Source Integration Pack for Atlas Suite that defines, for each tool:

module name

role in pipeline

command set

input/output contract

storage requirements

validation hooks

AtlasAI usage rules

priority phase

That would give you the exact blueprint for integrating all of this cleanly.


yes


Thought for 13s
Excellent. Here’s the Open Source Integration Pack for Atlas Suite + AtlasAI.

The goal is not just “add tools,” but to make each one a managed capability inside your tooling layer through adapters, jobs, validation, and command wrappers.

Integration principles
Every external tool should be integrated through the same contract:

Capability registry: Atlas Suite knows the tool exists, version, path, features, and health.

Adapter: wraps the tool’s CLI/API into structured commands.

Job runner: handles long-running tasks, progress, cancellation, retries.

Result normalization: logs, warnings, artifacts, and structured outputs land in a consistent format.

AtlasAI-safe access: AtlasAI invokes suite commands, never raw processes or scripts.

That matters because these tools all have different strengths: Tree-sitter is built for incremental parsing and syntax trees, ripgrep is extremely fast and respects ignore rules by default, SQLite is self-contained and transactional, CMake generates modern build systems including Ninja, Blender supports background and scripted execution, Assimp normalizes many 3D formats, OpenImageIO handles many image formats through a format-agnostic API, OpenVDB is built around sparse volumetric data, FastNoiseLite is a portable noise library, Graphviz visualizes graph structures, and GoogleTest provides a mature C++ testing framework. 

Tier 1: core backbone integrations
1. SQLite
Role: local operational database for Atlas Suite. SQLite is an in-process, self-contained, serverless, zero-configuration, transactional database engine, which makes it ideal for embedded tooling state. 

Use in Atlas Suite

workspace index

command history

job queue state

asset manifest store

schema cache

validation cache

AtlasAI plan history

Module

AtlasSuite.Storage.Sqlite

Commands

InitializeWorkspaceDbCommand

RebuildWorkspaceIndexCommand

QueryAssetManifestCommand

WriteToolJobStateCommand

Output contracts

normalized tables for files, symbols, assets, jobs, command logs, validation results

Why first
It becomes the persistence spine for almost every other integration. 

2. ripgrep
Role: fast workspace search engine. ripgrep recursively searches directories and respects .gitignore rules by default, which is exactly what you want for code-heavy repos. 

Use in Atlas Suite

repo-wide text search

AtlasAI context retrieval

compliance scans

reference lookups

“find all usages” precursor layer

Module

AtlasSuite.Tooling.Search

Commands

SearchWorkspaceCommand

SearchScopedFilesCommand

ScanForPatternViolationsCommand

Output contracts

match list with file, line, preview, scope, ignore status

Notes
This should be wrapped, not exposed directly, so AtlasAI can issue structured searches with filters and scopes. 

3. Tree-sitter
Role: code structure intelligence. Tree-sitter is an incremental parsing library and parser generator that builds concrete syntax trees and can efficiently update them as files change. 

Use in Atlas Suite

symbol extraction

class/function map

code region targeting

language-aware diffs

refactor support

AtlasAI code planning context

Module

AtlasSuite.Tooling.Parse

Commands

ParseFileSymbolsCommand

BuildCodeStructureMapCommand

LocateMutationTargetsCommand

Output contracts

file symbol graph

syntax node ranges

language-specific metadata

Why it matters
This is what makes AtlasAI feel repo-aware instead of text-search-only. 

4. CMake + Ninja
Role: build system integration. CMake generates modern build systems including Ninja, and CMake’s Ninja generators support single-config and multi-config workflows. 

Use in Atlas Suite

engine builds

suite builds

editor builds

client/server builds

test builds

package builds

Module

AtlasSuite.Tooling.Build

Commands

ConfigureBuildProfileCommand

RunBuildProfileCommand

RunTargetCommand

CollectBuildArtifactsCommand

Output contracts

profile, generator, config, targets, logs, artifacts, duration, errors

Why it fits
It gives you a clean bridge from suite UI to reproducible local builds. 

Tier 2: content and DCC pipeline
5. Blender
Role: managed DCC authoring and export tool. Blender supports command-line background mode and scripted execution, which makes it viable for headless export and validation jobs, not just manual editing. 

Use in Atlas Suite

open source assets

one-click export jobs

rig/animation prep

modular kit authoring

headless re-export batches

scene compliance checks through a custom add-on

Modules

AtlasSuite.Tooling.Blender

AtlasSuite.Tooling.Blender.Jobs

AtlasSuite.Tooling.Blender.Validation

Commands

LocateBlenderInstallCommand

OpenAssetInBlenderCommand

RunBlenderExportJobCommand

RunBlenderValidationJobCommand

DeployBlenderAddonCommand

Output contracts

source .blend

exported assets

sockets/helpers found

collision helpers found

rig/skeleton info

export preset used

validation results

Critical gap it closes
A proper DCC pipeline for your low-poly authored side while still keeping Atlas Suite as authority. 

6. Assimp
Role: import and normalization layer for 3D files. Assimp loads many 3D formats into a shared in-memory representation and supports 40+ import formats. 

Use in Atlas Suite

inspect external asset drops

validate imported meshes

detect skeleton/material/animation presence

convert external assets into normalized intermediate structures

Module

AtlasSuite.Tooling.AssetImport

Commands

InspectMeshAssetCommand

NormalizeImportedModelCommand

ValidateImportedSkeletonCommand

Output contracts

mesh count

skeleton presence

animation clips

material slots

warnings on unsupported or missing data

Best use
Between Blender output and engine ingest, or for third-party/model-library imports. 

7. OpenImageIO
Role: texture and image pipeline processing. OpenImageIO provides a format-agnostic API for reading, writing, and processing many image formats. 

Use in Atlas Suite

normalize texture sets

preview generation

mip prep

channel inspection

naming/size consistency checks

batch conversions

Module

AtlasSuite.Tooling.Images

Commands

InspectTextureSetCommand

NormalizeTextureSetCommand

GeneratePreviewAtlasCommand

Output contracts

dimensions

channels

format

color-space metadata where available

generated outputs

Why it’s useful
It gives you a serious asset-processing layer without making the engine own every preprocessing step. 

Tier 3: voxel and PCG support
8. OpenVDB
Role: sparse volumetric tooling. OpenVDB is built around a hierarchical sparse volumetric data structure and tools for efficient storage and manipulation of sparse volumetric grids. 

Use in Atlas Suite

voxel conversion utilities

sparse damage field tooling

destruction/repair field preprocessing

volumetric analysis tools

offline structural volume prep

Module

AtlasSuite.Tooling.VDB

Commands

ConvertMeshToSparseVolumeCommand

AnalyzeVoxelDensityCommand

GenerateDamageFieldCommand

Output contracts

sparse volume artifacts

density summaries

conversion statistics

validation warnings

Important note
This is best as an offline or tooling-side utility layer, not automatically the runtime core unless your engine architecture explicitly wants that. 

9. FastNoiseLite
Role: procedural signal generation. FastNoiseLite is an open-source, high-performance, portable noise library with multiple noise algorithms. 

Use in Atlas Suite

terrain masks

asteroid field shaping

biome/resource masks

anomaly distribution fields

repeatable seed previews

Module

AtlasSuite.Tooling.PCG

Commands

GenerateNoiseFieldCommand

PreviewProceduralMaskCommand

BakeResourceDistributionCommand

Output contracts

seed

algorithm

frequency params

generated field previews

exportable masks/data

Why it fits
It is simple, fast, and excellent for predictable procedural tooling. 

Tier 4: visualization and quality
10. Graphviz
Role: graph rendering. Graphviz is open-source graph visualization software used to represent structural information as graphs and networks. 

Use in Atlas Suite

repo dependency graphs

schema relationship maps

AtlasAI plan visualization

faction/economy diagrams

module dependency debugging

Module

AtlasSuite.Tooling.Graphs

Commands

RenderDependencyGraphCommand

RenderSchemaGraphCommand

RenderTaskPlanGraphCommand

Output contracts

DOT source

rendered image/SVG/PDF

graph metadata

Why it matters
It turns abstract system links into something you can actually inspect. 

11. GoogleTest
Role: C++ test integration. GoogleTest is Google’s C++ testing and mocking framework. 

Use in Atlas Suite

discover tests

run selected suites

regression checks

smoke tests after AtlasAI code changes

surface test failures directly in UI

Module

AtlasSuite.Tooling.Tests

Commands

DiscoverTestsCommand

RunTestSuiteCommand

RunTargetedRegressionCommand

Output contracts

suite/case names

pass/fail

duration

logs

linked source files when possible

Why it fits
It closes a major gap in safe code generation and refactor validation. 

Recommended adapter contract
Every tool adapter should implement the same interface shape:

public interface IToolCapabilityAdapter
{
    string ToolId { get; }
    string DisplayName { get; }
    Task<ToolHealthReport> CheckHealthAsync(CancellationToken ct);
    Task<IReadOnlyList<ToolCapability>> GetCapabilitiesAsync(CancellationToken ct);
    Task<ToolExecutionResult> ExecuteAsync(ToolExecutionRequest request, CancellationToken ct);
}
And every result should normalize to:

Success

Warnings

Errors

Artifacts

Logs

StructuredData

Duration

ExitCode

SuggestedFollowups

AtlasAI rules for using these tools
AtlasAI should only be allowed to:

discover tool capabilities through the capability registry

invoke tool wrappers through suite commands

run destructive tools only in approved scopes

prefer dry-run and inspection commands before mutation commands

attach artifacts and logs back to the command/job history

That keeps AtlasAI powerful without letting it become unpredictable.

Best phase plan
Phase 1
SQLite

ripgrep

Tree-sitter

CMake/Ninja

This gives Atlas Suite memory, search, code awareness, and build control. 

Phase 2
Blender

Assimp

GoogleTest

This gives you a real art pipeline plus safer code iteration. 

Phase 3
OpenImageIO

Graphviz

FastNoiseLite

This strengthens texture handling, graph/debug tooling, and procedural previews. 

Phase 4
OpenVDB

This adds deeper sparse volumetric tooling once the hybrid voxel pipeline is ready to exploit it. 

Biggest remaining gap after all this
Even with these integrations, the make-or-break piece is still the tool job system:

queued execution

progress

structured logs

cancellation

retry

artifact retention

result indexing in SQLite

Without that, the integrations work individually but don’t become a unified production tooling layer.

Strongest next move
The best next deliverable is a Tool Adapter + Job System spec for Atlas Suite, with exact module names, C# interfaces, command classes, job records, and UI panels for:

Tool Registry

Job Queue

Artifact Viewer

Validation Results

AtlasAI Tool Actions

That would turn this from a blueprint into implementation-ready architecture.


yes

Perfect — this is the layer that turns Atlas Suite from “a shell with integrations” into a real operating platform for development.

Atlas Suite — Tool Adapter + Job System Spec
Using the updated naming:

Atlas Suite = tooling platform

AtlasAI = integrated AI system

This spec covers:

Tool Capability Registry

Tool Adapter Contracts

Job System

Artifact System

Validation Result System

AtlasAI Tool Invocation Rules

UI Panels

Module Layout

Implementation Order

Immediate code scaffold targets

1. Core design goal
Every external or internal tool should behave the same way inside Atlas Suite.

That means whether AtlasAI runs:

a repo search

a Blender export

a build

a schema validation

a test suite

a graph render

a PCG preview

…the suite should process it through one common lifecycle:

Discover Tool
→ Check Capability
→ Build Request
→ Queue Job
→ Execute Through Adapter
→ Normalize Logs / Outputs
→ Store Artifacts
→ Publish Result
→ Surface to UI / AtlasAI
This is the backbone.

2. Tool Capability Registry
Purpose
Atlas Suite needs a central source of truth for all usable tools.

Without this:

AtlasAI guesses

modules hardcode dependencies

version drift becomes invisible

failures become inconsistent

Registry responsibilities
The registry should track:

tool id

display name

category

provider module

install path

detected version

health status

supported capabilities

supported commands/actions

input/output types

environment requirements

last validation/check time

Example tool categories
Search

Parse

Build

DCC

AssetImport

Imaging

Voxel

PCG

Graph

Test

Validation

Archive

CloudSync

Example registry entries
tool.ripgrep

tool.treesitter

tool.cmake

tool.ninja

tool.blender

tool.assimp

tool.openimageio

tool.graphviz

tool.googletest

tool.fastnoiselite

tool.openvdb

Suggested core models
public sealed class ToolDescriptor
{
    public string ToolId { get; init; } = "";
    public string DisplayName { get; init; } = "";
    public string Category { get; init; } = "";
    public string ProviderModuleId { get; init; } = "";
    public string ExecutablePath { get; init; } = "";
    public string Version { get; init; } = "";
    public ToolHealthStatus HealthStatus { get; init; }
    public IReadOnlyList<ToolCapabilityDescriptor> Capabilities { get; init; } = Array.Empty<ToolCapabilityDescriptor>();
    public DateTimeOffset LastCheckedUtc { get; init; }
}
public sealed class ToolCapabilityDescriptor
{
    public string CapabilityId { get; init; } = "";
    public string DisplayName { get; init; } = "";
    public string Description { get; init; } = "";
    public IReadOnlyList<string> SupportedRequestKinds { get; init; } = Array.Empty<string>();
    public bool SupportsDryRun { get; init; }
    public bool ProducesArtifacts { get; init; }
    public bool ProducesStructuredData { get; init; }
}
3. Tool Adapter Contract
Purpose
A tool adapter is the translation layer between Atlas Suite and a real tool.

Atlas Suite never talks directly to Blender, ripgrep, CMake, or anything else.
It always talks to an adapter.

Adapter responsibilities
Each adapter must:

detect whether tool is installed

detect version

describe supported capabilities

validate incoming requests

execute jobs

normalize raw outputs

map tool errors into suite errors

produce artifacts and structured results

Core interface
public interface IToolCapabilityAdapter
{
    string ToolId { get; }
    string DisplayName { get; }

    Task<ToolHealthReport> CheckHealthAsync(CancellationToken ct);
    Task<IReadOnlyList<ToolCapabilityDescriptor>> GetCapabilitiesAsync(CancellationToken ct);
    Task<ToolExecutionResult> ExecuteAsync(ToolExecutionRequest request, CancellationToken ct);
}
Health report
public sealed class ToolHealthReport
{
    public string ToolId { get; init; } = "";
    public ToolHealthStatus Status { get; init; }
    public string Version { get; init; } = "";
    public string Message { get; init; } = "";
    public string ExecutablePath { get; init; } = "";
    public IReadOnlyList<string> Warnings { get; init; } = Array.Empty<string>();
}
Request model
public sealed class ToolExecutionRequest
{
    public string RequestId { get; init; } = Guid.NewGuid().ToString("N");
    public string ToolId { get; init; } = "";
    public string CapabilityId { get; init; } = "";
    public string RequestKind { get; init; } = "";
    public string WorkspaceRoot { get; init; } = "";
    public bool IsDryRun { get; init; }
    public IReadOnlyDictionary<string, string> Parameters { get; init; } = new Dictionary<string, string>();
    public IReadOnlyList<string> InputPaths { get; init; } = Array.Empty<string>();
    public IReadOnlyList<string> ExpectedOutputPaths { get; init; } = Array.Empty<string>();
    public string RequestedBy { get; init; } = "";
    public string CorrelationId { get; init; } = "";
}
Result model
public sealed class ToolExecutionResult
{
    public bool Success { get; init; }
    public string ToolId { get; init; } = "";
    public string CapabilityId { get; init; } = "";
    public int ExitCode { get; init; }
    public string Summary { get; init; } = "";
    public IReadOnlyList<string> Warnings { get; init; } = Array.Empty<string>();
    public IReadOnlyList<string> Errors { get; init; } = Array.Empty<string>();
    public IReadOnlyList<ToolArtifactRecord> Artifacts { get; init; } = Array.Empty<ToolArtifactRecord>();
    public IReadOnlyList<ToolLogRecord> Logs { get; init; } = Array.Empty<ToolLogRecord>();
    public IReadOnlyDictionary<string, string> StructuredData { get; init; } = new Dictionary<string, string>();
    public TimeSpan Duration { get; init; }
}
4. Job System
Purpose
Some tool actions are too large or too long-running to be treated like simple instant commands.

Examples:

full repo indexing

Blender batch export

build all targets

test suite execution

compliance scan

graph generation

asset manifest rebuild

cloud sync

These should run as jobs.

Job lifecycle
Created
→ Queued
→ Preparing
→ Running
→ Succeeded / Failed / Cancelled
→ Archived
Job responsibilities
The job system must support:

queueing

prioritization

cancellation

retries

progress

log streaming

artifact registration

summary generation

persistence in SQLite

Core job model
public sealed class ToolJobRecord
{
    public string JobId { get; init; } = Guid.NewGuid().ToString("N");
    public string Title { get; init; } = "";
    public string ToolId { get; init; } = "";
    public string CapabilityId { get; init; } = "";
    public string Status { get; set; } = "Created";
    public string RequestedBy { get; init; } = "";
    public string CorrelationId { get; init; } = "";
    public int ProgressPercent { get; set; }
    public DateTimeOffset CreatedUtc { get; init; }
    public DateTimeOffset? StartedUtc { get; set; }
    public DateTimeOffset? FinishedUtc { get; set; }
    public int RetryCount { get; set; }
    public string Summary { get; set; } = "";
}
Job runner interfaces
public interface IToolJobQueue
{
    Task<string> EnqueueAsync(ToolExecutionRequest request, string title, CancellationToken ct);
    Task CancelAsync(string jobId, CancellationToken ct);
    Task RetryAsync(string jobId, CancellationToken ct);
}
public interface IToolJobRunner
{
    Task RunAsync(string jobId, CancellationToken ct);
}
public interface IToolJobStore
{
    Task SaveAsync(ToolJobRecord record, CancellationToken ct);
    Task<ToolJobRecord?> GetAsync(string jobId, CancellationToken ct);
    Task<IReadOnlyList<ToolJobRecord>> GetRecentAsync(int count, CancellationToken ct);
}
Job execution model
The runner should:

resolve job

resolve adapter

validate tool health

validate request

mark running

stream logs/progress

register artifacts

normalize result

write summary

notify UI + AtlasAI

5. Artifact System
Purpose
Many tools produce outputs that need to be retained and inspectable.

Examples:

exported meshes

rendered graphs

build logs

screenshots

validation reports

test outputs

generated docs

normalized textures

sparse volume files

Artifact record
public sealed class ToolArtifactRecord
{
    public string ArtifactId { get; init; } = Guid.NewGuid().ToString("N");
    public string JobId { get; init; } = "";
    public string ArtifactType { get; init; } = "";
    public string DisplayName { get; init; } = "";
    public string FilePath { get; init; } = "";
    public string ProducedByToolId { get; init; } = "";
    public long SizeBytes { get; init; }
    public string ContentHash { get; init; } = "";
    public DateTimeOffset CreatedUtc { get; init; }
}
Artifact categories
BuildLog

ValidationReport

TestReport

ExportedAsset

GraphRender

PreviewImage

SchemaDoc

IndexSnapshot

DiffPatch

VolumeData

TextureOutput

Artifact rules
Artifacts should be:

indexed

searchable

tied to jobs

tied to commands where relevant

optionally retained by policy

previewable in UI when practical

6. Log normalization
Purpose
Every tool emits logs differently. Atlas Suite must make them uniform.

Log record model
public sealed class ToolLogRecord
{
    public DateTimeOffset TimestampUtc { get; init; }
    public string JobId { get; init; } = "";
    public string ToolId { get; init; } = "";
    public string Severity { get; init; } = "";
    public string Message { get; init; } = "";
    public string? SourcePath { get; init; }
    public int? SourceLine { get; init; }
}
Severity levels
Trace

Info

Warning

Error

Critical

Why it matters
This lets:

the command log panel

the job panel

the diagnostics panel

AtlasAI summaries

all consume one shared log shape.

7. Validation Result System
Purpose
A huge number of tools are effectively validators.

Examples:

schema validation

scene validation

naming validation

mesh validation

texture validation

code style validation

dependency validation

These should not just return “success/fail.”
They should emit consistent issue objects.

Validation issue model
public sealed class ValidationIssue
{
    public string IssueId { get; init; } = Guid.NewGuid().ToString("N");
    public string RuleId { get; init; } = "";
    public string Severity { get; init; } = "";
    public string Category { get; init; } = "";
    public string Message { get; init; } = "";
    public string? FilePath { get; init; }
    public int? LineNumber { get; init; }
    public string? SuggestedFix { get; init; }
}
Validation report model
public sealed class ValidationReport
{
    public string ReportId { get; init; } = Guid.NewGuid().ToString("N");
    public string JobId { get; init; } = "";
    public string SourceToolId { get; init; } = "";
    public bool Success { get; init; }
    public IReadOnlyList<ValidationIssue> Issues { get; init; } = Array.Empty<ValidationIssue>();
    public string Summary { get; init; } = "";
}
Why this matters
Now every validation-capable tool feeds one common issue viewer.

8. AtlasAI tool invocation rules
Core rule
AtlasAI never launches tools directly.

AtlasAI may only:

query the tool registry

choose a supported capability

build a structured request

submit through command bus / job queue

inspect results

summarize outcomes

propose next steps

AtlasAI decision flow
Goal
→ Find relevant capability
→ Check tool health
→ Pick safe request type
→ Prefer inspect/validate before mutate
→ Queue job
→ Observe result
→ Summarize / continue
Allowed AtlasAI actions
Safe by default
search

parse

inspect asset

render graph

run validation

query manifest

discover tests

dry-run export

dry-run build config

Guarded
build

export assets

normalize textures

run batch jobs

regenerate docs

targeted reindex

Restricted
destructive overwrites

mass conversion

deletion of outputs

replacing source assets

running arbitrary scripts

AtlasAI request types
You should standardize AtlasAI requests as:

Inspect

Validate

Preview

Generate

Convert

Build

Test

Sync

Repair

Render

9. UI panel set
These are the suite panels that make the tool layer usable.

A. Tool Registry Panel
Shows:

all known tools

install path

detected version

health

capabilities

module owner

warnings

Actions:

recheck health

open settings

test capability

inspect logs

B. Job Queue Panel
Shows:

queued/running/completed jobs

progress

duration

who requested it

related tool

related artifacts

Actions:

cancel

retry

open result

open artifacts

filter by tool/status

C. Artifact Viewer Panel
Shows:

output files

previews where possible

artifact source job

generation time

retention policy

Actions:

open

compare

reveal in explorer

attach to report

promote to tracked asset

D. Validation Results Panel
Shows:

issues grouped by category/tool

severity

file path

suggested fix

Actions:

open file at issue

export report

run fix command

suppress/waive rule where allowed

E. AtlasAI Tool Actions Panel
Shows:

AtlasAI proposed tool usage

safety level

target scope

job plan preview

result summaries

Actions:

approve

dry-run

execute

inspect job

rollback if applicable

F. Diagnostics Panel
Shows:

normalized logs

health warnings

repeated failures

failing tools

failing modules

10. Module layout
Recommended structure:

AtlasSuite/
├── AtlasSuite.Tooling/
├── AtlasSuite.Tooling.Registry/
├── AtlasSuite.Tooling.Jobs/
├── AtlasSuite.Tooling.Artifacts/
├── AtlasSuite.Tooling.Validation/
├── AtlasSuite.Tooling.Search/
├── AtlasSuite.Tooling.Parse/
├── AtlasSuite.Tooling.Build/
├── AtlasSuite.Tooling.Blender/
├── AtlasSuite.Tooling.AssetImport/
├── AtlasSuite.Tooling.Images/
├── AtlasSuite.Tooling.VDB/
├── AtlasSuite.Tooling.PCG/
├── AtlasSuite.Tooling.Graphs/
├── AtlasSuite.Tooling.Tests/
└── AtlasSuite.AtlasAI/
Responsibility split
Tooling.Registry = discover/register tools

Tooling.Jobs = queue, runner, progress, retries

Tooling.Artifacts = artifact storage/indexing

Tooling.Validation = issue/report normalization

tool-specific modules = actual adapters

AtlasAI = planning + invocation logic

11. Command set
These commands should exist early.

Registry
RefreshToolRegistryCommand

CheckToolHealthCommand

GetToolCapabilitiesCommand

Jobs
QueueToolJobCommand

CancelToolJobCommand

RetryToolJobCommand

ArchiveToolJobCommand

Artifacts
RegisterArtifactCommand

OpenArtifactCommand

CompareArtifactsCommand

Validation
PublishValidationReportCommand

ResolveValidationIssueCommand

AtlasAI
BuildAtlasAIToolPlanCommand

ExecuteAtlasAIToolPlanCommand

PreviewAtlasAIToolPlanCommand

12. SQLite table plan
Since SQLite is your local persistence backbone, I’d start with these tables:

tools
tool_id

display_name

category

provider_module_id

executable_path

version

health_status

last_checked_utc

tool_capabilities
capability_id

tool_id

display_name

description

request_kinds_json

supports_dry_run

produces_artifacts

produces_structured_data

tool_jobs
job_id

title

tool_id

capability_id

status

requested_by

correlation_id

progress_percent

created_utc

started_utc

finished_utc

retry_count

summary

tool_logs
log_id

job_id

tool_id

severity

timestamp_utc

message

source_path

source_line

tool_artifacts
artifact_id

job_id

artifact_type

display_name

file_path

produced_by_tool_id

size_bytes

content_hash

created_utc

validation_reports
report_id

job_id

source_tool_id

success

summary

validation_issues
issue_id

report_id

rule_id

severity

category

message

file_path

line_number

suggested_fix

13. Implementation order
Phase 1 — backbone
Build:

Tool registry

Tool adapter interface

Job queue

Job store

Log normalization

Artifact registration

Goal:
Atlas Suite can register tools and run jobs in a consistent way.

Phase 2 — first real adapters
Add:

Search adapter

Parse adapter

Build adapter

Goal:
AtlasAI can search repo, inspect code structure, and run builds through the same system.

Phase 3 — validation and UI
Add:

Validation model

Validation panel

Tool registry panel

Job queue panel

Diagnostics panel

Goal:
Make the system visible and trustworthy.

Phase 4 — content pipeline
Add:

Blender adapter

Asset import adapter

Image adapter

Goal:
Turn Atlas Suite into a real content tool hub.

Phase 5 — advanced systems
Add:

Graphs

Tests

PCG

VDB

Goal:
Deepen project-specific power.

14. Immediate code scaffold targets
These are the exact files I’d generate first.

Registry
IToolCapabilityAdapter.cs

IToolRegistry.cs

ToolDescriptor.cs

ToolCapabilityDescriptor.cs

ToolHealthReport.cs

ToolRegistry.cs

Jobs
IToolJobQueue.cs

IToolJobRunner.cs

IToolJobStore.cs

ToolJobRecord.cs

ToolExecutionRequest.cs

ToolExecutionResult.cs

ToolJobQueue.cs

ToolJobRunner.cs

Logs + Artifacts
ToolLogRecord.cs

ToolArtifactRecord.cs

IArtifactStore.cs

ArtifactStore.cs

Validation
ValidationIssue.cs

ValidationReport.cs

IValidationReportStore.cs

AtlasAI bridge
AtlasAIToolRequest.cs

AtlasAIToolPlan.cs

IAtlasAIToolPlanner.cs

IAtlasAIToolExecutor.cs

Commands
QueueToolJobCommand.cs

CheckToolHealthCommand.cs

RefreshToolRegistryCommand.cs

RegisterArtifactCommand.cs

PublishValidationReportCommand.cs

15. Biggest remaining gap after this
Once this exists, the next major missing layer is:

policy + permissioning for tool actions

Meaning:

who can run what

what AtlasAI can run automatically

what requires approval

which paths/files/tools are protected

what counts as destructive

That should be the layer immediately after the job/tool foundation.

Strongest next move
The best next step is to generate the actual C# scaffold pack for:

Tool registry

Tool job queue

Artifact system

Validation system

AtlasAI tool planner bridge

That would give you the first implementation-ready code backbone for this entire tooling layer.


next

Perfect — let’s move from architecture into the actual implementation scaffold.

Atlas Suite — C# Scaffold Pack
This is the next layer after the spec:

exact project structure

core interfaces

core models

starter services

first commands

first adapters

first UI targets

Using your updated naming:

Atlas Suite = tooling shell

AtlasAI = integrated AI system

1. Suggested project structure
src/
├── AtlasSuite.Core/
│   ├── Results/
│   ├── Events/
│   ├── Models/
│   └── Interfaces/
├── AtlasSuite.Commanding/
│   ├── Commands/
│   ├── Handlers/
│   ├── Validators/
│   └── Services/
├── AtlasSuite.Tooling.Registry/
│   ├── Models/
│   ├── Interfaces/
│   └── Services/
├── AtlasSuite.Tooling.Jobs/
│   ├── Models/
│   ├── Interfaces/
│   └── Services/
├── AtlasSuite.Tooling.Artifacts/
│   ├── Models/
│   ├── Interfaces/
│   └── Services/
├── AtlasSuite.Tooling.Validation/
│   ├── Models/
│   ├── Interfaces/
│   └── Services/
├── AtlasSuite.Tooling.Search/
│   ├── Adapters/
│   └── Commands/
├── AtlasSuite.Tooling.Parse/
│   ├── Adapters/
│   └── Commands/
├── AtlasSuite.Tooling.Build/
│   ├── Adapters/
│   └── Commands/
├── AtlasSuite.AtlasAI/
│   ├── Models/
│   ├── Interfaces/
│   └── Services/
├── AtlasSuite.Storage.Sqlite/
│   ├── Interfaces/
│   └── Services/
└── AtlasSuite.Shell/
    ├── Panels/
    ├── ViewModels/
    └── Services/
2. Core enums
ToolHealthStatus.cs
namespace AtlasSuite.Tooling.Registry.Models;

public enum ToolHealthStatus
{
    Unknown = 0,
    Healthy = 1,
    Warning = 2,
    Missing = 3,
    Error = 4
}
ToolJobStatus.cs
namespace AtlasSuite.Tooling.Jobs.Models;

public enum ToolJobStatus
{
    Created = 0,
    Queued = 1,
    Preparing = 2,
    Running = 3,
    Succeeded = 4,
    Failed = 5,
    Cancelled = 6,
    Archived = 7
}
LogSeverity.cs
namespace AtlasSuite.Tooling.Jobs.Models;

public enum LogSeverity
{
    Trace = 0,
    Info = 1,
    Warning = 2,
    Error = 3,
    Critical = 4
}
3. Tool registry core files
ToolCapabilityDescriptor.cs
namespace AtlasSuite.Tooling.Registry.Models;

public sealed class ToolCapabilityDescriptor
{
    public string CapabilityId { get; init; } = string.Empty;
    public string DisplayName { get; init; } = string.Empty;
    public string Description { get; init; } = string.Empty;
    public IReadOnlyList<string> SupportedRequestKinds { get; init; } = Array.Empty<string>();
    public bool SupportsDryRun { get; init; }
    public bool ProducesArtifacts { get; init; }
    public bool ProducesStructuredData { get; init; }
}
ToolDescriptor.cs
namespace AtlasSuite.Tooling.Registry.Models;

public sealed class ToolDescriptor
{
    public string ToolId { get; init; } = string.Empty;
    public string DisplayName { get; init; } = string.Empty;
    public string Category { get; init; } = string.Empty;
    public string ProviderModuleId { get; init; } = string.Empty;
    public string ExecutablePath { get; init; } = string.Empty;
    public string Version { get; init; } = string.Empty;
    public ToolHealthStatus HealthStatus { get; init; } = ToolHealthStatus.Unknown;
    public IReadOnlyList<ToolCapabilityDescriptor> Capabilities { get; init; } = Array.Empty<ToolCapabilityDescriptor>();
    public DateTimeOffset LastCheckedUtc { get; init; } = DateTimeOffset.UtcNow;
}
ToolHealthReport.cs
namespace AtlasSuite.Tooling.Registry.Models;

public sealed class ToolHealthReport
{
    public string ToolId { get; init; } = string.Empty;
    public ToolHealthStatus Status { get; init; } = ToolHealthStatus.Unknown;
    public string Version { get; init; } = string.Empty;
    public string Message { get; init; } = string.Empty;
    public string ExecutablePath { get; init; } = string.Empty;
    public IReadOnlyList<string> Warnings { get; init; } = Array.Empty<string>();
}
IToolCapabilityAdapter.cs
using AtlasSuite.Tooling.Jobs.Models;
using AtlasSuite.Tooling.Registry.Models;

namespace AtlasSuite.Tooling.Registry.Interfaces;

public interface IToolCapabilityAdapter
{
    string ToolId { get; }
    string DisplayName { get; }

    Task<ToolHealthReport> CheckHealthAsync(CancellationToken ct);
    Task<IReadOnlyList<ToolCapabilityDescriptor>> GetCapabilitiesAsync(CancellationToken ct);
    Task<ToolExecutionResult> ExecuteAsync(ToolExecutionRequest request, CancellationToken ct);
}
IToolRegistry.cs
using AtlasSuite.Tooling.Registry.Models;

namespace AtlasSuite.Tooling.Registry.Interfaces;

public interface IToolRegistry
{
    Task RefreshAsync(CancellationToken ct);
    Task<IReadOnlyList<ToolDescriptor>> GetAllAsync(CancellationToken ct);
    Task<ToolDescriptor?> GetByIdAsync(string toolId, CancellationToken ct);
    Task<IToolCapabilityAdapter?> GetAdapterAsync(string toolId, CancellationToken ct);
}
ToolRegistry.cs
using AtlasSuite.Tooling.Registry.Interfaces;
using AtlasSuite.Tooling.Registry.Models;

namespace AtlasSuite.Tooling.Registry.Services;

public sealed class ToolRegistry : IToolRegistry
{
    private readonly IReadOnlyList<IToolCapabilityAdapter> _adapters;
    private readonly Dictionary<string, ToolDescriptor> _cache = new(StringComparer.OrdinalIgnoreCase);

    public ToolRegistry(IEnumerable<IToolCapabilityAdapter> adapters)
    {
        _adapters = adapters.ToList();
    }

    public async Task RefreshAsync(CancellationToken ct)
    {
        _cache.Clear();

        foreach (var adapter in _adapters)
        {
            var health = await adapter.CheckHealthAsync(ct);
            var capabilities = await adapter.GetCapabilitiesAsync(ct);

            _cache[adapter.ToolId] = new ToolDescriptor
            {
                ToolId = adapter.ToolId,
                DisplayName = adapter.DisplayName,
                Category = InferCategory(adapter.ToolId),
                ProviderModuleId = $"module.{adapter.ToolId}",
                ExecutablePath = health.ExecutablePath,
                Version = health.Version,
                HealthStatus = health.Status,
                Capabilities = capabilities,
                LastCheckedUtc = DateTimeOffset.UtcNow
            };
        }
    }

    public Task<IReadOnlyList<ToolDescriptor>> GetAllAsync(CancellationToken ct)
        => Task.FromResult<IReadOnlyList<ToolDescriptor>>(_cache.Values.OrderBy(x => x.ToolId).ToList());

    public Task<ToolDescriptor?> GetByIdAsync(string toolId, CancellationToken ct)
    {
        _cache.TryGetValue(toolId, out var descriptor);
        return Task.FromResult(descriptor);
    }

    public Task<IToolCapabilityAdapter?> GetAdapterAsync(string toolId, CancellationToken ct)
    {
        var adapter = _adapters.FirstOrDefault(x => string.Equals(x.ToolId, toolId, StringComparison.OrdinalIgnoreCase));
        return Task.FromResult(adapter);
    }

    private static string InferCategory(string toolId)
    {
        if (toolId.Contains("search", StringComparison.OrdinalIgnoreCase)) return "Search";
        if (toolId.Contains("parse", StringComparison.OrdinalIgnoreCase)) return "Parse";
        if (toolId.Contains("build", StringComparison.OrdinalIgnoreCase)) return "Build";
        return "General";
    }
}
4. Job system core files
ToolExecutionRequest.cs
namespace AtlasSuite.Tooling.Jobs.Models;

public sealed class ToolExecutionRequest
{
    public string RequestId { get; init; } = Guid.NewGuid().ToString("N");
    public string ToolId { get; init; } = string.Empty;
    public string CapabilityId { get; init; } = string.Empty;
    public string RequestKind { get; init; } = string.Empty;
    public string WorkspaceRoot { get; init; } = string.Empty;
    public bool IsDryRun { get; init; }
    public IReadOnlyDictionary<string, string> Parameters { get; init; } = new Dictionary<string, string>();
    public IReadOnlyList<string> InputPaths { get; init; } = Array.Empty<string>();
    public IReadOnlyList<string> ExpectedOutputPaths { get; init; } = Array.Empty<string>();
    public string RequestedBy { get; init; } = string.Empty;
    public string CorrelationId { get; init; } = string.Empty;
}
ToolLogRecord.cs
namespace AtlasSuite.Tooling.Jobs.Models;

public sealed class ToolLogRecord
{
    public DateTimeOffset TimestampUtc { get; init; } = DateTimeOffset.UtcNow;
    public string JobId { get; init; } = string.Empty;
    public string ToolId { get; init; } = string.Empty;
    public LogSeverity Severity { get; init; } = LogSeverity.Info;
    public string Message { get; init; } = string.Empty;
    public string? SourcePath { get; init; }
    public int? SourceLine { get; init; }
}
ToolArtifactRecord.cs
namespace AtlasSuite.Tooling.Artifacts.Models;

public sealed class ToolArtifactRecord
{
    public string ArtifactId { get; init; } = Guid.NewGuid().ToString("N");
    public string JobId { get; init; } = string.Empty;
    public string ArtifactType { get; init; } = string.Empty;
    public string DisplayName { get; init; } = string.Empty;
    public string FilePath { get; init; } = string.Empty;
    public string ProducedByToolId { get; init; } = string.Empty;
    public long SizeBytes { get; init; }
    public string ContentHash { get; init; } = string.Empty;
    public DateTimeOffset CreatedUtc { get; init; } = DateTimeOffset.UtcNow;
}
ToolExecutionResult.cs
using AtlasSuite.Tooling.Artifacts.Models;

namespace AtlasSuite.Tooling.Jobs.Models;

public sealed class ToolExecutionResult
{
    public bool Success { get; init; }
    public string ToolId { get; init; } = string.Empty;
    public string CapabilityId { get; init; } = string.Empty;
    public int ExitCode { get; init; }
    public string Summary { get; init; } = string.Empty;
    public IReadOnlyList<string> Warnings { get; init; } = Array.Empty<string>();
    public IReadOnlyList<string> Errors { get; init; } = Array.Empty<string>();
    public IReadOnlyList<ToolArtifactRecord> Artifacts { get; init; } = Array.Empty<ToolArtifactRecord>();
    public IReadOnlyList<ToolLogRecord> Logs { get; init; } = Array.Empty<ToolLogRecord>();
    public IReadOnlyDictionary<string, string> StructuredData { get; init; } = new Dictionary<string, string>();
    public TimeSpan Duration { get; init; } = TimeSpan.Zero;
}
ToolJobRecord.cs
namespace AtlasSuite.Tooling.Jobs.Models;

public sealed class ToolJobRecord
{
    public string JobId { get; init; } = Guid.NewGuid().ToString("N");
    public string Title { get; init; } = string.Empty;
    public string ToolId { get; init; } = string.Empty;
    public string CapabilityId { get; init; } = string.Empty;
    public ToolJobStatus Status { get; set; } = ToolJobStatus.Created;
    public string RequestedBy { get; init; } = string.Empty;
    public string CorrelationId { get; init; } = string.Empty;
    public int ProgressPercent { get; set; }
    public DateTimeOffset CreatedUtc { get; init; } = DateTimeOffset.UtcNow;
    public DateTimeOffset? StartedUtc { get; set; }
    public DateTimeOffset? FinishedUtc { get; set; }
    public int RetryCount { get; set; }
    public string Summary { get; set; } = string.Empty;
}
IToolJobStore.cs
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Tooling.Jobs.Interfaces;

public interface IToolJobStore
{
    Task SaveAsync(ToolJobRecord record, CancellationToken ct);
    Task<ToolJobRecord?> GetAsync(string jobId, CancellationToken ct);
    Task<IReadOnlyList<ToolJobRecord>> GetRecentAsync(int count, CancellationToken ct);
}
IToolJobQueue.cs
namespace AtlasSuite.Tooling.Jobs.Interfaces;

public interface IToolJobQueue
{
    Task<string> EnqueueAsync(Models.ToolExecutionRequest request, string title, CancellationToken ct);
    Task CancelAsync(string jobId, CancellationToken ct);
    Task RetryAsync(string jobId, CancellationToken ct);
}
IToolJobRunner.cs
namespace AtlasSuite.Tooling.Jobs.Interfaces;

public interface IToolJobRunner
{
    Task RunAsync(string jobId, CancellationToken ct);
}
InMemoryToolJobStore.cs
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Tooling.Jobs.Services;

public sealed class InMemoryToolJobStore : IToolJobStore
{
    private readonly Dictionary<string, ToolJobRecord> _jobs = new(StringComparer.OrdinalIgnoreCase);

    public Task SaveAsync(ToolJobRecord record, CancellationToken ct)
    {
        _jobs[record.JobId] = record;
        return Task.CompletedTask;
    }

    public Task<ToolJobRecord?> GetAsync(string jobId, CancellationToken ct)
    {
        _jobs.TryGetValue(jobId, out var record);
        return Task.FromResult(record);
    }

    public Task<IReadOnlyList<ToolJobRecord>> GetRecentAsync(int count, CancellationToken ct)
    {
        var result = _jobs.Values
            .OrderByDescending(x => x.CreatedUtc)
            .Take(count)
            .ToList();

        return Task.FromResult<IReadOnlyList<ToolJobRecord>>(result);
    }
}
ToolJobQueue.cs
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Tooling.Jobs.Services;

public sealed class ToolJobQueue : IToolJobQueue
{
    private readonly IToolJobStore _store;
    private readonly Dictionary<string, ToolExecutionRequest> _requests = new(StringComparer.OrdinalIgnoreCase);

    public ToolJobQueue(IToolJobStore store)
    {
        _store = store;
    }

    public async Task<string> EnqueueAsync(ToolExecutionRequest request, string title, CancellationToken ct)
    {
        var job = new ToolJobRecord
        {
            Title = title,
            ToolId = request.ToolId,
            CapabilityId = request.CapabilityId,
            Status = ToolJobStatus.Queued,
            RequestedBy = request.RequestedBy,
            CorrelationId = request.CorrelationId
        };

        _requests[job.JobId] = request;
        await _store.SaveAsync(job, ct);
        return job.JobId;
    }

    public async Task CancelAsync(string jobId, CancellationToken ct)
    {
        var job = await _store.GetAsync(jobId, ct);
        if (job is null)
            return;

        job.Status = ToolJobStatus.Cancelled;
        job.FinishedUtc = DateTimeOffset.UtcNow;
        job.Summary = "Job cancelled.";
        await _store.SaveAsync(job, ct);
    }

    public async Task RetryAsync(string jobId, CancellationToken ct)
    {
        var job = await _store.GetAsync(jobId, ct);
        if (job is null)
            return;

        job.Status = ToolJobStatus.Queued;
        job.ProgressPercent = 0;
        job.FinishedUtc = null;
        job.RetryCount++;
        job.Summary = "Job re-queued.";
        await _store.SaveAsync(job, ct);
    }

    public ToolExecutionRequest? GetRequest(string jobId)
        => _requests.TryGetValue(jobId, out var request) ? request : null;
}
ToolJobRunner.cs
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Models;
using AtlasSuite.Tooling.Registry.Interfaces;

namespace AtlasSuite.Tooling.Jobs.Services;

public sealed class ToolJobRunner : IToolJobRunner
{
    private readonly IToolJobStore _store;
    private readonly IToolRegistry _registry;
    private readonly ToolJobQueue _queue;

    public ToolJobRunner(
        IToolJobStore store,
        IToolRegistry registry,
        ToolJobQueue queue)
    {
        _store = store;
        _registry = registry;
        _queue = queue;
    }

    public async Task RunAsync(string jobId, CancellationToken ct)
    {
        var job = await _store.GetAsync(jobId, ct);
        if (job is null)
            return;

        var request = _queue.GetRequest(jobId);
        if (request is null)
        {
            job.Status = ToolJobStatus.Failed;
            job.Summary = "No execution request found.";
            job.FinishedUtc = DateTimeOffset.UtcNow;
            await _store.SaveAsync(job, ct);
            return;
        }

        var adapter = await _registry.GetAdapterAsync(request.ToolId, ct);
        if (adapter is null)
        {
            job.Status = ToolJobStatus.Failed;
            job.Summary = $"No adapter found for tool '{request.ToolId}'.";
            job.FinishedUtc = DateTimeOffset.UtcNow;
            await _store.SaveAsync(job, ct);
            return;
        }

        job.Status = ToolJobStatus.Running;
        job.StartedUtc = DateTimeOffset.UtcNow;
        job.ProgressPercent = 5;
        await _store.SaveAsync(job, ct);

        var result = await adapter.ExecuteAsync(request, ct);

        job.ProgressPercent = 100;
        job.FinishedUtc = DateTimeOffset.UtcNow;
        job.Status = result.Success ? ToolJobStatus.Succeeded : ToolJobStatus.Failed;
        job.Summary = result.Summary;

        await _store.SaveAsync(job, ct);
    }
}
5. Validation core files
ValidationIssue.cs
namespace AtlasSuite.Tooling.Validation.Models;

public sealed class ValidationIssue
{
    public string IssueId { get; init; } = Guid.NewGuid().ToString("N");
    public string RuleId { get; init; } = string.Empty;
    public string Severity { get; init; } = string.Empty;
    public string Category { get; init; } = string.Empty;
    public string Message { get; init; } = string.Empty;
    public string? FilePath { get; init; }
    public int? LineNumber { get; init; }
    public string? SuggestedFix { get; init; }
}
ValidationReport.cs
namespace AtlasSuite.Tooling.Validation.Models;

public sealed class ValidationReport
{
    public string ReportId { get; init; } = Guid.NewGuid().ToString("N");
    public string JobId { get; init; } = string.Empty;
    public string SourceToolId { get; init; } = string.Empty;
    public bool Success { get; init; }
    public IReadOnlyList<ValidationIssue> Issues { get; init; } = Array.Empty<ValidationIssue>();
    public string Summary { get; init; } = string.Empty;
}
6. AtlasAI bridge core files
AtlasAIToolRequest.cs
namespace AtlasSuite.AtlasAI.Models;

public sealed class AtlasAIToolRequest
{
    public string Goal { get; init; } = string.Empty;
    public string Scope { get; init; } = string.Empty;
    public bool DryRun { get; init; }
    public IReadOnlyList<string> Constraints { get; init; } = Array.Empty<string>();
    public string RequestedBy { get; init; } = "AtlasAI";
}
AtlasAIToolPlanStep.cs
namespace AtlasSuite.AtlasAI.Models;

public sealed class AtlasAIToolPlanStep
{
    public int Order { get; init; }
    public string ToolId { get; init; } = string.Empty;
    public string CapabilityId { get; init; } = string.Empty;
    public string RequestKind { get; init; } = string.Empty;
    public string Description { get; init; } = string.Empty;
    public IReadOnlyDictionary<string, string> Parameters { get; init; } = new Dictionary<string, string>();
}
AtlasAIToolPlan.cs
namespace AtlasSuite.AtlasAI.Models;

public sealed class AtlasAIToolPlan
{
    public string PlanId { get; init; } = Guid.NewGuid().ToString("N");
    public string Goal { get; init; } = string.Empty;
    public bool DryRun { get; init; }
    public IReadOnlyList<AtlasAIToolPlanStep> Steps { get; init; } = Array.Empty<AtlasAIToolPlanStep>();
}
IAtlasAIToolPlanner.cs
using AtlasSuite.AtlasAI.Models;

namespace AtlasSuite.AtlasAI.Interfaces;

public interface IAtlasAIToolPlanner
{
    Task<AtlasAIToolPlan> BuildPlanAsync(AtlasAIToolRequest request, CancellationToken ct);
}
IAtlasAIToolExecutor.cs
using AtlasSuite.AtlasAI.Models;

namespace AtlasSuite.AtlasAI.Interfaces;

public interface IAtlasAIToolExecutor
{
    Task ExecutePlanAsync(AtlasAIToolPlan plan, CancellationToken ct);
}
AtlasAIToolPlanner.cs
using AtlasSuite.AtlasAI.Interfaces;
using AtlasSuite.AtlasAI.Models;

namespace AtlasSuite.AtlasAI.Services;

public sealed class AtlasAIToolPlanner : IAtlasAIToolPlanner
{
    public Task<AtlasAIToolPlan> BuildPlanAsync(AtlasAIToolRequest request, CancellationToken ct)
    {
        var steps = new List<AtlasAIToolPlanStep>
        {
            new()
            {
                Order = 1,
                ToolId = "tool.search.ripgrep",
                CapabilityId = "cap.search.workspace",
                RequestKind = "Inspect",
                Description = $"Search workspace for scope: {request.Scope}",
                Parameters = new Dictionary<string, string>
                {
                    ["query"] = request.Scope
                }
            }
        };

        return Task.FromResult(new AtlasAIToolPlan
        {
            Goal = request.Goal,
            DryRun = request.DryRun,
            Steps = steps
        });
    }
}
7. First concrete adapters
RipgrepAdapter.cs
using AtlasSuite.Tooling.Jobs.Models;
using AtlasSuite.Tooling.Registry.Interfaces;
using AtlasSuite.Tooling.Registry.Models;

namespace AtlasSuite.Tooling.Search.Adapters;

public sealed class RipgrepAdapter : IToolCapabilityAdapter
{
    public string ToolId => "tool.search.ripgrep";
    public string DisplayName => "ripgrep Search";

    public Task<ToolHealthReport> CheckHealthAsync(CancellationToken ct)
    {
        return Task.FromResult(new ToolHealthReport
        {
            ToolId = ToolId,
            Status = ToolHealthStatus.Healthy,
            Version = "detected-at-runtime",
            Message = "ripgrep adapter ready",
            ExecutablePath = "rg"
        });
    }

    public Task<IReadOnlyList<ToolCapabilityDescriptor>> GetCapabilitiesAsync(CancellationToken ct)
    {
        IReadOnlyList<ToolCapabilityDescriptor> capabilities =
        [
            new ToolCapabilityDescriptor
            {
                CapabilityId = "cap.search.workspace",
                DisplayName = "Workspace Search",
                Description = "Searches the workspace for text matches.",
                SupportedRequestKinds = new[] { "Inspect", "Validate" },
                SupportsDryRun = true,
                ProducesArtifacts = false,
                ProducesStructuredData = true
            }
        ];

        return Task.FromResult(capabilities);
    }

    public Task<ToolExecutionResult> ExecuteAsync(ToolExecutionRequest request, CancellationToken ct)
    {
        var logs = new List<ToolLogRecord>
        {
            new()
            {
                ToolId = ToolId,
                Severity = LogSeverity.Info,
                Message = $"Search request received: {request.Parameters.GetValueOrDefault("query", "")}"
            }
        };

        return Task.FromResult(new ToolExecutionResult
        {
            Success = true,
            ToolId = ToolId,
            CapabilityId = request.CapabilityId,
            ExitCode = 0,
            Summary = "Search completed.",
            Logs = logs,
            StructuredData = new Dictionary<string, string>
            {
                ["matches"] = "0"
            },
            Duration = TimeSpan.FromMilliseconds(50)
        });
    }
}
TreeSitterAdapter.cs
using AtlasSuite.Tooling.Jobs.Models;
using AtlasSuite.Tooling.Registry.Interfaces;
using AtlasSuite.Tooling.Registry.Models;

namespace AtlasSuite.Tooling.Parse.Adapters;

public sealed class TreeSitterAdapter : IToolCapabilityAdapter
{
    public string ToolId => "tool.parse.treesitter";
    public string DisplayName => "Tree-sitter Parser";

    public Task<ToolHealthReport> CheckHealthAsync(CancellationToken ct)
    {
        return Task.FromResult(new ToolHealthReport
        {
            ToolId = ToolId,
            Status = ToolHealthStatus.Healthy,
            Version = "detected-at-runtime",
            Message = "tree-sitter adapter ready",
            ExecutablePath = "embedded-or-bridge"
        });
    }

    public Task<IReadOnlyList<ToolCapabilityDescriptor>> GetCapabilitiesAsync(CancellationToken ct)
    {
        IReadOnlyList<ToolCapabilityDescriptor> capabilities =
        [
            new ToolCapabilityDescriptor
            {
                CapabilityId = "cap.parse.symbols",
                DisplayName = "Parse File Symbols",
                Description = "Parses source files into structured symbols.",
                SupportedRequestKinds = new[] { "Inspect", "Validate" },
                SupportsDryRun = true,
                ProducesArtifacts = false,
                ProducesStructuredData = true
            }
        ];

        return Task.FromResult(capabilities);
    }

    public Task<ToolExecutionResult> ExecuteAsync(ToolExecutionRequest request, CancellationToken ct)
    {
        return Task.FromResult(new ToolExecutionResult
        {
            Success = true,
            ToolId = ToolId,
            CapabilityId = request.CapabilityId,
            ExitCode = 0,
            Summary = "Parse completed.",
            StructuredData = new Dictionary<string, string>
            {
                ["symbolCount"] = "0"
            },
            Duration = TimeSpan.FromMilliseconds(25)
        });
    }
}
8. First commands to add
RefreshToolRegistryCommand.cs
namespace AtlasSuite.Tooling.Registry.Commands;

public sealed record RefreshToolRegistryCommand;
QueueToolJobCommand.cs
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Tooling.Jobs.Commands;

public sealed record QueueToolJobCommand(
    ToolExecutionRequest Request,
    string Title);
CheckToolHealthCommand.cs
namespace AtlasSuite.Tooling.Registry.Commands;

public sealed record CheckToolHealthCommand(string ToolId);
9. First DI registration
ServiceCollectionExtensions.cs
using AtlasSuite.AtlasAI.Interfaces;
using AtlasSuite.AtlasAI.Services;
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Services;
using AtlasSuite.Tooling.Parse.Adapters;
using AtlasSuite.Tooling.Registry.Interfaces;
using AtlasSuite.Tooling.Registry.Services;
using AtlasSuite.Tooling.Search.Adapters;
using Microsoft.Extensions.DependencyInjection;

namespace AtlasSuite.Shell.Services;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddAtlasSuiteCore(this IServiceCollection services)
    {
        services.AddSingleton<IToolCapabilityAdapter, RipgrepAdapter>();
        services.AddSingleton<IToolCapabilityAdapter, TreeSitterAdapter>();

        services.AddSingleton<IToolRegistry, ToolRegistry>();

        services.AddSingleton<IToolJobStore, InMemoryToolJobStore>();
        services.AddSingleton<ToolJobQueue>();
        services.AddSingleton<IToolJobQueue>(sp => sp.GetRequiredService<ToolJobQueue>());
        services.AddSingleton<IToolJobRunner, ToolJobRunner>();

        services.AddSingleton<IAtlasAIToolPlanner, AtlasAIToolPlanner>();

        return services;
    }
}
10. First WPF panels to build
Do these before trying to get fancy.

Tool Registry Panel
Display:

ToolId

DisplayName

HealthStatus

Version

ExecutablePath

Job Queue Panel
Display:

JobId

Title

ToolId

Status

ProgressPercent

Summary

AtlasAI Plan Panel
Display:

Goal

DryRun

Step list

ToolId

CapabilityId

Description

Diagnostics Panel
Display:

recent logs

adapter health issues

failed jobs

11. What is still missing after this scaffold?
After this first scaffold, the next immediate gaps are:

A. SQLite-backed persistence
Right now the job store is in-memory only.

B. Real process execution
The adapters are placeholders and need:

process launching

stdout/stderr capture

exit code handling

timeout handling

C. Artifact store
We have the model, but not the service.

D. Validation report store
Same thing — models exist, persistence/service not yet built.

E. AtlasAI execution engine
Planner exists, executor still needs to queue and run steps.

F. Build adapter
You’ll want this right after search + parse.

12. Best next implementation order
I’d build the next set in this order:

SQLite job store

real process runner abstraction

Build adapter for CMake/Ninja

AtlasAI plan executor

artifact store

validation report store

Blender adapter base

tool registry panel + job queue panel

That gives you the first usable vertical slice.

13. Strongest next deliverable
The next thing to generate should be:

Phase 2 scaffold pack

SQLite-backed stores

process runner abstraction

CMake/Ninja build adapter

AtlasAI executor

artifact store

That would move Atlas Suite from “structured prototype” to “early functional platform.”


next

Absolutely — here’s the Phase 2 scaffold pack.

This is the point where Atlas Suite starts becoming actually functional, not just well-structured.

Atlas Suite — Phase 2 Scaffold Pack
This layer adds:

SQLite-backed persistence

real process runner abstraction

CMake/Ninja build adapter

AtlasAI tool executor

artifact store

validation report store

Using your current naming:

Atlas Suite = tooling shell/platform

AtlasAI = integrated AI system

1. Updated project structure
Add these folders/projects on top of the prior scaffold:

src/
├── AtlasSuite.Storage.Sqlite/
│   ├── Interfaces/
│   ├── Models/
│   ├── Services/
│   └── Sql/
├── AtlasSuite.Tooling.Process/
│   ├── Interfaces/
│   ├── Models/
│   └── Services/
├── AtlasSuite.Tooling.Build/
│   ├── Adapters/
│   ├── Models/
│   └── Services/
├── AtlasSuite.Tooling.Artifacts/
│   ├── Interfaces/
│   ├── Models/
│   └── Services/
├── AtlasSuite.Tooling.Validation/
│   ├── Interfaces/
│   ├── Models/
│   └── Services/
└── AtlasSuite.AtlasAI/
    ├── Interfaces/
    ├── Models/
    └── Services/
2. SQLite persistence layer
For early implementation, keep it simple and explicit.

ISqliteConnectionFactory.cs
using Microsoft.Data.Sqlite;

namespace AtlasSuite.Storage.Sqlite.Interfaces;

public interface ISqliteConnectionFactory
{
    SqliteConnection CreateConnection();
}
SqliteOptions.cs
namespace AtlasSuite.Storage.Sqlite.Models;

public sealed class SqliteOptions
{
    public string DatabasePath { get; init; } = "atlas_suite.db";
}
SqliteConnectionFactory.cs
using AtlasSuite.Storage.Sqlite.Interfaces;
using AtlasSuite.Storage.Sqlite.Models;
using Microsoft.Data.Sqlite;

namespace AtlasSuite.Storage.Sqlite.Services;

public sealed class SqliteConnectionFactory : ISqliteConnectionFactory
{
    private readonly string _connectionString;

    public SqliteConnectionFactory(SqliteOptions options)
    {
        var builder = new SqliteConnectionStringBuilder
        {
            DataSource = options.DatabasePath,
            Mode = SqliteOpenMode.ReadWriteCreate,
            Cache = SqliteCacheMode.Shared
        };

        _connectionString = builder.ToString();
    }

    public SqliteConnection CreateConnection()
        => new(_connectionString);
}
SqliteDatabaseInitializer.cs
using AtlasSuite.Storage.Sqlite.Interfaces;

namespace AtlasSuite.Storage.Sqlite.Services;

public sealed class SqliteDatabaseInitializer
{
    private readonly ISqliteConnectionFactory _factory;

    public SqliteDatabaseInitializer(ISqliteConnectionFactory factory)
    {
        _factory = factory;
    }

    public async Task InitializeAsync(CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var sql = """
        CREATE TABLE IF NOT EXISTS tool_jobs (
            job_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            tool_id TEXT NOT NULL,
            capability_id TEXT NOT NULL,
            status INTEGER NOT NULL,
            requested_by TEXT NOT NULL,
            correlation_id TEXT NOT NULL,
            progress_percent INTEGER NOT NULL,
            created_utc TEXT NOT NULL,
            started_utc TEXT NULL,
            finished_utc TEXT NULL,
            retry_count INTEGER NOT NULL,
            summary TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tool_artifacts (
            artifact_id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL,
            artifact_type TEXT NOT NULL,
            display_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            produced_by_tool_id TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            content_hash TEXT NOT NULL,
            created_utc TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS validation_reports (
            report_id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL,
            source_tool_id TEXT NOT NULL,
            success INTEGER NOT NULL,
            summary TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS validation_issues (
            issue_id TEXT PRIMARY KEY,
            report_id TEXT NOT NULL,
            rule_id TEXT NOT NULL,
            severity TEXT NOT NULL,
            category TEXT NOT NULL,
            message TEXT NOT NULL,
            file_path TEXT NULL,
            line_number INTEGER NULL,
            suggested_fix TEXT NULL
        );
        """;

        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        await command.ExecuteNonQueryAsync(ct);
    }
}
3. SQLite-backed job store
SqliteToolJobStore.cs
using AtlasSuite.Storage.Sqlite.Interfaces;
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Models;
using Microsoft.Data.Sqlite;

namespace AtlasSuite.Storage.Sqlite.Services;

public sealed class SqliteToolJobStore : IToolJobStore
{
    private readonly ISqliteConnectionFactory _factory;

    public SqliteToolJobStore(ISqliteConnectionFactory factory)
    {
        _factory = factory;
    }

    public async Task SaveAsync(ToolJobRecord record, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var sql = """
        INSERT INTO tool_jobs (
            job_id, title, tool_id, capability_id, status, requested_by, correlation_id,
            progress_percent, created_utc, started_utc, finished_utc, retry_count, summary
        )
        VALUES (
            $job_id, $title, $tool_id, $capability_id, $status, $requested_by, $correlation_id,
            $progress_percent, $created_utc, $started_utc, $finished_utc, $retry_count, $summary
        )
        ON CONFLICT(job_id) DO UPDATE SET
            title = excluded.title,
            tool_id = excluded.tool_id,
            capability_id = excluded.capability_id,
            status = excluded.status,
            requested_by = excluded.requested_by,
            correlation_id = excluded.correlation_id,
            progress_percent = excluded.progress_percent,
            created_utc = excluded.created_utc,
            started_utc = excluded.started_utc,
            finished_utc = excluded.finished_utc,
            retry_count = excluded.retry_count,
            summary = excluded.summary;
        """;

        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        command.Parameters.AddWithValue("$job_id", record.JobId);
        command.Parameters.AddWithValue("$title", record.Title);
        command.Parameters.AddWithValue("$tool_id", record.ToolId);
        command.Parameters.AddWithValue("$capability_id", record.CapabilityId);
        command.Parameters.AddWithValue("$status", (int)record.Status);
        command.Parameters.AddWithValue("$requested_by", record.RequestedBy);
        command.Parameters.AddWithValue("$correlation_id", record.CorrelationId);
        command.Parameters.AddWithValue("$progress_percent", record.ProgressPercent);
        command.Parameters.AddWithValue("$created_utc", record.CreatedUtc.UtcDateTime.ToString("O"));
        command.Parameters.AddWithValue("$started_utc", record.StartedUtc?.UtcDateTime.ToString("O") ?? (object)DBNull.Value);
        command.Parameters.AddWithValue("$finished_utc", record.FinishedUtc?.UtcDateTime.ToString("O") ?? (object)DBNull.Value);
        command.Parameters.AddWithValue("$retry_count", record.RetryCount);
        command.Parameters.AddWithValue("$summary", record.Summary);

        await command.ExecuteNonQueryAsync(ct);
    }

    public async Task<ToolJobRecord?> GetAsync(string jobId, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var sql = "SELECT * FROM tool_jobs WHERE job_id = $job_id LIMIT 1;";
        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        command.Parameters.AddWithValue("$job_id", jobId);

        await using var reader = await command.ExecuteReaderAsync(ct);
        if (!await reader.ReadAsync(ct))
            return null;

        return Map(reader);
    }

    public async Task<IReadOnlyList<ToolJobRecord>> GetRecentAsync(int count, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var sql = "SELECT * FROM tool_jobs ORDER BY created_utc DESC LIMIT $count;";
        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        command.Parameters.AddWithValue("$count", count);

        var results = new List<ToolJobRecord>();
        await using var reader = await command.ExecuteReaderAsync(ct);
        while (await reader.ReadAsync(ct))
            results.Add(Map(reader));

        return results;
    }

    private static ToolJobRecord Map(SqliteDataReader reader)
    {
        return new ToolJobRecord
        {
            JobId = reader.GetString(reader.GetOrdinal("job_id")),
            Title = reader.GetString(reader.GetOrdinal("title")),
            ToolId = reader.GetString(reader.GetOrdinal("tool_id")),
            CapabilityId = reader.GetString(reader.GetOrdinal("capability_id")),
            Status = (ToolJobStatus)reader.GetInt32(reader.GetOrdinal("status")),
            RequestedBy = reader.GetString(reader.GetOrdinal("requested_by")),
            CorrelationId = reader.GetString(reader.GetOrdinal("correlation_id")),
            ProgressPercent = reader.GetInt32(reader.GetOrdinal("progress_percent")),
            CreatedUtc = DateTimeOffset.Parse(reader.GetString(reader.GetOrdinal("created_utc"))),
            StartedUtc = reader.IsDBNull(reader.GetOrdinal("started_utc"))
                ? null
                : DateTimeOffset.Parse(reader.GetString(reader.GetOrdinal("started_utc"))),
            FinishedUtc = reader.IsDBNull(reader.GetOrdinal("finished_utc"))
                ? null
                : DateTimeOffset.Parse(reader.GetString(reader.GetOrdinal("finished_utc"))),
            RetryCount = reader.GetInt32(reader.GetOrdinal("retry_count")),
            Summary = reader.GetString(reader.GetOrdinal("summary"))
        };
    }
}
4. Process runner abstraction
This is critical because every external tool adapter will need it.

ProcessExecutionRequest.cs
namespace AtlasSuite.Tooling.Process.Models;

public sealed class ProcessExecutionRequest
{
    public string FileName { get; init; } = string.Empty;
    public string Arguments { get; init; } = string.Empty;
    public string WorkingDirectory { get; init; } = string.Empty;
    public IReadOnlyDictionary<string, string> EnvironmentVariables { get; init; } = new Dictionary<string, string>();
    public TimeSpan Timeout { get; init; } = TimeSpan.FromMinutes(10);
}
ProcessExecutionResult.cs
namespace AtlasSuite.Tooling.Process.Models;

public sealed class ProcessExecutionResult
{
    public bool TimedOut { get; init; }
    public int ExitCode { get; init; }
    public string StandardOutput { get; init; } = string.Empty;
    public string StandardError { get; init; } = string.Empty;
    public TimeSpan Duration { get; init; }
}
IProcessRunner.cs
using AtlasSuite.Tooling.Process.Models;

namespace AtlasSuite.Tooling.Process.Interfaces;

public interface IProcessRunner
{
    Task<ProcessExecutionResult> RunAsync(ProcessExecutionRequest request, CancellationToken ct);
}
ProcessRunner.cs
using System.Diagnostics;
using AtlasSuite.Tooling.Process.Interfaces;
using AtlasSuite.Tooling.Process.Models;

namespace AtlasSuite.Tooling.Process.Services;

public sealed class ProcessRunner : IProcessRunner
{
    public async Task<ProcessExecutionResult> RunAsync(ProcessExecutionRequest request, CancellationToken ct)
    {
        var startInfo = new ProcessStartInfo
        {
            FileName = request.FileName,
            Arguments = request.Arguments,
            WorkingDirectory = string.IsNullOrWhiteSpace(request.WorkingDirectory)
                ? Environment.CurrentDirectory
                : request.WorkingDirectory,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        foreach (var pair in request.EnvironmentVariables)
            startInfo.Environment[pair.Key] = pair.Value;

        using var process = new Process { StartInfo = startInfo };

        var started = process.Start();
        if (!started)
            throw new InvalidOperationException($"Failed to start process '{request.FileName}'.");

        var stopwatch = Stopwatch.StartNew();

        var stdoutTask = process.StandardOutput.ReadToEndAsync(ct);
        var stderrTask = process.StandardError.ReadToEndAsync(ct);

        using var timeoutCts = CancellationTokenSource.CreateLinkedTokenSource(ct);
        timeoutCts.CancelAfter(request.Timeout);

        try
        {
            await process.WaitForExitAsync(timeoutCts.Token);
        }
        catch (OperationCanceledException) when (!ct.IsCancellationRequested)
        {
            try
            {
                if (!process.HasExited)
                    process.Kill(entireProcessTree: true);
            }
            catch
            {
            }

            stopwatch.Stop();

            return new ProcessExecutionResult
            {
                TimedOut = true,
                ExitCode = -1,
                StandardOutput = await stdoutTask,
                StandardError = await stderrTask,
                Duration = stopwatch.Elapsed
            };
        }

        stopwatch.Stop();

        return new ProcessExecutionResult
        {
            TimedOut = false,
            ExitCode = process.ExitCode,
            StandardOutput = await stdoutTask,
            StandardError = await stderrTask,
            Duration = stopwatch.Elapsed
        };
    }
}
5. Artifact store
IArtifactStore.cs
using AtlasSuite.Tooling.Artifacts.Models;

namespace AtlasSuite.Tooling.Artifacts.Interfaces;

public interface IArtifactStore
{
    Task SaveAsync(ToolArtifactRecord artifact, CancellationToken ct);
    Task<IReadOnlyList<ToolArtifactRecord>> GetByJobIdAsync(string jobId, CancellationToken ct);
}
SqliteArtifactStore.cs
using AtlasSuite.Storage.Sqlite.Interfaces;
using AtlasSuite.Tooling.Artifacts.Interfaces;
using AtlasSuite.Tooling.Artifacts.Models;

namespace AtlasSuite.Storage.Sqlite.Services;

public sealed class SqliteArtifactStore : IArtifactStore
{
    private readonly ISqliteConnectionFactory _factory;

    public SqliteArtifactStore(ISqliteConnectionFactory factory)
    {
        _factory = factory;
    }

    public async Task SaveAsync(ToolArtifactRecord artifact, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var sql = """
        INSERT INTO tool_artifacts (
            artifact_id, job_id, artifact_type, display_name, file_path,
            produced_by_tool_id, size_bytes, content_hash, created_utc
        )
        VALUES (
            $artifact_id, $job_id, $artifact_type, $display_name, $file_path,
            $produced_by_tool_id, $size_bytes, $content_hash, $created_utc
        );
        """;

        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        command.Parameters.AddWithValue("$artifact_id", artifact.ArtifactId);
        command.Parameters.AddWithValue("$job_id", artifact.JobId);
        command.Parameters.AddWithValue("$artifact_type", artifact.ArtifactType);
        command.Parameters.AddWithValue("$display_name", artifact.DisplayName);
        command.Parameters.AddWithValue("$file_path", artifact.FilePath);
        command.Parameters.AddWithValue("$produced_by_tool_id", artifact.ProducedByToolId);
        command.Parameters.AddWithValue("$size_bytes", artifact.SizeBytes);
        command.Parameters.AddWithValue("$content_hash", artifact.ContentHash);
        command.Parameters.AddWithValue("$created_utc", artifact.CreatedUtc.UtcDateTime.ToString("O"));

        await command.ExecuteNonQueryAsync(ct);
    }

    public async Task<IReadOnlyList<ToolArtifactRecord>> GetByJobIdAsync(string jobId, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var sql = "SELECT * FROM tool_artifacts WHERE job_id = $job_id ORDER BY created_utc;";
        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        command.Parameters.AddWithValue("$job_id", jobId);

        var results = new List<ToolArtifactRecord>();
        await using var reader = await command.ExecuteReaderAsync(ct);

        while (await reader.ReadAsync(ct))
        {
            results.Add(new ToolArtifactRecord
            {
                ArtifactId = reader.GetString(reader.GetOrdinal("artifact_id")),
                JobId = reader.GetString(reader.GetOrdinal("job_id")),
                ArtifactType = reader.GetString(reader.GetOrdinal("artifact_type")),
                DisplayName = reader.GetString(reader.GetOrdinal("display_name")),
                FilePath = reader.GetString(reader.GetOrdinal("file_path")),
                ProducedByToolId = reader.GetString(reader.GetOrdinal("produced_by_tool_id")),
                SizeBytes = reader.GetInt64(reader.GetOrdinal("size_bytes")),
                ContentHash = reader.GetString(reader.GetOrdinal("content_hash")),
                CreatedUtc = DateTimeOffset.Parse(reader.GetString(reader.GetOrdinal("created_utc")))
            });
        }

        return results;
    }
}
6. Validation report store
IValidationReportStore.cs
using AtlasSuite.Tooling.Validation.Models;

namespace AtlasSuite.Tooling.Validation.Interfaces;

public interface IValidationReportStore
{
    Task SaveAsync(ValidationReport report, CancellationToken ct);
    Task<ValidationReport?> GetByJobIdAsync(string jobId, CancellationToken ct);
}
SqliteValidationReportStore.cs
using AtlasSuite.Storage.Sqlite.Interfaces;
using AtlasSuite.Tooling.Validation.Interfaces;
using AtlasSuite.Tooling.Validation.Models;

namespace AtlasSuite.Storage.Sqlite.Services;

public sealed class SqliteValidationReportStore : IValidationReportStore
{
    private readonly ISqliteConnectionFactory _factory;

    public SqliteValidationReportStore(ISqliteConnectionFactory factory)
    {
        _factory = factory;
    }

    public async Task SaveAsync(ValidationReport report, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        await using var tx = await connection.BeginTransactionAsync(ct);

        var reportSql = """
        INSERT INTO validation_reports (
            report_id, job_id, source_tool_id, success, summary
        )
        VALUES (
            $report_id, $job_id, $source_tool_id, $success, $summary
        );
        """;

        await using (var command = connection.CreateCommand())
        {
            command.Transaction = tx;
            command.CommandText = reportSql;
            command.Parameters.AddWithValue("$report_id", report.ReportId);
            command.Parameters.AddWithValue("$job_id", report.JobId);
            command.Parameters.AddWithValue("$source_tool_id", report.SourceToolId);
            command.Parameters.AddWithValue("$success", report.Success ? 1 : 0);
            command.Parameters.AddWithValue("$summary", report.Summary);
            await command.ExecuteNonQueryAsync(ct);
        }

        foreach (var issue in report.Issues)
        {
            var issueSql = """
            INSERT INTO validation_issues (
                issue_id, report_id, rule_id, severity, category,
                message, file_path, line_number, suggested_fix
            )
            VALUES (
                $issue_id, $report_id, $rule_id, $severity, $category,
                $message, $file_path, $line_number, $suggested_fix
            );
            """;

            await using var command = connection.CreateCommand();
            command.Transaction = tx;
            command.CommandText = issueSql;
            command.Parameters.AddWithValue("$issue_id", issue.IssueId);
            command.Parameters.AddWithValue("$report_id", report.ReportId);
            command.Parameters.AddWithValue("$rule_id", issue.RuleId);
            command.Parameters.AddWithValue("$severity", issue.Severity);
            command.Parameters.AddWithValue("$category", issue.Category);
            command.Parameters.AddWithValue("$message", issue.Message);
            command.Parameters.AddWithValue("$file_path", issue.FilePath ?? (object)DBNull.Value);
            command.Parameters.AddWithValue("$line_number", issue.LineNumber ?? (object)DBNull.Value);
            command.Parameters.AddWithValue("$suggested_fix", issue.SuggestedFix ?? (object)DBNull.Value);
            await command.ExecuteNonQueryAsync(ct);
        }

        await tx.CommitAsync(ct);
    }

    public async Task<ValidationReport?> GetByJobIdAsync(string jobId, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var reportSql = "SELECT * FROM validation_reports WHERE job_id = $job_id LIMIT 1;";
        await using var reportCommand = connection.CreateCommand();
        reportCommand.CommandText = reportSql;
        reportCommand.Parameters.AddWithValue("$job_id", jobId);

        await using var reportReader = await reportCommand.ExecuteReaderAsync(ct);
        if (!await reportReader.ReadAsync(ct))
            return null;

        var reportId = reportReader.GetString(reportReader.GetOrdinal("report_id"));
        var sourceToolId = reportReader.GetString(reportReader.GetOrdinal("source_tool_id"));
        var success = reportReader.GetInt32(reportReader.GetOrdinal("success")) == 1;
        var summary = reportReader.GetString(reportReader.GetOrdinal("summary"));

        await reportReader.CloseAsync();

        var issuesSql = "SELECT * FROM validation_issues WHERE report_id = $report_id;";
        await using var issueCommand = connection.CreateCommand();
        issueCommand.CommandText = issuesSql;
        issueCommand.Parameters.AddWithValue("$report_id", reportId);

        var issues = new List<ValidationIssue>();
        await using var issueReader = await issueCommand.ExecuteReaderAsync(ct);
        while (await issueReader.ReadAsync(ct))
        {
            issues.Add(new ValidationIssue
            {
                IssueId = issueReader.GetString(issueReader.GetOrdinal("issue_id")),
                RuleId = issueReader.GetString(issueReader.GetOrdinal("rule_id")),
                Severity = issueReader.GetString(issueReader.GetOrdinal("severity")),
                Category = issueReader.GetString(issueReader.GetOrdinal("category")),
                Message = issueReader.GetString(issueReader.GetOrdinal("message")),
                FilePath = issueReader.IsDBNull(issueReader.GetOrdinal("file_path"))
                    ? null
                    : issueReader.GetString(issueReader.GetOrdinal("file_path")),
                LineNumber = issueReader.IsDBNull(issueReader.GetOrdinal("line_number"))
                    ? null
                    : issueReader.GetInt32(issueReader.GetOrdinal("line_number")),
                SuggestedFix = issueReader.IsDBNull(issueReader.GetOrdinal("suggested_fix"))
                    ? null
                    : issueReader.GetString(issueReader.GetOrdinal("suggested_fix"))
            });
        }

        return new ValidationReport
        {
            ReportId = reportId,
            JobId = jobId,
            SourceToolId = sourceToolId,
            Success = success,
            Summary = summary,
            Issues = issues
        };
    }
}
7. Build adapter models
BuildProfile.cs
namespace AtlasSuite.Tooling.Build.Models;

public sealed class BuildProfile
{
    public string ProfileId { get; init; } = string.Empty;
    public string DisplayName { get; init; } = string.Empty;
    public string SourceDirectory { get; init; } = string.Empty;
    public string BuildDirectory { get; init; } = string.Empty;
    public string Generator { get; init; } = "Ninja";
    public string Configuration { get; init; } = "Debug";
    public IReadOnlyList<string> Targets { get; init; } = Array.Empty<string>();
}
8. CMake/Ninja build adapter
CMakeNinjaBuildAdapter.cs
using AtlasSuite.Tooling.Jobs.Models;
using AtlasSuite.Tooling.Process.Interfaces;
using AtlasSuite.Tooling.Process.Models;
using AtlasSuite.Tooling.Registry.Interfaces;
using AtlasSuite.Tooling.Registry.Models;

namespace AtlasSuite.Tooling.Build.Adapters;

public sealed class CMakeNinjaBuildAdapter : IToolCapabilityAdapter
{
    private readonly IProcessRunner _processRunner;

    public CMakeNinjaBuildAdapter(IProcessRunner processRunner)
    {
        _processRunner = processRunner;
    }

    public string ToolId => "tool.build.cmake";
    public string DisplayName => "CMake + Ninja Build";

    public Task<ToolHealthReport> CheckHealthAsync(CancellationToken ct)
    {
        return Task.FromResult(new ToolHealthReport
        {
            ToolId = ToolId,
            Status = ToolHealthStatus.Healthy,
            Version = "detected-at-runtime",
            Message = "CMake build adapter ready",
            ExecutablePath = "cmake"
        });
    }

    public Task<IReadOnlyList<ToolCapabilityDescriptor>> GetCapabilitiesAsync(CancellationToken ct)
    {
        IReadOnlyList<ToolCapabilityDescriptor> capabilities =
        [
            new ToolCapabilityDescriptor
            {
                CapabilityId = "cap.build.configure",
                DisplayName = "Configure Build",
                Description = "Runs CMake configure step.",
                SupportedRequestKinds = new[] { "Build", "Validate" },
                SupportsDryRun = false,
                ProducesArtifacts = true,
                ProducesStructuredData = true
            },
            new ToolCapabilityDescriptor
            {
                CapabilityId = "cap.build.compile",
                DisplayName = "Compile Targets",
                Description = "Builds configured targets.",
                SupportedRequestKinds = new[] { "Build", "Repair" },
                SupportsDryRun = false,
                ProducesArtifacts = true,
                ProducesStructuredData = true
            }
        ];

        return Task.FromResult(capabilities);
    }

    public async Task<ToolExecutionResult> ExecuteAsync(ToolExecutionRequest request, CancellationToken ct)
    {
        return request.CapabilityId switch
        {
            "cap.build.configure" => await RunConfigureAsync(request, ct),
            "cap.build.compile" => await RunBuildAsync(request, ct),
            _ => new ToolExecutionResult
            {
                Success = false,
                ToolId = ToolId,
                CapabilityId = request.CapabilityId,
                ExitCode = -1,
                Summary = $"Unsupported capability '{request.CapabilityId}'.",
                Errors = new[] { $"Unsupported capability '{request.CapabilityId}'." }
            }
        };
    }

    private async Task<ToolExecutionResult> RunConfigureAsync(ToolExecutionRequest request, CancellationToken ct)
    {
        var sourceDir = request.Parameters.GetValueOrDefault("sourceDir", request.WorkspaceRoot);
        var buildDir = request.Parameters.GetValueOrDefault("buildDir", Path.Combine(request.WorkspaceRoot, "build"));
        var generator = request.Parameters.GetValueOrDefault("generator", "Ninja");
        var config = request.Parameters.GetValueOrDefault("config", "Debug");

        Directory.CreateDirectory(buildDir);

        var processRequest = new ProcessExecutionRequest
        {
            FileName = "cmake",
            Arguments = $"-S \"{sourceDir}\" -B \"{buildDir}\" -G \"{generator}\" -DCMAKE_BUILD_TYPE={config}",
            WorkingDirectory = request.WorkspaceRoot,
            Timeout = TimeSpan.FromMinutes(10)
        };

        var result = await _processRunner.RunAsync(processRequest, ct);

        var logs = new List<ToolLogRecord>
        {
            new()
            {
                ToolId = ToolId,
                Severity = result.ExitCode == 0 ? LogSeverity.Info : LogSeverity.Error,
                Message = string.IsNullOrWhiteSpace(result.StandardOutput) ? result.StandardError : result.StandardOutput
            }
        };

        return new ToolExecutionResult
        {
            Success = !result.TimedOut && result.ExitCode == 0,
            ToolId = ToolId,
            CapabilityId = request.CapabilityId,
            ExitCode = result.ExitCode,
            Summary = result.TimedOut ? "Build configure timed out." : "Build configure completed.",
            Errors = result.ExitCode == 0 ? Array.Empty<string>() : new[] { result.StandardError },
            Logs = logs,
            StructuredData = new Dictionary<string, string>
            {
                ["buildDir"] = buildDir,
                ["config"] = config
            },
            Duration = result.Duration
        };
    }

    private async Task<ToolExecutionResult> RunBuildAsync(ToolExecutionRequest request, CancellationToken ct)
    {
        var buildDir = request.Parameters.GetValueOrDefault("buildDir", Path.Combine(request.WorkspaceRoot, "build"));
        var config = request.Parameters.GetValueOrDefault("config", "Debug");
        var target = request.Parameters.GetValueOrDefault("target", string.Empty);

        var targetArg = string.IsNullOrWhiteSpace(target) ? string.Empty : $" --target \"{target}\"";

        var processRequest = new ProcessExecutionRequest
        {
            FileName = "cmake",
            Arguments = $"--build \"{buildDir}\" --config {config}{targetArg}",
            WorkingDirectory = request.WorkspaceRoot,
            Timeout = TimeSpan.FromMinutes(30)
        };

        var result = await _processRunner.RunAsync(processRequest, ct);

        var logs = new List<ToolLogRecord>
        {
            new()
            {
                ToolId = ToolId,
                Severity = result.ExitCode == 0 ? LogSeverity.Info : LogSeverity.Error,
                Message = string.IsNullOrWhiteSpace(result.StandardOutput) ? result.StandardError : result.StandardOutput
            }
        };

        return new ToolExecutionResult
        {
            Success = !result.TimedOut && result.ExitCode == 0,
            ToolId = ToolId,
            CapabilityId = request.CapabilityId,
            ExitCode = result.ExitCode,
            Summary = result.TimedOut ? "Build timed out." : "Build completed.",
            Errors = result.ExitCode == 0 ? Array.Empty<string>() : new[] { result.StandardError },
            Logs = logs,
            StructuredData = new Dictionary<string, string>
            {
                ["buildDir"] = buildDir,
                ["config"] = config,
                ["target"] = target
            },
            Duration = result.Duration
        };
    }
}
9. AtlasAI tool executor
Now AtlasAI can build plans and execute them through the job system.

AtlasAIToolExecutionResult.cs
namespace AtlasSuite.AtlasAI.Models;

public sealed class AtlasAIToolExecutionResult
{
    public string PlanId { get; init; } = string.Empty;
    public bool Success { get; init; }
    public IReadOnlyList<string> JobIds { get; init; } = Array.Empty<string>();
    public IReadOnlyList<string> Notes { get; init; } = Array.Empty<string>();
}
Updated IAtlasAIToolExecutor.cs
using AtlasSuite.AtlasAI.Models;

namespace AtlasSuite.AtlasAI.Interfaces;

public interface IAtlasAIToolExecutor
{
    Task<AtlasAIToolExecutionResult> ExecutePlanAsync(AtlasAIToolPlan plan, string workspaceRoot, CancellationToken ct);
}
AtlasAIToolExecutor.cs
using AtlasSuite.AtlasAI.Interfaces;
using AtlasSuite.AtlasAI.Models;
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.AtlasAI.Services;

public sealed class AtlasAIToolExecutor : IAtlasAIToolExecutor
{
    private readonly IToolJobQueue _jobQueue;

    public AtlasAIToolExecutor(IToolJobQueue jobQueue)
    {
        _jobQueue = jobQueue;
    }

    public async Task<AtlasAIToolExecutionResult> ExecutePlanAsync(
        AtlasAIToolPlan plan,
        string workspaceRoot,
        CancellationToken ct)
    {
        var jobIds = new List<string>();

        foreach (var step in plan.Steps.OrderBy(x => x.Order))
        {
            var request = new ToolExecutionRequest
            {
                ToolId = step.ToolId,
                CapabilityId = step.CapabilityId,
                RequestKind = step.RequestKind,
                WorkspaceRoot = workspaceRoot,
                IsDryRun = plan.DryRun,
                Parameters = step.Parameters,
                RequestedBy = "AtlasAI",
                CorrelationId = plan.PlanId
            };

            var jobId = await _jobQueue.EnqueueAsync(request, step.Description, ct);
            jobIds.Add(jobId);
        }

        return new AtlasAIToolExecutionResult
        {
            PlanId = plan.PlanId,
            Success = true,
            JobIds = jobIds,
            Notes = new[] { $"Queued {jobIds.Count} AtlasAI tool job(s)." }
        };
    }
}
10. Upgrade the job runner to persist artifacts
Right now the runner ignores result artifacts. Fix that.

Updated ToolJobRunner.cs
using AtlasSuite.Tooling.Artifacts.Interfaces;
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Models;
using AtlasSuite.Tooling.Registry.Interfaces;

namespace AtlasSuite.Tooling.Jobs.Services;

public sealed class ToolJobRunner : IToolJobRunner
{
    private readonly IToolJobStore _store;
    private readonly IToolRegistry _registry;
    private readonly ToolJobQueue _queue;
    private readonly IArtifactStore _artifactStore;

    public ToolJobRunner(
        IToolJobStore store,
        IToolRegistry registry,
        ToolJobQueue queue,
        IArtifactStore artifactStore)
    {
        _store = store;
        _registry = registry;
        _queue = queue;
        _artifactStore = artifactStore;
    }

    public async Task RunAsync(string jobId, CancellationToken ct)
    {
        var job = await _store.GetAsync(jobId, ct);
        if (job is null)
            return;

        var request = _queue.GetRequest(jobId);
        if (request is null)
        {
            job.Status = ToolJobStatus.Failed;
            job.Summary = "No execution request found.";
            job.FinishedUtc = DateTimeOffset.UtcNow;
            await _store.SaveAsync(job, ct);
            return;
        }

        var adapter = await _registry.GetAdapterAsync(request.ToolId, ct);
        if (adapter is null)
        {
            job.Status = ToolJobStatus.Failed;
            job.Summary = $"No adapter found for tool '{request.ToolId}'.";
            job.FinishedUtc = DateTimeOffset.UtcNow;
            await _store.SaveAsync(job, ct);
            return;
        }

        job.Status = ToolJobStatus.Running;
        job.StartedUtc = DateTimeOffset.UtcNow;
        job.ProgressPercent = 5;
        await _store.SaveAsync(job, ct);

        var result = await adapter.ExecuteAsync(request, ct);

        foreach (var artifact in result.Artifacts)
        {
            var storedArtifact = artifact with { };
            await _artifactStore.SaveAsync(storedArtifact, ct);
        }

        job.ProgressPercent = 100;
        job.FinishedUtc = DateTimeOffset.UtcNow;
        job.Status = result.Success ? ToolJobStatus.Succeeded : ToolJobStatus.Failed;
        job.Summary = result.Summary;

        await _store.SaveAsync(job, ct);
    }
}
Because ToolArtifactRecord is a class with init, better to create artifacts with correct JobId inside adapters or make a new instance before storing if needed.

11. Dependency injection update
Updated ServiceCollectionExtensions.cs
using AtlasSuite.AtlasAI.Interfaces;
using AtlasSuite.AtlasAI.Services;
using AtlasSuite.Storage.Sqlite.Interfaces;
using AtlasSuite.Storage.Sqlite.Models;
using AtlasSuite.Storage.Sqlite.Services;
using AtlasSuite.Tooling.Artifacts.Interfaces;
using AtlasSuite.Tooling.Build.Adapters;
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Services;
using AtlasSuite.Tooling.Parse.Adapters;
using AtlasSuite.Tooling.Process.Interfaces;
using AtlasSuite.Tooling.Process.Services;
using AtlasSuite.Tooling.Registry.Interfaces;
using AtlasSuite.Tooling.Registry.Services;
using AtlasSuite.Tooling.Search.Adapters;
using AtlasSuite.Tooling.Validation.Interfaces;
using Microsoft.Extensions.DependencyInjection;

namespace AtlasSuite.Shell.Services;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddAtlasSuiteCore(this IServiceCollection services, string databasePath)
    {
        services.AddSingleton(new SqliteOptions { DatabasePath = databasePath });
        services.AddSingleton<ISqliteConnectionFactory, SqliteConnectionFactory>();
        services.AddSingleton<SqliteDatabaseInitializer>();

        services.AddSingleton<IProcessRunner, ProcessRunner>();

        services.AddSingleton<IToolCapabilityAdapter, RipgrepAdapter>();
        services.AddSingleton<IToolCapabilityAdapter, TreeSitterAdapter>();
        services.AddSingleton<IToolCapabilityAdapter, CMakeNinjaBuildAdapter>();

        services.AddSingleton<IToolRegistry, ToolRegistry>();

        services.AddSingleton<IToolJobStore, SqliteToolJobStore>();
        services.AddSingleton<IArtifactStore, SqliteArtifactStore>();
        services.AddSingleton<IValidationReportStore, SqliteValidationReportStore>();

        services.AddSingleton<ToolJobQueue>();
        services.AddSingleton<IToolJobQueue>(sp => sp.GetRequiredService<ToolJobQueue>());
        services.AddSingleton<IToolJobRunner, ToolJobRunner>();

        services.AddSingleton<IAtlasAIToolPlanner, AtlasAIToolPlanner>();
        services.AddSingleton<IAtlasAIToolExecutor, AtlasAIToolExecutor>();

        return services;
    }
}
12. First real vertical-slice workflow
Once this pack is in place, Atlas Suite can do this:

Flow
Start app

Initialize SQLite

Refresh tool registry

AtlasAI builds a plan

AtlasAI queues jobs

Job runner executes:

search

parse

build configure

build compile

Store job status/results/artifacts

Show in UI

That is the first genuine functional loop.

13. Biggest gaps after Phase 2
After this scaffold, the next real gaps are:

A. Background worker / scheduler
Right now jobs can be queued and run, but no service is automatically draining the queue.

B. Tool logs persistence
We normalize logs in memory/result objects, but we are not yet saving them to SQLite.

C. Real ripgrep and tree-sitter execution
Those adapters are still placeholders.

D. Validation publisher pipeline
Validation report store exists, but tools are not yet writing into it.

E. Build profile management
Profiles exist as a model, but not yet as a saved config system.

F. WPF bindings/viewmodels
The backend is taking shape, but the UI layer still needs real viewmodels and commands.

14. Best next implementation order
Here’s the smartest next sequence:

background job dispatcher service

tool log store

real ripgrep adapter execution

real build panel + job queue panel

build profile persistence

validation publishing pipeline

Blender adapter base

AtlasAI actions panel

That gives you a usable daily-driver skeleton.

15. Strongest next deliverable
The next thing to generate should be:

Phase 3 scaffold pack
with:

background job dispatcher

tool log store

real ripgrep process execution

build profile store

WPF viewmodels for Tool Registry and Job Queue

validation report publishing flow

That would push Atlas Suite into its first interactive working shell.


yes

Excellent — here’s the Phase 3 scaffold pack.

This is the layer where Atlas Suite starts feeling like a real working application shell instead of just a backend framework.

Atlas Suite — Phase 3 Scaffold Pack
This phase adds:

background job dispatcher

tool log store

real ripgrep process execution

build profile store

WPF viewmodels for Tool Registry + Job Queue

validation report publishing flow

Using your locked naming:

Atlas Suite = tooling shell

AtlasAI = integrated AI system

1. What Phase 3 solves
Up through Phase 2, you have:

tool registry

job queue/store

adapters

SQLite persistence

process runner

build adapter

AtlasAI planner/executor

But the gaps were:

queued jobs do not run automatically

logs are not stored persistently

ripgrep is still a stub

build profiles are not saved

no real WPF-facing models yet

validation flow exists but is not connected

This phase closes those gaps.

2. Updated project structure
Add these folders/files:

src/
├── AtlasSuite.Tooling.Jobs/
│   ├── Background/
│   ├── Models/
│   ├── Interfaces/
│   └── Services/
├── AtlasSuite.Tooling.Logging/
│   ├── Interfaces/
│   ├── Models/
│   └── Services/
├── AtlasSuite.Tooling.Build/
│   ├── Interfaces/
│   ├── Models/
│   └── Services/
├── AtlasSuite.Tooling.Validation/
│   ├── Interfaces/
│   ├── Models/
│   └── Services/
├── AtlasSuite.Shell/
│   ├── ViewModels/
│   ├── Panels/
│   └── Commands/
└── AtlasSuite.Storage.Sqlite/
    ├── Services/
    └── Sql/
3. Background job dispatcher
This is the service that continuously drains queued jobs.

IToolJobDispatcher.cs
namespace AtlasSuite.Tooling.Jobs.Interfaces;

public interface IToolJobDispatcher
{
    Task StartAsync(CancellationToken ct);
    Task StopAsync(CancellationToken ct);
}
IToolJobQueryService.cs
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Tooling.Jobs.Interfaces;

public interface IToolJobQueryService
{
    Task<IReadOnlyList<ToolJobRecord>> GetQueuedJobsAsync(int count, CancellationToken ct);
}
Update IToolJobStore.cs
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Tooling.Jobs.Interfaces;

public interface IToolJobStore
{
    Task SaveAsync(ToolJobRecord record, CancellationToken ct);
    Task<ToolJobRecord?> GetAsync(string jobId, CancellationToken ct);
    Task<IReadOnlyList<ToolJobRecord>> GetRecentAsync(int count, CancellationToken ct);
    Task<IReadOnlyList<ToolJobRecord>> GetByStatusAsync(ToolJobStatus status, int count, CancellationToken ct);
}
Update SqliteToolJobStore.cs
Add this method:

public async Task<IReadOnlyList<ToolJobRecord>> GetByStatusAsync(ToolJobStatus status, int count, CancellationToken ct)
{
    await using var connection = _factory.CreateConnection();
    await connection.OpenAsync(ct);

    var sql = "SELECT * FROM tool_jobs WHERE status = $status ORDER BY created_utc ASC LIMIT $count;";
    await using var command = connection.CreateCommand();
    command.CommandText = sql;
    command.Parameters.AddWithValue("$status", (int)status);
    command.Parameters.AddWithValue("$count", count);

    var results = new List<ToolJobRecord>();
    await using var reader = await command.ExecuteReaderAsync(ct);
    while (await reader.ReadAsync(ct))
        results.Add(Map(reader));

    return results;
}
ToolJobDispatcher.cs
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Tooling.Jobs.Background;

public sealed class ToolJobDispatcher : IToolJobDispatcher
{
    private readonly IToolJobStore _store;
    private readonly IToolJobRunner _runner;
    private CancellationTokenSource? _loopCts;
    private Task? _loopTask;

    public ToolJobDispatcher(
        IToolJobStore store,
        IToolJobRunner runner)
    {
        _store = store;
        _runner = runner;
    }

    public Task StartAsync(CancellationToken ct)
    {
        if (_loopTask is not null)
            return Task.CompletedTask;

        _loopCts = CancellationTokenSource.CreateLinkedTokenSource(ct);
        _loopTask = RunLoopAsync(_loopCts.Token);
        return Task.CompletedTask;
    }

    public async Task StopAsync(CancellationToken ct)
    {
        if (_loopCts is null || _loopTask is null)
            return;

        _loopCts.Cancel();

        try
        {
            await _loopTask.WaitAsync(ct);
        }
        catch (OperationCanceledException)
        {
        }

        _loopTask = null;
        _loopCts.Dispose();
        _loopCts = null;
    }

    private async Task RunLoopAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            var queuedJobs = await _store.GetByStatusAsync(ToolJobStatus.Queued, 5, ct);

            foreach (var job in queuedJobs)
            {
                if (ct.IsCancellationRequested)
                    break;

                await _runner.RunAsync(job.JobId, ct);
            }

            await Task.Delay(TimeSpan.FromSeconds(1), ct);
        }
    }
}
4. Tool log persistence
Right now results carry logs but they vanish after execution. Fix that.

IToolLogStore.cs
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Tooling.Logging.Interfaces;

public interface IToolLogStore
{
    Task SaveAsync(ToolLogRecord record, CancellationToken ct);
    Task SaveManyAsync(IEnumerable<ToolLogRecord> records, CancellationToken ct);
    Task<IReadOnlyList<ToolLogRecord>> GetByJobIdAsync(string jobId, CancellationToken ct);
    Task<IReadOnlyList<ToolLogRecord>> GetRecentAsync(int count, CancellationToken ct);
}
Update DB initializer SQL
Add table:

CREATE TABLE IF NOT EXISTS tool_logs (
    log_id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL,
    tool_id TEXT NOT NULL,
    severity INTEGER NOT NULL,
    timestamp_utc TEXT NOT NULL,
    message TEXT NOT NULL,
    source_path TEXT NULL,
    source_line INTEGER NULL
);
Update ToolLogRecord.cs
namespace AtlasSuite.Tooling.Jobs.Models;

public sealed class ToolLogRecord
{
    public string LogId { get; init; } = Guid.NewGuid().ToString("N");
    public DateTimeOffset TimestampUtc { get; init; } = DateTimeOffset.UtcNow;
    public string JobId { get; init; } = string.Empty;
    public string ToolId { get; init; } = string.Empty;
    public LogSeverity Severity { get; init; } = LogSeverity.Info;
    public string Message { get; init; } = string.Empty;
    public string? SourcePath { get; init; }
    public int? SourceLine { get; init; }
}
SqliteToolLogStore.cs
using AtlasSuite.Storage.Sqlite.Interfaces;
using AtlasSuite.Tooling.Jobs.Models;
using AtlasSuite.Tooling.Logging.Interfaces;

namespace AtlasSuite.Storage.Sqlite.Services;

public sealed class SqliteToolLogStore : IToolLogStore
{
    private readonly ISqliteConnectionFactory _factory;

    public SqliteToolLogStore(ISqliteConnectionFactory factory)
    {
        _factory = factory;
    }

    public async Task SaveAsync(ToolLogRecord record, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var sql = """
        INSERT INTO tool_logs (
            log_id, job_id, tool_id, severity, timestamp_utc, message, source_path, source_line
        )
        VALUES (
            $log_id, $job_id, $tool_id, $severity, $timestamp_utc, $message, $source_path, $source_line
        );
        """;

        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        command.Parameters.AddWithValue("$log_id", record.LogId);
        command.Parameters.AddWithValue("$job_id", record.JobId);
        command.Parameters.AddWithValue("$tool_id", record.ToolId);
        command.Parameters.AddWithValue("$severity", (int)record.Severity);
        command.Parameters.AddWithValue("$timestamp_utc", record.TimestampUtc.UtcDateTime.ToString("O"));
        command.Parameters.AddWithValue("$message", record.Message);
        command.Parameters.AddWithValue("$source_path", record.SourcePath ?? (object)DBNull.Value);
        command.Parameters.AddWithValue("$source_line", record.SourceLine ?? (object)DBNull.Value);

        await command.ExecuteNonQueryAsync(ct);
    }

    public async Task SaveManyAsync(IEnumerable<ToolLogRecord> records, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);
        await using var tx = await connection.BeginTransactionAsync(ct);

        foreach (var record in records)
        {
            var sql = """
            INSERT INTO tool_logs (
                log_id, job_id, tool_id, severity, timestamp_utc, message, source_path, source_line
            )
            VALUES (
                $log_id, $job_id, $tool_id, $severity, $timestamp_utc, $message, $source_path, $source_line
            );
            """;

            await using var command = connection.CreateCommand();
            command.Transaction = tx;
            command.CommandText = sql;
            command.Parameters.AddWithValue("$log_id", record.LogId);
            command.Parameters.AddWithValue("$job_id", record.JobId);
            command.Parameters.AddWithValue("$tool_id", record.ToolId);
            command.Parameters.AddWithValue("$severity", (int)record.Severity);
            command.Parameters.AddWithValue("$timestamp_utc", record.TimestampUtc.UtcDateTime.ToString("O"));
            command.Parameters.AddWithValue("$message", record.Message);
            command.Parameters.AddWithValue("$source_path", record.SourcePath ?? (object)DBNull.Value);
            command.Parameters.AddWithValue("$source_line", record.SourceLine ?? (object)DBNull.Value);

            await command.ExecuteNonQueryAsync(ct);
        }

        await tx.CommitAsync(ct);
    }

    public async Task<IReadOnlyList<ToolLogRecord>> GetByJobIdAsync(string jobId, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var sql = "SELECT * FROM tool_logs WHERE job_id = $job_id ORDER BY timestamp_utc;";
        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        command.Parameters.AddWithValue("$job_id", jobId);

        var results = new List<ToolLogRecord>();
        await using var reader = await command.ExecuteReaderAsync(ct);

        while (await reader.ReadAsync(ct))
        {
            results.Add(Map(reader));
        }

        return results;
    }

    public async Task<IReadOnlyList<ToolLogRecord>> GetRecentAsync(int count, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var sql = "SELECT * FROM tool_logs ORDER BY timestamp_utc DESC LIMIT $count;";
        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        command.Parameters.AddWithValue("$count", count);

        var results = new List<ToolLogRecord>();
        await using var reader = await command.ExecuteReaderAsync(ct);

        while (await reader.ReadAsync(ct))
        {
            results.Add(Map(reader));
        }

        return results;
    }

    private static ToolLogRecord Map(Microsoft.Data.Sqlite.SqliteDataReader reader)
    {
        return new ToolLogRecord
        {
            LogId = reader.GetString(reader.GetOrdinal("log_id")),
            JobId = reader.GetString(reader.GetOrdinal("job_id")),
            ToolId = reader.GetString(reader.GetOrdinal("tool_id")),
            Severity = (LogSeverity)reader.GetInt32(reader.GetOrdinal("severity")),
            TimestampUtc = DateTimeOffset.Parse(reader.GetString(reader.GetOrdinal("timestamp_utc"))),
            Message = reader.GetString(reader.GetOrdinal("message")),
            SourcePath = reader.IsDBNull(reader.GetOrdinal("source_path"))
                ? null
                : reader.GetString(reader.GetOrdinal("source_path")),
            SourceLine = reader.IsDBNull(reader.GetOrdinal("source_line"))
                ? null
                : reader.GetInt32(reader.GetOrdinal("source_line"))
        };
    }
}
5. Persist logs during job execution
Update ToolJobRunner.cs to save logs.

Updated constructor
private readonly IToolLogStore _logStore;
private readonly IValidationReportStore _validationStore;
Updated constructor body
public ToolJobRunner(
    IToolJobStore store,
    IToolRegistry registry,
    ToolJobQueue queue,
    IArtifactStore artifactStore,
    IToolLogStore logStore,
    IValidationReportStore validationStore)
{
    _store = store;
    _registry = registry;
    _queue = queue;
    _artifactStore = artifactStore;
    _logStore = logStore;
    _validationStore = validationStore;
}
Persist results inside RunAsync
var result = await adapter.ExecuteAsync(request, ct);

var logsToStore = result.Logs
    .Select(log => new ToolLogRecord
    {
        LogId = string.IsNullOrWhiteSpace(log.LogId) ? Guid.NewGuid().ToString("N") : log.LogId,
        JobId = job.JobId,
        ToolId = string.IsNullOrWhiteSpace(log.ToolId) ? request.ToolId : log.ToolId,
        Severity = log.Severity,
        TimestampUtc = log.TimestampUtc == default ? DateTimeOffset.UtcNow : log.TimestampUtc,
        Message = log.Message,
        SourcePath = log.SourcePath,
        SourceLine = log.SourceLine
    })
    .ToList();

if (logsToStore.Count > 0)
    await _logStore.SaveManyAsync(logsToStore, ct);

foreach (var artifact in result.Artifacts)
{
    var storedArtifact = new AtlasSuite.Tooling.Artifacts.Models.ToolArtifactRecord
    {
        ArtifactId = string.IsNullOrWhiteSpace(artifact.ArtifactId) ? Guid.NewGuid().ToString("N") : artifact.ArtifactId,
        JobId = job.JobId,
        ArtifactType = artifact.ArtifactType,
        DisplayName = artifact.DisplayName,
        FilePath = artifact.FilePath,
        ProducedByToolId = string.IsNullOrWhiteSpace(artifact.ProducedByToolId) ? request.ToolId : artifact.ProducedByToolId,
        SizeBytes = artifact.SizeBytes,
        ContentHash = artifact.ContentHash,
        CreatedUtc = artifact.CreatedUtc == default ? DateTimeOffset.UtcNow : artifact.CreatedUtc
    };

    await _artifactStore.SaveAsync(storedArtifact, ct);
}

if (result.ValidationReport is not null)
{
    var storedReport = new AtlasSuite.Tooling.Validation.Models.ValidationReport
    {
        ReportId = string.IsNullOrWhiteSpace(result.ValidationReport.ReportId)
            ? Guid.NewGuid().ToString("N")
            : result.ValidationReport.ReportId,
        JobId = job.JobId,
        SourceToolId = request.ToolId,
        Success = result.ValidationReport.Success,
        Summary = result.ValidationReport.Summary,
        Issues = result.ValidationReport.Issues
    };

    await _validationStore.SaveAsync(storedReport, ct);
}
That means we need to extend ToolExecutionResult.

6. Extend ToolExecutionResult
Updated ToolExecutionResult.cs
using AtlasSuite.Tooling.Artifacts.Models;
using AtlasSuite.Tooling.Validation.Models;

namespace AtlasSuite.Tooling.Jobs.Models;

public sealed class ToolExecutionResult
{
    public bool Success { get; init; }
    public string ToolId { get; init; } = string.Empty;
    public string CapabilityId { get; init; } = string.Empty;
    public int ExitCode { get; init; }
    public string Summary { get; init; } = string.Empty;
    public IReadOnlyList<string> Warnings { get; init; } = Array.Empty<string>();
    public IReadOnlyList<string> Errors { get; init; } = Array.Empty<string>();
    public IReadOnlyList<ToolArtifactRecord> Artifacts { get; init; } = Array.Empty<ToolArtifactRecord>();
    public IReadOnlyList<ToolLogRecord> Logs { get; init; } = Array.Empty<ToolLogRecord>();
    public IReadOnlyDictionary<string, string> StructuredData { get; init; } = new Dictionary<string, string>();
    public ValidationReport? ValidationReport { get; init; }
    public TimeSpan Duration { get; init; } = TimeSpan.Zero;
}
7. Real ripgrep adapter execution
Now replace the stub with real process execution.

Updated RipgrepAdapter.cs
using AtlasSuite.Tooling.Jobs.Models;
using AtlasSuite.Tooling.Process.Interfaces;
using AtlasSuite.Tooling.Process.Models;
using AtlasSuite.Tooling.Registry.Interfaces;
using AtlasSuite.Tooling.Registry.Models;

namespace AtlasSuite.Tooling.Search.Adapters;

public sealed class RipgrepAdapter : IToolCapabilityAdapter
{
    private readonly IProcessRunner _processRunner;

    public RipgrepAdapter(IProcessRunner processRunner)
    {
        _processRunner = processRunner;
    }

    public string ToolId => "tool.search.ripgrep";
    public string DisplayName => "ripgrep Search";

    public Task<ToolHealthReport> CheckHealthAsync(CancellationToken ct)
    {
        return Task.FromResult(new ToolHealthReport
        {
            ToolId = ToolId,
            Status = ToolHealthStatus.Healthy,
            Version = "detected-at-runtime",
            Message = "ripgrep adapter ready",
            ExecutablePath = "rg"
        });
    }

    public Task<IReadOnlyList<ToolCapabilityDescriptor>> GetCapabilitiesAsync(CancellationToken ct)
    {
        IReadOnlyList<ToolCapabilityDescriptor> capabilities =
        [
            new ToolCapabilityDescriptor
            {
                CapabilityId = "cap.search.workspace",
                DisplayName = "Workspace Search",
                Description = "Searches the workspace for text matches.",
                SupportedRequestKinds = new[] { "Inspect", "Validate" },
                SupportsDryRun = true,
                ProducesArtifacts = false,
                ProducesStructuredData = true
            }
        ];

        return Task.FromResult(capabilities);
    }

    public async Task<ToolExecutionResult> ExecuteAsync(ToolExecutionRequest request, CancellationToken ct)
    {
        var query = request.Parameters.TryGetValue("query", out var q) ? q : string.Empty;
        if (string.IsNullOrWhiteSpace(query))
        {
            return new ToolExecutionResult
            {
                Success = false,
                ToolId = ToolId,
                CapabilityId = request.CapabilityId,
                ExitCode = -1,
                Summary = "Search query was empty.",
                Errors = new[] { "Search query was empty." }
            };
        }

        var processRequest = new ProcessExecutionRequest
        {
            FileName = "rg",
            Arguments = $"--line-number --with-filename --color never \"{query}\" \"{request.WorkspaceRoot}\"",
            WorkingDirectory = request.WorkspaceRoot,
            Timeout = TimeSpan.FromMinutes(2)
        };

        var processResult = await _processRunner.RunAsync(processRequest, ct);

        var stdout = processResult.StandardOutput ?? string.Empty;
        var stderr = processResult.StandardError ?? string.Empty;

        var lines = stdout
            .Split(new[] { "\r\n", "\n" }, StringSplitOptions.RemoveEmptyEntries)
            .Take(500)
            .ToList();

        var structured = new Dictionary<string, string>
        {
            ["query"] = query,
            ["matchCount"] = lines.Count.ToString()
        };

        var logs = new List<ToolLogRecord>
        {
            new()
            {
                ToolId = ToolId,
                Severity = processResult.ExitCode == 0 || processResult.ExitCode == 1
                    ? LogSeverity.Info
                    : LogSeverity.Error,
                Message = processResult.ExitCode switch
                {
                    0 => $"Search completed with {lines.Count} match(es).",
                    1 => "Search completed with no matches.",
                    _ => string.IsNullOrWhiteSpace(stderr) ? "ripgrep execution failed." : stderr
                }
            }
        };

        for (var i = 0; i < lines.Count; i++)
        {
            structured[$"match.{i}"] = lines[i];
        }

        var success = !processResult.TimedOut && (processResult.ExitCode == 0 || processResult.ExitCode == 1);

        return new ToolExecutionResult
        {
            Success = success,
            ToolId = ToolId,
            CapabilityId = request.CapabilityId,
            ExitCode = processResult.ExitCode,
            Summary = processResult.TimedOut
                ? "Search timed out."
                : processResult.ExitCode == 1
                    ? "Search completed with no matches."
                    : "Search completed.",
            Errors = success ? Array.Empty<string>() : new[] { stderr },
            Logs = logs,
            StructuredData = structured,
            Duration = processResult.Duration
        };
    }
}
8. Build profile persistence
You need saved named build configs.

IBuildProfileStore.cs
using AtlasSuite.Tooling.Build.Models;

namespace AtlasSuite.Tooling.Build.Interfaces;

public interface IBuildProfileStore
{
    Task SaveAsync(BuildProfile profile, CancellationToken ct);
    Task<BuildProfile?> GetByIdAsync(string profileId, CancellationToken ct);
    Task<IReadOnlyList<BuildProfile>> GetAllAsync(CancellationToken ct);
}
Update DB initializer SQL
Add:

CREATE TABLE IF NOT EXISTS build_profiles (
    profile_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    source_directory TEXT NOT NULL,
    build_directory TEXT NOT NULL,
    generator TEXT NOT NULL,
    configuration TEXT NOT NULL,
    targets_json TEXT NOT NULL
);
SqliteBuildProfileStore.cs
using System.Text.Json;
using AtlasSuite.Storage.Sqlite.Interfaces;
using AtlasSuite.Tooling.Build.Interfaces;
using AtlasSuite.Tooling.Build.Models;

namespace AtlasSuite.Storage.Sqlite.Services;

public sealed class SqliteBuildProfileStore : IBuildProfileStore
{
    private readonly ISqliteConnectionFactory _factory;

    public SqliteBuildProfileStore(ISqliteConnectionFactory factory)
    {
        _factory = factory;
    }

    public async Task SaveAsync(BuildProfile profile, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var sql = """
        INSERT INTO build_profiles (
            profile_id, display_name, source_directory, build_directory,
            generator, configuration, targets_json
        )
        VALUES (
            $profile_id, $display_name, $source_directory, $build_directory,
            $generator, $configuration, $targets_json
        )
        ON CONFLICT(profile_id) DO UPDATE SET
            display_name = excluded.display_name,
            source_directory = excluded.source_directory,
            build_directory = excluded.build_directory,
            generator = excluded.generator,
            configuration = excluded.configuration,
            targets_json = excluded.targets_json;
        """;

        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        command.Parameters.AddWithValue("$profile_id", profile.ProfileId);
        command.Parameters.AddWithValue("$display_name", profile.DisplayName);
        command.Parameters.AddWithValue("$source_directory", profile.SourceDirectory);
        command.Parameters.AddWithValue("$build_directory", profile.BuildDirectory);
        command.Parameters.AddWithValue("$generator", profile.Generator);
        command.Parameters.AddWithValue("$configuration", profile.Configuration);
        command.Parameters.AddWithValue("$targets_json", JsonSerializer.Serialize(profile.Targets));

        await command.ExecuteNonQueryAsync(ct);
    }

    public async Task<BuildProfile?> GetByIdAsync(string profileId, CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var sql = "SELECT * FROM build_profiles WHERE profile_id = $profile_id LIMIT 1;";
        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        command.Parameters.AddWithValue("$profile_id", profileId);

        await using var reader = await command.ExecuteReaderAsync(ct);
        if (!await reader.ReadAsync(ct))
            return null;

        return Map(reader);
    }

    public async Task<IReadOnlyList<BuildProfile>> GetAllAsync(CancellationToken ct)
    {
        await using var connection = _factory.CreateConnection();
        await connection.OpenAsync(ct);

        var sql = "SELECT * FROM build_profiles ORDER BY display_name;";
        await using var command = connection.CreateCommand();
        command.CommandText = sql;

        var results = new List<BuildProfile>();
        await using var reader = await command.ExecuteReaderAsync(ct);

        while (await reader.ReadAsync(ct))
            results.Add(Map(reader));

        return results;
    }

    private static BuildProfile Map(Microsoft.Data.Sqlite.SqliteDataReader reader)
    {
        var targetsJson = reader.GetString(reader.GetOrdinal("targets_json"));
        var targets = JsonSerializer.Deserialize<List<string>>(targetsJson) ?? new List<string>();

        return new BuildProfile
        {
            ProfileId = reader.GetString(reader.GetOrdinal("profile_id")),
            DisplayName = reader.GetString(reader.GetOrdinal("display_name")),
            SourceDirectory = reader.GetString(reader.GetOrdinal("source_directory")),
            BuildDirectory = reader.GetString(reader.GetOrdinal("build_directory")),
            Generator = reader.GetString(reader.GetOrdinal("generator")),
            Configuration = reader.GetString(reader.GetOrdinal("configuration")),
            Targets = targets
        };
    }
}
9. Validation publishing service
This makes validation flow cleaner and reusable.

IValidationPublisher.cs
using AtlasSuite.Tooling.Validation.Models;

namespace AtlasSuite.Tooling.Validation.Interfaces;

public interface IValidationPublisher
{
    Task PublishAsync(string jobId, string sourceToolId, ValidationReport report, CancellationToken ct);
}
ValidationPublisher.cs
using AtlasSuite.Tooling.Validation.Interfaces;
using AtlasSuite.Tooling.Validation.Models;

namespace AtlasSuite.Tooling.Validation.Services;

public sealed class ValidationPublisher : IValidationPublisher
{
    private readonly IValidationReportStore _store;

    public ValidationPublisher(IValidationReportStore store)
    {
        _store = store;
    }

    public async Task PublishAsync(string jobId, string sourceToolId, ValidationReport report, CancellationToken ct)
    {
        var normalized = new ValidationReport
        {
            ReportId = string.IsNullOrWhiteSpace(report.ReportId)
                ? Guid.NewGuid().ToString("N")
                : report.ReportId,
            JobId = jobId,
            SourceToolId = sourceToolId,
            Success = report.Success,
            Summary = report.Summary,
            Issues = report.Issues
        };

        await _store.SaveAsync(normalized, ct);
    }
}
Then in ToolJobRunner, call the publisher instead of directly hitting the store.

10. WPF base classes
ViewModelBase.cs
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace AtlasSuite.Shell.ViewModels;

public abstract class ViewModelBase : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    protected void RaisePropertyChanged([CallerMemberName] string? propertyName = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));

    protected bool SetProperty<T>(ref T field, T value, [CallerMemberName] string? propertyName = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value))
            return false;

        field = value;
        RaisePropertyChanged(propertyName);
        return true;
    }
}
AsyncRelayCommand.cs
using System.Windows.Input;

namespace AtlasSuite.Shell.Commands;

public sealed class AsyncRelayCommand : ICommand
{
    private readonly Func<Task> _execute;
    private readonly Func<bool>? _canExecute;
    private bool _isRunning;

    public AsyncRelayCommand(Func<Task> execute, Func<bool>? canExecute = null)
    {
        _execute = execute;
        _canExecute = canExecute;
    }

    public event EventHandler? CanExecuteChanged;

    public bool CanExecute(object? parameter) => !_isRunning && (_canExecute?.Invoke() ?? true);

    public async void Execute(object? parameter)
    {
        if (!CanExecute(parameter))
            return;

        _isRunning = true;
        RaiseCanExecuteChanged();

        try
        {
            await _execute();
        }
        finally
        {
            _isRunning = false;
            RaiseCanExecuteChanged();
        }
    }

    public void RaiseCanExecuteChanged()
        => CanExecuteChanged?.Invoke(this, EventArgs.Empty);
}
11. Tool Registry ViewModel
ToolDescriptorItemViewModel.cs
using AtlasSuite.Tooling.Registry.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class ToolDescriptorItemViewModel : ViewModelBase
{
    public string ToolId { get; }
    public string DisplayName { get; }
    public string Category { get; }
    public string Version { get; }
    public string ExecutablePath { get; }
    public ToolHealthStatus HealthStatus { get; }

    public ToolDescriptorItemViewModel(ToolDescriptor descriptor)
    {
        ToolId = descriptor.ToolId;
        DisplayName = descriptor.DisplayName;
        Category = descriptor.Category;
        Version = descriptor.Version;
        ExecutablePath = descriptor.ExecutablePath;
        HealthStatus = descriptor.HealthStatus;
    }
}
ToolRegistryPanelViewModel.cs
using System.Collections.ObjectModel;
using AtlasSuite.Shell.Commands;
using AtlasSuite.Tooling.Registry.Interfaces;

namespace AtlasSuite.Shell.ViewModels;

public sealed class ToolRegistryPanelViewModel : ViewModelBase
{
    private readonly IToolRegistry _registry;
    private bool _isBusy;

    public ObservableCollection<ToolDescriptorItemViewModel> Tools { get; } = new();

    public bool IsBusy
    {
        get => _isBusy;
        set => SetProperty(ref _isBusy, value);
    }

    public AsyncRelayCommand RefreshCommand { get; }

    public ToolRegistryPanelViewModel(IToolRegistry registry)
    {
        _registry = registry;
        RefreshCommand = new AsyncRelayCommand(RefreshAsync, () => !IsBusy);
    }

    public async Task RefreshAsync()
    {
        IsBusy = true;
        try
        {
            await _registry.RefreshAsync(CancellationToken.None);
            var tools = await _registry.GetAllAsync(CancellationToken.None);

            Tools.Clear();
            foreach (var tool in tools.OrderBy(x => x.DisplayName))
                Tools.Add(new ToolDescriptorItemViewModel(tool));
        }
        finally
        {
            IsBusy = false;
            RefreshCommand.RaiseCanExecuteChanged();
        }
    }
}
12. Job Queue ViewModel
ToolJobItemViewModel.cs
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class ToolJobItemViewModel : ViewModelBase
{
    public string JobId { get; }
    public string Title { get; }
    public string ToolId { get; }
    public string CapabilityId { get; }
    public ToolJobStatus Status { get; }
    public int ProgressPercent { get; }
    public string Summary { get; }
    public DateTimeOffset CreatedUtc { get; }

    public ToolJobItemViewModel(ToolJobRecord record)
    {
        JobId = record.JobId;
        Title = record.Title;
        ToolId = record.ToolId;
        CapabilityId = record.CapabilityId;
        Status = record.Status;
        ProgressPercent = record.ProgressPercent;
        Summary = record.Summary;
        CreatedUtc = record.CreatedUtc;
    }
}
JobQueuePanelViewModel.cs
using System.Collections.ObjectModel;
using AtlasSuite.Shell.Commands;
using AtlasSuite.Tooling.Jobs.Interfaces;

namespace AtlasSuite.Shell.ViewModels;

public sealed class JobQueuePanelViewModel : ViewModelBase
{
    private readonly IToolJobStore _jobStore;
    private bool _isBusy;

    public ObservableCollection<ToolJobItemViewModel> Jobs { get; } = new();

    public bool IsBusy
    {
        get => _isBusy;
        set => SetProperty(ref _isBusy, value);
    }

    public AsyncRelayCommand RefreshCommand { get; }

    public JobQueuePanelViewModel(IToolJobStore jobStore)
    {
        _jobStore = jobStore;
        RefreshCommand = new AsyncRelayCommand(RefreshAsync, () => !IsBusy);
    }

    public async Task RefreshAsync()
    {
        IsBusy = true;
        try
        {
            var jobs = await _jobStore.GetRecentAsync(100, CancellationToken.None);

            Jobs.Clear();
            foreach (var job in jobs.OrderByDescending(x => x.CreatedUtc))
                Jobs.Add(new ToolJobItemViewModel(job));
        }
        finally
        {
            IsBusy = false;
            RefreshCommand.RaiseCanExecuteChanged();
        }
    }
}
13. Validation Results ViewModel
ValidationIssueItemViewModel.cs
using AtlasSuite.Tooling.Validation.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class ValidationIssueItemViewModel : ViewModelBase
{
    public string RuleId { get; }
    public string Severity { get; }
    public string Category { get; }
    public string Message { get; }
    public string? FilePath { get; }
    public int? LineNumber { get; }
    public string? SuggestedFix { get; }

    public ValidationIssueItemViewModel(ValidationIssue issue)
    {
        RuleId = issue.RuleId;
        Severity = issue.Severity;
        Category = issue.Category;
        Message = issue.Message;
        FilePath = issue.FilePath;
        LineNumber = issue.LineNumber;
        SuggestedFix = issue.SuggestedFix;
    }
}
ValidationResultsPanelViewModel.cs
using System.Collections.ObjectModel;
using AtlasSuite.Shell.Commands;
using AtlasSuite.Tooling.Validation.Interfaces;

namespace AtlasSuite.Shell.ViewModels;

public sealed class ValidationResultsPanelViewModel : ViewModelBase
{
    private readonly IValidationReportStore _store;
    private string _jobId = string.Empty;
    private string _summary = string.Empty;

    public ObservableCollection<ValidationIssueItemViewModel> Issues { get; } = new();

    public string JobId
    {
        get => _jobId;
        set => SetProperty(ref _jobId, value);
    }

    public string Summary
    {
        get => _summary;
        set => SetProperty(ref _summary, value);
    }

    public AsyncRelayCommand LoadCommand { get; }

    public ValidationResultsPanelViewModel(IValidationReportStore store)
    {
        _store = store;
        LoadCommand = new AsyncRelayCommand(LoadAsync, () => !string.IsNullOrWhiteSpace(JobId));
    }

    public async Task LoadAsync()
    {
        var report = await _store.GetByJobIdAsync(JobId, CancellationToken.None);

        Issues.Clear();
        Summary = report?.Summary ?? "No validation report found.";

        if (report is null)
            return;

        foreach (var issue in report.Issues)
            Issues.Add(new ValidationIssueItemViewModel(issue));
    }
}
14. Suggested first XAML panels
Tool Registry Panel
Columns:

DisplayName

ToolId

Category

HealthStatus

Version

ExecutablePath

Job Queue Panel
Columns:

Title

ToolId

Status

ProgressPercent

CreatedUtc

Summary

Validation Results Panel
Columns:

Severity

Category

RuleId

Message

FilePath

LineNumber

SuggestedFix

15. Dependency injection update
Updated ServiceCollectionExtensions.cs
using AtlasSuite.AtlasAI.Interfaces;
using AtlasSuite.AtlasAI.Services;
using AtlasSuite.Storage.Sqlite.Interfaces;
using AtlasSuite.Storage.Sqlite.Models;
using AtlasSuite.Storage.Sqlite.Services;
using AtlasSuite.Tooling.Artifacts.Interfaces;
using AtlasSuite.Tooling.Build.Adapters;
using AtlasSuite.Tooling.Build.Interfaces;
using AtlasSuite.Tooling.Jobs.Background;
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Services;
using AtlasSuite.Tooling.Logging.Interfaces;
using AtlasSuite.Tooling.Parse.Adapters;
using AtlasSuite.Tooling.Process.Interfaces;
using AtlasSuite.Tooling.Process.Services;
using AtlasSuite.Tooling.Registry.Interfaces;
using AtlasSuite.Tooling.Registry.Services;
using AtlasSuite.Tooling.Search.Adapters;
using AtlasSuite.Tooling.Validation.Interfaces;
using AtlasSuite.Tooling.Validation.Services;
using Microsoft.Extensions.DependencyInjection;

namespace AtlasSuite.Shell.Services;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddAtlasSuiteCore(this IServiceCollection services, string databasePath)
    {
        services.AddSingleton(new SqliteOptions { DatabasePath = databasePath });
        services.AddSingleton<ISqliteConnectionFactory, SqliteConnectionFactory>();
        services.AddSingleton<SqliteDatabaseInitializer>();

        services.AddSingleton<IProcessRunner, ProcessRunner>();

        services.AddSingleton<IToolCapabilityAdapter, RipgrepAdapter>();
        services.AddSingleton<IToolCapabilityAdapter, TreeSitterAdapter>();
        services.AddSingleton<IToolCapabilityAdapter, CMakeNinjaBuildAdapter>();

        services.AddSingleton<IToolRegistry, ToolRegistry>();

        services.AddSingleton<IToolJobStore, SqliteToolJobStore>();
        services.AddSingleton<IArtifactStore, SqliteArtifactStore>();
        services.AddSingleton<IValidationReportStore, SqliteValidationReportStore>();
        services.AddSingleton<IToolLogStore, SqliteToolLogStore>();
        services.AddSingleton<IBuildProfileStore, SqliteBuildProfileStore>();
        services.AddSingleton<IValidationPublisher, ValidationPublisher>();

        services.AddSingleton<ToolJobQueue>();
        services.AddSingleton<IToolJobQueue>(sp => sp.GetRequiredService<ToolJobQueue>());
        services.AddSingleton<IToolJobRunner, ToolJobRunner>();
        services.AddSingleton<IToolJobDispatcher, ToolJobDispatcher>();

        services.AddSingleton<IAtlasAIToolPlanner, AtlasAIToolPlanner>();
        services.AddSingleton<IAtlasAIToolExecutor, AtlasAIToolExecutor>();

        return services;
    }
}
16. First real startup flow
Your App.xaml.cs or host bootstrap should do:

var services = new ServiceCollection();
services.AddAtlasSuiteCore("atlas_suite.db");

var provider = services.BuildServiceProvider();

var dbInitializer = provider.GetRequiredService<SqliteDatabaseInitializer>();
await dbInitializer.InitializeAsync(CancellationToken.None);

var toolRegistry = provider.GetRequiredService<IToolRegistry>();
await toolRegistry.RefreshAsync(CancellationToken.None);

var dispatcher = provider.GetRequiredService<IToolJobDispatcher>();
await dispatcher.StartAsync(CancellationToken.None);
That gives you:

DB initialized

tools discovered

queue runner live

17. What Phase 3 gives you operationally
After this phase, Atlas Suite can now:

register tools

save jobs

auto-run queued jobs

persist logs

persist validation reports

persist build profiles

run real ripgrep searches

surface tool registry and job queue in WPF

load validation issues per job

That is the first point where the platform starts to feel alive.

18. Biggest remaining gaps after Phase 3
Now the next major holes are:

A. real Tree-sitter bridge
Still stubbed.

B. process-based tool health checks
Current health checks are optimistic placeholders.

C. job progress streaming
Progress jumps instead of streaming incrementally.

D. AtlasAI execution follow-through
AtlasAI queues jobs, but doesn’t yet track completion and chain steps based on results.

E. artifact viewer UI
Artifacts are stored but not surfaced well.

F. build panel UI
Profiles exist, but no proper build execution panel yet.

G. Blender adapter foundation
Still not started.

19. Best next implementation order
I’d go:

Build Panel + Build Profile UI

Artifact Viewer Panel

real tool health probes

Tree-sitter bridge

AtlasAI job tracking / result chaining

Blender adapter base

Validation issue actions

Diagnostics panel

That gives you a much more complete working shell.

20. Strongest next deliverable
The next best pack is:

Phase 4 scaffold pack
with:

Build Panel ViewModels + XAML structure

Artifact Viewer ViewModels

Diagnostics Panel ViewModels

real health-check execution for ripgrep/CMake/Ninja

Tree-sitter bridge scaffold

AtlasAI execution tracker

Blender adapter base scaffold

That would move Atlas Suite from “functional shell” into “actual serious development environment.”


yes

next steps please

Absolutely — here are the best next steps for Atlas Suite, in the right order, so you stop planning in circles and start turning it into a real platform.

Immediate next steps
1. Lock the foundation contracts
Before adding more features, freeze the core interfaces for:

tool registry

tool adapters

job queue

job runner

artifact store

validation publisher

AtlasAI planner/executor

This prevents refactor churn while the rest of the suite is built.

2. Build the first usable shell
Get Atlas Suite opening as a real WPF app with these panels only:

Tool Registry

Job Queue

Build Panel

Validation Results

AtlasAI Panel

Do not overbuild the UI yet. Just make the shell usable.

3. Finish the first real vertical slice
Your first end-to-end workflow should be:

launch Atlas Suite

initialize SQLite

refresh tools

load a saved build profile

run ripgrep search

queue a build configure

queue a compile

capture logs

show results in Job Queue

show validation/build issues

Once this works, Atlas Suite becomes real.

What to build next
Phase 4 target
This should be the next implementation milestone.

A. Build Panel
Add:

build profile selector

configure button

build button

target selector

configuration selector

live build status

recent build history

This becomes one of the main daily-use panels.

B. Artifact Viewer
You already store artifacts. Now surface them.

Show:

artifacts by job

file path

type

size

created time

Actions:

open

reveal in folder

compare later

C. Diagnostics Panel
Aggregate:

recent logs

failed jobs

unhealthy tools

repeated errors

This becomes your “what’s broken right now” panel.

D. Real health checks
Replace optimistic health reporting with actual checks for:

ripgrep

cmake

ninja

later blender

That way Atlas Suite can tell you what is really installed and usable.

E. Tree-sitter bridge
This is one of the biggest next-value items.

Once added, AtlasAI can:

inspect code structure

locate classes/functions

target edits safely

understand repo layout much better

F. AtlasAI execution tracker
Right now AtlasAI can plan and queue jobs. Next it needs to:

watch jobs complete

inspect results

decide follow-up steps

stop on failure

summarize outcomes

That makes AtlasAI start feeling intelligent inside the suite instead of just being a request generator.

After that
4. Start Blender integration base
After Build + Diagnostics + Tree-sitter, begin the Blender foundation:

Blender tool health check

Blender path settings

Blender adapter scaffold

basic open-in-Blender command

export job contract

placeholder Atlas Blender add-on structure

Do not start with full export automation yet. Start with controlled integration.

5. Add Build Profile management UI
You already have persistence. Now expose it.

Need:

create profile

edit profile

duplicate profile

save default profile

pick targets

This makes build workflows practical.

6. Add log viewer and per-job details
You are storing logs now. Surface them per job.

Need:

stdout/stderr view

severity filters

search within logs

copy/export logs

That will massively improve debugging.

Strong recommended implementation order
Do it in this order:

Build Panel

Diagnostics Panel

Artifact Viewer

real tool health checks

Tree-sitter bridge

AtlasAI execution tracker

Build Profile editor

per-job log viewer

Blender adapter base

Blender add-on skeleton

That order gives the most value fastest.

What not to do yet
Do not jump into:

full multi-user collaboration

full cloud sync

advanced Blender automation

PCG tooling panels

voxel authoring tools

massive AtlasAI autonomy

Those should come after the shell is trustworthy.

Definition of “good enough” before moving on
Before starting major new tooling, Atlas Suite should already be able to:

boot reliably

detect tools

queue jobs

run jobs automatically

save logs

save artifacts

save validation reports

show job status in UI

run builds from UI

let AtlasAI plan and launch tool actions safely

Once that exists, the rest can grow on solid ground.

Best next milestone
Your next milestone should be:

Atlas Suite Milestone 1 — Functional Tooling Shell
Deliverables:

WPF shell running

Tool Registry panel working

Job Queue panel working

Build panel working

Diagnostics panel working

Artifact viewer basic

real ripgrep and CMake/Ninja integration

SQLite persistence live

AtlasAI can plan and queue actions

That is the first version worth using regularly.

After Milestone 1
Then move to:

Milestone 2 — Code Intelligence + Controlled DCC
Deliverables:

Tree-sitter bridge

AtlasAI result-aware execution

Blender adapter base

Blender settings + health check

simple source asset open/export workflow

Then:

Milestone 3 — Content Pipeline Expansion
Deliverables:

Blender add-on

asset manifests

texture pipeline

validation automation

Assimp/OpenImageIO integration

Strongest immediate action
The single best thing to do next is:

build Phase 4 now around Build Panel, Diagnostics, Artifact Viewer, real health checks, and Tree-sitter scaffold

That’s the cleanest jump from architecture to a genuinely useful Atlas Suite.


yes

Excellent — here’s the Phase 4 scaffold pack and the concrete next move set for Atlas Suite.

This phase is where the suite starts becoming a serious day-to-day development environment instead of just a framework with panels.

Atlas Suite — Phase 4 Scaffold Pack
This phase adds:

Build Panel ViewModels + structure

Artifact Viewer ViewModels

Diagnostics Panel ViewModels

real tool health probes

Tree-sitter bridge scaffold

AtlasAI execution tracker

Blender adapter base scaffold

Using your locked naming:

Atlas Suite = tooling shell

AtlasAI = integrated AI system

1. Phase 4 goals
By the end of this phase, Atlas Suite should be able to:

show real build profiles and launch build jobs from UI

inspect artifacts produced by jobs

surface logs, failures, and unhealthy tools in one diagnostics view

detect whether core tools are actually installed

prepare for code intelligence with a real parser bridge

track AtlasAI plan execution beyond simple queueing

begin managed Blender integration cleanly

2. Recommended implementation order inside Phase 4
Do these in this order:

real health probes

Build Panel

Artifact Viewer

Diagnostics Panel

AtlasAI execution tracker

Tree-sitter bridge scaffold

Blender adapter base

That gives you value fast while keeping complexity under control.

3. Real tool health probes
Right now tool health is optimistic. Fix that first.

New interface: IToolHealthProbe.cs
namespace AtlasSuite.Tooling.Registry.Interfaces;

public interface IToolHealthProbe
{
    Task<Models.ToolHealthReport> ProbeAsync(string toolId, CancellationToken ct);
}
Helper: ExecutableProbeService.cs
using AtlasSuite.Tooling.Process.Interfaces;
using AtlasSuite.Tooling.Process.Models;
using AtlasSuite.Tooling.Registry.Models;

namespace AtlasSuite.Tooling.Registry.Services;

public sealed class ExecutableProbeService
{
    private readonly IProcessRunner _processRunner;

    public ExecutableProbeService(IProcessRunner processRunner)
    {
        _processRunner = processRunner;
    }

    public async Task<ToolHealthReport> ProbeVersionAsync(
        string toolId,
        string displayName,
        string executable,
        string versionArgs,
        CancellationToken ct)
    {
        try
        {
            var result = await _processRunner.RunAsync(new ProcessExecutionRequest
            {
                FileName = executable,
                Arguments = versionArgs,
                Timeout = TimeSpan.FromSeconds(10)
            }, ct);

            if (result.TimedOut)
            {
                return new ToolHealthReport
                {
                    ToolId = toolId,
                    Status = ToolHealthStatus.Warning,
                    Version = string.Empty,
                    Message = $"{displayName} probe timed out.",
                    ExecutablePath = executable
                };
            }

            var output = string.IsNullOrWhiteSpace(result.StandardOutput)
                ? result.StandardError
                : result.StandardOutput;

            return new ToolHealthReport
            {
                ToolId = toolId,
                Status = result.ExitCode == 0 ? ToolHealthStatus.Healthy : ToolHealthStatus.Warning,
                Version = ExtractSingleLine(output),
                Message = result.ExitCode == 0
                    ? $"{displayName} detected."
                    : $"{displayName} returned non-zero exit code.",
                ExecutablePath = executable
            };
        }
        catch (Exception ex)
        {
            return new ToolHealthReport
            {
                ToolId = toolId,
                Status = ToolHealthStatus.Missing,
                Version = string.Empty,
                Message = $"{displayName} not available: {ex.Message}",
                ExecutablePath = executable
            };
        }
    }

    private static string ExtractSingleLine(string text)
    {
        if (string.IsNullOrWhiteSpace(text))
            return string.Empty;

        return text.Split(new[] { "\r\n", "\n" }, StringSplitOptions.RemoveEmptyEntries)
            .FirstOrDefault() ?? string.Empty;
    }
}
Update RipgrepAdapter.cs health check
private readonly ExecutableProbeService _probeService;

public RipgrepAdapter(IProcessRunner processRunner, ExecutableProbeService probeService)
{
    _processRunner = processRunner;
    _probeService = probeService;
}

public Task<ToolHealthReport> CheckHealthAsync(CancellationToken ct)
    => _probeService.ProbeVersionAsync(ToolId, DisplayName, "rg", "--version", ct);
Update CMakeNinjaBuildAdapter.cs health check
Use CMake as the primary probe:

private readonly ExecutableProbeService _probeService;

public CMakeNinjaBuildAdapter(IProcessRunner processRunner, ExecutableProbeService probeService)
{
    _processRunner = processRunner;
    _probeService = probeService;
}

public Task<ToolHealthReport> CheckHealthAsync(CancellationToken ct)
    => _probeService.ProbeVersionAsync(ToolId, DisplayName, "cmake", "--version", ct);
Later add a second Ninja-specific probe.

4. Build Panel scaffold
This becomes one of the main daily-use panels.

BuildProfileItemViewModel.cs
using AtlasSuite.Tooling.Build.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class BuildProfileItemViewModel : ViewModelBase
{
    public string ProfileId { get; }
    public string DisplayName { get; }
    public string SourceDirectory { get; }
    public string BuildDirectory { get; }
    public string Generator { get; }
    public string Configuration { get; }
    public string TargetsDisplay { get; }

    public BuildProfileItemViewModel(BuildProfile profile)
    {
        ProfileId = profile.ProfileId;
        DisplayName = profile.DisplayName;
        SourceDirectory = profile.SourceDirectory;
        BuildDirectory = profile.BuildDirectory;
        Generator = profile.Generator;
        Configuration = profile.Configuration;
        TargetsDisplay = string.Join(", ", profile.Targets);
    }
}
BuildPanelViewModel.cs
using System.Collections.ObjectModel;
using AtlasSuite.Shell.Commands;
using AtlasSuite.Tooling.Build.Interfaces;
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class BuildPanelViewModel : ViewModelBase
{
    private readonly IBuildProfileStore _profileStore;
    private readonly IToolJobQueue _jobQueue;

    private BuildProfileItemViewModel? _selectedProfile;
    private string _selectedTarget = string.Empty;
    private string _selectedConfiguration = "Debug";
    private bool _isBusy;
    private string _statusMessage = "Ready.";

    public ObservableCollection<BuildProfileItemViewModel> Profiles { get; } = new();

    public BuildProfileItemViewModel? SelectedProfile
    {
        get => _selectedProfile;
        set => SetProperty(ref _selectedProfile, value);
    }

    public string SelectedTarget
    {
        get => _selectedTarget;
        set => SetProperty(ref _selectedTarget, value);
    }

    public string SelectedConfiguration
    {
        get => _selectedConfiguration;
        set => SetProperty(ref _selectedConfiguration, value);
    }

    public bool IsBusy
    {
        get => _isBusy;
        set => SetProperty(ref _isBusy, value);
    }

    public string StatusMessage
    {
        get => _statusMessage;
        set => SetProperty(ref _statusMessage, value);
    }

    public AsyncRelayCommand RefreshProfilesCommand { get; }
    public AsyncRelayCommand QueueConfigureCommand { get; }
    public AsyncRelayCommand QueueBuildCommand { get; }

    public BuildPanelViewModel(
        IBuildProfileStore profileStore,
        IToolJobQueue jobQueue)
    {
        _profileStore = profileStore;
        _jobQueue = jobQueue;

        RefreshProfilesCommand = new AsyncRelayCommand(RefreshProfilesAsync, () => !IsBusy);
        QueueConfigureCommand = new AsyncRelayCommand(QueueConfigureAsync, () => !IsBusy && SelectedProfile is not null);
        QueueBuildCommand = new AsyncRelayCommand(QueueBuildAsync, () => !IsBusy && SelectedProfile is not null);
    }

    public async Task RefreshProfilesAsync()
    {
        IsBusy = true;
        try
        {
            var profiles = await _profileStore.GetAllAsync(CancellationToken.None);

            Profiles.Clear();
            foreach (var profile in profiles.OrderBy(x => x.DisplayName))
                Profiles.Add(new BuildProfileItemViewModel(profile));

            StatusMessage = $"Loaded {Profiles.Count} build profile(s).";
        }
        finally
        {
            IsBusy = false;
            RaiseCommandStates();
        }
    }

    private async Task QueueConfigureAsync()
    {
        if (SelectedProfile is null)
            return;

        IsBusy = true;
        try
        {
            var request = new ToolExecutionRequest
            {
                ToolId = "tool.build.cmake",
                CapabilityId = "cap.build.configure",
                RequestKind = "Build",
                WorkspaceRoot = SelectedProfile.SourceDirectory,
                RequestedBy = "BuildPanel",
                CorrelationId = Guid.NewGuid().ToString("N"),
                Parameters = new Dictionary<string, string>
                {
                    ["sourceDir"] = SelectedProfile.SourceDirectory,
                    ["buildDir"] = SelectedProfile.BuildDirectory,
                    ["generator"] = SelectedProfile.Generator,
                    ["config"] = SelectedConfiguration
                }
            };

            await _jobQueue.EnqueueAsync(request, $"Configure {SelectedProfile.DisplayName}", CancellationToken.None);
            StatusMessage = $"Queued configure for '{SelectedProfile.DisplayName}'.";
        }
        finally
        {
            IsBusy = false;
            RaiseCommandStates();
        }
    }

    private async Task QueueBuildAsync()
    {
        if (SelectedProfile is null)
            return;

        IsBusy = true;
        try
        {
            var request = new ToolExecutionRequest
            {
                ToolId = "tool.build.cmake",
                CapabilityId = "cap.build.compile",
                RequestKind = "Build",
                WorkspaceRoot = SelectedProfile.SourceDirectory,
                RequestedBy = "BuildPanel",
                CorrelationId = Guid.NewGuid().ToString("N"),
                Parameters = new Dictionary<string, string>
                {
                    ["buildDir"] = SelectedProfile.BuildDirectory,
                    ["config"] = SelectedConfiguration,
                    ["target"] = SelectedTarget
                }
            };

            await _jobQueue.EnqueueAsync(request, $"Build {SelectedProfile.DisplayName}", CancellationToken.None);
            StatusMessage = $"Queued build for '{SelectedProfile.DisplayName}'.";
        }
        finally
        {
            IsBusy = false;
            RaiseCommandStates();
        }
    }

    private void RaiseCommandStates()
    {
        RefreshProfilesCommand.RaiseCanExecuteChanged();
        QueueConfigureCommand.RaiseCanExecuteChanged();
        QueueBuildCommand.RaiseCanExecuteChanged();
    }
}
Suggested Build Panel XAML structure
Layout:

top row: profile dropdown, configuration dropdown, target textbox/dropdown

buttons: Refresh Profiles / Queue Configure / Queue Build

bottom area: selected profile details + status

5. Artifact Viewer scaffold
Artifacts are already being saved. Now make them visible.

IArtifactQueryService.cs
using AtlasSuite.Tooling.Artifacts.Models;

namespace AtlasSuite.Tooling.Artifacts.Interfaces;

public interface IArtifactQueryService
{
    Task<IReadOnlyList<ToolArtifactRecord>> GetByJobIdAsync(string jobId, CancellationToken ct);
}
Your existing store can implement this too.

ArtifactItemViewModel.cs
using AtlasSuite.Tooling.Artifacts.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class ArtifactItemViewModel : ViewModelBase
{
    public string ArtifactId { get; }
    public string ArtifactType { get; }
    public string DisplayName { get; }
    public string FilePath { get; }
    public string ProducedByToolId { get; }
    public long SizeBytes { get; }
    public DateTimeOffset CreatedUtc { get; }

    public ArtifactItemViewModel(ToolArtifactRecord artifact)
    {
        ArtifactId = artifact.ArtifactId;
        ArtifactType = artifact.ArtifactType;
        DisplayName = artifact.DisplayName;
        FilePath = artifact.FilePath;
        ProducedByToolId = artifact.ProducedByToolId;
        SizeBytes = artifact.SizeBytes;
        CreatedUtc = artifact.CreatedUtc;
    }
}
ArtifactViewerPanelViewModel.cs
using System.Collections.ObjectModel;
using AtlasSuite.Shell.Commands;
using AtlasSuite.Tooling.Artifacts.Interfaces;

namespace AtlasSuite.Shell.ViewModels;

public sealed class ArtifactViewerPanelViewModel : ViewModelBase
{
    private readonly IArtifactStore _artifactStore;
    private string _jobId = string.Empty;
    private string _statusMessage = "Enter a job id.";
    private bool _isBusy;

    public ObservableCollection<ArtifactItemViewModel> Artifacts { get; } = new();

    public string JobId
    {
        get => _jobId;
        set => SetProperty(ref _jobId, value);
    }

    public string StatusMessage
    {
        get => _statusMessage;
        set => SetProperty(ref _statusMessage, value);
    }

    public bool IsBusy
    {
        get => _isBusy;
        set => SetProperty(ref _isBusy, value);
    }

    public AsyncRelayCommand LoadArtifactsCommand { get; }

    public ArtifactViewerPanelViewModel(IArtifactStore artifactStore)
    {
        _artifactStore = artifactStore;
        LoadArtifactsCommand = new AsyncRelayCommand(LoadArtifactsAsync, () => !IsBusy && !string.IsNullOrWhiteSpace(JobId));
    }

    public async Task LoadArtifactsAsync()
    {
        IsBusy = true;
        try
        {
            var artifacts = await _artifactStore.GetByJobIdAsync(JobId, CancellationToken.None);

            Artifacts.Clear();
            foreach (var artifact in artifacts.OrderBy(x => x.CreatedUtc))
                Artifacts.Add(new ArtifactItemViewModel(artifact));

            StatusMessage = $"Loaded {Artifacts.Count} artifact(s).";
        }
        finally
        {
            IsBusy = false;
            LoadArtifactsCommand.RaiseCanExecuteChanged();
        }
    }
}
Suggested Artifact Viewer XAML structure
Columns:

DisplayName

ArtifactType

ProducedByToolId

FilePath

SizeBytes

CreatedUtc

Later add buttons:

Open

Reveal in Explorer

Compare

6. Diagnostics Panel scaffold
This becomes the “what is broken right now” view.

DiagnosticsPanelViewModel.cs
using System.Collections.ObjectModel;
using AtlasSuite.Shell.Commands;
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Logging.Interfaces;
using AtlasSuite.Tooling.Registry.Interfaces;
using AtlasSuite.Tooling.Registry.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class DiagnosticsPanelViewModel : ViewModelBase
{
    private readonly IToolRegistry _toolRegistry;
    private readonly IToolJobStore _jobStore;
    private readonly IToolLogStore _logStore;
    private bool _isBusy;
    private string _statusMessage = "Ready.";

    public ObservableCollection<ToolDescriptorItemViewModel> UnhealthyTools { get; } = new();
    public ObservableCollection<ToolJobItemViewModel> FailedJobs { get; } = new();
    public ObservableCollection<RecentLogItemViewModel> RecentLogs { get; } = new();

    public bool IsBusy
    {
        get => _isBusy;
        set => SetProperty(ref _isBusy, value);
    }

    public string StatusMessage
    {
        get => _statusMessage;
        set => SetProperty(ref _statusMessage, value);
    }

    public AsyncRelayCommand RefreshCommand { get; }

    public DiagnosticsPanelViewModel(
        IToolRegistry toolRegistry,
        IToolJobStore jobStore,
        IToolLogStore logStore)
    {
        _toolRegistry = toolRegistry;
        _jobStore = jobStore;
        _logStore = logStore;
        RefreshCommand = new AsyncRelayCommand(RefreshAsync, () => !IsBusy);
    }

    public async Task RefreshAsync()
    {
        IsBusy = true;
        try
        {
            await _toolRegistry.RefreshAsync(CancellationToken.None);
            var tools = await _toolRegistry.GetAllAsync(CancellationToken.None);
            var failedJobs = await _jobStore.GetByStatusAsync(Tooling.Jobs.Models.ToolJobStatus.Failed, 50, CancellationToken.None);
            var logs = await _logStore.GetRecentAsync(100, CancellationToken.None);

            UnhealthyTools.Clear();
            foreach (var tool in tools.Where(t => t.HealthStatus != ToolHealthStatus.Healthy))
                UnhealthyTools.Add(new ToolDescriptorItemViewModel(tool));

            FailedJobs.Clear();
            foreach (var job in failedJobs.OrderByDescending(x => x.CreatedUtc))
                FailedJobs.Add(new ToolJobItemViewModel(job));

            RecentLogs.Clear();
            foreach (var log in logs.OrderByDescending(x => x.TimestampUtc))
                RecentLogs.Add(new RecentLogItemViewModel(log));

            StatusMessage = $"Diagnostics updated. Unhealthy tools: {UnhealthyTools.Count}, Failed jobs: {FailedJobs.Count}.";
        }
        finally
        {
            IsBusy = false;
            RefreshCommand.RaiseCanExecuteChanged();
        }
    }
}
RecentLogItemViewModel.cs
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class RecentLogItemViewModel : ViewModelBase
{
    public string JobId { get; }
    public string ToolId { get; }
    public LogSeverity Severity { get; }
    public DateTimeOffset TimestampUtc { get; }
    public string Message { get; }

    public RecentLogItemViewModel(ToolLogRecord log)
    {
        JobId = log.JobId;
        ToolId = log.ToolId;
        Severity = log.Severity;
        TimestampUtc = log.TimestampUtc;
        Message = log.Message;
    }
}
Suggested Diagnostics XAML structure
Three sections:

top-left: unhealthy tools

top-right: failed jobs

bottom: recent logs

7. Tree-sitter bridge scaffold
Do not fully implement parsing yet. Build the clean bridge first.

ISyntaxTreeBridge.cs
namespace AtlasSuite.Tooling.Parse.Interfaces;

public interface ISyntaxTreeBridge
{
    Task<ParseFileResult> ParseFileAsync(string filePath, CancellationToken ct);
}
ParseFileResult.cs
namespace AtlasSuite.Tooling.Parse.Models;

public sealed class ParseFileResult
{
    public bool Success { get; init; }
    public string FilePath { get; init; } = string.Empty;
    public string Language { get; init; } = string.Empty;
    public IReadOnlyList<ParsedSymbol> Symbols { get; init; } = Array.Empty<ParsedSymbol>();
    public IReadOnlyList<string> Errors { get; init; } = Array.Empty<string>();
}
ParsedSymbol.cs
namespace AtlasSuite.Tooling.Parse.Models;

public sealed class ParsedSymbol
{
    public string SymbolKind { get; init; } = string.Empty;
    public string Name { get; init; } = string.Empty;
    public int StartLine { get; init; }
    public int EndLine { get; init; }
    public string ParentName { get; init; } = string.Empty;
}
TreeSitterBridgeStub.cs
using AtlasSuite.Tooling.Parse.Interfaces;
using AtlasSuite.Tooling.Parse.Models;

namespace AtlasSuite.Tooling.Parse.Services;

public sealed class TreeSitterBridgeStub : ISyntaxTreeBridge
{
    public Task<ParseFileResult> ParseFileAsync(string filePath, CancellationToken ct)
    {
        return Task.FromResult(new ParseFileResult
        {
            Success = false,
            FilePath = filePath,
            Language = "unknown",
            Errors = new[] { "Tree-sitter bridge not yet implemented." }
        });
    }
}
Update TreeSitterAdapter.cs
Inject the bridge and make it use file input:

private readonly AtlasSuite.Tooling.Parse.Interfaces.ISyntaxTreeBridge _bridge;

public TreeSitterAdapter(AtlasSuite.Tooling.Parse.Interfaces.ISyntaxTreeBridge bridge)
{
    _bridge = bridge;
}
Then in ExecuteAsync, parse the first input file or a filePath parameter and return structured symbol data.

8. AtlasAI execution tracker
Right now AtlasAI queues jobs but does not understand completion state.

AtlasAITrackedPlanState.cs
namespace AtlasSuite.AtlasAI.Models;

public sealed class AtlasAITrackedPlanState
{
    public string PlanId { get; init; } = string.Empty;
    public string Goal { get; init; } = string.Empty;
    public string Status { get; set; } = "Queued";
    public IReadOnlyList<AtlasAITrackedStepState> Steps { get; init; } = Array.Empty<AtlasAITrackedStepState>();
    public string Summary { get; set; } = string.Empty;
}
AtlasAITrackedStepState.cs
namespace AtlasSuite.AtlasAI.Models;

public sealed class AtlasAITrackedStepState
{
    public int Order { get; init; }
    public string Description { get; init; } = string.Empty;
    public string JobId { get; init; } = string.Empty;
    public string Status { get; set; } = "Queued";
    public string ResultSummary { get; set; } = string.Empty;
}
IAtlasAIExecutionTracker.cs
using AtlasSuite.AtlasAI.Models;

namespace AtlasSuite.AtlasAI.Interfaces;

public interface IAtlasAIExecutionTracker
{
    Task<AtlasAITrackedPlanState> TrackPlanAsync(AtlasAIToolPlan plan, IReadOnlyList<string> jobIds, CancellationToken ct);
    Task<AtlasAITrackedPlanState?> GetPlanStateAsync(string planId, CancellationToken ct);
}
AtlasAIExecutionTracker.cs
using AtlasSuite.AtlasAI.Interfaces;
using AtlasSuite.AtlasAI.Models;
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.AtlasAI.Services;

public sealed class AtlasAIExecutionTracker : IAtlasAIExecutionTracker
{
    private readonly IToolJobStore _jobStore;
    private readonly Dictionary<string, AtlasAITrackedPlanState> _plans = new(StringComparer.OrdinalIgnoreCase);

    public AtlasAIExecutionTracker(IToolJobStore jobStore)
    {
        _jobStore = jobStore;
    }

    public Task<AtlasAITrackedPlanState?> GetPlanStateAsync(string planId, CancellationToken ct)
    {
        _plans.TryGetValue(planId, out var state);
        return Task.FromResult(state);
    }

    public async Task<AtlasAITrackedPlanState> TrackPlanAsync(AtlasAIToolPlan plan, IReadOnlyList<string> jobIds, CancellationToken ct)
    {
        var steps = new List<AtlasAITrackedStepState>();

        for (var i = 0; i < plan.Steps.Count; i++)
        {
            var jobId = i < jobIds.Count ? jobIds[i] : string.Empty;
            var step = plan.Steps[i];

            var job = string.IsNullOrWhiteSpace(jobId)
                ? null
                : await _jobStore.GetAsync(jobId, ct);

            steps.Add(new AtlasAITrackedStepState
            {
                Order = step.Order,
                Description = step.Description,
                JobId = jobId,
                Status = job?.Status.ToString() ?? "Unknown",
                ResultSummary = job?.Summary ?? string.Empty
            });
        }

        var overallStatus = steps.All(s => s.Status == ToolJobStatus.Succeeded.ToString())
            ? "Succeeded"
            : steps.Any(s => s.Status == ToolJobStatus.Failed.ToString())
                ? "Failed"
                : steps.Any(s => s.Status == ToolJobStatus.Running.ToString())
                    ? "Running"
                    : "Queued";

        var state = new AtlasAITrackedPlanState
        {
            PlanId = plan.PlanId,
            Goal = plan.Goal,
            Status = overallStatus,
            Summary = $"Tracked {steps.Count} AtlasAI step(s).",
            Steps = steps
        };

        _plans[plan.PlanId] = state;
        return state;
    }
}
Next update to AtlasAIToolExecutor.cs
Have it return queued jobs and optionally call tracker.

9. Blender adapter base scaffold
Do not overbuild yet. Just create a proper managed tool base.

BlenderAdapter.cs
using AtlasSuite.Tooling.Jobs.Models;
using AtlasSuite.Tooling.Process.Interfaces;
using AtlasSuite.Tooling.Registry.Interfaces;
using AtlasSuite.Tooling.Registry.Models;
using AtlasSuite.Tooling.Registry.Services;

namespace AtlasSuite.Tooling.Blender.Adapters;

public sealed class BlenderAdapter : IToolCapabilityAdapter
{
    private readonly IProcessRunner _processRunner;
    private readonly ExecutableProbeService _probeService;

    public BlenderAdapter(
        IProcessRunner processRunner,
        ExecutableProbeService probeService)
    {
        _processRunner = processRunner;
        _probeService = probeService;
    }

    public string ToolId => "tool.dcc.blender";
    public string DisplayName => "Blender";

    public Task<ToolHealthReport> CheckHealthAsync(CancellationToken ct)
        => _probeService.ProbeVersionAsync(ToolId, DisplayName, "blender", "--version", ct);

    public Task<IReadOnlyList<ToolCapabilityDescriptor>> GetCapabilitiesAsync(CancellationToken ct)
    {
        IReadOnlyList<ToolCapabilityDescriptor> capabilities =
        [
            new ToolCapabilityDescriptor
            {
                CapabilityId = "cap.blender.open",
                DisplayName = "Open Asset In Blender",
                Description = "Launches Blender with the requested asset.",
                SupportedRequestKinds = new[] { "Inspect", "Edit" },
                SupportsDryRun = false,
                ProducesArtifacts = false,
                ProducesStructuredData = false
            },
            new ToolCapabilityDescriptor
            {
                CapabilityId = "cap.blender.export",
                DisplayName = "Export Asset",
                Description = "Exports an asset using Atlas pipeline settings.",
                SupportedRequestKinds = new[] { "Generate", "Convert" },
                SupportsDryRun = true,
                ProducesArtifacts = true,
                ProducesStructuredData = true
            }
        ];

        return Task.FromResult(capabilities);
    }

    public Task<ToolExecutionResult> ExecuteAsync(ToolExecutionRequest request, CancellationToken ct)
    {
        return request.CapabilityId switch
        {
            "cap.blender.open" => OpenAsync(request, ct),
            "cap.blender.export" => ExportAsync(request, ct),
            _ => Task.FromResult(new ToolExecutionResult
            {
                Success = false,
                ToolId = ToolId,
                CapabilityId = request.CapabilityId,
                ExitCode = -1,
                Summary = $"Unsupported Blender capability '{request.CapabilityId}'.",
                Errors = new[] { $"Unsupported Blender capability '{request.CapabilityId}'." }
            })
        };
    }

    private Task<ToolExecutionResult> OpenAsync(ToolExecutionRequest request, CancellationToken ct)
    {
        return Task.FromResult(new ToolExecutionResult
        {
            Success = false,
            ToolId = ToolId,
            CapabilityId = request.CapabilityId,
            ExitCode = -1,
            Summary = "Blender open command scaffolded but not implemented."
        });
    }

    private Task<ToolExecutionResult> ExportAsync(ToolExecutionRequest request, CancellationToken ct)
    {
        return Task.FromResult(new ToolExecutionResult
        {
            Success = false,
            ToolId = ToolId,
            CapabilityId = request.CapabilityId,
            ExitCode = -1,
            Summary = request.IsDryRun
                ? "Blender export dry-run scaffold ready."
                : "Blender export scaffolded but not implemented."
        });
    }
}
10. DI updates for Phase 4
Update ServiceCollectionExtensions.cs:

using AtlasSuite.AtlasAI.Interfaces;
using AtlasSuite.AtlasAI.Services;
using AtlasSuite.Tooling.Blender.Adapters;
using AtlasSuite.Tooling.Parse.Interfaces;
using AtlasSuite.Tooling.Parse.Services;
using AtlasSuite.Tooling.Registry.Services;
Add registrations:

services.AddSingleton<ExecutableProbeService>();

services.AddSingleton<ISyntaxTreeBridge, TreeSitterBridgeStub>();

services.AddSingleton<IToolCapabilityAdapter, BlenderAdapter>();

services.AddSingleton<IAtlasAIExecutionTracker, AtlasAIExecutionTracker>();
11. Suggested Phase 4 startup behavior
When Atlas Suite starts:

initialize SQLite

start job dispatcher

refresh tool registry using real probes

load build profiles

refresh diagnostics

bring up AtlasAI panel with tracker state ready

allow build/configure/search workflows immediately

That makes the suite feel alive from launch.

12. Milestone target after Phase 4
At the end of this phase, Atlas Suite should support this real workflow:

open suite

see actual health of ripgrep / CMake / Blender

load build profiles

queue configure/build from UI

see build jobs run automatically

inspect logs in diagnostics

inspect artifacts by job

let AtlasAI queue actions and track step state

keep parser integration path ready

keep Blender integration path ready

That is a strong Milestone 1 functional shell.

13. Biggest remaining gaps after Phase 4
Once this phase is done, the next major gaps are:

A. actual Tree-sitter implementation
Still stubbed.

B. per-job detailed log viewer
Logs are stored, but no dedicated drill-down UI yet.

C. build history and last result summary panel
Useful for daily work.

D. artifact actions
Open/reveal/compare still need commands.

E. Blender executable path settings
Some systems will not have blender on PATH.

F. AtlasAI chained step execution
Tracking exists, but autonomous continuation still needs rules.

G. build profile editor
Profiles can be stored, but editing UI still needs to be added.

14. Best next steps after Phase 4
Do these next:

Build Profile Editor panel

Job Details / Log Viewer panel

Artifact actions

real Tree-sitter implementation

Blender settings + executable locator

AtlasAI step result chaining

Build history panel

Validation issue actions

That would push Atlas Suite from “functional shell” to “practical working environment.”

15. The most important practical next step
If you want the cleanest immediate progress path, build this specific UI set next:

Build Panel

Job Queue Panel

Diagnostics Panel

Artifact Viewer

AtlasAI Plan Tracker

That gives you the first truly useful operator surface for the suite.

The next thing I’d generate is the Phase 5 scaffold pack with:

Build Profile Editor

Job Details / Log Viewer

Artifact actions

AtlasAI Plan Tracker panel

Blender settings panel

real Tree-sitter process bridge


yes

Excellent — here’s the Phase 5 scaffold pack.

This phase turns Atlas Suite from a functional shell into something that starts feeling like a real developer workstation.

Atlas Suite — Phase 5 Scaffold Pack
This phase adds:

Build Profile Editor

Job Details / Log Viewer

Artifact actions

AtlasAI Plan Tracker panel

Blender settings panel

real Tree-sitter process bridge scaffold

Using your locked naming:

Atlas Suite = tooling shell

AtlasAI = integrated AI system

1. Phase 5 goals
By the end of this phase, Atlas Suite should let you:

create and edit build profiles in UI

inspect job details and full logs

view artifacts and act on them

monitor AtlasAI plans and step state

configure Blender path/settings cleanly

replace the parser stub with a real external bridge contract

This is the point where the suite becomes much more usable for daily iteration.

2. Recommended order inside Phase 5
Build these in this order:

Job Details / Log Viewer

Build Profile Editor

Artifact actions

AtlasAI Plan Tracker panel

Blender settings panel

Tree-sitter real bridge scaffold

That order gives immediate visibility, then control, then deeper integrations.

3. Job Details / Log Viewer
This is one of the biggest quality-of-life upgrades.

IJobDetailsQueryService.cs
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Tooling.Jobs.Interfaces;

public interface IJobDetailsQueryService
{
    Task<ToolJobRecord?> GetJobAsync(string jobId, CancellationToken ct);
    Task<IReadOnlyList<ToolLogRecord>> GetLogsAsync(string jobId, CancellationToken ct);
}
You can implement this by composing IToolJobStore and IToolLogStore.

JobDetailsQueryService.cs
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Models;
using AtlasSuite.Tooling.Logging.Interfaces;

namespace AtlasSuite.Tooling.Jobs.Services;

public sealed class JobDetailsQueryService : IJobDetailsQueryService
{
    private readonly IToolJobStore _jobStore;
    private readonly IToolLogStore _logStore;

    public JobDetailsQueryService(
        IToolJobStore jobStore,
        IToolLogStore logStore)
    {
        _jobStore = jobStore;
        _logStore = logStore;
    }

    public Task<ToolJobRecord?> GetJobAsync(string jobId, CancellationToken ct)
        => _jobStore.GetAsync(jobId, ct);

    public Task<IReadOnlyList<ToolLogRecord>> GetLogsAsync(string jobId, CancellationToken ct)
        => _logStore.GetByJobIdAsync(jobId, ct);
}
JobLogItemViewModel.cs
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class JobLogItemViewModel : ViewModelBase
{
    public DateTimeOffset TimestampUtc { get; }
    public string ToolId { get; }
    public LogSeverity Severity { get; }
    public string Message { get; }
    public string? SourcePath { get; }
    public int? SourceLine { get; }

    public JobLogItemViewModel(ToolLogRecord log)
    {
        TimestampUtc = log.TimestampUtc;
        ToolId = log.ToolId;
        Severity = log.Severity;
        Message = log.Message;
        SourcePath = log.SourcePath;
        SourceLine = log.SourceLine;
    }
}
JobDetailsPanelViewModel.cs
using System.Collections.ObjectModel;
using AtlasSuite.Shell.Commands;
using AtlasSuite.Tooling.Jobs.Interfaces;
using AtlasSuite.Tooling.Jobs.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class JobDetailsPanelViewModel : ViewModelBase
{
    private readonly IJobDetailsQueryService _queryService;

    private string _jobId = string.Empty;
    private string _title = string.Empty;
    private string _toolId = string.Empty;
    private string _status = string.Empty;
    private string _summary = string.Empty;
    private bool _isBusy;

    public ObservableCollection<JobLogItemViewModel> Logs { get; } = new();

    public string JobId
    {
        get => _jobId;
        set => SetProperty(ref _jobId, value);
    }

    public string Title
    {
        get => _title;
        set => SetProperty(ref _title, value);
    }

    public string ToolId
    {
        get => _toolId;
        set => SetProperty(ref _toolId, value);
    }

    public string Status
    {
        get => _status;
        set => SetProperty(ref _status, value);
    }

    public string Summary
    {
        get => _summary;
        set => SetProperty(ref _summary, value);
    }

    public bool IsBusy
    {
        get => _isBusy;
        set => SetProperty(ref _isBusy, value);
    }

    public AsyncRelayCommand LoadJobCommand { get; }

    public JobDetailsPanelViewModel(IJobDetailsQueryService queryService)
    {
        _queryService = queryService;
        LoadJobCommand = new AsyncRelayCommand(LoadAsync, () => !IsBusy && !string.IsNullOrWhiteSpace(JobId));
    }

    public async Task LoadAsync()
    {
        IsBusy = true;
        try
        {
            var job = await _queryService.GetJobAsync(JobId, CancellationToken.None);
            var logs = await _queryService.GetLogsAsync(JobId, CancellationToken.None);

            Title = job?.Title ?? string.Empty;
            ToolId = job?.ToolId ?? string.Empty;
            Status = job?.Status.ToString() ?? "Not Found";
            Summary = job?.Summary ?? "No job found.";

            Logs.Clear();
            foreach (var log in logs.OrderBy(x => x.TimestampUtc))
                Logs.Add(new JobLogItemViewModel(log));
        }
        finally
        {
            IsBusy = false;
            LoadJobCommand.RaiseCanExecuteChanged();
        }
    }
}
Suggested XAML structure
Top summary section:

JobId

Title

ToolId

Status

Summary

Bottom log grid:

Timestamp

Severity

ToolId

Message

SourcePath

SourceLine

4. Build Profile Editor
This is important because stored profiles are only useful once editable.

BuildProfileEditorViewModel.cs
using AtlasSuite.Shell.Commands;
using AtlasSuite.Tooling.Build.Interfaces;
using AtlasSuite.Tooling.Build.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class BuildProfileEditorViewModel : ViewModelBase
{
    private readonly IBuildProfileStore _store;

    private string _profileId = string.Empty;
    private string _displayName = string.Empty;
    private string _sourceDirectory = string.Empty;
    private string _buildDirectory = string.Empty;
    private string _generator = "Ninja";
    private string _configuration = "Debug";
    private string _targetsText = string.Empty;
    private string _statusMessage = "Ready.";
    private bool _isBusy;

    public string ProfileId
    {
        get => _profileId;
        set => SetProperty(ref _profileId, value);
    }

    public string DisplayName
    {
        get => _displayName;
        set => SetProperty(ref _displayName, value);
    }

    public string SourceDirectory
    {
        get => _sourceDirectory;
        set => SetProperty(ref _sourceDirectory, value);
    }

    public string BuildDirectory
    {
        get => _buildDirectory;
        set => SetProperty(ref _buildDirectory, value);
    }

    public string Generator
    {
        get => _generator;
        set => SetProperty(ref _generator, value);
    }

    public string Configuration
    {
        get => _configuration;
        set => SetProperty(ref _configuration, value);
    }

    public string TargetsText
    {
        get => _targetsText;
        set => SetProperty(ref _targetsText, value);
    }

    public string StatusMessage
    {
        get => _statusMessage;
        set => SetProperty(ref _statusMessage, value);
    }

    public bool IsBusy
    {
        get => _isBusy;
        set => SetProperty(ref _isBusy, value);
    }

    public AsyncRelayCommand SaveCommand { get; }
    public AsyncRelayCommand LoadCommand { get; }
    public AsyncRelayCommand NewProfileCommand { get; }

    public BuildProfileEditorViewModel(IBuildProfileStore store)
    {
        _store = store;

        SaveCommand = new AsyncRelayCommand(SaveAsync, () => !IsBusy);
        LoadCommand = new AsyncRelayCommand(LoadAsync, () => !IsBusy && !string.IsNullOrWhiteSpace(ProfileId));
        NewProfileCommand = new AsyncRelayCommand(NewAsync, () => !IsBusy);
    }

    public Task NewAsync()
    {
        ProfileId = Guid.NewGuid().ToString("N");
        DisplayName = string.Empty;
        SourceDirectory = string.Empty;
        BuildDirectory = string.Empty;
        Generator = "Ninja";
        Configuration = "Debug";
        TargetsText = string.Empty;
        StatusMessage = "New profile created.";
        return Task.CompletedTask;
    }

    public async Task LoadAsync()
    {
        IsBusy = true;
        try
        {
            var profile = await _store.GetByIdAsync(ProfileId, CancellationToken.None);
            if (profile is null)
            {
                StatusMessage = "Profile not found.";
                return;
            }

            DisplayName = profile.DisplayName;
            SourceDirectory = profile.SourceDirectory;
            BuildDirectory = profile.BuildDirectory;
            Generator = profile.Generator;
            Configuration = profile.Configuration;
            TargetsText = string.Join(", ", profile.Targets);
            StatusMessage = $"Loaded profile '{profile.DisplayName}'.";
        }
        finally
        {
            IsBusy = false;
            RaiseCommandStates();
        }
    }

    public async Task SaveAsync()
    {
        IsBusy = true;
        try
        {
            var profile = new BuildProfile
            {
                ProfileId = string.IsNullOrWhiteSpace(ProfileId) ? Guid.NewGuid().ToString("N") : ProfileId,
                DisplayName = DisplayName,
                SourceDirectory = SourceDirectory,
                BuildDirectory = BuildDirectory,
                Generator = Generator,
                Configuration = Configuration,
                Targets = TargetsText
                    .Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
                    .ToArray()
            };

            await _store.SaveAsync(profile, CancellationToken.None);
            ProfileId = profile.ProfileId;
            StatusMessage = $"Saved profile '{profile.DisplayName}'.";
        }
        finally
        {
            IsBusy = false;
            RaiseCommandStates();
        }
    }

    private void RaiseCommandStates()
    {
        SaveCommand.RaiseCanExecuteChanged();
        LoadCommand.RaiseCanExecuteChanged();
        NewProfileCommand.RaiseCanExecuteChanged();
    }
}
Suggested XAML fields
ProfileId

DisplayName

SourceDirectory

BuildDirectory

Generator

Configuration

TargetsText

Buttons:

New

Load

Save

5. Artifact actions
Now that artifacts are visible, add basic actions.

IArtifactActionService.cs
using AtlasSuite.Tooling.Artifacts.Models;

namespace AtlasSuite.Tooling.Artifacts.Interfaces;

public interface IArtifactActionService
{
    Task OpenAsync(ToolArtifactRecord artifact, CancellationToken ct);
    Task RevealInExplorerAsync(ToolArtifactRecord artifact, CancellationToken ct);
}
ArtifactActionService.cs
using System.Diagnostics;
using AtlasSuite.Tooling.Artifacts.Interfaces;
using AtlasSuite.Tooling.Artifacts.Models;

namespace AtlasSuite.Tooling.Artifacts.Services;

public sealed class ArtifactActionService : IArtifactActionService
{
    public Task OpenAsync(ToolArtifactRecord artifact, CancellationToken ct)
    {
        if (File.Exists(artifact.FilePath))
        {
            Process.Start(new ProcessStartInfo
            {
                FileName = artifact.FilePath,
                UseShellExecute = true
            });
        }

        return Task.CompletedTask;
    }

    public Task RevealInExplorerAsync(ToolArtifactRecord artifact, CancellationToken ct)
    {
        if (File.Exists(artifact.FilePath))
        {
            Process.Start(new ProcessStartInfo
            {
                FileName = "explorer.exe",
                Arguments = $"/select,\"{artifact.FilePath}\"",
                UseShellExecute = true
            });
        }

        return Task.CompletedTask;
    }
}
Update ArtifactViewerPanelViewModel.cs
Add selected artifact and commands.

private readonly AtlasSuite.Tooling.Artifacts.Interfaces.IArtifactActionService _artifactActionService;
private ArtifactItemViewModel? _selectedArtifact;

public ArtifactItemViewModel? SelectedArtifact
{
    get => _selectedArtifact;
    set => SetProperty(ref _selectedArtifact, value);
}

public AsyncRelayCommand OpenArtifactCommand { get; }
public AsyncRelayCommand RevealArtifactCommand { get; }
Constructor:

public ArtifactViewerPanelViewModel(
    IArtifactStore artifactStore,
    AtlasSuite.Tooling.Artifacts.Interfaces.IArtifactActionService artifactActionService)
{
    _artifactStore = artifactStore;
    _artifactActionService = artifactActionService;

    LoadArtifactsCommand = new AsyncRelayCommand(LoadArtifactsAsync, () => !IsBusy && !string.IsNullOrWhiteSpace(JobId));
    OpenArtifactCommand = new AsyncRelayCommand(OpenArtifactAsync, () => SelectedArtifact is not null);
    RevealArtifactCommand = new AsyncRelayCommand(RevealArtifactAsync, () => SelectedArtifact is not null);
}
Methods:

private async Task OpenArtifactAsync()
{
    if (SelectedArtifact is null)
        return;

    var record = new AtlasSuite.Tooling.Artifacts.Models.ToolArtifactRecord
    {
        ArtifactId = SelectedArtifact.ArtifactId,
        ArtifactType = SelectedArtifact.ArtifactType,
        DisplayName = SelectedArtifact.DisplayName,
        FilePath = SelectedArtifact.FilePath,
        ProducedByToolId = SelectedArtifact.ProducedByToolId,
        SizeBytes = SelectedArtifact.SizeBytes,
        CreatedUtc = SelectedArtifact.CreatedUtc
    };

    await _artifactActionService.OpenAsync(record, CancellationToken.None);
}

private async Task RevealArtifactAsync()
{
    if (SelectedArtifact is null)
        return;

    var record = new AtlasSuite.Tooling.Artifacts.Models.ToolArtifactRecord
    {
        ArtifactId = SelectedArtifact.ArtifactId,
        ArtifactType = SelectedArtifact.ArtifactType,
        DisplayName = SelectedArtifact.DisplayName,
        FilePath = SelectedArtifact.FilePath,
        ProducedByToolId = SelectedArtifact.ProducedByToolId,
        SizeBytes = SelectedArtifact.SizeBytes,
        CreatedUtc = SelectedArtifact.CreatedUtc
    };

    await _artifactActionService.RevealInExplorerAsync(record, CancellationToken.None);
}
Later add:

compare artifacts

attach artifact to report

promote artifact into tracked asset

6. AtlasAI Plan Tracker panel
Now surface AtlasAI state as a first-class panel.

AtlasAITrackedStepItemViewModel.cs
using AtlasSuite.AtlasAI.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class AtlasAITrackedStepItemViewModel : ViewModelBase
{
    public int Order { get; }
    public string Description { get; }
    public string JobId { get; }
    public string Status { get; }
    public string ResultSummary { get; }

    public AtlasAITrackedStepItemViewModel(AtlasAITrackedStepState step)
    {
        Order = step.Order;
        Description = step.Description;
        JobId = step.JobId;
        Status = step.Status;
        ResultSummary = step.ResultSummary;
    }
}
AtlasAIPlanTrackerPanelViewModel.cs
using System.Collections.ObjectModel;
using AtlasSuite.AtlasAI.Interfaces;
using AtlasSuite.Shell.Commands;

namespace AtlasSuite.Shell.ViewModels;

public sealed class AtlasAIPlanTrackerPanelViewModel : ViewModelBase
{
    private readonly IAtlasAIExecutionTracker _tracker;

    private string _planId = string.Empty;
    private string _goal = string.Empty;
    private string _status = string.Empty;
    private string _summary = string.Empty;
    private bool _isBusy;

    public ObservableCollection<AtlasAITrackedStepItemViewModel> Steps { get; } = new();

    public string PlanId
    {
        get => _planId;
        set => SetProperty(ref _planId, value);
    }

    public string Goal
    {
        get => _goal;
        set => SetProperty(ref _goal, value);
    }

    public string Status
    {
        get => _status;
        set => SetProperty(ref _status, value);
    }

    public string Summary
    {
        get => _summary;
        set => SetProperty(ref _summary, value);
    }

    public bool IsBusy
    {
        get => _isBusy;
        set => SetProperty(ref _isBusy, value);
    }

    public AsyncRelayCommand RefreshPlanCommand { get; }

    public AtlasAIPlanTrackerPanelViewModel(IAtlasAIExecutionTracker tracker)
    {
        _tracker = tracker;
        RefreshPlanCommand = new AsyncRelayCommand(RefreshAsync, () => !IsBusy && !string.IsNullOrWhiteSpace(PlanId));
    }

    public async Task RefreshAsync()
    {
        IsBusy = true;
        try
        {
            var state = await _tracker.GetPlanStateAsync(PlanId, CancellationToken.None);

            Goal = state?.Goal ?? string.Empty;
            Status = state?.Status ?? "Not Found";
            Summary = state?.Summary ?? "No plan state found.";

            Steps.Clear();
            if (state is not null)
            {
                foreach (var step in state.Steps.OrderBy(x => x.Order))
                    Steps.Add(new AtlasAITrackedStepItemViewModel(step));
            }
        }
        finally
        {
            IsBusy = false;
            RefreshPlanCommand.RaiseCanExecuteChanged();
        }
    }
}
Suggested XAML structure
Top:

PlanId

Goal

Status

Summary

Grid:

Order

Description

JobId

Status

ResultSummary

7. Blender settings panel
This is the right time to stop assuming Blender is on PATH.

BlenderSettings.cs
namespace AtlasSuite.Tooling.Blender.Models;

public sealed class BlenderSettings
{
    public string ExecutablePath { get; init; } = "blender";
    public string AddonDirectory { get; init; } = string.Empty;
    public string ExportPresetDirectory { get; init; } = string.Empty;
}
IBlenderSettingsStore.cs
using AtlasSuite.Tooling.Blender.Models;

namespace AtlasSuite.Tooling.Blender.Interfaces;

public interface IBlenderSettingsStore
{
    Task SaveAsync(BlenderSettings settings, CancellationToken ct);
    Task<BlenderSettings> LoadAsync(CancellationToken ct);
}
For now, store this in JSON rather than SQLite if you want a lightweight start.

JsonBlenderSettingsStore.cs
using System.Text.Json;
using AtlasSuite.Tooling.Blender.Interfaces;
using AtlasSuite.Tooling.Blender.Models;

namespace AtlasSuite.Tooling.Blender.Services;

public sealed class JsonBlenderSettingsStore : IBlenderSettingsStore
{
    private readonly string _settingsPath;

    public JsonBlenderSettingsStore(string settingsPath)
    {
        _settingsPath = settingsPath;
    }

    public async Task<BlenderSettings> LoadAsync(CancellationToken ct)
    {
        if (!File.Exists(_settingsPath))
            return new BlenderSettings();

        await using var stream = File.OpenRead(_settingsPath);
        var settings = await JsonSerializer.DeserializeAsync<BlenderSettings>(stream, cancellationToken: ct);
        return settings ?? new BlenderSettings();
    }

    public async Task SaveAsync(BlenderSettings settings, CancellationToken ct)
    {
        Directory.CreateDirectory(Path.GetDirectoryName(_settingsPath)!);

        await using var stream = File.Create(_settingsPath);
        await JsonSerializer.SerializeAsync(stream, settings, cancellationToken: ct, options: new JsonSerializerOptions
        {
            WriteIndented = true
        });
    }
}
BlenderSettingsPanelViewModel.cs
using AtlasSuite.Shell.Commands;
using AtlasSuite.Tooling.Blender.Interfaces;
using AtlasSuite.Tooling.Blender.Models;

namespace AtlasSuite.Shell.ViewModels;

public sealed class BlenderSettingsPanelViewModel : ViewModelBase
{
    private readonly IBlenderSettingsStore _store;

    private string _executablePath = "blender";
    private string _addonDirectory = string.Empty;
    private string _exportPresetDirectory = string.Empty;
    private string _statusMessage = "Ready.";
    private bool _isBusy;

    public string ExecutablePath
    {
        get => _executablePath;
        set => SetProperty(ref _executablePath, value);
    }

    public string AddonDirectory
    {
        get => _addonDirectory;
        set => SetProperty(ref _addonDirectory, value);
    }

    public string ExportPresetDirectory
    {
        get => _exportPresetDirectory;
        set => SetProperty(ref _exportPresetDirectory, value);
    }

    public string StatusMessage
    {
        get => _statusMessage;
        set => SetProperty(ref _statusMessage, value);
    }

    public bool IsBusy
    {
        get => _isBusy;
        set => SetProperty(ref _isBusy, value);
    }

    public AsyncRelayCommand LoadCommand { get; }
    public AsyncRelayCommand SaveCommand { get; }

    public BlenderSettingsPanelViewModel(IBlenderSettingsStore store)
    {
        _store = store;
        LoadCommand = new AsyncRelayCommand(LoadAsync, () => !IsBusy);
        SaveCommand = new AsyncRelayCommand(SaveAsync, () => !IsBusy);
    }

    public async Task LoadAsync()
    {
        IsBusy = true;
        try
        {
            var settings = await _store.LoadAsync(CancellationToken.None);
            ExecutablePath = settings.ExecutablePath;
            AddonDirectory = settings.AddonDirectory;
            ExportPresetDirectory = settings.ExportPresetDirectory;
            StatusMessage = "Blender settings loaded.";
        }
        finally
        {
            IsBusy = false;
            RaiseCommandStates();
        }
    }

    public async Task SaveAsync()
    {
        IsBusy = true;
        try
        {
            var settings = new BlenderSettings
            {
                ExecutablePath = ExecutablePath,
                AddonDirectory = AddonDirectory,
                ExportPresetDirectory = ExportPresetDirectory
            };

            await _store.SaveAsync(settings, CancellationToken.None);
            StatusMessage = "Blender settings saved.";
        }
        finally
        {
            IsBusy = false;
            RaiseCommandStates();
        }
    }

    private void RaiseCommandStates()
    {
        LoadCommand.RaiseCanExecuteChanged();
        SaveCommand.RaiseCanExecuteChanged();
    }
}
Important next update
Eventually BlenderAdapter should stop hardcoding "blender" and read from IBlenderSettingsStore.

8. Real Tree-sitter process bridge scaffold
Do not fake parsing forever. Replace the stub with a real bridge contract.

Integration model
Best approach:

Atlas Suite talks to a small local helper process

helper process uses Tree-sitter bindings

helper returns normalized JSON

Atlas Suite converts that into ParseFileResult

This keeps native/parser complexity isolated.

ITreeSitterBridgeProcess.cs
namespace AtlasSuite.Tooling.Parse.Interfaces;

public interface ITreeSitterBridgeProcess
{
    Task<string> ParseFileToJsonAsync(string filePath, CancellationToken ct);
}
TreeSitterBridgeProcess.cs
using AtlasSuite.Tooling.Parse.Interfaces;
using AtlasSuite.Tooling.Process.Interfaces;
using AtlasSuite.Tooling.Process.Models;

namespace AtlasSuite.Tooling.Parse.Services;

public sealed class TreeSitterBridgeProcess : ITreeSitterBridgeProcess
{
    private readonly IProcessRunner _processRunner;
    private readonly string _bridgeExecutablePath;

    public TreeSitterBridgeProcess(
        IProcessRunner processRunner,
        string bridgeExecutablePath)
    {
        _processRunner = processRunner;
        _bridgeExecutablePath = bridgeExecutablePath;
    }

    public async Task<string> ParseFileToJsonAsync(string filePath, CancellationToken ct)
    {
        var result = await _processRunner.RunAsync(new ProcessExecutionRequest
        {
            FileName = _bridgeExecutablePath,
            Arguments = $"\"{filePath}\"",
            WorkingDirectory = Path.GetDirectoryName(filePath) ?? Environment.CurrentDirectory,
            Timeout = TimeSpan.FromSeconds(30)
        }, ct);

        if (result.TimedOut)
            throw new TimeoutException("Tree-sitter bridge timed out.");

        if (result.ExitCode != 0)
            throw new InvalidOperationException(
                string.IsNullOrWhiteSpace(result.StandardError)
                    ? "Tree-sitter bridge failed."
                    : result.StandardError);

        return result.StandardOutput;
    }
}
TreeSitterJsonModels.cs
namespace AtlasSuite.Tooling.Parse.Models;

public sealed class TreeSitterJsonParseResult
{
    public string Language { get; init; } = string.Empty;
    public IReadOnlyList<TreeSitterJsonSymbol> Symbols { get; init; } = Array.Empty<TreeSitterJsonSymbol>();
}

public sealed class TreeSitterJsonSymbol
{
    public string SymbolKind { get; init; } = string.Empty;
    public string Name { get; init; } = string.Empty;
    public int StartLine { get; init; }
    public int EndLine { get; init; }
    public string ParentName { get; init; } = string.Empty;
}
TreeSitterBridge.cs
using System.Text.Json;
using AtlasSuite.Tooling.Parse.Interfaces;
using AtlasSuite.Tooling.Parse.Models;

namespace AtlasSuite.Tooling.Parse.Services;

public sealed class TreeSitterBridge : ISyntaxTreeBridge
{
    private readonly ITreeSitterBridgeProcess _process;

    public TreeSitterBridge(ITreeSitterBridgeProcess process)
    {
        _process = process;
    }

    public async Task<ParseFileResult> ParseFileAsync(string filePath, CancellationToken ct)
    {
        try
        {
            var json = await _process.ParseFileToJsonAsync(filePath, ct);
            var parsed = JsonSerializer.Deserialize<TreeSitterJsonParseResult>(json);

            return new ParseFileResult
            {
                Success = true,
                FilePath = filePath,
                Language = parsed?.Language ?? "unknown",
                Symbols = parsed?.Symbols?.Select(s => new ParsedSymbol
                {
                    SymbolKind = s.SymbolKind,
                    Name = s.Name,
                    StartLine = s.StartLine,
                    EndLine = s.EndLine,
                    ParentName = s.ParentName
                }).ToArray() ?? Array.Empty<ParsedSymbol>()
            };
        }
        catch (Exception ex)
        {
            return new ParseFileResult
            {
                Success = false,
                FilePath = filePath,
                Language = "unknown",
                Errors = new[] { ex.Message }
            };
        }
    }
}
Next adapter update
Then TreeSitterAdapter should:

accept filePath param or first input path

call ISyntaxTreeBridge.ParseFileAsync

return symbol count and structured data

later publish validation if parse fails

9. DI updates for Phase 5
Add these registrations:

services.AddSingleton<IJobDetailsQueryService, JobDetailsQueryService>();
services.AddSingleton<AtlasSuite.Tooling.Artifacts.Interfaces.IArtifactActionService, AtlasSuite.Tooling.Artifacts.Services.ArtifactActionService>();
For Blender settings store:

services.AddSingleton<AtlasSuite.Tooling.Blender.Interfaces.IBlenderSettingsStore>(
    _ => new AtlasSuite.Tooling.Blender.Services.JsonBlenderSettingsStore(
        Path.Combine(AppContext.BaseDirectory, "Settings", "blender.settings.json")));
For Tree-sitter, choose one of these depending on phase:

keep stub for now

or register real bridge process

Stub:

services.AddSingleton<AtlasSuite.Tooling.Parse.Interfaces.ISyntaxTreeBridge, AtlasSuite.Tooling.Parse.Services.TreeSitterBridgeStub>();
Real bridge later:

services.AddSingleton<AtlasSuite.Tooling.Parse.Interfaces.ITreeSitterBridgeProcess>(
    sp => new AtlasSuite.Tooling.Parse.Services.TreeSitterBridgeProcess(
        sp.GetRequiredService<AtlasSuite.Tooling.Process.Interfaces.IProcessRunner>(),
        Path.Combine(AppContext.BaseDirectory, "Tools", "TreeSitterBridge", "TreeSitterBridge.exe")));

services.AddSingleton<AtlasSuite.Tooling.Parse.Interfaces.ISyntaxTreeBridge, AtlasSuite.Tooling.Parse.Services.TreeSitterBridge>();
10. What Phase 5 gives you
Once this phase is done, Atlas Suite can:

inspect jobs in detail

read full persistent logs per job

edit and save build profiles

open and reveal artifacts

track AtlasAI plans in UI

manage Blender path/settings

support a real parser bridge architecture

That is a big step toward a real daily driver.

11. Biggest remaining gaps after Phase 5
After this, the next real holes are:

A. actual Tree-sitter helper implementation
The bridge contract exists, but the helper still needs to be written.

B. AtlasAI chained execution logic
Tracker exists, but AtlasAI still needs decision rules for “step 2 only if step 1 passed.”

C. Build history panel
You’ll want history beyond the general job list.

D. Artifact compare actions
Open/reveal is good, but compare and promote are still missing.

E. Blender adapter real execution
The adapter is scaffolded, but not actually launching/importing/exporting yet.

F. validation issue actions
You can view issues, but not act on them from UI.

G. workspace/repo intelligence layer
Still need richer project map and ownership graph.

12. Best next steps after Phase 5
Do these next:

Tree-sitter helper app

Build history panel

AtlasAI chained step executor

Blender adapter real open/export execution

validation issue actions

artifact compare

workspace index / repo map

tool permissions and policy gates

That would start turning Atlas Suite into a serious integrated environment.

13. Recommended milestone after this
Milestone 2 — Intelligent Development Shell
Target deliverables:

Build Panel

Build Profile Editor

Job Queue

Job Details / Log Viewer

Diagnostics

Artifact Viewer

AtlasAI Plan Tracker

Blender Settings

Tree-sitter bridge contract

real tool health checks

persistent SQLite-backed tooling data

That’s a very respectable milestone.

14. Strongest next move
The best next thing to generate after this is the Phase 6 scaffold pack for:

Tree-sitter helper app contract and JSON format

Build history panel

AtlasAI chained execution engine

Blender real process execution

validation issue actions

artifact compare service

That would move Atlas Suite from “capable shell” to “smart working environment.”



