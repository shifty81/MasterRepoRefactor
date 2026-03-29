# Config + Schemas

Back: [System Index](./README.md)  
Related: [AI / Arbiter](./AI_ARBITER.md) · [Runtime + Projects](./RUNTIME_AND_PROJECTS.md)

## Purpose

This doc indexes repo-observed JSON-backed configuration and content data. It is the natural input surface for the Arbiter Auto-Doc Generator.

## Important JSON files currently present

- `AI/Models/codellama.json`
- `AI/Models/llama3.json`
- `AI/Models/mistral.json`
- `AI/Models/orca_mini.json`
- `CMakePresets.json`
- `Config/AI.json`
- `Config/Builder.json`
- `Config/Editor.json`
- `Config/Engine.json`
- `Config/Projects.json`
- `Config/Server.json`
- `Projects/NovaForge/Assets/asset_manifest.json`
- `Projects/NovaForge/Config/game.json`
- `Projects/NovaForge/Config/player_settings.json`
- `Projects/NovaForge/Data/Universe/systems.json`
- `Projects/NovaForge/Data/factions.json`
- `Projects/NovaForge/Data/gas_types.json`
- `Projects/NovaForge/Modules/cockpit_module.json`
- `Projects/NovaForge/Modules/engine_module.json`
- `Projects/NovaForge/Parts/cockpit_mk1.json`
- `Projects/NovaForge/Parts/starter_hull.json`
- `Projects/NovaForge/Parts/thruster_basic.json`
- `Projects/NovaForge/Prefabs/starter_ship.json`
- `Projects/NovaForge/Recipes/crafting_recipes.json`
- `Projects/NovaForge/Scenes/main_scene.json`
- `Projects/NovaForge/Ships/nova_fighter.json`
- `Projects/NovaForge/Ships/patrol_cruiser.json`
- `Projects/NovaForge/UI/hud_layout.json`
- `vcpkg.json`

## Example schema notes

### `Config/AI.json`
- provider: `ollama`
- default model: `deepseek-coder`
- memory enabled: `True`

### `Config/Builder.json`
- snap distance: `0.1`
- max parts: `1000`

### `Config/Editor.json`
- theme: `dark`
- layout: `default`

### `Config/Engine.json`
- renderer backend: `OpenGL`
- physics backend: `Bullet`

### `Projects/NovaForge/Config/game.json`
- title: `NovaForge`
- version: `0.1.0`
- default player: `Prefabs/starter_ship.json`

## Schema documentation flow

```text
JSON / data files
      │
      ▼
Arbiter Auto-Doc Generator
      │
      ├── schema reference markdown
      ├── example tables
      ├── key/type/default summaries
      └── outbound links from system docs
```

## Recommendation

Treat every gameplay-critical JSON file as a documented contract, especially:
- config files
- scenes
- prefabs
- ships
- recipes
- module definitions
- part definitions
- universe/faction data
