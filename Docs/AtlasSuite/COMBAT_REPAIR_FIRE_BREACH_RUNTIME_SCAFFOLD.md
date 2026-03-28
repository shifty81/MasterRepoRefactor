# Combat + Repair + Fire/Breach Runtime Scaffold

## Purpose
This scaffold provides the minimum runtime structure to test:
- combat damage application
- hit zone routing
- breach creation and sealing
- fire start/spread/extinguish flow
- repair actions
- Dev World smoke-test execution
- Atlas Suite debug panel visibility

## Runtime loop
Atlas Suite
→ Dev World
→ spawn rig / mech / ship test targets
→ apply damage profile
→ route damage to zone / part / module
→ trigger breach or fire state
→ respond with repair tools/actions
→ verify state mutation
→ save/reload state

## Included areas
- damage profiles
- combat state service
- breach service
- fire service
- repair action service
- smoke test service
- debug panels
- playtest command

## Integration notes
Wire these services into:
- InteractionService
- BuilderPlacementService / validation
- PossessionService
- Mission runtime
- Save/load transaction pipeline
- Faction/economy incident hooks
