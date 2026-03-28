# ATLASAI Bridge Contract Spec

## Purpose

This document defines the contract boundary between the **AtlasAI WPF tooling shell** and the **native Atlas / MasterRepo backend**.

The goal is to keep the system modular, testable, and safe to refactor by ensuring the WPF layer never reaches directly into arbitrary engine internals. All cross-boundary interaction should pass through a clearly owned bridge.

---

## 1. Architectural Role

### AtlasAI.WpfHost owns
- workspace shell
- docking layout
- chat panels
- project explorer UI
- logs / notifications UI
- task queues / build panels
- document viewers
- archive browser UX
- settings and workspace profiles
- command dispatch to backend services

### Native Atlas backend owns
- engine runtime
- editor runtime services
- asset database access
- world / scene loading and saving
- simulation state
- build execution
- test execution
- code indexing / project scanning
- AI-accessible repo operations
- viewport rendering and frame lifecycle

### Bridge owns
- transport
- command routing
- request / response schemas
- event streaming
- authentication / session validation for local tooling
- version negotiation
- fault isolation

---

## 2. Design Principles

1. **UI and engine remain decoupled**  
   WPF should talk to stable services, not raw engine objects.

2. **Commands are explicit**  
   No hidden side effects. Each request must have a named operation and typed payload.

3. **Events are push-based**  
   The backend should stream logs, state changes, task progress, and runtime/editor events.

4. **Transport can change without changing semantics**  
   Named pipes, WebSocket, loopback HTTP, or in-process adapters should all preserve the same command schema.

5. **Versioned contract**  
   The bridge must expose protocol versioning so WPF and backend upgrades do not silently break each other.

6. **Editor-safe execution**  
   All backend commands must validate current editor/runtime state before mutating anything.

---

## 3. Recommended Implementation Pattern

### Primary transport
Use a **local service bridge** with:
- **HTTP/REST** for request/response operations
- **WebSocket** for event streams and long-running task updates

### Optional transport alternatives
- named pipes for Windows-only low-latency tooling
- in-process host adapter for future integrated tools testing
- gRPC only if strict typed service generation becomes necessary later

### Recommendation
For earliest implementation:
- REST on `localhost`
- WebSocket event stream on `localhost`
- JSON payloads
- backend hosted by native service layer or companion service executable

This gives the fastest path for WPF integration, diagnostics, and testing.

---

## 4. High-Level Bridge Components

```text
AtlasAI.WpfHost
   -> AtlasAI.Bridge.Client
      -> Transport Layer (REST / WS)
         -> AtlasBridgeService
            -> Service Router
               -> EditorService
               -> AssetService
               -> BuildService
               -> WorldService
               -> RepoService
               -> AISessionService
               -> RuntimeControlService
               -> Log/EventService
```

### WPF-side modules
- `AtlasAI.Bridge.Client`
- `AtlasAI.Bridge.Models`
- `AtlasAI.Bridge.Eventing`
- `AtlasAI.Bridge.Commands`

### Native-side modules
- `AtlasBridgeService`
- `AtlasBridge.Router`
- `AtlasBridge.Schema`
- `AtlasBridge.Session`
- `AtlasBridge.Telemetry`

---

## 5. Contract Layers

### Layer A — Session / handshake
Used when WPF connects to backend.

Responsibilities:
- verify backend is running
- negotiate protocol version
- identify workspace/project
- establish event stream subscription
- expose capability flags

### Layer B — Command API
Used for actions initiated by the user or AI tooling.

Examples:
- load project
- build solution
- run tests
- open asset
- save scene
- generate code patch
- request viewport attach
- execute editor command

### Layer C — Query API
Used for reads and lookups.

Examples:
- get current project status
- list assets
- fetch build history
- fetch runtime status
- search docs / archive / repo
- get entity selection details

### Layer D — Event stream
Used for asynchronous updates.

Examples:
- build started / completed
- log output
- runtime connected
- asset imported
- selection changed
- editor dirty state changed
- AI task progress changed
- crash / warning / watchdog event

---

## 6. Required Capability Areas

The bridge contract should be split into service domains.

### 6.1 Workspace Service
Operations:
- open workspace
- close workspace
- get active workspace
- list recent workspaces
- switch workspace profile
- read workspace settings
- write workspace settings

### 6.2 Project / Repo Service
Operations:
- load project metadata
- scan repo
- get solution structure
- list modules
- open file
- search symbols
- search text
- get git status summary
- get changed files

### 6.3 Build Service
Operations:
- queue build
- cancel build
- query build status
- query build history
- rebuild module
- clean target
- package target

Events:
- build queued
- build started
- build progress
- build completed
- build failed

### 6.4 Test Service
Operations:
- run test suite
- run targeted tests
- cancel tests
- fetch last results

Events:
- test started
- test case completed
- test run completed

### 6.5 Asset Service
Operations:
- list assets
- import asset
- reimport asset
- rename asset
- move asset
- delete asset
- validate asset
- get asset dependencies
- get asset references

Events:
- asset imported
- asset changed
- asset validation failed

### 6.6 World / Scene Service
Operations:
- open world
- save world
- save world as
- load scene chunk
- unload scene chunk
- query world state
- create entity
- duplicate entity
- delete entity
- set transform
- apply prefab

Events:
- world loaded
- scene saved
- entity selected
- entity created
- entity deleted
- world dirty state changed

### 6.7 Runtime Control Service
Operations:
- launch play mode
- stop play mode
- pause simulation
- resume simulation
- step frame
- attach debugger hooks
- query runtime health

Events:
- runtime started
- runtime stopped
- pause changed
- crash detected
- watchdog warning

### 6.8 Viewport Service
Operations:
- request viewport session
- attach native viewport handle
- resize viewport
- set camera mode
- set debug overlays
- capture screenshot
- pick object at screen point

Events:
- viewport ready
- viewport resized acknowledged
- selection under cursor

### 6.9 AI Service
Operations:
- create AI session
- submit prompt
- request code plan
- request patch proposal
- request asset generation task
- request design summarization
- index repo for AI
- cancel AI task

Events:
- AI task queued
- AI task progress
- AI task completed
- AI task failed

### 6.10 Archive / Knowledge Service
Operations:
- index archive item
- search archive
- attach archive doc to AI context
- tag archive item
- fetch archive metadata

Events:
- archive import completed
- archive index updated

### 6.11 Notification / Telemetry Service
Operations:
- get notifications
- acknowledge notification
- clear notification
- get health summary

Events:
- warning raised
- error raised
- notification created

---

## 7. Standard Command Envelope

All bridge commands should use a common envelope.

### Request
```json
{
  "protocolVersion": "1.0",
  "requestId": "uuid",
  "sessionId": "uuid",
  "service": "BuildService",
  "operation": "QueueBuild",
  "timestampUtc": "2026-03-27T12:00:00Z",
  "payload": {
    "target": "AtlasEditor",
    "configuration": "Debug",
    "platform": "x64"
  }
}
```

### Response
```json
{
  "protocolVersion": "1.0",
  "requestId": "uuid",
  "success": true,
  "errorCode": null,
  "message": "Build queued",
  "payload": {
    "buildId": "build-4821"
  }
}
```

### Error response
```json
{
  "protocolVersion": "1.0",
  "requestId": "uuid",
  "success": false,
  "errorCode": "INVALID_STATE",
  "message": "Cannot start build while project is unloading.",
  "payload": {
    "state": "ProjectUnloading"
  }
}
```

---

## 8. Standard Event Envelope

```json
{
  "protocolVersion": "1.0",
  "eventId": "uuid",
  "sessionId": "uuid",
  "service": "BuildService",
  "eventType": "BuildProgress",
  "timestampUtc": "2026-03-27T12:01:02Z",
  "payload": {
    "buildId": "build-4821",
    "stage": "Compile",
    "percent": 42.5,
    "currentItem": "WorldService.cpp"
  }
}
```

---

## 9. Versioning Rules

### Protocol versioning
- major version changes break compatibility
- minor version changes add optional fields or new operations
- patch version changes do not alter schema semantics

### Required handshake fields
Backend must expose:
- protocol version
- backend version
- repo version / build hash
- supported services
- capability flags

### Capability flags examples
- `supportsViewportAttach`
- `supportsLivePatch`
- `supportsAISession`
- `supportsProjectIndexing`
- `supportsMultiWorkspace`

WPF must degrade gracefully when a capability is absent.

---

## 10. State and Session Model

### Session types
- local desktop session
- editor-attached session
- runtime-only session
- headless service session

### Session responsibilities
- bind UI workspace to backend context
- scope events to the active workspace
- enforce project path consistency
- track per-window or per-user tool state if multi-user support arrives later

### Minimum session lifecycle
1. client discovers backend
2. handshake begins
3. session created
4. service capabilities returned
5. event subscriptions registered
6. command/query traffic begins
7. session disposed on disconnect or shutdown

---

## 11. Error Model

All failures should map to a stable error family.

### Core error codes
- `UNKNOWN_ERROR`
- `INVALID_REQUEST`
- `UNAUTHORIZED`
- `UNSUPPORTED_OPERATION`
- `TIMEOUT`
- `RESOURCE_BUSY`
- `INVALID_STATE`
- `NOT_FOUND`
- `VALIDATION_FAILED`
- `BACKEND_UNAVAILABLE`
- `VERSION_MISMATCH`
- `OPERATION_CANCELLED`

### Rules
- do not return raw engine exceptions directly to UI
- always provide user-safe message and developer-safe details separately
- log full backend diagnostics on native side
- propagate correlation ID for tracing

---

## 12. Security Model for Local Tooling

Even though this is local-first, the bridge should still enforce basic trust boundaries.

### Minimum protections
- bind only to loopback by default
- generate short-lived local session token during handshake
- reject commands without valid session
- optionally require workspace identity confirmation
- whitelist writable roots for file operations
- validate tool commands before execution

### Future-ready protections
- user identity / role support for multi-user local network mode
- signed automation commands
- audit log for mutating operations

---

## 13. Threading and Concurrency Rules

### WPF side
- never block UI thread waiting on bridge tasks
- marshal events onto UI thread only at view-model boundary
- keep command client async-first

### Native side
- separate bridge IO threads from engine/game thread
- route mutating editor commands through safe execution queue
- avoid direct engine mutation from socket/pipe threads
- long-running operations should return task IDs and stream progress asynchronously

---

## 14. Logging and Observability

Each request and event should support correlation.

### Required fields
- request ID
- session ID
- service name
- operation / event type
- timestamp
- duration on responses when applicable

### Recommended outputs
- bridge diagnostic log
- backend service log
- build/test log streams
- optional structured JSON log sink

### UI surfaces
- live output panel
- warnings/errors panel
- bridge health panel
- reconnect status indicator

---

## 15. Recommended Initial API Surface (MVP)

To avoid overbuilding, Phase 1 should implement only the bridge needed to make the WPF shell real.

### MVP queries
- get backend status
- get active workspace
- list recent projects
- get repo summary
- get build status
- get runtime state

### MVP commands
- open workspace
- queue build
- cancel build
- launch runtime/editor
- stop runtime/editor
- open file
- search repo
- create AI session
- submit prompt

### MVP events
- backend connected/disconnected
- build progress
- runtime status changed
- log output
- AI task progress
- notification raised

---

## 16. Expansion API Surface (Phase 2+)

After MVP is stable, add:
- viewport attach and selection sync
- asset database operations
- scene/world edit commands
- test orchestration
- code patch proposal/apply workflow
- archive ingestion and retrieval
- live editor/runtime synchronization

---

## 17. Ownership Rules

### AtlasAI.WpfHost must not own
- engine object lifetime
- world simulation state
- asset serialization rules
- build toolchain internals
- gameplay runtime authority

### Native backend must not own
- docking UI layout
- panel state persistence for shell UX
- chat panel rendering
- workspace chrome / desktop UX concerns

### Shared ownership only through schemas
Anything crossing the boundary must be represented as:
- DTO/schema
- command payload
- query response
- event payload

No raw native object references should cross the bridge.

---

## 18. Example Service Contracts

### Example: queue build
**Command**
- service: `BuildService`
- operation: `QueueBuild`

**Payload**
```json
{
  "target": "AtlasEditor",
  "configuration": "Debug",
  "platform": "x64",
  "rebuild": false
}
```

**Response**
```json
{
  "buildId": "build-4821",
  "status": "Queued"
}
```

### Example: create AI session
**Command**
- service: `AIService`
- operation: `CreateSession`

**Payload**
```json
{
  "workspaceId": "masterrepo-main",
  "contextScopes": ["repo", "docs", "archive"]
}
```

**Response**
```json
{
  "aiSessionId": "ai-1199",
  "status": "Ready"
}
```

### Example: world dirty state event
```json
{
  "service": "WorldService",
  "eventType": "DirtyStateChanged",
  "payload": {
    "worldId": "sector_021",
    "isDirty": true,
    "reason": "EntityTransformChanged"
  }
}
```

---

## 19. Refactor Guidance for Existing Repos

### Arbiter -> AtlasAI migration guidance
As Arbiter components move into MasterRepo:
- strip direct file-system side effects from UI code
- move operations into backend services
- keep WPF code focused on view-model and interaction flow
- replace internal shortcut logic with explicit bridge commands

### NovaForge integration guidance
As NovaForge systems merge into MasterRepo:
- expose gameplay/editor functions through service wrappers
- avoid direct WPF knowledge inside runtime/editor modules
- route all tooling interaction through Atlas bridge layers

---

## 20. Implementation Roadmap

### Phase 1 — Schema foundation
- define request envelope
- define response envelope
- define event envelope
- define version handshake
- define core error codes

### Phase 2 — MVP service host
- backend status service
- workspace service
- repo service
- build service
- AI service
- log event stream

### Phase 3 — WPF client integration
- async bridge client
- reconnect logic
- event subscription manager
- status indicator in shell
- output/build/chat integration

### Phase 4 — Editor/runtime expansion
- runtime control service
- viewport attach service
- asset/world services
- selection sync

### Phase 5 — Advanced workflows
- code patch proposal/apply
- archive ingestion/search
- test orchestration
- live patch / hot reload hooks

---

## 21. Final Recommendation

The bridge should be treated as a **product-level contract**, not a temporary glue layer.

If this stays disciplined, it gives you:
- safer refactors
- clean WPF/native separation
- easier diagnostics
- future plugin support
- optional alternate clients later (CLI, web UI, automation agent, remote admin shell)

That makes AtlasAI a real tooling platform around MasterRepo instead of a fragile desktop frontend tightly welded to engine code.

---

## 22. Canonical Naming

Use these names consistently:
- `AtlasAI.WpfHost`
- `AtlasAI.Shell`
- `AtlasAI.Bridge.Client`
- `AtlasBridgeService`
- `AtlasBridge.Schema`
- `AtlasBridge.Router`
- `Atlas.EditorService`
- `Atlas.BuildService`
- `Atlas.WorldService`
- `Atlas.AssetService`
- `Atlas.RuntimeControlService`

This keeps naming aligned with the broader architecture:
- **Atlas** = native engine/editor/backend
- **AtlasAI** = tooling UX + orchestration + AI workflows
- **NovaForge** = game/content layer

