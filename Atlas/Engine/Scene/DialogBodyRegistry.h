#pragma once
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Engine {

/// Phase 38D — Registry for dialog body components managing conversation flow and NPC dialogue state.
class DialogBodyRegistry {
public:
    enum class DialogBodyState { Idle, Active, Speaking, Waiting, Completed, Cancelled, Disabled, Custom };
    enum class DialogBodyScope { Global, Local, NPC, Player, Zone, Cutscene, Custom };
    enum class DialogTriggerType { OnApproach, OnInteract, OnEvent, OnTimer, OnCondition, OnSignal, Custom };
    enum class DialogFlowType { Linear, Branching, Conditional, Random, Scripted, Custom };
    enum class DialogBodyFlags { None=0, Persistent=1, Repeatable=2, SkipOnReplay=4, VoiceActed=8, Subtitled=16 };

    struct DialogLineConfig {
        std::string lineId;
        std::string bodyId;
        std::string speakerId;
        std::string text;
        std::string voiceAssetId;
        float duration{0.0f};
        bool autoAdvance{true};
        std::vector<std::string> responseIds;
    };

    struct DialogResponseDef {
        std::string responseId;
        std::string lineId;
        std::string responseText;
        std::string nextLineId;
        std::string conditionExpr;
        bool isDefault{false};
    };

    struct DialogBodyRecord {
        std::string bodyId;
        std::string name;
        DialogBodyScope scope{DialogBodyScope::NPC};
        DialogBodyState state{DialogBodyState::Idle};
        DialogFlowType flowType{DialogFlowType::Linear};
        DialogTriggerType triggerType{DialogTriggerType::OnInteract};
        std::string startLineId;
        int playCount{0};
        std::vector<std::string> lineIds;
        std::vector<std::string> responseIds;
        std::vector<int> flags;
    };

    // Body CRUD
    bool RegisterBody(const DialogBodyRecord& record);
    bool UnregisterBody(const std::string& bodyId);
    bool SetBodyScope(const std::string& bodyId, DialogBodyScope scope);
    bool SetBodyState(const std::string& bodyId, DialogBodyState state);
    bool SetFlowType(const std::string& bodyId, DialogFlowType flowType);
    bool SetTriggerType(const std::string& bodyId, DialogTriggerType triggerType);
    bool ActivateBody(const std::string& bodyId);
    bool CompleteBody(const std::string& bodyId);
    bool CancelBody(const std::string& bodyId);
    bool DisableBody(const std::string& bodyId);
    const DialogBodyRecord* GetBodyById(const std::string& bodyId) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByScope(DialogBodyScope scope) const;
    std::vector<std::string> GetBodiesByFlow(DialogFlowType flowType) const;
    std::vector<std::string> GetActiveBodies() const;
    std::vector<std::string> GetCompletedBodies() const;

    // Line CRUD
    bool AddLine(const std::string& bodyId, const DialogLineConfig& line);
    bool RemoveLine(const std::string& bodyId, const std::string& lineId);
    const DialogLineConfig* GetLine(const std::string& lineId) const;
    std::vector<std::string> GetLinesByBody(const std::string& bodyId) const;

    // Response CRUD
    bool AddResponse(const std::string& lineId, const DialogResponseDef& response);
    bool RemoveResponse(const std::string& lineId, const std::string& responseId);
    const DialogResponseDef* GetResponse(const std::string& responseId) const;
    std::vector<std::string> GetResponsesByLine(const std::string& lineId) const;

    void Clear();
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);

private:
    std::unordered_map<std::string, DialogBodyRecord> m_bodies;
    std::unordered_map<std::string, DialogLineConfig> m_lines;
    std::unordered_map<std::string, DialogResponseDef> m_responses;
};

} // namespace Atlas::Engine
