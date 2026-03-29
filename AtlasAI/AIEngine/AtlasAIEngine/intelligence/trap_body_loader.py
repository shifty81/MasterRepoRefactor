"""AtlasAI Phase 43D — Trap Body Loader.

Discovers and manages trap body manifests, mirroring the C++
TrapBodyRegistry for cross-language trap management.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class TrapEffectManifest:
    effect_id: str
    effect_name: str
    trap_type: str = "Spike"
    damage_amount: float = 10.0
    effect_radius: float = 2.0
    effect_duration: float = 0.5
    particle_effect_id: str = ""
    sound_cue_id: str = ""
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_fire(self) -> bool:
        return self.trap_type == "Fire"

    @property
    def is_poison(self) -> bool:
        return self.trap_type == "Poison"

    @property
    def is_electric(self) -> bool:
        return self.trap_type == "Electric"

    @property
    def is_explosive(self) -> bool:
        return self.trap_type == "Explosive"

    @property
    def is_void(self) -> bool:
        return self.trap_type == "Void"

    @property
    def is_spike(self) -> bool:
        return self.trap_type == "Spike"

    @property
    def is_ice(self) -> bool:
        return self.trap_type == "Ice"

    @property
    def is_high_damage(self) -> bool:
        return self.damage_amount >= 50.0

    @property
    def is_aoe(self) -> bool:
        return self.effect_radius > 1.0

    @property
    def has_particle(self) -> bool:
        return bool(self.particle_effect_id)

    @property
    def has_sound(self) -> bool:
        return bool(self.sound_cue_id)

    @property
    def is_long_duration(self) -> bool:
        return self.effect_duration > 2.0


@dataclass
class TrapTriggerZoneManifest:
    trigger_zone_id: str
    trap_body_id: str
    condition: str = "OnEnter"
    zone_radius: float = 1.5
    zone_height: float = 2.0
    player_only: bool = False
    npc_trigger: bool = True
    repeat_trigger: bool = False
    enabled: bool = True

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_on_enter(self) -> bool:
        return self.condition == "OnEnter"

    @property
    def is_on_exit(self) -> bool:
        return self.condition == "OnExit"

    @property
    def is_on_stay(self) -> bool:
        return self.condition == "OnStay"

    @property
    def is_on_timer(self) -> bool:
        return self.condition == "OnTimer"

    @property
    def is_player_only(self) -> bool:
        return self.player_only

    @property
    def triggers_npcs(self) -> bool:
        return self.npc_trigger

    @property
    def is_repeatable(self) -> bool:
        return self.repeat_trigger

    @property
    def is_large_zone(self) -> bool:
        return self.zone_radius > 5.0


@dataclass
class TrapBodyManifest:
    trap_body_id: str
    owner_entity_id: str
    zone_id: str = ""
    state: str = "Idle"
    arming_method: str = "Automatic"
    trap_type: str = "Spike"
    arming_delay_ms: float = 0.0
    cooldown_ms: float = 5000.0
    max_triggers: int = -1
    trigger_count: int = 0
    luck_modifier: float = 1.0
    enabled: bool = True
    effect_chain_ids: list = field(default_factory=list)

    @property
    def is_idle(self) -> bool:
        return self.state == "Idle"

    @property
    def is_armed(self) -> bool:
        return self.state == "Armed"

    @property
    def is_triggered(self) -> bool:
        return self.state == "Triggered"

    @property
    def is_cooldown(self) -> bool:
        return self.state == "Cooldown"

    @property
    def is_depleted(self) -> bool:
        return self.state == "Depleted"

    @property
    def is_disabled(self) -> bool:
        return self.state == "Disabled"

    @property
    def is_unlimited(self) -> bool:
        return self.max_triggers == -1

    @property
    def is_auto_armed(self) -> bool:
        return self.arming_method == "Automatic"

    @property
    def has_delay(self) -> bool:
        return self.arming_delay_ms > 0.0

    @property
    def has_long_cooldown(self) -> bool:
        return self.cooldown_ms > 10000.0

    @property
    def effect_count(self) -> int:
        return len(self.effect_chain_ids)

    @property
    def has_effects(self) -> bool:
        return len(self.effect_chain_ids) > 0

    @property
    def is_lucky(self) -> bool:
        return self.luck_modifier > 1.0

    @property
    def has_zone(self) -> bool:
        return bool(self.zone_id)


class TrapBodyLoader:
    """Loader for trap body manifests."""

    def __init__(self) -> None:
        self._manifests: dict = {}

    def load_manifest(self, data: dict) -> TrapBodyManifest:
        manifest = TrapBodyManifest(
            trap_body_id=data["trap_body_id"],
            owner_entity_id=data.get("owner_entity_id", ""),
            zone_id=data.get("zone_id", ""),
            state=data.get("state", "Idle"),
            arming_method=data.get("arming_method", "Automatic"),
            trap_type=data.get("trap_type", "Spike"),
            arming_delay_ms=data.get("arming_delay_ms", 0.0),
            cooldown_ms=data.get("cooldown_ms", 5000.0),
            max_triggers=data.get("max_triggers", -1),
            trigger_count=data.get("trigger_count", 0),
            luck_modifier=data.get("luck_modifier", 1.0),
            enabled=data.get("enabled", True),
            effect_chain_ids=data.get("effect_chain_ids", []),
        )
        self._manifests[manifest.trap_body_id] = manifest
        return manifest

    def load_batch(self, data_list: list) -> list:
        return [self.load_manifest(d) for d in data_list]

    def load_from_file(self, path) -> TrapBodyManifest:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_manifest(data)

    def save_manifest(self, manifest: TrapBodyManifest, path) -> None:
        data = {
            "trap_body_id": manifest.trap_body_id,
            "owner_entity_id": manifest.owner_entity_id,
            "zone_id": manifest.zone_id,
            "state": manifest.state,
            "arming_method": manifest.arming_method,
            "trap_type": manifest.trap_type,
            "arming_delay_ms": manifest.arming_delay_ms,
            "cooldown_ms": manifest.cooldown_ms,
            "max_triggers": manifest.max_triggers,
            "trigger_count": manifest.trigger_count,
            "luck_modifier": manifest.luck_modifier,
            "enabled": manifest.enabled,
            "effect_chain_ids": manifest.effect_chain_ids,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_trap_effect(self, data: dict) -> TrapEffectManifest:
        return TrapEffectManifest(
            effect_id=data["effect_id"],
            effect_name=data.get("effect_name", ""),
            trap_type=data.get("trap_type", "Spike"),
            damage_amount=data.get("damage_amount", 10.0),
            effect_radius=data.get("effect_radius", 2.0),
            effect_duration=data.get("effect_duration", 0.5),
            particle_effect_id=data.get("particle_effect_id", ""),
            sound_cue_id=data.get("sound_cue_id", ""),
            enabled=data.get("enabled", True),
        )

    def load_trigger_zone(self, data: dict) -> TrapTriggerZoneManifest:
        return TrapTriggerZoneManifest(
            trigger_zone_id=data["trigger_zone_id"],
            trap_body_id=data.get("trap_body_id", ""),
            condition=data.get("condition", "OnEnter"),
            zone_radius=data.get("zone_radius", 1.5),
            zone_height=data.get("zone_height", 2.0),
            player_only=data.get("player_only", False),
            npc_trigger=data.get("npc_trigger", True),
            repeat_trigger=data.get("repeat_trigger", False),
            enabled=data.get("enabled", True),
        )

    def validate(self, manifest: TrapBodyManifest) -> bool:
        return bool(manifest.trap_body_id)

    @property
    def loaded_count(self) -> int:
        return len(self._manifests)

    def clear(self) -> None:
        self._manifests.clear()
