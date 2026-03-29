# Master Repo Documentation Index

This is the primary entry point for the repo documentation set.

## Core documents

- [Project Vision](Project_Vision.md)
- [Core Runtime Framework](Core_Runtime_Framework.md)
- [Implementation Roadmap](Implementation_Roadmap.md)
- [Compliance Rules](Compliance_Rules.md)
- [Known Gaps and Risks](Known_Gaps_and_Risks.md)

## Gameplay systems

- [Character and Rig System](systems/Character_and_Rig_System.md)
- [Mech System](systems/Mech_System.md)
- [Ship System](systems/Ship_System.md)
- [EVA Airlock and Tether System](systems/EVA_Airlock_Tether_System.md)
- [Exterior Salvage System](systems/Exterior_Salvage_System.md)
- [Derelict Runtime System](systems/Derelict_Runtime_System.md)
- [Progression Economy and Loot](systems/Progression_Economy_Loot.md)
- [Skill System and Time Progression](systems/Skill_System.md)
- [Faction Mission Contract System](systems/Faction_Mission_Contract_System.md)
- [Sector Simulation and Living Universe](systems/Sector_Simulation_and_Living_Universe.md)
- [Titan and Seasonal Loop](systems/Titan_and_Seasonal_Loop.md)

## Tooling and pipeline

- [PCG and Asset Generation](systems/PCG_and_Asset_Generation.md)
- [Blender Integration](systems/Blender_Integration.md)
- [Arbiter Tooling Layer](systems/Arbiter_Tooling_Layer.md)

## Global framework glue

- [Global State Input and Interaction](systems/Global_State_Input_Interaction.md)
- [Equipment and Stat Modifier System](systems/Equipment_and_Stat_Modifier_System.md)
- [Ship Control and Navigation](systems/Ship_Control_and_Navigation.md)

## Quick loop diagram

```text
Spawn
 -> Equip Rig
 -> Board Ship
 -> Pilot
 -> EVA
 -> Salvage / Repair
 -> Return
 -> Craft / Upgrade
 -> Complete Mission
 -> Progress to harder sectors
 -> Build toward Titan endgame
```
