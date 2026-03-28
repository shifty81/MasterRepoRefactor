# Project Roadmap

> For the full epic and task breakdown see [`MASTER_IMPLEMENTATION_CHECKLIST.md`](../../New%20Implementations%20that%20need%20addressed/MASTER_IMPLEMENTATION_CHECKLIST.md).  
> For the architectural vision see [`Docs/Design/MASTER_DESIGN_DOCUMENT.md`](../Design/MASTER_DESIGN_DOCUMENT.md).

---

## What Has Been Completed

All ten foundation epics have been executed.

| Epic | Title | Key Outcomes |
|---|---|---|
| 1 | Lock the monorepo architecture | Ownership zones defined; boundary, dependency, and shipping-separation rules documented. |
| 2 | Restructure the repo physically | Atlas, NovaForge, Arbiter, and Shared directories established; code migrated to correct zones. |
| 3 | Stand up the bridge backbone | `AtlasBridgeContract` shared types created; bridge transport model documented; NovaForge bridge implementation scaffolded. |
| 4 | Wire the first usable endpoints | `/project/info`, `/editor/selection`, `/build/run`, and `/editor/tools/run` endpoints implemented; log routing added. |
| 5 | Refactor NovaForge into callable modules | Monolithic startup split; project context isolated; editor tool hooks separated from game runtime. |
| 6 | Refactor Arbiter into a real host shell | Generic modules separated from project-specific ones; NovaForge logic moved to a dedicated adapter; workspace loading standardised. |
| 7 | Build system cleanup | CMake structure updated; Arbiter made optional; editor/tooling targets separated from shipping; feature guards added. |
| 8 | Safety, logging, and operational controls | Action allowlist enforced; dry-run defaulted to `true`; audit logging added; local trust/auth guard implemented. |
| 9 | First real workflow milestone | Arbiter can read project info, query editor selection, launch a safe build target, and run a safe editor tool; shipping isolation verified. |
| 10 | Second-wave improvements | Search roots added; builder/PCG tool hooks expanded; richer editor state snapshots implemented; codegen proposal workflow and workspace dashboard added. |

---

## Current Status

The monorepo structure is stable and all ten foundation epics are complete. The bridge between Arbiter (AtlasAI) and the NovaForge/Atlas backend is operational with:

- REST endpoints for project info, editor state, build targets, and tool actions.
- WebSocket event streams for async feedback (build progress, selection changes).
- A dry-run-first safety model with audit logging on every mutating action.
- Clean zone boundaries enforced by CMake and documented in `Docs/Architecture/`.

---

## Near-Term Goals

### Scripts & Automation
- Add `Scripts/` entry points for common developer tasks (build, lint, run bridge server, run tests).
- Automate audit log rotation and workspace snapshot exports.
- Add a CI workflow that validates JSON schema correctness and runs bridge smoke tests.

### Testing Expansion
- Add unit tests for all bridge endpoint handlers (ProjectService, EditorService, BuildService).
- Add integration tests that spin up the bridge server and exercise each endpoint end-to-end.
- Add schema validation tests that confirm all request/response payloads round-trip against the schemas in `Shared/ToolProtocol/schemas/`.

### Documentation
- Populate per-module docs in `Docs/Atlas/`, `Docs/NovaForge/`, and `Docs/Arbiter/` as subsystems stabilise.
- Add an OpenAPI/AsyncAPI specification generated from the JSON schemas.

---

## Long-Term Vision

The following goals are drawn from `Docs/Design/MASTER_DESIGN_DOCUMENT.md` and `Docs/Design/MISSING_SYSTEMS_ADDENDUM.md`.

### Full Codegen Workflow
The codegen proposal workflow (Epic 10 / Task 10.4) provides the foundation for AI-assisted code generation. The long-term goal is a human-in-the-loop system where AtlasAI proposes, diffs, and — only after explicit approval — applies code changes to the repository.

### Multi-Workspace & Multi-Project Support
Arbiter should evolve to manage multiple concurrent project workspaces, each with an independent bridge session, so that Atlas engine work and NovaForge game work can be managed from a single Arbiter instance.

### Live Viewport Integration
The `supportsViewportAttach` capability (defined in `ProjectCapabilities`) will allow AtlasAI to observe and annotate the live editor viewport — enabling richer context for AI suggestions.

### Live Patch & Hot Reload
The `supportsLivePatch` capability will allow Arbiter to push approved code or data changes into a running editor session without a full rebuild.

### Expanded PCG & Builder Tooling
The `BuilderToolActionId` second-wave actions (Epic 10 / Task 10.2) provide the scaffolding for deep PCG and builder integration, including diagnostics, preview mesh generation, and builder entity validation — all accessible from AtlasAI without leaving the workspace.

### Shipping & Distribution
Shipping isolation rules (Epic 1 / Task 1.5, Epic 7 / Task 7.3) ensure that none of the tooling or AI infrastructure leaks into production builds. Long-term, the build system will include automated checks that verify this at every CI run.
