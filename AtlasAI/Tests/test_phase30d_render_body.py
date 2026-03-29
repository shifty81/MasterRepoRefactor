"""Phase 30D — Tests for RenderBodyRegistry.h and RenderBodyLoader."""
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    RenderBodyLoader,
    RenderBodyManifest,
    MaterialSlotDef,
    LODEntryDef,
)

RENDER_REGISTRY_H = SCENE_DIR / "RenderBodyRegistry.h"


def _read_registry() -> str:
    return RENDER_REGISTRY_H.read_text()


# ---------------------------------------------------------------------------
# RenderBodyRegistry.h
# ---------------------------------------------------------------------------

class TestRenderBodyRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(RENDER_REGISTRY_H.exists())


class TestRenderBodyRegistryStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_registry())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_registry())

    def test_class_declaration(self):
        self.assertIn("RenderBodyRegistry", _read_registry())

    def test_render_body_state_enum(self):
        self.assertIn("RenderBodyState", _read_registry())

    def test_mesh_primitive_enum(self):
        self.assertIn("MeshPrimitive", _read_registry())

    def test_render_layer_enum(self):
        self.assertIn("RenderLayer", _read_registry())

    def test_shading_model_enum(self):
        self.assertIn("ShadingModel", _read_registry())

    def test_cull_mode_enum(self):
        self.assertIn("CullMode", _read_registry())

    def test_material_slot_struct(self):
        self.assertIn("MaterialSlot", _read_registry())

    def test_lod_entry_struct(self):
        self.assertIn("LODEntry", _read_registry())

    def test_bounds_info_struct(self):
        self.assertIn("BoundsInfo", _read_registry())

    def test_render_flags_struct(self):
        self.assertIn("RenderFlags", _read_registry())

    def test_render_body_record_struct(self):
        self.assertIn("RenderBodyRecord", _read_registry())

    def test_register_body(self):
        self.assertIn("RegisterBody", _read_registry())

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_registry())

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_registry())

    def test_set_body_position(self):
        self.assertIn("SetBodyPosition", _read_registry())

    def test_set_body_visible(self):
        self.assertIn("SetBodyVisible", _read_registry())

    def test_get_all_body_ids(self):
        self.assertIn("GetAllBodyIds", _read_registry())

    def test_get_bodies_by_layer(self):
        self.assertIn("GetBodiesByLayer", _read_registry())

    def test_get_bodies_by_state(self):
        self.assertIn("GetBodiesByState", _read_registry())

    def test_get_visible_bodies(self):
        self.assertIn("GetVisibleBodies", _read_registry())

    def test_clear_method(self):
        self.assertIn("Clear()", _read_registry())

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_registry())

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_registry())

    def test_set_bounds(self):
        self.assertIn("SetBounds", _read_registry())

    def test_functional_include(self):
        self.assertIn("<functional>", _read_registry())


# ---------------------------------------------------------------------------
# MaterialSlotDef
# ---------------------------------------------------------------------------

class TestMaterialSlotDef(unittest.TestCase):
    def test_default_slot_index(self):
        s = MaterialSlotDef()
        self.assertEqual(s.slot_index, 0)

    def test_default_material_path(self):
        s = MaterialSlotDef()
        self.assertEqual(s.material_path, "")

    def test_has_material_false(self):
        s = MaterialSlotDef()
        self.assertFalse(s.has_material)

    def test_override_count_zero(self):
        s = MaterialSlotDef()
        self.assertEqual(s.override_count, 0)


# ---------------------------------------------------------------------------
# LODEntryDef
# ---------------------------------------------------------------------------

class TestLODEntryDef(unittest.TestCase):
    def test_default_lod_level(self):
        l = LODEntryDef()
        self.assertEqual(l.lod_level, 0)

    def test_default_mesh_path(self):
        l = LODEntryDef()
        self.assertEqual(l.mesh_path, "")

    def test_default_screen_size_threshold(self):
        l = LODEntryDef()
        self.assertAlmostEqual(l.screen_size_threshold, 1.0)

    def test_is_highest_lod_true(self):
        l = LODEntryDef(lod_level=0)
        self.assertTrue(l.is_highest_lod)


# ---------------------------------------------------------------------------
# RenderBodyManifest
# ---------------------------------------------------------------------------

class TestRenderBodyManifest(unittest.TestCase):
    def test_body_id(self):
        m = RenderBodyManifest(body_id="b001", name="Rock")
        self.assertEqual(m.body_id, "b001")

    def test_name_field(self):
        m = RenderBodyManifest(body_id="b001", name="Rock")
        self.assertEqual(m.name, "Rock")

    def test_default_mesh_path(self):
        m = RenderBodyManifest(body_id="b001", name="Rock")
        self.assertEqual(m.mesh_path, "")

    def test_default_primitive(self):
        m = RenderBodyManifest(body_id="b001", name="Rock")
        self.assertEqual(m.primitive, "Triangle")

    def test_default_render_layer(self):
        m = RenderBodyManifest(body_id="b001", name="Rock")
        self.assertEqual(m.render_layer, "World")

    def test_default_visible(self):
        m = RenderBodyManifest(body_id="b001", name="Rock")
        self.assertTrue(m.visible)

    def test_is_visible_true(self):
        m = RenderBodyManifest(body_id="b001", name="Rock")
        self.assertTrue(m.is_visible)

    def test_has_lods_false(self):
        m = RenderBodyManifest(body_id="b001", name="Rock")
        self.assertFalse(m.has_lods)

    def test_lod_count_zero(self):
        m = RenderBodyManifest(body_id="b001", name="Rock")
        self.assertEqual(m.lod_count, 0)

    def test_material_count_zero(self):
        m = RenderBodyManifest(body_id="b001", name="Rock")
        self.assertEqual(m.material_count, 0)


# ---------------------------------------------------------------------------
# RenderBodyLoader
# ---------------------------------------------------------------------------

class TestRenderBodyLoader(unittest.TestCase):
    def setUp(self):
        self.loader = RenderBodyLoader()

    def test_load_manifest_returns_manifest(self):
        data = {"body_id": "b001", "name": "Rock"}
        m = self.loader.load_manifest(data)
        self.assertIsInstance(m, RenderBodyManifest)

    def test_load_manifest_id(self):
        data = {"body_id": "b001", "name": "Rock"}
        m = self.loader.load_manifest(data)
        self.assertEqual(m.body_id, "b001")

    def test_load_manifest_name(self):
        data = {"body_id": "b001", "name": "Rock"}
        m = self.loader.load_manifest(data)
        self.assertEqual(m.name, "Rock")

    def test_load_batch(self):
        data_list = [
            {"body_id": "b001", "name": "Rock"},
            {"body_id": "b002", "name": "Tree"},
        ]
        results = self.loader.load_batch(data_list)
        self.assertEqual(len(results), 2)
        self.assertEqual(self.loader.loaded_count, 2)

    def test_validate_valid_manifest(self):
        m = RenderBodyManifest(body_id="b001", name="Rock")
        self.assertTrue(self.loader.validate(m))

    def test_validate_empty_name_fails(self):
        m = RenderBodyManifest(body_id="b001", name="")
        self.assertFalse(self.loader.validate(m))

    def test_loaded_count_zero(self):
        self.assertEqual(self.loader.loaded_count, 0)

    def test_clear_resets(self):
        self.loader.load_manifest({"body_id": "b001", "name": "Rock"})
        self.loader.clear()
        self.assertEqual(self.loader.loaded_count, 0)

    def test_save_manifest_creates_file(self):
        out = REPO_ROOT / "AtlasAI" / "Tests" / "_test_render_body_p30d.json"
        m = RenderBodyManifest(body_id="b001", name="Rock")
        self.loader.save_manifest(m, out)
        self.assertTrue(out.exists())
        loaded = self.loader.load_from_file(out)
        self.assertEqual(loaded.body_id, "b001")
        out.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
