# Master Repo — Missing Systems Addendum

> **Status:** Extension to the authoritative Master Repo canon.
>
> **Purpose:** Defines major systems that are present in the vision, but must be made explicit to ensure stability, scalability, usability, and long-term cohesion. These systems are the difference between a powerful project and one that can actually survive growth.
>
> **Source:** Derived from `RepoDirective1` addendum session. Original chat archived at `Docs/Archive/Chats/`.

---

## Priority Order

### Tier 1 (Highest Impact)

1. Project Law / Validation Layer
2. Unified Metadata / Tagging Backbone
3. Workspace Health Dashboard
4. AI Safety / Permission Layer
5. Formal State Machine Framework

### Tier 2

6. Dependency / Relationship Graph
7. Test Sandbox Suite
8. Command Palette
9. Macro / Automation Workflow System
10. Versioned Migration Framework

### Tier 3

11. Replay / Capture / Debug Snapshots
12. Logic Graph / Visual Scripting
13. Event Feed / Notification System
14. Preset / Template System
15. Development Telemetry Layer

### Tier 4

16. Plugin / Mod Framework
17. Encounter Director
18. Logistics Layer
19. Content Style Governor
20. Design Intent Linking

---

## 1. Project Law / Validation Layer

### Purpose

Master Repo needs an internal enforcement system that keeps architecture, naming, data, UI, and content aligned with repo law. Without this, the project will eventually drift back into inconsistency.

### Responsibilities

- Validate folder/module placement
- Validate dependency direction
- Validate schema files
- Validate naming conventions
- Detect forbidden legacy names
- Validate asset metadata completeness
- Validate UI style compliance
- Validate PCG kit compatibility
- Validate content budgets and limits
- Report orphaned or duplicate systems

### Output Modes

- Editor warnings, build warnings/errors
- Health dashboard entries
- AI audit reports, migration reports

---

## 2. Unified Metadata / Tagging Backbone

### Purpose

Everything in Master Repo should be discoverable and machine-readable by both tools and AI.

### Applies To

Meshes, materials, prefabs, modular parts, gameplay items, machines, ship parts, station parts, rooms, generation kits, missions, factions, UI panels, documents, schemas.

### Metadata Fields

| Field | Description |
|-------|-------------|
| `category` / `subtype` | Classification |
| `style_family` | Visual style group |
| `gameplay_role` | In-game function |
| `faction_compatibility` | Faction affinity |
| `tier` | Quality/progression tier |
| `interior_exterior` | Placement context |
| `procedural_weight` | PCG selection weight |
| `size_class` | Physical size category |
| `snap_type` | Builder snapping rules |
| `power_usage` | Power requirement |
| `oxygen_relevance` | Life support impact |
| `salvage_class` | Salvage classification |
| `damage_state_support` | Supports damage states |
| `authored_generated` | Origin type |
| `documentation_links` | Linked design docs |

### Why It Matters

Backbone for: Arbiter indexing, asset search, PCG filtering, builder snapping/filtering, dependency graphs, content audits, automatic documentation linking.

---

## 3. Dependency / Relationship Graph System

### Purpose

The editor must be able to visualize how systems relate. Master Repo is too large to rely only on folder browsing.

### Graph Views

- Module-to-module dependencies
- Class/system relationships
- Schema-to-system relationships
- Item-to-recipe-to-machine chains
- Prefab-to-generator chains
- Mission-to-faction-to-location links
- UI panel-to-data-source links
- Asset dependency trees
- AI knowledge source maps

### Why It Matters

Helps with: debugging, onboarding, AI reasoning, refactor planning, identifying fragile systems, spotting circular dependencies.

---

## 4. Replay / Capture / Debug Snapshot System

### Purpose

Systemic projects become impossible to debug without repeatable captured states.

### Captures

- Gameplay events, input traces, generation seeds
- Entity snapshots, AI/tool actions
- Runtime warnings/errors
- Economy/faction state slices
- UI/tooling state, simulation timeline

### Uses

- Bug reproduction, PCG debugging, regression testing
- AI-assisted failure analysis
- Comparing system behavior before/after changes

---

## 5. Test Sandbox Suite

### Purpose

Master Repo must have formal test environments, not just one giant dev level.

### Recommended Sandboxes

| Sandbox | Tests |
|---------|-------|
| Ship interior | Basic interior traversal |
| Airlock | Pressurize/depressurize cycle |
| Gravity/zero-G transition | Zone-based gravity switching |
| EVA tether | Tether logic, max length, retract |
| Salvage test zone | Full salvage loop |
| Mech control | Mech occupancy and controls |
| Crafting chain | Multi-machine recipe chain |
| Inventory/loadout | Item management |
| Station logistics | Input/output flows |
| Door/power/life support | System state machines |
| Faction combat | Combat and NPC behavior |
| PCG room/station generator | Generation validation |
| Anomaly/storm simulation | Event system stress |

---

## 6. Logic Graph / Visual Scripting Layer

### Purpose

Some systems benefit from graph-based authoring instead of pure code or JSON.

### Best Use Cases

- Mission logic, dialogue flows, event chains
- Anomaly behavior, scripted tutorial/setup flows
- Generation rule graphs, cinematic triggers
- Tool automations, state transitions for content logic

### Why It Matters

Gives designers, future collaborators, and AI a more visual authoring surface. Reduces the need to hardcode every interactive flow.

---

## 7. Formal State Machine Framework

### Purpose

A huge percentage of planned systems are state-driven. A reusable framework prevents ad hoc switch statements everywhere.

### Good Candidates

- Player movement state, EVA state, mech occupancy state
- Airlock state, door state
- Ship power state, life support state
- Crafting machine state, faction alert state
- Fleet job state, mission phase state
- UI mode state, tooling overlay state

### Why It Matters

Improves readability, debugging, and AI understanding of behavior logic.

---

## 8. Event Feed / Notification System

### Purpose

A unified way to communicate system changes to the user.

### Event Examples

- Oxygen low, hull breach, tether disconnected
- AI patch staged, build failed, indexing complete
- Recipe unlocked, ship reactor offline
- Salvage container opened, station attack detected
- PCG validation failed, collaborator joined

### Surfaces

- In-game HUD, editor sidebar, web dashboard, logs/history panel

---

## 9. Preset / Template System

### Purpose

Anything repeatable should be saveable as a preset.

### Preset Types

- Ships, rooms, station modules, loadouts
- Tool layouts, UI workspaces, AI workflows
- PCG configurations, faction setups, test scenarios
- Build configurations, export/package settings

---

## 10. AI Safety / Permission Layer

### Purpose

Arbiter should be powerful but governed.

### Permission Levels

| Scope | Description |
|-------|-------------|
| Read-only | No write access |
| Write-allowed | Scoped write paths |
| Doc-only auto-edit | Documentation files only |
| Schema generation | New schemas only |
| Patch staging | Must go through review |
| Core module protection | Restricted, escalation required |
| Delete/rename protection | Explicit confirmation required |

---

## 11. Damage Visualization Framework

### Purpose

Damage should be systemic and readable, not hidden in stats.

### Visual Effects

- Sparks, smoke, flickering lights
- Exposed conduits, leaking gas
- Cracked panels, venting air
- Damaged mech limbs, reactor instability visuals
- Salvage-ready component exposure

### Why It Matters

Strongly reinforces the salvage/survival fantasy and enables environmental storytelling.

---

## 12. Unified Interaction Language

### Purpose

One clear interaction philosophy across all interactable objects.

### Applies To

Doors, terminals, containers, machines, repair nodes, ships, mech seats, sockets, salvage points, build anchors, crafting stations, inventory access points.

### Standards

- Prompt style, interaction states
- Hold/tap logic, lock/error feedback
- Range rules, power requirement feedback
- Damaged/unavailable messaging

---

## 13. Logistics / Flow-of-Things Layer

### Purpose

Economy and crafting are stronger if physical/resource flow is formalized.

### Models

- Storage input/output, cargo transfer
- Machine feed chains, mass/volume handling
- Station routing, hauling jobs
- Ship cargo balance, automated logistics

---

## 14. Encounter Director

### Purpose

A systemic pacing layer that decides when and how pressure enters the game.

### Controls

- Pirate ambush frequency, distress signal generation
- Anomaly spikes, salvage site risk escalation
- Hazard intensity, faction retaliation
- Dynamic mission injection, environmental stress timing

---

## 15. Command Palette

### Purpose

A universal action search bar in the editor and tool suite.

### Commands

- Open file, open panel, rebuild project
- Run validation, index workspace
- Create schema, generate module
- Open design doc, launch test map
- Stage AI patch, inspect logs

---

## 16. Macro / Automation Workflow System

### Purpose

Support chained repeatable workflows in the editor.

### Examples

- Create new gameplay feature skeleton
- Create module + schema + docs + test map
- Import donor repo feature and start audit template
- Build and validate selected subsystem
- Generate UI panel shell from schema
- Stage AI patch then run law validation

---

## 17. Workspace Health Dashboard

### Purpose

A central status board for repo health at all times.

### Shows

| Category | Metrics |
|----------|---------|
| Schemas | Invalid, missing, stale |
| Documentation | Missing docs, unlinked design intent |
| Content | Untagged assets, budget overages |
| Dependencies | Broken dependencies, migration debt |
| AI | Drift/rule violations |
| Systems | Duplicate systems, failed tests |
| Build | Build issues, indexing status |

---

## 18. Plugin / Mod Extension Framework

### Purpose

Support optional modules cleanly without bloating the core repo.

### Extension Categories

- Gameplay packs, editor extensions
- AI providers, generation packs
- UI modules, analytics tools
- Content packs, experimental systems

---

## 19. Versioned Migration Framework

### Purpose

Formal way to upgrade old files and systems as data evolves.

### Applies To

Saves, schemas, configs, prefabs, asset metadata, mission definitions, recipe files, builder part definitions.

---

## 20. Development Telemetry Layer

### Purpose

Monitor the project during development (not player telemetry).

### Metrics

- Load times, panel/UI timings, generation durations
- Frame spikes, simulation bottlenecks, expensive systems
- Crash contexts, frequent validation failures
- Common AI patch rejection reasons

---

## 21. Design Intent Linking

### Purpose

Systems, files, assets, and docs should be linked to the design intent that created them.

### Example

A ship oxygen recycler module links to:

- Feature spec, schema, UI panel
- Crafting recipe, balance notes
- Test sandbox, AI-generated scaffolding history

---

## 22. Content Style Governor

### Purpose

Style should be enforceable, not just aspirational.

### Monitors

- Triangle/poly budget targets
- Material family rules, silhouette rules
- Modular kit compatibility, room density rules
- Readability at distance, damage readability
- Faction style variance, visual noise thresholds

---

## 23. Final Addendum Summary

> The project does not need more random feature ideas nearly as much as it needs systems that **protect, organize, explain, validate, and scale** what already exists.
>
> The most important truth this addendum adds is this:
>
> **Master Repo should not just be feature-rich. It should be self-aware, enforceable, inspectable, replayable, and resilient.**
>
> That is what will make it hold together as one cohesive platform.
