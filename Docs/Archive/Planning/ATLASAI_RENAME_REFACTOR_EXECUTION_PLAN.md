# ATLASAI RENAME + REFACTOR EXECUTION PLAN

## Goal

Safely rename Arbiter -> AtlasAI and ArbiterAI -> AtlasAI.Core while preserving buildability and preparing MasterRepo for full consolidation.

This is a staged identity refactor, not a blind global find/replace.

---

## Phase 0 - Preparation

### Create a rename inventory

Track every place `Arbiter` or `ArbiterAI` appears:

- solution names
- project names
- folder names
- namespaces
- assembly names
- executable names
- config keys
- environment variables
- scripts
- CI jobs
- docs
- branding strings
- tray/menu labels
- installer/package metadata
- JSON schema references

### Freeze new old-name usage

Immediately stop adding new references to:

- `Arbiter`
- `ArbiterAI`

All new work should use:

- `AtlasAI`
- `AtlasAI.Core`

---

## Phase 1 - Soft Rename (lowest risk)

Rename only outward-facing identity first.

### Update

- app title text
- tray text
- splash/about text
- docs and roadmap files
- repo planning docs
- UI labels
- branding assets

### Keep stable temporarily

- namespaces
- some internal folder names
- package IDs if needed for build continuity

### Outcome

Users and docs see `AtlasAI`, while code still compiles with minimal churn.

---

## Phase 2 - Project / Solution Rename

Rename solution and project identities next.

### Recommended target names

- `Arbiter.sln` -> `AtlasAI.sln`
- `Arbiter.WpfHost.csproj` -> `AtlasAI.WpfHost.csproj`
- `Arbiter.UI.csproj` -> `AtlasAI.UI.csproj`
- `Arbiter.Services.csproj` -> `AtlasAI.Services.csproj`
- `ArbiterAI.csproj` -> `AtlasAI.Core.csproj`

### Also update

- assembly name
- root namespace
- output executable name
- package metadata
- launch profiles

### Validate after each project rename

- solution loads
- project references resolve
- build works
- startup app still launches

---

## Phase 3 - Namespace Migration

Migrate namespaces module by module.

### Example mapping

- `Arbiter` -> `AtlasAI`
- `Arbiter.UI` -> `AtlasAI.UI`
- `Arbiter.Core` -> `AtlasAI.Core`
- `Arbiter.Agents` -> `AtlasAI.Agents`
- `Arbiter.Services` -> `AtlasAI.Services`

### Rules

- do one project/module at a time
- build after each module
- update using/import statements immediately
- avoid mass replace across unrelated files without review

### Temporary compatibility option

If needed, keep a short-lived compatibility layer:

- forwarding namespaces
- adapter classes
- config aliases

This should be temporary only.

---

## Phase 4 - Folder Rename

After namespaces and project references are stable, rename physical folders.

### Example

- `/Arbiter/` -> `/AtlasAI/`
- `/ArbiterAI/` -> `/AtlasAI.Core/`

### Check after renames

- relative paths in solution files
- scripts
- CI build paths
- asset/resource paths
- packaging scripts
- installer manifests

---

## Phase 5 - Config / Script / CI Cleanup

Update all operational references.

### Must review

- appsettings files
- JSON/YAML configs
- build scripts
- PowerShell/Bash helpers
- CI pipeline names
- deployment packaging
- registry/app data paths if applicable
- log folder names
- cache/index/archive folder defaults

### Example policy

Prefer new paths like:

- `%AppData%/AtlasAI/`
- `logs/AtlasAI/`
- `cache/AtlasAI/`

Add migration logic if old paths matter.

---

## Phase 6 - MasterRepo Integration Naming

As AtlasAI is absorbed into MasterRepo, use the final layout:

```text
/AI/AtlasAI.Core
/AI/AtlasAI.Agents
/Tools/AtlasAI.WpfHost
/Tools/AtlasAI.Shell
/Tools/AtlasAI.Bridge
```

### Related bridge rename

- `ArbiterBridge` -> `AtlasAI.Bridge`

### Service-facing names

- `ArbiterChat` -> `AtlasAI.Chat`
- `ArbiterArchive` -> `AtlasAI.Archive`
- `ArbiterWorkspace` -> `AtlasAI.Workspace`

---

## Phase 7 - Hard Cleanup

Remove all remaining legacy references.

### Search for and eliminate

- `Arbiter`
- `ArbiterAI`
- old executable names
- old window titles
- old namespace leftovers
- old folder references

### Final verification

- clean build passes
- runtime launch passes
- WPF shell launch passes
- logs go to new names
- archive/index paths work
- documentation matches codebase

---

## Safe Execution Checklist

- rename docs first
- rename visible branding second
- rename projects third
- rename namespaces fourth
- rename folders fifth
- fix scripts/configs sixth
- remove compatibility shims last

---

## Suggested Git Strategy

Use small, reviewable commits.

### Suggested commit sequence

1. `docs: rename Arbiter platform references to AtlasAI in planning docs`
2. `feat: update UI branding from Arbiter to AtlasAI`
3. `refactor: rename Arbiter solution and projects to AtlasAI`
4. `refactor: migrate namespaces from Arbiter.* to AtlasAI.*`
5. `refactor: rename ArbiterAI core modules to AtlasAI.Core`
6. `build: update scripts and CI for AtlasAI naming`
7. `cleanup: remove remaining Arbiter references`

---

## Risk Notes

### Biggest risk areas

- WPF XAML namespace mappings
- serialized config names
- assembly-qualified type names
- reflection-based loading
- script paths
- package/resource URIs
- hardcoded executable names

### Mitigation

- rename incrementally
- build/test after each stage
- keep a transition alias only where necessary
- do not combine rename and major logic rewrites in the same commit

---

## Final Result

The platform identity becomes:

- `Atlas` for engine/runtime/editor backend
- `AtlasAI` for tooling, chat, archive, automation, and orchestration
- `NovaForge` for the game layer

That gives MasterRepo a clean, unified naming system before deeper subsystem consolidation begins.
