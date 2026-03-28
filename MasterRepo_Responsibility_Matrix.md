# MasterRepo Responsibility Matrix

## Core split
- WPF Host = project/workspace/control center
- In-Engine Editor = spatial authoring, simulation editing, debug visualization
- In-Game Runtime = player-facing gameplay and live testing

## Matrix

| System / Feature | WPF Host | In-Engine Editor | In-Game Runtime | Primary Owner | Notes |
|---|---|---|---|---|---|
| Project launcher | Yes | No | No | WPF Host | Entry point |
| Repo/file browser | Yes | Partial | No | WPF Host | Editor gets contextual references only |
| Build/test launcher | Yes | Yes | No | WPF Host | Editor gets quick scenario launch |
| Logs/console | Yes | Yes | Minimal | WPF Host | Runtime only needs compact debug |
| Global settings/config | Yes | Partial | Partial | WPF Host | Runtime only for player/gameplay settings |
| AI chat/brainstorming | Yes | Yes | Limited | WPF Host | Runtime debug only |
| AI diff review / patch approval | Yes | Yes | No | WPF Host | Best outside runtime |
| Repo map / dependency explorer | Yes | Yes | No | WPF Host | Editor gets local contextual graph |
| JSON/data editors | Yes | Partial | No | WPF Host | Editor gets focused inspectors |
| Items/recipes/factions/missions editing | Yes | Partial | No | WPF Host | Runtime consumes only |
| Validation tools | Yes | Yes | Minimal | WPF Host | Runtime shows warnings only |
| Scene/world outliner | Mirror only | Yes | No | Editor | Editor is real owner |
| Property inspector | Optional deep view | Yes | Minimal inspect | Editor | Runtime only lightweight inspect |
| Transform gizmos | No | Yes | Simplified only | Editor | Runtime only if build mode needs it |
| Object placement | No | Yes | Simplified build mode | Editor | Spatial authoring belongs here |
| Prefab/template authoring | Metadata only | Yes | No | Editor | WPF manages catalogs |
| Voxel sculpt/edit/paint | No | Yes | Simplified player tools | Editor | Biggest tooling gap |
| Chunk rebuild / voxel debug | Status only | Yes | Limited debug | Editor | Must be spatial |
| Module placement / socket snapping | No | Yes | Simplified build mode | Editor | Full authoring belongs here |
| Ship/station layout authoring | No | Yes | Limited construction subset | Editor | Core spatial workflow |
| PCG rule editing | Yes | Partial | No | WPF Host | Bulk rule editing fits WPF |
| Seed controls / regenerate | Presets/batch | Yes | Debug only | Editor | Live preview in editor |
| PCG spawn/debug visualization | No | Yes | Limited debug | Editor | Spatial debug tool |
| Economy dashboards | Yes | Yes | Player market summary | WPF Host | Runtime only simplified view |
| Faction standings/influence dashboards | Yes | Yes | Summary only | WPF Host | Runtime gets player-facing summary |
| War/sector/anomaly debug views | Yes | Yes | Minimal | Editor | Spatial + sim context matters |
| Titan/season state tracking | Yes | Yes | Player summary | WPF Host | Runtime gets progression summary |
| Inventory UI | No | Debug/test version | Yes | Runtime | Core player UX |
| Crafting UI | No | Debug/test version | Yes | Runtime | Core player UX |
| Mission log / contracts | Authoring/balancing | Debug/test | Yes | Runtime | WPF for design, runtime for use |
| EVA / tether / airlock UI | No | Debug monitor | Yes | Runtime | Editor for state inspection only |
| Salvage / mining tools | No | Debug invoke | Yes | Runtime | Core player loop |
| Station terminals | Definitions only | Test shell | Yes | Runtime | WPF edits data |
| Fleet management panel | Deep planning | Debug/test | Yes | Runtime | WPF may provide richer ops view |
| Ship progression / fitting | Balancing | Debug/test | Yes | Runtime | Runtime shows operational fitting |
| Meta progression view | Analytics | Debug | Yes | Runtime | WPF useful for long-form analysis |
| Save slot management | Yes | Yes | Simple version | WPF Host | Runtime only practical save/load |
| Save inspection/debug | Yes | Yes | No | WPF Host | Keep diagnostics outside gameplay |
| Migration/version diagnostics | Yes | Yes | No | WPF Host | Not a runtime feature |
| Asset import workflow | Yes | Partial | No | WPF Host | Editor can support reimport/previews |
| Naming/path validation | Yes | Context warnings | No | WPF Host | Batch validation best in host |
| Material/icon preview | Yes | Yes | No | WPF Host | Both useful |
| Session browser / collaboration setup | Yes | Yes | No | WPF Host | Runtime should not own admin |
| Comments/review annotations | Yes | Yes | Minimal | WPF Host | Runtime gets lightweight overlays only |
| Edit locks / reservations | Yes | Yes | No | Editor | Needs in-context visibility |
| Documentation/design panels | Yes | Yes | No | WPF Host | Keep planning near execution |
| Scenario launch buttons | Yes | Yes | No | WPF Host | Key productivity feature |
| Dev overlay / live metrics | Limited mirror | Yes | Yes | Editor | Runtime gets compact gameplay debug |
| World/system orchestrator controls | Yes | Yes | No | WPF Host | Useful for test scenarios |

## Layer rules

### WPF Host should own
- project-wide management
- data/text-heavy editing
- AI planning, diff review, approvals
- build/test orchestration
- dashboards and diagnostics
- asset import and validation
- documentation and workflow control

### In-Engine Editor should own
- spatial authoring
- voxel editing
- module placement and snapping
- scene/world outliner
- property inspection
- gizmos
- PCG live preview and spatial debug
- simulation visualization

### In-Game Runtime should own
- player UX
- inventory, crafting, contracts, missions
- EVA, tether, airlock, salvage, mining
- ship and station interaction
- fleet/player operational UI
- live gameplay debug overlays

## Highest-priority tooling gaps
1. Voxel editor workflow
2. Scene/world outliner
3. Property inspector
4. Gizmo + placement workflow
5. Validation toolkit
6. PCG editor/debug mode
7. Undo/redo
8. Simulation dashboards
9. AI review/diff integration polish
10. Prefab/template authoring

## Recommended editor modes
- World Mode
- Voxel Mode
- Module Mode
- PCG Mode
- Data Mode
- Sim Mode
- AI Mode
