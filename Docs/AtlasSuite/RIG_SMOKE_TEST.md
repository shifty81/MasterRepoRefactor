# Rig Smoke Test Sequence

## Goal
Verify the minimum player-facing loop is testable in the executable.

## Sequence
1. Launch Atlas Suite.
2. Open NovaForge.
3. Start Dev World.
4. Spawn player rig at `spawn_core`.
5. Equip default tool in quick slot 1.
6. Interact with rig terminal.
7. Interact with inventory container.
8. Toggle airlock cycle.
9. Enter EVA lane.
10. Interact with salvage crate.
11. Move item into rig container.
12. Save profile.
13. Reload profile.
14. Verify rig state, quick slots, and inventory persisted.

## Pass conditions
- no fatal runtime errors
- interaction prompts appear
- rig state updates are visible
- quick slot activation path works
- inventory transfer path works
- save/reload reproduces expected state
