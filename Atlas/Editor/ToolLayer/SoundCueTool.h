#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P22 Tool — Sound cue node graph editor and audio routing.
class SoundCueTool : public ITool {
public:
    enum class SoundCueNodeType { Wave, Mixer, Modulator, Looping, Random, Delay, Oscillator, Custom };
    enum class AudioBusRouting { Master, Music, SFX, Voice, Ambient, Reverb, Custom };
    enum class MixerGroupType { Stereo, Mono, Surround, Binaural, Spatial, Custom };
    enum class AttenuationShape { Sphere, Capsule, Box, Cone, Custom };

    struct SoundCueNodeDef {
        std::string nodeId;
        std::string cueId;
        SoundCueNodeType nodeType{SoundCueNodeType::Wave};
        std::string assetRef;
        float volume{1.0f};
        float pitch{1.0f};
        float startTime{0.0f};
        bool looping{false};
    };

    struct SoundCueEdgeDef {
        std::string edgeId;
        std::string srcNodeId;
        std::string dstNodeId;
        std::string cueId;
        int srcPinIndex{0};
        int dstPinIndex{0};
        bool enabled{true};
    };

    struct SoundCueDef {
        std::string cueId;
        std::string name;
        AudioBusRouting routing{AudioBusRouting::SFX};
        MixerGroupType mixerGroup{MixerGroupType::Stereo};
        AttenuationShape attenuationShape{AttenuationShape::Sphere};
        float attenuationRadius{1200.0f};
        float volume{1.0f};
        bool spatialize{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SoundCueTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateSoundCue(const SoundCueDef& def);
    bool DeleteSoundCue(const std::string& cueId);
    const SoundCueDef* GetSoundCue(const std::string& cueId) const;
    std::vector<std::string> GetAllCueIds() const;

    std::string AddNode(const SoundCueNodeDef& node);
    bool RemoveNode(const std::string& nodeId);
    const SoundCueNodeDef* GetNode(const std::string& nodeId) const;
    std::vector<std::string> GetNodesForCue(const std::string& cueId) const;

    std::string AddEdge(const SoundCueEdgeDef& edge);
    bool RemoveEdge(const std::string& edgeId);
    std::vector<SoundCueEdgeDef> GetEdgesForCue(const std::string& cueId) const;

    bool SetRouting(const std::string& cueId, AudioBusRouting routing);
    std::vector<std::string> GetCuesByNodeType(SoundCueNodeType nodeType) const;
    bool SetAttenuationShape(const std::string& cueId, AttenuationShape shape);

    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, SoundCueDef> m_soundCues;
    std::unordered_map<std::string, SoundCueNodeDef> m_nodes;
    std::unordered_map<std::string, SoundCueEdgeDef> m_edges;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
