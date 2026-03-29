"""Phase 28A — Tests for P13 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P13_TOOLS = [
    "SceneCompositorTool",
    "LightBakerTool",
    "VFXGraphTool",
    "DecalProjectorTool",
    "AudioReverbZoneTool",
    "CurveEditorTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP13ToolsExist(unittest.TestCase):
    def test_scene_compositor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SceneCompositorTool.h").exists())

    def test_light_baker_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "LightBakerTool.h").exists())

    def test_vfx_graph_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "VFXGraphTool.h").exists())

    def test_decal_projector_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "DecalProjectorTool.h").exists())

    def test_audio_reverb_zone_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AudioReverbZoneTool.h").exists())

    def test_curve_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "CurveEditorTool.h").exists())


class TestP13PragmaOnce(unittest.TestCase):
    def test_scene_compositor_pragma_once(self):
        self.assertIn("#pragma once", _read("SceneCompositorTool"))

    def test_light_baker_pragma_once(self):
        self.assertIn("#pragma once", _read("LightBakerTool"))

    def test_vfx_graph_pragma_once(self):
        self.assertIn("#pragma once", _read("VFXGraphTool"))

    def test_decal_projector_pragma_once(self):
        self.assertIn("#pragma once", _read("DecalProjectorTool"))

    def test_audio_reverb_zone_pragma_once(self):
        self.assertIn("#pragma once", _read("AudioReverbZoneTool"))

    def test_curve_editor_pragma_once(self):
        self.assertIn("#pragma once", _read("CurveEditorTool"))


class TestP13Inheritance(unittest.TestCase):
    def test_scene_compositor_inherits_itool(self):
        self.assertIn(": public ITool", _read("SceneCompositorTool"))

    def test_light_baker_inherits_itool(self):
        self.assertIn(": public ITool", _read("LightBakerTool"))

    def test_vfx_graph_inherits_itool(self):
        self.assertIn(": public ITool", _read("VFXGraphTool"))

    def test_decal_projector_inherits_itool(self):
        self.assertIn(": public ITool", _read("DecalProjectorTool"))

    def test_audio_reverb_zone_inherits_itool(self):
        self.assertIn(": public ITool", _read("AudioReverbZoneTool"))

    def test_curve_editor_inherits_itool(self):
        self.assertIn(": public ITool", _read("CurveEditorTool"))


class TestP13GetToolName(unittest.TestCase):
    def test_scene_compositor_get_tool_name(self):
        self.assertIn("GetToolName", _read("SceneCompositorTool"))
        self.assertIn('"SceneCompositorTool"', _read("SceneCompositorTool"))

    def test_light_baker_get_tool_name(self):
        self.assertIn("GetToolName", _read("LightBakerTool"))
        self.assertIn('"LightBakerTool"', _read("LightBakerTool"))

    def test_vfx_graph_get_tool_name(self):
        self.assertIn("GetToolName", _read("VFXGraphTool"))
        self.assertIn('"VFXGraphTool"', _read("VFXGraphTool"))

    def test_decal_projector_get_tool_name(self):
        self.assertIn("GetToolName", _read("DecalProjectorTool"))
        self.assertIn('"DecalProjectorTool"', _read("DecalProjectorTool"))

    def test_audio_reverb_zone_get_tool_name(self):
        self.assertIn("GetToolName", _read("AudioReverbZoneTool"))
        self.assertIn('"AudioReverbZoneTool"', _read("AudioReverbZoneTool"))

    def test_curve_editor_get_tool_name(self):
        self.assertIn("GetToolName", _read("CurveEditorTool"))
        self.assertIn('"CurveEditorTool"', _read("CurveEditorTool"))


class TestP13Namespace(unittest.TestCase):
    def test_scene_compositor_namespace(self):
        self.assertIn("Atlas::Editor", _read("SceneCompositorTool"))

    def test_light_baker_namespace(self):
        self.assertIn("Atlas::Editor", _read("LightBakerTool"))

    def test_vfx_graph_namespace(self):
        self.assertIn("Atlas::Editor", _read("VFXGraphTool"))

    def test_decal_projector_namespace(self):
        self.assertIn("Atlas::Editor", _read("DecalProjectorTool"))

    def test_audio_reverb_zone_namespace(self):
        self.assertIn("Atlas::Editor", _read("AudioReverbZoneTool"))

    def test_curve_editor_namespace(self):
        self.assertIn("Atlas::Editor", _read("CurveEditorTool"))


class TestP13SpecializedAPI(unittest.TestCase):
    def test_scene_compositor_blend_mode(self):
        content = _read("SceneCompositorTool")
        self.assertIn("BlendMode", content)
        self.assertIn("RenderTarget", content)

    def test_light_baker_bounce_count(self):
        content = _read("LightBakerTool")
        self.assertIn("BounceCount", content)
        self.assertIn("BakeQuality", content)

    def test_vfx_graph_emitter_type(self):
        content = _read("VFXGraphTool")
        self.assertIn("EmitterType", content)
        self.assertIn("ConnectNodes", content)

    def test_decal_projector_surface_mask(self):
        content = _read("DecalProjectorTool")
        self.assertIn("SurfaceMask", content)
        self.assertIn("ProjectionShape", content)

    def test_audio_reverb_zone_decay_time(self):
        content = _read("AudioReverbZoneTool")
        self.assertIn("DecayTime", content)
        self.assertIn("BlendRadius", content)

    def test_curve_editor_keyframe(self):
        content = _read("CurveEditorTool")
        self.assertIn("Keyframe", content)
        self.assertIn("InterpolationType", content)


if __name__ == "__main__":
    unittest.main()
