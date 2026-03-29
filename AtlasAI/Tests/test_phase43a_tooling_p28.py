"""Phase 43A — Tests for P28 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P28_TOOLS = [
    "SubsurfaceScatteringTool",
    "VectorFieldEditorTool",
    "TerrainLODTool",
    "SoundVisualizerTool",
    "BlueprintCommentTool",
    "MeshSocketEditorTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP28ToolsExist(unittest.TestCase):
    def test_subsurface_scattering_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SubsurfaceScatteringTool.h").exists())

    def test_vector_field_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "VectorFieldEditorTool.h").exists())

    def test_terrain_lod_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "TerrainLODTool.h").exists())

    def test_sound_visualizer_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "SoundVisualizerTool.h").exists())

    def test_blueprint_comment_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "BlueprintCommentTool.h").exists())

    def test_mesh_socket_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "MeshSocketEditorTool.h").exists())


class TestP28PragmaOnce(unittest.TestCase):
    def test_subsurface_scattering_tool_pragma(self):
        self.assertIn("#pragma once", _read("SubsurfaceScatteringTool"))

    def test_vector_field_editor_tool_pragma(self):
        self.assertIn("#pragma once", _read("VectorFieldEditorTool"))

    def test_terrain_lod_tool_pragma(self):
        self.assertIn("#pragma once", _read("TerrainLODTool"))

    def test_sound_visualizer_tool_pragma(self):
        self.assertIn("#pragma once", _read("SoundVisualizerTool"))

    def test_blueprint_comment_tool_pragma(self):
        self.assertIn("#pragma once", _read("BlueprintCommentTool"))

    def test_mesh_socket_editor_tool_pragma(self):
        self.assertIn("#pragma once", _read("MeshSocketEditorTool"))


class TestP28ToolNames(unittest.TestCase):
    def test_subsurface_scattering_tool_class_name(self):
        self.assertIn("SubsurfaceScatteringTool", _read("SubsurfaceScatteringTool"))

    def test_vector_field_editor_tool_class_name(self):
        self.assertIn("VectorFieldEditorTool", _read("VectorFieldEditorTool"))

    def test_terrain_lod_tool_class_name(self):
        self.assertIn("TerrainLODTool", _read("TerrainLODTool"))

    def test_sound_visualizer_tool_class_name(self):
        self.assertIn("SoundVisualizerTool", _read("SoundVisualizerTool"))

    def test_blueprint_comment_tool_class_name(self):
        self.assertIn("BlueprintCommentTool", _read("BlueprintCommentTool"))

    def test_mesh_socket_editor_tool_class_name(self):
        self.assertIn("MeshSocketEditorTool", _read("MeshSocketEditorTool"))


class TestP28ITool(unittest.TestCase):
    def test_subsurface_scattering_tool_itool(self):
        self.assertIn(": public ITool", _read("SubsurfaceScatteringTool"))

    def test_vector_field_editor_tool_itool(self):
        self.assertIn(": public ITool", _read("VectorFieldEditorTool"))

    def test_terrain_lod_tool_itool(self):
        self.assertIn(": public ITool", _read("TerrainLODTool"))

    def test_sound_visualizer_tool_itool(self):
        self.assertIn(": public ITool", _read("SoundVisualizerTool"))

    def test_blueprint_comment_tool_itool(self):
        self.assertIn(": public ITool", _read("BlueprintCommentTool"))

    def test_mesh_socket_editor_tool_itool(self):
        self.assertIn(": public ITool", _read("MeshSocketEditorTool"))


class TestSubsurfaceScatteringToolDetail(unittest.TestCase):
    def test_scatter_model_enum(self):
        self.assertIn("ScatterModel", _read("SubsurfaceScatteringTool"))

    def test_transmission_mode_enum(self):
        self.assertIn("TransmissionMode", _read("SubsurfaceScatteringTool"))

    def test_sss_channel_enum(self):
        self.assertIn("SSSChannel", _read("SubsurfaceScatteringTool"))

    def test_profile_quality_enum(self):
        self.assertIn("ProfileQuality", _read("SubsurfaceScatteringTool"))

    def test_sss_profile_def_struct(self):
        self.assertIn("SSSProfileDef", _read("SubsurfaceScatteringTool"))

    def test_transmission_profile_def_struct(self):
        self.assertIn("TransmissionProfileDef", _read("SubsurfaceScatteringTool"))

    def test_sss_kernel_def_struct(self):
        self.assertIn("SSSKernelDef", _read("SubsurfaceScatteringTool"))

    def test_create_profile_method(self):
        self.assertIn("CreateProfile", _read("SubsurfaceScatteringTool"))

    def test_add_transmission_method(self):
        self.assertIn("AddTransmission", _read("SubsurfaceScatteringTool"))

    def test_add_kernel_method(self):
        self.assertIn("AddKernel", _read("SubsurfaceScatteringTool"))

    def test_burley_scatter_model(self):
        self.assertIn("Burley", _read("SubsurfaceScatteringTool"))


class TestVectorFieldEditorToolDetail(unittest.TestCase):
    def test_field_type_enum(self):
        self.assertIn("FieldType", _read("VectorFieldEditorTool"))

    def test_field_dimension_enum(self):
        self.assertIn("FieldDimension", _read("VectorFieldEditorTool"))

    def test_voxel_data_type_enum(self):
        self.assertIn("VoxelDataType", _read("VectorFieldEditorTool"))

    def test_particle_coupling_enum(self):
        self.assertIn("ParticleCoupling", _read("VectorFieldEditorTool"))

    def test_vector_field_def_struct(self):
        self.assertIn("VectorFieldDef", _read("VectorFieldEditorTool"))

    def test_flow_visualization_def_struct(self):
        self.assertIn("FlowVisualizationDef", _read("VectorFieldEditorTool"))

    def test_particle_coupling_def_struct(self):
        self.assertIn("ParticleCouplingDef", _read("VectorFieldEditorTool"))

    def test_create_field_method(self):
        self.assertIn("CreateField", _read("VectorFieldEditorTool"))

    def test_add_visualization_method(self):
        self.assertIn("AddVisualization", _read("VectorFieldEditorTool"))

    def test_add_coupling_method(self):
        self.assertIn("AddCoupling", _read("VectorFieldEditorTool"))

    def test_vortex_type(self):
        self.assertIn("Vortex", _read("VectorFieldEditorTool"))


class TestTerrainLODToolDetail(unittest.TestCase):
    def test_lod_method_enum(self):
        self.assertIn("LODMethod", _read("TerrainLODTool"))

    def test_tessellation_mode_enum(self):
        self.assertIn("TessellationMode", _read("TerrainLODTool"))

    def test_heightmap_quality_enum(self):
        self.assertIn("HeightmapQuality", _read("TerrainLODTool"))

    def test_transition_type_enum(self):
        self.assertIn("TransitionType", _read("TerrainLODTool"))

    def test_terrain_lod_group_def_struct(self):
        self.assertIn("TerrainLODGroupDef", _read("TerrainLODTool"))

    def test_lod_level_def_struct(self):
        self.assertIn("LODLevelDef", _read("TerrainLODTool"))

    def test_tess_config_def_struct(self):
        self.assertIn("TessConfigDef", _read("TerrainLODTool"))

    def test_create_lod_group_method(self):
        self.assertIn("CreateLODGroup", _read("TerrainLODTool"))

    def test_add_lod_level_method(self):
        self.assertIn("AddLODLevel", _read("TerrainLODTool"))

    def test_set_tess_config_method(self):
        self.assertIn("SetTessConfig", _read("TerrainLODTool"))

    def test_screen_size_lod_method(self):
        self.assertIn("ScreenSize", _read("TerrainLODTool"))


class TestSoundVisualizerToolDetail(unittest.TestCase):
    def test_vis_mode_enum(self):
        self.assertIn("VisMode", _read("SoundVisualizerTool"))

    def test_freq_scale_enum(self):
        self.assertIn("FreqScale", _read("SoundVisualizerTool"))

    def test_window_function_enum(self):
        self.assertIn("WindowFunction", _read("SoundVisualizerTool"))

    def test_overlay_type_enum(self):
        self.assertIn("OverlayType", _read("SoundVisualizerTool"))

    def test_waveform_vis_def_struct(self):
        self.assertIn("WaveformVisDef", _read("SoundVisualizerTool"))

    def test_spectrum_analyzer_def_struct(self):
        self.assertIn("SpectrumAnalyzerDef", _read("SoundVisualizerTool"))

    def test_audio_overlay_def_struct(self):
        self.assertIn("AudioOverlayDef", _read("SoundVisualizerTool"))

    def test_create_waveform_vis_method(self):
        self.assertIn("CreateWaveformVis", _read("SoundVisualizerTool"))

    def test_add_spectrum_analyzer_method(self):
        self.assertIn("AddSpectrumAnalyzer", _read("SoundVisualizerTool"))

    def test_add_overlay_method(self):
        self.assertIn("AddOverlay", _read("SoundVisualizerTool"))

    def test_waterfall_vis_mode(self):
        self.assertIn("Waterfall", _read("SoundVisualizerTool"))


class TestBlueprintCommentToolDetail(unittest.TestCase):
    def test_comment_type_enum(self):
        self.assertIn("CommentType", _read("BlueprintCommentTool"))

    def test_comment_color_enum(self):
        self.assertIn("CommentColor", _read("BlueprintCommentTool"))

    def test_comment_style_enum(self):
        self.assertIn("CommentStyle", _read("BlueprintCommentTool"))

    def test_comment_scope_enum(self):
        self.assertIn("CommentScope", _read("BlueprintCommentTool"))

    def test_comment_block_def_struct(self):
        self.assertIn("CommentBlockDef", _read("BlueprintCommentTool"))

    def test_comment_group_def_struct(self):
        self.assertIn("CommentGroupDef", _read("BlueprintCommentTool"))

    def test_doc_annotation_def_struct(self):
        self.assertIn("DocAnnotationDef", _read("BlueprintCommentTool"))

    def test_create_comment_method(self):
        self.assertIn("CreateComment", _read("BlueprintCommentTool"))

    def test_create_group_method(self):
        self.assertIn("CreateGroup", _read("BlueprintCommentTool"))

    def test_add_doc_annotation_method(self):
        self.assertIn("AddDocAnnotation", _read("BlueprintCommentTool"))

    def test_todo_comment_type(self):
        self.assertIn("Todo", _read("BlueprintCommentTool"))


class TestMeshSocketEditorToolDetail(unittest.TestCase):
    def test_socket_type_enum(self):
        self.assertIn("SocketType", _read("MeshSocketEditorTool"))

    def test_socket_space_enum(self):
        self.assertIn("SocketSpace", _read("MeshSocketEditorTool"))

    def test_preview_mode_enum(self):
        self.assertIn("PreviewMode", _read("MeshSocketEditorTool"))

    def test_socket_visibility_enum(self):
        self.assertIn("SocketVisibility", _read("MeshSocketEditorTool"))

    def test_socket_def_struct(self):
        self.assertIn("SocketDef", _read("MeshSocketEditorTool"))

    def test_preview_attachment_def_struct(self):
        self.assertIn("PreviewAttachmentDef", _read("MeshSocketEditorTool"))

    def test_socket_constraint_def_struct(self):
        self.assertIn("SocketConstraintDef", _read("MeshSocketEditorTool"))

    def test_create_socket_method(self):
        self.assertIn("CreateSocket", _read("MeshSocketEditorTool"))

    def test_add_preview_attachment_method(self):
        self.assertIn("AddPreviewAttachment", _read("MeshSocketEditorTool"))

    def test_add_constraint_method(self):
        self.assertIn("AddConstraint", _read("MeshSocketEditorTool"))

    def test_move_socket_method(self):
        self.assertIn("MoveSocket", _read("MeshSocketEditorTool"))


if __name__ == "__main__":
    unittest.main()
