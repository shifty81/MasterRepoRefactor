# MASTERREPO_GITHUB_ISSUES_PACK

## Purpose
This document converts the roadmap into **ready-to-create GitHub issues**.

Each issue includes:
- title
- description
- tasks
- acceptance criteria
- labels

---

# PHASE 1 — MONOREPO FOUNDATION

## Issue 1.1 — Create MasterRepo top-level structure
**Labels:** phase-1, architecture, repo

### Tasks
- Create folders: Atlas, NovaForge, Arbiter, Shared, Docs, Tools, Scripts, Tests
- Add placeholder README in each

### Acceptance Criteria
- Repo matches target tree blueprint at top level

---

## Issue 1.2 — Add base CMake + options
**Labels:** phase-1, build

### Tasks
- Add root CMakeLists.txt
- Add cmake/Options.cmake
- Verify configure succeeds

### Acceptance Criteria
- CMake config runs without errors

---

# PHASE 2 — SHARED + BRIDGE

## Issue 2.1 — Create ArbiterBridgeContract
**Labels:** phase-2, shared

### Tasks
- Add Shared/ArbiterBridgeContract
- Add ArbiterBridgeTypes.h

### Acceptance Criteria
- Target compiles as INTERFACE lib

---

## Issue 2.2 — Add project manifest
**Labels:** phase-2, shared

### Tasks
- Add Shared/ProjectManifests/novaforge.project.json

### Acceptance Criteria
- Arbiter can load manifest (stub)

---

# PHASE 3 — ATLAS EXTRACTION

## Issue 3.1 — Move Core systems to Atlas
**Labels:** phase-3, atlas

### Tasks
- Move Core/*
- Update includes + CMake

### Acceptance Criteria
- AtlasCore builds clean

---

## Issue 3.2 — Move Engine systems to Atlas
**Labels:** phase-3, atlas

### Tasks
- Move Engine/*
- Validate dependencies

### Acceptance Criteria
- AtlasEngine builds clean

---

# PHASE 4 — NOVAFORGE STRUCTURE

## Issue 4.1 — Create NovaForge modules
**Labels:** phase-4, novaforge

### Tasks
- Create Gameplay, World, Tools, App folders

### Acceptance Criteria
- Folder structure matches blueprint

---

## Issue 4.2 — Move data/content
**Labels:** phase-4, novaforge

### Tasks
- Move Projects/NovaForge data → NovaForge/Data + Content

### Acceptance Criteria
- Game data loads from new paths

---

# PHASE 5 — SPLIT MIXED SYSTEMS

## Issue 5.1 — Split Editor systems
**Labels:** phase-5, refactor

### Tasks
- Separate generic editor → Atlas
- Move project tools → NovaForge/Tools

### Acceptance Criteria
- Editor builds without NovaForge dependency leakage

---

## Issue 5.2 — Split Runtime systems
**Labels:** phase-5, refactor

### Tasks
- Separate generic runtime → Atlas
- Move project boot logic → NovaForge/App

### Acceptance Criteria
- Runtime layer is project-agnostic

---

# PHASE 6 — ARBITER EXTRACTION

## Issue 6.1 — Create Arbiter structure
**Labels:** phase-6, arbiter

### Tasks
- Create HostApp, AIEngine, ProjectAdapters

### Acceptance Criteria
- Folder structure matches blueprint

---

## Issue 6.2 — Move AI + IDE systems
**Labels:** phase-6, arbiter

### Tasks
- Move AI/, IDE/, Agents/ into Arbiter

### Acceptance Criteria
- Arbiter builds independently

---

# PHASE 7 — BRIDGE INTEGRATION

## Issue 7.1 — Implement bridge service
**Labels:** phase-7, integration

### Tasks
- Add NovaForgeIntegrationArbiter
- Stub start/stop endpoints

### Acceptance Criteria
- Arbiter can connect (stub)

---

## Issue 7.2 — Implement project adapter
**Labels:** phase-7, integration

### Tasks
- Add Arbiter/ProjectAdapters/NovaForge
- Load manifest + connect to bridge

### Acceptance Criteria
- Adapter initializes successfully

---

# PHASE 8 — BUILD + DEPENDENCY CLEANUP

## Issue 8.1 — Enforce dependency rules
**Labels:** phase-8, architecture

### Tasks
- Audit includes
- Remove forbidden dependencies

### Acceptance Criteria
- No violations per dependency charter

---

## Issue 8.2 — Shipping isolation
**Labels:** phase-8, build

### Tasks
- Disable Arbiter integration in shipping builds
- Verify client/server clean

### Acceptance Criteria
- Shipping build has zero Arbiter linkage

---

# PHASE 9 — VALIDATION

## Issue 9.1 — Add integration tests
**Labels:** phase-9, testing

### Tasks
- Add bridge smoke tests
- Add build validation tests

### Acceptance Criteria
- Tests pass in CI

---

## Issue 9.2 — Final architecture audit
**Labels:** phase-9, audit

### Tasks
- Verify folder ownership
- Verify target graph

### Acceptance Criteria
- Matches blueprint + charter

---

# Suggested Labels

- phase-1 … phase-9
- atlas
- novaforge
- arbiter
- shared
- integration
- refactor
- architecture
- build
- testing
