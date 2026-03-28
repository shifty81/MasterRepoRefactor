# DEV WORLD RUNTIME SCAFFOLD

## Purpose
This pack scaffolds the first NovaForge **Dev World** runtime slice so Atlas Suite can launch a predictable test environment for gameplay systems.

## Launch Flow
```text
Atlas Suite
→ Open NovaForge
→ PlaytestService.StartDevWorld()
→ EngineBridge.LoadScene("Projects/NovaForge/Scenes/dev_world.scene.json")
→ Spawn rig at `spawn_dev_room`
→ Enable test terminals and debug panels
```

## Core Runtime Goals
- single deterministic test scene
- one player spawn path
- one interaction path per major gameplay pillar
- zero menu dependency for core tests
- resettable state for repeated testing

## Included Runtime Areas
- Spawn Room
- Rig Terminal
- Inventory / Crafting Terminal
- Airlock + Pressure Room
- EVA Lane
- Mech Bay
- Ship Hangar
- Builder Pad
- Combat Range
- Salvage Lane
- Mission Board
- Economy / Faction Debug Terminals
- Save / Load Checkpoint

## Required Runtime Hooks
- scene load callback
- player spawn registration
- terminal interaction interface
- dev command registry
- checkpoint save/load
- construct spawn helpers
- objective test helpers

## Recommended Next Wiring
1. connect `PlaytestService` to `DevWorldBootstrap`
2. register `DevWorldSceneDefinition` in project scene loader
3. map each terminal to a single gameplay service
4. add one end-to-end smoke test command: `dev.run_full_loop`
