# MASTERREPO_PHASE_EXECUTION_ROADMAP

## Purpose
This roadmap defines the **exact phased execution plan** to migrate your current repos into the unified MasterRepo architecture.

Each phase includes:
- goal
- key actions
- deliverables
- effort estimate
- risk level
- success criteria

---

# PHASE 1 — FOUNDATION (LOW RISK)

## Goal
Establish the monorepo structure without breaking anything.

## Key Actions
- Create top-level folders:
  - Atlas/
  - NovaForge/
  - Arbiter/
  - Shared/
  - Docs/
  - Tools/
  - Scripts/
  - Tests/
- Add root CMake + Options.cmake
- Drop in first-pass build skeleton

## Deliverables
- Repo builds (even if mostly empty)
- Folder structure matches blueprint

## Effort
Low (1–2 days)

## Risk
Very low

## Success Criteria
- CMake configure succeeds
- No existing code broken yet

---

# PHASE 2 — SHARED + BRIDGE BASE (LOW RISK)

## Goal
Introduce the contract layer safely.

## Key Actions
- Create Shared/ArbiterBridgeContract
- Add ArbiterBridgeTypes.h
- Add Shared/ProjectManifests/novaforge.project.json

## Deliverables
- Shared target exists
- Manifest loads (stub)

## Effort
Low (1 day)

## Risk
Very low

## Success Criteria
- Shared builds clean
- No runtime impact

---

# PHASE 3 — ATLAS EXTRACTION (MEDIUM RISK)

## Goal
Move reusable engine systems into Atlas.

## Key Actions
- Move Core → Atlas/Core
- Move Engine → Atlas/Engine
- Move UI → Atlas/UI
- Update includes + CMake per module

## Deliverables
- AtlasCore
- AtlasEngine
- AtlasUI targets compiling

## Effort
Medium (3–5 days)

## Risk
Medium (include breakage)

## Success Criteria
- Atlas builds independently
- No NovaForge references inside Atlas

---

# PHASE 4 — NOVAFORGE STRUCTURE (LOW–MEDIUM RISK)

## Goal
Organize NovaForge as a proper project layer.

## Key Actions
- Create:
  - Gameplay/
  - World/
  - Tools/
  - App/
  - Data/
  - Content/
- Move:
  - Data → NovaForge/Data
  - Assets → NovaForge/Content

## Deliverables
- Clean NovaForge folder structure

## Effort
Medium (2–4 days)

## Risk
Low–Medium

## Success Criteria
- Game still loads data from new paths

---

# PHASE 5 — SPLIT MIXED SYSTEMS (HIGH VALUE, HIGH RISK)

## Goal
Untangle mixed ownership systems.

## Key Actions
- Split Editor:
  - generic → Atlas
  - project → NovaForge/Tools
- Split Runtime:
  - generic → Atlas
  - project → NovaForge/App
- Split AI/IDE/Agents → Arbiter

## Deliverables
- Clean ownership boundaries

## Effort
High (5–10 days)

## Risk
High

## Success Criteria
- No circular dependencies
- Ownership zones are clear

---

# PHASE 6 — ARBITER EXTRACTION (MEDIUM RISK)

## Goal
Move all tooling/AI into Arbiter.

## Key Actions
- Create:
  - HostApp/
  - AIEngine/
  - Archive/
  - Automation/
  - ProjectAdapters/
- Move AI, IDE, Agents

## Deliverables
- Arbiter builds independently

## Effort
Medium (3–6 days)

## Risk
Medium

## Success Criteria
- Arbiter runs standalone
- No runtime dependency from game

---

# PHASE 7 — BRIDGE INTEGRATION (MEDIUM RISK)

## Goal
Connect Arbiter ↔ NovaForge cleanly.

## Key Actions
- Implement NovaForgeIntegrationArbiter
- Add bridge service (start/stop)
- Add Arbiter project adapter

## Deliverables
- Working (stubbed) communication layer

## Effort
Medium (2–4 days)

## Risk
Medium

## Success Criteria
- Arbiter connects to NovaForge (even minimally)

---

# PHASE 8 — BUILD + DEPENDENCY CLEANUP (HIGH VALUE)

## Goal
Enforce architecture rules.

## Key Actions
- Audit all includes
- Remove forbidden dependencies
- Gate Arbiter integration behind flags
- Ensure shipping build isolation

## Deliverables
- Clean dependency graph

## Effort
Medium (3–5 days)

## Risk
Medium

## Success Criteria
- No violations of dependency charter
- Shipping builds contain zero Arbiter code

---

# PHASE 9 — VALIDATION + HARDENING (LOW RISK)

## Goal
Stabilize and verify system.

## Key Actions
- Add integration tests
- Add build verification tests
- Final architecture audit

## Deliverables
- Stable, validated monorepo

## Effort
Low–Medium (2–4 days)

## Risk
Low

## Success Criteria
- CI passes
- Repo structure matches blueprint
- System is maintainable

---

# TOTAL ESTIMATE

| Phase | Effort |
|------|--------|
| 1–2 | 2–3 days |
| 3–4 | 5–9 days |
| 5 | 5–10 days |
| 6–7 | 5–10 days |
| 8–9 | 5–9 days |

**Total:** ~22–41 days (depending on refactor depth)

---

# RECOMMENDED EXECUTION ORDER (REALISTIC)

Week 1:
- Phase 1
- Phase 2
- Start Phase 3

Week 2:
- Finish Phase 3
- Phase 4

Week 3:
- Phase 5 (major refactor)

Week 4:
- Phase 6
- Phase 7

Week 5:
- Phase 8
- Phase 9

---

# FINAL NOTE

Do NOT attempt to do everything at once.

The correct strategy is:
- move → build → verify → repeat

Small, safe iterations will get you to a clean architecture much faster than a single massive refactor.
