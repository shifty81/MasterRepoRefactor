# Repo Boundaries

## Purpose

This document defines what each top-level ownership zone owns, what it does not own,
and what dependencies are forbidden across zone boundaries.

---

## Atlas

### Owns
- engine runtime
- renderer
- physics, audio, animation, input, networking
- ECS and world systems
- editor framework (backend only)
- custom UI framework
- asset pipeline runtime
- platform abstraction

### Does not own
- NovaForge gameplay logic
- Arbiter host UI, chat, archive, or automation internals
- game-specific data tables or content

### Forbidden dependencies
- Atlas must not depend on Arbiter
- Atlas must not depend on NovaForge

---

## NovaForge

### Owns
- all game-specific gameplay systems
- client and server bootstraps
- game data and content definitions
- game-specific tools and validators
- Arbiter-facing integration code (under `NovaForge/Integrations/Arbiter/` only)

### Does not own
- engine internals (consumed via Atlas API)
- Arbiter host UI, chat, archive, or automation internals
- build toolchain logic outside of game-specific wrappers

### Forbidden dependencies
- NovaForge must not depend on Arbiter host, chat, archive, UI, or automation internals
- NovaForge may consume Shared contracts only for bridge integration

---

## Arbiter

### Owns
- AI tooling shell (HostApp)
- AI engine and orchestration (AIEngine)
- archive and knowledge systems (Archive)
- automation workflows (Automation)
- Visual Studio extension (VisualStudioExtension)
- project adapters (ProjectAdapters/*)
- workspace and session management

### Does not own
- engine runtime
- world simulation state
- asset serialization rules
- build toolchain internals
- gameplay runtime authority
- docking/shell logic of native editor panels

### Forbidden dependencies
- Arbiter must not directly reference Atlas engine internals
- Arbiter may use Shared contracts and project adapters only

---

## Shared

### Owns
- bridge contracts (ArbiterBridgeContract)
- project manifests (ProjectManifests)
- tool protocol definitions (ToolProtocol)
- build metadata
- naming and style conventions

### Does not own
- gameplay logic
- editor shell logic
- Arbiter host UI code
- engine implementation details

### Rules
- Shared must remain small and stable
- Shared defines boundaries; it must not know who consumes them

---

## Dependency direction (summary)

```
Shared ─────────────► Atlas        ✓ allowed
Shared ─────────────► NovaForge    ✓ allowed
Shared ─────────────► Arbiter      ✓ allowed

Atlas ──────────────► NovaForge    ✗ forbidden
Atlas ──────────────► Arbiter      ✗ forbidden

NovaForge ──────────► Arbiter internals  ✗ forbidden
NovaForge ──────────► Shared contracts  ✓ allowed (bridge only)

Arbiter ────────────► Shared contracts           ✓ allowed
Arbiter ────────────► ProjectAdapters/NovaForge  ✓ allowed
Arbiter ────────────► NovaForge only through bridge/protocol  ✓ allowed
```

---

## Shipping separation rules

- Shipping client / server builds must not pull any Arbiter UI or tooling assemblies.
- Editor-only integrations must be guarded by `MASTERREPO_BUILD_EDITOR` and
  `NOVAFORGE_ENABLE_ARBITER_INTEGRATION` flags.
- Development-only tooling paths must not leak into runtime binaries.
