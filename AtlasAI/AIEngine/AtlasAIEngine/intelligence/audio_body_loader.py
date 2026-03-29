"""AtlasAI Phase 27D — Audio Body Loader.

Discovers and manages audio body manifests, mirroring the C++
AudioBodyRegistry for cross-language spatial audio scene setup.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class AttenuationCurveDef:
    """Describes how a sound attenuates over distance."""

    model: str = "InverseDistance"
    min_distance: float = 1.0
    max_distance: float = 50.0
    rolloff_factor: float = 1.0
    reference_distance: float = 1.0
    use_custom_curve: bool = False

    @property
    def distance_range(self) -> float:
        return self.max_distance - self.min_distance

    @property
    def is_attenuated(self) -> bool:
        return self.model != "None"


@dataclass
class ReverbZoneDef:
    """A spatial reverb zone definition."""

    zone_id: str
    name: str
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    radius: float = 10.0
    min_distance: float = 8.0
    decay_time: float = 1.49
    preset_name: str = "Generic"
    enabled: bool = True

    @property
    def position(self) -> tuple[float, float, float]:
        return (self.pos_x, self.pos_y, self.pos_z)

    def contains_point(self, px: float, py: float, pz: float) -> bool:
        dx = px - self.pos_x
        dy = py - self.pos_y
        dz = pz - self.pos_z
        return (dx * dx + dy * dy + dz * dz) <= self.radius * self.radius


@dataclass
class AudioBodyManifest:
    """Parsed audio body manifest for a single spatial audio source."""

    body_id: str
    name: str
    source_type: str = "Point"
    body_state: str = "Inactive"
    audio_layer: str = "SFX"
    attenuation: AttenuationCurveDef = field(
        default_factory=AttenuationCurveDef
    )
    volume_db: float = 0.0
    pitch_semitones: float = 0.0
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    loop: bool = False
    play_on_activate: bool = False
    spatialize: bool = True
    audio_clip_id: str = ""
    linked_entity_id: str = ""
    scene_id: str = ""
    priority: int = 128
    always_play: bool = False
    manifest_path: str = ""

    @property
    def position(self) -> tuple[float, float, float]:
        return (self.pos_x, self.pos_y, self.pos_z)

    @property
    def is_active(self) -> bool:
        return self.body_state in ("Active", "Playing")

    @property
    def is_playing(self) -> bool:
        return self.body_state == "Playing"

    @property
    def is_spatialized(self) -> bool:
        return self.spatialize


class AudioBodyLoader:
    """Discovers and manages audio body manifests for spatial audio scene setup."""

    def __init__(self) -> None:
        self._bodies: dict[str, AudioBodyManifest] = {}
        self._reverb_zones: dict[str, ReverbZoneDef] = {}
        self._active: set[str] = set()
        self._playing: set[str] = set()
        self._next_zone: int = 0

    # ------------------------------------------------------------------
    # Body registration
    # ------------------------------------------------------------------

    def register(
        self,
        body_id: str,
        name: str,
        source_type: str = "Point",
        scene_id: str = "",
        audio_layer: str = "SFX",
        priority: int = 128,
        always_play: bool = False,
    ) -> AudioBodyManifest:
        manifest = AudioBodyManifest(
            body_id=body_id,
            name=name,
            source_type=source_type,
            scene_id=scene_id,
            audio_layer=audio_layer,
            priority=priority,
            always_play=always_play,
        )
        self._bodies[body_id] = manifest
        logger.debug("Registered audio body %s", body_id)
        return manifest

    def register_from_dict(self, data: dict) -> Optional[AudioBodyManifest]:
        try:
            body_id = data["body_id"]
            name = data["name"]
            manifest = self.register(
                body_id=body_id,
                name=name,
                source_type=data.get("source_type", "Point"),
                scene_id=data.get("scene_id", ""),
                audio_layer=data.get("audio_layer", "SFX"),
                priority=data.get("priority", 128),
                always_play=data.get("always_play", False),
            )
            manifest.volume_db = data.get("volume_db", 0.0)
            manifest.pitch_semitones = data.get("pitch_semitones", 0.0)
            manifest.loop = data.get("loop", False)
            manifest.play_on_activate = data.get("play_on_activate", False)
            manifest.spatialize = data.get("spatialize", True)
            manifest.audio_clip_id = data.get("audio_clip_id", "")
            manifest.linked_entity_id = data.get("linked_entity_id", "")
            manifest.pos_x = data.get("pos_x", 0.0)
            manifest.pos_y = data.get("pos_y", 0.0)
            manifest.pos_z = data.get("pos_z", 0.0)
            att = data.get("attenuation", {})
            if att:
                manifest.attenuation = AttenuationCurveDef(
                    model=att.get("model", "InverseDistance"),
                    min_distance=att.get("min_distance", 1.0),
                    max_distance=att.get("max_distance", 50.0),
                )
            return manifest
        except (KeyError, TypeError) as exc:
            logger.error("register_from_dict failed: %s", exc)
            return None

    def unregister(self, body_id: str) -> bool:
        if body_id not in self._bodies:
            return False
        del self._bodies[body_id]
        self._active.discard(body_id)
        self._playing.discard(body_id)
        return True

    def get_manifest(self, body_id: str) -> Optional[AudioBodyManifest]:
        return self._bodies.get(body_id)

    def get_registered_count(self) -> int:
        return len(self._bodies)

    def get_all_body_ids(self) -> list[str]:
        return list(self._bodies.keys())

    def get_bodies_by_scene(self, scene_id: str) -> list[str]:
        return [bid for bid, m in self._bodies.items() if m.scene_id == scene_id]

    def get_bodies_by_layer(self, audio_layer: str) -> list[str]:
        return [bid for bid, m in self._bodies.items() if m.audio_layer == audio_layer]

    def get_bodies_by_type(self, source_type: str) -> list[str]:
        return [bid for bid, m in self._bodies.items() if m.source_type == source_type]

    # ------------------------------------------------------------------
    # Activation and playback
    # ------------------------------------------------------------------

    def activate(self, body_id: str) -> bool:
        if body_id not in self._bodies:
            logger.warning("Cannot activate unknown body %s", body_id)
            return False
        self._active.add(body_id)
        m = self._bodies[body_id]
        m.body_state = "Active"
        return True

    def deactivate(self, body_id: str) -> bool:
        if body_id not in self._active:
            return False
        self._active.discard(body_id)
        self._playing.discard(body_id)
        m = self._bodies.get(body_id)
        if m:
            m.body_state = "Inactive"
        return True

    def play(self, body_id: str) -> bool:
        if body_id not in self._bodies:
            return False
        self.activate(body_id)
        self._playing.add(body_id)
        m = self._bodies[body_id]
        m.body_state = "Playing"
        return True

    def pause(self, body_id: str) -> bool:
        if body_id not in self._playing:
            return False
        self._playing.discard(body_id)
        m = self._bodies.get(body_id)
        if m:
            m.body_state = "Paused"
        return True

    def stop(self, body_id: str) -> bool:
        if body_id not in self._active and body_id not in self._playing:
            return False
        self._playing.discard(body_id)
        m = self._bodies.get(body_id)
        if m:
            m.body_state = "Stopped"
        return True

    def is_active(self, body_id: str) -> bool:
        return body_id in self._active

    def is_playing(self, body_id: str) -> bool:
        return body_id in self._playing

    def get_active_count(self) -> int:
        return len(self._active)

    def get_playing_count(self) -> int:
        return len(self._playing)

    def get_active_ids(self) -> list[str]:
        return list(self._active)

    def get_playing_ids(self) -> list[str]:
        return list(self._playing)

    def activate_all_in_scene(self, scene_id: str) -> int:
        activated = 0
        for body_id, m in self._bodies.items():
            if m.scene_id == scene_id and body_id not in self._active:
                self.activate(body_id)
                activated += 1
        return activated

    def deactivate_all_in_scene(self, scene_id: str) -> int:
        ids = self.get_bodies_by_scene(scene_id)
        deactivated = 0
        for body_id in ids:
            if self.deactivate(body_id):
                deactivated += 1
        return deactivated

    def activate_always_play(self) -> int:
        activated = 0
        for body_id, m in self._bodies.items():
            if m.always_play and body_id not in self._active:
                self.activate(body_id)
                activated += 1
        return activated

    def play_on_activate_all(self) -> int:
        played = 0
        for body_id in list(self._active):
            m = self._bodies.get(body_id)
            if m and m.play_on_activate:
                self.play(body_id)
                played += 1
        return played

    # ------------------------------------------------------------------
    # Reverb zones
    # ------------------------------------------------------------------

    def register_reverb_zone(
        self,
        name: str,
        pos_x: float = 0.0,
        pos_y: float = 0.0,
        pos_z: float = 0.0,
        radius: float = 10.0,
        preset_name: str = "Generic",
    ) -> ReverbZoneDef:
        zone_id = f"zone_{self._next_zone:04d}"
        self._next_zone += 1
        zone = ReverbZoneDef(
            zone_id=zone_id,
            name=name,
            pos_x=pos_x,
            pos_y=pos_y,
            pos_z=pos_z,
            radius=radius,
            preset_name=preset_name,
        )
        self._reverb_zones[zone_id] = zone
        return zone

    def unregister_reverb_zone(self, zone_id: str) -> bool:
        if zone_id not in self._reverb_zones:
            return False
        del self._reverb_zones[zone_id]
        return True

    def get_reverb_zone(self, zone_id: str) -> Optional[ReverbZoneDef]:
        return self._reverb_zones.get(zone_id)

    def get_reverb_zone_count(self) -> int:
        return len(self._reverb_zones)

    def get_all_zone_ids(self) -> list[str]:
        return list(self._reverb_zones.keys())

    def get_zones_containing_point(
        self, px: float, py: float, pz: float
    ) -> list[str]:
        return [
            zid for zid, z in self._reverb_zones.items()
            if z.enabled and z.contains_point(px, py, pz)
        ]

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_registry(self, output_path: str) -> bool:
        data = {
            "bodies": [
                {
                    "body_id": m.body_id,
                    "name": m.name,
                    "source_type": m.source_type,
                    "scene_id": m.scene_id,
                    "audio_layer": m.audio_layer,
                    "priority": m.priority,
                    "always_play": m.always_play,
                    "volume_db": m.volume_db,
                    "loop": m.loop,
                    "spatialize": m.spatialize,
                    "audio_clip_id": m.audio_clip_id,
                    "attenuation": {
                        "model": m.attenuation.model,
                        "min_distance": m.attenuation.min_distance,
                        "max_distance": m.attenuation.max_distance,
                    },
                }
                for m in self._bodies.values()
            ],
            "reverb_zones": [
                {
                    "zone_id": z.zone_id,
                    "name": z.name,
                    "pos_x": z.pos_x,
                    "pos_y": z.pos_y,
                    "pos_z": z.pos_z,
                    "radius": z.radius,
                    "preset_name": z.preset_name,
                    "enabled": z.enabled,
                }
                for z in self._reverb_zones.values()
            ],
        }
        try:
            Path(output_path).write_text(json.dumps(data, indent=2))
            return True
        except OSError as exc:
            logger.error("Failed to save audio registry: %s", exc)
            return False

    def load_registry(self, input_path: str) -> int:
        try:
            data = json.loads(Path(input_path).read_text())
            loaded = 0
            for entry in data.get("bodies", []):
                if self.register_from_dict(entry) is not None:
                    loaded += 1
            for zd in data.get("reverb_zones", []):
                try:
                    zone = ReverbZoneDef(
                        zone_id=zd["zone_id"],
                        name=zd["name"],
                        pos_x=zd.get("pos_x", 0.0),
                        pos_y=zd.get("pos_y", 0.0),
                        pos_z=zd.get("pos_z", 0.0),
                        radius=zd.get("radius", 10.0),
                        preset_name=zd.get("preset_name", "Generic"),
                        enabled=zd.get("enabled", True),
                    )
                    self._reverb_zones[zone.zone_id] = zone
                except (KeyError, TypeError):
                    pass
            return loaded
        except (OSError, json.JSONDecodeError) as exc:
            logger.error("Failed to load audio registry: %s", exc)
            return 0

    def clear(self) -> None:
        self._bodies.clear()
        self._reverb_zones.clear()
        self._active.clear()
        self._playing.clear()
        self._next_zone = 0
