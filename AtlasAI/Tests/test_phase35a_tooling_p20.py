"""Phase 35A — Tests for P20 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P20_TOOLS = [
    "OnlineSubsystemTool",
    "ReplicationGraphTool",
    "ChaosCacheTool",
    "TextureCompressionTool",
    "CurveEditorTool",
    "ConversationGraphTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP20ToolsExist(unittest.TestCase):
    def test_online_subsystem_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "OnlineSubsystemTool.h").exists())

    def test_replication_graph_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ReplicationGraphTool.h").exists())

    def test_chaos_cache_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ChaosCacheTool.h").exists())

    def test_texture_compression_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "TextureCompressionTool.h").exists())

    def test_curve_editor_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "CurveEditorTool.h").exists())

    def test_conversation_graph_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ConversationGraphTool.h").exists())


class TestP20PragmaOnce(unittest.TestCase):
    def test_online_subsystem_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("OnlineSubsystemTool"))

    def test_replication_graph_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("ReplicationGraphTool"))

    def test_chaos_cache_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("ChaosCacheTool"))

    def test_texture_compression_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("TextureCompressionTool"))

    def test_curve_editor_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("CurveEditorTool"))

    def test_conversation_graph_tool_pragma_once(self):
        self.assertIn("#pragma once", _read("ConversationGraphTool"))


class TestP20ToolName(unittest.TestCase):
    def test_online_subsystem_tool_class_name(self):
        self.assertIn("OnlineSubsystemTool", _read("OnlineSubsystemTool"))

    def test_replication_graph_tool_class_name(self):
        self.assertIn("ReplicationGraphTool", _read("ReplicationGraphTool"))

    def test_chaos_cache_tool_class_name(self):
        self.assertIn("ChaosCacheTool", _read("ChaosCacheTool"))

    def test_texture_compression_tool_class_name(self):
        self.assertIn("TextureCompressionTool", _read("TextureCompressionTool"))

    def test_curve_editor_tool_class_name(self):
        self.assertIn("CurveEditorTool", _read("CurveEditorTool"))

    def test_conversation_graph_tool_class_name(self):
        self.assertIn("ConversationGraphTool", _read("ConversationGraphTool"))


class TestP20ITool(unittest.TestCase):
    def test_online_subsystem_tool_itool(self):
        self.assertIn(": public ITool", _read("OnlineSubsystemTool"))

    def test_replication_graph_tool_itool(self):
        self.assertIn(": public ITool", _read("ReplicationGraphTool"))

    def test_chaos_cache_tool_itool(self):
        self.assertIn(": public ITool", _read("ChaosCacheTool"))

    def test_texture_compression_tool_itool(self):
        self.assertIn(": public ITool", _read("TextureCompressionTool"))

    def test_curve_editor_tool_itool(self):
        self.assertIn(": public ITool", _read("CurveEditorTool"))

    def test_conversation_graph_tool_itool(self):
        self.assertIn(": public ITool", _read("ConversationGraphTool"))


class TestOnlineSubsystemToolDetail(unittest.TestCase):
    def test_session_state_enum(self):
        self.assertIn("SessionState", _read("OnlineSubsystemTool"))

    def test_lobby_config_struct(self):
        self.assertIn("LobbyConfig", _read("OnlineSubsystemTool"))

    def test_create_session_method(self):
        self.assertIn("CreateSession", _read("OnlineSubsystemTool"))

    def test_matchmaking_phase_enum(self):
        self.assertIn("MatchmakingPhase", _read("OnlineSubsystemTool"))


class TestReplicationGraphToolDetail(unittest.TestCase):
    def test_rep_node_type_enum(self):
        self.assertIn("RepNodeType", _read("ReplicationGraphTool"))

    def test_bandwidth_budget_def_struct(self):
        self.assertIn("BandwidthBudgetDef", _read("ReplicationGraphTool"))

    def test_create_rep_node_method(self):
        self.assertIn("CreateRepNode", _read("ReplicationGraphTool"))

    def test_set_max_bytes_per_second_method(self):
        self.assertIn("SetMaxBytesPerSecond", _read("ReplicationGraphTool"))


class TestChaosCacheToolDetail(unittest.TestCase):
    def test_cache_record_state_enum(self):
        self.assertIn("CacheRecordState", _read("ChaosCacheTool"))

    def test_cache_playback_config_struct(self):
        self.assertIn("CachePlaybackConfig", _read("ChaosCacheTool"))

    def test_start_recording_method(self):
        self.assertIn("StartRecording", _read("ChaosCacheTool"))

    def test_play_cache_method(self):
        self.assertIn("PlayCache", _read("ChaosCacheTool"))


class TestTextureCompressionToolDetail(unittest.TestCase):
    def test_compression_format_enum(self):
        self.assertIn("CompressionFormat", _read("TextureCompressionTool"))

    def test_mip_chain_config_struct(self):
        self.assertIn("MipChainConfig", _read("TextureCompressionTool"))

    def test_create_profile_method(self):
        self.assertIn("CreateProfile", _read("TextureCompressionTool"))

    def test_set_compression_format_method(self):
        self.assertIn("SetCompressionFormat", _read("TextureCompressionTool"))


class TestCurveEditorToolDetail(unittest.TestCase):
    def test_interpolation_mode_enum(self):
        self.assertIn("InterpolationMode", _read("CurveEditorTool"))

    def test_curve_track_def_struct(self):
        self.assertIn("CurveTrackDef", _read("CurveEditorTool"))

    def test_create_curve_asset_method(self):
        self.assertIn("CreateCurveAsset", _read("CurveEditorTool"))

    def test_evaluate_curve_method(self):
        self.assertIn("EvaluateCurve", _read("CurveEditorTool"))


class TestConversationGraphToolDetail(unittest.TestCase):
    def test_conv_node_type_enum(self):
        self.assertIn("ConvNodeType", _read("ConversationGraphTool"))

    def test_speaker_def_struct(self):
        self.assertIn("SpeakerDef", _read("ConversationGraphTool"))

    def test_create_graph_method(self):
        self.assertIn("CreateGraph", _read("ConversationGraphTool"))

    def test_add_node_method(self):
        self.assertIn("AddNode", _read("ConversationGraphTool"))


if __name__ == "__main__":
    unittest.main()
