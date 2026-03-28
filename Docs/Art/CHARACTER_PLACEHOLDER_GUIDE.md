# Character Placeholder Guide

## Why a placeholder?

NovaForge uses a **modular low-poly character system** driven entirely by data files
(`NovaForge/Content/Data/Characters/`).  No character mesh is hardcoded in the engine.

A free low-poly male base is an ideal starting point because:

- It matches the project's established **hybrid voxel + low-poly** art direction.
- It gives every developer a concrete visual to work against immediately.
- It is CC0 (public domain) — no licence restrictions on in-development builds.
- It works directly with the existing `base_humanoid` skeleton.  The bone mapping
  table below shows the standard rename needed when exporting from Blender — this
  one-time rename in Blender (or via a rename script) is all that is required
  before the mesh slots and animation retargeting are fully automatic.

---

## Recommended free asset

| Property | Value |
|---|---|
| **Pack** | Ultimate Low Poly Humans |
| **Author** | Quaternius |
| **Licence** | CC0 (Public Domain) |
| **Download** | https://quaternius.com/packs/ultimatecharacters.html |
| **Alternate** | https://opengameart.org (search: low poly male humanoid) |
| **Preferred format** | glTF 2.0 (`.glb`) |

---

## How to add the asset to your local build

1. Download the pack and locate the male base mesh.
2. Export or convert to `.glb` (glTF 2.0).
3. Place files in:
   ```
   NovaForge/Content/Meshes/Characters/
   ```
4. Rename files to match the IDs in `ASSET_MANIFEST.json`:
   - `free_lowpoly_male_base.glb` — combined mesh for smoke test
   - `mesh_head_lowpoly.glb`
   - `mesh_torso_lowpoly.glb`
   - `mesh_arm_l_lowpoly.glb` / `mesh_arm_r_lowpoly.glb`
   - `mesh_leg_l_lowpoly.glb` / `mesh_leg_r_lowpoly.glb`
   - `mesh_hands_lowpoly.glb`
   - `mesh_feet_lowpoly.glb`
   - `mesh_fps_hands_lowpoly.glb`
   - `mesh_placeholder_shadow_capsule.glb`

> **Note:** All `.glb`, `.fbx`, and `.obj` files are git-ignored in this directory.
> The `ASSET_MANIFEST.json` is the authoritative list of what the engine expects.

---

## Blender import settings

| Setting | Value |
|---|---|
| Scale factor | `1.0` (1 Blender unit = 1 m) |
| Up axis | `Y` |
| Forward axis | `-Z` |
| Smooth normals | `OFF` (flat shading required by art style) |
| Vertex colours | `ON` — bake any material colours to vertex colours |
| Animations | Export with `animation_naming_prefix = placeholder_` |

---

## Skeleton bone name mapping

The project's `base_humanoid` skeleton uses this bone naming convention.
Map the free asset's bones to these names in Blender before export:

| Project bone name | Typical free-asset bone | Description |
|---|---|---|
| `root` | `Root` / `Hips_root` | Root motion bone |
| `pelvis` | `Hips` | Pelvis |
| `spine_01` | `Spine` | Lower spine |
| `spine_02` | `Spine1` | Mid spine |
| `spine_back` | `Spine2` | Upper spine / backpack attach |
| `neck` | `Neck` | Neck |
| `head` | `Head` | Head / helmet socket |
| `upperarm_l` | `LeftArm` | Left upper arm |
| `lowerarm_l` | `LeftForeArm` | Left forearm |
| `hand_l` | `LeftHand` | Left hand / tool socket |
| `upperarm_r` | `RightArm` | Right upper arm |
| `lowerarm_r` | `RightForeArm` | Right forearm |
| `hand_r` | `RightHand` | Right hand / tool socket |
| `thigh_l` | `LeftUpLeg` | Left thigh |
| `calf_l` | `LeftLeg` | Left calf |
| `foot_l` | `LeftFoot` | Left foot |
| `thigh_r` | `RightUpLeg` | Right thigh |
| `calf_r` | `RightLeg` | Right calf |
| `foot_r` | `RightFoot` | Right foot |

---

## How the placeholder wires into the project

```
default_character.character.json
        │
        ▼
placeholder_male_base.json          ← body slot definitions (8 slots)
        │
        ├── placeholder_male_base_rig.json      ← FPS camera & rig attach offsets
        │
        └── placeholder_male_base_anim_map.json ← animation clip ID mapping
                │
                ▼
        character_layers.animation.json         ← layer stack (base/additive/tool/IK)
                │
                ▼
        RigController (C++)  ←→  PlayerRigState (C#)
```

---

## Poly budget

| Part | Max tris |
|---|---|
| Head | 800 |
| Torso | 1 200 |
| Each arm | 500 |
| Each leg | 600 |
| Hands | 400 |
| Feet | 400 |
| **Total body** | **≤ 5 000** |
| FPS hands | 600 |
| Shadow capsule | 64 |
| **Hard ceiling (full rig)** | **6 500** |

This matches the `max_tri_count` enforced by `LowPolyCharacterGenerator`.

---

## When to replace the placeholder

The placeholder is permanent as long as it is flagged `"is_placeholder": true` in
`placeholder_male_base.json`.  Remove that flag (or flip it to `false`) when a
production-quality mesh has been signed off by the art director.

The CI test `test_character_placeholder.py::TestPlaceholderCharacterContent`
validates the JSON data structure — it does **not** require the binary mesh files
to be present (they are git-ignored).  Binary presence is validated at runtime
by the AssetRegistry.
