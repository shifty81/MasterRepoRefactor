# Runtime + Projects

Back: [System Index](./README.md)  
Related: [Engine](./ENGINE.md) · [Config + Schemas](./CONFIG_AND_SCHEMAS.md)

## Purpose

`Runtime/` holds shared game runtime features, while `Projects/` contains product/game-specific content. In the current repo, `Projects/NovaForge/` is the key game-facing area.

## Current repo footprint

Top-level runtime/project areas:
- `Runtime/AI`
- `Runtime/Achievement`
- `Runtime/Analytics`
- `Runtime/Animation`
- `Runtime/Audio`
- `Runtime/BuilderRuntime`
- `Runtime/Collision`
- `Runtime/Combat`
- `Runtime/Components`
- `Runtime/Crafting`
- `Runtime/Crowd`
- `Runtime/Damage`
- `Runtime/Dialogue`
- `Runtime/ECS`
- `Runtime/Economy`
- `Runtime/Equipment`
- `Runtime/Faction`
- `Runtime/Factions`
- `Runtime/Gameplay`
- `Runtime/Hazards`
- `Runtime/HeadlessServer`
- `Runtime/Input`
- `Runtime/Inventory`
- `Runtime/Leaderboard`
- `Runtime/Minimap`
- `Runtime/Mod`
- `Runtime/Multiplayer`
- `Runtime/NPC`
- `Runtime/Narrative`
- `Runtime/Network`
- `Runtime/Notification`
- `Runtime/Physics`
- `Runtime/Player`
- `Runtime/Quest`
- `Runtime/Replay`
- `Runtime/Save`
- `Runtime/SaveGame`
- `Runtime/SaveLoad`
- `Runtime/Scene`
- `Runtime/Session`
- `Runtime/Sim`
- `Runtime/Spawn`
- `Runtime/StateSync`
- `Runtime/Streaming`
- `Runtime/Systems`
- `Runtime/UI`
- `Runtime/Universe`
- `Runtime/World`
- `Projects/NovaForge`

## NovaForge content map

```text
Projects/NovaForge/
├── Assets
├── Config
├── Data
├── Modules
├── Parts
├── Prefabs
├── Recipes
├── Scenes
├── Ships
└── UI
```

## Observed gameplay/config themes
- zero-gravity or space-forward physics configuration
- ship/default-player bootstrap
- faction data
- crafting recipes and items
- UI layout data
- prefab and ship definitions

## Project-specific standards
- use `Rig` terminology in character/equipment docs
- preserve season configurability with server authority by default
- align runtime gameplay docs with voxel + low-poly hybrid architecture
