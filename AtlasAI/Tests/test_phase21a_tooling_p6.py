"""Phase 21A — Tests for P6 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P6_TOOLS = [
    "SplinePathTool",
    "FoliagePainterTool",
    "ParticleSystemTool",
    "LightProbeVolumeTool",
    "CollisionEditorTool",
    "PrefabVariantTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP6ToolsExist(unittest.TestCase):
    def test_spline_path_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SplinePathTool.h").exists())

    def test_foliage_painter_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "FoliagePainterTool.h").exists())

    def test_particle_system_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ParticleSystemTool.h").exists())

    def test_light_probe_volume_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "LightProbeVolumeTool.h").exists())

    def test_collision_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "CollisionEditorTool.h").exists())

    def test_prefab_variant_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "PrefabVariantTool.h").exists())


class TestP6PragmaOnce(unittest.TestCase):
    def test_spline_path_pragma_once(self):
        self.assertIn("#pragma once", _read("SplinePathTool"))

    def test_foliage_painter_pragma_once(self):
        self.assertIn("#pragma once", _read("FoliagePainterTool"))

    def test_particle_system_pragma_once(self):
        self.assertIn("#pragma once", _read("ParticleSystemTool"))

    def test_light_probe_volume_pragma_once(self):
        self.assertIn("#pragma once", _read("LightProbeVolumeTool"))

    def test_collision_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("CollisionEditorTool"))

    def test_prefab_variant_pragma_once(self):
        self.assertIn("#pragma once", _read("PrefabVariantTool"))


class TestP6Inheritance(unittest.TestCase):
    def test_spline_path_inherits_itool(self):
        self.assertIn("ITool", _read("SplinePathTool"))

    def test_foliage_painter_inherits_itool(self):
        self.assertIn("ITool", _read("FoliagePainterTool"))

    def test_particle_system_inherits_itool(self):
        self.assertIn("ITool", _read("ParticleSystemTool"))

    def test_light_probe_volume_inherits_itool(self):
        self.assertIn("ITool", _read("LightProbeVolumeTool"))

    def test_collision_editor_inherits_itool(self):
        self.assertIn("ITool", _read("CollisionEditorTool"))

    def test_prefab_variant_inherits_itool(self):
        self.assertIn("ITool", _read("PrefabVariantTool"))


class TestP6GetToolName(unittest.TestCase):
    def test_spline_path_get_tool_name(self):
        self.assertIn('"SplinePathTool"', _read("SplinePathTool"))

    def test_foliage_painter_get_tool_name(self):
        self.assertIn('"FoliagePainterTool"', _read("FoliagePainterTool"))

    def test_particle_system_get_tool_name(self):
        self.assertIn('"ParticleSystemTool"', _read("ParticleSystemTool"))

    def test_light_probe_volume_get_tool_name(self):
        self.assertIn('"LightProbeVolumeTool"', _read("LightProbeVolumeTool"))

    def test_collision_editor_get_tool_name(self):
        self.assertIn('"CollisionEditorTool"', _read("CollisionEditorTool"))

    def test_prefab_variant_get_tool_name(self):
        self.assertIn('"PrefabVariantTool"', _read("PrefabVariantTool"))


class TestP6Namespace(unittest.TestCase):
    def test_spline_path_namespace(self):
        self.assertIn("Atlas::Editor", _read("SplinePathTool"))

    def test_foliage_painter_namespace(self):
        self.assertIn("Atlas::Editor", _read("FoliagePainterTool"))

    def test_particle_system_namespace(self):
        self.assertIn("Atlas::Editor", _read("ParticleSystemTool"))

    def test_light_probe_volume_namespace(self):
        self.assertIn("Atlas::Editor", _read("LightProbeVolumeTool"))

    def test_collision_editor_namespace(self):
        self.assertIn("Atlas::Editor", _read("CollisionEditorTool"))

    def test_prefab_variant_namespace(self):
        self.assertIn("Atlas::Editor", _read("PrefabVariantTool"))


class TestP6SpecializedAPI(unittest.TestCase):
    # SplinePathTool
    def test_spline_path_create_path(self):
        self.assertIn("CreatePath", _read("SplinePathTool"))

    def test_spline_path_add_node(self):
        self.assertIn("AddNode", _read("SplinePathTool"))

    def test_spline_path_type_enum(self):
        self.assertIn("SplineType", _read("SplinePathTool"))

    def test_spline_path_set_closed(self):
        self.assertIn("SetPathClosed", _read("SplinePathTool"))

    # FoliagePainterTool
    def test_foliage_painter_add_layer(self):
        self.assertIn("AddLayer", _read("FoliagePainterTool"))

    def test_foliage_painter_paint_area(self):
        self.assertIn("PaintArea", _read("FoliagePainterTool"))

    def test_foliage_painter_erase_area(self):
        self.assertIn("EraseArea", _read("FoliagePainterTool"))

    def test_foliage_painter_brush_struct(self):
        self.assertIn("FoliageBrush", _read("FoliagePainterTool"))

    # ParticleSystemTool
    def test_particle_system_place_emitter(self):
        self.assertIn("PlaceEmitter", _read("ParticleSystemTool"))

    def test_particle_system_emitter_shape_enum(self):
        self.assertIn("EmitterShape", _read("ParticleSystemTool"))

    def test_particle_system_play_emitter(self):
        self.assertIn("PlayEmitter", _read("ParticleSystemTool"))

    def test_particle_system_register_preset(self):
        self.assertIn("RegisterPreset", _read("ParticleSystemTool"))

    # LightProbeVolumeTool
    def test_light_probe_add_volume(self):
        self.assertIn("AddVolume", _read("LightProbeVolumeTool"))

    def test_light_probe_bake_volume(self):
        self.assertIn("BakeVolume", _read("LightProbeVolumeTool"))

    def test_light_probe_set_resolution(self):
        self.assertIn("SetResolution", _read("LightProbeVolumeTool"))

    def test_light_probe_bake_all(self):
        self.assertIn("BakeAll", _read("LightProbeVolumeTool"))

    # CollisionEditorTool
    def test_collision_editor_add_collider(self):
        self.assertIn("AddCollider", _read("CollisionEditorTool"))

    def test_collision_editor_collider_type_enum(self):
        self.assertIn("ColliderType", _read("CollisionEditorTool"))

    def test_collision_editor_set_trigger(self):
        self.assertIn("SetTrigger", _read("CollisionEditorTool"))

    def test_collision_editor_get_colliders_for_entity(self):
        self.assertIn("GetCollidersForEntity", _read("CollisionEditorTool"))

    # PrefabVariantTool
    def test_prefab_variant_create_variant(self):
        self.assertIn("CreateVariant", _read("PrefabVariantTool"))

    def test_prefab_variant_add_override(self):
        self.assertIn("AddOverride", _read("PrefabVariantTool"))

    def test_prefab_variant_struct(self):
        self.assertIn("PrefabVariant", _read("PrefabVariantTool"))

    def test_prefab_variant_get_variants_for_prefab(self):
        self.assertIn("GetVariantsForPrefab", _read("PrefabVariantTool"))


if __name__ == "__main__":
    unittest.main()
