# Consolidation Steps

## Step 1
Create the unified folder structure.

## Step 2
Import every generated pack into `/Archive/ImportedPacks/` first.

## Step 3
For each subsystem:
- compare duplicate files
- choose canonical owner
- merge into canonical destination
- archive rejected duplicates

## Step 4
Unify build targets into one executable:
- MasterRepoEditorRuntime

## Step 5
Replace phase-local entry points with one boot path.

## Step 6
Run a compile pass.

## Step 7
Run a subsystem smoke test:
- data load
- world boot
- gameplay boot
- editor boot
- save/load shell
- UI shell

## Step 8
Start implementing missing critical gaps:
- real input
- rendering
- save/load
- voxel editor
- system hookups
