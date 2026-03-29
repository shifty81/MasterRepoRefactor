"""AtlasAI Phase 41D — Inventory Body Loader.

Discovers and manages inventory body manifests, mirroring the C++
InventoryBodyRegistry for cross-language inventory management.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class InventoryItemManifest:
    item_id: str
    item_name: str
    rarity: str = "Common"
    category: str = "Misc"
    stack_policy: str = "NoStack"
    max_stack: int = 1
    weight: float = 1.0
    value: int = 0
    icon_asset_id: str = ""
    tradeable: bool = True
    destroyable: bool = True

    @property
    def is_common(self) -> bool:
        return self.rarity == "Common"

    @property
    def is_legendary(self) -> bool:
        return self.rarity == "Legendary"

    @property
    def is_rare(self) -> bool:
        return self.rarity in ("Rare", "Epic", "Legendary", "Unique")

    @property
    def is_stackable(self) -> bool:
        return self.stack_policy in ("Stack", "StackCapped")

    @property
    def is_tradeable(self) -> bool:
        return self.tradeable

    @property
    def has_icon(self) -> bool:
        return bool(self.icon_asset_id)

    @property
    def is_weapon(self) -> bool:
        return self.category == "Weapon"

    @property
    def is_consumable(self) -> bool:
        return self.category == "Consumable"


@dataclass
class InventorySlotManifest:
    slot_id: str
    container_id: str
    slot_type: str = "Bag"
    item_id: str = ""
    quantity: int = 0
    slot_index: int = 0
    locked: bool = False

    @property
    def is_occupied(self) -> bool:
        return bool(self.item_id) and self.quantity > 0

    @property
    def is_empty(self) -> bool:
        return not self.is_occupied

    @property
    def is_locked(self) -> bool:
        return self.locked

    @property
    def is_equipment_slot(self) -> bool:
        return self.slot_type not in ("Bag", "Custom")

    @property
    def has_stack(self) -> bool:
        return self.quantity > 1


@dataclass
class InventoryBodyManifest:
    container_id: str
    owner_entity_id: str
    inventory_state: str = "Active"
    max_slots: int = 20
    max_weight: float = 100.0
    current_weight: float = 0.0
    display_name: str = ""
    slots: list = field(default_factory=list)

    @property
    def is_active(self) -> bool:
        return self.inventory_state == "Active"

    @property
    def is_locked(self) -> bool:
        return self.inventory_state == "Locked"

    @property
    def is_full(self) -> bool:
        return self.inventory_state == "Full"

    @property
    def is_empty(self) -> bool:
        return self.inventory_state == "Empty"

    @property
    def is_overweight(self) -> bool:
        return self.inventory_state == "Overweight"

    @property
    def has_owner(self) -> bool:
        return bool(self.owner_entity_id)

    @property
    def weight_ratio(self) -> float:
        if self.max_weight <= 0:
            return 0.0
        return min(1.0, self.current_weight / self.max_weight)

    @property
    def slot_count(self) -> int:
        return len(self.slots)

    @property
    def has_slots(self) -> bool:
        return len(self.slots) > 0

    @property
    def has_display_name(self) -> bool:
        return bool(self.display_name)


class InventoryBodyLoader:
    """Loader for inventory body manifests."""

    def __init__(self) -> None:
        self._manifests: dict = {}

    def load_manifest(self, data: dict) -> InventoryBodyManifest:
        slots = []
        for s in data.get("slots", []):
            slot = InventorySlotManifest(
                slot_id=s.get("slot_id", ""),
                container_id=s.get("container_id", data.get("container_id", "")),
                slot_type=s.get("slot_type", "Bag"),
                item_id=s.get("item_id", ""),
                quantity=s.get("quantity", 0),
                slot_index=s.get("slot_index", 0),
                locked=s.get("locked", False),
            )
            slots.append(slot)

        manifest = InventoryBodyManifest(
            container_id=data["container_id"],
            owner_entity_id=data.get("owner_entity_id", ""),
            inventory_state=data.get("inventory_state", "Active"),
            max_slots=data.get("max_slots", 20),
            max_weight=data.get("max_weight", 100.0),
            current_weight=data.get("current_weight", 0.0),
            display_name=data.get("display_name", ""),
            slots=slots,
        )
        self._manifests[manifest.container_id] = manifest
        return manifest

    def load_batch(self, data_list: list) -> list:
        return [self.load_manifest(d) for d in data_list]

    def load_from_file(self, path) -> InventoryBodyManifest:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def save_manifest(self, manifest: InventoryBodyManifest, path) -> None:
        slots_data = []
        for s in manifest.slots:
            slots_data.append({
                "slot_id": s.slot_id,
                "container_id": s.container_id,
                "slot_type": s.slot_type,
                "item_id": s.item_id,
                "quantity": s.quantity,
                "slot_index": s.slot_index,
                "locked": s.locked,
            })
        data = {
            "container_id": manifest.container_id,
            "owner_entity_id": manifest.owner_entity_id,
            "inventory_state": manifest.inventory_state,
            "max_slots": manifest.max_slots,
            "max_weight": manifest.max_weight,
            "current_weight": manifest.current_weight,
            "display_name": manifest.display_name,
            "slots": slots_data,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def validate(self, manifest: InventoryBodyManifest) -> bool:
        return bool(manifest.container_id)

    @property
    def loaded_count(self) -> int:
        return len(self._manifests)

    def clear(self) -> None:
        self._manifests.clear()
