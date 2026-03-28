# SHIP + MECH SMOKE TEST

## Goal
Verify the full possession chain in Atlas Suite Dev World.

## Sequence
1. Start Atlas Suite
2. Open NovaForge
3. Load Dev World
4. Spawn rig at default spawn
5. Use interaction key on mech entry point
6. Confirm mech possession state
7. Confirm mech camera/input profile
8. Exit mech
9. Use interaction key on ship cockpit entry
10. Confirm ship possession state
11. Open construct control panel
12. Read cargo/module placeholder state
13. Exit ship
14. Save state
15. Reload state and verify last safe construct/room reference

## Expected results
- no null possession target errors
- no duplicate controller ownership
- clean camera swaps
- clean return to rig state
- save/load restores a valid fallback state if current possession target is unavailable
