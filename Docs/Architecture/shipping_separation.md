# Shipping Separation Rules

## Goal

Shipping client and server builds must not include Arbiter UI, tooling code,
or any development-only infrastructure.

## CMake flags

| Flag | Default | Purpose |
|------|---------|---------|
| `MASTERREPO_BUILD_EDITOR` | `ON` | Include editor targets |
| `NOVAFORGE_ENABLE_ARBITER_INTEGRATION` | `ON` | Include NovaForge bridge layer |
| `MASTERREPO_BUILD_TOOLS` | `ON` | Include developer tool targets |

For a shipping build, set:

```cmake
-DMASTERREPO_BUILD_EDITOR=OFF
-DNOVAFORGE_ENABLE_ARBITER_INTEGRATION=OFF
-DMASTERREPO_BUILD_TOOLS=OFF
```

## Rules

1. `NovaForge/Integrations/Arbiter/` must only be compiled when
   `NOVAFORGE_ENABLE_ARBITER_INTEGRATION=ON`.

2. Atlas editor systems (`Atlas/Editor/`) must only be compiled when
   `ATLAS_ENABLE_EDITOR=ON`.

3. Arbiter is a C#/.NET project. It must never be referenced by C++ game
   or engine targets directly.

4. Any header in `NovaForge/Integrations/Arbiter/include/` must be guarded
   and never `#include`d from core gameplay or runtime code.

## Verification

Before any release:

1. Configure with all tooling/editor flags OFF.
2. Confirm CMake configure succeeds.
3. Confirm build succeeds without any Arbiter or editor artifacts.
4. Confirm no `ArbiterBridge*` symbols appear in shipping binaries.
