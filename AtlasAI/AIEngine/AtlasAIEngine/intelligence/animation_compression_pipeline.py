"""AtlasAI Phase 42B — Animation Compression Pipeline.

Manages compression scheme entries, per-track overrides, and compression previews
for the AnimationCompressionTool cross-language pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class CompressionSchemeEntry:
    """An animation compression scheme definition."""
    scheme_id: str
    scheme_name: str
    codec: str = "ACL"
    quality: str = "Medium"
    key_reduction: str = "Linear"
    error_threshold: float = 0.01
    rotation_tolerance: float = 0.0001
    translation_tolerance: float = 0.001
    strip_additive_ref_pose: bool = False
    enabled: bool = True

    @property
    def is_lossless(self) -> bool:
        return self.quality == "Lossless"

    @property
    def is_acl(self) -> bool:
        return self.codec == "ACL"

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_high_quality(self) -> bool:
        return self.quality in ("High", "Lossless")

    @property
    def uses_key_reduction(self) -> bool:
        return self.key_reduction != "None"

    @property
    def has_tight_tolerance(self) -> bool:
        return self.error_threshold < 0.001


@dataclass
class TrackCompressionEntry:
    """A per-track compression override."""
    track_comp_id: str
    scheme_id: str
    track_type: str = "Rotation"
    bone_name: str = ""
    override_codec: str = "None"
    override_quality: str = "Medium"
    use_override: bool = False
    enabled: bool = True

    @property
    def is_rotation(self) -> bool:
        return self.track_type == "Rotation"

    @property
    def is_translation(self) -> bool:
        return self.track_type == "Translation"

    @property
    def is_scale(self) -> bool:
        return self.track_type == "Scale"

    @property
    def has_bone(self) -> bool:
        return bool(self.bone_name)

    @property
    def is_override_active(self) -> bool:
        return self.use_override and self.override_codec != "None"

    @property
    def is_enabled(self) -> bool:
        return self.enabled


@dataclass
class CompressionPreviewEntry:
    """A compression preview result."""
    preview_id: str
    scheme_id: str
    animation_asset_id: str = ""
    original_size_kb: float = 0.0
    compressed_size_kb: float = 0.0
    max_error: float = 0.0
    avg_error: float = 0.0
    preview_generated: bool = False

    @property
    def is_generated(self) -> bool:
        return self.preview_generated

    @property
    def compression_ratio(self) -> float:
        if self.original_size_kb <= 0:
            return 0.0
        return self.compressed_size_kb / self.original_size_kb

    @property
    def space_saved_kb(self) -> float:
        return max(0.0, self.original_size_kb - self.compressed_size_kb)

    @property
    def is_high_error(self) -> bool:
        return self.max_error > 1.0

    @property
    def has_animation(self) -> bool:
        return bool(self.animation_asset_id)


class AnimationCompressionPipeline:
    """Pipeline managing animation compression schemes, track overrides, and previews."""

    def __init__(self) -> None:
        self._schemes: Dict[str, CompressionSchemeEntry] = {}
        self._track_compressions: Dict[str, Dict[str, TrackCompressionEntry]] = {}
        self._previews: Dict[str, CompressionPreviewEntry] = {}

    def add_scheme(self, entry: CompressionSchemeEntry) -> bool:
        if not entry.scheme_id:
            return False
        self._schemes[entry.scheme_id] = entry
        if entry.scheme_id not in self._track_compressions:
            self._track_compressions[entry.scheme_id] = {}
        return True

    def get_scheme(self, scheme_id: str) -> Optional[CompressionSchemeEntry]:
        return self._schemes.get(scheme_id)

    def remove_scheme(self, scheme_id: str) -> bool:
        if scheme_id not in self._schemes:
            return False
        del self._schemes[scheme_id]
        self._track_compressions.pop(scheme_id, None)
        return True

    def get_all_schemes(self) -> List[CompressionSchemeEntry]:
        return list(self._schemes.values())

    def get_schemes_by_codec(self, codec: str) -> List[CompressionSchemeEntry]:
        return [s for s in self._schemes.values() if s.codec == codec]

    def get_schemes_by_quality(self, quality: str) -> List[CompressionSchemeEntry]:
        return [s for s in self._schemes.values() if s.quality == quality]

    def add_track_compression(self, scheme_id: str, entry: TrackCompressionEntry) -> bool:
        if scheme_id not in self._schemes:
            return False
        if scheme_id not in self._track_compressions:
            self._track_compressions[scheme_id] = {}
        self._track_compressions[scheme_id][entry.track_comp_id] = entry
        return True

    def remove_track_compression(self, scheme_id: str, track_comp_id: str) -> bool:
        if scheme_id not in self._track_compressions:
            return False
        if track_comp_id not in self._track_compressions[scheme_id]:
            return False
        del self._track_compressions[scheme_id][track_comp_id]
        return True

    def get_track_compressions_for_scheme(self, scheme_id: str) -> List[TrackCompressionEntry]:
        return list(self._track_compressions.get(scheme_id, {}).values())

    def get_track_compressions_by_type(self, track_type: str) -> List[TrackCompressionEntry]:
        result = []
        for entries in self._track_compressions.values():
            result.extend(e for e in entries.values() if e.track_type == track_type)
        return result

    def add_preview(self, entry: CompressionPreviewEntry) -> bool:
        if not entry.preview_id:
            return False
        self._previews[entry.preview_id] = entry
        return True

    def generate_preview(self, preview_id: str) -> bool:
        if preview_id not in self._previews:
            return False
        self._previews[preview_id].preview_generated = True
        return True

    def remove_preview(self, preview_id: str) -> bool:
        if preview_id not in self._previews:
            return False
        del self._previews[preview_id]
        return True

    def get_preview(self, preview_id: str) -> Optional[CompressionPreviewEntry]:
        return self._previews.get(preview_id)

    def get_previews_for_scheme(self, scheme_id: str) -> List[CompressionPreviewEntry]:
        return [p for p in self._previews.values() if p.scheme_id == scheme_id]

    def get_generated_previews(self) -> List[CompressionPreviewEntry]:
        return [p for p in self._previews.values() if p.preview_generated]

    def validate(self, entry: CompressionSchemeEntry) -> bool:
        return bool(entry.scheme_id) and bool(entry.scheme_name)

    @property
    def scheme_count(self) -> int:
        return len(self._schemes)

    @property
    def is_empty(self) -> bool:
        return len(self._schemes) == 0

    def clear(self) -> None:
        self._schemes.clear()
        self._track_compressions.clear()
        self._previews.clear()
