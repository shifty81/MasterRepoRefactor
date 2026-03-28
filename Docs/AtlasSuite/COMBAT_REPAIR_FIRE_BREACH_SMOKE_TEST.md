# Combat + Repair + Fire/Breach Smoke Test

## Test sequence
1. Load Dev World
2. Spawn rig and baseline target construct
3. Apply kinetic damage to hull plate
4. Confirm damage routed to target zone
5. Trigger breach state
6. Trigger localized fire state
7. Use breach patch action
8. Use fire suppression action
9. Use repair restore action
10. Save and reload
11. Confirm state persistence

## Expected outcomes
- damage event emitted
- part/module state changed
- breach visible in debug service state
- fire visible in debug service state
- repair actions reduce or clear hazard states
- save/load restores resulting state correctly
