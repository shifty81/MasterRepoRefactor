# Mech System

Mechs are modular, stateful assemblies that extend the player's capabilities.

## Core concepts

- Entered through a transition from on-foot state
- Modular parts attached to sockets
- Tier-gated progression
- Supports repair, salvage, lifting, and exterior work

## Basic state flow

```text
OnFoot
 -> EnterMech transition
 -> InMech
 -> ExitMech transition
 -> OnFoot
```

## MVP priorities

- Salvage Walker T1
- Parked proxy in mech bay
- Promotion to full mech on interaction
- Tool mount support

## Related docs
- [Ship System](Ship_System.md)
- [EVA Airlock and Tether System](EVA_Airlock_Tether_System.md)
- [Equipment and Stat Modifier System](Equipment_and_Stat_Modifier_System.md)
