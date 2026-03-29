#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P19 Tool — MetaSound source authoring, graph node configuration, and audio parameter management.
class MetaSoundTool : public ITool {
public:
    enum class MetaSoundNodeType { Input, Output, Generator, Effect, Modulator, Trigger, Variable, Comment };
    enum class AudioParameterType { Bool, Int, Float, String, Object, Trigger, AudioBuffer };
    enum class WaveformType { Sine, Square, Triangle, Saw, Noise, Custom };

    struct MetaSoundNodeDef {
        std::string nodeId;
        std::string name;
        MetaSoundNodeType nodeType{MetaSoundNodeType::Generator};
        std::vector<std::string> inputs;
        std::vector<std::string> outputs;
        std::string category;
        std::string description;
    };

    struct AudioParameterDef {
        std::string paramId;
        std::string name;
        AudioParameterType paramType{AudioParameterType::Float};
        std::string defaultValue;
        float minValue{0.0f};
        float maxValue{1.0f};
        bool exposed{false};
    };

    struct MetaSoundGraphDef {
        std::string graphId;
        std::string name;
        std::vector<std::string> nodes;
        std::vector<std::string> connections;
        std::vector<std::string> parameters;
        float masterGain{1.0f};
        int sampleRate{48000};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MetaSoundTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateGraph(const std::string& name);
    bool RemoveGraph(const std::string& graphId);
    std::string AddNode(const std::string& graphId, const std::string& name, MetaSoundNodeType type);
    bool RemoveNode(const std::string& graphId, const std::string& nodeId);
    bool ConnectNodes(const std::string& graphId, const std::string& srcNodeId, const std::string& dstNodeId);
    bool DisconnectNodes(const std::string& graphId, const std::string& srcNodeId, const std::string& dstNodeId);
    std::string AddParameter(const std::string& graphId, const std::string& name, AudioParameterType type);
    bool RemoveParameter(const std::string& graphId, const std::string& paramId);
    bool SetParameterDefault(const std::string& paramId, const std::string& defaultValue);
    bool SetParameterRange(const std::string& paramId, float minValue, float maxValue);
    bool SetMasterGain(const std::string& graphId, float gain);
    bool SetSampleRate(const std::string& graphId, int sampleRate);
    bool SetWaveform(const std::string& nodeId, WaveformType waveform);
    bool PreviewGraph(const std::string& graphId);
    bool PlayGraph(const std::string& graphId);
    bool StopGraph(const std::string& graphId);
    const MetaSoundGraphDef* GetGraph(const std::string& graphId) const;
    const MetaSoundNodeDef* GetNode(const std::string& nodeId) const;
    const AudioParameterDef* GetParameter(const std::string& paramId) const;
    std::vector<std::string> GetAllGraphIds() const;
    std::vector<std::string> GetNodesByType(MetaSoundNodeType type) const;
    std::vector<std::string> GetParametersByType(AudioParameterType type) const;
    bool ValidateGraph(const std::string& graphId) const;
    bool ExportGraph(const std::string& graphId, const std::string& filePath) const;
    bool SaveGraph(const std::string& graphId, const std::string& filePath) const;
    bool LoadGraph(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, MetaSoundGraphDef> m_graphs;
    std::unordered_map<std::string, MetaSoundNodeDef> m_nodes;
    std::unordered_map<std::string, AudioParameterDef> m_parameters;
    int m_nextGraphIndex{0};
    int m_nextNodeIndex{0};
    int m_nextParamIndex{0};
};

} // namespace Atlas::Editor
