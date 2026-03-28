"""Tests for the gameplay loop hookup systems — Salvage, Station, Manufacturing, Contracts."""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestSalvageSourceFilesExist(unittest.TestCase):
    """Verify salvage system source files are present."""

    def _check(self, relative_path: str):
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing source file: {relative_path}")

    def test_salvage_reward_types_header(self):
        self._check("NovaForge/Gameplay/Salvage/SalvageRewardTypes.h")

    def test_salvage_system_header(self):
        self._check("NovaForge/Gameplay/Salvage/SalvageSystem.h")

    def test_salvage_system_source(self):
        self._check("NovaForge/Gameplay/Salvage/SalvageSystem.cpp")


class TestSalvageHeaderContent(unittest.TestCase):
    """Verify salvage headers contain expected declarations."""

    def _read(self, path: str) -> str:
        return (REPO_ROOT / path).read_text(encoding="utf-8")

    def test_reward_types_has_loot_entry(self):
        content = self._read("NovaForge/Gameplay/Salvage/SalvageRewardTypes.h")
        self.assertIn("LootEntry", content)

    def test_reward_types_has_loot_table(self):
        content = self._read("NovaForge/Gameplay/Salvage/SalvageRewardTypes.h")
        self.assertIn("LootTable", content)

    def test_reward_types_has_salvage_reward(self):
        content = self._read("NovaForge/Gameplay/Salvage/SalvageRewardTypes.h")
        self.assertIn("SalvageReward", content)

    def test_salvage_system_has_spawn_wreck(self):
        content = self._read("NovaForge/Gameplay/Salvage/SalvageSystem.h")
        self.assertIn("spawnWreck", content)

    def test_salvage_system_has_salvage(self):
        content = self._read("NovaForge/Gameplay/Salvage/SalvageSystem.h")
        self.assertIn("salvage", content)

    def test_salvage_system_has_apply_reward_to_inventory(self):
        content = self._read("NovaForge/Gameplay/Salvage/SalvageSystem.h")
        self.assertIn("applyRewardToInventory", content)

    def test_salvage_system_has_notify_mission_progress(self):
        content = self._read("NovaForge/Gameplay/Salvage/SalvageSystem.h")
        self.assertIn("notifyMissionProgress", content)

    def test_salvage_system_has_register_loot_table(self):
        content = self._read("NovaForge/Gameplay/Salvage/SalvageSystem.h")
        self.assertIn("registerLootTable", content)


class TestStationSourceFilesExist(unittest.TestCase):
    """Verify station service source files are present."""

    def _check(self, relative_path: str):
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing source file: {relative_path}")

    def test_station_types_header(self):
        self._check("NovaForge/Gameplay/Station/StationTypes.h")

    def test_station_services_header(self):
        self._check("NovaForge/Gameplay/Station/StationServices.h")

    def test_station_services_source(self):
        self._check("NovaForge/Gameplay/Station/StationServices.cpp")


class TestStationHeaderContent(unittest.TestCase):
    """Verify station headers contain expected declarations."""

    def _read(self, path: str) -> str:
        return (REPO_ROOT / path).read_text(encoding="utf-8")

    def test_station_types_has_service_type_enum(self):
        content = self._read("NovaForge/Gameplay/Station/StationTypes.h")
        self.assertIn("EServiceType", content)

    def test_station_types_has_station_record(self):
        content = self._read("NovaForge/Gameplay/Station/StationTypes.h")
        self.assertIn("StationRecord", content)

    def test_station_types_has_storage_slot(self):
        content = self._read("NovaForge/Gameplay/Station/StationTypes.h")
        self.assertIn("StorageSlot", content)

    def test_station_services_has_deposit_items(self):
        content = self._read("NovaForge/Gameplay/Station/StationServices.h")
        self.assertIn("depositItems", content)

    def test_station_services_has_withdraw_items(self):
        content = self._read("NovaForge/Gameplay/Station/StationServices.h")
        self.assertIn("withdrawItems", content)

    def test_station_services_has_repair_ship(self):
        content = self._read("NovaForge/Gameplay/Station/StationServices.h")
        self.assertIn("repairShip", content)

    def test_station_services_has_resupply(self):
        content = self._read("NovaForge/Gameplay/Station/StationServices.h")
        self.assertIn("resupply", content)

    def test_station_services_has_query_storage(self):
        content = self._read("NovaForge/Gameplay/Station/StationServices.h")
        self.assertIn("queryStorage", content)


class TestManufacturingSourceFilesExist(unittest.TestCase):
    """Verify manufacturing queue source files are present."""

    def _check(self, relative_path: str):
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing source file: {relative_path}")

    def test_manufacturing_queue_header(self):
        self._check("NovaForge/Gameplay/Manufacturing/ManufacturingQueue.h")

    def test_manufacturing_queue_source(self):
        self._check("NovaForge/Gameplay/Manufacturing/ManufacturingQueue.cpp")


class TestManufacturingHeaderContent(unittest.TestCase):
    """Verify manufacturing queue header contains expected declarations."""

    def _read(self, path: str) -> str:
        return (REPO_ROOT / path).read_text(encoding="utf-8")

    def test_manufacturing_has_job_status_enum(self):
        content = self._read("NovaForge/Gameplay/Manufacturing/ManufacturingQueue.h")
        self.assertIn("EJobStatus", content)

    def test_manufacturing_has_recipe_definition(self):
        content = self._read("NovaForge/Gameplay/Manufacturing/ManufacturingQueue.h")
        self.assertIn("RecipeDefinition", content)

    def test_manufacturing_has_manufacturing_job(self):
        content = self._read("NovaForge/Gameplay/Manufacturing/ManufacturingQueue.h")
        self.assertIn("ManufacturingJob", content)

    def test_manufacturing_has_queue_job(self):
        content = self._read("NovaForge/Gameplay/Manufacturing/ManufacturingQueue.h")
        self.assertIn("queueJob", content)

    def test_manufacturing_has_tick(self):
        content = self._read("NovaForge/Gameplay/Manufacturing/ManufacturingQueue.h")
        self.assertIn("tick", content)

    def test_manufacturing_has_cancel_job(self):
        content = self._read("NovaForge/Gameplay/Manufacturing/ManufacturingQueue.h")
        self.assertIn("cancelJob", content)

    def test_manufacturing_has_collect_completed(self):
        content = self._read("NovaForge/Gameplay/Manufacturing/ManufacturingQueue.h")
        self.assertIn("collectCompleted", content)

    def test_manufacturing_has_register_recipe(self):
        content = self._read("NovaForge/Gameplay/Manufacturing/ManufacturingQueue.h")
        self.assertIn("registerRecipe", content)


class TestContractRewardSourceFilesExist(unittest.TestCase):
    """Verify contract reward system source files are present."""

    def _check(self, relative_path: str):
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing source file: {relative_path}")

    def test_contract_reward_system_header(self):
        self._check("NovaForge/Gameplay/Missions/ContractRewardSystem.h")

    def test_contract_reward_system_source(self):
        self._check("NovaForge/Gameplay/Missions/ContractRewardSystem.cpp")


class TestContractRewardHeaderContent(unittest.TestCase):
    """Verify contract reward header contains expected declarations."""

    def _read(self, path: str) -> str:
        return (REPO_ROOT / path).read_text(encoding="utf-8")

    def test_contract_reward_has_contract_reward_struct(self):
        content = self._read("NovaForge/Gameplay/Missions/ContractRewardSystem.h")
        self.assertIn("ContractReward", content)

    def test_contract_reward_has_credits_awarded(self):
        content = self._read("NovaForge/Gameplay/Missions/ContractRewardSystem.h")
        self.assertIn("creditsAwarded", content)

    def test_contract_reward_has_faction_standing_delta(self):
        content = self._read("NovaForge/Gameplay/Missions/ContractRewardSystem.h")
        self.assertIn("factionStandingDelta", content)

    def test_contract_reward_has_award_credits(self):
        content = self._read("NovaForge/Gameplay/Missions/ContractRewardSystem.h")
        self.assertIn("awardCredits", content)

    def test_contract_reward_has_award_faction_standing(self):
        content = self._read("NovaForge/Gameplay/Missions/ContractRewardSystem.h")
        self.assertIn("awardFactionStanding", content)

    def test_contract_reward_has_award_skill_xp(self):
        content = self._read("NovaForge/Gameplay/Missions/ContractRewardSystem.h")
        self.assertIn("awardSkillXp", content)

    def test_contract_reward_has_complete_contract(self):
        content = self._read("NovaForge/Gameplay/Missions/ContractRewardSystem.h")
        self.assertIn("completeContract", content)

    def test_contract_reward_has_update_contract_gates(self):
        content = self._read("NovaForge/Gameplay/Missions/ContractRewardSystem.h")
        self.assertIn("updateContractGates", content)


class TestGameplayDataDefinitionsExist(unittest.TestCase):
    """Verify JSON data definition files for gameplay loop systems."""

    def _load_json(self, relative_path: str) -> dict:
        full = REPO_ROOT / relative_path
        self.assertTrue(full.exists(), f"Missing file: {relative_path}")
        return json.loads(full.read_text(encoding="utf-8"))

    # Salvage loot tables
    def test_salvage_loot_tables_exists(self):
        self._load_json("NovaForge/Data/Definitions/Salvage/default_salvage_loot_tables.json")

    def test_salvage_loot_tables_has_version(self):
        data = self._load_json("NovaForge/Data/Definitions/Salvage/default_salvage_loot_tables.json")
        self.assertIn("version", data)

    def test_salvage_loot_tables_has_tables(self):
        data = self._load_json("NovaForge/Data/Definitions/Salvage/default_salvage_loot_tables.json")
        self.assertIn("loot_tables", data)
        self.assertIsInstance(data["loot_tables"], list)
        self.assertGreater(len(data["loot_tables"]), 0)

    def test_salvage_loot_tables_entries_have_item_id(self):
        data = self._load_json("NovaForge/Data/Definitions/Salvage/default_salvage_loot_tables.json")
        for table in data["loot_tables"]:
            for entry in table["entries"]:
                self.assertIn("item_id", entry)

    def test_salvage_loot_tables_entries_have_drop_chance(self):
        data = self._load_json("NovaForge/Data/Definitions/Salvage/default_salvage_loot_tables.json")
        for table in data["loot_tables"]:
            for entry in table["entries"]:
                self.assertIn("drop_chance", entry)
                self.assertGreaterEqual(entry["drop_chance"], 0.0)
                self.assertLessEqual(entry["drop_chance"], 1.0)

    # Station config
    def test_station_config_exists(self):
        self._load_json("NovaForge/Data/Definitions/Station/default_station_config.json")

    def test_station_config_has_version(self):
        data = self._load_json("NovaForge/Data/Definitions/Station/default_station_config.json")
        self.assertIn("version", data)

    def test_station_config_has_stations(self):
        data = self._load_json("NovaForge/Data/Definitions/Station/default_station_config.json")
        self.assertIn("stations", data)
        self.assertIsInstance(data["stations"], list)
        self.assertGreater(len(data["stations"]), 0)

    def test_station_config_stations_have_id(self):
        data = self._load_json("NovaForge/Data/Definitions/Station/default_station_config.json")
        for s in data["stations"]:
            self.assertIn("station_id", s)

    def test_station_config_has_manufacturing_recipes(self):
        data = self._load_json("NovaForge/Data/Definitions/Station/default_station_config.json")
        self.assertIn("manufacturing_recipes", data)
        self.assertIsInstance(data["manufacturing_recipes"], list)
        self.assertGreater(len(data["manufacturing_recipes"]), 0)

    def test_station_config_recipes_have_ingredients(self):
        data = self._load_json("NovaForge/Data/Definitions/Station/default_station_config.json")
        for recipe in data["manufacturing_recipes"]:
            self.assertIn("ingredients", recipe)

    # Contract rewards
    def test_contract_rewards_exists(self):
        self._load_json("NovaForge/Data/Definitions/Missions/default_contract_rewards.json")

    def test_contract_rewards_has_version(self):
        data = self._load_json("NovaForge/Data/Definitions/Missions/default_contract_rewards.json")
        self.assertIn("version", data)

    def test_contract_rewards_has_reward_tiers(self):
        data = self._load_json("NovaForge/Data/Definitions/Missions/default_contract_rewards.json")
        self.assertIn("reward_tiers", data)
        self.assertIsInstance(data["reward_tiers"], list)
        self.assertGreater(len(data["reward_tiers"]), 0)

    def test_contract_rewards_tiers_have_credits_base(self):
        data = self._load_json("NovaForge/Data/Definitions/Missions/default_contract_rewards.json")
        for tier in data["reward_tiers"]:
            self.assertIn("credits_base", tier)

    def test_contract_rewards_has_standing_gates(self):
        data = self._load_json("NovaForge/Data/Definitions/Missions/default_contract_rewards.json")
        self.assertIn("standing_gates", data)

    def test_contract_rewards_tiers_have_tier_field(self):
        data = self._load_json("NovaForge/Data/Definitions/Missions/default_contract_rewards.json")
        for tier in data["reward_tiers"]:
            self.assertIn("tier", tier)


class TestGameplayCMakeListsUpdated(unittest.TestCase):
    """Verify NovaForge/Gameplay/CMakeLists.txt includes new gameplay loop sources."""

    def _cmake(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/CMakeLists.txt").read_text(encoding="utf-8")

    def test_cmake_includes_salvage_system(self):
        self.assertIn("SalvageSystem.cpp", self._cmake())

    def test_cmake_includes_station_services(self):
        self.assertIn("StationServices.cpp", self._cmake())

    def test_cmake_includes_manufacturing_queue(self):
        self.assertIn("ManufacturingQueue.cpp", self._cmake())

    def test_cmake_includes_contract_reward_system(self):
        self.assertIn("ContractRewardSystem.cpp", self._cmake())


if __name__ == "__main__":
    unittest.main()
