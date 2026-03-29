# Builder

Back: [System Index](./README.md)  
Related: [Editor](./EDITOR.md) · [PCG](./PCG.md) · [Runtime + Projects](./RUNTIME_AND_PROJECTS.md)

## Purpose

`Builder/` contains the modular construction pipeline used for ships, stations, assemblies, parts, snap rules, damage, export, packaging, and physics-ready structures.

## Current repo footprint

Detected `Builder/` modules:
- `Builder/Assembly`
- `Builder/Blueprint`
- `Builder/Collision`
- `Builder/Core`
- `Builder/Damage`
- `Builder/Export`
- `Builder/InteriorNode`
- `Builder/Modules`
- `Builder/Packaging`
- `Builder/Parts`
- `Builder/PhysicsData`
- `Builder/SnapRules`

## Builder architecture

```text
Parts / Modules / Interior Nodes
             │
             ▼
       Snap + Weld Rules
             │
             ▼
       Assembly Graph
        │        │
        ▼        ▼
   Physics Data  Damage Data
        │        │
        └──► Export / Packaging
```

## Project-fit note

This system is a strong fit for the project's hybrid direction:
- voxel systems define structural mass, destruction, mining, repair
- builder modules and low-poly components define readable visual assemblies and interactable surface detail

## Suggested extensions
- tier propagation rules for module visuals
- conduit / pipe / panel decoration propagation
- interior + exterior style inheritance from functional upgrades
