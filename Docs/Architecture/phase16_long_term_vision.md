# Phase 16 — Long-Term Vision

> **Status:** Complete — all four sub-phases implemented.

This document details the concrete implementation plan for the four long-term vision themes
identified in the roadmap.  Each phase is broken into discrete, testable checklist items.

---

## Phase 16A — Full Codegen Workflow

**Status:** `[x] Complete`

The AI-assisted codegen loop closes the human-in-the-loop gap: AtlasAI proposes a source
change, a unified diff is surfaced in the Atlas IDE diff panel, the developer inspects and
approves (or rejects) the patch, and the approved diff is applied automatically.
`CodegenDiffRelay` (Phase 13) already bridges the AI ↔ bridge boundary; this phase wires
the remaining IDE and patch-application pieces.

- [x] Implement `DiffPanelWidget` in `Atlas/Editor/Panels/` — renders a two-column unified
  diff view, highlights additions/deletions, supports approve/reject actions.
- [x] Add `CodegenApprovalService` endpoint to the FastAPI bridge (`AtlasAI/Services/`) that
  receives a diff payload from `CodegenDiffRelay` and holds it pending UI approval.
- [x] Wire approve/reject signals from `DiffPanelWidget` back to `CodegenApprovalService` via
  the WebSocket event relay.
- [x] Implement `PatchApplicator` utility (`Atlas/Editor/Core/`) that applies a validated diff
  to the workspace file tree using Python's `patch` library or a native equivalent.
- [x] Add integration test `AtlasAI/Tests/test_phase16a_codegen_workflow.py` exercising the
  full propose → approve → apply round trip.

---

## Phase 16B — Multi-Workspace & Multi-Project

**Status:** `[x] Complete`

`MultiWorkspaceManager` (Phase 13, `AtlasAI/live/multi_workspace.py`) tracks concurrent
bridge sessions, but the Atlas IDE shell has no UI surface for switching between them.
This phase adds workspace lifecycle management and project-switching UX to the editor shell.

- [x] Extend `MultiWorkspaceManager` with `activate(workspace_id)` / `close(workspace_id)`
  lifecycle methods and a `WorkspaceChangedEvent` signal.
- [x] Add `WorkspaceSwitcherPanel` to `Atlas/Editor/Panels/` — lists open workspaces, shows
  active project name and connection status, supports single-click switch.
- [x] Wire `WorkspaceSwitcherPanel` into `EditorShell` menu bar and toolbar.
- [x] Implement project-state serialisation so switching workspaces saves/restores editor
  layout, open documents, and inspector selection.
- [x] Add tests in `AtlasAI/Tests/test_phase16b_multi_workspace.py` covering open, switch,
  and close transitions with mock bridge sessions.

---

## Phase 16C — Expanded PCG & Builder Tooling

**Status:** `[x] Complete`

The second wave of `BuilderToolActionId` values (beyond the scaffold established in Phase 11)
enables deeper procedural content generation from within the editor — preview mesh generation,
builder entity validation, and real-time diagnostics — without leaving the AtlasAI workspace.

- [x] Define second-wave `BuilderToolActionId` entries in
  `Atlas/Editor/PCG/BuilderToolActionId.h` (e.g. `PreviewMesh`, `ValidateEntity`,
  `RunDiagnostics`, `ExportPCGSeed`).
- [x] Implement `PreviewMeshGenerator` (`Atlas/Engine/PCG/`) that produces a lightweight
  proxy mesh for a PCG descriptor, callable from both editor and bridge contexts.
- [x] Add `BuilderEntityValidator` (`Atlas/Editor/Validation/`) that checks builder entity
  components against schema and reports structured diagnostics.
- [x] Expose PCG diagnostics through a new `DiagnosticsPanel` in `Atlas/Editor/Panels/`
  with severity filtering and jump-to-source links.
- [x] Add `AtlasAI/Tests/test_phase16c_pcg_builder.py` covering action dispatch, preview
  mesh output shape, and validator error reporting.

---

## Phase 16D — Shipping & Distribution

**Status:** `[x] Complete`

The Inno Setup script (`AtlasAI/Installer/atlasai_setup.iss`) already describes the
installer layout.  This phase automates the release pipeline: a tagged push triggers a
GitHub Actions workflow that compiles the installer, signs the artefact, and publishes it
to the GitHub release.

- [x] Create `.github/workflows/release.yml` — triggers on `push` to tags matching
  `v[0-9]*`, runs on `windows-latest`, builds the Inno Setup installer via `iscc.exe`.
- [x] Add installer signing step using a repository secret (`CODESIGN_PFX`) and
  `signtool.exe` from the Windows SDK.
- [x] Upload the compiled `.exe` as a GitHub release artefact using the `softprops/action-gh-release`
  action.
- [x] Add a Linux/macOS tarball job to the same workflow for the AtlasAI Python package
  distribution (`python -m build` → upload `.whl` and `.tar.gz`).
- [x] Document the release procedure in `Docs/Architecture/shipping_separation.md` and
  update `README.md` with a "Download" badge pointing to the latest release.
