# Monorepo Layout

## Top-level structure

```text
MasterRepo/
├── Atlas/          engine, editor framework, runtime foundations, custom UI
├── NovaForge/      game project, gameplay systems, data, content
├── AtlasAI/        AI tooling shell, automation, archive, VS extension
├── Shared/         bridge contracts, manifests, tool protocol only
├── Docs/           architecture, integration, and implementation docs
├── ThirdParty/     vendored external dependencies
├── Tools/          repo-wide developer tools
├── Scripts/        automation, setup, build, and CI scripts
├── Tests/          repo-level integration and verification tests
├── Build/          build orchestration metadata and artifacts
└── cmake/          CMake modules and target helpers
```

## Atlas structure

```text
Atlas/
├── Core/            containers, memory, math, IO, logging, diagnostics, jobs
├── Engine/          ECS, world, scene, assets, rendering, physics, audio, input
├── Runtime/         app framework, game loop, simulation, save/load
├── Editor/          editor framework, panels, commands, selection, tools
├── UI/              custom UI framework, layout, controls, styling, themes
├── Assets/          engine asset definitions
├── Config/          engine configuration
└── CMake/           Atlas-specific CMake helpers
```

## NovaForge structure

```text
NovaForge/
├── Client/          client app, presentation, HUD, input, client services
├── Server/          server app, simulation authority, persistence
├── Gameplay/        factions, economy, mining, combat, PCG, missions, builder
├── World/           galaxy, sectors, planets, stations, ships, encounters
├── Data/            config, definitions, tables, recipes, modules, parts
├── Content/         prefabs, scenes, UI, audio, materials, VFX
├── Tools/           importers, validators, authoring, generators
├── Integrations/    integration layers (Arbiter bridge under Integrations/Arbiter/)
├── App/             NovaForge app bootstrap, session, project context
├── Tests/           NovaForge unit and integration tests
├── Docs/            NovaForge-specific documentation
└── CMake/           NovaForge CMake helpers
```

## AtlasAI structure

```text
AtlasAI/
├── HostApp/         shell, workspace, chat, logs, build, file explorer
├── AIEngine/        core, models, providers, tools, memory, sessions, planning
├── ProjectAdapters/ per-project adapters (NovaForge adapter here)
├── Archive/         ingestion, indexing, retrieval, storage
├── Automation/      workflows, jobs, triggers, audit
├── VisualStudioExtension/  tool window, commands, inline assist
├── Tests/           AtlasAI unit tests
└── Config/          AtlasAI configuration
```

## Shared structure

```text
Shared/
├── ArbiterBridgeContract/  C++ header-only bridge types
├── ProjectManifests/       novaforge.project.json and others
├── ToolProtocol/           protocol docs and schemas
├── BuildMetadata/          build metadata artifacts
└── Conventions/            naming and coding conventions
```

## Module targets

### Atlas
- `AtlasCore`
- `AtlasEngine`
- `AtlasRuntime`
- `AtlasEditor`
- `AtlasUI`

### NovaForge
- `NovaForgeApp`
- `NovaForgeGameplay`
- `NovaForgeWorld`
- `NovaForgeIntegrationAtlasAI`

### Shared
- `ArbiterBridgeContract` (INTERFACE library)
