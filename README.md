# MasterRepoRefactor

A unified custom platform built around a monorepo architecture. Combines a game engine, editor/IDE, AI development assistant (AtlasAI), runtime tooling, and procedural world framework. The flagship game NovaForge demonstrates the full platform capabilities.

> **Design canon:** [Docs/Design/MASTER_DESIGN_DOCUMENT.md](Docs/Design/MASTER_DESIGN_DOCUMENT.md)
> **Architecture:** [Docs/Architecture/monorepo_layout.md](Docs/Architecture/monorepo_layout.md)
> **All docs:** [Docs/README.md](Docs/README.md)

---

## What This Is

MasterRepo is **not** just a game repo or just an AI coding tool. It is:

- **A game engine** (Atlas) — custom rendering, ECS, physics, audio, input, UI framework
- **A development environment** — custom editor/IDE with dockable panels, asset browser, code editor, and diff preview
- **A project-aware AI operating layer** (AtlasAI) — workspace indexing, patch generation, audit, and documentation
- **A runtime world simulation framework** — EVA, ship interiors, life support, airlocks, PCG
- **A content authoring platform** — ship/station builder, tooling overlay, design document system

The flagship game, **NovaForge**, is a low-poly first-person systemic sci-fi survival/salvage/build/exploration experience that serves as the proving ground for the entire platform.

---

## Monorepo Structure

```
MasterRepoRefactor/
├── Atlas/          Engine, editor framework, runtime foundations, custom UI
├── NovaForge/      Game project — gameplay, world, data, content, tools
├── AtlasAI/        AI tooling shell — host app, AI engine, automation, VS extension
├── Shared/         Bridge contracts, project manifests, tool protocol (interface only)
├── Docs/           Architecture, design, and integration documentation
├── ThirdParty/     Vendored external dependencies
├── Tools/          Repo-wide developer tools
├── Scripts/        Automation, setup, build, and CI scripts
├── Tests/          Repo-level integration and verification tests
├── Build/          Build orchestration metadata
└── cmake/          CMake modules and target helpers
```

See [Docs/Architecture/monorepo_layout.md](Docs/Architecture/monorepo_layout.md) for the full module breakdown.

---

## Core Ownership Zones

| Zone | Owns |
|------|------|
| **Atlas** | Engine runtime, renderer, ECS, custom UI framework, editor framework backend |
| **NovaForge** | All game-specific systems, client/server bootstraps, game data and content |
| **AtlasAI** | AI shell (HostApp), AI engine, archive, automation, VS extension, project adapters |
| **Shared** | Bridge contracts (`AtlasBridgeContract`), project manifests, tool protocol types only |

Key rule: dependencies flow **downward** — Atlas does not depend on NovaForge; NovaForge does not depend on AtlasAI internals. See [Docs/Architecture/dependency_rules.md](Docs/Architecture/dependency_rules.md).

---

## Documentation

### Design

| Document | Description |
|----------|-------------|
| [Master Design Document](Docs/Design/MASTER_DESIGN_DOCUMENT.md) | Full unified vision — all pillars, systems, gameplay design, implementation order, and canon laws |
| [Missing Systems Addendum](Docs/Design/MISSING_SYSTEMS_ADDENDUM.md) | Governance, validation, telemetry, metadata, and scaling systems |

### Architecture

| Document | Description |
|----------|-------------|
| [Monorepo Layout](Docs/Architecture/monorepo_layout.md) | Folder structure and CMake module targets |
| [Repo Boundaries](Docs/Architecture/repo_boundaries.md) | Zone ownership and forbidden cross-boundary dependencies |
| [Dependency Rules](Docs/Architecture/dependency_rules.md) | Module dependency direction and hard rules |
| [Shipping Separation](Docs/Architecture/shipping_separation.md) | CMake flags for tooling-free shipping builds |

### Integration

| Document | Description |
|----------|-------------|
| [AtlasAI Bridge](Docs/Integration/atlasai_bridge.md) | Transport model, protocol, and whitelisted tool actions |
| [Project Manifest Spec](Docs/Integration/project_manifest_spec.md) | `novaforge.project.json` schema |
| [Tool Protocol](Docs/Integration/tool_protocol.md) | REST/WebSocket endpoint and event reference |

---

## Build

This project uses **CMake**. Each zone has its own `CMakeLists.txt`.

### CMake Targets

| Target | Zone | Description |
|--------|------|-------------|
| `AtlasCore` | Atlas | Core platform utilities |
| `AtlasEngine` | Atlas | ECS, world, scene, assets, rendering |
| `AtlasRuntime` | Atlas | App framework, game loop, simulation |
| `AtlasEditor` | Atlas | Editor framework and panels |
| `AtlasUI` | Atlas | Custom UI framework |
| `NovaForgeApp` | NovaForge | Client/server bootstrap |
| `NovaForgeGameplay` | NovaForge | Factions, combat, economy, PCG |
| `NovaForgeWorld` | NovaForge | Galaxy, sectors, planets, ships |
| `NovaForgeIntegrationAtlasAI` | NovaForge | AtlasAI bridge integration layer |
| `AtlasBridgeContract` | Shared | Header-only bridge interface |

### Shipping Builds

To build without editor/tooling code:

```cmake
cmake -DMASTERREPO_BUILD_EDITOR=OFF \
      -DNOVAFORGE_ENABLE_ARBITER_INTEGRATION=OFF \
      -DMASTERREPO_BUILD_TOOLS=OFF \
      ..
```

### Tests

```bash
ctest --test-dir Build/
```

---

## Non-Negotiable Architecture Laws

- **No ImGui** — all UI is custom
- **No Atlas → NovaForge dependencies**
- **No Atlas → AtlasAI dependencies**
- **No NovaForge → AtlasAI internals** (bridge contract only)
- **Shared must stay small** — it defines boundaries, not implementations
- **Shipping builds must not include AtlasAI UI or tooling**

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Read the [architecture laws](Docs/Architecture/repo_boundaries.md) before adding code
4. Commit your changes (`git commit -m 'Add your feature'`)
5. Push to the branch and open a Pull Request

---

## License

This project is open source. See [LICENSE](LICENSE) for details.

