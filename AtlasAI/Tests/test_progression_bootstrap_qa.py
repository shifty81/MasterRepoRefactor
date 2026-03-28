"""Tests for D3 (ProgressionRewardSystem) and A2 (WorldBootstrap)."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# =============================================================================
# D3 — ProgressionRewardSystem
# =============================================================================

class TestProgressionRewardFilesExist(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_progression_reward_system_header(self):
        self._check("NovaForge/Gameplay/Progression/ProgressionRewardSystem.h")

    def test_progression_reward_system_source(self):
        self._check("NovaForge/Gameplay/Progression/ProgressionRewardSystem.cpp")


class TestProgressionRewardContent(unittest.TestCase):
    def _read(self) -> str:
        return (
            REPO_ROOT / "NovaForge/Gameplay/Progression/ProgressionRewardSystem.h"
        ).read_text(encoding="utf-8")

    def test_has_contract_reward_payload(self):
        self.assertIn("ContractRewardPayload", self._read())

    def test_has_contract_gate_requirement(self):
        self.assertIn("ContractGateRequirement", self._read())

    def test_has_player_progression_record(self):
        self.assertIn("PlayerProgressionRecord", self._read())

    def test_has_apply_contract_reward(self):
        self.assertIn("applyContractReward", self._read())

    def test_has_award_credits(self):
        self.assertIn("awardCredits", self._read())

    def test_has_apply_faction_standing(self):
        self.assertIn("applyFactionStanding", self._read())

    def test_has_award_skill_xp(self):
        self.assertIn("awardSkillXP", self._read())

    def test_has_meets_gating_requirements(self):
        self.assertIn("meetsGatingRequirements", self._read())

    def test_has_get_credits(self):
        self.assertIn("getCredits", self._read())

    def test_has_get_faction_standing(self):
        self.assertIn("getFactionStanding", self._read())

    def test_has_get_skill_level(self):
        self.assertIn("getSkillLevel", self._read())

    def test_has_register_gate(self):
        self.assertIn("registerGate", self._read())

    def test_has_credits_field(self):
        self.assertIn("credits", self._read())

    def test_has_faction_standing_field(self):
        self.assertIn("factionStanding", self._read())

    def test_has_skill_xp_field(self):
        self.assertIn("skillXP", self._read())

    def test_has_skill_id_field(self):
        self.assertIn("skillId", self._read())


class TestProgressionRewardImplContent(unittest.TestCase):
    def _read(self) -> str:
        return (
            REPO_ROOT / "NovaForge/Gameplay/Progression/ProgressionRewardSystem.cpp"
        ).read_text(encoding="utf-8")

    def test_awards_credits(self):
        self.assertIn("awardCredits", self._read())

    def test_applies_faction_standing(self):
        self.assertIn("applyFactionStanding", self._read())

    def test_awards_skill_xp(self):
        self.assertIn("awardSkillXP", self._read())

    def test_has_clamping_logic(self):
        # Faction standing should be clamped to [-10, +10].
        self.assertIn("10.f", self._read())

    def test_checks_gating_requirements(self):
        self.assertIn("meetsGatingRequirements", self._read())


# =============================================================================
# A2 — WorldBootstrap
# =============================================================================

class TestWorldBootstrapFilesExist(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_world_bootstrap_header(self):
        self._check("NovaForge/App/Bootstrap/WorldBootstrap.h")

    def test_world_bootstrap_source(self):
        self._check("NovaForge/App/Bootstrap/WorldBootstrap.cpp")


class TestWorldBootstrapContent(unittest.TestCase):
    def _read(self) -> str:
        return (
            REPO_ROOT / "NovaForge/App/Bootstrap/WorldBootstrap.h"
        ).read_text(encoding="utf-8")

    def test_has_eboot_phase_enum(self):
        self.assertIn("EBootPhase", self._read())

    def test_has_boot_phase_result(self):
        self.assertIn("BootPhaseResult", self._read())

    def test_has_phase_delegate(self):
        self.assertIn("PhaseDelegate", self._read())

    def test_has_world_bootstrap_class(self):
        self.assertIn("WorldBootstrap", self._read())

    def test_has_register_phase(self):
        self.assertIn("RegisterPhase", self._read())

    def test_has_run_all(self):
        self.assertIn("RunAll", self._read())

    def test_has_run_phase(self):
        self.assertIn("RunPhase", self._read())

    def test_has_is_ready(self):
        self.assertIn("IsReady", self._read())

    def test_has_has_failed(self):
        self.assertIn("HasFailed", self._read())

    def test_has_set_editor_mode(self):
        self.assertIn("SetEditorMode", self._read())

    def test_has_get_history(self):
        self.assertIn("GetHistory", self._read())

    def test_boot_phases_cover_critical_path(self):
        text = self._read()
        for phase in [
            "LoadConfig",
            "LoadDataRegistry",
            "InitialiseGameplaySystems",
            "LoadOrGenerateWorld",
            "SpawnPlayer",
            "BootstrapUI",
            "BootstrapEditor",
            "Ready",
            "Failed",
        ]:
            self.assertIn(phase, text, f"Missing boot phase: {phase}")


class TestWorldBootstrapImplContent(unittest.TestCase):
    def _read(self) -> str:
        return (
            REPO_ROOT / "NovaForge/App/Bootstrap/WorldBootstrap.cpp"
        ).read_text(encoding="utf-8")

    def test_run_all_returns_bool(self):
        self.assertIn("RunAll", self._read())

    def test_run_phase_invokes_delegate(self):
        self.assertIn("RunPhase", self._read())

    def test_skips_editor_phase_in_runtime_mode(self):
        self.assertIn("BootstrapEditor", self._read())
        self.assertIn("m_editorMode", self._read())

    def test_records_history(self):
        self.assertIn("m_history", self._read())

    def test_phase_order_defined(self):
        self.assertIn("kPhaseOrder", self._read())


class TestAppCMakeUpdated(unittest.TestCase):
    def _cmake(self) -> str:
        return (REPO_ROOT / "NovaForge/App/CMakeLists.txt").read_text(encoding="utf-8")

    def test_cmake_includes_world_bootstrap(self):
        self.assertIn("WorldBootstrap.cpp", self._cmake())

    def test_cmake_includes_bootstrap_dir(self):
        self.assertIn("Bootstrap", self._cmake())


# =============================================================================
# F2 — QA / Smoke Tests (structural)
# =============================================================================

class TestSaveSystemSmokeStructure(unittest.TestCase):
    """Verify the SaveSystem supports the full persistence path (B3 closure)."""

    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Save/include/SaveSystem.h").read_text(encoding="utf-8")

    def test_has_player_slot(self):
        self.assertIn("SavedPlayerState", self._read())

    def test_has_voxel_slot(self):
        self.assertIn("SavedVoxelChunk", self._read())

    def test_has_economy_slot(self):
        self.assertIn("SavedEconomyState", self._read())

    def test_has_contract_slot(self):
        self.assertIn("SavedContractState", self._read())

    def test_has_flush_and_load(self):
        text = self._read()
        self.assertIn("flushToSlot", text)
        self.assertIn("loadFromSlot", text)

    def test_has_validate_bundle(self):
        self.assertIn("validateBundle", self._read())

    def test_max_slots_defined(self):
        self.assertIn("kMaxSlots", self._read())


class TestPCGDeterminismSmokeStructure(unittest.TestCase):
    """Verify PCGWorldGen has seed-based deterministic generation API."""

    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/PCG/PCGWorldGen.h").read_text(encoding="utf-8")

    def test_has_world_seed(self):
        self.assertIn("worldSeed", self._read())

    def test_has_generate(self):
        self.assertIn("generate", self._read())

    def test_has_sector_count(self):
        self.assertIn("sectorCount", self._read())


class TestEconomyWorldSimSmokeStructure(unittest.TestCase):
    """Verify economy/WorldSim systems are structurally ready for smoke tests."""

    def _read_trade(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/Economy/TradeMarket.h").read_text(encoding="utf-8")

    def _read_worldsim(self) -> str:
        return (REPO_ROOT / "NovaForge/Gameplay/WorldSim/WorldSimSystem.h").read_text(encoding="utf-8")

    def test_trade_market_has_place_order(self):
        self.assertIn("placeOrder", self._read_trade())

    def test_trade_market_has_get_best_price(self):
        self.assertIn("getBestPrice", self._read_trade())

    def test_world_sim_has_tick(self):
        self.assertIn("tick", self._read_worldsim())

    def test_world_sim_has_titan_pressure(self):
        self.assertIn("getGlobalPressure", self._read_worldsim())


class TestUIFrameworkSmokeStructure(unittest.TestCase):
    """Verify RuntimeUIShell has the minimal HUD/message API."""

    def _read(self) -> str:
        return (REPO_ROOT / "NovaForge/UI/include/RuntimeUIShell.h").read_text(encoding="utf-8")

    def test_has_push_message(self):
        self.assertIn("PushMessage", self._read())

    def test_has_tick(self):
        self.assertIn("Tick", self._read())


if __name__ == "__main__":
    unittest.main()
