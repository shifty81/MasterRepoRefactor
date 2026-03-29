# MasterRepo Networking / Authority Model

## Purpose
This document locks the authority and networking model for Master Repo so gameplay, voxel edits, module graphs, simulation state, remote tooling, collaboration, and web-connected workflows all grow from one coherent truth model.

---

## 1. Decision summary

### Locked decision
Master Repo will adopt a **server-authoritative core model with local-first development capability**.

That means:
- a single authority source owns canonical world truth for networked sessions
- local single-user sessions can run authority and client in the same process or local host mode
- runtime systems are designed now to respect authority boundaries even before full multiplayer is complete
- collaboration, remote tooling, and future multiplayer all build on the same authority doctrine

This is **not** a pure peer-to-peer model and **not** a late-added multiplayer patch.

It is an authority-first architecture intended to avoid future rewrites.

---

## 2. Why this model was chosen

### Pure peer-to-peer was rejected because
- voxel and structural edits are conflict-prone
- persistent simulation truth becomes harder to protect
- cheat resistance and trust boundaries are poor
- web tooling and remote collaboration need clearer ownership
- rollback and audit become harder

### Client-authoritative gameplay was rejected because
- structural edits, economy state, missions, and AI-assisted tooling need canonical validation
- remote collaboration needs predictable truth
- future dedicated server support would become painful

### Server-authoritative core advantages
- one canonical world state
- explicit validation points
- easier save ownership
- cleaner collaboration model
- safer AI-assisted actions
- easier audit and conflict resolution
- scalable from local single-user to hosted sessions

---

## 3. Authority layers

Master Repo authority is split into layers:

### Layer A — Canonical World Authority
The authoritative owner of persistent world truth.

Owns:
- voxel edits
- structure truth
- module placement/removal
- simulation truth
- player progression truth
- mission outcomes
- save commits
- approved persistent tooling edits that affect world/project state

### Layer B — Session Authority
Handles live session state such as:
- player connections
- active actor state
- ephemeral interaction flows
- permission gating
- collaborative edit session state

### Layer C — Local Presentation Layer
Client-side presentation and prediction where allowed:
- camera
- UI
- local previews
- input buffering
- temporary tool ghosts
- non-authoritative debug views
- optimistic interaction previews when policy allows

### Layer D — External Access Layer
Web clients, remote panels, tablet views, and other external surfaces that consume authority through controlled APIs.

---

## 4. Modes of operation

## 4.1 Local solo mode
The same machine may host:
- authority
- runtime client
- tooling client
- AI session
- optional local web portal

### Locked rule
Even in local solo mode, systems should behave as if authority boundaries exist.

This allows painless evolution toward multiplayer or remote collaboration.

## 4.2 Hosted co-op or dev session
One host/server process owns canonical truth.  
Other clients connect for gameplay, tooling, or observation.

## 4.3 Dedicated authority server mode
Future-ready mode where the server runs simulation and persistence while clients attach for gameplay or tooling.

## 4.4 Remote web/tool mode
External surfaces never become authority by default.  
They submit requests to the authority layer.

---

## 5. Canonical truth ownership

## 5.1 Authoritative domains
The server-authoritative layer owns final truth for:
- world metadata
- structure registries
- voxel chunk state
- module registries and graphs
- economy/faction simulation
- mission state
- player persistent state
- build placements
- AI-approved persistent modifications
- save/load commits

## 5.2 Client-owned local state
Clients may own only local presentation state such as:
- camera orientation
- local UI panel arrangement
- hovered selections
- non-authoritative preview ghosts
- temporary prediction buffers
- local preferences

## 5.3 Shared but authority-validated state
Some state may exist on both sides, but server truth wins:
- player transform
- inventory actions
- build attempts
- module interaction
- mission progression
- damage events
- tool actions

---

## 6. Authority by subsystem

## 6.1 Voxel subsystem
### Locked rule
All persistent voxel edits must be authority-validated.

Clients may preview:
- planned mining cuts
- repair fills
- placement outlines
- build previews

But canonical chunk modification happens only through authority confirmation.

### Why
Voxel edits are structural truth and directly affect:
- collision
- air seals
- power routing anchors
- save data
- other users

## 6.2 Module subsystem
### Locked rule
Module placement, removal, upgrade, state transitions, and graph membership are authoritative actions.

Clients may preview sockets and placements, but authority resolves:
- validity
- costs
- collisions
- graph updates
- persistence

## 6.3 Simulation subsystem
### Locked rule
Economy, factions, missions, seasonal state, and jobs are server-authoritative always.

Clients never become authority over world-scale simulation.

## 6.4 Player subsystem
Player input originates client-side, but persistent or game-critical effects are authority-validated.

### Example
- movement may use prediction
- inventory commits are authoritative
- mission completion is authoritative
- equipment swaps are authoritative
- death/injury consequences are authoritative

## 6.5 Tooling subsystem
Tooling interaction is split:
- local viewport tools may run client-side
- edits affecting canonical world/project state must be authority-validated
- debug-only local visualizations may remain local

## 6.6 Arbiter / AI subsystem
AI can propose actions locally or remotely, but any action affecting:
- persistent project files
- live world state
- authoritative build data
- player or sim state

must pass through authority and permission checks.

---

## 7. Request / command model

### Locked decision
Networked and remote mutation flows should use an explicit **request -> validate -> apply -> replicate** model.

### Standard mutation flow
1. client or tool submits request
2. authority checks permissions
3. authority validates against current truth
4. authority applies mutation
5. authority emits resulting events/state deltas
6. clients update from authoritative result

### Why
This creates:
- auditability
- safer tooling
- conflict control
- easier replay/debug
- better cheat resistance

---

## 8. Replication model

## 8.1 Replication goals
- send canonical state deltas efficiently
- keep clients synchronized without full-state spam
- support multiple interest scopes
- separate persistent truth from local-only noise

## 8.2 Replication categories

### Entity state replication
For:
- player state
- active NPCs
- moving actors
- interactables
- active tool targets
- temporary gameplay objects that matter to clients

### Structure replication
For:
- structure metadata
- transform anchors
- damage summaries
- module lists where needed
- structure-local graph changes
- docking and attachment states

### Voxel replication
For:
- chunk edits
- chunk streaming
- damage/repair deltas
- structural state updates

### Simulation replication
For:
- faction changes relevant to client
- mission updates
- economy summaries if needed
- hazard/event notifications
- seasonal/global state summaries

### Tooling/session replication
For:
- collaborative selections when shared
- workspace annotations
- review comments
- active build session markers
- shared inspection state where enabled

## 8.3 Locked rule
Replication must be domain-aware and interest-scoped.  
Do not broadcast all world state to all clients blindly.

---

## 9. Interest management

## 9.1 Purpose
Clients should receive only relevant state based on:
- location
- ownership
- role
- session mode
- explicit subscriptions
- tool/session context

## 9.2 Examples
### Gameplay client receives
- nearby entities
- nearby voxel chunks
- relevant mission state
- owned ship/station updates
- local hazard info

### Tooling client may receive
- extended graph/debug info for selected structure
- extra metadata for inspected objects
- collaboration state for current workspace

### Web observer may receive
- summaries only
- read-only telemetry
- approved camera outputs
- audit-safe project status

## 9.3 Locked rule
Interest management is mandatory for scalability and privacy/trust boundaries.

---

## 10. Prediction and reconciliation

## 10.1 Where prediction is allowed
Prediction may be used for:
- player movement
- camera and interaction feel
- tool placement ghosts
- temporary UI state
- non-persistent animation cues

## 10.2 Where prediction is limited or disallowed
Prediction should not authoritatively commit:
- voxel edits
- inventory truth
- mission completion
- economy changes
- final module graph updates
- permission-sensitive tooling edits

## 10.3 Locked rule
Prediction improves feel; authority defines truth.

Clients must reconcile cleanly with authority responses.

---

## 11. Conflict resolution

Because Master Repo includes gameplay and tooling collaboration, conflict rules are critical.

## 11.1 Core policy
When two clients attempt conflicting mutations:
- authority serializes and validates requests
- first valid accepted request updates truth
- later conflicting requests are rejected, transformed, or revalidated against new truth

## 11.2 Example conflicts
- two users place a module in the same socket
- one user repairs a hull section while another mines it
- a tool session edits a structure while simulation damage occurs
- AI proposes a world change while a human edits the same target

## 11.3 Locked rule
Conflict resolution happens at authority, never through client-side guesswork alone.

---

## 12. Collaboration model

## 12.1 Collaboration types
Master Repo supports multiple collaborative roles:
- gameplay co-op
- shared build session
- shared tooling inspection
- shared design/review session
- remote observer/reviewer
- AI-assisted collaborative planning

## 12.2 Shared edit sessions
Collaborative editing should support:
- active lock/claim indicators where needed
- soft reservations
- comment/review overlays
- explicit approval flows for risky changes
- role-based visibility of tooling state

## 12.3 Locked rule
Collaboration features are built on top of authority + permission + audit, not parallel ad hoc sync systems.

---

## 13. Persistence relationship

### Locked rule
Only authority commits persistent world/project state.

Clients may:
- request saves
- trigger autosave policies if allowed
- save local preferences
- export local artifacts where permitted

But canonical save packages are written by authority-owned persistence flows.

This prevents:
- divergent world truth
- accidental overwrite conflicts
- confusing AI or tool writes from untrusted surfaces

---

## 14. Tooling and remote project edits

This project uniquely mixes runtime and project-space tooling.

## 14.1 World edits
World-affecting edits are authority-validated game/session mutations.

## 14.2 Project/workspace edits
Project-affecting edits like:
- schema changes
- code patches
- config changes
- data definition updates

must pass through:
- permission model
- approval workflow
- audit logging
- authority or trusted project host validation

## 14.3 Locked rule
Remote or AI-assisted project edits are never applied silently as client-side truth.

---

## 15. Arbiter / AI relationship

## 15.1 AI as client of authority
Arbiter is treated as a privileged but bounded actor, not a magical bypass.

It may:
- inspect state
- propose actions
- request edits
- generate patches
- annotate systems

It may not bypass:
- authority validation
- permissions
- audit logging
- approval gates

## 15.2 Locked rule
AI actions that mutate authoritative state must be attributable and replayable through authority logs.

---

## 16. Session roles

Suggested roles:
- **Observer**
- **Player**
- **Builder**
- **Reviewer**
- **Operator**
- **Admin**
- **LocalOwner**
- **AIWorker** (non-human role with bounded permissions)

### Role examples
- Observer: read-only, maybe telemetry and approved camera views
- Player: gameplay interactions within granted scope
- Builder: build/place/edit structures within allowed session areas
- Reviewer: inspect and annotate
- Operator: run tools and controlled maintenance actions
- Admin: authority management and high-risk actions
- LocalOwner: highest local environment permissions
- AIWorker: constrained automation role

Authority and security documents must align with these roles.

---

## 17. Network topology guidance

## 17.1 Supported logical topologies
- local listen-server style
- local authority + local client in one executable
- dedicated authority server + multiple clients
- authority server + web clients + desktop clients
- authority host + remote AI/tool workers through controlled APIs

## 17.2 Locked rule
Topology may vary, but the authority doctrine does not.

---

## 18. Message categories

Recommended message families:
- connection/session
- auth/role negotiation
- request/command
- validation result
- state delta replication
- chunk stream transfer
- event notification
- tooling collaboration
- AI workflow / patch review
- diagnostics/telemetry

### Locked rule
Mutating actions should be explicit requests, not ambiguous state pushes.

---

## 19. Domain authority map

### World metadata
Authority-owned

### Structures
Authority-owned

### Voxel chunks
Authority-owned

### Module graphs
Authority-owned

### Player persistent state
Authority-owned, player-request driven

### Local camera/UI state
Client-owned

### Shared tooling annotations
Authority-mediated when collaborative
Local-only when private

### AI patch proposals
Stored and managed through authority/project host workflows

---

## 20. Latency and feel guidance

Because the project includes first-person traversal, EVA, building, and tooling, responsiveness matters.

### Recommended approach
- local input responsiveness through prediction where safe
- authoritative correction where truth matters
- clear visual feedback for pending actions
- user-facing indication when an edit is preview vs committed

### Locked rule
UI and tools should communicate pending vs authoritative state clearly.

This is especially important for:
- building
- module placement
- collaborative edits
- AI-proposed changes

---

## 21. Offline and degraded modes

## 21.1 Offline mode
In full local/offline use, the same process may fulfill:
- authority
- client
- tooling
- AI
- persistence

### Locked rule
Offline mode is a deployment convenience, not a different authority philosophy.

## 21.2 Degraded connection mode
Clients should handle:
- temporary disconnection
- delayed command acknowledgment
- stale collaborative annotations
- paused remote tooling views

Persistent authoritative mutations should not commit locally and hope for the best later unless an explicit offline queue model is designed.

---

## 22. Security relationship

Authority doctrine and security doctrine must align.

### Locked rule
Authority says **who owns truth**.  
Security says **who is allowed to ask for changes**.

Both are required.

### Examples
- a Player role may move and interact, but not run admin project migrations
- a Builder role may place structures, but not alter global simulation rules
- an AIWorker may propose or perform bounded tasks, but not bypass approval for destructive changes

---

## 23. Logging and auditability

## 23.1 Required logs
Authority should log:
- connections
- role/permission changes
- mutation requests
- approvals/rejections
- save commits
- AI-attributed actions
- collaboration conflicts
- high-risk admin/tool actions

## 23.2 Locked rule
High-impact authority decisions must be auditable.

This is critical for:
- debugging
- trust
- rollback
- collaborative accountability
- AI safety

---

## 24. Proposed core interfaces

### Core authority/session types
- `AuthorityHost`
- `SessionManager`
- `ConnectionManager`
- `RoleManager`
- `CommandRouter`
- `ReplicationManager`
- `InterestManager`
- `ConflictResolver`

### Domain handlers
- `VoxelAuthorityService`
- `ModuleAuthorityService`
- `SimulationAuthorityService`
- `PlayerAuthorityService`
- `ToolingAuthorityService`
- `AIActionAuthorityService`

### Data structures
- `AuthorityCommand`
- `ValidationResult`
- `ReplicationDelta`
- `InterestScope`
- `SessionRole`
- `AuditRecord`

---

## 25. Proposed logical class diagram

```text
AuthorityHost
 ├─ SessionManager
 ├─ RoleManager
 ├─ CommandRouter
 ├─ ConflictResolver
 ├─ ReplicationManager
 ├─ InterestManager
 ├─ AuditLogger
 ├─ SaveManager
 ├─ VoxelAuthorityService
 ├─ ModuleAuthorityService
 ├─ SimulationAuthorityService
 ├─ PlayerAuthorityService
 ├─ ToolingAuthorityService
 └─ AIActionAuthorityService
```

---

## 26. Migration guidance for legacy repos

When auditing old networking or editor sync code:
- remove hidden client-authoritative mutations
- convert direct shared-state writes into request/validate/apply flows
- isolate tool collaboration from gameplay replication where appropriate
- preserve useful command/message abstractions if they fit authority-first design
- do not let remote UI or AI paths bypass validation

### Example refactors
- old “client places module directly” code -> request placement -> authority validates -> replicate result
- old “shared editor panel state via loose socket sync” -> tooling collaboration messages mediated by authority
- old “AI patch applied locally to live files” -> request/approval/audit/apply pipeline

---

## 27. Hard rules going forward

1. **Canonical world truth is server-authoritative**
2. **Local solo mode still respects authority boundaries**
3. **Mutations use request -> validate -> apply -> replicate**
4. **Voxel and module edits are always authority-validated**
5. **Simulation truth is never client-authoritative**
6. **Clients own presentation, not canonical persistence**
7. **Replication is domain-aware and interest-scoped**
8. **Prediction improves feel but does not define truth**
9. **Conflict resolution happens at authority**
10. **Remote tooling and AI edits cannot bypass authority and permissions**
11. **Only authority commits canonical persistent state**
12. **High-impact actions must be auditable**

---

## 28. Immediate follow-on implementation tasks

### Required code tasks
1. Create `AuthorityHost`
2. Create `SessionRole` model
3. Create `AuthorityCommand` base type
4. Create `CommandRouter`
5. Create `ValidationResult`
6. Create `ReplicationManager`
7. Create `InterestManager`
8. Create `AuditLogger`
9. Create `VoxelAuthorityService`
10. Create `ModuleAuthorityService`
11. Create `ToolingAuthorityService`
12. Create `AIActionAuthorityService`

### Required design tasks
1. Replication target matrix by subsystem
2. Interest scope rules document
3. Conflict resolution catalog
4. Collaborative tooling session rules
5. Client prediction/reconciliation policy
6. Authority log schema

---

## 29. Final locked outcome

Master Repo networking and authority architecture is now:

**a server-authoritative core model with local-first development capability, explicit request/validation/apply flows, domain-aware replication, interest-scoped visibility, auditable collaboration, and bounded AI/tool participation**

In practical terms:
- one authority owns canonical truth
- local sessions still follow that logic
- clients can be responsive without becoming truth owners
- voxel, module, simulation, and persistent edits are validated centrally
- collaboration and AI actions are mediated, attributable, and auditable

This is the networking and authority model all future multiplayer, remote tooling, collaboration, and AI-integrated workflows should follow.
