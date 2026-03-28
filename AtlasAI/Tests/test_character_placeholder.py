"""Tests for the placeholder_male_base character integration.

Validates that all character data definition files are present, structurally
correct, and consistent with each other.  Binary mesh files are git-ignored
and therefore NOT checked here — their presence is validated at runtime by
the AssetRegistry.
"""

import json
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _p(rel: str) -> Path:
    return REPO_ROOT / rel


def _load_json(rel: str) -> dict:
    path = _p(rel)
    assert path.exists(), f"Missing file: {rel}"
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Core data files present
# ---------------------------------------------------------------------------

class TestPlaceholderCharacterFilesExist:
    def test_placeholder_male_base_json(self):
        assert _p("NovaForge/Content/Data/Characters/placeholder_male_base.json").exists()

    def test_placeholder_male_base_rig_json(self):
        assert _p("NovaForge/Content/Data/Characters/placeholder_male_base_rig.json").exists()

    def test_placeholder_male_base_anim_map_json(self):
        assert _p("NovaForge/Content/Data/Animation/placeholder_male_base_anim_map.json").exists()

    def test_asset_manifest(self):
        assert _p("NovaForge/Content/Meshes/Characters/ASSET_MANIFEST.json").exists()

    def test_guide_doc(self):
        assert _p("Docs/Art/CHARACTER_PLACEHOLDER_GUIDE.md").exists()


# ---------------------------------------------------------------------------
# placeholder_male_base.json structure
# ---------------------------------------------------------------------------

class TestPlaceholderCharacterContent:
    def setup_method(self):
        self.data = _load_json("NovaForge/Content/Data/Characters/placeholder_male_base.json")

    def test_id(self):
        assert self.data["id"] == "placeholder_male_base"

    def test_skeleton_id(self):
        assert self.data["skeleton_id"] == "base_humanoid"

    def test_is_placeholder_flag(self):
        assert self.data.get("is_placeholder") is True

    def test_has_eight_body_parts(self):
        assert len(self.data["body_parts"]) == 8

    def test_default_palette_has_roles(self):
        palette = self.data.get("default_palette", [])
        assert len(palette) == 3
        roles = {entry["role"] for entry in palette}
        assert roles == {"skin_tone", "suit_primary", "suit_accent"}

    def test_body_part_slots(self):
        slots = {p["slot"] for p in self.data["body_parts"]}
        expected = {"Head", "Torso", "ArmLeft", "ArmRight", "LegLeft", "LegRight", "Hands", "Feet"}
        assert slots == expected

    def test_all_body_parts_have_mesh_id(self):
        for part in self.data["body_parts"]:
            assert "mesh_id" in part, f"Body part {part.get('slot')} missing mesh_id"
            assert part["mesh_id"], f"Body part {part.get('slot')} has empty mesh_id"

    def test_all_body_parts_have_tri_budget(self):
        for part in self.data["body_parts"]:
            assert "tri_budget" in part, f"Body part {part.get('slot')} missing tri_budget"
            assert part["tri_budget"] > 0

    def test_total_tri_budget_within_ceiling(self):
        total = sum(p["tri_budget"] for p in self.data["body_parts"])
        assert total <= self.data["max_tri_count"], (
            f"Sum of tri budgets ({total}) exceeds max_tri_count ({self.data['max_tri_count']})")

    def test_has_seven_sockets(self):
        assert len(self.data["sockets"]) == 7

    def test_required_sockets_present(self):
        socket_ids = {s["id"] for s in self.data["sockets"]}
        required = {
            "socket_hand_r", "socket_hand_l",
            "socket_backpack", "socket_helmet",
            "socket_tool_mount", "socket_hip_r", "socket_hip_l",
        }
        assert required.issubset(socket_ids)

    def test_movement_modes(self):
        modes = set(self.data["movement_modes"])
        assert {"fps", "eva", "mech"}.issubset(modes)

    def test_scale_is_reasonable(self):
        assert 1.5 <= self.data["scale_meters"] <= 2.2

    def test_eye_height_below_scale(self):
        assert self.data["eye_height_meters"] < self.data["scale_meters"]

    def test_source_asset_named(self):
        assert self.data.get("source_asset"), "source_asset must be specified"

    def test_flat_shaded_flag(self):
        assert self.data.get("flat_shaded") is True

    def test_vertex_colors_flag(self):
        assert self.data.get("use_vertex_colors") is True


# ---------------------------------------------------------------------------
# placeholder_male_base_rig.json structure
# ---------------------------------------------------------------------------

class TestPlaceholderRigContent:
    def setup_method(self):
        self.data = _load_json("NovaForge/Content/Data/Characters/placeholder_male_base_rig.json")

    def test_references_correct_character(self):
        assert self.data["character_id"] == "placeholder_male_base"

    def test_has_fps_camera(self):
        cam = self.data.get("fps_camera", {})
        assert "eye_socket_bone" in cam
        assert "local_offset" in cam
        assert len(cam["local_offset"]) == 3

    def test_has_fps_hands(self):
        hands = self.data.get("fps_hands", {})
        assert "mesh_id" in hands
        assert "socket" in hands
        assert len(hands["local_offset"]) == 3

    def test_rig_slots_present(self):
        slots = self.data.get("rig_slots", {})
        required = {"helmet", "torso", "backpack", "primary", "secondary"}
        assert required.issubset(set(slots.keys()))

    def test_all_rig_slots_have_socket(self):
        for slot_name, slot in self.data["rig_slots"].items():
            assert "socket" in slot, f"rig_slot '{slot_name}' missing 'socket'"


# ---------------------------------------------------------------------------
# placeholder_male_base_anim_map.json structure
# ---------------------------------------------------------------------------

class TestPlaceholderAnimMapContent:
    def setup_method(self):
        self.data = _load_json("NovaForge/Content/Data/Animation/placeholder_male_base_anim_map.json")

    def test_references_correct_character(self):
        assert self.data["character_id"] == "placeholder_male_base"

    def test_is_placeholder_flag(self):
        assert self.data.get("is_placeholder") is True

    def test_skeleton_id(self):
        assert self.data["skeleton_id"] == "base_humanoid"

    def test_has_clip_map(self):
        assert isinstance(self.data.get("clip_map"), dict)
        assert len(self.data["clip_map"]) > 0

    def test_required_locomotion_clips_mapped(self):
        cm = self.data["clip_map"]
        required = {"anim_fps_idle", "anim_fps_walk_f", "anim_fps_run_f",
                    "anim_add_breathing", "anim_tool_idle"}
        for clip in required:
            assert clip in cm, f"Required clip '{clip}' missing from clip_map"
            assert cm[clip], f"Clip '{clip}' has empty mapping"

    def test_has_retarget_settings(self):
        retarget = self.data.get("retarget_settings", {})
        assert "source_rig" in retarget
        assert "target_rig" in retarget
        assert retarget["target_rig"] == "base_humanoid"


# ---------------------------------------------------------------------------
# ASSET_MANIFEST.json structure
# ---------------------------------------------------------------------------

class TestAssetManifestContent:
    def setup_method(self):
        self.data = _load_json("NovaForge/Content/Meshes/Characters/ASSET_MANIFEST.json")

    def test_manifest_version(self):
        assert self.data.get("manifest_version") == 1

    def test_character_id(self):
        assert self.data["character_id"] == "placeholder_male_base"

    def test_asset_source_present(self):
        src = self.data.get("asset_source", {})
        assert "name" in src
        assert "license" in src
        assert "url" in src

    def test_cc0_license(self):
        assert "CC0" in self.data["asset_source"]["license"]

    def test_expected_files_list(self):
        files = self.data.get("expected_files", [])
        assert len(files) >= 8, "Manifest should list at least 8 mesh files"

    def test_each_expected_file_has_required_keys(self):
        for f in self.data["expected_files"]:
            assert "file" in f, f"Entry missing 'file' key: {f}"
            assert "description" in f, f"Entry missing 'description': {f}"
            assert "max_tris" in f, f"Entry missing 'max_tris': {f}"
            assert f["max_tris"] > 0

    def test_combined_mesh_listed(self):
        files = {f["file"] for f in self.data["expected_files"]}
        assert "free_lowpoly_male_base.glb" in files

    def test_fps_hands_mesh_listed(self):
        files = {f["file"] for f in self.data["expected_files"]}
        assert "mesh_fps_hands_lowpoly.glb" in files

    def test_import_settings_present(self):
        imp = self.data.get("import_settings", {})
        assert "scale_factor" in imp
        assert "up_axis" in imp
        assert "import_animations" in imp


# ---------------------------------------------------------------------------
# default_character.character.json cross-reference
# ---------------------------------------------------------------------------

class TestDefaultCharacterUpdated:
    def setup_method(self):
        self.data = _load_json(
            "NovaForge/Data/Definitions/Characters/default_character.character.json")

    def test_references_placeholder_base(self):
        assert self.data.get("base_definition") == "placeholder_male_base"

    def test_references_rig_definition(self):
        assert self.data.get("rig_definition") == "placeholder_male_base_rig"

    def test_references_anim_map(self):
        assert self.data.get("anim_map") == "placeholder_male_base_anim_map"

    def test_has_eight_parts(self):
        assert len(self.data.get("parts", [])) == 8

    def test_all_eight_slots_covered(self):
        slots = {p["slot"] for p in self.data["parts"]}
        expected = {"Head", "Torso", "ArmLeft", "ArmRight", "LegLeft", "LegRight", "Hands", "Feet"}
        assert slots == expected

    def test_skeleton_id_present(self):
        assert self.data.get("skeleton_id") == "base_humanoid"


# ---------------------------------------------------------------------------
# .gitignore covers binary mesh files
# ---------------------------------------------------------------------------

class TestGitignoreCoversMeshes:
    def test_gitignore_excludes_glb(self):
        gitignore = _p(".gitignore").read_text(encoding="utf-8")
        assert ".glb" in gitignore

    def test_gitignore_excludes_fbx(self):
        gitignore = _p(".gitignore").read_text(encoding="utf-8")
        assert ".fbx" in gitignore

    def test_gitignore_preserves_asset_manifest(self):
        gitignore = _p(".gitignore").read_text(encoding="utf-8")
        assert "ASSET_MANIFEST.json" in gitignore
