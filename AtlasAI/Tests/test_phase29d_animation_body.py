"""Phase 29D — Tests for AnimationBodyRegistry.h and AnimationBodyLoader."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    AnimationBodyLoader,
    AnimationBodyManifest,
    AnimationClipDef,
    AnimationBlendWeightDef,
)

ANIM_REGISTRY_H = SCENE_DIR / "AnimationBodyRegistry.h"


def _read_registry() -> str:
    return ANIM_REGISTRY_H.read_text()


# ---------------------------------------------------------------------------
# AnimationBodyRegistry.h
# ---------------------------------------------------------------------------

class TestAnimationBodyRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(ANIM_REGISTRY_H.exists())


class TestAnimationBodyRegistryStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_registry())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_registry())

    def test_class_declaration(self):
        self.assertIn("AnimationBodyRegistry", _read_registry())

    def test_animation_body_state_enum(self):
        self.assertIn("AnimationBodyState", _read_registry())

    def test_animation_clip_type_enum(self):
        self.assertIn("AnimationClipType", _read_registry())

    def test_blend_space_enum(self):
        self.assertIn("BlendSpace", _read_registry())

    def test_animation_layer_enum(self):
        self.assertIn("AnimationLayer", _read_registry())

    def test_clip_bounds_struct(self):
        self.assertIn("ClipBounds", _read_registry())

    def test_blend_weights_struct(self):
        self.assertIn("BlendWeights", _read_registry())

    def test_animation_runtime_settings_struct(self):
        self.assertIn("AnimationRuntimeSettings", _read_registry())

    def test_animation_lod_settings_struct(self):
        self.assertIn("AnimationLODSettings", _read_registry())

    def test_animation_body_record_struct(self):
        self.assertIn("AnimationBodyRecord", _read_registry())

    def test_register_body(self):
        self.assertIn("RegisterBody", _read_registry())

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_registry())

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_registry())

    def test_set_body_position(self):
        self.assertIn("SetBodyPosition", _read_registry())

    def test_activate_body(self):
        self.assertIn("ActivateBody", _read_registry())

    def test_deactivate_body(self):
        self.assertIn("DeactivateBody", _read_registry())

    def test_play_body(self):
        self.assertIn("PlayBody", _read_registry())

    def test_get_all_body_ids(self):
        self.assertIn("GetAllBodyIds", _read_registry())

    def test_get_bodies_by_scene(self):
        self.assertIn("GetBodiesByScene", _read_registry())

    def test_get_bodies_by_layer(self):
        self.assertIn("GetBodiesByLayer", _read_registry())

    def test_get_bodies_by_state(self):
        self.assertIn("GetBodiesByState", _read_registry())

    def test_clear_method(self):
        self.assertIn("Clear()", _read_registry())

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_registry())

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_registry())

    def test_set_lod_settings(self):
        self.assertIn("SetLODSettings", _read_registry())

    def test_set_animation_speed(self):
        self.assertIn("SetAnimationSpeed", _read_registry())

    def test_functional_include(self):
        self.assertIn("<functional>", _read_registry())


# ---------------------------------------------------------------------------
# AnimationClipDef dataclass
# ---------------------------------------------------------------------------

class TestAnimationClipDefDataclass(unittest.TestCase):
    def test_clip_id(self):
        c = AnimationClipDef(clip_id="c001", name="Run")
        self.assertEqual(c.clip_id, "c001")

    def test_name(self):
        c = AnimationClipDef(clip_id="c001", name="Run")
        self.assertEqual(c.name, "Run")

    def test_default_clip_type(self):
        c = AnimationClipDef(clip_id="c001", name="Run")
        self.assertEqual(c.clip_type, "Skeletal")

    def test_default_duration(self):
        c = AnimationClipDef(clip_id="c001", name="Run")
        self.assertAlmostEqual(c.duration, 1.0)

    def test_is_looping_false(self):
        c = AnimationClipDef(clip_id="c001", name="Run")
        self.assertFalse(c.is_looping)

    def test_is_looping_true(self):
        c = AnimationClipDef(clip_id="c001", name="Run", loop=True)
        self.assertTrue(c.is_looping)

    def test_total_blend_time(self):
        c = AnimationClipDef(clip_id="c001", name="Run", blend_in=0.2, blend_out=0.3)
        self.assertAlmostEqual(c.total_blend_time, 0.5)


# ---------------------------------------------------------------------------
# AnimationBlendWeightDef dataclass
# ---------------------------------------------------------------------------

class TestAnimationBlendWeightDefDataclass(unittest.TestCase):
    def test_layer(self):
        bw = AnimationBlendWeightDef(layer="Base")
        self.assertEqual(bw.layer, "Base")

    def test_default_weight(self):
        bw = AnimationBlendWeightDef(layer="Base")
        self.assertAlmostEqual(bw.weight, 1.0)

    def test_is_additive_false(self):
        bw = AnimationBlendWeightDef(layer="Base")
        self.assertFalse(bw.is_additive)

    def test_is_additive_true(self):
        bw = AnimationBlendWeightDef(layer="Additive")
        self.assertTrue(bw.is_additive)

    def test_bone_count(self):
        bw = AnimationBlendWeightDef(layer="Override", mask_bones=["Spine", "Head"])
        self.assertEqual(bw.bone_count, 2)


# ---------------------------------------------------------------------------
# AnimationBodyManifest dataclass
# ---------------------------------------------------------------------------

class TestAnimationBodyManifestDataclass(unittest.TestCase):
    def test_body_id(self):
        m = AnimationBodyManifest(body_id="b001", name="Hero")
        self.assertEqual(m.body_id, "b001")

    def test_name(self):
        m = AnimationBodyManifest(body_id="b001", name="Hero")
        self.assertEqual(m.name, "Hero")

    def test_default_clip_type(self):
        m = AnimationBodyManifest(body_id="b001", name="Hero")
        self.assertEqual(m.clip_type, "Skeletal")

    def test_default_body_state(self):
        m = AnimationBodyManifest(body_id="b001", name="Hero")
        self.assertEqual(m.body_state, "Inactive")

    def test_is_playing_false(self):
        m = AnimationBodyManifest(body_id="b001", name="Hero")
        self.assertFalse(m.is_playing)

    def test_is_playing_true(self):
        m = AnimationBodyManifest(body_id="b001", name="Hero", body_state="Playing")
        self.assertTrue(m.is_playing)

    def test_has_clips_false(self):
        m = AnimationBodyManifest(body_id="b001", name="Hero")
        self.assertFalse(m.has_clips)

    def test_has_clips_true(self):
        c = AnimationClipDef(clip_id="c001", name="Run")
        m = AnimationBodyManifest(body_id="b001", name="Hero", clips=[c])
        self.assertTrue(m.has_clips)
        self.assertEqual(m.clip_count, 1)


# ---------------------------------------------------------------------------
# AnimationBodyLoader
# ---------------------------------------------------------------------------

class TestAnimationBodyLoaderBasic(unittest.TestCase):
    def setUp(self):
        self.loader = AnimationBodyLoader()

    def test_initial_count(self):
        self.assertEqual(self.loader.loaded_count, 0)

    def test_load_manifest(self):
        data = {"body_id": "b001", "name": "Hero"}
        m = self.loader.load_manifest(data)
        self.assertIsNotNone(m)
        self.assertEqual(m.name, "Hero")

    def test_loaded_count_after_load(self):
        self.loader.load_manifest({"body_id": "b001", "name": "Hero"})
        self.loader.load_manifest({"body_id": "b002", "name": "Mage"})
        self.assertEqual(self.loader.loaded_count, 2)

    def test_load_manifest_with_clip_type(self):
        data = {"body_id": "b001", "name": "Hero", "clip_type": "Morph"}
        m = self.loader.load_manifest(data)
        self.assertEqual(m.clip_type, "Morph")

    def test_load_manifest_with_body_state(self):
        data = {"body_id": "b001", "name": "Hero", "body_state": "Playing"}
        m = self.loader.load_manifest(data)
        self.assertTrue(m.is_playing)

    def test_load_manifest_with_position(self):
        data = {"body_id": "b001", "name": "Hero", "pos_x": 1.0, "pos_y": 2.0, "pos_z": 3.0}
        m = self.loader.load_manifest(data)
        self.assertAlmostEqual(m.pos_x, 1.0)
        self.assertAlmostEqual(m.pos_y, 2.0)
        self.assertAlmostEqual(m.pos_z, 3.0)

    def test_load_manifest_with_clips(self):
        data = {
            "body_id": "b001",
            "name": "Hero",
            "clips": [
                {"clip_id": "c001", "name": "Run", "loop": True},
                {"clip_id": "c002", "name": "Idle"},
            ],
        }
        m = self.loader.load_manifest(data)
        self.assertTrue(m.has_clips)
        self.assertEqual(m.clip_count, 2)

    def test_load_manifest_with_blend_weights(self):
        data = {
            "body_id": "b001",
            "name": "Hero",
            "blend_weights": [
                {"layer": "Additive", "weight": 0.5, "mask_bones": ["Spine"]},
            ],
        }
        m = self.loader.load_manifest(data)
        self.assertEqual(len(m.blend_weights), 1)
        self.assertTrue(m.blend_weights[0].is_additive)

    def test_clear(self):
        self.loader.load_manifest({"body_id": "b001", "name": "Hero"})
        self.loader.clear()
        self.assertEqual(self.loader.loaded_count, 0)


class TestAnimationBodyLoaderBatch(unittest.TestCase):
    def setUp(self):
        self.loader = AnimationBodyLoader()

    def test_load_batch(self):
        data_list = [
            {"body_id": "b001", "name": "Hero"},
            {"body_id": "b002", "name": "Villain"},
        ]
        results = self.loader.load_batch(data_list)
        self.assertEqual(len(results), 2)
        self.assertEqual(self.loader.loaded_count, 2)


class TestAnimationBodyLoaderValidate(unittest.TestCase):
    def setUp(self):
        self.loader = AnimationBodyLoader()

    def test_validate_valid(self):
        m = AnimationBodyManifest(body_id="b001", name="Hero")
        self.assertTrue(self.loader.validate(m))

    def test_validate_missing_body_id(self):
        m = AnimationBodyManifest(body_id="", name="Hero")
        self.assertFalse(self.loader.validate(m))

    def test_validate_missing_name(self):
        m = AnimationBodyManifest(body_id="b001", name="")
        self.assertFalse(self.loader.validate(m))


class TestAnimationBodyLoaderSaveLoad(unittest.TestCase):
    def setUp(self):
        self.loader = AnimationBodyLoader()

    def test_save_and_load_manifest(self):
        out = str(REPO_ROOT / "AtlasAI" / "Tests" / "_test_anim_manifest_p29d.json")
        m = AnimationBodyManifest(
            body_id="b001",
            name="Hero",
            clips=[AnimationClipDef(clip_id="c001", name="Run")],
        )
        self.loader.save_manifest(m, out)
        loaded = self.loader.load_from_file(out)
        self.assertEqual(loaded.body_id, "b001")
        self.assertEqual(loaded.clip_count, 1)
        Path(out).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
