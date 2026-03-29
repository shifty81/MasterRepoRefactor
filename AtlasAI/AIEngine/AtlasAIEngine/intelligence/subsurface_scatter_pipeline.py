"""AtlasAI Phase 43B — Subsurface Scatter Pipeline.

Manages SSS profiles, transmission definitions, and scatter kernels
for the SubsurfaceScatteringTool cross-language pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class SSSProfileEntry:
    """A subsurface scattering profile."""
    profile_id: str
    profile_name: str
    scatter_model: str = "Burley"
    quality: str = "Medium"
    scatter_radius_r: float = 1.0
    scatter_radius_g: float = 0.7
    scatter_radius_b: float = 0.5
    opacity: float = 1.0
    enabled: bool = True

    @property
    def is_burley(self) -> bool:
        return self.scatter_model == "Burley"

    @property
    def is_separable(self) -> bool:
        return self.scatter_model == "Separable"

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def is_high_quality(self) -> bool:
        return self.quality in ("High", "Ultra")

    @property
    def is_opaque(self) -> bool:
        return self.opacity >= 1.0

    @property
    def has_rgb_radii(self) -> bool:
        return (self.scatter_radius_r != self.scatter_radius_g or
                self.scatter_radius_g != self.scatter_radius_b)

    @property
    def max_scatter_radius(self) -> float:
        return max(self.scatter_radius_r, self.scatter_radius_g, self.scatter_radius_b)

    @property
    def is_chromatic(self) -> bool:
        return self.has_rgb_radii


@dataclass
class TransmissionEntry:
    """Transmission profile for SSS."""
    transmission_id: str
    profile_id: str
    mode: str = "Thick"
    transmittance_r: float = 0.2
    transmittance_g: float = 0.1
    transmittance_b: float = 0.05
    thickness: float = 1.0
    shadow_cast: bool = True
    enabled: bool = True

    @property
    def is_thick(self) -> bool:
        return self.mode == "Thick"

    @property
    def is_thin(self) -> bool:
        return self.mode == "Thin"

    @property
    def is_wrap(self) -> bool:
        return self.mode == "Wrap"

    @property
    def casts_shadow(self) -> bool:
        return self.shadow_cast

    @property
    def is_translucent(self) -> bool:
        return any(v > 0 for v in [self.transmittance_r, self.transmittance_g, self.transmittance_b])

    @property
    def is_enabled(self) -> bool:
        return self.enabled


@dataclass
class SSSKernelEntry:
    """A scatter kernel definition."""
    kernel_id: str
    profile_id: str
    channel: str = "All"
    sample_count: int = 32
    scatter_scale: float = 1.0
    world_unit_scale: float = 0.1
    use_follow_surface: bool = True
    enabled: bool = True

    @property
    def is_all_channels(self) -> bool:
        return self.channel == "All"

    @property
    def is_high_sample(self) -> bool:
        return self.sample_count >= 64

    @property
    def is_low_sample(self) -> bool:
        return self.sample_count <= 16

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def uses_follow_surface(self) -> bool:
        return self.use_follow_surface


class SubsurfaceScatterPipeline:
    """Pipeline managing SSS profiles, transmission entries, and scatter kernels."""

    def __init__(self) -> None:
        self._profiles: Dict[str, SSSProfileEntry] = {}
        self._transmissions: Dict[str, Dict[str, TransmissionEntry]] = {}
        self._kernels: Dict[str, Dict[str, SSSKernelEntry]] = {}

    def add_profile(self, entry: SSSProfileEntry) -> bool:
        if not entry.profile_id:
            return False
        self._profiles[entry.profile_id] = entry
        self._transmissions.setdefault(entry.profile_id, {})
        self._kernels.setdefault(entry.profile_id, {})
        return True

    def get_profile(self, profile_id: str) -> Optional[SSSProfileEntry]:
        return self._profiles.get(profile_id)

    def remove_profile(self, profile_id: str) -> bool:
        if profile_id not in self._profiles:
            return False
        del self._profiles[profile_id]
        self._transmissions.pop(profile_id, None)
        self._kernels.pop(profile_id, None)
        return True

    def get_all_profiles(self) -> List[SSSProfileEntry]:
        return list(self._profiles.values())

    def get_profiles_by_model(self, model: str) -> List[SSSProfileEntry]:
        return [p for p in self._profiles.values() if p.scatter_model == model]

    def get_enabled_profiles(self) -> List[SSSProfileEntry]:
        return [p for p in self._profiles.values() if p.enabled]

    def add_transmission(self, profile_id: str, entry: TransmissionEntry) -> bool:
        if profile_id not in self._profiles:
            return False
        self._transmissions.setdefault(profile_id, {})[entry.transmission_id] = entry
        return True

    def remove_transmission(self, profile_id: str, transmission_id: str) -> bool:
        if profile_id not in self._transmissions:
            return False
        if transmission_id not in self._transmissions[profile_id]:
            return False
        del self._transmissions[profile_id][transmission_id]
        return True

    def get_transmissions_for_profile(self, profile_id: str) -> List[TransmissionEntry]:
        return list(self._transmissions.get(profile_id, {}).values())

    def add_kernel(self, profile_id: str, entry: SSSKernelEntry) -> bool:
        if profile_id not in self._profiles:
            return False
        self._kernels.setdefault(profile_id, {})[entry.kernel_id] = entry
        return True

    def remove_kernel(self, profile_id: str, kernel_id: str) -> bool:
        if profile_id not in self._kernels:
            return False
        if kernel_id not in self._kernels[profile_id]:
            return False
        del self._kernels[profile_id][kernel_id]
        return True

    def get_kernels_for_profile(self, profile_id: str) -> List[SSSKernelEntry]:
        return list(self._kernels.get(profile_id, {}).values())

    def get_kernels_by_channel(self, channel: str) -> List[SSSKernelEntry]:
        result = []
        for kernels in self._kernels.values():
            result.extend(k for k in kernels.values() if k.channel == channel)
        return result

    def validate(self, entry: SSSProfileEntry) -> bool:
        return bool(entry.profile_id) and bool(entry.profile_name)

    @property
    def profile_count(self) -> int:
        return len(self._profiles)

    @property
    def is_empty(self) -> bool:
        return len(self._profiles) == 0

    def clear(self) -> None:
        self._profiles.clear()
        self._transmissions.clear()
        self._kernels.clear()
