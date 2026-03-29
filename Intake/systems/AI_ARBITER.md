# AI / Arbiter

Back: [System Index](./README.md)  
Related: [Config + Schemas](./CONFIG_AND_SCHEMAS.md) · [Tools + Agents](./TOOLS_AND_AGENTS.md) · [Project Standard](../standards/MASTER_PROJECT_STANDARD.md)

## Purpose

`AI/` contains the Arbiter orchestration layer plus supporting AI services for planning, learning, validation, metrics, prompting, orchestration, model access, memory, and visualization.

## Current repo footprint

Primary AI modules discovered under `AI/`:
- `AI/AgentScheduler`
- `AI/AnomalyAlerting`
- `AI/Arbiter`
- `AI/ArchiveLearning`
- `AI/AssetLearning`
- `AI/BugTriage`
- `AI/BuildReport`
- `AI/CodeLearning`
- `AI/ConflictResolver`
- `AI/Context`
- `AI/ContextHelp`
- `AI/CyclicDependencyResolver`
- `AI/DecisionVisualizer`
- `AI/Embeddings`
- `AI/ErrorLearning`
- `AI/GoalPlanner`
- `AI/KnowledgeIngestion`
- `AI/Memory`
- `AI/MetaLearning`
- `AI/MetricsDashboard`
- `AI/ModelManager`
- `AI/Models`
- `AI/MultiAgent`
- `AI/OllamaClient`
- `AI/Orchestrator`
- `AI/PromptTemplate`
- `AI/Prompts`
- `AI/ReasoningVisualizer`
- `AI/RegressionTest`
- `AI/RenderingOptimizer`
- `AI/ResourceMonitor`
- `AI/RulesEngine`
- `AI/Sandbox`
- `AI/Server`
- `AI/SessionMemory`
- `AI/StreamingResponse`
- `AI/SuggestionSandbox`
- `AI/TestGen`
- `AI/Training`
- `AI/Tutorial`
- `AI/Validator`

## Arbiter role

The current repo already establishes Arbiter as the central orchestrator:

```text
User / Editor / Web UI
        │
        ▼
+----------------------+
|  ArbiterOrchestrator |
+----------------------+
   │      │        │
   │      │        ├── Knowledge Query
   │      ├────────┤
   │               └── Workflow Execution
   ▼
Model / Prompt / Memory / Agent Coordination / Validator
```

## Key responsibilities
- conversational planning
- workflow dispatch
- knowledge base query
- multi-agent coordination
- code/content assistance
- project memory and context routing
- validation / regression / metrics support

## Recommended documentation split inside the repo
- `Docs/AI/AI_SYSTEM.md` — platform-level overview
- `Docs/AI/ARBITER_WORKFLOWS.md` — intent routing, workflow graph, tool permissions
- `Docs/AI/ARBITER_MEMORY.md` — memory classes and retention policy
- `Docs/AI/ARBITER_MODELS.md` — provider/backend/model matrix
- `Docs/AI/ARBITER_SCHEMA_REFERENCE.md` — generated from JSON/schema inputs

## Dependency map

```text
Arbiter
├── ModelManager
├── OllamaClient
├── PromptTemplate
├── PromptLibrary
├── Memory / SessionMemory
├── KnowledgeIngestion
├── MultiAgent
├── Orchestrator
├── Validator / RegressionTest
└── MetricsDashboard / BuildReport / ResourceMonitor
```

## Gaps the pack is designed to close
- many AI modules exist, but their contracts are not split into stable per-system docs
- current Arbiter README is intentionally light and TODO-heavy
- schema-driven documentation is not automated yet

## Delivered with this pack
- an auto-doc generator that turns JSON/config/data structures into Markdown docs
- a compliance scanner that can verify AI doc presence and naming drift
