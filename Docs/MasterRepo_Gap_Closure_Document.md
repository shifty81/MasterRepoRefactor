# Master Repo Gap Closure Document

## Purpose
This document converts the remaining project gaps into a controlled closure plan so Master Repo can move from broad architecture to fully locked implementation.

---

## Status Legend
- **Locked**: decision already made and should be treated as project law
- **Needs Lock**: requires a final decision before deeper implementation
- **Open**: known gap but can wait briefly
- **Blocked**: prevents safe expansion if unresolved

---

## 1. Current locked foundations

### Project identity
- Hybrid voxel + low-poly modular simulation platform
- Integrated runtime + tooling + IDE + AI assistant + optional web layer
- Archive-first migration from legacy repos
- Data-driven architecture wherever practical

### Locked architecture doctrine
- Voxels are the structural truth layer
- Modules are the functional truth layer
- Low-poly assets are the readability/style layer
- Legacy zip repos are mixed-content donors, never blind imports
- Migration occurs by subsystem, not by entire archive

---

## 2. Gap register

## Gap 01 — Entity / Component Architecture
**Status:** Needs Lock  
**Priority:** Tier 1  
**Risk:** Critical  

### Why it matters
This defines how all runtime objects are represented, updated, edited, saved, and exposed to tooling and AI.

### Missing decisions
- ECS vs hybrid object/component model
- ownership and lifetime rules
- runtime/editor identity model
- serialization boundary rules
- relation between voxel structures, module instances, actors, and sim agents

### Recommendation
Use a **hybrid model**:
- lightweight entity/component core for runtime systems
- explicit high-level object wrappers for ships, stations, players, tools, editor selections, and AI-facing objects

### Closure output needed
- Entity model spec
- Component lifecycle rules
- Save identity format
- Editor/runtime object ownership map

### Suggested implementation order
1. Define base entity IDs and world-unique identity policy
2. Define component registration/update order
3. Define gameplay wrapper objects
4. Define serialization ownership rules

---

## Gap 02 — Rendering Pipeline Architecture
**Status:** Needs Lock  
**Priority:** Tier 1  
**Risk:** Critical  

### Missing decisions
- renderer type and frame pipeline
- voxel rendering path
- modular/low-poly rendering path
- material system contract
- lighting path
- debug rendering and tooling overlays
- transparency/post-process strategy

### Recommendation
Adopt a **clean modular renderer split**:
- world geometry pass
- voxel mesh pass
- modular/static mesh pass
- transparent/effects pass
- debug/tool overlay pass
- UI/IDE pass

### Closure output needed
- Rendering architecture document
- Material/shader contract
- Pass order diagram
- Debug draw interface spec

---

## Gap 03 — Physics Architecture
**Status:** Needs Lock  
**Priority:** Tier 2  
**Risk:** High  

### Missing decisions
- rigid body integration model
- voxel collision refresh rules
- ship movement physics
- zero-G EVA model
- mech control/occupancy behavior
- destruction breakup rules
- gravity volume handling

### Recommendation
Separate physics into:
- character motion
- ship/vehicle motion
- voxel collision + destruction updates
- environmental hazards
- tool/build interactions

### Closure output needed
- Physics subsystem spec
- Collision ownership rules
- Structural destruction transition rules

---

## Gap 04 — Save / Load / Persistence Architecture
**Status:** Needs Lock  
**Priority:** Tier 1  
**Risk:** Critical  

### Missing decisions
- chunk persistence format
- per-structure save partitioning
- world streaming save rules
- versioning/migration format
- autosave/incremental save strategy
- deterministic rebuild vs snapshot mix

### Recommendation
Use **layered persistence**:
- config/meta saves
- chunk-level voxel data
- structure-level module/network data
- simulation snapshots
- versioned migration handlers

### Closure output needed
- Save format master spec
- Version migration policy
- Autosave and corruption recovery strategy

---

## Gap 05 — Networking / Multiplayer / Collaboration Authority
**Status:** Needs Lock  
**Priority:** Tier 1  
**Risk:** Critical  

### Missing decisions
- single-player-first vs multiplayer-ready boundaries
- authoritative state owner
- replication rules for voxels/modules/sim
- remote edit conflict handling
- collaboration model for tooling/web access

### Recommendation
Design **server-authoritative core boundaries now**, even if MVP is local-first.

### Closure output needed
- Authority model document
- Replication target table
- Conflict resolution rules
- Collaboration session policy

---

## Gap 06 — Security / Auth / Trust Model
**Status:** Needs Lock  
**Priority:** Tier 1  
**Risk:** Critical  

### Missing decisions
- account/role tiers
- AI execution permissions
- remote file/system access limits
- approval requirements for destructive actions
- audit logging
- plugin/script trust model

### Recommendation
Adopt a **trust-bounded platform model**:
- viewer
- contributor
- builder
- admin
- local-owner
- AI agent permissions constrained by role and task type

### Closure output needed
- Security model
- Permission matrix
- AI action approval matrix
- Audit log requirements

---

## Gap 07 — UI / UX Design System
**Status:** Open  
**Priority:** Tier 2  
**Risk:** High  

### Missing decisions
- universal widget set
- panel docking behavior
- navigation standards
- keyboard/mouse focus rules
- game vs tool vs IDE visual language
- in-game HUD and equipment UI design rules

### Recommendation
Create a **single design system** with variants:
- Runtime HUD
- Tooling Overlay
- IDE Workspace
- AI Panels
- Web Remote Panels

### Closure output needed
- UI style guide
- Widget catalog
- Panel behavior rules
- Input/focus routing guide

---

## Gap 08 — Audio Architecture
**Status:** Open  
**Priority:** Tier 3  
**Risk:** Medium  

### Missing decisions
- event routing
- ambience layers
- interior/exterior transitions
- ship/mech/hazard mixing
- diegetic UI sounds
- tool feedback sounds

### Closure output needed
- Audio event taxonomy
- Mixing category tree
- Zone transition rules

---

## Gap 09 — Animation Pipeline
**Status:** Open  
**Priority:** Tier 3  
**Risk:** Medium  

### Missing decisions
- first-person rig behavior
- mech transfer/pilot occupancy
- procedural overlays
- interaction animation framework
- weapon/tool animation standards

### Closure output needed
- Rig and animation spec
- State machine standards
- Procedural animation integration guide

---

## Gap 10 — Asset / Content Pipeline Standards
**Status:** Needs Lock  
**Priority:** Tier 2  
**Risk:** High  

### Missing decisions
- naming standards
- modular kit requirements
- LOD policy
- collision authoring rules
- Blender/export/import rules
- PCG-ready asset tagging

### Closure output needed
- Asset pipeline handbook
- Naming and folder standards
- Kit authoring rules
- Export validation checklist

---

## Gap 11 — Testing Strategy
**Status:** Needs Lock  
**Priority:** Tier 2  
**Risk:** High  

### Missing decisions
- unit/integration test split
- schema validation tests
- save/load regression tests
- PCG determinism tests
- AI patch safety tests
- tooling/UI smoke tests

### Closure output needed
- Test pyramid
- Minimum test gate for merges
- Automated schema/save/PCG validation pipeline

---

## Gap 12 — Build / Release / Deployment
**Status:** Open  
**Priority:** Tier 2  
**Risk:** High  

### Missing decisions
- CI layout
- editor/runtime target separation
- local vs release config handling
- packaging model
- web/server deployment topology

### Closure output needed
- Build pipeline document
- Release channel strategy
- Environment configuration policy

---

## Gap 13 — Arbiter Memory / Retrieval / Approval Workflow
**Status:** Needs Lock  
**Priority:** Tier 2  
**Risk:** High  

### Missing decisions
- memory scopes
- knowledge graph layout
- indexing cadence
- proposal/diff workflow
- rollback/undo model
- multi-agent conflict handling

### Closure output needed
- Arbiter operational policy
- Indexing and memory rules
- Approval workflow spec
- Patch rollback model

---

## Gap 14 — Documentation Governance
**Status:** Open  
**Priority:** Tier 3  
**Risk:** Medium  

### Missing decisions
- source-of-truth hierarchy
- ADR format
- schema change governance
- deprecation policy
- migration approval flow

### Closure output needed
- Documentation governance guide
- ADR template
- Change control process

---

## Gap 15 — Final Macro Gameplay Loop Lock
**Status:** Needs Lock  
**Priority:** Tier 3  
**Risk:** High  

### Missing decisions
- onboarding flow
- first-session priorities
- progression pacing
- how salvage/mining/building/crafting/faction play interlock
- MVP loop vs long-term universe loop
- seasonal reset cadence impact

### Closure output needed
- Golden path game design document
- MVP gameplay loop map
- Progression pacing ladder

---

## 3. Priority ranking

### Tier 1 — must lock before major subsystem expansion
1. Entity / Component Architecture
2. Rendering Pipeline Architecture
3. Save / Load Architecture
4. Networking / Authority Model
5. Security / Auth / Trust Model

### Tier 2 — should lock immediately after Tier 1
6. Physics Architecture
7. UI / UX Design System
8. Asset / Content Pipeline
9. Testing Strategy
10. Arbiter Workflow Rules
11. Build / Deployment Pipeline

### Tier 3 — can follow once core foundations are fixed
12. Audio Architecture
13. Animation Pipeline
14. Documentation Governance
15. Final Macro Gameplay Loop Lock

---

## 4. Recommended closure sequence

### Phase A — platform core closure
- Entity / Component Architecture
- Rendering Pipeline
- Save / Load
- Networking / Authority
- Security / Permissions

### Phase B — implementation safety closure
- Physics
- UI / UX system
- Asset/content pipeline
- Testing strategy
- Arbiter workflow/approval

### Phase C — product completeness closure
- Build/release pipeline
- Audio
- Animation
- Documentation governance
- Macro gameplay lock

---

## 5. Immediate action list

### Next 5 documents to create
1. **MasterRepo_Entity_Component_Architecture.md**
2. **MasterRepo_Rendering_Pipeline_Architecture.md**
3. **MasterRepo_Save_Load_Architecture.md**
4. **MasterRepo_Networking_Authority_Model.md**
5. **MasterRepo_Security_And_Trust_Model.md**

### Why these first
Together they prevent deep rework in nearly every other subsystem.

---

## 6. Risk summary

### Highest architectural risk
Implementing gameplay, tooling, or AI workflows before entity/save/authority/security are locked.

### Highest production risk
Letting legacy repo migration outrun architecture closure.

### Highest usability risk
Building many tools before input/focus/UI rules are standardized.

### Highest technical debt risk
Adding AI editing and web collaboration before trust boundaries and rollback rules exist.

---

## 7. Final state target

When these gaps are closed, Master Repo becomes:
- structurally coherent
- migration-safe
- AI-safe
- tooling-safe
- ready for long-horizon implementation without architecture drift

That is the point where the project moves from “large, well-scoped concept” to “stable execution platform.”

---

## 8. Final recommendation
Do not expand breadth first from here.

Expand by **closing the Tier 1 gaps first**, then use those decisions to guide all future migration and implementation work.
