"""Phase 41D — Tests for InventoryBodyRegistry.h and inventory_body_loader.py."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    InventoryBodyLoader,
    InventoryBodyManifest,
    InventoryItemManifest,
    InventorySlotManifest,
)


def _read_header(name: str) -> str:
    return (SCENE_DIR / f"{name}.h").read_text()


# ---------------------------------------------------------------------------
# InventoryBodyRegistry.h
# ---------------------------------------------------------------------------

class TestInventoryBodyRegistryHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "InventoryBodyRegistry.h").exists())


class TestInventoryBodyRegistryNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("InventoryBodyRegistry"))


class TestInventoryBodyRegistryEnums(unittest.TestCase):
    def test_item_rarity_enum(self):
        self.assertIn("ItemRarity", _read_header("InventoryBodyRegistry"))

    def test_item_category_enum(self):
        self.assertIn("ItemCategory", _read_header("InventoryBodyRegistry"))

    def test_slot_type_enum(self):
        self.assertIn("SlotType", _read_header("InventoryBodyRegistry"))

    def test_inventory_state_enum(self):
        self.assertIn("InventoryState", _read_header("InventoryBodyRegistry"))

    def test_stack_policy_enum(self):
        self.assertIn("StackPolicy", _read_header("InventoryBodyRegistry"))

    def test_common_rarity_value(self):
        self.assertIn("Common", _read_header("InventoryBodyRegistry"))

    def test_legendary_rarity_value(self):
        self.assertIn("Legendary", _read_header("InventoryBodyRegistry"))

    def test_weapon_category_value(self):
        self.assertIn("Weapon", _read_header("InventoryBodyRegistry"))

    def test_consumable_category_value(self):
        self.assertIn("Consumable", _read_header("InventoryBodyRegistry"))

    def test_active_state_value(self):
        self.assertIn("Active", _read_header("InventoryBodyRegistry"))

    def test_locked_state_value(self):
        self.assertIn("Locked", _read_header("InventoryBodyRegistry"))


class TestInventoryBodyRegistryStructs(unittest.TestCase):
    def test_item_def_struct(self):
        self.assertIn("ItemDef", _read_header("InventoryBodyRegistry"))

    def test_inventory_slot_def_struct(self):
        self.assertIn("InventorySlotDef", _read_header("InventoryBodyRegistry"))

    def test_inventory_body_record_struct(self):
        self.assertIn("InventoryBodyRecord", _read_header("InventoryBodyRegistry"))

    def test_max_stack_in_item(self):
        self.assertIn("maxStack", _read_header("InventoryBodyRegistry"))

    def test_max_slots_in_record(self):
        self.assertIn("maxSlots", _read_header("InventoryBodyRegistry"))

    def test_weight_in_item(self):
        self.assertIn("weight", _read_header("InventoryBodyRegistry"))

    def test_quantity_in_slot(self):
        self.assertIn("quantity", _read_header("InventoryBodyRegistry"))


class TestInventoryBodyRegistryMethods(unittest.TestCase):
    def test_register_item(self):
        self.assertIn("RegisterItem", _read_header("InventoryBodyRegistry"))

    def test_unregister_item(self):
        self.assertIn("UnregisterItem", _read_header("InventoryBodyRegistry"))

    def test_get_items_by_rarity(self):
        self.assertIn("GetItemsByRarity", _read_header("InventoryBodyRegistry"))

    def test_get_items_by_category(self):
        self.assertIn("GetItemsByCategory", _read_header("InventoryBodyRegistry"))

    def test_get_tradeable_items(self):
        self.assertIn("GetTradeableItems", _read_header("InventoryBodyRegistry"))

    def test_get_stackable_items(self):
        self.assertIn("GetStackableItems", _read_header("InventoryBodyRegistry"))

    def test_register_container(self):
        self.assertIn("RegisterContainer", _read_header("InventoryBodyRegistry"))

    def test_unregister_container(self):
        self.assertIn("UnregisterContainer", _read_header("InventoryBodyRegistry"))

    def test_set_container_state(self):
        self.assertIn("SetContainerState", _read_header("InventoryBodyRegistry"))

    def test_lock_container(self):
        self.assertIn("LockContainer", _read_header("InventoryBodyRegistry"))

    def test_get_containers_by_owner(self):
        self.assertIn("GetContainersByOwner", _read_header("InventoryBodyRegistry"))

    def test_get_full_containers(self):
        self.assertIn("GetFullContainers", _read_header("InventoryBodyRegistry"))

    def test_add_slot(self):
        self.assertIn("AddSlot", _read_header("InventoryBodyRegistry"))

    def test_remove_slot(self):
        self.assertIn("RemoveSlot", _read_header("InventoryBodyRegistry"))

    def test_set_slot_item(self):
        self.assertIn("SetSlotItem", _read_header("InventoryBodyRegistry"))

    def test_clear_slot(self):
        self.assertIn("ClearSlot", _read_header("InventoryBodyRegistry"))

    def test_move_item(self):
        self.assertIn("MoveItem", _read_header("InventoryBodyRegistry"))

    def test_get_occupied_slots(self):
        self.assertIn("GetOccupiedSlots", _read_header("InventoryBodyRegistry"))

    def test_get_free_slots(self):
        self.assertIn("GetFreeSlots", _read_header("InventoryBodyRegistry"))

    def test_get_locked_slots(self):
        self.assertIn("GetLockedSlots", _read_header("InventoryBodyRegistry"))

    def test_clear(self):
        self.assertIn("Clear", _read_header("InventoryBodyRegistry"))

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_header("InventoryBodyRegistry"))

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_header("InventoryBodyRegistry"))


# ---------------------------------------------------------------------------
# InventoryItemManifest
# ---------------------------------------------------------------------------

class TestInventoryItemManifest(unittest.TestCase):
    def test_item_id(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword")
        self.assertEqual(i.item_id, "item_001")

    def test_item_name(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword")
        self.assertEqual(i.item_name, "Iron Sword")

    def test_default_rarity_common(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword")
        self.assertEqual(i.rarity, "Common")

    def test_is_common_true(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword", rarity="Common")
        self.assertTrue(i.is_common)

    def test_is_legendary_false(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword", rarity="Common")
        self.assertFalse(i.is_legendary)

    def test_is_legendary_true(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Ancient Blade", rarity="Legendary")
        self.assertTrue(i.is_legendary)

    def test_is_rare_false(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword", rarity="Common")
        self.assertFalse(i.is_rare)

    def test_is_rare_true(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword", rarity="Rare")
        self.assertTrue(i.is_rare)

    def test_is_stackable_false(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword", stack_policy="NoStack")
        self.assertFalse(i.is_stackable)

    def test_is_stackable_true(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Gold Coin", stack_policy="Stack")
        self.assertTrue(i.is_stackable)

    def test_is_tradeable_true(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword", tradeable=True)
        self.assertTrue(i.is_tradeable)

    def test_has_icon_false(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword")
        self.assertFalse(i.has_icon)

    def test_has_icon_true(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword", icon_asset_id="icon_sword")
        self.assertTrue(i.has_icon)

    def test_is_weapon_true(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword", category="Weapon")
        self.assertTrue(i.is_weapon)

    def test_is_consumable_false(self):
        i = InventoryItemManifest(item_id="item_001", item_name="Iron Sword", category="Weapon")
        self.assertFalse(i.is_consumable)


# ---------------------------------------------------------------------------
# InventorySlotManifest
# ---------------------------------------------------------------------------

class TestInventorySlotManifest(unittest.TestCase):
    def test_slot_id(self):
        s = InventorySlotManifest(slot_id="slot_001", container_id="cont_001")
        self.assertEqual(s.slot_id, "slot_001")

    def test_is_occupied_false(self):
        s = InventorySlotManifest(slot_id="slot_001", container_id="cont_001")
        self.assertFalse(s.is_occupied)

    def test_is_occupied_true(self):
        s = InventorySlotManifest(slot_id="slot_001", container_id="cont_001", item_id="item_001", quantity=1)
        self.assertTrue(s.is_occupied)

    def test_is_empty_true(self):
        s = InventorySlotManifest(slot_id="slot_001", container_id="cont_001")
        self.assertTrue(s.is_empty)

    def test_is_locked_false(self):
        s = InventorySlotManifest(slot_id="slot_001", container_id="cont_001", locked=False)
        self.assertFalse(s.is_locked)

    def test_is_locked_true(self):
        s = InventorySlotManifest(slot_id="slot_001", container_id="cont_001", locked=True)
        self.assertTrue(s.is_locked)

    def test_is_equipment_slot_false(self):
        s = InventorySlotManifest(slot_id="slot_001", container_id="cont_001", slot_type="Bag")
        self.assertFalse(s.is_equipment_slot)

    def test_is_equipment_slot_true(self):
        s = InventorySlotManifest(slot_id="slot_001", container_id="cont_001", slot_type="Weapon")
        self.assertTrue(s.is_equipment_slot)

    def test_has_stack_false(self):
        s = InventorySlotManifest(slot_id="slot_001", container_id="cont_001", quantity=1)
        self.assertFalse(s.has_stack)

    def test_has_stack_true(self):
        s = InventorySlotManifest(slot_id="slot_001", container_id="cont_001", item_id="item_001", quantity=5)
        self.assertTrue(s.has_stack)


# ---------------------------------------------------------------------------
# InventoryBodyManifest
# ---------------------------------------------------------------------------

class TestInventoryBodyManifest(unittest.TestCase):
    def test_container_id(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001")
        self.assertEqual(m.container_id, "cont_001")

    def test_owner_entity_id(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001")
        self.assertEqual(m.owner_entity_id, "player_001")

    def test_default_state_active(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001")
        self.assertEqual(m.inventory_state, "Active")

    def test_is_active_true(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001", inventory_state="Active")
        self.assertTrue(m.is_active)

    def test_is_locked_false(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001", inventory_state="Active")
        self.assertFalse(m.is_locked)

    def test_is_locked_true(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001", inventory_state="Locked")
        self.assertTrue(m.is_locked)

    def test_is_full_false(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001", inventory_state="Active")
        self.assertFalse(m.is_full)

    def test_is_full_true(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001", inventory_state="Full")
        self.assertTrue(m.is_full)

    def test_is_overweight_true(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001", inventory_state="Overweight")
        self.assertTrue(m.is_overweight)

    def test_has_owner_true(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001")
        self.assertTrue(m.has_owner)

    def test_weight_ratio_zero(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001", current_weight=0.0, max_weight=100.0)
        self.assertAlmostEqual(m.weight_ratio, 0.0)

    def test_weight_ratio_half(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001", current_weight=50.0, max_weight=100.0)
        self.assertAlmostEqual(m.weight_ratio, 0.5)

    def test_has_slots_false(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001")
        self.assertFalse(m.has_slots)

    def test_slot_count_zero(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001")
        self.assertEqual(m.slot_count, 0)

    def test_has_display_name_false(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001")
        self.assertFalse(m.has_display_name)

    def test_has_display_name_true(self):
        m = InventoryBodyManifest(container_id="cont_001", owner_entity_id="player_001", display_name="Main Bag")
        self.assertTrue(m.has_display_name)


# ---------------------------------------------------------------------------
# InventoryBodyLoader
# ---------------------------------------------------------------------------

class TestInventoryBodyLoader(unittest.TestCase):
    def setUp(self):
        self.loader = InventoryBodyLoader()
        self.data = {
            "container_id": "cont_001",
            "owner_entity_id": "player_001",
            "inventory_state": "Active",
            "max_slots": 20,
            "max_weight": 100.0,
            "current_weight": 0.0,
            "display_name": "Player Bag",
            "slots": [],
        }

    def test_load_manifest(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.container_id, "cont_001")

    def test_load_manifest_owner(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.owner_entity_id, "player_001")

    def test_load_manifest_state(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.inventory_state, "Active")

    def test_load_manifest_max_slots(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.max_slots, 20)

    def test_load_batch(self):
        data2 = dict(self.data)
        data2["container_id"] = "cont_002"
        data2["owner_entity_id"] = "npc_001"
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

    def test_slots_loaded(self):
        data = dict(self.data)
        data["slots"] = [
            {
                "slot_id": "slot_001",
                "container_id": "cont_001",
                "slot_type": "Bag",
                "item_id": "item_sword",
                "quantity": 1,
                "slot_index": 0,
                "locked": False,
            }
        ]
        manifest = self.loader.load_manifest(data)
        self.assertEqual(len(manifest.slots), 1)
        s = manifest.slots[0]
        self.assertEqual(s.slot_id, "slot_001")
        self.assertEqual(s.item_id, "item_sword")
        self.assertEqual(s.quantity, 1)

    def test_save_and_load(self):
        manifest = self.loader.load_manifest(self.data)
        save_path = REPO_ROOT / "AtlasAI" / "Tests" / "_test_inv_save.json"
        try:
            self.loader.save_manifest(manifest, save_path)
            loader2 = InventoryBodyLoader()
            loaded = loader2.load_from_file(save_path)
            self.assertEqual(loaded.container_id, "cont_001")
        finally:
            if save_path.exists():
                save_path.unlink()

    def test_display_name_loaded(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.display_name, "Player Bag")


if __name__ == "__main__":
    unittest.main()
