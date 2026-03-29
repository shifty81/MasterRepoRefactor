# Duplicate Resolution Table

## Shared types likely duplicated across packs

| Type / System | Canonical Destination | Resolution Rule |
|---|---|---|
| DataRegistry | /Source/Data | Merge all loaders into one authoritative version |
| Item/Recipe/Mission/Faction models | /Source/Data | Keep one canonical model set |
| ModuleDefinition | /Source/Data or /Source/Gameplay/Modules | Remove pack-local duplicates |
| GameplayManager-like boot helpers | /Source/Game or /Source/Gameplay | Keep one main runtime gameplay coordinator |
| SaveManager scaffolds | /Source/Save | Merge into one system |
| Season types | /Source/Gameplay/Season | Keep Phase 12.1 version as authority |
| UI state/controller stubs | /Source/UI | Collapse duplicates into one shared UI layer |
| Tooling/dev overlay types | /Source/Editor or /Source/UI | Keep one overlay path |
| Editor selection handle types | /Source/Editor | Single selection model only |
| Camera/controller helpers | /Source/Editor or /Source/Input | Separate editor/gameplay versions cleanly |
| Module/ship/fleet/meta progression types | /Source/Gameplay | Keep latest phase version |
| Titan/endgame/season systems | /Source/Gameplay | Keep latest phase version |

## Resolution rule
Prefer the most recent pack version only when it aligns with the canonical ownership map.
Otherwise merge behavior into the canonical owner and archive the duplicates.
