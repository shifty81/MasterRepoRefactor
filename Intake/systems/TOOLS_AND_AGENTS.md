# Tools + Agents

Back: [System Index](./README.md)  
Related: [AI / Arbiter](./AI_ARBITER.md) · [Editor](./EDITOR.md)

## Purpose

`Tools/` contains standalone or embedded utilities. `Agents/` contains specialized automation units for build, code, cleanup, refactor, editor, PCG, asset, and debug workflows.

## Current repo footprint

Detected `Tools/` modules:
- `Tools/AdminConsole`
- `Tools/AnalyticsDashboard`
- `Tools/AssetPipeline`
- `Tools/AssetTools`
- `Tools/BenchmarkRunner`
- `Tools/BuildTools`
- `Tools/ChangeTracker`
- `Tools/CodeAudit`
- `Tools/DependencyAnalyzer`
- `Tools/DocGenerator`
- `Tools/GUI`
- `Tools/GitPanel`
- `Tools/Importer`
- `Tools/Locator`
- `Tools/MemoryProfiler`
- `Tools/MetricsReporting`
- `Tools/Packing`
- `Tools/Profiler`
- `Tools/ReplayTimeline`
- `Tools/Scaffolding`
- `Tools/ScriptRunner`
- `Tools/ServerManager`
- `Tools/SimulationPlayback`
- `Tools/TestPipeline`

Detected `Agents/` modules:
- `Agents/AssetAgent`
- `Agents/BuildAgent`
- `Agents/CleanupAgent`
- `Agents/CodeAgent`
- `Agents/DebugAgent`
- `Agents/EditorAgent`
- `Agents/FixAgent`
- `Agents/PCGAgent`
- `Agents/RefactorAgent`
- `Agents/SelfBuildAgent`
- `Agents/VersionAgent`

## Operational model

```text
Arbiter
  │
  ├── invokes Agents for scoped execution
  │      ├── BuildAgent
  │      ├── CodeAgent
  │      ├── RefactorAgent
  │      ├── PCGAgent
  │      └── EditorAgent
  │
  └── uses Tools for repo insight / output
         ├── DocGenerator
         ├── CodeAudit
         ├── DependencyAnalyzer
         ├── AssetPipeline
         └── TestPipeline
```

## Why this pack matters here
The repo already contains a `Tools/DocGenerator` module, but this docs pack adds a repo-ready, markdown-first layer plus a Python compliance workflow that can run even before those C++ tools are finished.
