"""Phase 39D — Tests for QuestBodyRegistry.h and quest_body_loader.py."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    QuestBodyLoader,
    QuestBodyManifest,
    QuestObjectiveManifest,
    QuestRewardManifest,
)


def _read_header(name: str) -> str:
    return (SCENE_DIR / f"{name}.h").read_text()


# ---------------------------------------------------------------------------
# QuestBodyRegistry.h
# ---------------------------------------------------------------------------

class TestQuestBodyRegistryHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "QuestBodyRegistry.h").exists())


class TestQuestBodyRegistryNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("QuestBodyRegistry"))


class TestQuestBodyRegistryEnums(unittest.TestCase):
    def test_quest_body_state_enum(self):
        self.assertIn("QuestBodyState", _read_header("QuestBodyRegistry"))

    def test_quest_body_scope_enum(self):
        self.assertIn("QuestBodyScope", _read_header("QuestBodyRegistry"))

    def test_objective_trigger_type_enum(self):
        self.assertIn("ObjectiveTriggerType", _read_header("QuestBodyRegistry"))

    def test_reward_type_enum(self):
        self.assertIn("RewardType", _read_header("QuestBodyRegistry"))

    def test_quest_body_flags_enum(self):
        self.assertIn("QuestBodyFlags", _read_header("QuestBodyRegistry"))

    def test_active_state_value(self):
        self.assertIn("Active", _read_header("QuestBodyRegistry"))

    def test_completed_state_value(self):
        self.assertIn("Completed", _read_header("QuestBodyRegistry"))

    def test_side_quest_scope_value(self):
        self.assertIn("SideQuest", _read_header("QuestBodyRegistry"))

    def test_main_story_scope_value(self):
        self.assertIn("MainStory", _read_header("QuestBodyRegistry"))

    def test_trackable_flag(self):
        self.assertIn("Trackable", _read_header("QuestBodyRegistry"))


class TestQuestBodyRegistryStructs(unittest.TestCase):
    def test_quest_objective_def_struct(self):
        self.assertIn("QuestObjectiveDef", _read_header("QuestBodyRegistry"))

    def test_quest_reward_def_struct(self):
        self.assertIn("QuestRewardDef", _read_header("QuestBodyRegistry"))

    def test_quest_body_record_struct(self):
        self.assertIn("QuestBodyRecord", _read_header("QuestBodyRegistry"))

    def test_dependency_ids_in_objective(self):
        self.assertIn("dependencyIds", _read_header("QuestBodyRegistry"))

    def test_condition_expr_in_reward(self):
        self.assertIn("conditionExpr", _read_header("QuestBodyRegistry"))

    def test_play_count_in_quest(self):
        self.assertIn("playCount", _read_header("QuestBodyRegistry"))


class TestQuestBodyRegistryMethods(unittest.TestCase):
    def test_register_quest(self):
        self.assertIn("RegisterQuest", _read_header("QuestBodyRegistry"))

    def test_unregister_quest(self):
        self.assertIn("UnregisterQuest", _read_header("QuestBodyRegistry"))

    def test_set_quest_scope(self):
        self.assertIn("SetQuestScope", _read_header("QuestBodyRegistry"))

    def test_set_quest_state(self):
        self.assertIn("SetQuestState", _read_header("QuestBodyRegistry"))

    def test_activate_quest(self):
        self.assertIn("ActivateQuest", _read_header("QuestBodyRegistry"))

    def test_complete_quest(self):
        self.assertIn("CompleteQuest", _read_header("QuestBodyRegistry"))

    def test_fail_quest(self):
        self.assertIn("FailQuest", _read_header("QuestBodyRegistry"))

    def test_abandon_quest(self):
        self.assertIn("AbandonQuest", _read_header("QuestBodyRegistry"))

    def test_lock_quest(self):
        self.assertIn("LockQuest", _read_header("QuestBodyRegistry"))

    def test_get_quest_by_id(self):
        self.assertIn("GetQuestById", _read_header("QuestBodyRegistry"))

    def test_get_all_quest_ids(self):
        self.assertIn("GetAllQuestIds", _read_header("QuestBodyRegistry"))

    def test_get_quests_by_scope(self):
        self.assertIn("GetQuestsByScope", _read_header("QuestBodyRegistry"))

    def test_get_active_quests(self):
        self.assertIn("GetActiveQuests", _read_header("QuestBodyRegistry"))

    def test_get_completed_quests(self):
        self.assertIn("GetCompletedQuests", _read_header("QuestBodyRegistry"))

    def test_get_failed_quests(self):
        self.assertIn("GetFailedQuests", _read_header("QuestBodyRegistry"))

    def test_add_objective(self):
        self.assertIn("AddObjective", _read_header("QuestBodyRegistry"))

    def test_remove_objective(self):
        self.assertIn("RemoveObjective", _read_header("QuestBodyRegistry"))

    def test_complete_objective(self):
        self.assertIn("CompleteObjective", _read_header("QuestBodyRegistry"))

    def test_increment_objective(self):
        self.assertIn("IncrementObjective", _read_header("QuestBodyRegistry"))

    def test_get_objective(self):
        self.assertIn("GetObjective", _read_header("QuestBodyRegistry"))

    def test_get_objectives_by_quest(self):
        self.assertIn("GetObjectivesByQuest", _read_header("QuestBodyRegistry"))

    def test_get_completed_objectives(self):
        self.assertIn("GetCompletedObjectives", _read_header("QuestBodyRegistry"))

    def test_add_reward(self):
        self.assertIn("AddReward", _read_header("QuestBodyRegistry"))

    def test_remove_reward(self):
        self.assertIn("RemoveReward", _read_header("QuestBodyRegistry"))

    def test_distribute_reward(self):
        self.assertIn("DistributeReward", _read_header("QuestBodyRegistry"))

    def test_get_reward(self):
        self.assertIn("GetReward", _read_header("QuestBodyRegistry"))

    def test_get_rewards_by_quest(self):
        self.assertIn("GetRewardsByQuest", _read_header("QuestBodyRegistry"))

    def test_get_pending_rewards(self):
        self.assertIn("GetPendingRewards", _read_header("QuestBodyRegistry"))

    def test_clear(self):
        self.assertIn("Clear", _read_header("QuestBodyRegistry"))

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_header("QuestBodyRegistry"))

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_header("QuestBodyRegistry"))


# ---------------------------------------------------------------------------
# QuestObjectiveManifest
# ---------------------------------------------------------------------------

class TestQuestObjectiveManifest(unittest.TestCase):
    def test_objective_id(self):
        o = QuestObjectiveManifest(objective_id="obj_001", quest_id="quest_001")
        self.assertEqual(o.objective_id, "obj_001")

    def test_quest_id(self):
        o = QuestObjectiveManifest(objective_id="obj_001", quest_id="quest_001")
        self.assertEqual(o.quest_id, "quest_001")

    def test_is_completed_false(self):
        o = QuestObjectiveManifest(objective_id="obj_001", quest_id="quest_001", completed=False)
        self.assertFalse(o.is_completed)

    def test_is_completed_true(self):
        o = QuestObjectiveManifest(objective_id="obj_001", quest_id="quest_001", completed=True)
        self.assertTrue(o.is_completed)

    def test_has_trigger_false(self):
        o = QuestObjectiveManifest(objective_id="obj_001", quest_id="quest_001", trigger_expr="")
        self.assertFalse(o.has_trigger)

    def test_has_trigger_true(self):
        o = QuestObjectiveManifest(objective_id="obj_001", quest_id="quest_001", trigger_expr="on_enter_zone")
        self.assertTrue(o.has_trigger)

    def test_is_optional_false(self):
        o = QuestObjectiveManifest(objective_id="obj_001", quest_id="quest_001", optional=False)
        self.assertFalse(o.is_optional)

    def test_is_optional_true(self):
        o = QuestObjectiveManifest(objective_id="obj_001", quest_id="quest_001", optional=True)
        self.assertTrue(o.is_optional)

    def test_progress_ratio_zero(self):
        o = QuestObjectiveManifest(objective_id="obj_001", quest_id="quest_001", target_count=5, current_count=0)
        self.assertAlmostEqual(o.progress_ratio, 0.0)

    def test_progress_ratio_full(self):
        o = QuestObjectiveManifest(objective_id="obj_001", quest_id="quest_001", target_count=5, current_count=5)
        self.assertAlmostEqual(o.progress_ratio, 1.0)


# ---------------------------------------------------------------------------
# QuestRewardManifest
# ---------------------------------------------------------------------------

class TestQuestRewardManifest(unittest.TestCase):
    def test_reward_id(self):
        r = QuestRewardManifest(reward_id="reward_001", quest_id="quest_001")
        self.assertEqual(r.reward_id, "reward_001")

    def test_quest_id(self):
        r = QuestRewardManifest(reward_id="reward_001", quest_id="quest_001")
        self.assertEqual(r.quest_id, "quest_001")

    def test_is_distributed_false(self):
        r = QuestRewardManifest(reward_id="reward_001", quest_id="quest_001", distributed=False)
        self.assertFalse(r.is_distributed)

    def test_is_distributed_true(self):
        r = QuestRewardManifest(reward_id="reward_001", quest_id="quest_001", distributed=True)
        self.assertTrue(r.is_distributed)

    def test_has_condition_false(self):
        r = QuestRewardManifest(reward_id="reward_001", quest_id="quest_001", condition_expr="")
        self.assertFalse(r.has_condition)

    def test_has_condition_true(self):
        r = QuestRewardManifest(reward_id="reward_001", quest_id="quest_001", condition_expr="level >= 10")
        self.assertTrue(r.has_condition)

    def test_is_item_false(self):
        r = QuestRewardManifest(reward_id="reward_001", quest_id="quest_001", reward_type="Experience")
        self.assertFalse(r.is_item)

    def test_is_item_true(self):
        r = QuestRewardManifest(reward_id="reward_001", quest_id="quest_001", reward_type="Item")
        self.assertTrue(r.is_item)


# ---------------------------------------------------------------------------
# QuestBodyManifest
# ---------------------------------------------------------------------------

class TestQuestBodyManifest(unittest.TestCase):
    def test_quest_id(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact")
        self.assertEqual(q.quest_id, "quest_001")

    def test_name(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact")
        self.assertEqual(q.name, "The Lost Artifact")

    def test_default_scope_side_quest(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact")
        self.assertEqual(q.scope, "SideQuest")

    def test_default_quest_state_inactive(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact")
        self.assertEqual(q.quest_state, "Inactive")

    def test_is_active_false(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact", quest_state="Inactive")
        self.assertFalse(q.is_active)

    def test_is_active_true(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact", quest_state="Active")
        self.assertTrue(q.is_active)

    def test_is_completed_false(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact", quest_state="Active")
        self.assertFalse(q.is_completed)

    def test_is_completed_true(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact", quest_state="Completed")
        self.assertTrue(q.is_completed)

    def test_is_failed_false(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact", quest_state="Active")
        self.assertFalse(q.is_failed)

    def test_is_failed_true(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact", quest_state="Failed")
        self.assertTrue(q.is_failed)

    def test_is_main_story_false(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact", scope="SideQuest")
        self.assertFalse(q.is_main_story)

    def test_is_main_story_true(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact", scope="MainStory")
        self.assertTrue(q.is_main_story)

    def test_has_objectives_false(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact")
        self.assertFalse(q.has_objectives)

    def test_has_objectives_true(self):
        obj = QuestObjectiveManifest(objective_id="obj_001", quest_id="quest_001")
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact", objectives=[obj])
        self.assertTrue(q.has_objectives)

    def test_has_rewards_false(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact")
        self.assertFalse(q.has_rewards)

    def test_has_rewards_true(self):
        r = QuestRewardManifest(reward_id="reward_001", quest_id="quest_001")
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact", rewards=[r])
        self.assertTrue(q.has_rewards)

    def test_has_giver_false(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact")
        self.assertFalse(q.has_giver)

    def test_has_giver_true(self):
        q = QuestBodyManifest(quest_id="quest_001", name="The Lost Artifact", giver_npc_id="npc_elder")
        self.assertTrue(q.has_giver)


# ---------------------------------------------------------------------------
# QuestBodyLoader
# ---------------------------------------------------------------------------

class TestQuestBodyLoader(unittest.TestCase):
    def setUp(self):
        self.loader = QuestBodyLoader()
        self.data = {
            "quest_id": "quest_001",
            "name": "The Lost Artifact",
            "scope": "SideQuest",
            "quest_state": "Inactive",
            "objectives": [
                {
                    "objective_id": "obj_001",
                    "quest_id": "quest_001",
                    "description": "Find the artifact",
                    "trigger_type": "OnCollect",
                    "trigger_expr": "collect_artifact",
                    "target_count": 1,
                    "current_count": 0,
                    "completed": False,
                    "optional": False,
                    "dependency_ids": [],
                }
            ],
            "rewards": [
                {
                    "reward_id": "reward_001",
                    "quest_id": "quest_001",
                    "reward_type": "Experience",
                    "reward_asset_id": "",
                    "quantity": 500,
                    "distributed": False,
                    "condition_expr": "",
                }
            ],
        }

    def test_load_manifest(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.quest_id, "quest_001")

    def test_load_manifest_name(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.name, "The Lost Artifact")

    def test_load_manifest_scope(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.scope, "SideQuest")

    def test_load_batch(self):
        manifests = self.loader.load_batch([self.data, self.data])
        self.assertEqual(len(manifests), 2)

    def test_loaded_count(self):
        self.loader.load_manifest(self.data)
        self.assertEqual(self.loader.loaded_count, 1)

    def test_validate(self):
        m = self.loader.load_manifest(self.data)
        self.assertTrue(self.loader.validate(m))

    def test_clear(self):
        self.loader.load_manifest(self.data)
        self.loader.clear()
        self.assertEqual(self.loader.loaded_count, 0)

    def test_objective_loaded_objective_id(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.objectives[0].objective_id, "obj_001")

    def test_objective_loaded_quest_id(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.objectives[0].quest_id, "quest_001")

    def test_objective_loaded_description(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.objectives[0].description, "Find the artifact")

    def test_objective_loaded_target_count(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.objectives[0].target_count, 1)

    def test_reward_loaded_reward_id(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.rewards[0].reward_id, "reward_001")

    def test_reward_loaded_quest_id(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.rewards[0].quest_id, "quest_001")

    def test_reward_loaded_reward_type(self):
        m = self.loader.load_manifest(self.data)
        self.assertEqual(m.rewards[0].reward_type, "Experience")

    def test_save_and_load(self):
        import tempfile
        import os
        m = self.loader.load_manifest(self.data)
        save_path = REPO_ROOT / "AtlasAI" / "Tests" / "_quest_body_test_save.json"
        self.loader.save_manifest(m, save_path)
        loader2 = QuestBodyLoader()
        m2 = loader2.load_from_file(save_path)
        self.assertEqual(m2.quest_id, "quest_001")
        save_path.unlink()


if __name__ == "__main__":
    unittest.main()
