#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P20 Tool — Conversation graph node authoring, speaker configuration, and dialogue flow management.
class ConversationGraphTool : public ITool {
public:
    enum class ConvNodeType { Dialogue, Choice, Condition, Action, Jump, Entry, Exit, Custom };
    enum class SpeakerRole { Player, NPC, Narrator, System, Ambient, Custom };
    enum class DialogueFlowState { Idle, Active, Branching, Waiting, Complete, Error, Custom };

    struct SpeakerDef {
        std::string speakerId;
        std::string name;
        SpeakerRole role{SpeakerRole::NPC};
        std::string voiceActorId;
        std::string portraitAsset;
        std::string defaultEmotion;
        bool canInterrupt{false};
    };

    struct ConvNodeDef {
        std::string nodeId;
        std::string text;
        ConvNodeType nodeType{ConvNodeType::Dialogue};
        std::string speakerId;
        std::vector<std::string> conditions;
        std::vector<std::string> actions;
        std::vector<std::string> nextNodeIds;
        float displayTime{0.0f};
    };

    struct ConversationGraphDef {
        std::string graphId;
        std::string name;
        std::string entryNodeId;
        std::string ownerNpcId;
        std::vector<std::string> nodeIds;
        std::vector<std::string> speakerIds;
        DialogueFlowState flowState{DialogueFlowState::Idle};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ConversationGraphTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateGraph(const ConversationGraphDef& def);
    bool DeleteGraph(const std::string& graphId);
    bool SetEntryNode(const std::string& graphId, const std::string& nodeId);
    bool SetOwnerNpc(const std::string& graphId, const std::string& npcId);
    const ConversationGraphDef* GetGraph(const std::string& graphId) const;
    std::vector<std::string> GetAllGraphIds() const;

    std::string AddNode(const std::string& graphId, const ConvNodeDef& node);
    bool RemoveNode(const std::string& graphId, const std::string& nodeId);
    bool SetNodeType(const std::string& nodeId, ConvNodeType type);
    bool SetNodeText(const std::string& nodeId, const std::string& text);
    bool LinkNodes(const std::string& fromNodeId, const std::string& toNodeId);
    bool UnlinkNodes(const std::string& fromNodeId, const std::string& toNodeId);
    const ConvNodeDef* GetNode(const std::string& nodeId) const;
    std::vector<std::string> GetNodesByType(ConvNodeType type) const;

    std::string AddSpeaker(const std::string& graphId, const SpeakerDef& speaker);
    bool RemoveSpeaker(const std::string& graphId, const std::string& speakerId);
    bool SetSpeakerRole(const std::string& speakerId, SpeakerRole role);
    const SpeakerDef* GetSpeaker(const std::string& speakerId) const;

    bool ValidateGraph(const std::string& graphId) const;
    bool ExportGraph(const std::string& graphId, const std::string& filePath) const;
    bool ImportGraph(const std::string& filePath);
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, ConversationGraphDef> m_graphs;
    std::unordered_map<std::string, ConvNodeDef> m_nodes;
    std::unordered_map<std::string, SpeakerDef> m_speakers;
    int m_nextGraphIndex{0};
};

} // namespace Atlas::Editor
