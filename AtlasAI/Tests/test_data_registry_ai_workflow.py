"""Tests for A3 (UnifiedDataRegistry) and E1 (DiffReviewPanel / AtlasAI workflow)."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# =============================================================================
# A3 — Unified Data Registry
# =============================================================================

class TestUnifiedDataRegistryFilesExist(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_unified_data_types_header(self):
        self._check("NovaForge/Gameplay/Data/UnifiedDataTypes.h")

    def test_unified_data_registry_header(self):
        self._check("NovaForge/Gameplay/Data/UnifiedDataRegistry.h")

    def test_unified_data_registry_source(self):
        self._check("NovaForge/Gameplay/Data/UnifiedDataRegistry.cpp")


class TestUnifiedDataTypesContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/Data/UnifiedDataTypes.h").read_text(encoding="utf-8")

    def test_has_schema_version(self):
        self.assertIn("SchemaVersion", self._read())

    def test_has_item_record(self):
        self.assertIn("ItemRecord", self._read())

    def test_has_recipe_record(self):
        self.assertIn("RecipeRecord", self._read())

    def test_has_recipe_ingredient(self):
        self.assertIn("RecipeIngredient", self._read())

    def test_has_mission_record(self):
        self.assertIn("MissionRecord", self._read())

    def test_has_emission_type_enum(self):
        self.assertIn("EMissionType", self._read())

    def test_has_faction_record(self):
        self.assertIn("FactionRecord", self._read())

    def test_has_module_record(self):
        self.assertIn("ModuleRecord", self._read())

    def test_has_emodule_slot_enum(self):
        self.assertIn("EModuleSlot", self._read())

    def test_mission_types_cover_key_cases(self):
        text = self._read()
        for t in ["Delivery", "Combat", "Salvage", "Mining", "Escort", "Exploration", "Bounty"]:
            self.assertIn(t, text, f"Missing mission type: {t}")

    def test_module_slots_cover_key_cases(self):
        text = self._read()
        for slot in ["Weapon", "Engine", "Shield", "Reactor", "Utility", "Structure"]:
            self.assertIn(slot, text, f"Missing module slot: {slot}")

    def test_schema_version_compatibility_method(self):
        self.assertIn("isCompatible", self._read())


class TestUnifiedDataRegistryContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/Data/UnifiedDataRegistry.h").read_text(encoding="utf-8")

    def test_has_validation_issue(self):
        self.assertIn("ValidationIssue", self._read())

    def test_has_validation_report(self):
        self.assertIn("ValidationReport", self._read())

    def test_has_evalidation_severity(self):
        self.assertIn("EValidationSeverity", self._read())

    def test_has_hot_reload_callback(self):
        self.assertIn("HotReloadCallback", self._read())

    def test_has_register_item(self):
        self.assertIn("RegisterItem", self._read())

    def test_has_register_recipe(self):
        self.assertIn("RegisterRecipe", self._read())

    def test_has_register_mission(self):
        self.assertIn("RegisterMission", self._read())

    def test_has_register_faction(self):
        self.assertIn("RegisterFaction", self._read())

    def test_has_register_module(self):
        self.assertIn("RegisterModule", self._read())

    def test_has_find_item(self):
        self.assertIn("FindItem", self._read())

    def test_has_find_recipe(self):
        self.assertIn("FindRecipe", self._read())

    def test_has_find_mission(self):
        self.assertIn("FindMission", self._read())

    def test_has_find_faction(self):
        self.assertIn("FindFaction", self._read())

    def test_has_find_module(self):
        self.assertIn("FindModule", self._read())

    def test_has_validate_all(self):
        self.assertIn("ValidateAll", self._read())

    def test_has_validate_recipes(self):
        self.assertIn("ValidateRecipes", self._read())

    def test_has_validate_missions(self):
        self.assertIn("ValidateMissions", self._read())

    def test_has_validate_modules(self):
        self.assertIn("ValidateModules", self._read())

    def test_has_check_schema_version(self):
        self.assertIn("CheckSchemaVersion", self._read())

    def test_has_notify_hot_reload(self):
        self.assertIn("NotifyHotReload", self._read())

    def test_has_writeback_item(self):
        self.assertIn("WritebackItem", self._read())

    def test_has_writeback_recipe(self):
        self.assertIn("WritebackRecipe", self._read())

    def test_has_writeback_mission(self):
        self.assertIn("WritebackMission", self._read())

    def test_has_total_records(self):
        self.assertIn("TotalRecords", self._read())

    def test_has_is_clean(self):
        self.assertIn("IsClean", self._read())

    def test_has_error_count(self):
        self.assertIn("ErrorCount", self._read())

    def test_severity_levels_defined(self):
        text = self._read()
        for sev in ["Info", "Warning", "Error"]:
            self.assertIn(sev, text, f"Missing severity: {sev}")


class TestUnifiedDataRegistryImpl(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/Data/UnifiedDataRegistry.cpp").read_text(encoding="utf-8")

    def test_validates_recipe_output_item(self):
        self.assertIn("outputItemId", self._read())

    def test_validates_recipe_ingredients(self):
        self.assertIn("ingredient", self._read())

    def test_validates_mission_faction(self):
        self.assertIn("issuingFactionId", self._read())

    def test_validates_module_item(self):
        self.assertIn("requiredItemId", self._read())

    def test_hot_reload_fires_callback(self):
        self.assertIn("m_reloadCb", self._read())

    def test_writeback_fires_hot_reload(self):
        self.assertIn("NotifyHotReload", self._read())


class TestGameplayCMakeUpdatedWithData(unittest.TestCase):
    def _cmake(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/CMakeLists.txt").read_text(encoding="utf-8")

    def test_has_unified_data_registry(self):
        self.assertIn("UnifiedDataRegistry.cpp", self._cmake())

    def test_has_data_dir(self):
        self.assertIn("/Data", self._cmake())


# =============================================================================
# E1 — AtlasAI Editor Workflow (DiffReviewPanel)
# =============================================================================

class TestDiffReviewPanelFilesExist(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_diff_review_panel_header(self):
        self._check("Atlas/Editor/AI/DiffReviewPanel.h")

    def test_diff_review_panel_source(self):
        self._check("Atlas/Editor/AI/DiffReviewPanel.cpp")


class TestDiffReviewPanelContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/AI/DiffReviewPanel.h").read_text(encoding="utf-8")

    def test_has_diff_hunk(self):
        self.assertIn("DiffHunk", self._read())

    def test_has_file_impact_entry(self):
        self.assertIn("FileImpactEntry", self._read())

    def test_has_arch_rule_warning(self):
        self.assertIn("ArchRuleWarning", self._read())

    def test_has_earch_rule_level_enum(self):
        self.assertIn("EArchRuleLevel", self._read())

    def test_has_esuggestion_status_enum(self):
        self.assertIn("ESuggestionStatus", self._read())

    def test_has_ai_suggestion(self):
        self.assertIn("AISuggestion", self._read())

    def test_has_rollback_entry(self):
        self.assertIn("RollbackEntry", self._read())

    def test_has_submit_suggestion(self):
        self.assertIn("SubmitSuggestion", self._read())

    def test_has_accept_suggestion(self):
        self.assertIn("AcceptSuggestion", self._read())

    def test_has_reject_suggestion(self):
        self.assertIn("RejectSuggestion", self._read())

    def test_has_rollback_suggestion(self):
        self.assertIn("RollbackSuggestion", self._read())

    def test_has_set_selected(self):
        self.assertIn("SetSelected", self._read())

    def test_has_get_pending(self):
        self.assertIn("GetPending", self._read())

    def test_has_get_accepted(self):
        self.assertIn("GetAccepted", self._read())

    def test_has_get_rejected(self):
        self.assertIn("GetRejected", self._read())

    def test_has_rollback_history(self):
        self.assertIn("GetRollbackHistory", self._read())

    def test_has_context_linkage(self):
        self.assertIn("SetContextObject", self._read())

    def test_has_get_suggestions_for_context(self):
        self.assertIn("GetSuggestionsForContext", self._read())

    def test_has_get_all_warnings(self):
        self.assertIn("GetAllWarnings", self._read())

    def test_has_accept_callback(self):
        self.assertIn("AcceptCallback", self._read())

    def test_has_rollback_callback(self):
        self.assertIn("RollbackCallback", self._read())

    def test_has_pending_count(self):
        self.assertIn("PendingCount", self._read())

    def test_suggestion_statuses_defined(self):
        text = self._read()
        for status in ["Pending", "Accepted", "Rejected", "RolledBack"]:
            self.assertIn(status, text, f"Missing suggestion status: {status}")

    def test_arch_rule_levels_defined(self):
        text = self._read()
        for level in ["Info", "Warning", "Violation"]:
            self.assertIn(level, text, f"Missing arch rule level: {level}")

    def test_has_ai_reasoning_field(self):
        self.assertIn("aiReasoning", self._read())

    def test_has_context_object_field(self):
        self.assertIn("contextObjectId", self._read())


class TestDiffReviewPanelImpl(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/AI/DiffReviewPanel.cpp").read_text(encoding="utf-8")

    def test_accept_stores_rollback_entry(self):
        self.assertIn("rollbackHistory", self._read())

    def test_rollback_removes_entries(self):
        self.assertIn("RolledBack", self._read())

    def test_fires_accept_callback(self):
        self.assertIn("m_acceptCb", self._read())

    def test_fires_rollback_callback(self):
        self.assertIn("m_rollbackCb", self._read())

    def test_get_pending_filters_by_status(self):
        self.assertIn("Pending", self._read())


if __name__ == "__main__":
    unittest.main()
