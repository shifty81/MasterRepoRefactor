# Rig + Interaction Runtime Scaffold

## Purpose
This pack provides a repo-ready skeleton for the first playable **rig + interaction** loop inside Atlas Suite and NovaForge.

## Scope
- rig bootstrap and state container
- first-person interaction service contracts
- airlock/terminal/container interaction stubs
- quick-slot and equipment state wiring
- playable smoke-test sequence
- WPF playtest integration hook

## Immediate integration target
```text
Atlas Suite
→ Dev World Play
→ Spawn rig
→ Equip starter loadout
→ Interact with terminal
→ Open airlock
→ Enter EVA test lane
→ Loot container
→ Save/Reload
```

## Recommended wiring order
1. `RigBootstrapService` into existing Dev World bootstrap.
2. `PlayerRigState` into your real player runtime state.
3. `InteractionService` into trace/collision/interactable components.
4. `QuickSlotService` into inventory/equipment UI.
5. `RigSmokeTestService` into Atlas Suite Playtest debug command.

## Notes
- Keep the rig as the canonical player suit/backpack assembly.
- Keep JSON/config as the authoritative data surface where practical.
- Keep Atlas Suite as the host shell, not the gameplay owner.
