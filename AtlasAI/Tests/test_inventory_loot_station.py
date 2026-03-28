"""Tests for D1 (Inventory + LootResolver) and D2 (StorageSystem)."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# =============================================================================
# D1 — Inventory system
# =============================================================================

class TestInventoryFilesExist(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_inventory_types_header(self):
        self._check("NovaForge/Gameplay/Inventory/InventoryTypes.h")

    def test_inventory_system_header(self):
        self._check("NovaForge/Gameplay/Inventory/InventorySystem.h")

    def test_inventory_system_source(self):
        self._check("NovaForge/Gameplay/Inventory/InventorySystem.cpp")


class TestInventoryTypesContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/Inventory/InventoryTypes.h").read_text(encoding="utf-8")

    def test_has_item_category_enum(self):
        self.assertIn("EItemCategory", self._read())

    def test_has_item_definition(self):
        self.assertIn("ItemDefinition", self._read())

    def test_has_inventory_slot(self):
        self.assertIn("InventorySlot", self._read())

    def test_has_inventory_limits(self):
        self.assertIn("InventoryLimits", self._read())

    def test_has_mass_per_unit(self):
        self.assertIn("massPerUnit", self._read())

    def test_has_volume_per_unit(self):
        self.assertIn("volumePerUnit", self._read())

    def test_has_base_value(self):
        self.assertIn("baseValue", self._read())

    def test_categories_cover_key_types(self):
        text = self._read()
        for cat in ["Resource", "Component", "Weapon", "Module",
                    "Consumable", "QuestItem", "Equipment", "Blueprint"]:
            self.assertIn(cat, text, f"Missing item category: {cat}")


class TestInventorySystemContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/Inventory/InventorySystem.h").read_text(encoding="utf-8")

    def test_has_register_item(self):
        self.assertIn("registerItem", self._read())

    def test_has_find_item_def(self):
        self.assertIn("findItemDef", self._read())

    def test_has_create_inventory(self):
        self.assertIn("createInventory", self._read())

    def test_has_insert_items(self):
        self.assertIn("insertItems", self._read())

    def test_has_remove_items(self):
        self.assertIn("removeItems", self._read())

    def test_has_count_items(self):
        self.assertIn("countItems", self._read())

    def test_has_has_items(self):
        self.assertIn("hasItems", self._read())

    def test_has_can_insert(self):
        self.assertIn("canInsert", self._read())

    def test_has_get_remaining_mass(self):
        self.assertIn("getRemainingMass", self._read())

    def test_has_get_remaining_volume(self):
        self.assertIn("getRemainingVolume", self._read())

    def test_has_entity_inventory(self):
        self.assertIn("EntityInventory", self._read())


# =============================================================================
# D1 — LootResolver
# =============================================================================

class TestLootResolverFilesExist(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_loot_resolver_header(self):
        self._check("NovaForge/Gameplay/Economy/LootResolver.h")

    def test_loot_resolver_source(self):
        self._check("NovaForge/Gameplay/Economy/LootResolver.cpp")


class TestLootResolverContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/Economy/LootResolver.h").read_text(encoding="utf-8")

    def test_has_resolved_loot_entry(self):
        self.assertIn("ResolvedLootEntry", self._read())

    def test_has_loot_reward(self):
        self.assertIn("LootReward", self._read())

    def test_has_register_table(self):
        self.assertIn("registerTable", self._read())

    def test_has_resolve(self):
        self.assertIn("resolve", self._read())

    def test_has_apply_to_inventory(self):
        self.assertIn("applyToInventory", self._read())

    def test_has_apply_mining_yield(self):
        self.assertIn("applyMiningYield", self._read())

    def test_has_credits_awarded(self):
        self.assertIn("creditsAwarded", self._read())


# =============================================================================
# D2 — StorageSystem
# =============================================================================

class TestStorageSystemFilesExist(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_storage_system_header(self):
        self._check("NovaForge/Gameplay/Storage/StorageSystem.h")

    def test_storage_system_source(self):
        self._check("NovaForge/Gameplay/Storage/StorageSystem.cpp")


class TestStorageSystemContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/Storage/StorageSystem.h").read_text(encoding="utf-8")

    def test_has_storage_depot(self):
        self.assertIn("StorageDepot", self._read())

    def test_has_manufacturing_job(self):
        self.assertIn("ManufacturingJob", self._read())

    def test_has_job_status_enum(self):
        self.assertIn("EJobStatus", self._read())

    def test_has_module_bay(self):
        self.assertIn("ModuleBay", self._read())

    def test_has_module_bay_slot(self):
        self.assertIn("ModuleBaySlot", self._read())

    def test_has_create_depot(self):
        self.assertIn("createDepot", self._read())

    def test_has_deposit_items(self):
        self.assertIn("depositItems", self._read())

    def test_has_withdraw_items(self):
        self.assertIn("withdrawItems", self._read())

    def test_has_query_item_count(self):
        self.assertIn("queryItemCount", self._read())

    def test_has_queue_manufacturing_job(self):
        self.assertIn("queueManufacturingJob", self._read())

    def test_has_tick_jobs(self):
        self.assertIn("tickJobs", self._read())

    def test_has_collect_completed_job(self):
        self.assertIn("collectCompletedJob", self._read())

    def test_has_list_jobs(self):
        self.assertIn("listJobs", self._read())

    def test_has_create_module_bay(self):
        self.assertIn("createModuleBay", self._read())

    def test_has_store_module(self):
        self.assertIn("storeModule", self._read())

    def test_has_retrieve_module(self):
        self.assertIn("retrieveModule", self._read())

    def test_has_job_statuses(self):
        text = self._read()
        for s in ["Queued", "InProgress", "Completed", "Failed"]:
            self.assertIn(s, text, f"Missing job status: {s}")


class TestGameplayCMakeUpdated(unittest.TestCase):
    def _cmake(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/CMakeLists.txt").read_text(encoding="utf-8")

    def test_has_inventory_system(self):
        self.assertIn("InventorySystem.cpp", self._cmake())

    def test_has_storage_system(self):
        self.assertIn("StorageSystem.cpp", self._cmake())

    def test_has_loot_resolver(self):
        self.assertIn("LootResolver.cpp", self._cmake())

    def test_has_progression_reward_system(self):
        self.assertIn("ProgressionRewardSystem.cpp", self._cmake())

    def test_has_inventory_dir(self):
        self.assertIn("Inventory", self._cmake())

    def test_has_storage_dir(self):
        self.assertIn("Storage", self._cmake())


if __name__ == "__main__":
    unittest.main()
