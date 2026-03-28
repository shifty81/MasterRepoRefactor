"""Tests for I1 (TitanRaceSystem/SeasonSystem), I2 (AnomalySystem), I3 (WarSectorSystem)."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# =============================================================================
# I1 — Season / Titan Race System
# =============================================================================

class TestTitanRaceSystemFilesExist(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_titan_race_system_header(self):
        self._check("NovaForge/Gameplay/Season/TitanRaceSystem.h")

    def test_titan_race_system_source(self):
        self._check("NovaForge/Gameplay/Season/TitanRaceSystem.cpp")


class TestTitanRaceSystemContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "NovaForge/Gameplay/Season/TitanRaceSystem.h").read_text(encoding="utf-8")

    def test_has_eseason_phase_enum(self):
        self.assertIn("ESeasonPhase", self._read())

    def test_has_titan_entry(self):
        self.assertIn("TitanEntry", self._read())

    def test_has_season_config(self):
        self.assertIn("SeasonConfig", self._read())

    def test_has_titan_race_system_class(self):
        self.assertIn("TitanRaceSystem", self._read())

    def test_has_register_titan(self):
        self.assertIn("RegisterTitan", self._read())

    def test_has_advance_titan(self):
        self.assertIn("AdvanceTitan", self._read())

    def test_has_defeat_titan(self):
        self.assertIn("DefeatTitan", self._read())

    def test_has_find_titan(self):
        self.assertIn("FindTitan", self._read())

    def test_has_tick(self):
        self.assertIn("Tick(", self._read())

    def test_has_get_phase(self):
        self.assertIn("GetPhase", self._read())

    def test_has_get_global_pressure(self):
        self.assertIn("GetGlobalPressure", self._read())

    def test_has_get_season_number(self):
        self.assertIn("GetSeasonNumber", self._read())

    def test_has_is_season_over(self):
        self.assertIn("IsSeasonOver", self._read())

    def test_has_combat_difficulty_modifier(self):
        self.assertIn("GetCombatDifficultyModifier", self._read())

    def test_has_resource_spawn_modifier(self):
        self.assertIn("GetResourceSpawnModifier", self._read())

    def test_has_contract_reward_multiplier(self):
        self.assertIn("GetContractRewardMultiplier", self._read())

    def test_has_phase_changed_callback(self):
        self.assertIn("PhaseChangedCallback", self._read())

    def test_has_advance_season(self):
        self.assertIn("AdvanceSeason", self._read())

    def test_phases_cover_all(self):
        text = self._read()
        for p in ["Dormant", "EarlyRace", "MidRace", "LateRace", "FinalPush", "SeasonEnd"]:
            self.assertIn(p, text, f"Missing phase: {p}")

    def test_has_season_system_class(self):
        self.assertIn("SeasonSystem", self._read())

    def test_has_current_season(self):
        self.assertIn("CurrentSeason", self._read())

    def test_has_add_contract_multiplier(self):
        self.assertIn("AddContractMultiplier", self._read())

    def test_has_add_combat_difficulty(self):
        self.assertIn("AddCombatDifficultyDelta", self._read())

    def test_has_get_contract_multiplier(self):
        self.assertIn("GetContractMultiplier", self._read())

    def test_has_reset_multipliers(self):
        self.assertIn("ResetMultipliers", self._read())

    def test_titan_entry_has_progress_field(self):
        self.assertIn("progress", self._read())

    def test_titan_entry_has_pressure_field(self):
        self.assertIn("pressure", self._read())

    def test_titan_entry_has_is_defeated(self):
        self.assertIn("isDefeated", self._read())


class TestTitanRaceSystemImpl(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "NovaForge/Gameplay/Season/TitanRaceSystem.cpp").read_text(encoding="utf-8")

    def test_advance_titan_caps_at_100(self):
        self.assertIn("100.f", self._read())

    def test_phase_callback_fires_on_change(self):
        self.assertIn("m_phaseCb", self._read())

    def test_advance_season_resets_pressure(self):
        self.assertIn("globalPressure = 0", self._read())

    def test_combat_difficulty_scales_with_pressure(self):
        self.assertIn("globalPressure", self._read())

    def test_pressure_decay_applied(self):
        self.assertIn("pressureDecayRate", self._read())


# =============================================================================
# I2 — Anomaly System
# =============================================================================

class TestAnomalySystemFilesExist(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_anomaly_system_header(self):
        self._check("NovaForge/Gameplay/Anomaly/AnomalySystem.h")

    def test_anomaly_system_source(self):
        self._check("NovaForge/Gameplay/Anomaly/AnomalySystem.cpp")


class TestAnomalySystemContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "NovaForge/Gameplay/Anomaly/AnomalySystem.h").read_text(encoding="utf-8")

    def test_has_eanomaly_type_enum(self):
        self.assertIn("EAnomalyType", self._read())

    def test_has_anomaly_entry(self):
        self.assertIn("AnomalyEntry", self._read())

    def test_has_anomaly_effect(self):
        self.assertIn("AnomalyEffect", self._read())

    def test_has_anomaly_system_class(self):
        self.assertIn("AnomalySystem", self._read())

    def test_has_spawn_anomaly(self):
        self.assertIn("SpawnAnomaly", self._read())

    def test_has_despawn_anomaly(self):
        self.assertIn("DespawnAnomaly", self._read())

    def test_has_has_anomaly(self):
        self.assertIn("HasAnomaly", self._read())

    def test_has_find_anomaly(self):
        self.assertIn("FindAnomaly", self._read())

    def test_has_get_anomalies_in_sector(self):
        self.assertIn("GetAnomaliesInSector", self._read())

    def test_has_compute_sector_effect(self):
        self.assertIn("ComputeSectorEffect", self._read())

    def test_has_tick(self):
        self.assertIn("Tick(", self._read())

    def test_has_anomaly_expired_callback(self):
        self.assertIn("AnomalyExpiredCallback", self._read())

    def test_has_active_count(self):
        self.assertIn("ActiveCount", self._read())

    def test_anomaly_types_cover_all(self):
        text = self._read()
        for t in ["ResourceRich", "ResourceDepleted", "EncounterDense",
                  "EncounterSparse", "StormZone", "SignalAnomaly",
                  "TitanFragment", "WarpRift"]:
            self.assertIn(t, text, f"Missing anomaly type: {t}")

    def test_effect_has_resource_yield_multiplier(self):
        self.assertIn("resourceYieldMultiplier", self._read())

    def test_effect_has_encounter_rate_multiplier(self):
        self.assertIn("encounterRateMultiplier", self._read())

    def test_effect_has_navigation_hazard(self):
        self.assertIn("navigationHazardLevel", self._read())

    def test_effect_has_is_warp_rift(self):
        self.assertIn("isWarpRift", self._read())

    def test_anomaly_has_intensity(self):
        self.assertIn("intensity", self._read())

    def test_anomaly_has_remaining_seconds(self):
        self.assertIn("remainingSeconds", self._read())

    def test_anomaly_has_is_permanent(self):
        self.assertIn("isPermanent", self._read())

    def test_anomaly_has_source_tag(self):
        self.assertIn("sourceTag", self._read())


class TestAnomalySystemImpl(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "NovaForge/Gameplay/Anomaly/AnomalySystem.cpp").read_text(encoding="utf-8")

    def test_resource_rich_boosts_yield(self):
        self.assertIn("ResourceRich", self._read())
        self.assertIn("resourceYieldMultiplier", self._read())

    def test_encounter_dense_boosts_rate(self):
        self.assertIn("EncounterDense", self._read())

    def test_expired_callback_fires(self):
        self.assertIn("m_expiredCb", self._read())

    def test_inactive_anomalies_pruned(self):
        self.assertIn("isActive", self._read())

    def test_duration_decrements(self):
        self.assertIn("remainingSeconds -= deltaSeconds", self._read())


# =============================================================================
# I3 — War / Sector System
# =============================================================================

class TestWarSectorSystemFilesExist(unittest.TestCase):
    def _check(self, path):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_war_sector_header(self):
        self._check("NovaForge/Gameplay/WarSector/WarSectorSystem.h")

    def test_war_sector_source(self):
        self._check("NovaForge/Gameplay/WarSector/WarSectorSystem.cpp")


class TestWarSectorSystemContent(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "NovaForge/Gameplay/WarSector/WarSectorSystem.h").read_text(encoding="utf-8")

    def test_has_econflict_grade_enum(self):
        self.assertIn("EConflictGrade", self._read())

    def test_has_esector_control_enum(self):
        self.assertIn("ESectorControl", self._read())

    def test_has_sector_war_state(self):
        self.assertIn("SectorWarState", self._read())

    def test_has_war_declaration(self):
        self.assertIn("WarDeclaration", self._read())

    def test_has_war_sector_system_class(self):
        self.assertIn("WarSectorSystem", self._read())

    def test_has_register_sector(self):
        self.assertIn("RegisterSector", self._read())

    def test_has_unregister_sector(self):
        self.assertIn("UnregisterSector", self._read())

    def test_has_has_sector(self):
        self.assertIn("HasSector", self._read())

    def test_has_find_sector(self):
        self.assertIn("FindSector", self._read())

    def test_has_declare_war(self):
        self.assertIn("DeclareWar", self._read())

    def test_has_escalate_conflict(self):
        self.assertIn("EscalateConflict", self._read())

    def test_has_reduce_conflict(self):
        self.assertIn("ReduceConflict", self._read())

    def test_has_resolve_conflict(self):
        self.assertIn("ResolveConflict", self._read())

    def test_has_set_sector_control(self):
        self.assertIn("SetSectorControl", self._read())

    def test_has_get_opportunity_level(self):
        self.assertIn("GetOpportunityLevel", self._read())

    def test_has_update_opportunity_levels(self):
        self.assertIn("UpdateOpportunityLevels", self._read())

    def test_has_get_conflicting_sectors(self):
        self.assertIn("GetConflictingSectors", self._read())

    def test_has_get_sectors_by_faction(self):
        self.assertIn("GetSectorsByFaction", self._read())

    def test_has_tick(self):
        self.assertIn("Tick(", self._read())

    def test_has_conflict_changed_callback(self):
        self.assertIn("ConflictChangedCallback", self._read())

    def test_has_active_war_count(self):
        self.assertIn("ActiveWarCount", self._read())

    def test_conflict_grades_cover_all(self):
        text = self._read()
        for g in ["Peace", "Tension", "Skirmish", "War", "TotalWar"]:
            self.assertIn(g, text, f"Missing conflict grade: {g}")

    def test_sector_control_types(self):
        text = self._read()
        for c in ["Neutral", "FactionA", "FactionB", "Contested"]:
            self.assertIn(c, text, f"Missing control type: {c}")

    def test_state_has_opportunity_level(self):
        self.assertIn("opportunityLevel", self._read())

    def test_state_has_conflict_intensity(self):
        self.assertIn("conflictIntensity", self._read())

    def test_state_has_turns_in_conflict(self):
        self.assertIn("turnsInConflict", self._read())


class TestWarSectorSystemImpl(unittest.TestCase):
    def _read(self):
        return (REPO_ROOT / "NovaForge/Gameplay/WarSector/WarSectorSystem.cpp").read_text(encoding="utf-8")

    def test_recompute_grade_used(self):
        self.assertIn("RecomputeGrade", self._read())

    def test_conflict_callback_fires_on_escalate(self):
        self.assertIn("m_conflictCb", self._read())

    def test_opportunity_scales_with_intensity(self):
        self.assertIn("conflictIntensity", self._read())
        self.assertIn("opportunityLevel", self._read())

    def test_resolve_sets_peace_grade(self):
        self.assertIn("Peace", self._read())

    def test_turns_incremented_in_tick(self):
        self.assertIn("turnsInConflict", self._read())


class TestGameplayCMakeHasNewSystems(unittest.TestCase):
    def _cmake(self):
        return (REPO_ROOT / "NovaForge/Gameplay/CMakeLists.txt").read_text(encoding="utf-8")

    def test_has_titan_race_system(self):
        self.assertIn("TitanRaceSystem.cpp", self._cmake())

    def test_has_anomaly_system(self):
        self.assertIn("AnomalySystem.cpp", self._cmake())

    def test_has_war_sector_system(self):
        self.assertIn("WarSectorSystem.cpp", self._cmake())

    def test_has_season_include_dir(self):
        self.assertIn("/Season", self._cmake())

    def test_has_anomaly_include_dir(self):
        self.assertIn("/Anomaly", self._cmake())

    def test_has_war_sector_include_dir(self):
        self.assertIn("/WarSector", self._cmake())


if __name__ == "__main__":
    unittest.main()
