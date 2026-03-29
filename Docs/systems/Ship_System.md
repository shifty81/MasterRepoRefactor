# Ship System

Ships are both vehicles and mobile bases.

## Core features

- Modular shell assembly
- Interior linkage through `Socket_InteriorRoot`
- Pilot seat control
- EVA integration
- Mech bay support

## Ship core loop

```text
Board ship
 -> sit in pilot seat
 -> gain ship control
 -> travel
 -> stop / stabilize
 -> exit seat
```

## Minimum modules

- cockpit
- cargo bay
- ramp
- airlock
- engine
- interior link anchor

## Related docs
- [Ship Control and Navigation](Ship_Control_and_Navigation.md)
- [EVA Airlock and Tether System](EVA_Airlock_Tether_System.md)
- [PCG and Asset Generation](PCG_and_Asset_Generation.md)
