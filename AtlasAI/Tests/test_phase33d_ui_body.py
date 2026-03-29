"""Phase 33D — Tests for UIBodyRegistry.h and UIBodyLoader."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCENE_DIR = REPO_ROOT / "Atlas" / "Engine" / "Scene"
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    UIBodyLoader,
    UIBodyManifest,
    UIStyleManifest,
    UILayoutManifest,
)

UI_REGISTRY_H = SCENE_DIR / "UIBodyRegistry.h"


def _read_registry() -> str:
    return UI_REGISTRY_H.read_text()


# ---------------------------------------------------------------------------
# UIBodyRegistry.h
# ---------------------------------------------------------------------------

class TestUIBodyRegistryExists(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(UI_REGISTRY_H.exists())


class TestUIBodyRegistryStructure(unittest.TestCase):
    def test_pragma_once(self):
        self.assertIn("#pragma once", _read_registry())

    def test_namespace(self):
        self.assertIn("Atlas::Engine", _read_registry())

    def test_class_declaration(self):
        self.assertIn("UIBodyRegistry", _read_registry())

    def test_ui_body_state_enum(self):
        self.assertIn("UIBodyState", _read_registry())

    def test_ui_body_type_enum(self):
        self.assertIn("UIBodyType", _read_registry())

    def test_ui_anchor_enum(self):
        self.assertIn("UIAnchor", _read_registry())

    def test_ui_scale_mode_enum(self):
        self.assertIn("UIScaleMode", _read_registry())

    def test_ui_update_mode_enum(self):
        self.assertIn("UIUpdateMode", _read_registry())

    def test_ui_style_def_struct(self):
        self.assertIn("UIStyleDef", _read_registry())

    def test_ui_layout_def_struct(self):
        self.assertIn("UILayoutDef", _read_registry())

    def test_ui_body_record_struct(self):
        self.assertIn("UIBodyRecord", _read_registry())

    def test_register_body(self):
        self.assertIn("RegisterBody", _read_registry())

    def test_unregister_body(self):
        self.assertIn("UnregisterBody", _read_registry())

    def test_set_body_state(self):
        self.assertIn("SetBodyState", _read_registry())

    def test_set_body_visible(self):
        self.assertIn("SetBodyVisible", _read_registry())

    def test_set_body_enabled(self):
        self.assertIn("SetBodyEnabled", _read_registry())

    def test_set_body_interactive(self):
        self.assertIn("SetBodyInteractive", _read_registry())

    def test_set_body_position(self):
        self.assertIn("SetBodyPosition", _read_registry())

    def test_set_body_size(self):
        self.assertIn("SetBodySize", _read_registry())

    def test_set_style_def(self):
        self.assertIn("SetStyleDef", _read_registry())

    def test_set_layout_def(self):
        self.assertIn("SetLayoutDef", _read_registry())

    def test_get_all_body_ids(self):
        self.assertIn("GetAllBodyIds", _read_registry())

    def test_get_bodies_by_type(self):
        self.assertIn("GetBodiesByType", _read_registry())

    def test_get_bodies_by_state(self):
        self.assertIn("GetBodiesByState", _read_registry())

    def test_get_visible_bodies(self):
        self.assertIn("GetVisibleBodies", _read_registry())

    def test_get_active_bodies(self):
        self.assertIn("GetActiveBodies", _read_registry())

    def test_clear_method(self):
        self.assertIn("Clear", _read_registry())

    def test_save_registry(self):
        self.assertIn("SaveRegistry", _read_registry())

    def test_load_registry(self):
        self.assertIn("LoadRegistry", _read_registry())


# ---------------------------------------------------------------------------
# UIStyleManifest
# ---------------------------------------------------------------------------

class TestUIStyleManifest(unittest.TestCase):
    def test_style_id(self):
        s = UIStyleManifest(style_id="s001")
        self.assertEqual(s.style_id, "s001")

    def test_default_font_family(self):
        s = UIStyleManifest(style_id="s001")
        self.assertEqual(s.font_family, "Arial")

    def test_default_font_size(self):
        s = UIStyleManifest(style_id="s001")
        self.assertEqual(s.font_size, 14)

    def test_has_border_true(self):
        s = UIStyleManifest(style_id="s001", border_width=1.0)
        self.assertTrue(s.has_border)

    def test_is_transparent_true(self):
        s = UIStyleManifest(style_id="s001", bg_a=0.8)
        self.assertTrue(s.is_transparent)


# ---------------------------------------------------------------------------
# UILayoutManifest
# ---------------------------------------------------------------------------

class TestUILayoutManifest(unittest.TestCase):
    def test_layout_id(self):
        l = UILayoutManifest(layout_id="l001")
        self.assertEqual(l.layout_id, "l001")

    def test_default_anchor(self):
        l = UILayoutManifest(layout_id="l001")
        self.assertEqual(l.anchor, "Center")

    def test_default_width(self):
        l = UILayoutManifest(layout_id="l001")
        self.assertAlmostEqual(l.width, 100.0)

    def test_is_centered_true(self):
        l = UILayoutManifest(layout_id="l001", anchor="Center")
        self.assertTrue(l.is_centered)

    def test_has_z_order_false(self):
        l = UILayoutManifest(layout_id="l001")
        self.assertFalse(l.has_z_order)


# ---------------------------------------------------------------------------
# UIBodyManifest
# ---------------------------------------------------------------------------

class TestUIBodyManifest(unittest.TestCase):
    def test_body_id(self):
        m = UIBodyManifest(body_id="b001", name="Health Bar")
        self.assertEqual(m.body_id, "b001")

    def test_name_field(self):
        m = UIBodyManifest(body_id="b001", name="Health Bar")
        self.assertEqual(m.name, "Health Bar")

    def test_default_ui_type(self):
        m = UIBodyManifest(body_id="b001", name="Health Bar")
        self.assertEqual(m.ui_type, "Widget")

    def test_is_visible_true(self):
        m = UIBodyManifest(body_id="b001", name="Health Bar", visible=True)
        self.assertTrue(m.is_visible)

    def test_is_interactive_true(self):
        m = UIBodyManifest(body_id="b001", name="Health Bar", interactive=True, enabled=True)
        self.assertTrue(m.is_interactive)

    def test_is_active_false(self):
        m = UIBodyManifest(body_id="b001", name="Health Bar", body_state="Hidden")
        self.assertFalse(m.is_active)


# ---------------------------------------------------------------------------
# UIBodyLoader
# ---------------------------------------------------------------------------

class TestUIBodyLoader(unittest.TestCase):
    def _loader(self):
        return UIBodyLoader()

    def test_load_manifest_returns_manifest(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "b001", "name": "Health Bar"})
        self.assertIsInstance(m, UIBodyManifest)

    def test_load_manifest_id(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "b001", "name": "Health Bar"})
        self.assertEqual(m.body_id, "b001")

    def test_load_manifest_name(self):
        loader = self._loader()
        m = loader.load_manifest({"body_id": "b001", "name": "Health Bar"})
        self.assertEqual(m.name, "Health Bar")

    def test_load_batch(self):
        loader = self._loader()
        batch = loader.load_batch([
            {"body_id": "b001", "name": "Health Bar"},
            {"body_id": "b002", "name": "Minimap"},
        ])
        self.assertEqual(len(batch), 2)

    def test_validate_valid_manifest(self):
        loader = self._loader()
        m = UIBodyManifest(body_id="b001", name="Health Bar")
        self.assertTrue(loader.validate(m))

    def test_validate_empty_name_fails(self):
        loader = self._loader()
        m = UIBodyManifest(body_id="b001", name="")
        self.assertFalse(loader.validate(m))

    def test_loaded_count_zero(self):
        loader = self._loader()
        self.assertEqual(loader.loaded_count, 0)

    def test_clear_resets(self):
        loader = self._loader()
        loader.load_manifest({"body_id": "b001", "name": "Health Bar"})
        loader.clear()
        self.assertEqual(loader.loaded_count, 0)

    def test_save_manifest_creates_file(self):
        loader = self._loader()
        m = UIBodyManifest(body_id="b001", name="Health Bar")
        save_path = REPO_ROOT / "AtlasAI" / "Tests" / "_test_ui_save_33d.json"
        try:
            loader.save_manifest(m, save_path)
            self.assertTrue(save_path.exists())
        finally:
            if save_path.exists():
                save_path.unlink()


if __name__ == "__main__":
    unittest.main()
