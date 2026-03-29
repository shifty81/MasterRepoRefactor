# Editor

Back: [System Index](./README.md)  
Related: [Builder](./BUILDER.md) · [Tools + Agents](./TOOLS_AND_AGENTS.md)

## Purpose

`Editor/` houses the custom editor stack for content creation, viewport tools, panels, node editors, GUI editing, builder editing, and PCG authoring.

## Current repo footprint

Detected `Editor/` modules:
- `Editor/BuilderEditor`
- `Editor/Commands`
- `Editor/Core`
- `Editor/Docking`
- `Editor/GUIEditor`
- `Editor/Gizmo`
- `Editor/Gizmos`
- `Editor/MaterialEditor`
- `Editor/Modes`
- `Editor/NodeEditors`
- `Editor/Overlay`
- `Editor/PCGEditor`
- `Editor/Panels`
- `Editor/Render`
- `Editor/Tools`
- `Editor/UI`
- `Editor/Viewport`

## Editor direction

The project direction favors a custom UI/editor experience rather than defaulting to ImGui as the main user-facing layer.

## Editor flow

```text
Project Load
   │
   ▼
Layout / Panels / Docking
   │
   ├── Viewport
   ├── Builder Editor
   ├── PCG Editor
   ├── Material / Node Editors
   ├── Commands / Gizmos / Tools
   └── AI Panel / Arbiter Integration
```

## Expected responsibilities
- project browser
- scene and prefab editing
- builder authoring
- PCG authoring
- AI-assisted tasking and review
- diagnostics, overlays, and property inspection
