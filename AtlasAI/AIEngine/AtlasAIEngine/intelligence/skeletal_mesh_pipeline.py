"""AtlasAI Phase 41B — Skeletal Mesh Pipeline.

Manages skeletal mesh bone definitions, weight paint entries, and LOD configs
for the SkeletalMeshEditorTool cross-language pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class BoneEntry:
    """A bone definition in a skeletal mesh."""
    bone_id: str
    bone_name: str
    parent_bone_id: str = ""
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    rot_x: float = 0.0
    rot_y: float = 0.0
    rot_z: float = 0.0
    length: float = 1.0
    is_root: bool = False

    @property
    def has_parent(self) -> bool:
        return bool(self.parent_bone_id)

    @property
    def is_leaf(self) -> bool:
        return self.length < 0.01

    @property
    def is_at_origin(self) -> bool:
        return self.pos_x == 0.0 and self.pos_y == 0.0 and self.pos_z == 0.0

    @property
    def is_root_bone(self) -> bool:
        return self.is_root

    @property
    def has_rotation(self) -> bool:
        return self.rot_x != 0.0 or self.rot_y != 0.0 or self.rot_z != 0.0


@dataclass
class WeightPaintEntry:
    """A weight painting entry for a bone on a mesh."""
    entry_id: str
    bone_id: str
    mesh_id: str
    brush_radius: float = 5.0
    brush_strength: float = 0.5
    mode: str = "Additive"
    symmetry: bool = False
    applied: bool = False

    @property
    def is_additive(self) -> bool:
        return self.mode == "Additive"

    @property
    def is_subtractive(self) -> bool:
        return self.mode == "Subtractive"

    @property
    def is_applied(self) -> bool:
        return self.applied

    @property
    def is_symmetric(self) -> bool:
        return self.symmetry

    @property
    def is_strong(self) -> bool:
        return self.brush_strength > 0.75


@dataclass
class MeshLODEntry:
    """A mesh LOD configuration."""
    lod_id: str
    mesh_id: str
    lod_level: int = 0
    screen_size_threshold: float = 1.0
    reduction_percent: float = 0.0
    strategy: str = "Auto"
    generated: bool = False

    @property
    def is_base_lod(self) -> bool:
        return self.lod_level == 0

    @property
    def is_auto(self) -> bool:
        return self.strategy == "Auto"

    @property
    def is_generated(self) -> bool:
        return self.generated

    @property
    def has_reduction(self) -> bool:
        return self.reduction_percent > 0.0

    @property
    def is_high_lod(self) -> bool:
        return self.lod_level >= 3


class SkeletalMeshPipeline:
    """Pipeline managing skeletal mesh bones, weight paint entries, and LODs."""

    def __init__(self) -> None:
        self._bones: Dict[str, BoneEntry] = {}
        self._weight_entries: Dict[str, WeightPaintEntry] = {}
        self._lods: Dict[str, MeshLODEntry] = {}
        self._edit_mode: str = "Bones"

    def add_bone(self, entry: BoneEntry) -> bool:
        if not entry.bone_id:
            return False
        self._bones[entry.bone_id] = entry
        return True

    def get_bone(self, bone_id: str) -> Optional[BoneEntry]:
        return self._bones.get(bone_id)

    def remove_bone(self, bone_id: str) -> bool:
        if bone_id not in self._bones:
            return False
        del self._bones[bone_id]
        return True

    def get_all_bones(self) -> List[BoneEntry]:
        return list(self._bones.values())

    def get_root_bones(self) -> List[BoneEntry]:
        return [b for b in self._bones.values() if b.is_root]

    def get_children(self, parent_bone_id: str) -> List[BoneEntry]:
        return [b for b in self._bones.values() if b.parent_bone_id == parent_bone_id]

    def rename_bone(self, bone_id: str, new_name: str) -> bool:
        if bone_id not in self._bones:
            return False
        self._bones[bone_id].bone_name = new_name
        return True

    def add_weight_entry(self, entry: WeightPaintEntry) -> bool:
        if not entry.entry_id:
            return False
        self._weight_entries[entry.entry_id] = entry
        return True

    def remove_weight_entry(self, entry_id: str) -> bool:
        if entry_id not in self._weight_entries:
            return False
        del self._weight_entries[entry_id]
        return True

    def get_weight_entry(self, entry_id: str) -> Optional[WeightPaintEntry]:
        return self._weight_entries.get(entry_id)

    def get_weight_entries_by_bone(self, bone_id: str) -> List[WeightPaintEntry]:
        return [e for e in self._weight_entries.values() if e.bone_id == bone_id]

    def apply_weight(self, entry_id: str) -> bool:
        if entry_id not in self._weight_entries:
            return False
        self._weight_entries[entry_id].applied = True
        return True

    def add_lod(self, entry: MeshLODEntry) -> bool:
        if not entry.lod_id:
            return False
        self._lods[entry.lod_id] = entry
        return True

    def remove_lod(self, lod_id: str) -> bool:
        if lod_id not in self._lods:
            return False
        del self._lods[lod_id]
        return True

    def get_lod(self, lod_id: str) -> Optional[MeshLODEntry]:
        return self._lods.get(lod_id)

    def get_lods_by_mesh(self, mesh_id: str) -> List[MeshLODEntry]:
        return [l for l in self._lods.values() if l.mesh_id == mesh_id]

    def generate_lod(self, lod_id: str) -> bool:
        if lod_id not in self._lods:
            return False
        self._lods[lod_id].generated = True
        return True

    def set_edit_mode(self, mode: str) -> bool:
        valid_modes = {"Bones", "Weights", "Sockets", "LOD", "Morph", "Physics", "Custom"}
        if mode not in valid_modes:
            return False
        self._edit_mode = mode
        return True

    @property
    def edit_mode(self) -> str:
        return self._edit_mode

    def validate(self, entry: BoneEntry) -> bool:
        return bool(entry.bone_id) and bool(entry.bone_name)

    @property
    def bone_count(self) -> int:
        return len(self._bones)

    @property
    def is_empty(self) -> bool:
        return len(self._bones) == 0

    def clear(self) -> None:
        self._bones.clear()
        self._weight_entries.clear()
        self._lods.clear()
