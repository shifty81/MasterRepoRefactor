"""AtlasAI Phase 39D — Quest Body Loader.

Discovers and manages quest body manifests, mirroring the C++
QuestBodyRegistry for cross-language quest management.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class QuestObjectiveManifest:
    objective_id: str
    quest_id: str
    description: str = ""
    trigger_type: str = "OnCondition"
    trigger_expr: str = ""
    target_count: int = 1
    current_count: int = 0
    completed: bool = False
    optional: bool = False
    dependency_ids: list = field(default_factory=list)

    @property
    def is_completed(self) -> bool:
        return self.completed

    @property
    def has_trigger(self) -> bool:
        return bool(self.trigger_expr)

    @property
    def is_optional(self) -> bool:
        return self.optional

    @property
    def progress_ratio(self) -> float:
        if self.target_count <= 0:
            return 0.0
        return min(1.0, self.current_count / self.target_count)


@dataclass
class QuestRewardManifest:
    reward_id: str
    quest_id: str
    reward_type: str = "Experience"
    reward_asset_id: str = ""
    quantity: int = 1
    distributed: bool = False
    condition_expr: str = ""

    @property
    def is_distributed(self) -> bool:
        return self.distributed

    @property
    def has_condition(self) -> bool:
        return bool(self.condition_expr)

    @property
    def is_item(self) -> bool:
        return self.reward_type == "Item"


@dataclass
class QuestBodyManifest:
    quest_id: str
    name: str
    scope: str = "SideQuest"
    quest_state: str = "Inactive"
    description: str = ""
    giver_npc_id: str = ""
    start_condition_expr: str = ""
    fail_condition_expr: str = ""
    play_count: int = 0
    objectives: list = field(default_factory=list)
    rewards: list = field(default_factory=list)

    @property
    def is_active(self) -> bool:
        return self.quest_state == "Active"

    @property
    def is_completed(self) -> bool:
        return self.quest_state == "Completed"

    @property
    def is_failed(self) -> bool:
        return self.quest_state == "Failed"

    @property
    def is_main_story(self) -> bool:
        return self.scope == "MainStory"

    @property
    def has_objectives(self) -> bool:
        return bool(self.objectives)

    @property
    def has_rewards(self) -> bool:
        return bool(self.rewards)

    @property
    def has_giver(self) -> bool:
        return bool(self.giver_npc_id)


class QuestBodyLoader:
    def __init__(self) -> None:
        self._loaded: List[QuestBodyManifest] = []

    def load_manifest(self, data: dict) -> QuestBodyManifest:
        objectives_data = data.get("objectives", [])
        objectives = []
        for o in objectives_data:
            objectives.append(QuestObjectiveManifest(
                objective_id=o.get("objective_id", ""),
                quest_id=o.get("quest_id", ""),
                description=o.get("description", ""),
                trigger_type=o.get("trigger_type", "OnCondition"),
                trigger_expr=o.get("trigger_expr", ""),
                target_count=int(o.get("target_count", 1)),
                current_count=int(o.get("current_count", 0)),
                completed=bool(o.get("completed", False)),
                optional=bool(o.get("optional", False)),
                dependency_ids=o.get("dependency_ids", []),
            ))
        rewards_data = data.get("rewards", [])
        rewards = []
        for r in rewards_data:
            rewards.append(QuestRewardManifest(
                reward_id=r.get("reward_id", ""),
                quest_id=r.get("quest_id", ""),
                reward_type=r.get("reward_type", "Experience"),
                reward_asset_id=r.get("reward_asset_id", ""),
                quantity=int(r.get("quantity", 1)),
                distributed=bool(r.get("distributed", False)),
                condition_expr=r.get("condition_expr", ""),
            ))
        manifest = QuestBodyManifest(
            quest_id=data["quest_id"],
            name=data["name"],
            scope=data.get("scope", "SideQuest"),
            quest_state=data.get("quest_state", "Inactive"),
            description=data.get("description", ""),
            giver_npc_id=data.get("giver_npc_id", ""),
            start_condition_expr=data.get("start_condition_expr", ""),
            fail_condition_expr=data.get("fail_condition_expr", ""),
            play_count=int(data.get("play_count", 0)),
            objectives=objectives,
            rewards=rewards,
        )
        self._loaded.append(manifest)
        return manifest

    def load_from_file(self, path) -> QuestBodyManifest:
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def load_batch(self, data_list: list) -> List[QuestBodyManifest]:
        return [self.load_manifest(d) for d in data_list]

    def save_manifest(self, manifest: QuestBodyManifest, path) -> None:
        p = Path(path)
        data = {
            "quest_id": manifest.quest_id,
            "name": manifest.name,
            "scope": manifest.scope,
            "quest_state": manifest.quest_state,
            "description": manifest.description,
            "giver_npc_id": manifest.giver_npc_id,
            "start_condition_expr": manifest.start_condition_expr,
            "fail_condition_expr": manifest.fail_condition_expr,
            "play_count": manifest.play_count,
            "objectives": [
                {
                    "objective_id": o.objective_id,
                    "quest_id": o.quest_id,
                    "description": o.description,
                    "trigger_type": o.trigger_type,
                    "trigger_expr": o.trigger_expr,
                    "target_count": o.target_count,
                    "current_count": o.current_count,
                    "completed": o.completed,
                    "optional": o.optional,
                    "dependency_ids": o.dependency_ids,
                }
                for o in manifest.objectives
            ],
            "rewards": [
                {
                    "reward_id": r.reward_id,
                    "quest_id": r.quest_id,
                    "reward_type": r.reward_type,
                    "reward_asset_id": r.reward_asset_id,
                    "quantity": r.quantity,
                    "distributed": r.distributed,
                    "condition_expr": r.condition_expr,
                }
                for r in manifest.rewards
            ],
        }
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: QuestBodyManifest) -> bool:
        return bool(manifest.quest_id) and bool(manifest.name)

    def clear(self) -> None:
        self._loaded.clear()

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)
