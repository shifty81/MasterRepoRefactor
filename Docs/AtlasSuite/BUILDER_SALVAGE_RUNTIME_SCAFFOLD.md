# BUILDER + SALVAGE RUNTIME SCAFFOLD

## Purpose
This scaffold finishes the next playable chain inside Atlas Suite:

```text
Atlas Suite
→ Dev World
→ Spawn rig
→ enter builder mode
→ place part ghost
→ validate placement
→ weld/finalize
→ apply damage
→ mark salvage target
→ cut/detach part
→ recover loot into container
```

## Scope
This pack provides:
- builder placement contracts
- ghost placement service
- snap profile support
- weld/finalize flow
- construct validation stub
- damage + salvage mark flow
- cut/detach flow
- salvage recovery stubs
- WPF debug panels for builder and salvage
- Dev World smoke-test service

## Runtime goals
The scaffold should support these first runtime actions:
1. Load a starter construct definition in Dev World
2. Enter builder placement mode
3. Preview and place a hull plate or utility part
4. Run validation pass
5. Weld/finalize the part
6. Apply test damage to the part
7. Mark the part for salvage
8. Cut/detach the part
9. Generate a salvage recovery record
10. Move the recovered item into a test container

## Design rules
- Builder remains data-driven
- Parts are structural, modules are functional
- Placement is not final until welded
- Validation is multi-pass and explicit
- Salvage uses real construct records, not fake loot-only props
- Recovery outputs should be deterministic from part state where possible

## Suggested integration order
1. Wire `BuilderPlaytestCommand` into Atlas Suite playtest menu
2. Register `BuilderPlacementService` and `SalvageRuntimeService`
3. Load `dev_builder_salvage_construct.json` in Dev World
4. Connect builder/salvage debug panels to live runtime services
5. Replace placeholder validation rules with real construct checks
6. Route salvage outputs into real inventory/container systems
