# DEV WORLD TEST SEQUENCE

## Target Smoke Test
```text
spawn rig
→ equip starter cutter
→ open airlock
→ enter EVA lane
→ return through airlock
→ enter mech
→ exit mech
→ board starter ship
→ open builder pad
→ place starter hull plate
→ validate construct
→ shoot target dummy
→ salvage detached part
→ move loot into container
→ accept starter mission
→ complete starter mission
→ save profile
→ reload profile
```

## Validation Expectations
- no fatal errors in Output Log
- player state persists across save/load
- inventory changes persist
- construct placement persists
- mission state writes back cleanly
