# PCG

Back: [System Index](./README.md)  
Related: [Builder](./BUILDER.md) · [Runtime + Projects](./RUNTIME_AND_PROJECTS.md)

## Purpose

`PCG/` should own procedural generation rules for universe layout, structures, points of interest, resource fields, wrecks, ruins, mission sites, and content variation.

## Current repo footprint

Detected `PCG/` modules:
- `PCG/Advanced`
- `PCG/Audio`
- `PCG/Biomes`
- `PCG/Cave`
- `PCG/Cities`
- `PCG/Climate`
- `PCG/DeterministicVerifier`
- `PCG/Dungeon`
- `PCG/Geometry`
- `PCG/MapGenerator`
- `PCG/Narrative`
- `PCG/Noise`
- `PCG/Pipeline`
- `PCG/Planet`
- `PCG/Quests`
- `PCG/Rules`
- `PCG/SpaceLayout`
- `PCG/Story`
- `PCG/Structures`
- `PCG/Textures`
- `PCG/Validation`
- `PCG/Vegetation`
- `PCG/Voxel`
- `PCG/Weather`
- `PCG/World`
- `PCG/WorldGenerator`

## PCG role in project direction

```text
Voxel Layer             Low-Poly Layer
-----------             --------------
mass                    silhouettes
terrain / hull volume   panels / modules / props
damage state            readable shape language
mining / salvage        interactable attachments
repair state            visual upgrade expression
```

## Recommended doc subjects
- world seed flow
- structure grammar
- salvage site generation
- faction style sets
- upgrade-driven visual propagation
- deterministic reproduction rules
