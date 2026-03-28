# Expected Result — AtlasSuite Pack Migration

After integrating the five AtlasSuite zip packs you should have:

## Atlas/UI/AtlasSuite/ — Editor Shell
- `App/` — WPF application entry point (`App.xaml`, `App.xaml.cs`)
- `Shell/` — Main window XAML and code-behind
- `Workspace/` — Workspace service
- `ProjectBrowser/` — Project browser service
- `Docking/` — Dock layout service
- `ViewportHost/` — Viewport host control
- `PlaytestHost/` — Playtest commands for DevWorld, Rig, Vehicle, and Builder modes
- `ToolHost/` — Tool host service
- `Integration/` — Engine bridge
- `Panels/RigLoadout/` — Rig loadout panel
- `Panels/ConstructControl/` — Construct control panel
- `Panels/BuilderDebug/` — Builder debug panel
- `Panels/SalvageDebug/` — Salvage debug panel

## NovaForge/Runtime/ — Game Systems
- `DevWorld/` — Bootstrap, registry, scene definition, terminals, entities, smoke-test services
- `Player/` — Player spawn interface, rig state, rig bootstrap service
- `Interaction/` — Interactable interface, interaction service, airlock and loot interactables
- `Inventory/` — Inventory debug service, quickslot service
- `Missions/` — Mission service interface
- `Economy/` — Economy debug service interface
- `Factions/` — Faction debug service interface
- `SaveLoad/` — Save/load service interface, rig save state
- `Constructs/` — Construct record, construct service interfaces
- `Combat/` — Combat test service interface
- `Salvage/` — Salvage test and runtime services, recovery record
- `Vehicles/` — Possession state/service, mech entry/exit, ship cockpit/exit, construct control
- `Builder/` — Placement service, placement record/state/preview, validation service, salvage marking

## NovaForge/Content/ — Project Data
- `Scenes/` — `dev_world.scene.json`
- `Config/` — `dev_world.json`, `dev_world_constructs.json`, `rig_default_loadout.json`, `dev_builder_salvage.json`
- `Data/Missions/` — `mission_dev_salvage_intro.json`
- `Data/Constructs/` — `dev_mech_mk1.json`, `dev_ship_starter.json`
- `Data/Interactables/` — `dev_world_airlock_terminal.json`
- `Data/Builder/` — builder construct and hull-plate definitions
- `Data/Salvage/` — salvage recovery data

## Docs/AtlasSuite/
- Nine scaffold and smoke-test markdown documents covering all migrated systems
- `README.md` index of all documents

## Archive
- All five source zip files moved to `Docs/Archive/ZipFiles/`
- Chat export text files moved to `Docs/Archive/Chats/`
