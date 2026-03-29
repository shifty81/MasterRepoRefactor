# Blender Integration

Blender acts as a procedural asset compiler.

## Job flow

```text
Arbiter request
 -> payload build
 -> queue job
 -> run Blender headless
 -> export FBX/GLTF + metadata
 -> import
 -> register
 -> validate
```

## Core scripts

- `generate_interior.py`
- `generate_ship.py`
- `generate_mech.py`
- `generate_character.py`
