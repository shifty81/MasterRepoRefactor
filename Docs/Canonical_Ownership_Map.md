# Canonical Ownership Map

## Core
- GameOrchestrator -> /Source/Core
- App / Engine bootstrap -> /Source/Core
- IntegrationCoordinator -> /Source/Game or /Source/Core

## World
- World / SystemScheduler -> /Source/World
- StructureRegistry / VoxelSubsystem -> /Source/World or /Source/Gameplay/Voxel if later split

## Data
- DataRegistry -> /Source/Data
- all shared definition structs -> /Source/Data

## Rendering
- Renderer / debug draw / viewport -> /Source/Rendering

## Input
- gameplay input context -> /Source/Input
- editor input context -> /Source/Editor or /Source/Input

## Editor
- editor mode controller
- outliner
- inspector
- gizmos
- voxel tools
- PCG editor tools

## Gameplay
- gameplay loops and domain systems only
- no shared core/data boot code here

## Save
- SaveManager
- domain adapters
- migration/version handling

## UI
- runtime UI
- editor panel UI bridge
- shared widget/model layer if needed

## Archive
- all legacy or superseded pack content
- never treated as live canonical source
