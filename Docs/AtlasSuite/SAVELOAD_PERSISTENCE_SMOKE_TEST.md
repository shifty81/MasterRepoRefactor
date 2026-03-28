# Save/Load + Persistence Smoke Test

## Test sequence
1. Load Atlas Suite Dev World
2. Spawn rig and equip default loadout
3. Enter mech and exit
4. Enter ship and exit
5. Place and weld builder part
6. Mark/cut/recover one salvage target
7. Accept and complete one dev mission
8. Apply one economy mutation and one faction standing change
9. Apply combat damage, create breach, ignite fire, then repair
10. Save snapshot
11. Reset runtime
12. Reload snapshot
13. Validate restored state in debug panels

## Expected outcomes
- one save manifest created
- all registered contributors serialized
- runtime restored without missing records
- debug panel displays contributor statuses
- smoke test reports pass/fail by subsystem
