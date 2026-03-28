"""Tests for C2 (Outliner/Inspector), C3 (Gizmo/Placement), and C7 (Prefabs)."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# =============================================================================
# C2 — Outliner + Inspector completion
# =============================================================================

class TestHierarchyNodeExists(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_hierarchy_node_header(self):
        self._check("Atlas/Editor/Outliner/HierarchyNode.h")

    def test_scene_hierarchy_system_header(self):
        self._check("Atlas/Editor/Outliner/SceneHierarchySystem.h")

    def test_scene_hierarchy_system_source(self):
        self._check("Atlas/Editor/Outliner/SceneHierarchySystem.cpp")


class TestHierarchyNodeContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/Outliner/HierarchyNode.h").read_text(encoding="utf-8")

    def test_has_node_type_enum(self):
        self.assertIn("ENodeType", self._read())

    def test_has_component_summary_entry(self):
        self.assertIn("ComponentSummaryEntry", self._read())

    def test_has_hierarchy_node_struct(self):
        self.assertIn("HierarchyNode", self._read())

    def test_has_pos_fields(self):
        self.assertIn("posX", self._read())

    def test_has_rot_fields(self):
        self.assertIn("rotX", self._read())

    def test_has_scale_fields(self):
        self.assertIn("scaleX", self._read())

    def test_has_owner_id(self):
        self.assertIn("ownerId", self._read())

    def test_has_faction_id(self):
        self.assertIn("factionId", self._read())

    def test_has_linked_asset_id(self):
        self.assertIn("linkedAssetId", self._read())

    def test_has_is_locked(self):
        self.assertIn("isLocked", self._read())

    def test_node_types_cover_key_entities(self):
        text = self._read()
        for t in ["Entity", "Module", "Structure", "Character", "FleetGroup",
                  "VoxelChunk", "Folder"]:
            self.assertIn(t, text, f"Missing node type: {t}")


class TestSceneHierarchySystemContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/Outliner/SceneHierarchySystem.h").read_text(encoding="utf-8")

    def test_has_add_node(self):
        self.assertIn("AddNode", self._read())

    def test_has_remove_node(self):
        self.assertIn("RemoveNode", self._read())

    def test_has_reparent_node(self):
        self.assertIn("ReparentNode", self._read())

    def test_has_set_transform(self):
        self.assertIn("SetTransform", self._read())

    def test_has_reset_transform(self):
        self.assertIn("ResetTransform", self._read())

    def test_has_add_component(self):
        self.assertIn("AddComponent", self._read())

    def test_has_set_component_active(self):
        self.assertIn("SetComponentActive", self._read())

    def test_has_create_folder(self):
        self.assertIn("CreateFolder", self._read())

    def test_has_group_into_folder(self):
        self.assertIn("GroupIntoFolder", self._read())

    def test_has_set_visible(self):
        self.assertIn("SetVisible", self._read())

    def test_has_set_locked(self):
        self.assertIn("SetLocked", self._read())

    def test_has_set_property(self):
        self.assertIn("SetProperty", self._read())

    def test_has_transform_edit_callback(self):
        self.assertIn("TransformEditCallback", self._read())

    def test_has_property_edit_callback(self):
        self.assertIn("PropertyEditCallback", self._read())

    def test_has_list_root_nodes(self):
        self.assertIn("ListRootNodes", self._read())

    def test_has_list_children(self):
        self.assertIn("ListChildren", self._read())

    def test_has_list_by_type(self):
        self.assertIn("ListByType", self._read())

    def test_has_flat_list(self):
        self.assertIn("FlatList", self._read())


# =============================================================================
# C3 — Gizmo + Placement completion
# =============================================================================

class TestPlacementSystemExists(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_placement_system_header(self):
        self._check("Atlas/Editor/Gizmos/PlacementSystem.h")

    def test_placement_system_source(self):
        self._check("Atlas/Editor/Gizmos/PlacementSystem.cpp")


class TestPlacementSystemContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/Gizmos/PlacementSystem.h").read_text(encoding="utf-8")

    def test_has_grid_snap_result(self):
        self.assertIn("GridSnapResult", self._read())

    def test_has_socket_point(self):
        self.assertIn("SocketPoint", self._read())

    def test_has_placement_ghost(self):
        self.assertIn("PlacementGhost", self._read())

    def test_has_placement_validity_result(self):
        self.assertIn("PlacementValidityResult", self._read())

    def test_has_set_grid_size(self):
        self.assertIn("SetGridSize", self._read())

    def test_has_snap_to_grid(self):
        self.assertIn("SnapToGrid", self._read())

    def test_has_register_socket(self):
        self.assertIn("RegisterSocket", self._read())

    def test_has_find_nearest_socket(self):
        self.assertIn("FindNearestSocket", self._read())

    def test_has_begin_placement(self):
        self.assertIn("BeginPlacement", self._read())

    def test_has_update_placement_position(self):
        self.assertIn("UpdatePlacementPosition", self._read())

    def test_has_confirm_placement(self):
        self.assertIn("ConfirmPlacement", self._read())

    def test_has_check_validity(self):
        self.assertIn("CheckValidity", self._read())

    def test_has_apply_delta_move(self):
        self.assertIn("ApplyDeltaMove", self._read())

    def test_has_apply_transform(self):
        self.assertIn("ApplyTransform", self._read())

    def test_has_set_local_space(self):
        self.assertIn("SetLocalSpace", self._read())

    def test_has_placement_confirmed_callback(self):
        self.assertIn("PlacementConfirmedCallback", self._read())


# =============================================================================
# C7 — Prefab / Template Authoring
# =============================================================================

class TestPrefabFilesExist(unittest.TestCase):
    def _check(self, path: str):
        self.assertTrue((REPO_ROOT / path).exists(), f"Missing: {path}")

    def test_prefab_types_header(self):
        self._check("Atlas/Editor/Prefabs/PrefabTypes.h")

    def test_prefab_library_header(self):
        self._check("Atlas/Editor/Prefabs/PrefabLibrary.h")

    def test_prefab_library_source(self):
        self._check("Atlas/Editor/Prefabs/PrefabLibrary.cpp")

    def test_prefab_manager_header(self):
        self._check("Atlas/Editor/Prefabs/PrefabManager.h")

    def test_prefab_manager_source(self):
        self._check("Atlas/Editor/Prefabs/PrefabManager.cpp")


class TestPrefabTypesContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/Prefabs/PrefabTypes.h").read_text(encoding="utf-8")

    def test_has_prefab_category_enum(self):
        self.assertIn("EPrefabCategory", self._read())

    def test_has_prefab_voxel_cell(self):
        self.assertIn("PrefabVoxelCell", self._read())

    def test_has_prefab_child_node(self):
        self.assertIn("PrefabChildNode", self._read())

    def test_has_prefab_metadata(self):
        self.assertIn("PrefabMetadata", self._read())

    def test_has_prefab_definition(self):
        self.assertIn("PrefabDefinition", self._read())

    def test_has_use_count(self):
        self.assertIn("useCount", self._read())

    def test_has_thumbnail_path(self):
        self.assertIn("thumbnailPath", self._read())

    def test_categories_cover_key_types(self):
        text = self._read()
        for cat in ["Structure", "Module", "Terrain", "Character"]:
            self.assertIn(cat, text, f"Missing prefab category: {cat}")


class TestPrefabLibraryContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/Prefabs/PrefabLibrary.h").read_text(encoding="utf-8")

    def test_has_register_prefab(self):
        self.assertIn("RegisterPrefab", self._read())

    def test_has_unregister_prefab(self):
        self.assertIn("UnregisterPrefab", self._read())

    def test_has_find_by_id(self):
        self.assertIn("FindById", self._read())

    def test_has_list_by_category(self):
        self.assertIn("ListByCategory", self._read())

    def test_has_search(self):
        self.assertIn("Search", self._read())

    def test_has_update_metadata(self):
        self.assertIn("UpdateMetadata", self._read())

    def test_has_increment_use_count(self):
        self.assertIn("IncrementUseCount", self._read())

    def test_has_count_by_category(self):
        self.assertIn("CountByCategory", self._read())


class TestPrefabManagerContent(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/Prefabs/PrefabManager.h").read_text(encoding="utf-8")

    def test_has_capture_from_selection(self):
        self.assertIn("CaptureFromSelection", self._read())

    def test_has_save_to_library(self):
        self.assertIn("SaveToLibrary", self._read())

    def test_has_place(self):
        self.assertIn("Place", self._read())

    def test_has_generate_id(self):
        self.assertIn("GenerateId", self._read())

    def test_has_selection_snapshot(self):
        self.assertIn("SelectionSnapshot", self._read())

    def test_has_prefab_placement_result(self):
        self.assertIn("PrefabPlacementResult", self._read())

    def test_has_place_callback(self):
        self.assertIn("PrefabPlaceCallback", self._read())


class TestEditorCMakeFullyUpdated(unittest.TestCase):
    def _cmake(self) -> str:
        return (REPO_ROOT / "Atlas/Editor/CMakeLists.txt").read_text(encoding="utf-8")

    def test_has_scene_hierarchy_system(self):
        self.assertIn("SceneHierarchySystem.cpp", self._cmake())

    def test_has_placement_system(self):
        self.assertIn("PlacementSystem.cpp", self._cmake())

    def test_has_prefab_library(self):
        self.assertIn("PrefabLibrary.cpp", self._cmake())

    def test_has_prefab_manager(self):
        self.assertIn("PrefabManager.cpp", self._cmake())

    def test_has_prefabs_dir(self):
        self.assertIn("Prefabs", self._cmake())


if __name__ == "__main__":
    unittest.main()
