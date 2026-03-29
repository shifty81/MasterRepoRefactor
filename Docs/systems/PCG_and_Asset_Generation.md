# PCG and Asset Generation

## Core rule

Geometry and materials should be as procedural as practical, but always validated.

## Asset generation chain

```text
Schema
 -> payload
 -> Blender generation
 -> export
 -> import
 -> registry
 -> runtime assembly
```

## Generation targets

- interiors
- ships
- mechs
- character cosmetics
- later: props, wrecks, structures
