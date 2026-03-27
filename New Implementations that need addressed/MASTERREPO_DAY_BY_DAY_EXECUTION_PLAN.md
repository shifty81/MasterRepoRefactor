# MASTERREPO_DAY_BY_DAY_EXECUTION_PLAN.md

## Purpose

This is a **practical day-by-day execution plan** for consolidating:

- MasterRepo (destination)
- Arbiter → AtlasAI
- ArbiterAI → AtlasAI.Core
- NovaForge → gameplay/content systems

Built on top of all prior planning docs.

This assumes focused work blocks (can map to real days or sessions).

---

# WEEK 1 — FOUNDATION + STRUCTURE

## Day 1 — Repo Setup + Backup
- Backup all zips
- Extract into temp workspace
- Inventory modules (keep/refactor/archive)
- Create `/Docs/Migration` and store all plans

## Day 2 — Create MasterRepo Skeleton
- Create all top-level folders
- Add README per folder
- Commit empty structure

## Day 3 — Docs Migration
- Move all design + planning docs
- Organize into `/Docs/*`
- Create DOC_INDEX.md

## Day 4 — Naming Alignment (AtlasAI)
- Update docs naming
- Define naming conventions
- Create rename map

## Day 5 — Shared Layer Setup
- Create `/Shared/*`
- Define base contracts (Command/Event/Error)
- Add version + handshake model

---

# WEEK 2 — SERVICES + ENGINE ALIGNMENT

## Day 6 — Service Scaffolding
- Create all `/Services/*`
- Add startup + logging
- Health check endpoints

## Day 7 — Build + Telemetry Services
- Implement basic build execution
- Implement log streaming

## Day 8 — Editor + Simulation Service (MVP)
- Basic command endpoints
- Stub responses if needed

## Day 9 — Engine Reorganization (Part 1)
- Move core systems into `/Engine/AtlasCore`, Runtime, Platform

## Day 10 — Engine Reorganization (Part 2)
- Renderer, Simulation, World, Assets
- Fix includes incrementally

---

# WEEK 3 — WPF TOOLING (AtlasAI)

## Day 11 — WPF Host Setup
- Create `AtlasAI.WpfHost`
- Launch empty shell window

## Day 12 — Shell + Docking
- Implement layout system
- Basic panel system

## Day 13 — Chat Panel
- Create chat UI
- Hook to dummy AI endpoint

## Day 14 — Logs + Build Panels
- Connect to telemetry + build service
- Display live data

## Day 15 — Workspace System
- Session persistence
- Panel restore

---

# WEEK 4 — ATLASAI CORE + BRIDGE

## Day 16 — AI Core Migration (Part 1)
- Move core orchestration
- Setup AtlasAI.Core

## Day 17 — AI Modules (Agents/Memory/Indexing)
- Move and separate logic from UI

## Day 18 — AI Service Host
- Connect AtlasAI to service layer

## Day 19 — Bridge Implementation (Part 1)
- Create bridge client
- Connect to services

## Day 20 — Bridge Implementation (Part 2)
- Add commands:
  - build
  - logs
  - editor
  - simulation

---

# WEEK 5 — NOVAFORGE GAME SYSTEMS

## Day 21 — NovaForge Core
- Create `/Game/NovaForge`
- Move core systems

## Day 22 — Ships + Stations
- Move modular systems
- Fix dependencies

## Day 23 — Interiors + Characters
- FPS/mech systems

## Day 24 — Factions + Economy
- standings, markets

## Day 25 — Missions + Exploration
- procedural tasks, scanning

## Day 26 — Mining + Construction
- resource + building systems

## Day 27 — Combat Systems
- PVE/PVP + security logic

---

# WEEK 6 — CONTENT + DATA + BUILD

## Day 28 — Content Migration
- `/Content/*` population

## Day 29 — Data Migration
- `/Data/*` normalization

## Day 30 — Config Cleanup
- `/Config/*` separation

## Day 31 — Build System Setup
- Solutions + scripts

## Day 32 — Service + Tool Startup Scripts
- One-command dev startup

---

# WEEK 7 — TESTING + CLEANUP

## Day 33 — Test Framework Setup
- `/Tests/*` structure

## Day 34 — Integration Tests
- service + bridge

## Day 35 — WPF + Service Validation
- full workflow test

## Day 36 — Remove Duplicates
- delete legacy code

## Day 37 — Rename Cleanup
- remove Arbiter leftovers

---

# WEEK 8 — HARDENING

## Day 38 — Dependency Audit
- enforce rules doc

## Day 39 — CI Setup
- build + validation checks

## Day 40 — Final Review
- architecture validation
- missing systems check

---

# FINAL RESULT

At completion:

- Atlas (engine) is clean
- AtlasAI (tooling + AI) fully integrated
- NovaForge gameplay fully migrated
- WPF tooling fully operational
- services + bridge stable
- repo structure enforceable long-term

---

# REALITY NOTE

This can compress or expand depending on time.

Even if stretched:

👉 Follow the ORDER — that’s what keeps this from breaking.

