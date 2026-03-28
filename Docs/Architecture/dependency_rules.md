# Dependency Rules

See also: `repo_boundaries.md` for zone-level rules.

## Dependency direction

Dependencies must flow **downward** toward more stable, reusable layers:

```
Tools / UI
   ↓
Services / Bridge
   ↓
Shared Contracts / Schemas
   ↓
Engine / Runtime / Editor Backend
   ↓
Core Platform / Utilities
```

## Hard rules

1. No engine module may depend on a game module.
2. No shared contract module may depend on an implementation module.
3. No WPF module may become the hidden owner of service business logic.
4. No AI module may require UI assemblies to function.
5. No service should require WPF to be running.

## Allowed dependencies

| Module | May depend on |
|--------|---------------|
| `AtlasCore` | C++ standard library, platform wrappers |
| `AtlasEngine` | `AtlasCore`, selected `Shared` contracts |
| `AtlasRuntime` | `AtlasEngine`, `AtlasCore` |
| `AtlasEditor` | `AtlasRuntime`, engine modules |
| `AtlasUI` | `AtlasCore` |
| `NovaForgeApp` | `AtlasRuntime` |
| `NovaForgeGameplay` | `AtlasEngine` |
| `NovaForgeWorld` | `AtlasEngine` |
| `NovaForgeIntegrationAtlasAI` | `AtlasBridgeContract`, `AtlasRuntime` |
| `AtlasBridgeContract` | nothing (header-only interface) |
| AtlasAI C# adapters | `Shared/ToolProtocol`, manifests |

## Forbidden dependencies

- `Atlas*` → `NovaForge*`
- `Atlas*` → `AtlasAI*`
- `NovaForge*` (non-integration) → `AtlasAI*`
- `Shared*` → engine implementations
- `Shared*` → game implementations
- `Shared*` → UI assemblies

## Red flags

If any of these appear, the architecture is drifting:

- WPF view models containing gameplay logic
- Engine modules importing NovaForge headers
- Shared contract assemblies importing service code
- AI orchestration modules coupled to visual controls
- Multiple "utility" libraries becoming unowned dumping grounds
