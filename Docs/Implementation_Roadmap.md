# Implementation Roadmap

See also:
- [Project Vision](Project_Vision.md)
- [Compliance Rules](Compliance_Rules.md)
- [Known Gaps and Risks](Known_Gaps_and_Risks.md)

## Golden rule

If code exists but does not match Master Repo standards, refactor it before relying on it.

## Strict build order

### Phase 1: Core foundation
- Global state
- Input routing
- Interaction framework
- Debug overlay

### Phase 2: Character and rig
- Character controller
- Rig slots
- Equipment and stat modifiers
- EVA readiness checks

### Phase 3: Ship core loop
- Ship actor
- Seat control
- Ship movement
- Stabilization
- Boarding flow

### Phase 4: EVA
- Airlock
- Tether
- EVA movement
- Return flow

### Phase 5: Salvage
- Repair targets
- Cut seams
- Salvage nodes
- Loot drops

### Phase 6: Inventory and crafting
- Resource inventory
- Crafting recipes
- Upgrade outputs

### Phase 7: Progression and tiers
- Unified tier system
- Skill-gated unlocks
- Upgrade propagation

### Phase 8: Missions
- Contracts
- Objective runtime
- Rewards and reputation

### Phase 9: Sectors and travel
- Sector state
- Spawn director
- Travel between sectors

### Phase 10: Endgame
- Titan construction
- Seasonal collapse
- Legacy rewards

## Vertical slice success criteria

```text
Spawn
 -> Equip Rig
 -> Board Ship
 -> Pilot
 -> EVA
 -> Salvage
 -> Return
 -> Craft
 -> Upgrade
 -> Complete Mission
```
