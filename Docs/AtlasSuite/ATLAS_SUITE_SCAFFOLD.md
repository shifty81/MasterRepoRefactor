# Atlas Suite Scaffold Pack

This pack provides a starter structure for the **Atlas Suite** WPF shell that hosts:
- project browser
- workspace shell
- docking layout
- viewport host
- playtest controls
- logs and inspector panels
- Arbiter integration entry points

## Startup flow

```text
App
→ MainWindow
→ WorkspaceService.Initialize()
→ ToolHostService.RegisterBuiltIns()
→ EngineBridge.Initialize()
→ ProjectBrowserViewModel.OpenProject()
→ WorkspaceService.LoadProject("NovaForge")
→ ViewportHostControl.AttachSurface()
→ PlaytestService.EnterEditMode()
```

## Primary rules
- Atlas Suite is the **host shell**, not the engine.
- Engine/editor/runtime boundaries stay separate.
- Viewport hosting must remain replaceable.
- Tool panels register through `ToolHostService`.
- Project switching must route through `WorkspaceService`.
- Play mode transitions must go through `PlaytestService`.

## Suggested next implementation order
1. Compile Atlas Suite shell with docking + placeholder panels.
2. Replace placeholder viewport with real engine surface binding.
3. Implement project open/load for NovaForge.
4. Add play/stop bridge.
5. Add Dev World bootstrap command.
6. Add content browser + inspector binding.
7. Add rig/debug/mission/faction/economy panels.

## Dev World command target

```text
Open NovaForge
→ Load Dev World
→ Spawn Rig
→ Enable test panels
→ Press Play
```

## Panels included in this scaffold
- Content Browser
- Inspector
- World Outliner
- Output Log
- Command Palette
- Debug Panel
- Mission Debug
- Economy Debug
- Faction Debug
- Rig Loadout

## Bridge expectations
The engine bridge should eventually expose:
- initialize/shutdown
- attach viewport surface
- load project
- load world
- start/stop play session
- save/load current state
- execute console/debug command
