"""Phase 24A — Tests for P9 ToolLayer headers."""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_LAYER = REPO_ROOT / "Atlas" / "Editor" / "ToolLayer"

P9_TOOLS = [
    "PostProcessVolumeTool",
    "TimelineSequencerTool",
    "BlueprintDebuggerTool",
    "AudioMixerTool",
    "FluidSimulationTool",
    "ProceduralAnimationTool",
]


def _read(name: str) -> str:
    return (TOOL_LAYER / f"{name}.h").read_text()


class TestP9ToolsExist(unittest.TestCase):
    def test_post_process_volume_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "PostProcessVolumeTool.h").exists())

    def test_timeline_sequencer_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "TimelineSequencerTool.h").exists())

    def test_blueprint_debugger_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "BlueprintDebuggerTool.h").exists())

    def test_audio_mixer_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "AudioMixerTool.h").exists())

    def test_fluid_simulation_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "FluidSimulationTool.h").exists())

    def test_procedural_animation_tool_exists(self):
        self.assertTrue((TOOL_LAYER / "ProceduralAnimationTool.h").exists())


class TestP9PragmaOnce(unittest.TestCase):
    def test_post_process_volume_pragma_once(self):
        self.assertIn("#pragma once", _read("PostProcessVolumeTool"))

    def test_timeline_sequencer_pragma_once(self):
        self.assertIn("#pragma once", _read("TimelineSequencerTool"))

    def test_blueprint_debugger_pragma_once(self):
        self.assertIn("#pragma once", _read("BlueprintDebuggerTool"))

    def test_audio_mixer_pragma_once(self):
        self.assertIn("#pragma once", _read("AudioMixerTool"))

    def test_fluid_simulation_pragma_once(self):
        self.assertIn("#pragma once", _read("FluidSimulationTool"))

    def test_procedural_animation_pragma_once(self):
        self.assertIn("#pragma once", _read("ProceduralAnimationTool"))


class TestP9Inheritance(unittest.TestCase):
    def test_post_process_volume_inherits_itool(self):
        self.assertIn("ITool", _read("PostProcessVolumeTool"))

    def test_timeline_sequencer_inherits_itool(self):
        self.assertIn("ITool", _read("TimelineSequencerTool"))

    def test_blueprint_debugger_inherits_itool(self):
        self.assertIn("ITool", _read("BlueprintDebuggerTool"))

    def test_audio_mixer_inherits_itool(self):
        self.assertIn("ITool", _read("AudioMixerTool"))

    def test_fluid_simulation_inherits_itool(self):
        self.assertIn("ITool", _read("FluidSimulationTool"))

    def test_procedural_animation_inherits_itool(self):
        self.assertIn("ITool", _read("ProceduralAnimationTool"))


class TestP9GetToolName(unittest.TestCase):
    def test_post_process_volume_get_tool_name(self):
        self.assertIn('"PostProcessVolumeTool"', _read("PostProcessVolumeTool"))

    def test_timeline_sequencer_get_tool_name(self):
        self.assertIn('"TimelineSequencerTool"', _read("TimelineSequencerTool"))

    def test_blueprint_debugger_get_tool_name(self):
        self.assertIn('"BlueprintDebuggerTool"', _read("BlueprintDebuggerTool"))

    def test_audio_mixer_get_tool_name(self):
        self.assertIn('"AudioMixerTool"', _read("AudioMixerTool"))

    def test_fluid_simulation_get_tool_name(self):
        self.assertIn('"FluidSimulationTool"', _read("FluidSimulationTool"))

    def test_procedural_animation_get_tool_name(self):
        self.assertIn('"ProceduralAnimationTool"', _read("ProceduralAnimationTool"))


class TestP9Namespace(unittest.TestCase):
    def test_post_process_volume_namespace(self):
        self.assertIn("Atlas::Editor", _read("PostProcessVolumeTool"))

    def test_timeline_sequencer_namespace(self):
        self.assertIn("Atlas::Editor", _read("TimelineSequencerTool"))

    def test_blueprint_debugger_namespace(self):
        self.assertIn("Atlas::Editor", _read("BlueprintDebuggerTool"))

    def test_audio_mixer_namespace(self):
        self.assertIn("Atlas::Editor", _read("AudioMixerTool"))

    def test_fluid_simulation_namespace(self):
        self.assertIn("Atlas::Editor", _read("FluidSimulationTool"))

    def test_procedural_animation_namespace(self):
        self.assertIn("Atlas::Editor", _read("ProceduralAnimationTool"))


class TestP9SpecializedAPI(unittest.TestCase):
    # PostProcessVolumeTool
    def test_post_process_create_volume(self):
        self.assertIn("CreateVolume", _read("PostProcessVolumeTool"))

    def test_post_process_volume_shape_enum(self):
        self.assertIn("VolumeShape", _read("PostProcessVolumeTool"))

    def test_post_process_add_effect(self):
        self.assertIn("AddEffect", _read("PostProcessVolumeTool"))

    def test_post_process_effect_type_enum(self):
        self.assertIn("EffectType", _read("PostProcessVolumeTool"))

    def test_post_process_query_point(self):
        self.assertIn("QueryPoint", _read("PostProcessVolumeTool"))

    def test_post_process_volume_struct(self):
        self.assertIn("PostProcessVolume", _read("PostProcessVolumeTool"))

    # TimelineSequencerTool
    def test_timeline_create_sequence(self):
        self.assertIn("CreateSequence", _read("TimelineSequencerTool"))

    def test_timeline_add_track(self):
        self.assertIn("AddTrack", _read("TimelineSequencerTool"))

    def test_timeline_add_keyframe(self):
        self.assertIn("AddKeyframe", _read("TimelineSequencerTool"))

    def test_timeline_track_type_enum(self):
        self.assertIn("TrackType", _read("TimelineSequencerTool"))

    def test_timeline_interpolation_type_enum(self):
        self.assertIn("InterpolationType", _read("TimelineSequencerTool"))

    def test_timeline_playback_state_enum(self):
        self.assertIn("PlaybackState", _read("TimelineSequencerTool"))

    def test_timeline_scrub(self):
        self.assertIn("Scrub", _read("TimelineSequencerTool"))

    # BlueprintDebuggerTool
    def test_blueprint_debugger_attach_graph(self):
        self.assertIn("AttachGraph", _read("BlueprintDebuggerTool"))

    def test_blueprint_debugger_add_breakpoint(self):
        self.assertIn("AddBreakpoint", _read("BlueprintDebuggerTool"))

    def test_blueprint_debugger_breakpoint_type_enum(self):
        self.assertIn("BreakpointType", _read("BlueprintDebuggerTool"))

    def test_blueprint_debugger_step_over(self):
        self.assertIn("StepOver", _read("BlueprintDebuggerTool"))

    def test_blueprint_debugger_watch_variable(self):
        self.assertIn("AddWatchVariable", _read("BlueprintDebuggerTool"))

    def test_blueprint_debugger_node_execution_state(self):
        self.assertIn("NodeExecutionState", _read("BlueprintDebuggerTool"))

    # AudioMixerTool
    def test_audio_mixer_create_bus(self):
        self.assertIn("CreateBus", _read("AudioMixerTool"))

    def test_audio_mixer_bus_type_enum(self):
        self.assertIn("BusType", _read("AudioMixerTool"))

    def test_audio_mixer_set_bus_volume(self):
        self.assertIn("SetBusVolume", _read("AudioMixerTool"))

    def test_audio_mixer_add_send(self):
        self.assertIn("AddSend", _read("AudioMixerTool"))

    def test_audio_mixer_add_effect(self):
        self.assertIn("AddEffect", _read("AudioMixerTool"))

    def test_audio_mixer_effect_slot_type_enum(self):
        self.assertIn("EffectSlotType", _read("AudioMixerTool"))

    # FluidSimulationTool
    def test_fluid_create_domain(self):
        self.assertIn("CreateDomain", _read("FluidSimulationTool"))

    def test_fluid_fluid_type_enum(self):
        self.assertIn("FluidType", _read("FluidSimulationTool"))

    def test_fluid_solver_type_enum(self):
        self.assertIn("SolverType", _read("FluidSimulationTool"))

    def test_fluid_create_emitter(self):
        self.assertIn("CreateEmitter", _read("FluidSimulationTool"))

    def test_fluid_bake_domain(self):
        self.assertIn("BakeDomain", _read("FluidSimulationTool"))

    def test_fluid_domain_struct(self):
        self.assertIn("FluidDomain", _read("FluidSimulationTool"))

    # ProceduralAnimationTool
    def test_procedural_anim_create_rule(self):
        self.assertIn("CreateRule", _read("ProceduralAnimationTool"))

    def test_procedural_anim_rule_type_enum(self):
        self.assertIn("RuleType", _read("ProceduralAnimationTool"))

    def test_procedural_anim_solver_algorithm_enum(self):
        self.assertIn("SolverAlgorithm", _read("ProceduralAnimationTool"))

    def test_procedural_anim_create_ik_target(self):
        self.assertIn("CreateIKTarget", _read("ProceduralAnimationTool"))

    def test_procedural_anim_create_layer(self):
        self.assertIn("CreateLayer", _read("ProceduralAnimationTool"))

    def test_procedural_anim_rule_struct(self):
        self.assertIn("ProceduralRule", _read("ProceduralAnimationTool"))


if __name__ == "__main__":
    unittest.main()
