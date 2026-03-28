# SHIP + MECH POSSESSION SCAFFOLD

## Purpose
This pack adds the next executable-ready bridge in Atlas Suite:

Rig -> EVA -> Mech -> Ship

It provides starter runtime contracts and WPF panel stubs for:
- construct registration
- seat/entry points
- possession transitions
- mech enter/exit flow
- ship cockpit enter/exit flow
- cargo/module access hooks
- Dev World smoke testing

## Intended flow
1. Spawn player rig in Dev World
2. Approach mech bay
3. Interact with mech entry point
4. Transfer control to mech pawn/controller
5. Exit mech back to rig
6. Approach ship cockpit
7. Transfer control to ship pilot state
8. Open cargo/module test panel
9. Save and restore possession state

## Required real integrations
- engine-side pawn/controller possession bridge
- camera mode switching
- input context switching
- animation state routing
- construct/module runtime state hooks
- save/load persistence wiring

## Done when
- player can enter and exit mech
- player can enter and exit ship
- possession state survives playtest loop
- basic cargo/module interactions are exposed in Dev World
