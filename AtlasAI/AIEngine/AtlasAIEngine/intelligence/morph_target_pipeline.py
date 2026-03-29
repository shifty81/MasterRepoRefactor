"""AtlasAI Phase 39B — Morph Target Pipeline.

Manages morph target entries, corrective shapes, and blend presets
for the MorphTargetEditorTool cross-language pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class MorphTargetEntry:
    """A morph target definition."""
    morph_id: str
    morph_name: str
    scope: str = "Character"
    default_weight: float = 0.0
    min_weight: float = 0.0
    max_weight: float = 1.0
    enabled: bool = True

    @property
    def is_active(self) -> bool:
        return self.default_weight > 0.0

    @property
    def is_full(self) -> bool:
        return self.default_weight >= self.max_weight

    @property
    def is_character(self) -> bool:
        return self.scope == "Character"

    @property
    def weight_range(self) -> float:
        return self.max_weight - self.min_weight


@dataclass
class CorrectiveShapeEntry:
    """A corrective shape definition linked to a morph target."""
    corrective_id: str
    morph_id: str
    mode: str = "Automatic"
    trigger_expr: str = ""
    threshold: float = 0.5
    enabled: bool = True

    @property
    def has_trigger(self) -> bool:
        return bool(self.trigger_expr)

    @property
    def is_automatic(self) -> bool:
        return self.mode == "Automatic"

    @property
    def is_active(self) -> bool:
        return self.enabled


@dataclass
class MorphBlendPresetEntry:
    """A blend preset combining multiple morph targets."""
    preset_id: str
    preset_name: str
    blend_mode: str = "Additive"
    morph_ids: list = field(default_factory=list)
    weights: list = field(default_factory=list)
    enabled: bool = True

    @property
    def is_empty(self) -> bool:
        return not bool(self.morph_ids)

    @property
    def morph_count(self) -> int:
        return len(self.morph_ids)

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_additive(self) -> bool:
        return self.blend_mode == "Additive"


class MorphTargetPipeline:
    """Pipeline managing morph targets, correctives, and blend presets."""

    def __init__(self) -> None:
        self._morphs: Dict[str, MorphTargetEntry] = {}
        self._correctives: Dict[str, Dict[str, CorrectiveShapeEntry]] = {}
        self._presets: Dict[str, MorphBlendPresetEntry] = {}

    def add_morph(self, entry: MorphTargetEntry) -> bool:
        if not entry.morph_id:
            return False
        self._morphs[entry.morph_id] = entry
        return True

    def get_morph(self, morph_id: str) -> Optional[MorphTargetEntry]:
        return self._morphs.get(morph_id)

    def remove_morph(self, morph_id: str) -> bool:
        if morph_id in self._morphs:
            del self._morphs[morph_id]
            self._correctives.pop(morph_id, None)
            return True
        return False

    def get_all_morphs(self) -> List[MorphTargetEntry]:
        return list(self._morphs.values())

    def add_corrective(self, morph_id: str, corrective: CorrectiveShapeEntry) -> bool:
        if morph_id not in self._morphs:
            return False
        if morph_id not in self._correctives:
            self._correctives[morph_id] = {}
        self._correctives[morph_id][corrective.corrective_id] = corrective
        return True

    def remove_corrective(self, morph_id: str, corrective_id: str) -> bool:
        if morph_id in self._correctives and corrective_id in self._correctives[morph_id]:
            del self._correctives[morph_id][corrective_id]
            return True
        return False

    def get_correctives_for_morph(self, morph_id: str) -> List[CorrectiveShapeEntry]:
        return list(self._correctives.get(morph_id, {}).values())

    def add_preset(self, entry: MorphBlendPresetEntry) -> bool:
        if not entry.preset_id:
            return False
        self._presets[entry.preset_id] = entry
        return True

    def get_preset(self, preset_id: str) -> Optional[MorphBlendPresetEntry]:
        return self._presets.get(preset_id)

    def remove_preset(self, preset_id: str) -> bool:
        if preset_id in self._presets:
            del self._presets[preset_id]
            return True
        return False

    def get_all_presets(self) -> List[MorphBlendPresetEntry]:
        return list(self._presets.values())

    def get_active_morphs(self) -> List[MorphTargetEntry]:
        return [m for m in self._morphs.values() if m.is_active]

    def get_disabled_morphs(self) -> List[MorphTargetEntry]:
        return [m for m in self._morphs.values() if not m.enabled]

    def set_weight(self, morph_id: str, weight: float) -> bool:
        if morph_id in self._morphs:
            self._morphs[morph_id].default_weight = weight
            return True
        return False

    def get_morphs_by_scope(self, scope: str) -> List[MorphTargetEntry]:
        return [m for m in self._morphs.values() if m.scope == scope]

    def validate(self, entry: MorphTargetEntry) -> bool:
        return bool(entry.morph_id) and bool(entry.morph_name)

    @property
    def morph_count(self) -> int:
        return len(self._morphs)

    @property
    def is_empty(self) -> bool:
        return len(self._morphs) == 0

    def clear(self) -> None:
        self._morphs.clear()
        self._correctives.clear()
        self._presets.clear()
