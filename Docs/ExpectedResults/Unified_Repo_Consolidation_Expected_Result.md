# Expected Result — Unified Repo Consolidation Pack

After applying this consolidation pack, you should have:
- one canonical repo tree
- one build target
- one startup path
- one orchestrator
- a clear map for resolving duplicates
- a clean next step into real integration work

## Canonical Build Target
`MasterRepoEditorRuntime` — the single unified executable that boots App → GameOrchestrator → all subsystems.

## Boot Order
1. `DataRegistry::Initialize` (data root)
2. `SaveManager::Initialize`
3. `World::Initialize(*Data)`
4. `Renderer::Initialize`
5. `RuntimeUIShell::Initialize`
6. `EditorShell::Initialize`
7. `GameOrchestrator::StartVerticalSliceSession`

## Status
All canonical sources migrated to:
- `NovaForge/App/` — App, GameOrchestrator, DataRegistry bootstrap
- `Atlas/Engine/Rendering/` — Renderer
- `NovaForge/Save/` — SaveManager
- `NovaForge/UI/` — RuntimeUIShell
- `Atlas/Editor/` — EditorShell
- `NovaForge/World/` — World
