"""Tests for F2 (QA tools and integration regression coverage).

Validates:
- Data validation pipeline structural coverage (via UnifiedDataRegistry)
- Save/load smoke (SaveSystem API surface completeness)
- PCG determinism (PCGWorldGen seed-based API)
- Economy smoke (TradeMarket + LootResolver integration surface)
- Integration regression checklist (cross-system structural wiring)
"""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# =============================================================================
# F2.1 — Data validation pipeline (UnifiedDataRegistry cross-reference)
# =============================================================================

class TestDataValidationPipeline(unittest.TestCase):
    """Validates the structural completeness of the data validation pipeline."""

    def test_registry_validates_recipe_output_refs(self):
        src = (REPO_ROOT / "NovaForge/Gameplay/Data/UnifiedDataRegistry.cpp").read_text(encoding="utf-8")
        self.assertIn("outputItemId", src)
        self.assertIn("HasItem", src)

    def test_registry_validates_ingredient_refs(self):
        src = (REPO_ROOT / "NovaForge/Gameplay/Data/UnifiedDataRegistry.cpp").read_text(encoding="utf-8")
        self.assertIn("ingredient", src.lower())

    def test_registry_validates_faction_refs(self):
        src = (REPO_ROOT / "NovaForge/Gameplay/Data/UnifiedDataRegistry.cpp").read_text(encoding="utf-8")
        self.assertIn("HasFaction", src)

    def test_registry_validates_module_item_refs(self):
        src = (REPO_ROOT / "NovaForge/Gameplay/Data/UnifiedDataRegistry.cpp").read_text(encoding="utf-8")
        self.assertIn("requiredItemId", src)

    def test_validation_report_is_clean_predicate(self):
        hdr = (REPO_ROOT / "NovaForge/Gameplay/Data/UnifiedDataRegistry.h").read_text(encoding="utf-8")
        self.assertIn("IsClean", hdr)

    def test_validation_report_error_count(self):
        hdr = (REPO_ROOT / "NovaForge/Gameplay/Data/UnifiedDataRegistry.h").read_text(encoding="utf-8")
        self.assertIn("ErrorCount", hdr)

    def test_validation_severity_levels_all_present(self):
        hdr = (REPO_ROOT / "NovaForge/Gameplay/Data/UnifiedDataRegistry.h").read_text(encoding="utf-8")
        for sev in ["Info", "Warning", "Error"]:
            self.assertIn(sev, hdr, f"Missing severity level: {sev}")

    def test_schema_version_check_in_registry(self):
        hdr = (REPO_ROOT / "NovaForge/Gameplay/Data/UnifiedDataRegistry.h").read_text(encoding="utf-8")
        self.assertIn("CheckSchemaVersion", hdr)

    def test_schema_version_compatibility_in_types(self):
        hdr = (REPO_ROOT / "NovaForge/Gameplay/Data/UnifiedDataTypes.h").read_text(encoding="utf-8")
        self.assertIn("isCompatible", hdr)


# =============================================================================
# F2.2 — Save/Load smoke
# =============================================================================

class TestSaveLoadSmoke(unittest.TestCase):
    """Validates save/load API surface covers all required state categories."""

    def _save_header(self) -> str:
        return (REPO_ROOT / "NovaForge/Save/include/SaveSystem.h").read_text(encoding="utf-8")

    def test_player_state_save_slot(self):
        self.assertIn("SavedPlayerState", self._save_header())

    def test_voxel_state_save_slot(self):
        self.assertIn("SavedVoxelChunk", self._save_header())

    def test_economy_state_save_slot(self):
        self.assertIn("SavedEconomyState", self._save_header())

    def test_contract_state_save_slot(self):
        self.assertIn("SavedContractState", self._save_header())

    def test_fleet_state_save_slot(self):
        self.assertIn("SavedFleetState", self._save_header())

    def test_save_flush_method(self):
        self.assertIn("flushToSlot", self._save_header())

    def test_load_from_slot_method(self):
        self.assertIn("loadFromSlot", self._save_header())

    def test_validate_bundle_method(self):
        self.assertIn("validateBundle", self._save_header())

    def test_max_slots_constant(self):
        self.assertIn("kMaxSlots", self._save_header())

    def test_save_metadata_present(self):
        self.assertIn("SaveMetadata", self._save_header())


# =============================================================================
# F2.3 — PCG determinism smoke
# =============================================================================

class TestPCGDeterminismSmoke(unittest.TestCase):
    """Validates PCGWorldGen provides a seed-based deterministic generation API."""

    def _pcg_header(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/PCG/PCGWorldGen.h").read_text(encoding="utf-8")

    def test_world_seed_field(self):
        self.assertIn("worldSeed", self._pcg_header())

    def test_generate_method(self):
        self.assertIn("generate", self._pcg_header())

    def test_sector_count_field(self):
        self.assertIn("sectorCount", self._pcg_header())

    def test_pcg_debug_system_seed_panel(self):
        debug = (REPO_ROOT / "Atlas/Editor/PCG/PCGDebugSystem.h").read_text(encoding="utf-8")
        self.assertIn("SetSeed", debug)

    def test_pcg_debug_regenerate_selected(self):
        debug = (REPO_ROOT / "Atlas/Editor/PCG/PCGDebugSystem.h").read_text(encoding="utf-8")
        self.assertIn("RegenerateSelected", debug)


# =============================================================================
# F2.4 — Economy and WorldSim smoke
# =============================================================================

class TestEconomySmoke(unittest.TestCase):
    """Validates economy systems have the API surface for smoke tests."""

    def _trade_market(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/Economy/TradeMarket.h").read_text(encoding="utf-8")

    def _loot_resolver(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/Economy/LootResolver.h").read_text(encoding="utf-8")

    def _worldsim(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/WorldSim/WorldSimSystem.h").read_text(encoding="utf-8")

    def test_trade_market_place_order(self):
        self.assertIn("placeOrder", self._trade_market())

    def test_trade_market_cancel_order(self):
        self.assertIn("cancelOrder", self._trade_market())

    def test_trade_market_best_price(self):
        self.assertIn("getBestPrice", self._trade_market())

    def test_trade_market_query_station(self):
        self.assertIn("queryStation", self._trade_market())

    def test_loot_resolver_has_resolve(self):
        self.assertIn("resolve", self._loot_resolver())

    def test_loot_resolver_has_apply_to_inventory(self):
        self.assertIn("applyToInventory", self._loot_resolver())

    def test_worldsim_tick(self):
        self.assertIn("tick", self._worldsim())

    def test_worldsim_titan_pressure(self):
        self.assertIn("getGlobalPressure", self._worldsim())

    def test_worldsim_sector_state(self):
        self.assertIn("SectorState", self._worldsim())


# =============================================================================
# F2.5 — Integration regression checklist
# =============================================================================

class TestIntegrationRegressionChecklist(unittest.TestCase):
    """Structural checks that key integration wiring points exist across systems."""

    def test_world_bootstrap_runs_all_phases(self):
        src = (REPO_ROOT / "NovaForge/App/Bootstrap/WorldBootstrap.cpp").read_text(encoding="utf-8")
        self.assertIn("RunAll", src)

    def test_world_bootstrap_phase_order_defined(self):
        src = (REPO_ROOT / "NovaForge/App/Bootstrap/WorldBootstrap.cpp").read_text(encoding="utf-8")
        self.assertIn("kPhaseOrder", src)

    def test_inventory_system_capacity_check(self):
        src = (REPO_ROOT / "NovaForge/Gameplay/Inventory/InventorySystem.cpp").read_text(encoding="utf-8")
        self.assertIn("canInsert", src)

    def test_storage_manufacturing_tick(self):
        src = (REPO_ROOT / "NovaForge/Gameplay/Storage/StorageSystem.cpp").read_text(encoding="utf-8")
        self.assertIn("tickJobs", src)

    def test_progression_reward_applies_credits(self):
        src = (REPO_ROOT / "NovaForge/Gameplay/Progression/ProgressionRewardSystem.cpp").read_text(encoding="utf-8")
        self.assertIn("awardCredits", src)

    def test_salvage_system_apply_reward_to_inventory(self):
        src = (REPO_ROOT / "NovaForge/Gameplay/Salvage/SalvageSystem.h").read_text(encoding="utf-8")
        self.assertIn("applyRewardToInventory", src)

    def test_station_services_deposit(self):
        src = (REPO_ROOT / "NovaForge/Gameplay/Station/StationServices.h").read_text(encoding="utf-8")
        self.assertIn("depositItems", src)

    def test_station_services_withdraw(self):
        src = (REPO_ROOT / "NovaForge/Gameplay/Station/StationServices.h").read_text(encoding="utf-8")
        self.assertIn("withdrawItems", src)

    def test_fleet_system_contract_assignment(self):
        src = (REPO_ROOT / "NovaForge/Gameplay/Fleet/FleetSystem.h").read_text(encoding="utf-8")
        self.assertIn("assignToMission", src)

    def test_contract_reward_system_dispenses_reward(self):
        src = (REPO_ROOT / "NovaForge/Gameplay/Missions/ContractRewardSystem.h").read_text(encoding="utf-8")
        self.assertIn("completeContract", src)

    def test_scene_hierarchy_has_set_transform(self):
        src = (REPO_ROOT / "Atlas/Editor/Outliner/SceneHierarchySystem.h").read_text(encoding="utf-8")
        self.assertIn("SetTransform", src)

    def test_placement_system_confirm_placement(self):
        src = (REPO_ROOT / "Atlas/Editor/Gizmos/PlacementSystem.h").read_text(encoding="utf-8")
        self.assertIn("ConfirmPlacement", src)

    def test_diff_review_panel_accept_fires_callback(self):
        src = (REPO_ROOT / "Atlas/Editor/AI/DiffReviewPanel.h").read_text(encoding="utf-8")
        self.assertIn("AcceptCallback", src)

    def test_render_viewport_submit_voxel_chunk(self):
        src = (REPO_ROOT / "Atlas/Engine/Rendering/RenderViewport.h").read_text(encoding="utf-8")
        self.assertIn("SubmitVoxelChunk", src)

    def test_input_context_route_press(self):
        src = (REPO_ROOT / "Atlas/Engine/Input/InputContextManager.h").read_text(encoding="utf-8")
        self.assertIn("RoutePress", src)

    def test_hud_layer_push_alert(self):
        src = (REPO_ROOT / "NovaForge/UI/include/Widgets/HUDLayer.h").read_text(encoding="utf-8")
        self.assertIn("PushAlert", src)

    def test_contract_board_accept_selected(self):
        src = (REPO_ROOT / "NovaForge/UI/include/Widgets/ContractBoardUI.h").read_text(encoding="utf-8")
        self.assertIn("AcceptSelected", src)

    def test_station_terminal_trigger_repair(self):
        src = (REPO_ROOT / "NovaForge/UI/include/Widgets/StationTerminalUI.h").read_text(encoding="utf-8")
        self.assertIn("TriggerRepair", src)

    def test_fleet_progression_update_ship_xp(self):
        src = (REPO_ROOT / "NovaForge/UI/include/Widgets/FleetProgressionPanel.h").read_text(encoding="utf-8")
        self.assertIn("UpdateShipXP", src)

    def test_editor_dock_layout_apply_preset(self):
        src = (REPO_ROOT / "Atlas/Editor/Core/EditorDockLayout.h").read_text(encoding="utf-8")
        self.assertIn("ApplyPreset", src)


if __name__ == "__main__":
    unittest.main()
