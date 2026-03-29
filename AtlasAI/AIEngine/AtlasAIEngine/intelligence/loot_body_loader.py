"""AtlasAI Phase 42D — Loot Body Loader.

Discovers and manages loot body manifests, mirroring the C++
LootBodyRegistry for cross-language loot table management.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class LootEntryManifest:
    loot_entry_id: str
    item_id: str
    rarity: str = "Common"
    pool_type: str = "Item"
    drop_weight: float = 1.0
    min_quantity: int = 1
    max_quantity: int = 1
    drop_chance: float = 1.0
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_rare(self) -> bool:
        return self.rarity in ("Rare", "Epic", "Legendary", "Mythic")

    @property
    def is_legendary(self) -> bool:
        return self.rarity == "Legendary"

    @property
    def is_mythic(self) -> bool:
        return self.rarity == "Mythic"

    @property
    def is_common(self) -> bool:
        return self.rarity == "Common"

    @property
    def is_guaranteed(self) -> bool:
        return self.drop_chance >= 1.0

    @property
    def is_stackable(self) -> bool:
        return self.max_quantity > 1

    @property
    def is_currency(self) -> bool:
        return self.pool_type == "Currency"

    @property
    def is_blueprint(self) -> bool:
        return self.pool_type == "Blueprint"

    @property
    def quantity_range(self) -> int:
        return self.max_quantity - self.min_quantity


@dataclass
class LootTableManifest:
    loot_table_id: str
    loot_table_name: str
    drop_condition: str = "Always"
    roll_method: str = "Weighted"
    max_rolls: int = 1
    min_rolls: int = 1
    guaranteed_chance: float = 0.0
    enabled: bool = True
    loot_entry_ids: list = field(default_factory=list)

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_always_drop(self) -> bool:
        return self.drop_condition == "Always"

    @property
    def is_on_kill(self) -> bool:
        return self.drop_condition == "OnKill"

    @property
    def is_weighted(self) -> bool:
        return self.roll_method == "Weighted"

    @property
    def is_guaranteed_roll(self) -> bool:
        return self.roll_method == "Guaranteed"

    @property
    def has_guaranteed_chance(self) -> bool:
        return self.guaranteed_chance > 0.0

    @property
    def has_entries(self) -> bool:
        return len(self.loot_entry_ids) > 0

    @property
    def entry_count(self) -> int:
        return len(self.loot_entry_ids)

    @property
    def max_possible_rolls(self) -> int:
        return self.max_rolls


@dataclass
class LootBodyManifest:
    loot_body_id: str
    owner_entity_id: str
    loot_table_id: str = ""
    level: int = 1
    luck_modifier: float = 1.0
    exhausted: bool = False
    display_name: str = ""
    active_pool_ids: list = field(default_factory=list)

    @property
    def is_exhausted(self) -> bool:
        return self.exhausted

    @property
    def is_active(self) -> bool:
        return not self.exhausted

    @property
    def has_owner(self) -> bool:
        return bool(self.owner_entity_id)

    @property
    def has_loot_table(self) -> bool:
        return bool(self.loot_table_id)

    @property
    def is_lucky(self) -> bool:
        return self.luck_modifier > 1.0

    @property
    def is_unlucky(self) -> bool:
        return self.luck_modifier < 1.0

    @property
    def has_display_name(self) -> bool:
        return bool(self.display_name)

    @property
    def is_high_level(self) -> bool:
        return self.level >= 50

    @property
    def pool_count(self) -> int:
        return len(self.active_pool_ids)


class LootBodyLoader:
    """Loader for loot body manifests."""

    def __init__(self) -> None:
        self._manifests: dict = {}

    def load_manifest(self, data: dict) -> LootBodyManifest:
        manifest = LootBodyManifest(
            loot_body_id=data["loot_body_id"],
            owner_entity_id=data.get("owner_entity_id", ""),
            loot_table_id=data.get("loot_table_id", ""),
            level=data.get("level", 1),
            luck_modifier=data.get("luck_modifier", 1.0),
            exhausted=data.get("exhausted", False),
            display_name=data.get("display_name", ""),
            active_pool_ids=data.get("active_pool_ids", []),
        )
        self._manifests[manifest.loot_body_id] = manifest
        return manifest

    def load_batch(self, data_list: list) -> list:
        return [self.load_manifest(d) for d in data_list]

    def load_from_file(self, path) -> LootBodyManifest:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def save_manifest(self, manifest: LootBodyManifest, path) -> None:
        data = {
            "loot_body_id": manifest.loot_body_id,
            "owner_entity_id": manifest.owner_entity_id,
            "loot_table_id": manifest.loot_table_id,
            "level": manifest.level,
            "luck_modifier": manifest.luck_modifier,
            "exhausted": manifest.exhausted,
            "display_name": manifest.display_name,
            "active_pool_ids": manifest.active_pool_ids,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_loot_table(self, data: dict) -> LootTableManifest:
        return LootTableManifest(
            loot_table_id=data["loot_table_id"],
            loot_table_name=data.get("loot_table_name", ""),
            drop_condition=data.get("drop_condition", "Always"),
            roll_method=data.get("roll_method", "Weighted"),
            max_rolls=data.get("max_rolls", 1),
            min_rolls=data.get("min_rolls", 1),
            guaranteed_chance=data.get("guaranteed_chance", 0.0),
            enabled=data.get("enabled", True),
            loot_entry_ids=data.get("loot_entry_ids", []),
        )

    def load_loot_entry(self, data: dict) -> LootEntryManifest:
        return LootEntryManifest(
            loot_entry_id=data["loot_entry_id"],
            item_id=data.get("item_id", ""),
            rarity=data.get("rarity", "Common"),
            pool_type=data.get("pool_type", "Item"),
            drop_weight=data.get("drop_weight", 1.0),
            min_quantity=data.get("min_quantity", 1),
            max_quantity=data.get("max_quantity", 1),
            drop_chance=data.get("drop_chance", 1.0),
            enabled=data.get("enabled", True),
        )

    def validate(self, manifest: LootBodyManifest) -> bool:
        return bool(manifest.loot_body_id)

    @property
    def loaded_count(self) -> int:
        return len(self._manifests)

    def clear(self) -> None:
        self._manifests.clear()
