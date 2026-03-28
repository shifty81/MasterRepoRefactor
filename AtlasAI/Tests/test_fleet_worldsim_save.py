"""Tests for Fleet system, WorldSim, SaveSystem, and AssetPipeline."""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# =============================================================================
# Fleet System (D4)
# =============================================================================

class TestFleetSourceFilesExist(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_fleet_types_header(self):
        self._check("NovaForge/Gameplay/Fleet/FleetTypes.h")

    def test_fleet_system_header(self):
        self._check("NovaForge/Gameplay/Fleet/FleetSystem.h")

    def test_fleet_system_source(self):
        self._check("NovaForge/Gameplay/Fleet/FleetSystem.cpp")


class TestFleetTypesContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/Fleet/FleetTypes.h").read_text(encoding="utf-8")

    def test_has_fleet_role_enum(self):
        self.assertIn("EFleetRole", self._read())

    def test_has_fleet_status_enum(self):
        self.assertIn("EFleetStatus", self._read())

    def test_has_fleet_ship(self):
        self.assertIn("FleetShip", self._read())

    def test_has_fleet_record(self):
        self.assertIn("FleetRecord", self._read())

    def test_has_fleet_assignment(self):
        self.assertIn("FleetAssignment", self._read())

    def test_has_income_per_tick(self):
        self.assertIn("incomePerTick", self._read())

    def test_has_risk_level(self):
        self.assertIn("riskLevel", self._read())


class TestFleetSystemContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/Fleet/FleetSystem.h").read_text(encoding="utf-8")

    def test_has_create_fleet(self):
        self.assertIn("createFleet", self._read())

    def test_has_add_ship(self):
        self.assertIn("addShip", self._read())

    def test_has_assign_to_mission(self):
        self.assertIn("assignToMission", self._read())

    def test_has_release_from_mission(self):
        self.assertIn("releaseFromMission", self._read())

    def test_has_recalculate_income_and_risk(self):
        self.assertIn("recalculateIncomeAndRisk", self._read())

    def test_has_tick(self):
        self.assertIn("tick", self._read())

    def test_has_move_to(self):
        self.assertIn("moveTo", self._read())

    def test_has_list_fleets(self):
        self.assertIn("listFleets", self._read())


class TestFleetDataDefinitionExists(unittest.TestCase):
    def _load(self, path: str) -> dict:
        full = REPO_ROOT / path
        self.assertTrue(full.exists(), f"Missing: {path}")
        return json.loads(full.read_text(encoding="utf-8"))

    def test_fleet_config_exists(self):
        self._load("NovaForge/Data/Definitions/Fleet/default_fleet_config.json")

    def test_fleet_config_has_version(self):
        d = self._load("NovaForge/Data/Definitions/Fleet/default_fleet_config.json")
        self.assertIn("version", d)

    def test_fleet_config_has_fleet_definitions(self):
        d = self._load("NovaForge/Data/Definitions/Fleet/default_fleet_config.json")
        self.assertIn("fleet_definitions", d)
        self.assertIsInstance(d["fleet_definitions"], list)
        self.assertGreater(len(d["fleet_definitions"]), 0)

    def test_fleet_definitions_have_ships(self):
        d = self._load("NovaForge/Data/Definitions/Fleet/default_fleet_config.json")
        for fleet in d["fleet_definitions"]:
            self.assertIn("ships", fleet)

    def test_fleet_config_has_sector_risk_modifiers(self):
        d = self._load("NovaForge/Data/Definitions/Fleet/default_fleet_config.json")
        self.assertIn("sector_risk_modifiers", d)


# =============================================================================
# WorldSim (D4)
# =============================================================================

class TestWorldSimSourceFilesExist(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_world_sim_types_header(self):
        self._check("NovaForge/Gameplay/WorldSim/WorldSimTypes.h")

    def test_world_sim_system_header(self):
        self._check("NovaForge/Gameplay/WorldSim/WorldSimSystem.h")

    def test_world_sim_system_source(self):
        self._check("NovaForge/Gameplay/WorldSim/WorldSimSystem.cpp")


class TestWorldSimTypesContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/WorldSim/WorldSimTypes.h").read_text(encoding="utf-8")

    def test_has_sector_control_enum(self):
        self.assertIn("ESectorControl", self._read())

    def test_has_sector_state(self):
        self.assertIn("SectorState", self._read())

    def test_has_anomaly_type_enum(self):
        self.assertIn("EAnomalyType", self._read())

    def test_has_anomaly_event(self):
        self.assertIn("AnomalyEvent", self._read())

    def test_has_titan_race_state(self):
        self.assertIn("TitanRaceState", self._read())

    def test_has_opportunity_level(self):
        self.assertIn("opportunityLevel", self._read())

    def test_has_danger_level(self):
        self.assertIn("dangerLevel", self._read())


class TestWorldSimSystemContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/WorldSim/WorldSimSystem.h").read_text(encoding="utf-8")

    def test_has_register_sector(self):
        self.assertIn("registerSector", self._read())

    def test_has_update_sector_control(self):
        self.assertIn("updateSectorControl", self._read())

    def test_has_set_war_active(self):
        self.assertIn("setWarActive", self._read())

    def test_has_spawn_anomaly(self):
        self.assertIn("spawnAnomaly", self._read())

    def test_has_resolve_anomaly(self):
        self.assertIn("resolveAnomaly", self._read())

    def test_has_advance_titan_phase(self):
        self.assertIn("advanceTitanPhase", self._read())

    def test_has_get_global_pressure(self):
        self.assertIn("getGlobalPressure", self._read())

    def test_has_list_war_zones(self):
        self.assertIn("listWarZones", self._read())


class TestWorldSimDataDefinitionExists(unittest.TestCase):
    def _load(self, path: str) -> dict:
        full = REPO_ROOT / path
        self.assertTrue(full.exists(), f"Missing: {path}")
        return json.loads(full.read_text(encoding="utf-8"))

    def test_world_sim_config_exists(self):
        self._load("NovaForge/Data/Definitions/WorldSim/default_world_sim_config.json")

    def test_world_sim_config_has_sectors(self):
        d = self._load("NovaForge/Data/Definitions/WorldSim/default_world_sim_config.json")
        self.assertIn("sectors", d)
        self.assertGreater(len(d["sectors"]), 0)

    def test_world_sim_config_sectors_have_danger_level(self):
        d = self._load("NovaForge/Data/Definitions/WorldSim/default_world_sim_config.json")
        for s in d["sectors"]:
            self.assertIn("danger_level", s)

    def test_world_sim_config_has_titan_race(self):
        d = self._load("NovaForge/Data/Definitions/WorldSim/default_world_sim_config.json")
        self.assertIn("titan_race", d)

    def test_world_sim_config_has_anomaly_types(self):
        d = self._load("NovaForge/Data/Definitions/WorldSim/default_world_sim_config.json")
        self.assertIn("anomaly_types", d)
        self.assertGreater(len(d["anomaly_types"]), 0)


# =============================================================================
# SaveSystem (B3)
# =============================================================================

class TestSaveSystemSourceFilesExist(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_save_system_header(self):
        self._check("NovaForge/Save/include/SaveSystem.h")

    def test_save_system_source(self):
        self._check("NovaForge/Save/src/SaveSystem.cpp")


class TestSaveSystemContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Save/include/SaveSystem.h").read_text(encoding="utf-8")

    def test_has_saved_player_state(self):
        self.assertIn("SavedPlayerState", self._read())

    def test_has_saved_voxel_chunk(self):
        self.assertIn("SavedVoxelChunk", self._read())

    def test_has_saved_economy_state(self):
        self.assertIn("SavedEconomyState", self._read())

    def test_has_saved_contract_state(self):
        self.assertIn("SavedContractState", self._read())

    def test_has_save_bundle(self):
        self.assertIn("SaveBundle", self._read())

    def test_has_save_player(self):
        self.assertIn("savePlayer", self._read())

    def test_has_save_voxel_chunk(self):
        self.assertIn("saveVoxelChunk", self._read())

    def test_has_save_economy(self):
        self.assertIn("saveEconomy", self._read())

    def test_has_save_contracts(self):
        self.assertIn("saveContracts", self._read())

    def test_has_flush_to_slot(self):
        self.assertIn("flushToSlot", self._read())

    def test_has_load_from_slot(self):
        self.assertIn("loadFromSlot", self._read())

    def test_has_validate_bundle(self):
        self.assertIn("validateBundle", self._read())

    def test_has_max_slots(self):
        self.assertIn("kMaxSlots", self._read())


class TestSaveCMakeUpdated(unittest.TestCase):
    def _cmake(self) -> str:
        return (REPO_ROOT / "NovaForge/Save/CMakeLists.txt").read_text(encoding="utf-8")

    def test_cmake_includes_save_system(self):
        self.assertIn("SaveSystem.cpp", self._cmake())


# =============================================================================
# Asset Pipeline (F1)
# =============================================================================

class TestAssetPipelineSourceFilesExist(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_asset_naming_rules_header(self):
        self._check("Atlas/Engine/AssetPipeline/AssetNamingRules.h")

    def test_asset_naming_rules_source(self):
        self._check("Atlas/Engine/AssetPipeline/AssetNamingRules.cpp")

    def test_asset_import_validator_header(self):
        self._check("Atlas/Engine/AssetPipeline/AssetImportValidator.h")

    def test_asset_import_validator_source(self):
        self._check("Atlas/Engine/AssetPipeline/AssetImportValidator.cpp")


class TestAssetNamingRulesContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Engine/AssetPipeline/AssetNamingRules.h").read_text(encoding="utf-8")

    def test_has_asset_type_rule(self):
        self.assertIn("AssetTypeRule", self._read())

    def test_has_validate_name(self):
        self.assertIn("ValidateName", self._read())

    def test_has_validate_path(self):
        self.assertIn("ValidatePath", self._read())

    def test_has_get_rules(self):
        self.assertIn("GetRules", self._read())


class TestAssetImportValidatorContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Engine/AssetPipeline/AssetImportValidator.h").read_text(encoding="utf-8")

    def test_has_import_issue_level(self):
        self.assertIn("EImportIssueLevel", self._read())

    def test_has_import_issue(self):
        self.assertIn("ImportIssue", self._read())

    def test_has_import_validation_result(self):
        self.assertIn("ImportValidationResult", self._read())

    def test_has_validate(self):
        self.assertIn("Validate", self._read())

    def test_has_validate_batch(self):
        self.assertIn("ValidateBatch", self._read())

    def test_has_is_import_allowed(self):
        self.assertIn("IsImportAllowed", self._read())


class TestAtlasEngineCMakeUpdated(unittest.TestCase):
    def _cmake(self) -> str:
        return (REPO_ROOT / "Atlas/Engine/CMakeLists.txt").read_text(encoding="utf-8")

    def test_cmake_includes_naming_rules(self):
        self.assertIn("AssetNamingRules.cpp", self._cmake())

    def test_cmake_includes_import_validator(self):
        self.assertIn("AssetImportValidator.cpp", self._cmake())

    def test_cmake_includes_asset_pipeline_dir(self):
        self.assertIn("AssetPipeline", self._cmake())


# =============================================================================
# Gameplay CMakeLists updates
# =============================================================================

class TestGameplayCMakeUpdated(unittest.TestCase):
    def _cmake(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/CMakeLists.txt").read_text(encoding="utf-8")

    def test_cmake_includes_fleet_system(self):
        self.assertIn("FleetSystem.cpp", self._cmake())

    def test_cmake_includes_world_sim_system(self):
        self.assertIn("WorldSimSystem.cpp", self._cmake())


if __name__ == "__main__":
    unittest.main()
