# MasterRepo Rendering Pipeline Architecture

## Purpose
This document locks the rendering architecture for Master Repo so voxel structures, low-poly modular visuals, tooling overlays, IDE surfaces, debug visualization, and UI all render through one coherent pipeline.

---

## 1. Decision summary

### Locked decision
Master Repo will use a **modular multi-pass renderer** with clearly separated render domains.

The renderer will be organized into distinct passes for:
- world geometry
- voxel-generated geometry
- modular/low-poly geometry
- transparencies and effects
- debug and tooling overlays
- UI / IDE surfaces

This is a **hybrid simulation/editor renderer**, not a game-only renderer.

### Core goals
- support voxel + low-poly hybrid visuals
- support runtime and tooling in the same executable
- support debug-heavy development workflows
- keep pass responsibilities explicit
- allow future expansion into web/remote view integration and multi-view editors

---

## 2. Why this model was chosen

### Single monolithic scene pass was rejected because
- debug and tool layers need stricter separation
- voxel meshes and modular meshes have different update patterns
- UI/IDE rendering has different needs than 3D world rendering
- post-process and transparency ordering become harder to reason about
- long-term maintainability suffers

### Fully separate renderers were rejected because
- tooling and game need to coexist live
- duplicate material/light/camera logic would be wasteful
- shared runtime/editor scenes need consistent visibility rules

### Modular multi-pass advantages
- clear ownership per pass
- easier profiling
- easier debug control
- clean integration of editor overlays
- better future support for multiple windows/viewports
- makes voxel-specific meshing and update costs easier to isolate

---

## 3. High-level architecture

The renderer is split into:

### Layer A — Render Frontend
Responsible for:
- scene extraction
- visibility gathering
- camera/view setup
- render list generation
- pass scheduling
- debug request collection
- UI surface registration

### Layer B — Render Backend
Responsible for:
- GPU resource management
- pass execution
- buffer management
- shader/material binding
- draw/dispatch submission
- render target lifecycle

### Layer C — Render Domains
Logical content domains:
- voxel domain
- modular/static mesh domain
- dynamic actor domain
- effects domain
- tooling/debug domain
- UI/IDE domain

### Layer D — Presentation
Responsible for:
- final compositing
- output to main viewport
- output to editor/tool panels
- screenshot and preview surfaces
- optional offscreen rendering for remote/web streaming later

---

## 4. Locked pass order

The standard frame should follow this order:

1. **Frame setup**
2. **Visibility and extraction**
3. **Shadow / lighting prep**
4. **Opaque world pass**
5. **Voxel geometry pass**
6. **Modular / low-poly geometry pass**
7. **Dynamic actor pass**
8. **Transparent / effects pass**
9. **Debug visualization pass**
10. **Tooling overlay 3D pass**
11. **UI / IDE pass**
12. **Composite / presentation**
13. **Frame diagnostics + capture hooks**

### Important clarification
“Opaque world pass” may include terrain, skybox background geometry, or non-voxel/non-module geometry depending on world type.

Voxel and modular passes are kept explicitly visible in the architecture even if backend optimization later merges pieces for efficiency.

---

## 5. Render domains

## 5.1 Voxel domain
Responsible for rendering geometry generated from voxel data.

### Characteristics
- chunk-based
- regenerated as voxel edits occur
- can carry damage and material variation
- often higher geometry churn than static low-poly modules
- tied closely to structure state and PCG updates

### Locked rule
Voxel cells are never rendered individually.  
Voxel rendering happens through generated chunk or structure meshes.

### Required inputs
- chunk mesh handles
- voxel material data
- structure transform anchors
- damage / heat / integrity visualization flags
- culling bounds

---

## 5.2 Modular / low-poly domain
Responsible for:
- modules
- structural shells
- interactable devices
- faction style dressing
- authored kit pieces
- room details
- readable visual elements

### Characteristics
- authored mesh instances
- lower update frequency than voxel meshes
- may change with upgrades, damage states, or faction style
- often the readability layer for the player

### Locked rule
Low-poly authored pieces are the **visual readability layer**, not the structural truth layer.

---

## 5.3 Dynamic actor domain
Responsible for:
- player body / first-person proxies where needed
- NPCs
- mechs
- tools
- moving entities
- dynamic doors/turrets/animated objects
- particles or geometry-driven runtime entities not owned by voxel/modular static domains

### Characteristics
- animation or frequent transform changes
- higher per-frame update needs
- more likely to use skinning or dynamic material parameters

---

## 5.4 Effects domain
Responsible for:
- particles
- sparks
- breaches
- dust
- atmosphere leaks
- shield or scanner effects
- beam tools
- decals if used
- screen-space or mesh-based effect visuals

### Locked rule
Effects must remain logically separate from debug visuals and tooling visuals even if they share backend resources.

---

## 5.5 Tooling / debug domain
Responsible for:
- gizmos
- selection bounds
- socket markers
- graph overlays
- chunk boundaries
- nav/path/power/air debug lines
- interaction markers
- runtime diagnostics
- profiling surfaces in-world where applicable

### Locked rule
Debug and tooling visuals are first-class render content, not hacks layered on ad hoc late in development.

This is a critical project decision.

---

## 5.6 UI / IDE domain
Responsible for:
- runtime HUD
- inventory/equipment windows
- crafting panels
- docking editor panels
- AI chat surfaces
- design panels
- PDF/web/code/data displays
- modal dialogs
- notifications
- editor workspace surfaces

### Locked rule
UI and IDE are part of the renderer’s official architecture and must support multi-panel composition, focus routing, and layered rendering.

---

## 6. Camera and view model

## 6.1 View abstraction
Every visible rendering target uses a **ViewContext** abstraction.

A view context defines:
- camera transform
- projection type
- near/far values
- visibility filters
- lighting context
- render feature toggles
- target surface
- debug/tool enable flags

### Example view types
- Main gameplay camera
- Tool free camera
- Ship interior preview camera
- Orthographic build camera
- Material preview panel camera
- Module inspector preview camera
- Offscreen capture camera

## 6.2 Multi-view support
The renderer must support more than one active view per frame eventually.

Even if MVP uses one main viewport, architecture must allow:
- docking panel previews
- secondary camera panels
- split editors
- minimap/radar capture passes
- screenshot/export surfaces

---

## 7. Visibility and extraction

## 7.1 Extraction phase
Game/editor/runtime state is converted into renderable state during extraction.

### Extraction gathers
- visible voxel chunks
- visible modular mesh instances
- visible dynamic actors
- light sources
- effect emitters
- debug requests
- UI surface draw trees

## 7.2 Locked rule
Render code should consume extracted render data, not directly traverse arbitrary gameplay state during draw submission.

This keeps rendering deterministic and easier to profile.

## 7.3 Visibility categories
Visibility should support filtering by:
- runtime layer
- editor/tool layer
- selection/debug modes
- interior/exterior context
- ownership tags
- camera-specific masks

---

## 8. Material system contract

## 8.1 Material goals
The material system must support:
- low-poly stylized materials
- voxel surface materials
- damage states
- emissives for machinery/power states
- transparent materials
- debug coloring
- UI surface materials

## 8.2 Locked material contract
A material must resolve through:
- shader family
- material parameters
- texture set if applicable
- render state flags
- domain compatibility

### Domain compatibility examples
- voxel opaque
- modular opaque
- dynamic/skinned
- transparent
- UI
- debug

## 8.3 Style doctrine
The project is low-poly and readable.  
Materials should favor:
- clean shapes
- strong readability
- restrained complexity
- meaningful state communication over photorealism

---

## 9. Lighting architecture

## 9.1 Lighting goals
Support:
- interior ship/station lighting
- exterior space/sector lighting
- emissive machinery feedback
- hazard/event lighting
- tool/debug visibility
- performance-conscious development workflows

## 9.2 Required light categories
- directional/sector light where applicable
- point lights
- spot lights
- emissive contributions
- ambient probes or simplified ambient solution
- emergency/hazard lighting

## 9.3 Locked rule
Lighting must remain compatible with:
- interior/exterior transitions
- airlock and breach states
- damaged power systems
- faction style presentation
- tooling overlays staying legible

### Tooling legibility rule
Tooling overlays must not become unreadable due to world lighting.  
They may use protected render styles or explicit overlay shading.

---

## 10. Transparency and effects ordering

## 10.1 Transparent content examples
- glass
- shield visuals
- atmosphere overlays
- oxygen leak effects
- holograms
- UI-in-world surfaces
- warning screens
- force fields if used

## 10.2 Locked rule
Transparency is a dedicated pass domain and must follow stable ordering rules.

### Ordering policy
1. opaque first
2. transparents next
3. debug/tooling after transparents when overlay readability matters
4. UI after world-space passes unless using world-space surfaces intentionally

---

## 11. Debug and tooling rendering

## 11.1 Core debug features to support
- voxel chunk bounds
- structural integrity heatmap
- power graph lines
- air pressure region visualization
- socket/node markers
- pathing visualization
- selection highlight
- transform gizmos
- collision overlays
- mission/debug markers

## 11.2 Locked rule
Every major simulation subsystem should be able to submit structured debug visualization through a shared debug draw interface.

### Required interface concept
A central `DebugDrawService` or equivalent should accept requests like:
- line
- box
- sphere
- arrow
- text label
- icon marker
- mesh marker
- heatmap region

## 11.3 Tool/render separation
Not all debug visuals are tool visuals and not all tool visuals are debug visuals.

Examples:
- transform gizmo = tool visual
- air pressure overlay = debug visual
- selected module halo = may be both

Keep categories explicit.

---

## 12. UI / IDE rendering architecture

## 12.1 UI goals
- runtime HUD
- in-game inventory/equipment/crafting
- tool mode panels
- IDE/editor workspace windows
- AI chat and diff panels
- embedded web/PDF/code/data panels

## 12.2 Locked rule
UI rendering must support a retained layout tree or equivalent structured panel system.

This project is too complex for ad hoc screen-space widgets only.

## 12.3 UI layers
At minimum:
- gameplay HUD layer
- modal/game menu layer
- tooling workspace layer
- IDE document/content layer
- notification layer
- cursor/focus visualization layer

## 12.4 Embedded content surfaces
The architecture must support panels that render:
- text/code
- documents
- data tables
- web views
- PDF/image previews

Even if implementation comes later, render integration should reserve for it now.

---

## 13. Voxel + modular visual relationship

This is a core project-specific rendering rule.

### Locked doctrine
- voxels define mass, damage, and structure
- low-poly authored meshes define readability and functional styling
- rendering must allow both to coexist without ambiguity

### Practical consequences
- hull mass may render from voxel-generated mesh
- reactor housing may render from module shell mesh
- damage may expose voxel damage beneath low-poly shell
- upgrades may swap authored module shells while leaving voxel support mass intact
- PCG may place low-poly dressing over voxel-generated structure anchors

---

## 14. Update frequency model

Different render domains update at different rates.

### Voxel domain
- event-driven remesh when edits occur
- occasional streaming updates

### Modular domain
- mostly stable instance lists
- refresh on placement/removal/upgrade/damage state change

### Dynamic actor domain
- frequent per-frame transform/animation updates

### UI domain
- retained layout updates on interaction/data changes
- frame updates for animation/cursor/text input as needed

### Locked rule
Do not force all render domains through the same update cadence if their data lifecycles differ.

---

## 15. GPU resource model

The renderer backend should manage:
- mesh buffers
- voxel chunk buffers
- material/shader resources
- uniform/parameter buffers
- texture atlases or material textures
- render targets
- depth buffers
- UI surfaces
- debug draw buffers

### Locked rule
GPU resources must be owned by render backend systems, not by arbitrary gameplay objects.

Gameplay and tools provide data/requests; render backend owns GPU lifetime.

---

## 16. Diagnostics and profiling

## 16.1 Required diagnostics
- draw counts
- voxel chunk render counts
- pass timings
- material/shader counts
- transparent counts
- UI panel counts
- debug draw counts
- overdraw / fill cost indicators where possible
- remesh/update event counts

## 16.2 Locked rule
Rendering diagnostics are not optional.  
The renderer must expose profiling information early because tooling/debug-heavy workflows depend on it.

---

## 17. Screenshot, preview, and export support

Because the project includes tooling and IDE features, the renderer must support:
- screenshot capture
- thumbnail generation
- module preview rendering
- asset icon rendering
- scene preview surfaces
- documentation/design image export later if needed

### Locked rule
Offscreen render targets are official supported outputs, not special hacks.

---

## 18. Proposed base interfaces

### Frontend types
- `Renderer`
- `RenderFrameContext`
- `ViewContext`
- `RenderScene`
- `RenderExtractionContext`

### Render list types
- `VoxelRenderItem`
- `MeshRenderItem`
- `DynamicRenderItem`
- `EffectRenderItem`
- `DebugRenderItem`
- `UIRenderItem`

### Backend/resource types
- `MeshBufferHandle`
- `MaterialHandle`
- `TextureHandle`
- `RenderTargetHandle`
- `ShaderHandle`

### Tool/debug services
- `DebugDrawService`
- `SelectionHighlightService`
- `GizmoRenderService`

---

## 19. Proposed pass structure

```text
Renderer
 ├─ FrameSetupPass
 ├─ VisibilityPass
 ├─ ShadowPrepPass
 ├─ OpaqueWorldPass
 ├─ VoxelGeometryPass
 ├─ ModularGeometryPass
 ├─ DynamicActorPass
 ├─ TransparentEffectsPass
 ├─ DebugPass
 ├─ ToolOverlay3DPass
 ├─ UIPass
 └─ CompositePresentPass
```

This is the conceptual structure.  
Backend implementation may collapse or optimize internally, but architecture and profiling should still expose these logical phases.

---

## 20. Migration guidance for legacy repos

When auditing legacy rendering code:
- separate runtime scene rendering from tool overlays
- move voxel rendering into explicit chunk/structure mesh paths
- separate UI from debug draws
- isolate material bindings from gameplay logic
- remove hidden dependencies where gameplay objects directly own GPU state
- preserve useful render helpers only if they fit pass-based ownership

### Example refactors
- Old `ShipRenderer` gameplay class -> extraction logic + render items + structure visual wrapper
- Old debug immediate draw calls everywhere -> central DebugDrawService
- Old UI overlay mixed into gameplay render -> UI domain pass with clear surface routing

---

## 21. Hard rules going forward

1. **Rendering is pass-based and domain-aware**
2. **Voxel cells do not render individually**
3. **Low-poly modules are readability visuals, not structural truth**
4. **Tooling/debug overlays are first-class render citizens**
5. **UI/IDE rendering is part of core architecture**
6. **Render submission uses extracted render state, not arbitrary gameplay traversal**
7. **GPU resource lifetime belongs to render backend**
8. **Multiple views and offscreen targets must remain architecturally supported**
9. **Lighting must preserve tool readability**
10. **Legacy rendering code must conform to this pass/domain model**

---

## 22. Immediate follow-on implementation tasks

### Required code tasks
1. Create `Renderer` frontend shell
2. Create `ViewContext`
3. Create render extraction stage
4. Create `VoxelRenderItem` and `MeshRenderItem`
5. Create logical pass scheduler
6. Create `DebugDrawService`
7. Create UI surface registration system
8. Create offscreen render target abstraction
9. Add render diagnostics output

### Required design tasks
1. Material/shader contract document
2. Lighting model document
3. Debug visualization standards document
4. UI surface/render integration document
5. Performance budget assumptions for major domains

---

## 23. Final locked outcome

Master Repo rendering architecture is now:

**a modular multi-pass renderer with explicit voxel, modular, dynamic, effects, tooling/debug, and UI/IDE domains**

In practical terms:
- voxel structures render through generated meshes
- low-poly modules render through authored mesh systems
- tooling and debug overlays are built into the renderer from the start
- UI and IDE panels are official render surfaces
- extraction separates gameplay/editor state from draw submission
- the same renderer supports simulation, editing, AI-assisted workflows, and future preview/export tasks

This is the rendering architecture all future visual, tool, and interface work should follow.
