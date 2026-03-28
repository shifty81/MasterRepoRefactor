"""Tests for B4 (UI Framework: HUD, Inventory, ContractBoard, StationTerminal, FleetPanel, EditorDock)."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# =============================================================================
# UIWidgetBase
# =============================================================================

class TestUIWidgetBaseExists(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_widget_base_header(self):
        self._check("NovaForge/UI/include/Widgets/UIWidgetBase.h")

    def test_hud_layer_header(self):
        self._check("NovaForge/UI/include/Widgets/HUDLayer.h")

    def test_inventory_screen_header(self):
        self._check("NovaForge/UI/include/Widgets/InventoryScreen.h")

    def test_contract_board_header(self):
        self._check("NovaForge/UI/include/Widgets/ContractBoardUI.h")

    def test_station_terminal_header(self):
        self._check("NovaForge/UI/include/Widgets/StationTerminalUI.h")

    def test_fleet_progression_header(self):
        self._check("NovaForge/UI/include/Widgets/FleetProgressionPanel.h")


class TestUIWidgetBaseContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/UI/include/Widgets/UIWidgetBase.h").read_text(encoding="utf-8")

    def test_has_widget_type_enum(self):
        self.assertIn("EWidgetType", self._read())

    def test_has_widget_state_enum(self):
        self.assertIn("EWidgetState", self._read())

    def test_has_widget_rect(self):
        self.assertIn("WidgetRect", self._read())

    def test_has_ui_widget(self):
        self.assertIn("UIWidget", self._read())

    def test_widget_types_cover_key_types(self):
        text = self._read()
        for t in ["Panel", "Label", "Button", "ProgressBar", "ListView", "Slot", "Icon"]:
            self.assertIn(t, text, f"Missing widget type: {t}")


# =============================================================================
# HUDLayer
# =============================================================================

class TestHUDLayerContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/UI/include/Widgets/HUDLayer.h").read_text(encoding="utf-8")

    def test_has_hud_player_stats(self):
        self.assertIn("HUDPlayerStats", self._read())

    def test_has_hud_alert_message(self):
        self.assertIn("HUDAlertMessage", self._read())

    def test_has_hud_mission_track(self):
        self.assertIn("HUDMissionTrack", self._read())

    def test_has_update_player_stats(self):
        self.assertIn("UpdatePlayerStats", self._read())

    def test_has_push_alert(self):
        self.assertIn("PushAlert", self._read())

    def test_has_set_active_mission(self):
        self.assertIn("SetActiveMission", self._read())

    def test_has_set_mission_progress(self):
        self.assertIn("SetMissionProgress", self._read())

    def test_has_build_widgets(self):
        self.assertIn("BuildWidgets", self._read())

    def test_has_clear_expired_alerts(self):
        self.assertIn("ClearExpiredAlerts", self._read())

    def test_has_credits_field(self):
        self.assertIn("credits", self._read())

    def test_has_health_field(self):
        self.assertIn("health", self._read())


# =============================================================================
# InventoryScreen
# =============================================================================

class TestInventoryScreenContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/UI/include/Widgets/InventoryScreen.h").read_text(encoding="utf-8")

    def test_has_inventory_screen_item(self):
        self.assertIn("InventoryScreenItem", self._read())

    def test_has_inventory_screen_state(self):
        self.assertIn("InventoryScreenState", self._read())

    def test_has_set_items(self):
        self.assertIn("SetItems", self._read())

    def test_has_set_capacity(self):
        self.assertIn("SetCapacity", self._read())

    def test_has_open_close(self):
        text = self._read()
        self.assertIn("Open", text)
        self.assertIn("Close", text)

    def test_has_select_item(self):
        self.assertIn("SelectItem", self._read())

    def test_has_get_selected_item(self):
        self.assertIn("GetSelectedItem", self._read())

    def test_has_category_filter(self):
        self.assertIn("SetCategoryFilter", self._read())

    def test_has_build_widgets(self):
        self.assertIn("BuildWidgets", self._read())


# =============================================================================
# ContractBoardUI
# =============================================================================

class TestContractBoardUIContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/UI/include/Widgets/ContractBoardUI.h").read_text(encoding="utf-8")

    def test_has_contract_board_entry(self):
        self.assertIn("ContractBoardEntry", self._read())

    def test_has_set_contracts(self):
        self.assertIn("SetContracts", self._read())

    def test_has_mark_contract_locked(self):
        self.assertIn("MarkContractLocked", self._read())

    def test_has_select_contract(self):
        self.assertIn("SelectContract", self._read())

    def test_has_accept_selected(self):
        self.assertIn("AcceptSelected", self._read())

    def test_has_decline_selected(self):
        self.assertIn("DeclineSelected", self._read())

    def test_has_accept_callback(self):
        self.assertIn("AcceptCallback", self._read())

    def test_has_build_widgets(self):
        self.assertIn("BuildWidgets", self._read())


# =============================================================================
# StationTerminalUI
# =============================================================================

class TestStationTerminalUIContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/UI/include/Widgets/StationTerminalUI.h").read_text(encoding="utf-8")

    def test_has_estation_tab_enum(self):
        self.assertIn("EStationTab", self._read())

    def test_has_storage_row(self):
        self.assertIn("StationStorageRow", self._read())

    def test_has_manufacturing_row(self):
        self.assertIn("StationManufacturingRow", self._read())

    def test_has_set_storage_rows(self):
        self.assertIn("SetStorageRows", self._read())

    def test_has_set_manufacturing_rows(self):
        self.assertIn("SetManufacturingRows", self._read())

    def test_has_set_tab(self):
        self.assertIn("SetTab", self._read())

    def test_has_trigger_repair(self):
        self.assertIn("TriggerRepair", self._read())

    def test_has_trigger_resupply(self):
        self.assertIn("TriggerResupply", self._read())

    def test_tabs_cover_key_types(self):
        text = self._read()
        for tab in ["Storage", "Manufacturing", "Repair", "Resupply", "Market"]:
            self.assertIn(tab, text, f"Missing station tab: {tab}")

    def test_has_deposit_callback(self):
        self.assertIn("DepositCallback", self._read())

    def test_has_withdraw_callback(self):
        self.assertIn("WithdrawCallback", self._read())


# =============================================================================
# FleetProgressionPanel
# =============================================================================

class TestFleetProgressionPanelContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/UI/include/Widgets/FleetProgressionPanel.h").read_text(encoding="utf-8")

    def test_has_fleet_ship_entry(self):
        self.assertIn("FleetShipEntry", self._read())

    def test_has_fleet_progression_state(self):
        self.assertIn("FleetProgressionState", self._read())

    def test_has_set_fleet_state(self):
        self.assertIn("SetFleetState", self._read())

    def test_has_update_ship_xp(self):
        self.assertIn("UpdateShipXP", self._read())

    def test_has_update_ship_condition(self):
        self.assertIn("UpdateShipCondition", self._read())

    def test_has_select_ship(self):
        self.assertIn("SelectShip", self._read())

    def test_has_get_selected_ship(self):
        self.assertIn("GetSelectedShip", self._read())

    def test_has_build_widgets(self):
        self.assertIn("BuildWidgets", self._read())

    def test_has_level_field(self):
        self.assertIn("level", self._read())

    def test_has_role_tag_field(self):
        self.assertIn("roleTag", self._read())


# =============================================================================
# EditorDockLayout (B4 editor panel docking)
# =============================================================================

class TestEditorDockLayoutExists(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_editor_dock_layout_header(self):
        self._check("Atlas/Editor/Core/EditorDockLayout.h")

    def test_editor_dock_layout_source(self):
        self._check("Atlas/Editor/Core/EditorDockLayout.cpp")


class TestEditorDockLayoutContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/Core/EditorDockLayout.h").read_text(encoding="utf-8")

    def test_has_edock_region_enum(self):
        self.assertIn("EDockRegion", self._read())

    def test_has_dock_panel(self):
        self.assertIn("DockPanel", self._read())

    def test_has_dock_layout_preset(self):
        self.assertIn("DockLayoutPreset", self._read())

    def test_has_register_panel(self):
        self.assertIn("RegisterPanel", self._read())

    def test_has_show_panel(self):
        self.assertIn("ShowPanel", self._read())

    def test_has_hide_panel(self):
        self.assertIn("HidePanel", self._read())

    def test_has_toggle_panel(self):
        self.assertIn("TogglePanel", self._read())

    def test_has_focus_panel(self):
        self.assertIn("FocusPanel", self._read())

    def test_has_register_preset(self):
        self.assertIn("RegisterPreset", self._read())

    def test_has_apply_preset(self):
        self.assertIn("ApplyPreset", self._read())

    def test_has_set_panel_size(self):
        self.assertIn("SetPanelSize", self._read())

    def test_has_list_by_region(self):
        self.assertIn("ListByRegion", self._read())

    def test_has_draw_all(self):
        self.assertIn("DrawAll", self._read())

    def test_dock_regions_cover_key_cases(self):
        text = self._read()
        for region in ["Left", "Right", "Bottom", "Top", "Centre", "FloatingModal"]:
            self.assertIn(region, text, f"Missing dock region: {region}")


class TestUICMakeUpdated(unittest.TestCase):
    def _cmake(self) -> str:
        return (REPO_ROOT / "NovaForge/UI/CMakeLists.txt").read_text(encoding="utf-8")

    def test_has_hud_layer(self):
        self.assertIn("HUDLayer.cpp", self._cmake())

    def test_has_inventory_screen(self):
        self.assertIn("InventoryScreen.cpp", self._cmake())

    def test_has_contract_board(self):
        self.assertIn("ContractBoardUI.cpp", self._cmake())

    def test_has_station_terminal(self):
        self.assertIn("StationTerminalUI.cpp", self._cmake())

    def test_has_fleet_progression(self):
        self.assertIn("FleetProgressionPanel.cpp", self._cmake())

    def test_has_widgets_dir(self):
        self.assertIn("Widgets", self._cmake())


class TestEditorCMakeUpdatedWithDock(unittest.TestCase):
    def _cmake(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/CMakeLists.txt").read_text(encoding="utf-8")

    def test_has_editor_dock_layout(self):
        self.assertIn("EditorDockLayout.cpp", self._cmake())

    def test_has_diff_review_panel(self):
        self.assertIn("DiffReviewPanel.cpp", self._cmake())

    def test_has_ai_dir(self):
        self.assertIn("/AI", self._cmake())


if __name__ == "__main__":
    unittest.main()
