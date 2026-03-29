"""Phase 42D — Tests for LootBodyRegistry.h and loot_body_loader.py."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    LootBodyLoader,
    LootBodyManifest,
    LootTableManifest,
    LootEntryManifest,
)


def _read_header(name: str) -> str:
    return (SCENE_DIR / f"{name}.h").read_text()


# ---------------------------------------------------------------------------
# LootBodyRegistry.h
# ---------------------------------------------------------------------------

class TestLootBodyRegistryHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "LootBodyRegistry.h").exists())


class TestLootBodyRegistryNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("LootBodyRegistry"))


class TestLootBodyRegistryEnums(unittest.TestCase):
    def test_loot_rarity_enum(self):
        self.assertIn("LootRarity", _read_header("LootBodyRegistry"))

    def test_drop_condition_enum(self):
        self.assertIn("DropCondition", _read_header("LootBodyRegistry"))

    def test_roll_method_enum(self):
        self.assertIn("RollMethod", _read_header("LootBodyRegistry"))

    def test_loot_pool_type_enum(self):
        self.assertIn("LootPoolType", _read_header("LootBodyRegistry"))

    def test_common_rarity_value(self):
        self.assertIn("Common", _read_header("LootBodyRegistry"))

    def test_legendary_rarity_value(self):
        self.assertIn("Legendary", _read_header("LootBodyRegistry"))

    def test_mythic_rarity_value(self):
        self.assertIn("Mythic", _read_header("LootBodyRegistry"))

    def test_on_kill_condition_value(self):
        self.assertIn("OnKill", _read_header("LootBodyRegistry"))

    def test_weighted_roll_value(self):
        self.assertIn("Weighted", _read_header("LootBodyRegistry"))

    def test_item_pool_type_value(self):
        self.assertIn("Item", _read_header("LootBodyRegistry"))

    def test_blueprint_pool_type_value(self):
        self.assertIn("Blueprint", _read_header("LootBodyRegistry"))


class TestLootBodyRegistryStructs(unittest.TestCase):
    def test_loot_entry_def_struct(self):
        self.assertIn("LootEntryDef", _read_header("LootBodyRegistry"))

    def test_loot_table_def_struct(self):
        self.assertIn("LootTableDef", _read_header("LootBodyRegistry"))

    def test_loot_body_record_struct(self):
        self.assertIn("LootBodyRecord", _read_header("LootBodyRegistry"))

    def test_drop_weight_in_entry(self):
        self.assertIn("dropWeight", _read_header("LootBodyRegistry"))

    def test_max_rolls_in_table(self):
        self.assertIn("maxRolls", _read_header("LootBodyRegistry"))

    def test_luck_modifier_in_record(self):
        self.assertIn("luckModifier", _read_header("LootBodyRegistry"))

    def test_drop_chance_in_entry(self):
        self.assertIn("dropChance", _read_header("LootBodyRegistry"))


class TestLootBodyRegistryMethods(unittest.TestCase):
    def test_register_loot_entry(self):
        self.assertIn("RegisterLootEntry", _read_header("LootBodyRegistry"))

    def test_unregister_loot_entry(self):
        self.assertIn("UnregisterLootEntry", _read_header("LootBodyRegistry"))

    def test_get_loot_entries_by_rarity(self):
        self.assertIn("GetLootEntriesByRarity", _read_header("LootBodyRegistry"))

    def test_get_loot_entries_by_pool(self):
        self.assertIn("GetLootEntriesByPool", _read_header("LootBodyRegistry"))

    def test_get_enabled_loot_entries(self):
        self.assertIn("GetEnabledLootEntries", _read_header("LootBodyRegistry"))

    def test_register_loot_table(self):
        self.assertIn("RegisterLootTable", _read_header("LootBodyRegistry"))

    def test_unregister_loot_table(self):
        self.assertIn("UnregisterLootTable", _read_header("LootBodyRegistry"))

    def test_add_entry_to_table(self):
        self.assertIn("AddEntryToTable", _read_header("LootBodyRegistry"))

    def test_remove_entry_from_table(self):
        self.assertIn("RemoveEntryFromTable", _read_header("LootBodyRegistry"))

    def test_set_drop_condition(self):
        self.assertIn("SetDropCondition", _read_header("LootBodyRegistry"))

    def test_set_roll_method(self):
        self.assertIn("SetRollMethod", _read_header("LootBodyRegistry"))

    def test_register_loot_body(self):
        self.assertIn("RegisterLootBody", _read_header("LootBodyRegistry"))

    def test_unregister_loot_body(self):
        self.assertIn("UnregisterLootBody", _read_header("LootBodyRegistry"))

    def test_exhaust_loot_body(self):
        self.assertIn("ExhaustLootBody", _read_header("LootBodyRegistry"))

    def test_reset_loot_body(self):
        self.assertIn("ResetLootBody", _read_header("LootBodyRegistry"))

    def test_set_luck_modifier(self):
        self.assertIn("SetLuckModifier", _read_header("LootBodyRegistry"))

    def test_get_exhausted_bodies(self):
        self.assertIn("GetExhaustedBodies", _read_header("LootBodyRegistry"))

    def test_get_active_bodies(self):
        self.assertIn("GetActiveBodies", _read_header("LootBodyRegistry"))

    def test_clear(self):
        self.assertIn("Clear", _read_header("LootBodyRegistry"))

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_header("LootBodyRegistry"))

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_header("LootBodyRegistry"))


# ---------------------------------------------------------------------------
# LootEntryManifest
# ---------------------------------------------------------------------------

class TestLootEntryManifest(unittest.TestCase):
    def test_loot_entry_id(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_sword")
        self.assertEqual(e.loot_entry_id, "le_001")

    def test_item_id(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_sword")
        self.assertEqual(e.item_id, "item_sword")

    def test_default_rarity_common(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_sword")
        self.assertEqual(e.rarity, "Common")

    def test_is_common_true(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_sword", rarity="Common")
        self.assertTrue(e.is_common)

    def test_is_rare_false(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_sword", rarity="Common")
        self.assertFalse(e.is_rare)

    def test_is_rare_true(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_sword", rarity="Rare")
        self.assertTrue(e.is_rare)

    def test_is_legendary_true(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_sword", rarity="Legendary")
        self.assertTrue(e.is_legendary)

    def test_is_mythic_true(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_sword", rarity="Mythic")
        self.assertTrue(e.is_mythic)

    def test_is_guaranteed_true(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_sword", drop_chance=1.0)
        self.assertTrue(e.is_guaranteed)

    def test_is_guaranteed_false(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_sword", drop_chance=0.5)
        self.assertFalse(e.is_guaranteed)

    def test_is_stackable_true(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_coin", max_quantity=5)
        self.assertTrue(e.is_stackable)

    def test_is_currency_true(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_gold", pool_type="Currency")
        self.assertTrue(e.is_currency)

    def test_is_blueprint_true(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_bp", pool_type="Blueprint")
        self.assertTrue(e.is_blueprint)

    def test_quantity_range(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_coin", min_quantity=1, max_quantity=5)
        self.assertEqual(e.quantity_range, 4)

    def test_is_enabled_true(self):
        e = LootEntryManifest(loot_entry_id="le_001", item_id="item_sword", enabled=True)
        self.assertTrue(e.is_enabled)


# ---------------------------------------------------------------------------
# LootTableManifest
# ---------------------------------------------------------------------------

class TestLootTableManifest(unittest.TestCase):
    def test_loot_table_id(self):
        t = LootTableManifest(loot_table_id="lt_001", loot_table_name="Boss Drop")
        self.assertEqual(t.loot_table_id, "lt_001")

    def test_loot_table_name(self):
        t = LootTableManifest(loot_table_id="lt_001", loot_table_name="Boss Drop")
        self.assertEqual(t.loot_table_name, "Boss Drop")

    def test_default_drop_condition_always(self):
        t = LootTableManifest(loot_table_id="lt_001", loot_table_name="Boss Drop")
        self.assertEqual(t.drop_condition, "Always")

    def test_is_always_drop_true(self):
        t = LootTableManifest(loot_table_id="lt_001", loot_table_name="Boss Drop", drop_condition="Always")
        self.assertTrue(t.is_always_drop)

    def test_is_on_kill_false(self):
        t = LootTableManifest(loot_table_id="lt_001", loot_table_name="Boss Drop", drop_condition="Always")
        self.assertFalse(t.is_on_kill)

    def test_is_on_kill_true(self):
        t = LootTableManifest(loot_table_id="lt_001", loot_table_name="Mob Drop", drop_condition="OnKill")
        self.assertTrue(t.is_on_kill)

    def test_is_weighted_true(self):
        t = LootTableManifest(loot_table_id="lt_001", loot_table_name="Boss Drop", roll_method="Weighted")
        self.assertTrue(t.is_weighted)

    def test_is_guaranteed_roll_true(self):
        t = LootTableManifest(loot_table_id="lt_001", loot_table_name="Boss Drop", roll_method="Guaranteed")
        self.assertTrue(t.is_guaranteed_roll)

    def test_has_guaranteed_chance_false(self):
        t = LootTableManifest(loot_table_id="lt_001", loot_table_name="Boss Drop", guaranteed_chance=0.0)
        self.assertFalse(t.has_guaranteed_chance)

    def test_has_entries_false(self):
        t = LootTableManifest(loot_table_id="lt_001", loot_table_name="Boss Drop")
        self.assertFalse(t.has_entries)

    def test_entry_count_zero(self):
        t = LootTableManifest(loot_table_id="lt_001", loot_table_name="Boss Drop")
        self.assertEqual(t.entry_count, 0)

    def test_max_possible_rolls(self):
        t = LootTableManifest(loot_table_id="lt_001", loot_table_name="Boss Drop", max_rolls=3)
        self.assertEqual(t.max_possible_rolls, 3)


# ---------------------------------------------------------------------------
# LootBodyManifest
# ---------------------------------------------------------------------------

class TestLootBodyManifest(unittest.TestCase):
    def test_loot_body_id(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001")
        self.assertEqual(m.loot_body_id, "lb_001")

    def test_owner_entity_id(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001")
        self.assertEqual(m.owner_entity_id, "boss_001")

    def test_is_exhausted_false(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001", exhausted=False)
        self.assertFalse(m.is_exhausted)

    def test_is_exhausted_true(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001", exhausted=True)
        self.assertTrue(m.is_exhausted)

    def test_is_active_true(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001", exhausted=False)
        self.assertTrue(m.is_active)

    def test_has_owner_true(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001")
        self.assertTrue(m.has_owner)

    def test_has_loot_table_false(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001")
        self.assertFalse(m.has_loot_table)

    def test_has_loot_table_true(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001", loot_table_id="lt_001")
        self.assertTrue(m.has_loot_table)

    def test_is_lucky_false(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001", luck_modifier=1.0)
        self.assertFalse(m.is_lucky)

    def test_is_lucky_true(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001", luck_modifier=1.5)
        self.assertTrue(m.is_lucky)

    def test_is_unlucky_true(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001", luck_modifier=0.5)
        self.assertTrue(m.is_unlucky)

    def test_has_display_name_false(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001")
        self.assertFalse(m.has_display_name)

    def test_has_display_name_true(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001", display_name="Dragon Hoard")
        self.assertTrue(m.has_display_name)

    def test_is_high_level_false(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001", level=10)
        self.assertFalse(m.is_high_level)

    def test_is_high_level_true(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001", level=60)
        self.assertTrue(m.is_high_level)

    def test_pool_count_zero(self):
        m = LootBodyManifest(loot_body_id="lb_001", owner_entity_id="boss_001")
        self.assertEqual(m.pool_count, 0)


# ---------------------------------------------------------------------------
# LootBodyLoader
# ---------------------------------------------------------------------------

class TestLootBodyLoader(unittest.TestCase):
    def setUp(self):
        self.loader = LootBodyLoader()
        self.data = {
            "loot_body_id": "lb_001",
            "owner_entity_id": "boss_001",
            "loot_table_id": "lt_001",
            "level": 20,
            "luck_modifier": 1.2,
            "exhausted": False,
            "display_name": "Dragon Hoard",
            "active_pool_ids": [],
        }

    def test_load_manifest(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.loot_body_id, "lb_001")

    def test_load_manifest_owner(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.owner_entity_id, "boss_001")

    def test_load_manifest_loot_table(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.loot_table_id, "lt_001")

    def test_load_manifest_level(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.level, 20)

    def test_load_manifest_luck(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertAlmostEqual(manifest.luck_modifier, 1.2)

    def test_load_batch(self):
        data2 = dict(self.data)
        data2["loot_body_id"] = "lb_002"
        data2["owner_entity_id"] = "mob_001"
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

    def test_save_and_load(self):
        manifest = self.loader.load_manifest(self.data)
        save_path = REPO_ROOT / "AtlasAI" / "Tests" / "_test_loot_save.json"
        try:
            self.loader.save_manifest(manifest, save_path)
            loader2 = LootBodyLoader()
            loaded = loader2.load_from_file(save_path)
            self.assertEqual(loaded.loot_body_id, "lb_001")
        finally:
            if save_path.exists():
                save_path.unlink()

    def test_display_name_loaded(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.display_name, "Dragon Hoard")

    def test_load_loot_table(self):
        table_data = {
            "loot_table_id": "lt_001",
            "loot_table_name": "Boss Drop",
            "drop_condition": "OnKill",
            "roll_method": "Weighted",
            "max_rolls": 3,
            "min_rolls": 1,
            "guaranteed_chance": 0.1,
            "enabled": True,
            "loot_entry_ids": ["le_001", "le_002"],
        }
        table = self.loader.load_loot_table(table_data)
        self.assertEqual(table.loot_table_id, "lt_001")
        self.assertEqual(table.drop_condition, "OnKill")
        self.assertEqual(table.entry_count, 2)

    def test_load_loot_entry(self):
        entry_data = {
            "loot_entry_id": "le_001",
            "item_id": "item_sword",
            "rarity": "Rare",
            "pool_type": "Item",
            "drop_weight": 2.0,
            "min_quantity": 1,
            "max_quantity": 1,
            "drop_chance": 0.3,
            "enabled": True,
        }
        entry = self.loader.load_loot_entry(entry_data)
        self.assertEqual(entry.loot_entry_id, "le_001")
        self.assertEqual(entry.rarity, "Rare")
        self.assertAlmostEqual(entry.drop_weight, 2.0)


if __name__ == "__main__":
    unittest.main()
