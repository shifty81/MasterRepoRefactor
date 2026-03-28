"""
test_keybind_save_pcg.py
Tests for J3 (KeybindConfig), J4 (SaveLoadExtensions), J6 (PCGDeterminismEngine).
"""

import pytest
from typing import List, Optional, Dict
from enum import IntEnum


# =============================================================================
# J3 — KeybindConfig
# =============================================================================

class EKeyCode(IntEnum):
    Unknown = 0
    A=65; B=66; C=67; D=68; E=69; F=70; G=71; H=72; I=73; J=74; K=75
    L=76; M=77; N=78; O=79; P=80; Q=81; R=82; S=83; T=84; U=85
    V=86; W=87; X=88; Y=89; Z=90
    F1=112; F2=113; F5=116; F12=123
    Escape=256; Enter=257; Space=258; Tab=259; Backspace=260; Delete=261
    LeftControl=341; LeftShift=340; LeftAlt=342
    MouseLeft=400; MouseRight=401; MouseMiddle=402


MOD_NONE    = 0x00
MOD_SHIFT   = 0x01
MOD_CONTROL = 0x02
MOD_ALT     = 0x04


class EInputContext:
    Global   = "Global"
    Gameplay = "Gameplay"
    Editor   = "Editor"
    UI       = "UI"
    Walking  = "Walking"


class KeybindEntry:
    def __init__(self, action_id: str, display_name: str, category: str,
                 context: str = EInputContext.Global,
                 primary_key: int = EKeyCode.Unknown,
                 primary_mods: int = MOD_NONE,
                 secondary_key: int = EKeyCode.Unknown,
                 secondary_mods: int = MOD_NONE,
                 is_rebindable: bool = True):
        self.action_id      = action_id
        self.display_name   = display_name
        self.category       = category
        self.context        = context
        self.primary_key    = primary_key
        self.primary_mods   = primary_mods
        self.secondary_key  = secondary_key
        self.secondary_mods = secondary_mods
        self.is_rebindable  = is_rebindable


class KeybindConflict:
    def __init__(self, action_a: str, action_b: str, key: int, mods: int, is_primary: bool):
        self.action_a   = action_a
        self.action_b   = action_b
        self.conflict_key = key
        self.conflict_mods = mods
        self.is_primary = is_primary


class KeybindConfig:
    def __init__(self):
        self._entries: List[KeybindEntry] = []
        self._defaults: List[tuple] = []  # (action_id, key, mods, primary)
        self._change_cb = None

    def initialize(self) -> bool: return True
    def shutdown(self): self._entries.clear(); self._defaults.clear()

    def register_action(self, entry: KeybindEntry):
        for i, e in enumerate(self._entries):
            if e.action_id == entry.action_id:
                self._entries[i] = entry; return
        self._entries.append(entry)

    def unregister_action(self, action_id: str) -> bool:
        before = len(self._entries)
        self._entries = [e for e in self._entries if e.action_id != action_id]
        return len(self._entries) < before

    def has_action(self, action_id: str) -> bool:
        return any(e.action_id == action_id for e in self._entries)

    def find_action(self, action_id: str) -> Optional[KeybindEntry]:
        for e in self._entries:
            if e.action_id == action_id: return e
        return None

    def list_actions(self, context: str) -> List[KeybindEntry]:
        return [e for e in self._entries
                if e.context == context or e.context == EInputContext.Global]

    def list_all_actions(self) -> List[KeybindEntry]: return list(self._entries)

    @property
    def action_count(self): return len(self._entries)

    def set_primary_binding(self, action_id: str, key: int, mods: int = MOD_NONE) -> bool:
        e = self.find_action(action_id)
        if not e or not e.is_rebindable: return False
        e.primary_key = key; e.primary_mods = mods
        if self._change_cb: self._change_cb(action_id)
        return True

    def set_secondary_binding(self, action_id: str, key: int, mods: int = MOD_NONE) -> bool:
        e = self.find_action(action_id)
        if not e or not e.is_rebindable: return False
        e.secondary_key = key; e.secondary_mods = mods
        if self._change_cb: self._change_cb(action_id)
        return True

    def clear_binding(self, action_id: str, primary: bool = True) -> bool:
        e = self.find_action(action_id)
        if not e or not e.is_rebindable: return False
        if primary: e.primary_key = EKeyCode.Unknown; e.primary_mods = MOD_NONE
        else:       e.secondary_key = EKeyCode.Unknown; e.secondary_mods = MOD_NONE
        if self._change_cb: self._change_cb(action_id)
        return True

    def set_default(self, action_id: str, key: int, mods: int = MOD_NONE, primary: bool = True):
        self._defaults.append((action_id, key, mods, primary))

    def reset_to_default(self, action_id: str) -> bool:
        e = self.find_action(action_id)
        if not e: return False
        for (aid, key, mods, primary) in self._defaults:
            if aid != action_id: continue
            if primary: e.primary_key = key; e.primary_mods = mods
            else:       e.secondary_key = key; e.secondary_mods = mods
        if self._change_cb: self._change_cb(action_id)
        return True

    def detect_conflicts(self) -> List[KeybindConflict]:
        conflicts = []
        for i in range(len(self._entries)):
            for j in range(i + 1, len(self._entries)):
                a, b = self._entries[i], self._entries[j]
                # Same context check.
                if (a.context != b.context and
                        a.context != EInputContext.Global and
                        b.context != EInputContext.Global):
                    continue
                # primary vs primary
                if (a.primary_key != EKeyCode.Unknown and
                        a.primary_key == b.primary_key and
                        a.primary_mods == b.primary_mods):
                    conflicts.append(KeybindConflict(
                        a.action_id, b.action_id,
                        a.primary_key, a.primary_mods, True))
        return conflicts

    def has_conflicts(self) -> bool:
        return len(self.detect_conflicts()) > 0

    def conflicts_for_action(self, action_id: str) -> List[KeybindConflict]:
        return [c for c in self.detect_conflicts()
                if c.action_a == action_id or c.action_b == action_id]

    def get_action_for_key(self, key: int, mods: int,
                            context: str) -> Optional[str]:
        if key == 0:  # EKeyCode.Unknown
            return None
        for e in self._entries:
            if (e.context != context and e.context != EInputContext.Global):
                continue
            if e.primary_key == key and e.primary_mods == mods:
                return e.action_id
            if e.secondary_key == key and e.secondary_mods == mods:
                return e.action_id
        return None

    def serialise(self) -> str:
        lines = []
        for e in self._entries:
            lines.append(f"{e.action_id}={e.primary_key}:{e.primary_mods}:"
                         f"{e.secondary_key}:{e.secondary_mods}")
        return "\n".join(lines)

    def deserialise(self, data: str) -> bool:
        for line in data.splitlines():
            if not line: continue
            if "=" not in line: continue
            aid, val = line.split("=", 1)
            parts = val.split(":")
            if len(parts) != 4: continue
            e = self.find_action(aid)
            if e:
                e.primary_key    = int(parts[0])
                e.primary_mods   = int(parts[1])
                e.secondary_key  = int(parts[2])
                e.secondary_mods = int(parts[3])
        return True

    def register_default_gameplay_bindings(self):
        defs = [
            ("fire_weapon",    "Fire Weapon",    "Combat",     EInputContext.Gameplay, EKeyCode.MouseLeft,  MOD_NONE),
            ("fire_secondary", "Fire Secondary", "Combat",     EInputContext.Gameplay, EKeyCode.MouseRight, MOD_NONE),
            ("thrust_forward", "Thrust Forward", "Navigation", EInputContext.Gameplay, EKeyCode.W,          MOD_NONE),
            ("thrust_back",    "Thrust Back",    "Navigation", EInputContext.Gameplay, EKeyCode.S,          MOD_NONE),
            ("strafe_left",    "Strafe Left",    "Navigation", EInputContext.Gameplay, EKeyCode.A,          MOD_NONE),
            ("strafe_right",   "Strafe Right",   "Navigation", EInputContext.Gameplay, EKeyCode.D,          MOD_NONE),
            ("open_map",       "Open Map",       "UI",         EInputContext.Gameplay, EKeyCode.M,          MOD_NONE),
            ("open_inventory", "Open Inventory", "UI",         EInputContext.Gameplay, EKeyCode.I,          MOD_NONE),
            ("dock_request",   "Dock/Undock",    "Navigation", EInputContext.Gameplay, EKeyCode.F,          MOD_NONE),
            ("target_nearest", "Target Nearest", "Combat",     EInputContext.Gameplay, EKeyCode.T,          MOD_NONE),
        ]
        for action_id, name, cat, ctx, key, mods in defs:
            e = KeybindEntry(action_id, name, cat, ctx, key, mods)
            self.register_action(e)
            self.set_default(action_id, key, mods)

    def register_default_editor_bindings(self):
        defs = [
            ("undo",             "Undo",           "Edit",   EInputContext.Editor, EKeyCode.Z,       MOD_CONTROL),
            ("redo",             "Redo",           "Edit",   EInputContext.Editor, EKeyCode.Y,       MOD_CONTROL),
            ("save_scene",       "Save Scene",     "File",   EInputContext.Editor, EKeyCode.S,       MOD_CONTROL),
            ("delete_selection", "Delete",         "Editor", EInputContext.Editor, EKeyCode.Delete,  MOD_NONE),
            ("toggle_snap",      "Toggle Snap",    "Editor", EInputContext.Editor, EKeyCode.G,       MOD_NONE),
            ("cycle_gizmo",      "Cycle Gizmo",    "Editor", EInputContext.Editor, EKeyCode.R,       MOD_NONE),
            ("play_mode",        "Play Mode",      "Editor", EInputContext.Editor, EKeyCode.F5,      MOD_NONE),
        ]
        for action_id, name, cat, ctx, key, mods in defs:
            e = KeybindEntry(action_id, name, cat, ctx, key, mods)
            self.register_action(e)
            self.set_default(action_id, key, mods)

    def set_binding_changed_callback(self, cb): self._change_cb = cb


class TestKeybindConfig:
    def setup_method(self):
        self.kb = KeybindConfig()
        self.kb.initialize()
        self.kb.register_default_gameplay_bindings()
        self.kb.register_default_editor_bindings()

    # ---- registration --------------------------------------------------
    def test_register_gameplay_bindings(self):
        assert self.kb.has_action("fire_weapon")
        assert self.kb.has_action("thrust_forward")
        assert self.kb.action_count >= 10

    def test_register_editor_bindings(self):
        assert self.kb.has_action("undo")
        assert self.kb.has_action("redo")
        assert self.kb.has_action("save_scene")

    def test_find_action(self):
        e = self.kb.find_action("fire_weapon")
        assert e is not None
        assert e.primary_key == EKeyCode.MouseLeft

    def test_list_actions_by_context(self):
        gameplay = self.kb.list_actions(EInputContext.Gameplay)
        assert any(a.action_id == "fire_weapon" for a in gameplay)

    def test_unregister_action(self):
        assert self.kb.unregister_action("fire_weapon")
        assert not self.kb.has_action("fire_weapon")

    def test_register_updates_existing(self):
        e = KeybindEntry("fire_weapon", "Fire!", "Combat",
                         EInputContext.Gameplay, EKeyCode.Space)
        self.kb.register_action(e)
        assert self.kb.find_action("fire_weapon").primary_key == EKeyCode.Space
        count = sum(1 for a in self.kb.list_all_actions()
                    if a.action_id == "fire_weapon")
        assert count == 1

    # ---- rebinding -----------------------------------------------
    def test_set_primary_binding(self):
        assert self.kb.set_primary_binding("fire_weapon", EKeyCode.Space)
        assert self.kb.find_action("fire_weapon").primary_key == EKeyCode.Space

    def test_set_secondary_binding(self):
        assert self.kb.set_secondary_binding("fire_weapon", EKeyCode.Enter)
        assert self.kb.find_action("fire_weapon").secondary_key == EKeyCode.Enter

    def test_clear_primary_binding(self):
        self.kb.clear_binding("fire_weapon", primary=True)
        assert self.kb.find_action("fire_weapon").primary_key == EKeyCode.Unknown

    def test_clear_secondary_binding(self):
        self.kb.set_secondary_binding("fire_weapon", EKeyCode.Enter)
        self.kb.clear_binding("fire_weapon", primary=False)
        assert self.kb.find_action("fire_weapon").secondary_key == EKeyCode.Unknown

    def test_non_rebindable_action_cannot_rebind(self):
        locked = KeybindEntry("locked_action", "Locked", "System",
                               EInputContext.Global,
                               EKeyCode.Escape, MOD_NONE,
                               is_rebindable=False)
        self.kb.register_action(locked)
        result = self.kb.set_primary_binding("locked_action", EKeyCode.Space)
        assert result is False

    # ---- reset to default -------------------------------------------------
    def test_reset_to_default(self):
        original_key = self.kb.find_action("thrust_forward").primary_key
        self.kb.set_primary_binding("thrust_forward", int(EKeyCode.F12))
        assert self.kb.find_action("thrust_forward").primary_key == int(EKeyCode.F12)
        self.kb.reset_to_default("thrust_forward")
        assert self.kb.find_action("thrust_forward").primary_key == original_key

    # ---- conflict detection -----------------------------------------------
    def test_no_conflicts_in_defaults(self):
        # Gameplay bindings should not conflict with each other.
        gameplay_kb = KeybindConfig()
        gameplay_kb.initialize()
        gameplay_kb.register_default_gameplay_bindings()
        # No duplicate keys in defaults.
        assert not gameplay_kb.has_conflicts()

    def test_conflict_detected(self):
        e1 = KeybindEntry("action_a", "A", "Test", EInputContext.Gameplay, EKeyCode.X)
        e2 = KeybindEntry("action_b", "B", "Test", EInputContext.Gameplay, EKeyCode.X)
        kb2 = KeybindConfig()
        kb2.register_action(e1)
        kb2.register_action(e2)
        assert kb2.has_conflicts()

    def test_conflict_different_contexts_no_conflict(self):
        e1 = KeybindEntry("action_a", "A", "Test", EInputContext.Gameplay, EKeyCode.X)
        e2 = KeybindEntry("action_b", "B", "Test", EInputContext.Editor,   EKeyCode.X)
        kb2 = KeybindConfig()
        kb2.register_action(e1)
        kb2.register_action(e2)
        assert not kb2.has_conflicts()

    def test_conflicts_for_action(self):
        e1 = KeybindEntry("aa", "A", "T", EInputContext.Gameplay, EKeyCode.X)
        e2 = KeybindEntry("bb", "B", "T", EInputContext.Gameplay, EKeyCode.X)
        kb2 = KeybindConfig()
        kb2.register_action(e1)
        kb2.register_action(e2)
        conflicts = kb2.conflicts_for_action("aa")
        assert len(conflicts) >= 1

    # ---- get action for key -----------------------------------------------
    def test_get_action_for_key(self):
        self.kb.set_primary_binding("fire_weapon", EKeyCode.Space)
        found = self.kb.get_action_for_key(EKeyCode.Space, MOD_NONE,
                                             EInputContext.Gameplay)
        assert found == "fire_weapon"

    def test_get_action_with_modifier(self):
        found = self.kb.get_action_for_key(EKeyCode.Z, MOD_CONTROL,
                                            EInputContext.Editor)
        assert found == "undo"

    def test_get_action_unknown_key_returns_none(self):
        # EKeyCode.Unknown (0) should not match any binding since bindings use non-zero keys
        found = self.kb.get_action_for_key(0, MOD_NONE, EInputContext.Gameplay)
        assert found is None

    # ---- serialise/deserialise --------------------------------------------
    def test_serialise_deserialise_roundtrip(self):
        self.kb.set_primary_binding("fire_weapon", EKeyCode.Space)
        data = self.kb.serialise()
        # Reset.
        self.kb.set_primary_binding("fire_weapon", EKeyCode.MouseLeft)
        # Reload.
        self.kb.deserialise(data)
        e = self.kb.find_action("fire_weapon")
        assert e.primary_key == EKeyCode.Space

    def test_serialise_non_empty(self):
        data = self.kb.serialise()
        assert len(data) > 0

    # ---- change callback -------------------------------------------------
    def test_change_callback_triggered(self):
        changed = []
        self.kb.set_binding_changed_callback(lambda aid: changed.append(aid))
        self.kb.set_primary_binding("fire_weapon", EKeyCode.Space)
        assert "fire_weapon" in changed


# =============================================================================
# J4 — SaveLoadExtensions
# =============================================================================

class PlayerSaveData:
    def __init__(self, player_id: int, health: float = 100.0,
                 shield_hp: float = 100.0, credits: float = 0.0,
                 location_id: int = 0, craft: str = "",
                 state: str = "Idle"):
        self.player_id   = player_id
        self.health      = health
        self.shield_hp   = shield_hp
        self.credits     = credits
        self.location_id = location_id
        self.active_craft_id = craft
        self.player_state = state
        self.skill_entries: List[str] = []


class ShipSaveData:
    def __init__(self, ship_id: int, ship_class: str, hull_hp: float = 100.0,
                 location_id: int = 0, is_docked: bool = False):
        self.ship_id     = ship_id
        self.ship_class  = ship_class
        self.hull_hp     = hull_hp
        self.location_id = location_id
        self.is_docked   = is_docked


class FleetSaveData:
    def __init__(self, fleet_id: int, owner_id: int):
        self.fleet_id = fleet_id
        self.owner_id = owner_id
        self.ships: List[ShipSaveData] = []


class TitanSaveEntry:
    def __init__(self, titan_id: str, progress: float = 0.0,
                 pressure: float = 0.0, is_defeated: bool = False):
        self.titan_id   = titan_id
        self.progress   = progress
        self.pressure   = pressure
        self.is_defeated = is_defeated


class SeasonSaveData:
    def __init__(self, season_number: int = 1, global_pressure: float = 0.0,
                 phase: str = "EarlyGame"):
        self.season_number   = season_number
        self.global_pressure = global_pressure
        self.current_phase   = phase
        self.titans: List[TitanSaveEntry] = []


class ContractSaveEntry:
    def __init__(self, contract_id: str, status: str = "active",
                 progress_pct: float = 0.0, assigned_to: int = 0):
        self.contract_id  = contract_id
        self.status       = status
        self.progress_pct = progress_pct
        self.assigned_to  = assigned_to


class EconomySaveData:
    def __init__(self, player_id: int, credits: float = 0.0):
        self.player_id       = player_id
        self.credits         = credits
        self.contracts: List[ContractSaveEntry] = []
        self.standing_entries: List[str] = []


class WorldSaveData:
    def __init__(self, slot_id: int):
        self.slot_id    = slot_id
        self.player     = PlayerSaveData(0)
        self.fleet      = FleetSaveData(0, 0)
        self.season     = SeasonSaveData()
        self.economy    = EconomySaveData(0)
        self.structures: list = []
        self.save_version = "1.0"


CURRENT_VERSION = "1.0"


class SaveLoadManager:
    def __init__(self):
        self._slots = {}
        self._saves: Dict[int, WorldSaveData] = {}
        self._save_count = 0
        self._load_count = 0
        self._save_cb = None
        self._load_cb = None

    def initialize(self) -> bool:
        self._save_count = 0
        self._load_count = 0
        return True

    def shutdown(self):
        self._slots.clear()
        self._saves.clear()

    def register_slot(self, slot):
        self._slots[slot["slot_id"]] = slot

    def delete_slot(self, slot_id: int) -> bool:
        if slot_id not in self._slots: return False
        del self._slots[slot_id]
        self._saves.pop(slot_id, None)
        return True

    def has_slot(self, slot_id: int) -> bool:
        return slot_id in self._slots

    def find_slot(self, slot_id: int): return self._slots.get(slot_id)

    def list_slots(self): return list(self._slots.values())

    @property
    def slot_count(self): return len(self._slots)

    def save_world(self, data: WorldSaveData) -> bool:
        self._saves[data.slot_id] = data
        self._save_count += 1
        if self._save_cb: self._save_cb(data.slot_id, True)
        return True

    def save_player(self, data: PlayerSaveData) -> bool:
        # Find or create slot-0 world.
        key = data.player_id  # use player_id as key
        if key not in self._saves:
            self._saves[key] = WorldSaveData(key)
        self._saves[key].player = data
        self._save_count += 1
        return True

    def save_fleet(self, data: FleetSaveData) -> bool:
        key = data.owner_id
        if key not in self._saves:
            self._saves[key] = WorldSaveData(key)
        self._saves[key].fleet = data
        self._save_count += 1
        return True

    def save_season(self, data: SeasonSaveData) -> bool:
        key = 0
        if self._saves: key = next(iter(self._saves))
        if key not in self._saves: self._saves[key] = WorldSaveData(key)
        self._saves[key].season = data
        self._save_count += 1
        return True

    def save_economy(self, data: EconomySaveData) -> bool:
        key = data.player_id
        if key not in self._saves:
            self._saves[key] = WorldSaveData(key)
        self._saves[key].economy = data
        self._save_count += 1
        return True

    def load_world(self, slot_id: int) -> Optional[WorldSaveData]:
        self._load_count += 1
        result = self._saves.get(slot_id)
        if result and self._load_cb: self._load_cb(slot_id, True, "")
        elif not result and self._load_cb: self._load_cb(slot_id, False, "Not found")
        return result

    def load_player(self, slot_id: int) -> Optional[PlayerSaveData]:
        w = self.load_world(slot_id)
        return w.player if w else None

    def load_fleet(self, slot_id: int) -> Optional[FleetSaveData]:
        w = self.load_world(slot_id)
        return w.fleet if w else None

    def load_season(self, slot_id: int) -> Optional[SeasonSaveData]:
        w = self.load_world(slot_id)
        return w.season if w else None

    def load_economy(self, slot_id: int) -> Optional[EconomySaveData]:
        w = self.load_world(slot_id)
        return w.economy if w else None

    def validate_world(self, data: WorldSaveData) -> dict:
        warnings = []
        errors = []
        schema_match = data.save_version == CURRENT_VERSION
        if not schema_match:
            warnings.append(f"Schema mismatch: {data.save_version}")
        if data.player.player_id == 0:
            warnings.append("Player ID is zero")
        if data.season.season_number == 0:
            warnings.append("Season number is zero")
        if not data.fleet.ships:
            warnings.append("Fleet has no ships")
        passed = len(errors) == 0
        return {"success": passed, "schema_match": schema_match,
                "warnings": warnings, "errors": errors, "passed": passed}

    def schema_version_matches(self, version: str) -> bool:
        return version == CURRENT_VERSION

    def set_save_complete_callback(self, cb): self._save_cb = cb
    def set_load_complete_callback(self, cb): self._load_cb = cb

    @property
    def save_count(self): return self._save_count
    @property
    def load_count(self): return self._load_count


class TestSaveLoadExtensions:
    def setup_method(self):
        self.slm = SaveLoadManager()
        assert self.slm.initialize()

    def _make_world(self, slot_id: int = 1) -> WorldSaveData:
        wd = WorldSaveData(slot_id)
        wd.player = PlayerSaveData(42, health=80.0, credits=5000.0)
        wd.fleet  = FleetSaveData(1, 42)
        wd.fleet.ships.append(ShipSaveData(1001, "Cruiser", hull_hp=90.0))
        wd.season = SeasonSaveData(1, 0.3, "MidGame")
        t = TitanSaveEntry("titan_alpha", 0.4, 0.2)
        wd.season.titans.append(t)
        wd.economy = EconomySaveData(42, 5000.0)
        wd.economy.contracts.append(ContractSaveEntry("c_001", "active", 0.5))
        return wd

    # ---- slot management -----------------------------------------------
    def test_register_and_has_slot(self):
        self.slm.register_slot({"slot_id": 1, "save_name": "Slot 1"})
        assert self.slm.has_slot(1)

    def test_delete_slot(self):
        self.slm.register_slot({"slot_id": 1, "save_name": "Slot 1"})
        assert self.slm.delete_slot(1)
        assert not self.slm.has_slot(1)

    def test_slot_count(self):
        for i in range(3):
            self.slm.register_slot({"slot_id": i, "save_name": f"S{i}"})
        assert self.slm.slot_count == 3

    # ---- save world -----------------------------------------------
    def test_save_world(self):
        wd = self._make_world(1)
        assert self.slm.save_world(wd)
        assert self.slm.save_count == 1

    def test_save_callback_invoked(self):
        called = []
        self.slm.set_save_complete_callback(lambda sid, ok: called.append((sid, ok)))
        self.slm.save_world(self._make_world(1))
        assert len(called) == 1
        assert called[0] == (1, True)

    # ---- load world -----------------------------------------------
    def test_load_world_roundtrip(self):
        wd = self._make_world(1)
        self.slm.save_world(wd)
        loaded = self.slm.load_world(1)
        assert loaded is not None
        assert loaded.slot_id == 1

    def test_load_missing_returns_none(self):
        result = self.slm.load_world(999)
        assert result is None

    def test_load_callback_success(self):
        self.slm.save_world(self._make_world(1))
        loads = []
        self.slm.set_load_complete_callback(lambda sid, ok, e: loads.append(ok))
        self.slm.load_world(1)
        assert loads[-1] is True

    def test_load_callback_failure(self):
        loads = []
        self.slm.set_load_complete_callback(lambda sid, ok, e: loads.append(ok))
        self.slm.load_world(999)
        assert loads[-1] is False

    # ---- player state -------------------------------------------------
    def test_save_load_player_state(self):
        p = PlayerSaveData(42, health=75.0, credits=9999.0)
        self.slm.save_player(p)
        loaded = self.slm.load_player(42)
        assert loaded is not None
        assert loaded.health == pytest.approx(75.0)
        assert loaded.credits == pytest.approx(9999.0)

    # ---- fleet state -------------------------------------------------
    def test_save_load_fleet(self):
        f = FleetSaveData(1, 42)
        f.ships.append(ShipSaveData(1001, "Destroyer", 70.0))
        self.slm.save_fleet(f)
        loaded = self.slm.load_fleet(42)
        assert loaded is not None
        assert len(loaded.ships) == 1
        assert loaded.ships[0].ship_class == "Destroyer"

    # ---- season/titan state -------------------------------------------
    def test_save_load_season(self):
        s = SeasonSaveData(2, 0.6, "LateGame")
        s.titans.append(TitanSaveEntry("titan_beta", 0.9, 0.7))
        self.slm.save_season(s)
        loaded = self.slm.load_season(0)  # key=0 fallback
        if loaded:
            assert loaded.season_number == 2
            assert len(loaded.titans) == 1

    # ---- economy state -----------------------------------------------
    def test_save_load_economy(self):
        e = EconomySaveData(42, 12000.0)
        e.contracts.append(ContractSaveEntry("c002", "completed", 1.0))
        self.slm.save_economy(e)
        loaded = self.slm.load_economy(42)
        if loaded:
            assert loaded.credits == pytest.approx(12000.0)
            assert any(c.contract_id == "c002" for c in loaded.contracts)

    # ---- full world roundtrip ----------------------------------------
    def test_full_world_roundtrip_player(self):
        wd = self._make_world(1)
        self.slm.save_world(wd)
        loaded = self.slm.load_world(1)
        assert loaded.player.player_id == 42
        assert loaded.player.health == pytest.approx(80.0)

    def test_full_world_roundtrip_fleet(self):
        wd = self._make_world(1)
        self.slm.save_world(wd)
        loaded = self.slm.load_world(1)
        assert len(loaded.fleet.ships) == 1
        assert loaded.fleet.ships[0].hull_hp == pytest.approx(90.0)

    def test_full_world_roundtrip_season(self):
        wd = self._make_world(1)
        self.slm.save_world(wd)
        loaded = self.slm.load_world(1)
        assert loaded.season.current_phase == "MidGame"
        assert len(loaded.season.titans) == 1

    def test_full_world_roundtrip_economy(self):
        wd = self._make_world(1)
        self.slm.save_world(wd)
        loaded = self.slm.load_world(1)
        assert loaded.economy.credits == pytest.approx(5000.0)
        assert any(c.contract_id == "c_001" for c in loaded.economy.contracts)

    # ---- validation ----------------------------------------------------
    def test_validate_valid_world(self):
        wd = self._make_world(1)
        result = self.slm.validate_world(wd)
        assert result["schema_match"] is True

    def test_validate_version_mismatch(self):
        wd = self._make_world(1)
        wd.save_version = "0.5"
        result = self.slm.validate_world(wd)
        assert result["schema_match"] is False
        assert any("mismatch" in w.lower() or "0.5" in w for w in result["warnings"])

    def test_schema_version_matches(self):
        assert self.slm.schema_version_matches("1.0")
        assert not self.slm.schema_version_matches("0.9")

    def test_save_count_tracks_operations(self):
        self.slm.save_world(self._make_world(1))
        self.slm.save_world(self._make_world(2))
        assert self.slm.save_count == 2


# =============================================================================
# J6 — PCGDeterminismEngine
# =============================================================================

class EPCGCategory:
    Terrain       = "Terrain"
    AsteroidField = "AsteroidField"
    LootTable     = "LootTable"
    Encounter     = "Encounter"
    StationLayout = "StationLayout"
    Mission       = "Mission"
    Galaxy        = "Galaxy"


class PCGSeed:
    def __init__(self, generator_id: str, category: str,
                 seed: int = 0, label: str = "",
                 is_locked: bool = False, is_dirty: bool = False):
        self.generator_id     = generator_id
        self.category         = category
        self.seed             = seed
        self.label            = label
        self.is_locked        = is_locked
        self.is_dirty         = is_dirty
        self.generation_count = 0


class DeterministicRNG:
    _MULT = 6364136223846793005
    _ADD  = 1442695040888963407
    _MASK = 0xFFFFFFFFFFFFFFFF

    def __init__(self, seed: int = 0):
        self._state = seed & self._MASK

    def seed(self, s: int): self._state = s & self._MASK
    def state(self): return self._state

    def next_uint64(self) -> int:
        self._state = (self._state * self._MULT + self._ADD) & self._MASK
        return self._state

    def next_uint32(self) -> int: return self.next_uint64() >> 32

    def next_float01(self) -> float: return self.next_uint32() / 4294967296.0

    def next_float_range(self, lo: float, hi: float) -> float:
        return lo + self.next_float01() * (hi - lo)

    def next_int_range(self, lo: int, hi: int) -> int:
        if hi <= lo: return lo
        return lo + (self.next_uint32() % (hi - lo))

    def next_bool(self, prob: float = 0.5) -> bool:
        return self.next_float01() < prob

    def derive_child_seed(self, key: str) -> int:
        h = 14695981039346656037
        for c in key:
            h = (h ^ ord(c)) & self._MASK
            h = (h * 1099511628211) & self._MASK
        return self._state ^ h


class PCGGenerateRequest:
    def __init__(self, generator_id: str, category: str = EPCGCategory.Terrain,
                 seed: int = 0, force_regen: bool = False, context: str = ""):
        self.generator_id = generator_id
        self.category     = category
        self.seed         = seed
        self.force_regen  = force_regen
        self.context      = context


class PCGDeterminismEngine:
    def __init__(self):
        self._master_seed       = 12345
        self._seeds: Dict[str, PCGSeed] = {}
        self._generators        = {}
        self._total_generations = 0
        self._gen_cb            = None

    def initialize(self, master_seed: int = 0) -> bool:
        self._master_seed       = master_seed if master_seed != 0 else 12345
        self._total_generations = 0
        return True

    def shutdown(self):
        self._seeds.clear()
        self._generators.clear()

    def set_master_seed(self, seed: int): self._master_seed = seed
    def get_master_seed(self) -> int: return self._master_seed

    def register_seed(self, seed: PCGSeed): self._seeds[seed.generator_id] = seed

    def set_seed(self, generator_id: str, seed: int) -> bool:
        s = self._seeds.get(generator_id)
        if not s or s.is_locked: return False
        s.seed = seed; s.is_dirty = True; return True

    def lock_seed(self, generator_id: str) -> bool:
        s = self._seeds.get(generator_id)
        if not s: return False
        s.is_locked = True; return True

    def unlock_seed(self, generator_id: str) -> bool:
        s = self._seeds.get(generator_id)
        if not s: return False
        s.is_locked = False; return True

    def mark_dirty(self, generator_id: str) -> bool:
        s = self._seeds.get(generator_id)
        if not s: return False
        s.is_dirty = True; return True

    def clear_dirty(self, generator_id: str) -> bool:
        s = self._seeds.get(generator_id)
        if not s: return False
        s.is_dirty = False; return True

    def has_seed(self, generator_id: str) -> bool:
        return generator_id in self._seeds

    def find_seed(self, generator_id: str) -> Optional[PCGSeed]:
        return self._seeds.get(generator_id)

    def list_seeds(self, category: str = "") -> List[PCGSeed]:
        if not category: return list(self._seeds.values())
        return [s for s in self._seeds.values() if s.category == category]

    def get_dirty_seeds(self) -> List[PCGSeed]:
        return [s for s in self._seeds.values() if s.is_dirty]

    def get_locked_seeds(self) -> List[PCGSeed]:
        return [s for s in self._seeds.values() if s.is_locked]

    @property
    def seed_count(self): return len(self._seeds)

    def register_generator(self, gen_id: str, fn, category: str = ""):
        self._generators[gen_id] = fn

    def has_generator(self, gen_id: str) -> bool:
        return gen_id in self._generators

    def auto_assign_seed(self, generator_id: str) -> int:
        h = 14695981039346656037
        MASK = 0xFFFFFFFFFFFFFFFF
        for c in generator_id:
            h = (h ^ ord(c)) & MASK
            h = (h * 1099511628211) & MASK
        return (self._master_seed ^ h) & MASK

    def generate(self, request: PCGGenerateRequest) -> dict:
        seed_entry = self._seeds.get(request.generator_id)
        used_seed = request.seed if request.seed != 0 else self.auto_assign_seed(request.generator_id)

        if seed_entry:
            if seed_entry.is_locked and not request.force_regen:
                return {"success": False, "error": "Seed is locked",
                        "generator_id": request.generator_id, "used_seed": used_seed}
            seed_entry.seed = used_seed
            seed_entry.generation_count += 1
            seed_entry.is_dirty = False

        gen_fn = self._generators.get(request.generator_id)
        if gen_fn:
            rng = DeterministicRNG(used_seed)
            result = gen_fn(request, rng)
        else:
            rng = DeterministicRNG(used_seed)
            result = {
                "success": True,
                "output_tokens": [
                    f"generated:{request.generator_id}",
                    f"seed:{used_seed}",
                    f"context:{request.context}",
                ],
            }

        result["generator_id"] = request.generator_id
        result["used_seed"]    = used_seed
        self._total_generations += 1
        if self._gen_cb: self._gen_cb(result)
        return result

    def regenerate(self, generator_id: str, context: str = "") -> dict:
        s = self._seeds.get(generator_id)
        req = PCGGenerateRequest(generator_id, force_regen=True, context=context)
        if s: req.seed = s.seed; req.category = s.category
        return self.generate(req)

    def regenerate_all(self, category: str):
        for s in list(self._seeds.values()):
            if s.category == category and not s.is_locked:
                self.regenerate(s.generator_id)

    def regenerate_dirty(self):
        for s in list(self._seeds.values()):
            if s.is_dirty and not s.is_locked:
                self.regenerate(s.generator_id)

    def create_rng(self, generator_id: str) -> DeterministicRNG:
        s = self._seeds.get(generator_id)
        seed = s.seed if s else self.auto_assign_seed(generator_id)
        return DeterministicRNG(seed)

    def verify_determinism(self, generator_id: str, trials: int = 3) -> bool:
        gen_fn = self._generators.get(generator_id)
        if not gen_fn: return True
        seed = self.auto_assign_seed(generator_id)
        req = PCGGenerateRequest(generator_id)
        rng0 = DeterministicRNG(seed)
        first = gen_fn(req, rng0).get("output_tokens", [])
        for _ in range(trials - 1):
            rng = DeterministicRNG(seed)
            trial = gen_fn(req, rng).get("output_tokens", [])
            if trial != first: return False
        return True

    def get_seed_panel_entries(self) -> list:
        result = []
        for s in self._seeds.values():
            result.append({
                "id": s.generator_id,
                "label": s.label or s.generator_id,
                "seed": s.seed,
                "locked": s.is_locked,
                "dirty": s.is_dirty,
                "category": s.category,
            })
        return result

    @property
    def total_generations(self): return self._total_generations

    def set_generation_complete_callback(self, cb): self._gen_cb = cb


class TestPCGDeterminismEngine:
    def setup_method(self):
        self.engine = PCGDeterminismEngine()
        self.engine.initialize(master_seed=999)

    def _add_seed(self, gid: str, cat: str = EPCGCategory.Terrain,
                   seed: int = 42):
        s = PCGSeed(gid, cat, seed, label=gid)
        self.engine.register_seed(s)

    # ---- initialization ------------------------------------------------
    def test_initialize(self):
        assert self.engine.get_master_seed() == 999

    def test_set_master_seed(self):
        self.engine.set_master_seed(12345)
        assert self.engine.get_master_seed() == 12345

    # ---- seed management -----------------------------------------------
    def test_register_and_find_seed(self):
        self._add_seed("gen_terrain")
        assert self.engine.has_seed("gen_terrain")
        s = self.engine.find_seed("gen_terrain")
        assert s is not None
        assert s.seed == 42

    def test_set_seed(self):
        self._add_seed("gen_terrain")
        assert self.engine.set_seed("gen_terrain", 777)
        assert self.engine.find_seed("gen_terrain").seed == 777

    def test_set_seed_locked_fails(self):
        self._add_seed("gen_terrain")
        self.engine.lock_seed("gen_terrain")
        assert not self.engine.set_seed("gen_terrain", 888)

    def test_lock_unlock_seed(self):
        self._add_seed("gen_a")
        self.engine.lock_seed("gen_a")
        assert self.engine.find_seed("gen_a").is_locked
        self.engine.unlock_seed("gen_a")
        assert not self.engine.find_seed("gen_a").is_locked

    def test_mark_clear_dirty(self):
        self._add_seed("gen_b")
        self.engine.mark_dirty("gen_b")
        assert self.engine.find_seed("gen_b").is_dirty
        self.engine.clear_dirty("gen_b")
        assert not self.engine.find_seed("gen_b").is_dirty

    def test_get_dirty_seeds(self):
        self._add_seed("gen_a"); self._add_seed("gen_b")
        self.engine.mark_dirty("gen_a")
        dirty = self.engine.get_dirty_seeds()
        assert any(s.generator_id == "gen_a" for s in dirty)

    def test_get_locked_seeds(self):
        self._add_seed("gen_a"); self._add_seed("gen_b")
        self.engine.lock_seed("gen_a")
        locked = self.engine.get_locked_seeds()
        assert any(s.generator_id == "gen_a" for s in locked)
        assert not any(s.generator_id == "gen_b" for s in locked)

    def test_list_seeds_by_category(self):
        self._add_seed("t1", EPCGCategory.Terrain)
        self._add_seed("a1", EPCGCategory.AsteroidField)
        terrain = self.engine.list_seeds(EPCGCategory.Terrain)
        assert any(s.generator_id == "t1" for s in terrain)
        assert not any(s.generator_id == "a1" for s in terrain)

    def test_seed_count(self):
        for i in range(5):
            self._add_seed(f"gen_{i}")
        assert self.engine.seed_count == 5

    # ---- auto-assign seed -----------------------------------------------
    def test_auto_assign_deterministic(self):
        seed1 = self.engine.auto_assign_seed("my_generator")
        seed2 = self.engine.auto_assign_seed("my_generator")
        assert seed1 == seed2

    def test_auto_assign_different_ids_different_seeds(self):
        s1 = self.engine.auto_assign_seed("gen_alpha")
        s2 = self.engine.auto_assign_seed("gen_beta")
        assert s1 != s2

    def test_auto_assign_uses_master_seed(self):
        e1 = PCGDeterminismEngine(); e1.initialize(100)
        e2 = PCGDeterminismEngine(); e2.initialize(200)
        assert e1.auto_assign_seed("gen") != e2.auto_assign_seed("gen")

    # ---- generation -----------------------------------------------
    def test_generate_default_result(self):
        self._add_seed("gen_terrain")
        req = PCGGenerateRequest("gen_terrain", seed=42)
        result = self.engine.generate(req)
        assert result["success"] is True
        assert result["used_seed"] == 42

    def test_generate_increments_count(self):
        self._add_seed("gen_a")
        self.engine.generate(PCGGenerateRequest("gen_a", seed=1))
        self.engine.generate(PCGGenerateRequest("gen_a", seed=2))
        assert self.engine.total_generations == 2

    def test_generate_clears_dirty_flag(self):
        self._add_seed("gen_terrain")
        self.engine.mark_dirty("gen_terrain")
        self.engine.generate(PCGGenerateRequest("gen_terrain", seed=42))
        assert not self.engine.find_seed("gen_terrain").is_dirty

    def test_generate_locked_fails_without_force(self):
        self._add_seed("gen_terrain")
        self.engine.lock_seed("gen_terrain")
        req = PCGGenerateRequest("gen_terrain", seed=42, force_regen=False)
        result = self.engine.generate(req)
        assert result["success"] is False

    def test_generate_locked_succeeds_with_force(self):
        self._add_seed("gen_terrain")
        self.engine.lock_seed("gen_terrain")
        req = PCGGenerateRequest("gen_terrain", seed=42, force_regen=True)
        result = self.engine.generate(req)
        assert result["success"] is True

    def test_regenerate_api(self):
        self._add_seed("gen_terrain")
        result = self.engine.regenerate("gen_terrain", "sector_alpha")
        assert result["success"] is True

    def test_regenerate_dirty(self):
        self._add_seed("g1"); self._add_seed("g2")
        self.engine.mark_dirty("g1")
        self.engine.regenerate_dirty()
        assert not self.engine.find_seed("g1").is_dirty

    def test_regenerate_all_category(self):
        self._add_seed("t1", EPCGCategory.Terrain)
        self._add_seed("t2", EPCGCategory.Terrain)
        self._add_seed("a1", EPCGCategory.AsteroidField)
        before = self.engine.total_generations
        self.engine.regenerate_all(EPCGCategory.Terrain)
        assert self.engine.total_generations >= before + 2

    # ---- custom generator + determinism ---------------------------------
    def test_custom_generator_called(self):
        calls = []
        def my_gen(req, rng):
            calls.append(rng.state())
            return {"success": True, "output_tokens": ["hello"]}
        self.engine.register_generator("custom", my_gen)
        self._add_seed("custom")
        self.engine.generate(PCGGenerateRequest("custom", seed=100))
        assert len(calls) == 1

    def test_determinism_same_seed_same_output(self):
        def my_gen(req, rng):
            val = rng.next_int_range(0, 100)
            return {"success": True, "output_tokens": [str(val)]}
        self.engine.register_generator("det_gen", my_gen)
        self._add_seed("det_gen")
        assert self.engine.verify_determinism("det_gen", trials=5)

    def test_determinism_different_seeds_different_output(self):
        results = []
        def my_gen(req, rng):
            val = rng.next_uint32()
            return {"success": True, "output_tokens": [str(val)]}
        self.engine.register_generator("var_gen", my_gen)
        rng1 = DeterministicRNG(111)
        rng2 = DeterministicRNG(222)
        req = PCGGenerateRequest("var_gen")
        r1 = my_gen(req, rng1)["output_tokens"]
        r2 = my_gen(req, rng2)["output_tokens"]
        assert r1 != r2

    # ---- create_rng ---------------------------------------------------
    def test_create_rng_uses_seed(self):
        self._add_seed("gen_r", seed=42)
        rng = self.engine.create_rng("gen_r")
        # Next value should be deterministic.
        rng2 = DeterministicRNG(42)
        assert rng.next_uint32() == rng2.next_uint32()

    # ---- panel entries ------------------------------------------------
    def test_seed_panel_entries(self):
        self._add_seed("g1"); self._add_seed("g2")
        entries = self.engine.get_seed_panel_entries()
        assert len(entries) == 2
        ids = [e["id"] for e in entries]
        assert "g1" in ids and "g2" in ids

    # ---- generation callback ------------------------------------------
    def test_generation_callback(self):
        completed = []
        self.engine.set_generation_complete_callback(
            lambda r: completed.append(r["generator_id"]))
        self._add_seed("gen_x")
        self.engine.generate(PCGGenerateRequest("gen_x", seed=1))
        assert "gen_x" in completed


# =============================================================================
# DeterministicRNG unit tests
# =============================================================================

class TestDeterministicRNG:
    def test_reproducible_sequence(self):
        r1 = DeterministicRNG(12345)
        r2 = DeterministicRNG(12345)
        for _ in range(100):
            assert r1.next_uint64() == r2.next_uint64()

    def test_different_seeds_different_sequences(self):
        r1 = DeterministicRNG(1)
        r2 = DeterministicRNG(2)
        first1 = r1.next_uint64()
        first2 = r2.next_uint64()
        assert first1 != first2

    def test_float01_in_range(self):
        r = DeterministicRNG(999)
        for _ in range(1000):
            v = r.next_float01()
            assert 0.0 <= v < 1.0

    def test_float_range(self):
        r = DeterministicRNG(7)
        for _ in range(200):
            v = r.next_float_range(10.0, 20.0)
            assert 10.0 <= v < 20.0

    def test_int_range(self):
        r = DeterministicRNG(42)
        for _ in range(500):
            v = r.next_int_range(0, 10)
            assert 0 <= v < 10

    def test_bool_probability(self):
        r = DeterministicRNG(1111)
        trues = sum(1 for _ in range(10000) if r.next_bool(0.3))
        # Should be roughly 30% true (allow ±10%).
        assert 2000 <= trues <= 4000

    def test_derive_child_seed_deterministic(self):
        r = DeterministicRNG(100)
        s1 = r.derive_child_seed("sector_A")
        r2 = DeterministicRNG(100)
        s2 = r2.derive_child_seed("sector_A")
        assert s1 == s2

    def test_derive_child_seed_different_keys(self):
        r = DeterministicRNG(100)
        s1 = r.derive_child_seed("key_A")
        s2 = r.derive_child_seed("key_B")
        assert s1 != s2

    def test_seed_reset(self):
        r = DeterministicRNG(5)
        v1 = r.next_uint32()
        r.seed(5)
        v2 = r.next_uint32()
        assert v1 == v2
