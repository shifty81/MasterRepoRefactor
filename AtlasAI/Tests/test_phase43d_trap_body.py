"""Phase 43D — Tests for TrapBodyRegistry.h and trap_body_loader.py."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    TrapBodyLoader,
    TrapBodyManifest,
    TrapTriggerZoneManifest,
    TrapEffectManifest,
)


def _read_header(name: str) -> str:
    return (SCENE_DIR / f"{name}.h").read_text()


# ---------------------------------------------------------------------------
# TrapBodyRegistry.h
# ---------------------------------------------------------------------------

class TestTrapBodyRegistryHeaderExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue((SCENE_DIR / "TrapBodyRegistry.h").exists())


class TestTrapBodyRegistryNamespace(unittest.TestCase):
    def test_namespace(self):
        self.assertIn("namespace Atlas::Engine", _read_header("TrapBodyRegistry"))


class TestTrapBodyRegistryEnums(unittest.TestCase):
    def test_trap_type_enum(self):
        self.assertIn("TrapType", _read_header("TrapBodyRegistry"))

    def test_trigger_condition_enum(self):
        self.assertIn("TriggerCondition", _read_header("TrapBodyRegistry"))

    def test_trap_state_enum(self):
        self.assertIn("TrapState", _read_header("TrapBodyRegistry"))

    def test_arming_method_enum(self):
        self.assertIn("ArmingMethod", _read_header("TrapBodyRegistry"))

    def test_spike_trap_type(self):
        self.assertIn("Spike", _read_header("TrapBodyRegistry"))

    def test_fire_trap_type(self):
        self.assertIn("Fire", _read_header("TrapBodyRegistry"))

    def test_poison_trap_type(self):
        self.assertIn("Poison", _read_header("TrapBodyRegistry"))

    def test_electric_trap_type(self):
        self.assertIn("Electric", _read_header("TrapBodyRegistry"))

    def test_explosive_trap_type(self):
        self.assertIn("Explosive", _read_header("TrapBodyRegistry"))

    def test_void_trap_type(self):
        self.assertIn("Void", _read_header("TrapBodyRegistry"))

    def test_on_enter_condition(self):
        self.assertIn("OnEnter", _read_header("TrapBodyRegistry"))

    def test_on_timer_condition(self):
        self.assertIn("OnTimer", _read_header("TrapBodyRegistry"))

    def test_armed_state(self):
        self.assertIn("Armed", _read_header("TrapBodyRegistry"))

    def test_depleted_state(self):
        self.assertIn("Depleted", _read_header("TrapBodyRegistry"))


class TestTrapBodyRegistryStructs(unittest.TestCase):
    def test_trap_effect_def_struct(self):
        self.assertIn("TrapEffectDef", _read_header("TrapBodyRegistry"))

    def test_trap_trigger_zone_def_struct(self):
        self.assertIn("TrapTriggerZoneDef", _read_header("TrapBodyRegistry"))

    def test_trap_body_record_struct(self):
        self.assertIn("TrapBodyRecord", _read_header("TrapBodyRegistry"))

    def test_damage_amount_in_effect(self):
        self.assertIn("damageAmount", _read_header("TrapBodyRegistry"))

    def test_zone_radius_in_zone(self):
        self.assertIn("zoneRadius", _read_header("TrapBodyRegistry"))

    def test_cooldown_ms_in_record(self):
        self.assertIn("cooldownMs", _read_header("TrapBodyRegistry"))

    def test_max_triggers_in_record(self):
        self.assertIn("maxTriggers", _read_header("TrapBodyRegistry"))


class TestTrapBodyRegistryMethods(unittest.TestCase):
    def test_register_trap_effect(self):
        self.assertIn("RegisterTrapEffect", _read_header("TrapBodyRegistry"))

    def test_unregister_trap_effect(self):
        self.assertIn("UnregisterTrapEffect", _read_header("TrapBodyRegistry"))

    def test_get_effects_by_type(self):
        self.assertIn("GetEffectsByType", _read_header("TrapBodyRegistry"))

    def test_register_trigger_zone(self):
        self.assertIn("RegisterTriggerZone", _read_header("TrapBodyRegistry"))

    def test_set_trigger_condition(self):
        self.assertIn("SetTriggerCondition", _read_header("TrapBodyRegistry"))

    def test_register_trap_body(self):
        self.assertIn("RegisterTrapBody", _read_header("TrapBodyRegistry"))

    def test_arm_trap(self):
        self.assertIn("ArmTrap", _read_header("TrapBodyRegistry"))

    def test_disarm_trap(self):
        self.assertIn("DisarmTrap", _read_header("TrapBodyRegistry"))

    def test_trigger_trap(self):
        self.assertIn("TriggerTrap", _read_header("TrapBodyRegistry"))

    def test_reset_trap(self):
        self.assertIn("ResetTrap", _read_header("TrapBodyRegistry"))

    def test_disable_trap(self):
        self.assertIn("DisableTrap", _read_header("TrapBodyRegistry"))

    def test_set_trap_state(self):
        self.assertIn("SetTrapState", _read_header("TrapBodyRegistry"))

    def test_add_effect_to_chain(self):
        self.assertIn("AddEffectToChain", _read_header("TrapBodyRegistry"))

    def test_get_trap_bodies_by_state(self):
        self.assertIn("GetTrapBodiesByState", _read_header("TrapBodyRegistry"))

    def test_get_armed_traps(self):
        self.assertIn("GetArmedTraps", _read_header("TrapBodyRegistry"))

    def test_get_depleted_traps(self):
        self.assertIn("GetDepletedTraps", _read_header("TrapBodyRegistry"))

    def test_clear(self):
        self.assertIn("Clear", _read_header("TrapBodyRegistry"))

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_header("TrapBodyRegistry"))

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_header("TrapBodyRegistry"))


# ---------------------------------------------------------------------------
# TrapEffectManifest
# ---------------------------------------------------------------------------

class TestTrapEffectManifest(unittest.TestCase):
    def test_effect_id(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike Damage")
        self.assertEqual(e.effect_id, "te_001")

    def test_effect_name(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike Damage")
        self.assertEqual(e.effect_name, "Spike Damage")

    def test_default_trap_type_spike(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike Damage")
        self.assertEqual(e.trap_type, "Spike")

    def test_is_spike_true(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike Damage", trap_type="Spike")
        self.assertTrue(e.is_spike)

    def test_is_fire_false(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike Damage", trap_type="Spike")
        self.assertFalse(e.is_fire)

    def test_is_fire_true(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Fire Burn", trap_type="Fire")
        self.assertTrue(e.is_fire)

    def test_is_poison_true(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Poison", trap_type="Poison")
        self.assertTrue(e.is_poison)

    def test_is_electric_true(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Zap", trap_type="Electric")
        self.assertTrue(e.is_electric)

    def test_is_explosive_true(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Boom", trap_type="Explosive")
        self.assertTrue(e.is_explosive)

    def test_is_void_true(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Void", trap_type="Void")
        self.assertTrue(e.is_void)

    def test_is_ice_true(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Freeze", trap_type="Ice")
        self.assertTrue(e.is_ice)

    def test_is_high_damage_false(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike", damage_amount=10.0)
        self.assertFalse(e.is_high_damage)

    def test_is_high_damage_true(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike", damage_amount=100.0)
        self.assertTrue(e.is_high_damage)

    def test_is_aoe_false(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike", effect_radius=0.5)
        self.assertFalse(e.is_aoe)

    def test_is_aoe_true(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Bomb", effect_radius=5.0)
        self.assertTrue(e.is_aoe)

    def test_has_particle_false(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike")
        self.assertFalse(e.has_particle)

    def test_has_particle_true(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike", particle_effect_id="pe_001")
        self.assertTrue(e.has_particle)

    def test_has_sound_false(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike")
        self.assertFalse(e.has_sound)

    def test_is_long_duration_false(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike", effect_duration=0.5)
        self.assertFalse(e.is_long_duration)

    def test_is_enabled_true(self):
        e = TrapEffectManifest(effect_id="te_001", effect_name="Spike", enabled=True)
        self.assertTrue(e.is_enabled)


# ---------------------------------------------------------------------------
# TrapTriggerZoneManifest
# ---------------------------------------------------------------------------

class TestTrapTriggerZoneManifest(unittest.TestCase):
    def test_trigger_zone_id(self):
        z = TrapTriggerZoneManifest(trigger_zone_id="tz_001", trap_body_id="tb_001")
        self.assertEqual(z.trigger_zone_id, "tz_001")

    def test_default_condition_on_enter(self):
        z = TrapTriggerZoneManifest(trigger_zone_id="tz_001", trap_body_id="tb_001")
        self.assertEqual(z.condition, "OnEnter")

    def test_is_on_enter_true(self):
        z = TrapTriggerZoneManifest(trigger_zone_id="tz_001", trap_body_id="tb_001", condition="OnEnter")
        self.assertTrue(z.is_on_enter)

    def test_is_on_exit_false(self):
        z = TrapTriggerZoneManifest(trigger_zone_id="tz_001", trap_body_id="tb_001", condition="OnEnter")
        self.assertFalse(z.is_on_exit)

    def test_is_on_exit_true(self):
        z = TrapTriggerZoneManifest(trigger_zone_id="tz_001", trap_body_id="tb_001", condition="OnExit")
        self.assertTrue(z.is_on_exit)

    def test_is_on_stay_true(self):
        z = TrapTriggerZoneManifest(trigger_zone_id="tz_001", trap_body_id="tb_001", condition="OnStay")
        self.assertTrue(z.is_on_stay)

    def test_is_on_timer_true(self):
        z = TrapTriggerZoneManifest(trigger_zone_id="tz_001", trap_body_id="tb_001", condition="OnTimer")
        self.assertTrue(z.is_on_timer)

    def test_is_player_only_false(self):
        z = TrapTriggerZoneManifest(trigger_zone_id="tz_001", trap_body_id="tb_001", player_only=False)
        self.assertFalse(z.is_player_only)

    def test_triggers_npcs_true(self):
        z = TrapTriggerZoneManifest(trigger_zone_id="tz_001", trap_body_id="tb_001", npc_trigger=True)
        self.assertTrue(z.triggers_npcs)

    def test_is_repeatable_false(self):
        z = TrapTriggerZoneManifest(trigger_zone_id="tz_001", trap_body_id="tb_001", repeat_trigger=False)
        self.assertFalse(z.is_repeatable)

    def test_is_large_zone_false(self):
        z = TrapTriggerZoneManifest(trigger_zone_id="tz_001", trap_body_id="tb_001", zone_radius=1.5)
        self.assertFalse(z.is_large_zone)

    def test_is_large_zone_true(self):
        z = TrapTriggerZoneManifest(trigger_zone_id="tz_001", trap_body_id="tb_001", zone_radius=10.0)
        self.assertTrue(z.is_large_zone)


# ---------------------------------------------------------------------------
# TrapBodyManifest
# ---------------------------------------------------------------------------

class TestTrapBodyManifest(unittest.TestCase):
    def test_trap_body_id(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001")
        self.assertEqual(m.trap_body_id, "tb_001")

    def test_owner_entity_id(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001")
        self.assertEqual(m.owner_entity_id, "dungeon_001")

    def test_default_state_idle(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001")
        self.assertEqual(m.state, "Idle")

    def test_is_idle_true(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", state="Idle")
        self.assertTrue(m.is_idle)

    def test_is_armed_false(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", state="Idle")
        self.assertFalse(m.is_armed)

    def test_is_armed_true(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", state="Armed")
        self.assertTrue(m.is_armed)

    def test_is_triggered_true(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", state="Triggered")
        self.assertTrue(m.is_triggered)

    def test_is_cooldown_true(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", state="Cooldown")
        self.assertTrue(m.is_cooldown)

    def test_is_depleted_true(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", state="Depleted")
        self.assertTrue(m.is_depleted)

    def test_is_disabled_true(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", state="Disabled")
        self.assertTrue(m.is_disabled)

    def test_is_unlimited_true(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", max_triggers=-1)
        self.assertTrue(m.is_unlimited)

    def test_is_unlimited_false(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", max_triggers=3)
        self.assertFalse(m.is_unlimited)

    def test_is_auto_armed_true(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", arming_method="Automatic")
        self.assertTrue(m.is_auto_armed)

    def test_has_delay_false(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", arming_delay_ms=0.0)
        self.assertFalse(m.has_delay)

    def test_has_delay_true(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", arming_delay_ms=500.0)
        self.assertTrue(m.has_delay)

    def test_has_long_cooldown_false(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", cooldown_ms=5000.0)
        self.assertFalse(m.has_long_cooldown)

    def test_effect_count_zero(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001")
        self.assertEqual(m.effect_count, 0)

    def test_has_effects_false(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001")
        self.assertFalse(m.has_effects)

    def test_is_lucky_false(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", luck_modifier=1.0)
        self.assertFalse(m.is_lucky)

    def test_has_zone_false(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001")
        self.assertFalse(m.has_zone)

    def test_has_zone_true(self):
        m = TrapBodyManifest(trap_body_id="tb_001", owner_entity_id="dungeon_001", zone_id="tz_001")
        self.assertTrue(m.has_zone)


# ---------------------------------------------------------------------------
# TrapBodyLoader
# ---------------------------------------------------------------------------

class TestTrapBodyLoader(unittest.TestCase):
    def setUp(self):
        self.loader = TrapBodyLoader()
        self.data = {
            "trap_body_id": "tb_001",
            "owner_entity_id": "dungeon_001",
            "zone_id": "tz_001",
            "state": "Idle",
            "arming_method": "Automatic",
            "trap_type": "Spike",
            "arming_delay_ms": 0.0,
            "cooldown_ms": 5000.0,
            "max_triggers": -1,
            "trigger_count": 0,
            "luck_modifier": 1.0,
            "enabled": True,
            "effect_chain_ids": ["te_001"],
        }

    def test_load_manifest(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.trap_body_id, "tb_001")

    def test_load_manifest_owner(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.owner_entity_id, "dungeon_001")

    def test_load_manifest_zone(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.zone_id, "tz_001")

    def test_load_manifest_state(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.state, "Idle")

    def test_load_manifest_trap_type(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.trap_type, "Spike")

    def test_load_manifest_cooldown(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertAlmostEqual(manifest.cooldown_ms, 5000.0)

    def test_load_manifest_effect_chain(self):
        manifest = self.loader.load_manifest(self.data)
        self.assertEqual(manifest.effect_chain_ids, ["te_001"])

    def test_load_batch(self):
        data2 = dict(self.data)
        data2["trap_body_id"] = "tb_002"
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
        save_path = REPO_ROOT / "AtlasAI" / "Tests" / "_test_trap_save.json"
        try:
            self.loader.save_manifest(manifest, save_path)
            loader2 = TrapBodyLoader()
            loaded = loader2.load_from_file(save_path)
            self.assertEqual(loaded.trap_body_id, "tb_001")
        finally:
            if save_path.exists():
                save_path.unlink()

    def test_load_trap_effect(self):
        effect_data = {
            "effect_id": "te_001",
            "effect_name": "Spike Damage",
            "trap_type": "Spike",
            "damage_amount": 15.0,
            "effect_radius": 0.5,
            "effect_duration": 0.2,
            "particle_effect_id": "pe_spike",
            "sound_cue_id": "sc_spike",
            "enabled": True,
        }
        effect = self.loader.load_trap_effect(effect_data)
        self.assertEqual(effect.effect_id, "te_001")
        self.assertEqual(effect.trap_type, "Spike")
        self.assertAlmostEqual(effect.damage_amount, 15.0)

    def test_load_trigger_zone(self):
        zone_data = {
            "trigger_zone_id": "tz_001",
            "trap_body_id": "tb_001",
            "condition": "OnEnter",
            "zone_radius": 2.0,
            "zone_height": 3.0,
            "player_only": False,
            "npc_trigger": True,
            "repeat_trigger": False,
            "enabled": True,
        }
        zone = self.loader.load_trigger_zone(zone_data)
        self.assertEqual(zone.trigger_zone_id, "tz_001")
        self.assertEqual(zone.condition, "OnEnter")
        self.assertAlmostEqual(zone.zone_radius, 2.0)


if __name__ == "__main__":
    unittest.main()
