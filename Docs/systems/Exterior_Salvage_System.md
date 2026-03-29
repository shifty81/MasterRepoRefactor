# Exterior Salvage System

Exterior work is stateful, tool-gated, and modular.

## Target categories

- repair panel
- salvage panel
- cut seam
- detachable module

## First loop

```text
EVA out
 -> repair panel
 -> cut seam
 -> salvage panel
 -> detach module
 -> loot outcome
 -> return to ship
```

## Required tool tags

- `repair_tool`
- `cut_tool`
- `salvage_tool`
