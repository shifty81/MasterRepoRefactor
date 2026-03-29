"""Phase 40D — Tests for AchievementBodyRegistry.h and achievement_body_loader.py."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    AchievementBodyLoader,
    AchievementBodyManifest,
    AchievementProgressManifest,
    AchievementRewardManifest,
)


def _read_header(name: str) -> str:
    return (SCENE_DIR / f"{name}.h").read_text()


# ---------------------------------------------------------------------------
# AchievementBodyRegistry.h
# ---------------------------------------------------------------------------

class TestAchievementBodyRegistryHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "AchievementBodyRegistry.h").exists())


class TestAchievementBodyRegistryNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("AchievementBodyRegistry"))


class TestAchievementBodyRegistryEnums(unittest.TestCase):
    def test_achievement_state_enum(self):
        self.assertIn("AchievementState", _read_header("AchievementBodyRegistry"))

    def test_achievement_scope_enum(self):
        self.assertIn("AchievementScope", _read_header("AchievementBodyRegistry"))

    def test_trigger_condition_type_enum(self):
        self.assertIn("TriggerConditionType", _read_header("AchievementBodyRegistry"))

    def test_reward_tier_type_enum(self):
        self.assertIn("RewardTierType", _read_header("AchievementBodyRegistry"))

    def test_achievement_flags_enum(self):
        self.assertIn("AchievementFlags", _read_header("AchievementBodyRegistry"))

    def test_locked_state_value(self):
        self.assertIn("Locked", _read_header("AchievementBodyRegistry"))

    def test_unlocked_state_value(self):
        self.assertIn("Unlocked", _read_header("AchievementBodyRegistry"))

    def test_story_scope_value(self):
        self.assertIn("Story", _read_header("AchievementBodyRegistry"))

    def test_combat_scope_value(self):
        self.assertIn("Combat", _read_header("AchievementBodyRegistry"))

    def test_gold_tier_value(self):
        self.assertIn("Gold", _read_header("AchievementBodyRegistry"))

    def test_hidden_flag_value(self):
        self.assertIn("Hidden", _read_header("AchievementBodyRegistry"))


class TestAchievementBodyRegistryStructs(unittest.TestCase):
    def test_achievement_progress_def_struct(self):
        self.assertIn("AchievementProgressDef", _read_header("AchievementBodyRegistry"))

    def test_achievement_reward_def_struct(self):
        self.assertIn("AchievementRewardDef", _read_header("AchievementBodyRegistry"))

    def test_achievement_body_record_struct(self):
        self.assertIn("AchievementBodyRecord", _read_header("AchievementBodyRegistry"))

    def test_target_value_in_progress(self):
        self.assertIn("targetValue", _read_header("AchievementBodyRegistry"))

    def test_xp_value_in_reward(self):
        self.assertIn("xpValue", _read_header("AchievementBodyRegistry"))

    def test_display_order_in_achievement(self):
        self.assertIn("displayOrder", _read_header("AchievementBodyRegistry"))


class TestAchievementBodyRegistryMethods(unittest.TestCase):
    def test_register_achievement(self):
        self.assertIn("RegisterAchievement", _read_header("AchievementBodyRegistry"))

    def test_unregister_achievement(self):
        self.assertIn("UnregisterAchievement", _read_header("AchievementBodyRegistry"))

    def test_set_achievement_scope(self):
        self.assertIn("SetAchievementScope", _read_header("AchievementBodyRegistry"))

    def test_set_achievement_state(self):
        self.assertIn("SetAchievementState", _read_header("AchievementBodyRegistry"))

    def test_unlock_achievement(self):
        self.assertIn("UnlockAchievement", _read_header("AchievementBodyRegistry"))

    def test_claim_achievement(self):
        self.assertIn("ClaimAchievement", _read_header("AchievementBodyRegistry"))

    def test_hide_achievement(self):
        self.assertIn("HideAchievement", _read_header("AchievementBodyRegistry"))

    def test_get_achievement_by_id(self):
        self.assertIn("GetAchievementById", _read_header("AchievementBodyRegistry"))

    def test_get_all_achievement_ids(self):
        self.assertIn("GetAllAchievementIds", _read_header("AchievementBodyRegistry"))

    def test_get_achievements_by_scope(self):
        self.assertIn("GetAchievementsByScope", _read_header("AchievementBodyRegistry"))

    def test_get_locked_achievements(self):
        self.assertIn("GetLockedAchievements", _read_header("AchievementBodyRegistry"))

    def test_get_unlocked_achievements(self):
        self.assertIn("GetUnlockedAchievements", _read_header("AchievementBodyRegistry"))

    def test_get_claimed_achievements(self):
        self.assertIn("GetClaimedAchievements", _read_header("AchievementBodyRegistry"))

    def test_get_in_progress_achievements(self):
        self.assertIn("GetInProgressAchievements", _read_header("AchievementBodyRegistry"))

    def test_add_progress(self):
        self.assertIn("AddProgress", _read_header("AchievementBodyRegistry"))

    def test_remove_progress(self):
        self.assertIn("RemoveProgress", _read_header("AchievementBodyRegistry"))

    def test_update_progress_value(self):
        self.assertIn("UpdateProgressValue", _read_header("AchievementBodyRegistry"))

    def test_satisfy_progress(self):
        self.assertIn("SatisfyProgress", _read_header("AchievementBodyRegistry"))

    def test_get_progress(self):
        self.assertIn("GetProgress", _read_header("AchievementBodyRegistry"))

    def test_get_progress_by_achievement(self):
        self.assertIn("GetProgressByAchievement", _read_header("AchievementBodyRegistry"))

    def test_get_satisfied_progress(self):
        self.assertIn("GetSatisfiedProgress", _read_header("AchievementBodyRegistry"))

    def test_add_reward(self):
        self.assertIn("AddReward", _read_header("AchievementBodyRegistry"))

    def test_remove_reward(self):
        self.assertIn("RemoveReward", _read_header("AchievementBodyRegistry"))

    def test_claim_reward(self):
        self.assertIn("ClaimReward", _read_header("AchievementBodyRegistry"))

    def test_get_reward(self):
        self.assertIn("GetReward", _read_header("AchievementBodyRegistry"))

    def test_get_rewards_by_achievement(self):
        self.assertIn("GetRewardsByAchievement", _read_header("AchievementBodyRegistry"))

    def test_get_unclaimed_rewards(self):
        self.assertIn("GetUnclaimedRewards", _read_header("AchievementBodyRegistry"))

    def test_get_rewards_by_tier(self):
        self.assertIn("GetRewardsByTier", _read_header("AchievementBodyRegistry"))

    def test_clear(self):
        self.assertIn("Clear", _read_header("AchievementBodyRegistry"))

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_header("AchievementBodyRegistry"))

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_header("AchievementBodyRegistry"))


# ---------------------------------------------------------------------------
# AchievementProgressManifest
# ---------------------------------------------------------------------------

class TestAchievementProgressManifest(unittest.TestCase):
    def test_progress_id(self):
        p = AchievementProgressManifest(progress_id="prog_001", achievement_id="ach_001")
        self.assertEqual(p.progress_id, "prog_001")

    def test_achievement_id(self):
        p = AchievementProgressManifest(progress_id="prog_001", achievement_id="ach_001")
        self.assertEqual(p.achievement_id, "ach_001")

    def test_is_satisfied_false(self):
        p = AchievementProgressManifest(progress_id="prog_001", achievement_id="ach_001", satisfied=False)
        self.assertFalse(p.is_satisfied)

    def test_is_satisfied_true(self):
        p = AchievementProgressManifest(progress_id="prog_001", achievement_id="ach_001", satisfied=True)
        self.assertTrue(p.is_satisfied)

    def test_has_condition_false(self):
        p = AchievementProgressManifest(progress_id="prog_001", achievement_id="ach_001", condition_expr="")
        self.assertFalse(p.has_condition)

    def test_has_condition_true(self):
        p = AchievementProgressManifest(progress_id="prog_001", achievement_id="ach_001", condition_expr="kills >= 10")
        self.assertTrue(p.has_condition)

    def test_progress_ratio_zero(self):
        p = AchievementProgressManifest(progress_id="prog_001", achievement_id="ach_001", current_value=0, target_value=10)
        self.assertAlmostEqual(p.progress_ratio, 0.0)

    def test_progress_ratio_full(self):
        p = AchievementProgressManifest(progress_id="prog_001", achievement_id="ach_001", current_value=10, target_value=10)
        self.assertAlmostEqual(p.progress_ratio, 1.0)

    def test_is_complete_false(self):
        p = AchievementProgressManifest(progress_id="prog_001", achievement_id="ach_001", current_value=5, target_value=10)
        self.assertFalse(p.is_complete)

    def test_is_complete_true(self):
        p = AchievementProgressManifest(progress_id="prog_001", achievement_id="ach_001", current_value=10, target_value=10)
        self.assertTrue(p.is_complete)


# ---------------------------------------------------------------------------
# AchievementRewardManifest
# ---------------------------------------------------------------------------

class TestAchievementRewardManifest(unittest.TestCase):
    def test_reward_id(self):
        r = AchievementRewardManifest(reward_id="rew_001", achievement_id="ach_001")
        self.assertEqual(r.reward_id, "rew_001")

    def test_achievement_id(self):
        r = AchievementRewardManifest(reward_id="rew_001", achievement_id="ach_001")
        self.assertEqual(r.achievement_id, "ach_001")

    def test_is_claimed_false(self):
        r = AchievementRewardManifest(reward_id="rew_001", achievement_id="ach_001", claimed=False)
        self.assertFalse(r.is_claimed)

    def test_is_claimed_true(self):
        r = AchievementRewardManifest(reward_id="rew_001", achievement_id="ach_001", claimed=True)
        self.assertTrue(r.is_claimed)

    def test_is_gold_false(self):
        r = AchievementRewardManifest(reward_id="rew_001", achievement_id="ach_001", tier="Bronze")
        self.assertFalse(r.is_gold)

    def test_is_gold_true(self):
        r = AchievementRewardManifest(reward_id="rew_001", achievement_id="ach_001", tier="Gold")
        self.assertTrue(r.is_gold)

    def test_is_platinum_false(self):
        r = AchievementRewardManifest(reward_id="rew_001", achievement_id="ach_001", tier="Gold")
        self.assertFalse(r.is_platinum)

    def test_is_platinum_true(self):
        r = AchievementRewardManifest(reward_id="rew_001", achievement_id="ach_001", tier="Platinum")
        self.assertTrue(r.is_platinum)

    def test_has_xp_false(self):
        r = AchievementRewardManifest(reward_id="rew_001", achievement_id="ach_001", xp_value=0)
        self.assertFalse(r.has_xp)

    def test_has_xp_true(self):
        r = AchievementRewardManifest(reward_id="rew_001", achievement_id="ach_001", xp_value=500)
        self.assertTrue(r.has_xp)


# ---------------------------------------------------------------------------
# AchievementBodyManifest
# ---------------------------------------------------------------------------

class TestAchievementBodyManifest(unittest.TestCase):
    def test_achievement_id(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood")
        self.assertEqual(a.achievement_id, "ach_001")

    def test_name(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood")
        self.assertEqual(a.name, "First Blood")

    def test_default_scope_story(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood")
        self.assertEqual(a.scope, "Story")

    def test_default_state_locked(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood")
        self.assertEqual(a.achievement_state, "Locked")

    def test_is_locked_true(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", achievement_state="Locked")
        self.assertTrue(a.is_locked)

    def test_is_locked_false(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", achievement_state="Unlocked")
        self.assertFalse(a.is_locked)

    def test_is_unlocked_false(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", achievement_state="Locked")
        self.assertFalse(a.is_unlocked)

    def test_is_unlocked_true(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", achievement_state="Unlocked")
        self.assertTrue(a.is_unlocked)

    def test_is_claimed_false(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", achievement_state="Locked")
        self.assertFalse(a.is_claimed)

    def test_is_claimed_true(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", achievement_state="Claimed")
        self.assertTrue(a.is_claimed)

    def test_is_in_progress_false(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", achievement_state="Locked")
        self.assertFalse(a.is_in_progress)

    def test_is_in_progress_true(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", achievement_state="InProgress")
        self.assertTrue(a.is_in_progress)

    def test_is_story_true(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", scope="Story")
        self.assertTrue(a.is_story)

    def test_is_story_false(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", scope="Combat")
        self.assertFalse(a.is_story)

    def test_has_progress_false(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood")
        self.assertFalse(a.has_progress)

    def test_has_progress_true(self):
        prog = AchievementProgressManifest(progress_id="prog_001", achievement_id="ach_001")
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", progress_items=[prog])
        self.assertTrue(a.has_progress)

    def test_has_rewards_false(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood")
        self.assertFalse(a.has_rewards)

    def test_has_rewards_true(self):
        rew = AchievementRewardManifest(reward_id="rew_001", achievement_id="ach_001")
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", rewards=[rew])
        self.assertTrue(a.has_rewards)

    def test_has_icon_false(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood")
        self.assertFalse(a.has_icon)

    def test_has_icon_true(self):
        a = AchievementBodyManifest(achievement_id="ach_001", name="First Blood", icon_asset_id="icon_001")
        self.assertTrue(a.has_icon)


# ---------------------------------------------------------------------------
# AchievementBodyLoader
# ---------------------------------------------------------------------------

class TestAchievementBodyLoader(unittest.TestCase):
    def setUp(self):
        self.loader = AchievementBodyLoader()
        self.data = {
            "achievement_id": "ach_001",
            "name": "First Blood",
            "scope": "Combat",
            "achievement_state": "Locked",
            "description": "Win your first battle",
            "icon_asset_id": "",
            "display_order": 1,
            "play_count": 0,
            "progress_items": [],
            "rewards": [],
        }

    def test_load_manifest(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.achievement_id, "ach_001")

    def test_load_manifest_name(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.name, "First Blood")

    def test_load_manifest_scope(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.scope, "Combat")

    def test_load_batch(self):
        data2 = dict(self.data)
        data2["achievement_id"] = "ach_002"
        data2["name"] = "Explorer"
        manifests = self.loader.load_batch([self.data, data2])
        self.assertEqual(len(manifests), 2)

    def test_loaded_count(self):
        self.loader.load_manifest(self.data)
        self.assertEqual(self.loader.loaded_count, 1)

    def test_validate(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertTrue(self.loader.validate(manifest))

    def test_clear(self):
        self.loader.load_manifest(self.data)
        self.loader.clear()
        self.assertEqual(self.loader.loaded_count, 0)

    def test_progress_loaded(self):
        data = dict(self.data)
        data["progress_items"] = [{
            "progress_id": "prog_001",
            "achievement_id": "ach_001",
            "condition_type": "OnKill",
            "condition_expr": "kills >= 1",
            "target_value": 1,
            "current_value": 0,
            "satisfied": False,
        }]
        manifest = self.loader.load_manifest(data)
        self.assertEqual(len(manifest.progress_items), 1)
        p = manifest.progress_items[0]
        self.assertEqual(p.progress_id, "prog_001")
        self.assertEqual(p.achievement_id, "ach_001")
        self.assertEqual(p.condition_type, "OnKill")
        self.assertEqual(p.target_value, 1)

    def test_reward_loaded(self):
        data = dict(self.data)
        data["rewards"] = [{
            "reward_id": "rew_001",
            "achievement_id": "ach_001",
            "tier": "Gold",
            "reward_asset_id": "asset_rew",
            "xp_value": 1000,
            "claimed": False,
            "claim_condition_expr": "",
        }]
        manifest = self.loader.load_manifest(data)
        self.assertEqual(len(manifest.rewards), 1)
        r = manifest.rewards[0]
        self.assertEqual(r.reward_id, "rew_001")
        self.assertEqual(r.achievement_id, "ach_001")
        self.assertEqual(r.tier, "Gold")
        self.assertEqual(r.xp_value, 1000)

    def test_save_and_load(self):
        import tempfile, os
        manifest = self.loader.load_manifest(self.data)
        save_path = REPO_ROOT / "AtlasAI" / "Tests" / "_test_ach_save.json"
        try:
            self.loader.save_manifest(manifest, save_path)
            loader2 = AchievementBodyLoader()
            loaded = loader2.load_from_file(save_path)
            self.assertEqual(loaded.achievement_id, "ach_001")
        finally:
            if save_path.exists():
                save_path.unlink()


if __name__ == "__main__":
    unittest.main()
