# Character and Rig System

The in-game wearable player system is called the **rig**.

## Rig definition

Rig = space suit + backpack assembly.

## Core slots

- `slot_rig_helmet`
- `slot_rig_torso`
- `slot_rig_gloves`
- `slot_rig_boots`
- `slot_rig_pack`
- `slot_tool_primary`

## Core goals

- Full body first-person awareness
- Modular equippable visuals
- Stat-bearing gear
- EVA readiness validation

## Core loop

```text
Equip rig
 -> aggregate stats and capability flags
 -> validate EVA/tool readiness
 -> rebuild character visuals
```

## Key related docs
- [Equipment and Stat Modifier System](Equipment_and_Stat_Modifier_System.md)
- [Global State Input Interaction](Global_State_Input_Interaction.md)
- [EVA Airlock and Tether System](EVA_Airlock_Tether_System.md)
