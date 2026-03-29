# Core

Back: [System Index](./README.md)  
Related: [Engine](./ENGINE.md) · [Config + Schemas](./CONFIG_AND_SCHEMAS.md)

## Purpose

`Core/` is the foundational substrate shared across engine, editor, runtime, tooling, and AI systems.

## Current repo footprint

Detected `Core/` modules:
- `Core/Allocator`
- `Core/ArchiveSystem`
- `Core/AssetMetadata`
- `Core/AsyncTask`
- `Core/Cache`
- `Core/CloudSync`
- `Core/CodeIntelligence`
- `Core/CommandSystem`
- `Core/Compression`
- `Core/Config`
- `Core/Coroutine`
- `Core/CrashReport`
- `Core/DataTable`
- `Core/Database`
- `Core/DeterministicSeed`
- `Core/ECS`
- `Core/EventDispatcher`
- `Core/EventLog`
- `Core/EventQueue`
- `Core/EventReplay`
- `Core/Events`
- `Core/FeatureFlags`
- `Core/GameState`
- `Core/HotReload`
- `Core/JobSystem`
- `Core/Jobs`
- `Core/LocalCIPipeline`
- `Core/Localisation`
- `Core/Localization`
- `Core/Messaging`
- `Core/Metadata`
- `Core/Net`
- `Core/NetworkProtocolGen`
- `Core/PackageManager`
- `Core/PluginSystem`
- `Core/Pool`
- `Core/Profiler`
- `Core/Profiling`
- `Core/Reflection`
- `Core/Render`
- `Core/Resource`
- `Core/ResourceManager`
- `Core/RingBuffer`
- `Core/Scripting`
- `Core/Serialization`
- `Core/Signal`
- `Core/StateMachine`
- `Core/Tags`
- `Core/TaskSystem`
- `Core/Telemetry`
- `Core/Threading`
- `Core/Time`
- `Core/TransactionManager`
- `Core/VersionSystem`

## Responsibility model

```text
Core
├── data + serialization
├── jobs + async + tasking
├── events + messaging
├── config + metadata + reflection
├── persistence + archive + versioning
├── telemetry + profiling + crash reporting
└── shared platform-neutral utilities
```

## Notes
- `Localization` and `Localisation` both exist right now and should be consolidated into one canonical active path.
- Core should remain dependency-light and avoid taking on gameplay logic directly.
- Versioning, serialization, and deterministic seed logic are especially important for voxel/PCG systems.
