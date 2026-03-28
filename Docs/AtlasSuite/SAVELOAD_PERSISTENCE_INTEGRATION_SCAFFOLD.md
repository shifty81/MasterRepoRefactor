# Save/Load + Persistence Integration Scaffold

## Purpose
This scaffold ties the existing Atlas Suite / NovaForge vertical-slice packs into
one persistence pipeline so Dev World state can be captured, restored, validated,
and debugged through a common save/load integration layer.

## Goals
- define a shared save manifest
- register subsystem persistence contributors
- support snapshot save/load
- support deterministic Dev World restore
- expose persistence status to Atlas Suite debug panels
- provide smoke-test orchestration

## Covered subsystem lanes
- rig / interaction
- ship + mech possession
- builder + salvage
- mission runtime
- economy state
- faction standing / events
- combat / breach / fire / repair

## Integration flow
Atlas Suite
→ open Dev World
→ gather persistence contributors
→ build save manifest
→ write snapshot
→ clear/reboot runtime
→ reload snapshot
→ validate subsystem restoration
→ surface result in debug UI

## Notes
This scaffold intentionally uses simple JSON snapshot records first.
Delta journals, migrations, archive tiers, and rollback layers can be added later
on top of this baseline.
