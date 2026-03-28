"""Tests for AtlasSuite runtime systems migrated from the five zip packs.

Checks that all key files landed in their canonical repo locations.
"""

import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _p(rel: str) -> Path:
    return REPO_ROOT / rel


# ---------------------------------------------------------------------------
# Atlas UI — Shell & App
# ---------------------------------------------------------------------------

class TestAtlasSuiteUIShell:
    def test_app_xaml(self):
        assert _p("Atlas/UI/AtlasSuite/App/App.xaml").exists()

    def test_app_xaml_cs(self):
        assert _p("Atlas/UI/AtlasSuite/App/App.xaml.cs").exists()

    def test_main_window_xaml(self):
        assert _p("Atlas/UI/AtlasSuite/Shell/MainWindow.xaml").exists()

    def test_main_window_cs(self):
        assert _p("Atlas/UI/AtlasSuite/Shell/MainWindow.xaml.cs").exists()

    def test_workspace_service(self):
        assert _p("Atlas/UI/AtlasSuite/Workspace/WorkspaceService.cs").exists()

    def test_project_browser_service(self):
        assert _p("Atlas/UI/AtlasSuite/ProjectBrowser/ProjectBrowserService.cs").exists()

    def test_dock_layout_service(self):
        assert _p("Atlas/UI/AtlasSuite/Docking/DockLayoutService.cs").exists()

    def test_tool_host_service(self):
        assert _p("Atlas/UI/AtlasSuite/ToolHost/ToolHostService.cs").exists()

    def test_engine_bridge(self):
        assert _p("Atlas/UI/AtlasSuite/Integration/EngineBridge.cs").exists()

    def test_viewport_host_xaml(self):
        assert _p("Atlas/UI/AtlasSuite/ViewportHost/ViewportHostControl.xaml").exists()


# ---------------------------------------------------------------------------
# Atlas UI — PlaytestHost commands
# ---------------------------------------------------------------------------

class TestAtlasSuitePlaytestHost:
    def test_playtest_service(self):
        assert _p("Atlas/UI/AtlasSuite/PlaytestHost/PlaytestService.cs").exists()

    def test_devworld_play_command(self):
        assert _p("Atlas/UI/AtlasSuite/PlaytestHost/DevWorldPlayCommand.cs").exists()

    def test_rig_playtest_command(self):
        assert _p("Atlas/UI/AtlasSuite/PlaytestHost/RigPlaytestCommand.cs").exists()

    def test_vehicle_playtest_command(self):
        assert _p("Atlas/UI/AtlasSuite/PlaytestHost/VehiclePlaytestCommand.cs").exists()

    def test_builder_playtest_command(self):
        assert _p("Atlas/UI/AtlasSuite/PlaytestHost/BuilderPlaytestCommand.cs").exists()


# ---------------------------------------------------------------------------
# Atlas UI — Panels
# ---------------------------------------------------------------------------

class TestAtlasSuiteUIPanels:
    def test_rig_loadout_panel_xaml(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/RigLoadout/RigLoadoutPanel.xaml").exists()

    def test_rig_loadout_panel_cs(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/RigLoadout/RigLoadoutPanel.xaml.cs").exists()

    def test_construct_control_panel_xaml(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/ConstructControl/ConstructControlPanel.xaml").exists()

    def test_builder_debug_panel_xaml(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/BuilderDebug/BuilderDebugPanel.xaml").exists()

    def test_salvage_debug_panel_xaml(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/SalvageDebug/SalvageDebugPanel.xaml").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — DevWorld
# ---------------------------------------------------------------------------

class TestNovaForgeDevWorld:
    def test_devworld_bootstrap(self):
        assert _p("NovaForge/Runtime/DevWorld/DevWorldBootstrap.cs").exists()

    def test_devworld_registry(self):
        assert _p("NovaForge/Runtime/DevWorld/DevWorldRegistry.cs").exists()

    def test_devworld_scene_definition(self):
        assert _p("NovaForge/Runtime/DevWorld/DevWorldSceneDefinition.cs").exists()

    def test_idev_terminal(self):
        assert _p("NovaForge/Runtime/DevWorld/Terminals/IDevTerminal.cs").exists()

    def test_rig_loadout_terminal(self):
        assert _p("NovaForge/Runtime/DevWorld/Terminals/RigLoadoutTerminal.cs").exists()

    def test_inventory_crafting_terminal(self):
        assert _p("NovaForge/Runtime/DevWorld/Terminals/InventoryCraftingTerminal.cs").exists()

    def test_mission_board_terminal(self):
        assert _p("NovaForge/Runtime/DevWorld/Terminals/MissionBoardTerminal.cs").exists()

    def test_economy_debug_terminal(self):
        assert _p("NovaForge/Runtime/DevWorld/Terminals/EconomyDebugTerminal.cs").exists()

    def test_faction_debug_terminal(self):
        assert _p("NovaForge/Runtime/DevWorld/Terminals/FactionDebugTerminal.cs").exists()

    def test_save_checkpoint_terminal(self):
        assert _p("NovaForge/Runtime/DevWorld/Terminals/SaveCheckpointTerminal.cs").exists()

    def test_starter_ship_spawner(self):
        assert _p("NovaForge/Runtime/DevWorld/Entities/StarterShipSpawner.cs").exists()

    def test_starter_mech_spawner(self):
        assert _p("NovaForge/Runtime/DevWorld/Entities/StarterMechSpawner.cs").exists()

    def test_combat_dummy_spawner(self):
        assert _p("NovaForge/Runtime/DevWorld/Entities/CombatDummySpawner.cs").exists()

    def test_salvage_wreck_spawner(self):
        assert _p("NovaForge/Runtime/DevWorld/Entities/SalvageWreckSpawner.cs").exists()

    def test_devworld_smoke_test_service(self):
        assert _p("NovaForge/Runtime/DevWorld/Services/DevWorldSmokeTestService.cs").exists()

    def test_rig_smoke_test_service(self):
        assert _p("NovaForge/Runtime/DevWorld/Services/RigSmokeTestService.cs").exists()

    def test_vehicle_smoke_test_service(self):
        assert _p("NovaForge/Runtime/DevWorld/Services/VehicleSmokeTestService.cs").exists()

    def test_builder_salvage_smoke_test_service(self):
        assert _p("NovaForge/Runtime/DevWorld/Services/BuilderSalvageSmokeTestService.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — Player & Interaction
# ---------------------------------------------------------------------------

class TestNovaForgePlayerInteraction:
    def test_iplayer_spawn_service(self):
        assert _p("NovaForge/Runtime/Player/IPlayerSpawnService.cs").exists()

    def test_player_rig_state(self):
        assert _p("NovaForge/Runtime/Player/PlayerRigState.cs").exists()

    def test_rig_bootstrap_service(self):
        assert _p("NovaForge/Runtime/Player/RigBootstrapService.cs").exists()

    def test_iinteractable(self):
        assert _p("NovaForge/Runtime/Interaction/IInteractable.cs").exists()

    def test_interaction_service(self):
        assert _p("NovaForge/Runtime/Interaction/InteractionService.cs").exists()

    def test_airlock_terminal_interactable(self):
        assert _p("NovaForge/Runtime/Interaction/AirlockTerminalInteractable.cs").exists()

    def test_loot_container_interactable(self):
        assert _p("NovaForge/Runtime/Interaction/LootContainerInteractable.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — Inventory, SaveLoad, Economy, Factions, Missions
# ---------------------------------------------------------------------------

class TestNovaForgeInventorySaveLoadServices:
    def test_iinventory_debug_service(self):
        assert _p("NovaForge/Runtime/Inventory/IInventoryDebugService.cs").exists()

    def test_quickslot_service(self):
        assert _p("NovaForge/Runtime/Inventory/QuickSlotService.cs").exists()

    def test_isave_load_service(self):
        assert _p("NovaForge/Runtime/SaveLoad/ISaveLoadService.cs").exists()

    def test_rig_save_state(self):
        assert _p("NovaForge/Runtime/SaveLoad/RigSaveState.cs").exists()

    def test_ieconomy_debug_service(self):
        assert _p("NovaForge/Runtime/Economy/IEconomyDebugService.cs").exists()

    def test_ifaction_debug_service(self):
        assert _p("NovaForge/Runtime/Factions/IFactionDebugService.cs").exists()

    def test_imission_service(self):
        assert _p("NovaForge/Runtime/Missions/IMissionService.cs").exists()

    def test_icombat_test_service(self):
        assert _p("NovaForge/Runtime/Combat/ICombatTestService.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — Constructs & Vehicles
# ---------------------------------------------------------------------------

class TestNovaForgeConstructsVehicles:
    def test_construct_record(self):
        assert _p("NovaForge/Runtime/Constructs/ConstructRecord.cs").exists()

    def test_iconstruct_service(self):
        assert _p("NovaForge/Runtime/Constructs/IConstructService.cs").exists()

    def test_iconstruct_spawn_service(self):
        assert _p("NovaForge/Runtime/Constructs/IConstructSpawnService.cs").exists()

    def test_possession_state(self):
        assert _p("NovaForge/Runtime/Vehicles/PossessionState.cs").exists()

    def test_ipossession_service(self):
        assert _p("NovaForge/Runtime/Vehicles/IPossessionService.cs").exists()

    def test_possession_service(self):
        assert _p("NovaForge/Runtime/Vehicles/PossessionService.cs").exists()

    def test_mech_entry_interactable(self):
        assert _p("NovaForge/Runtime/Vehicles/Mech/MechEntryInteractable.cs").exists()

    def test_mech_exit_service(self):
        assert _p("NovaForge/Runtime/Vehicles/Mech/MechExitService.cs").exists()

    def test_ship_cockpit_interactable(self):
        assert _p("NovaForge/Runtime/Vehicles/Ship/ShipCockpitInteractable.cs").exists()

    def test_ship_exit_service(self):
        assert _p("NovaForge/Runtime/Vehicles/Ship/ShipExitService.cs").exists()

    def test_construct_control_service(self):
        assert _p("NovaForge/Runtime/Vehicles/Ship/ConstructControlService.cs").exists()

    def test_construct_control_snapshot(self):
        assert _p("NovaForge/Runtime/Vehicles/Ship/ConstructControlSnapshot.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — Builder & Salvage
# ---------------------------------------------------------------------------

class TestNovaForgeBuilderSalvage:
    def test_builder_placement_service(self):
        assert _p("NovaForge/Runtime/Builder/BuilderPlacementService.cs").exists()

    def test_ibuilder_placement_service(self):
        assert _p("NovaForge/Runtime/Builder/IBuilderPlacementService.cs").exists()

    def test_placement_state(self):
        assert _p("NovaForge/Runtime/Builder/Placement/PlacementState.cs").exists()

    def test_builder_placement_record(self):
        assert _p("NovaForge/Runtime/Builder/Placement/BuilderPlacementRecord.cs").exists()

    def test_placement_preview_result(self):
        assert _p("NovaForge/Runtime/Builder/Placement/PlacementPreviewResult.cs").exists()

    def test_validation_severity(self):
        assert _p("NovaForge/Runtime/Builder/Validation/ValidationSeverity.cs").exists()

    def test_validation_result(self):
        assert _p("NovaForge/Runtime/Builder/Validation/ValidationResult.cs").exists()

    def test_iconstruct_validation_service(self):
        assert _p("NovaForge/Runtime/Builder/Validation/IConstructValidationService.cs").exists()

    def test_construct_validation_service(self):
        assert _p("NovaForge/Runtime/Builder/Validation/ConstructValidationService.cs").exists()

    def test_salvage_mark_state(self):
        assert _p("NovaForge/Runtime/Builder/Salvage/SalvageMarkState.cs").exists()

    def test_salvage_target_record(self):
        assert _p("NovaForge/Runtime/Builder/Salvage/SalvageTargetRecord.cs").exists()

    def test_isalvage_runtime_service(self):
        assert _p("NovaForge/Runtime/Salvage/ISalvageRuntimeService.cs").exists()

    def test_isalvage_test_service(self):
        assert _p("NovaForge/Runtime/Salvage/ISalvageTestService.cs").exists()

    def test_salvage_runtime_service(self):
        assert _p("NovaForge/Runtime/Salvage/SalvageRuntimeService.cs").exists()

    def test_salvage_recovery_record(self):
        assert _p("NovaForge/Runtime/Salvage/SalvageRecoveryRecord.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Content
# ---------------------------------------------------------------------------

class TestNovaForgeContent:
    def test_dev_world_scene(self):
        assert _p("NovaForge/Content/Scenes/dev_world.scene.json").exists()

    def test_dev_world_config(self):
        assert _p("NovaForge/Content/Config/dev_world.json").exists()

    def test_dev_world_constructs_config(self):
        assert _p("NovaForge/Content/Config/dev_world_constructs.json").exists()

    def test_rig_default_loadout_config(self):
        assert _p("NovaForge/Content/Config/rig_default_loadout.json").exists()

    def test_dev_builder_salvage_config(self):
        assert _p("NovaForge/Content/Config/dev_builder_salvage.json").exists()

    def test_mission_dev_salvage_intro(self):
        assert _p("NovaForge/Content/Data/Missions/mission_dev_salvage_intro.json").exists()

    def test_dev_mech_mk1(self):
        assert _p("NovaForge/Content/Data/Constructs/dev_mech_mk1.json").exists()

    def test_dev_ship_starter(self):
        assert _p("NovaForge/Content/Data/Constructs/dev_ship_starter.json").exists()

    def test_airlock_terminal_data(self):
        assert _p("NovaForge/Content/Data/Interactables/dev_world_airlock_terminal.json").exists()

    def test_builder_construct_data(self):
        assert _p("NovaForge/Content/Data/Builder/dev_builder_salvage_construct.json").exists()

    def test_hull_plate_part_data(self):
        assert _p("NovaForge/Content/Data/Builder/part_hull_plate_mk1_a.json").exists()

    def test_salvage_recovery_data(self):
        assert _p("NovaForge/Content/Data/Salvage/recovery_hull_plate_mk1_a.json").exists()


# ---------------------------------------------------------------------------
# Docs/AtlasSuite
# ---------------------------------------------------------------------------

class TestAtlasSuiteDocs:
    def test_readme_index(self):
        assert _p("Docs/AtlasSuite/README.md").exists()

    def test_atlas_suite_scaffold_md(self):
        assert _p("Docs/AtlasSuite/ATLAS_SUITE_SCAFFOLD.md").exists()

    def test_dev_world_bootstrap_md(self):
        assert _p("Docs/AtlasSuite/DEV_WORLD_BOOTSTRAP.md").exists()

    def test_dev_world_runtime_scaffold_md(self):
        assert _p("Docs/AtlasSuite/DEV_WORLD_RUNTIME_SCAFFOLD.md").exists()

    def test_dev_world_test_sequence_md(self):
        assert _p("Docs/AtlasSuite/DEV_WORLD_TEST_SEQUENCE.md").exists()

    def test_rig_interaction_scaffold_md(self):
        assert _p("Docs/AtlasSuite/RIG_INTERACTION_SCAFFOLD.md").exists()

    def test_rig_smoke_test_md(self):
        assert _p("Docs/AtlasSuite/RIG_SMOKE_TEST.md").exists()

    def test_ship_mech_scaffold_md(self):
        assert _p("Docs/AtlasSuite/SHIP_MECH_POSSESSION_SCAFFOLD.md").exists()

    def test_ship_mech_smoke_test_md(self):
        assert _p("Docs/AtlasSuite/SHIP_MECH_SMOKE_TEST.md").exists()

    def test_builder_salvage_scaffold_md(self):
        assert _p("Docs/AtlasSuite/BUILDER_SALVAGE_RUNTIME_SCAFFOLD.md").exists()

    def test_builder_salvage_smoke_test_md(self):
        assert _p("Docs/AtlasSuite/BUILDER_SALVAGE_SMOKE_TEST.md").exists()

    def test_combat_repair_fire_breach_scaffold_md(self):
        assert _p("Docs/AtlasSuite/COMBAT_REPAIR_FIRE_BREACH_RUNTIME_SCAFFOLD.md").exists()

    def test_combat_repair_fire_breach_smoke_test_md(self):
        assert _p("Docs/AtlasSuite/COMBAT_REPAIR_FIRE_BREACH_SMOKE_TEST.md").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — Combat (extended)
# ---------------------------------------------------------------------------

class TestNovaForgeCombatExtended:
    def test_damage_profile(self):
        assert _p("NovaForge/Runtime/Combat/DamageProfile.cs").exists()

    def test_combat_event_record(self):
        assert _p("NovaForge/Runtime/Combat/CombatEventRecord.cs").exists()

    def test_icombat_state_service(self):
        assert _p("NovaForge/Runtime/Combat/ICombatStateService.cs").exists()

    def test_combat_state_service(self):
        assert _p("NovaForge/Runtime/Combat/CombatStateService.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — Hazards
# ---------------------------------------------------------------------------

class TestNovaForgeHazards:
    def test_breach_state(self):
        assert _p("NovaForge/Runtime/Hazards/Breach/BreachState.cs").exists()

    def test_ibreach_service(self):
        assert _p("NovaForge/Runtime/Hazards/Breach/IBreachService.cs").exists()

    def test_breach_service(self):
        assert _p("NovaForge/Runtime/Hazards/Breach/BreachService.cs").exists()

    def test_fire_state(self):
        assert _p("NovaForge/Runtime/Hazards/Fire/FireState.cs").exists()

    def test_ifire_service(self):
        assert _p("NovaForge/Runtime/Hazards/Fire/IFireService.cs").exists()

    def test_fire_service(self):
        assert _p("NovaForge/Runtime/Hazards/Fire/FireService.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — Repair
# ---------------------------------------------------------------------------

class TestNovaForgeRepair:
    def test_repair_action_def(self):
        assert _p("NovaForge/Runtime/Repair/RepairActionDef.cs").exists()

    def test_irepair_action_service(self):
        assert _p("NovaForge/Runtime/Repair/IRepairActionService.cs").exists()

    def test_repair_action_service(self):
        assert _p("NovaForge/Runtime/Repair/RepairActionService.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — SaveLoad (extended)
# ---------------------------------------------------------------------------

class TestNovaForgeSaveLoadExtended:
    def test_combat_repair_save_state(self):
        assert _p("NovaForge/Runtime/SaveLoad/CombatRepairSaveState.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — DevWorld smoke tests (extended)
# ---------------------------------------------------------------------------

class TestNovaForgeDevWorldSmokeExtended:
    def test_combat_repair_fire_breach_smoke_test_service(self):
        assert _p("NovaForge/Runtime/DevWorld/Services/CombatRepairFireBreachSmokeTestService.cs").exists()


# ---------------------------------------------------------------------------
# Atlas UI — AtlasSuite Debug Panels (combat/repair/hazard)
# ---------------------------------------------------------------------------

class TestAtlasSuiteCombatRepairPanels:
    def test_combat_debug_panel_xaml(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/CombatDebug/CombatDebugPanel.xaml").exists()

    def test_combat_debug_panel_cs(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/CombatDebug/CombatDebugPanel.xaml.cs").exists()

    def test_repair_debug_panel_xaml(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/RepairDebug/RepairDebugPanel.xaml").exists()

    def test_repair_debug_panel_cs(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/RepairDebug/RepairDebugPanel.xaml.cs").exists()

    def test_hazard_debug_panel_xaml(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/HazardDebug/HazardDebugPanel.xaml").exists()

    def test_hazard_debug_panel_cs(self):
        assert _p("Atlas/UI/AtlasSuite/Panels/HazardDebug/HazardDebugPanel.xaml.cs").exists()

    def test_combat_repair_fire_breach_playtest_command(self):
        assert _p("Atlas/UI/AtlasSuite/PlaytestHost/CombatRepairFireBreachPlaytestCommand.cs").exists()


# ---------------------------------------------------------------------------
# NovaForge Content — Combat & Repair data
# ---------------------------------------------------------------------------

class TestNovaForgeContentCombatRepair:
    def test_dev_combat_repair_config(self):
        assert _p("NovaForge/Content/Config/dev_combat_repair_fire_breach.json").exists()

    def test_damage_profile_kinetic_slug(self):
        assert _p("NovaForge/Content/Data/Combat/damage_profile_kinetic_slug_mk1.json").exists()

    def test_dev_damage_hull_segment(self):
        assert _p("NovaForge/Content/Data/Combat/dev_damage_hull_segment.json").exists()

    def test_emergency_breach_patch(self):
        assert _p("NovaForge/Content/Data/Repair/emergency_breach_patch.json").exists()

    def test_portable_fire_suppress(self):
        assert _p("NovaForge/Content/Data/Repair/portable_fire_suppress.json").exists()

    def test_field_hull_restore(self):
        assert _p("NovaForge/Content/Data/Repair/field_hull_restore.json").exists()


# ---------------------------------------------------------------------------
# Archive — zips and chats moved correctly
# ---------------------------------------------------------------------------

class TestArchive:
    def test_atlas_suite_pack_archived(self):
        assert _p("Docs/Archive/ZipFiles/atlas_suite_pack.zip").exists()

    def test_devworld_pack_archived(self):
        assert _p("Docs/Archive/ZipFiles/atlas_suite_devworld_pack.zip").exists()

    def test_vehicle_pack_archived(self):
        assert _p("Docs/Archive/ZipFiles/atlas_suite_vehicle_pack.zip").exists()

    def test_rig_pack_archived(self):
        assert _p("Docs/Archive/ZipFiles/atlas_suite_rig_pack.zip").exists()

    def test_builder_salvage_pack_archived(self):
        assert _p("Docs/Archive/ZipFiles/atlas_suite_builder_salvage_pack.zip").exists()

    def test_combat_repair_pack_archived(self):
        assert _p("Docs/Archive/ZipFiles/atlas_suite_combat_repair_pack.zip").exists()

    def test_chat_export_1_archived(self):
        assert _p("Docs/Archive/Chats/New Text Document.txt").exists()

    def test_chat_export_2_archived(self):
        assert _p("Docs/Archive/Chats/New Text Document (2).txt").exists()

    def test_chat_export_3_archived(self):
        assert _p("Docs/Archive/Chats/New Text Document (3).txt").exists()


# ---------------------------------------------------------------------------
# NovaForge Runtime — Vertical Slice (Gameplay, Session, Player, UI)
# ---------------------------------------------------------------------------

class TestNovaForgeVerticalSlice:
    def test_vertical_slice_game_mode_header(self):
        assert _p("NovaForge/Runtime/Gameplay/VerticalSliceGameMode.h").exists()

    def test_vertical_slice_game_mode_source(self):
        assert _p("NovaForge/Runtime/Gameplay/VerticalSliceGameMode.cpp").exists()

    def test_session_bootstrap_header(self):
        assert _p("NovaForge/Runtime/Session/SessionBootstrap.h").exists()

    def test_session_bootstrap_source(self):
        assert _p("NovaForge/Runtime/Session/SessionBootstrap.cpp").exists()

    def test_rig_controller_header(self):
        assert _p("NovaForge/Runtime/Player/RigController.h").exists()

    def test_rig_controller_source(self):
        assert _p("NovaForge/Runtime/Player/RigController.cpp").exists()

    def test_hud_runtime_controller_header(self):
        assert _p("NovaForge/Runtime/UI/HudRuntimeController.h").exists()

    def test_hud_runtime_controller_source(self):
        assert _p("NovaForge/Runtime/UI/HudRuntimeController.cpp").exists()


# ---------------------------------------------------------------------------
# Docs — Runtime gameplay spec
# ---------------------------------------------------------------------------

class TestRuntimeGameplayDocs:
    def test_expanded_runtime_gameplay_spec(self):
        assert _p("Docs/Runtime/EXPANDED_RUNTIME_GAMEPLAY_SPEC.md").exists()


# ---------------------------------------------------------------------------
# AtlasAI — Ingestion files
# ---------------------------------------------------------------------------

class TestAtlasAIIngestion:
    def test_ingestion_manifest(self):
        assert _p("AtlasAI/Ingestion/INGESTION_MANIFEST.json").exists()

    def test_knowledge_chunks(self):
        assert _p("AtlasAI/Ingestion/knowledge_chunks.json").exists()

    def test_zips_not_in_root(self):
        root_zips = list(REPO_ROOT.glob("*.zip"))
        assert root_zips == [], f"Unexpected zip(s) in root: {root_zips}"

    def test_txt_not_in_root(self):
        root_txts = [f for f in REPO_ROOT.glob("*.txt") if f.name != "CMakeLists.txt"]
        assert root_txts == [], f"Unexpected txt(s) in root: {root_txts}"
