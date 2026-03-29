# EVA Airlock and Tether System

EVA is a continuation of the player's character state, not a separate avatar.

## Core flow

```text
Interior traversal
 -> enter airlock
 -> cycle to vacuum
 -> exit to EVA
 -> tether attaches to ship
 -> perform exterior work
 -> return to airlock
 -> cycle to pressurized
 -> re-enter interior
```

## Core subsystems

- EVA runtime subsystem
- airlock runtime component
- tether runtime component
- EVA state component
- EVA safety component
- EVA interaction component

## First slice rules

- same player actor throughout
- tether auto-attaches on exit
- ship acts as oxygen / tether / return source
