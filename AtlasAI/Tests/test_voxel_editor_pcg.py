"""Tests for the Voxel Editor workflow (C1) and PCG Debug mode (C4)."""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestVoxelEditorSourceFilesExist(unittest.TestCase):
    """Verify voxel editor source files are present."""

    def _check(self, path: str):
        full = REPO_ROOT / path
        self.assertTrue(full.exists(), f"Missing: {path}")

    def test_voxel_types_header(self):
        self._check("Atlas/Editor/Voxel/VoxelTypes.h")

    def test_voxel_chunk_editor_header(self):
        self._check("Atlas/Editor/Voxel/VoxelChunkEditor.h")

    def test_voxel_chunk_editor_source(self):
        self._check("Atlas/Editor/Voxel/VoxelChunkEditor.cpp")

    def test_voxel_editor_mode_header(self):
        self._check("Atlas/Editor/Voxel/VoxelEditorMode.h")

    def test_voxel_editor_mode_source(self):
        self._check("Atlas/Editor/Voxel/VoxelEditorMode.cpp")


class TestVoxelTypesContent(unittest.TestCase):
    """Verify VoxelTypes.h contains the expected declarations."""

    def _read(self, path: str) -> str:
        return (REPO_ROOT / path).read_text(encoding="utf-8")

    def test_has_voxel_pos(self):
        self.assertIn("VoxelPos", self._read("Atlas/Editor/Voxel/VoxelTypes.h"))

    def test_has_voxel_cell(self):
        self.assertIn("VoxelCell", self._read("Atlas/Editor/Voxel/VoxelTypes.h"))

    def test_has_dirty_region(self):
        self.assertIn("DirtyRegion", self._read("Atlas/Editor/Voxel/VoxelTypes.h"))

    def test_has_brush_settings(self):
        self.assertIn("BrushSettings", self._read("Atlas/Editor/Voxel/VoxelTypes.h"))

    def test_has_brush_op_enum(self):
        self.assertIn("EBrushOp", self._read("Atlas/Editor/Voxel/VoxelTypes.h"))

    def test_has_brush_shape_enum(self):
        self.assertIn("EBrushShape", self._read("Atlas/Editor/Voxel/VoxelTypes.h"))

    def test_has_chunk_edit_result(self):
        self.assertIn("ChunkEditResult", self._read("Atlas/Editor/Voxel/VoxelTypes.h"))

    def test_has_chunk_size_constant(self):
        self.assertIn("kChunkSize", self._read("Atlas/Editor/Voxel/VoxelTypes.h"))


class TestVoxelChunkEditorContent(unittest.TestCase):
    """Verify VoxelChunkEditor.h contains the expected API."""

    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/Voxel/VoxelChunkEditor.h").read_text(encoding="utf-8")

    def test_has_set_cell(self):
        self.assertIn("SetCell", self._read())

    def test_has_clear_cell(self):
        self.assertIn("ClearCell", self._read())

    def test_has_apply_brush(self):
        self.assertIn("ApplyBrush", self._read())

    def test_has_is_dirty(self):
        self.assertIn("IsDirty", self._read())

    def test_has_clear_dirty(self):
        self.assertIn("ClearDirty", self._read())

    def test_has_trigger_mesh_rebuild(self):
        self.assertIn("TriggerMeshRebuild", self._read())

    def test_has_serialise(self):
        self.assertIn("Serialise", self._read())

    def test_has_deserialise(self):
        self.assertIn("Deserialise", self._read())

    def test_has_in_bounds(self):
        self.assertIn("InBounds", self._read())


class TestVoxelEditorModeContent(unittest.TestCase):
    """Verify VoxelEditorMode.h contains the expected API."""

    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/Voxel/VoxelEditorMode.h").read_text(encoding="utf-8")

    def test_has_get_or_create_chunk(self):
        self.assertIn("GetOrCreateChunk", self._read())

    def test_has_stroke(self):
        self.assertIn("Stroke", self._read())

    def test_has_set_brush(self):
        self.assertIn("SetBrush", self._read())

    def test_has_get_dirty_chunk_ids(self):
        self.assertIn("GetDirtyChunkIds", self._read())

    def test_has_rebuild_dirty_meshes(self):
        self.assertIn("RebuildDirtyMeshes", self._read())

    def test_has_serialise_all(self):
        self.assertIn("SerialiseAll", self._read())

    def test_has_deserialise_all(self):
        self.assertIn("DeserialiseAll", self._read())


class TestPCGDebugSourceFilesExist(unittest.TestCase):
    """Verify PCG debug source files are present."""

    def _check(self, path: str):
        full = REPO_ROOT / path
        self.assertTrue(full.exists(), f"Missing: {path}")

    def test_pcg_debug_types_header(self):
        self._check("Atlas/Editor/PCG/PCGDebugTypes.h")

    def test_pcg_debug_system_header(self):
        self._check("Atlas/Editor/PCG/PCGDebugSystem.h")

    def test_pcg_debug_system_source(self):
        self._check("Atlas/Editor/PCG/PCGDebugSystem.cpp")


class TestPCGDebugTypesContent(unittest.TestCase):
    """Verify PCGDebugTypes.h contains the expected declarations."""

    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/PCG/PCGDebugTypes.h").read_text(encoding="utf-8")

    def test_has_pcg_spawn_point(self):
        self.assertIn("PCGSpawnPoint", self._read())

    def test_has_pcg_generation_bounds(self):
        self.assertIn("PCGGenerationBounds", self._read())

    def test_has_pcg_rule_inspector_entry(self):
        self.assertIn("PCGRuleInspectorEntry", self._read())

    def test_has_pcg_debug_state(self):
        self.assertIn("PCGDebugState", self._read())


class TestPCGDebugSystemContent(unittest.TestCase):
    """Verify PCGDebugSystem.h contains the expected API."""

    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/PCG/PCGDebugSystem.h").read_text(encoding="utf-8")

    def test_has_set_seed(self):
        self.assertIn("SetSeed", self._read())

    def test_has_regenerate_world(self):
        self.assertIn("RegenerateWorld", self._read())

    def test_has_regenerate_selected(self):
        self.assertIn("RegenerateSelected", self._read())

    def test_has_add_spawn_point(self):
        self.assertIn("AddSpawnPoint", self._read())

    def test_has_add_region_bounds(self):
        self.assertIn("AddRegionBounds", self._read())

    def test_has_register_rule(self):
        self.assertIn("RegisterRule", self._read())

    def test_has_override_rule(self):
        self.assertIn("OverrideRule", self._read())

    def test_has_clear_override(self):
        self.assertIn("ClearOverride", self._read())

    def test_has_lock_content(self):
        self.assertIn("LockContent", self._read())

    def test_has_regenerate_callback(self):
        self.assertIn("RegenerateCallback", self._read())


class TestEditorCMakeUpdated(unittest.TestCase):
    """Verify Atlas/Editor/CMakeLists.txt includes new voxel and PCG sources."""

    def _cmake(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/CMakeLists.txt").read_text(encoding="utf-8")

    def test_cmake_includes_voxel_chunk_editor(self):
        self.assertIn("VoxelChunkEditor.cpp", self._cmake())

    def test_cmake_includes_voxel_editor_mode(self):
        self.assertIn("VoxelEditorMode.cpp", self._cmake())

    def test_cmake_includes_pcg_debug_system(self):
        self.assertIn("PCGDebugSystem.cpp", self._cmake())

    def test_cmake_includes_voxel_dir(self):
        self.assertIn("Voxel", self._cmake())

    def test_cmake_includes_pcg_dir(self):
        self.assertIn("PCG", self._cmake())


if __name__ == "__main__":
    unittest.main()
