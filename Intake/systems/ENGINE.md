# Engine

Back: [System Index](./README.md)  
Related: [Core](./CORE.md) · [Editor](./EDITOR.md) · [Runtime + Projects](./RUNTIME_AND_PROJECTS.md)

## Purpose

`Engine/` provides rendering, physics, scene, input, networking, animation, audio, and simulation-level runtime services.

## Current repo footprint

Detected `Engine/` modules:
- `Engine/AI`
- `Engine/Animation`
- `Engine/Asset`
- `Engine/Audio`
- `Engine/Camera`
- `Engine/Cinematic`
- `Engine/Core`
- `Engine/Curve`
- `Engine/Debug`
- `Engine/Decals`
- `Engine/Font`
- `Engine/Graphics`
- `Engine/Input`
- `Engine/Lighting`
- `Engine/Lod`
- `Engine/Math`
- `Engine/Net`
- `Engine/Network`
- `Engine/Occlusion`
- `Engine/Particles`
- `Engine/Pathfinding`
- `Engine/Physics`
- `Engine/Platform`
- `Engine/PostProcess`
- `Engine/Raycast`
- `Engine/Render`
- `Engine/Scene`
- `Engine/Scripting`
- `Engine/Shader`
- `Engine/Shadows`
- `Engine/Sim`
- `Engine/Spatial`
- `Engine/Spline`
- `Engine/Terrain`
- `Engine/Tile`
- `Engine/Timeline`
- `Engine/Tween`
- `Engine/Vehicle`
- `Engine/Voxel`
- `Engine/Water`
- `Engine/Window`
- `Engine/World`

## High-level structure

```text
            +------------------+
            |      Engine      |
            +------------------+
              │    │    │   │
      ┌───────┘    │    │   └─────────┐
      ▼            ▼    ▼             ▼
  Render      Physics  Scene       Net/Input
      │            │    │             │
      └──────┬─────┘    └──────┬──────┘
             ▼                 ▼
        Runtime Game      Editor Viewports
```

## Standards
- Engine stays generic enough to support multiple products.
- Project-specific gameplay should stay under `Projects/` and `Runtime/`.
- Voxel and low-poly rendering paths must coexist cleanly.
