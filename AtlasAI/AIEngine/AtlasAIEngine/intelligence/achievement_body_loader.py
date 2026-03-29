"""AtlasAI Phase 40D — Achievement Body Loader.

Discovers and manages achievement body manifests, mirroring the C++
AchievementBodyRegistry for cross-language achievement management.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class AchievementProgressManifest:
    progress_id: str
    achievement_id: str
    condition_type: str = "OnComplete"
    condition_expr: str = ""
    target_value: int = 1
    current_value: int = 0
    satisfied: bool = False

    @property
    def is_satisfied(self) -> bool:
        return self.satisfied

    @property
    def has_condition(self) -> bool:
        return bool(self.condition_expr)

    @property
    def progress_ratio(self) -> float:
        if self.target_value <= 0:
            return 0.0
        return min(1.0, self.current_value / self.target_value)

    @property
    def is_complete(self) -> bool:
        return self.current_value >= self.target_value


@dataclass
class AchievementRewardManifest:
    reward_id: str
    achievement_id: str
    tier: str = "Bronze"
    reward_asset_id: str = ""
    xp_value: int = 0
    claimed: bool = False
    claim_condition_expr: str = ""

    @property
    def is_claimed(self) -> bool:
        return self.claimed

    @property
    def is_gold(self) -> bool:
        return self.tier == "Gold"

    @property
    def is_platinum(self) -> bool:
        return self.tier == "Platinum"

    @property
    def has_xp(self) -> bool:
        return self.xp_value > 0


@dataclass
class AchievementBodyManifest:
    achievement_id: str
    name: str
    scope: str = "Story"
    achievement_state: str = "Locked"
    description: str = ""
    icon_asset_id: str = ""
    display_order: int = 0
    play_count: int = 0
    progress_items: list = field(default_factory=list)
    rewards: list = field(default_factory=list)

    @property
    def is_locked(self) -> bool:
        return self.achievement_state == "Locked"

    @property
    def is_unlocked(self) -> bool:
        return self.achievement_state == "Unlocked"

    @property
    def is_claimed(self) -> bool:
        return self.achievement_state == "Claimed"

    @property
    def is_in_progress(self) -> bool:
        return self.achievement_state == "InProgress"

    @property
    def is_story(self) -> bool:
        return self.scope == "Story"

    @property
    def has_progress(self) -> bool:
        return bool(self.progress_items)

    @property
    def has_rewards(self) -> bool:
        return bool(self.rewards)

    @property
    def has_icon(self) -> bool:
        return bool(self.icon_asset_id)


class AchievementBodyLoader:
    def __init__(self) -> None:
        self._loaded: List[AchievementBodyManifest] = []

    def load_manifest(self, data: dict) -> AchievementBodyManifest:
        progress_data = data.get("progress_items", [])
        progress_items = []
        for p in progress_data:
            progress_items.append(AchievementProgressManifest(
                progress_id=p.get("progress_id", ""),
                achievement_id=p.get("achievement_id", ""),
                condition_type=p.get("condition_type", "OnComplete"),
                condition_expr=p.get("condition_expr", ""),
                target_value=int(p.get("target_value", 1)),
                current_value=int(p.get("current_value", 0)),
                satisfied=bool(p.get("satisfied", False)),
            ))
        rewards_data = data.get("rewards", [])
        rewards = []
        for r in rewards_data:
            rewards.append(AchievementRewardManifest(
                reward_id=r.get("reward_id", ""),
                achievement_id=r.get("achievement_id", ""),
                tier=r.get("tier", "Bronze"),
                reward_asset_id=r.get("reward_asset_id", ""),
                xp_value=int(r.get("xp_value", 0)),
                claimed=bool(r.get("claimed", False)),
                claim_condition_expr=r.get("claim_condition_expr", ""),
            ))
        manifest = AchievementBodyManifest(
            achievement_id=data["achievement_id"],
            name=data["name"],
            scope=data.get("scope", "Story"),
            achievement_state=data.get("achievement_state", "Locked"),
            description=data.get("description", ""),
            icon_asset_id=data.get("icon_asset_id", ""),
            display_order=int(data.get("display_order", 0)),
            play_count=int(data.get("play_count", 0)),
            progress_items=progress_items,
            rewards=rewards,
        )
        self._loaded.append(manifest)
        return manifest

    def load_from_file(self, path) -> AchievementBodyManifest:
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def load_batch(self, data_list: list) -> List[AchievementBodyManifest]:
        return [self.load_manifest(d) for d in data_list]

    def save_manifest(self, manifest: AchievementBodyManifest, path) -> None:
        p = Path(path)
        data = {
            "achievement_id": manifest.achievement_id,
            "name": manifest.name,
            "scope": manifest.scope,
            "achievement_state": manifest.achievement_state,
            "description": manifest.description,
            "icon_asset_id": manifest.icon_asset_id,
            "display_order": manifest.display_order,
            "play_count": manifest.play_count,
            "progress_items": [
                {
                    "progress_id": pr.progress_id,
                    "achievement_id": pr.achievement_id,
                    "condition_type": pr.condition_type,
                    "condition_expr": pr.condition_expr,
                    "target_value": pr.target_value,
                    "current_value": pr.current_value,
                    "satisfied": pr.satisfied,
                }
                for pr in manifest.progress_items
            ],
            "rewards": [
                {
                    "reward_id": r.reward_id,
                    "achievement_id": r.achievement_id,
                    "tier": r.tier,
                    "reward_asset_id": r.reward_asset_id,
                    "xp_value": r.xp_value,
                    "claimed": r.claimed,
                    "claim_condition_expr": r.claim_condition_expr,
                }
                for r in manifest.rewards
            ],
        }
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: AchievementBodyManifest) -> bool:
        return bool(manifest.achievement_id) and bool(manifest.name)

    def clear(self) -> None:
        self._loaded.clear()

    @property
    def loaded_count(self) -> int:
        return len(self._loaded)
