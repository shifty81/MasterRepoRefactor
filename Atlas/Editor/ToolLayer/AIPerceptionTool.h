#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P16 Tool — AI perception configuration, sense authoring, and stimulus source management.
class AIPerceptionTool : public ITool {
public:
    enum class SenseType { Sight, Hearing, Damage, Touch, Team, Prediction, Custom };
    enum class PerceptionReaction { Curious, Alert, Hostile, Fleeing, Investigating, Idle };
    enum class StimulusStrength { Whisper, Quiet, Normal, Loud, Extreme };

    struct SenseDef {
        std::string senseId;
        std::string name;
        SenseType senseType{SenseType::Sight};
        float range{1000.0f};
        float angle{90.0f};
        float lossRadius{1200.0f};
        float affinity{1.0f};
        float maxAge{5.0f};
    };

    struct StimulusSource {
        std::string sourceId;
        std::string name;
        SenseType senseType{SenseType::Hearing};
        StimulusStrength strength{StimulusStrength::Normal};
        std::vector<float> position;
        float emitRadius{200.0f};
        float duration{2.0f};
    };

    struct PerceptionConfig {
        std::string agentId;
        std::vector<std::string> senses;
        std::unordered_map<std::string, PerceptionReaction> reactionMap;
        SenseType dominantSense{SenseType::Sight};
        float updateInterval{0.1f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AIPerceptionTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateSense(const std::string& name, SenseType type = SenseType::Sight);
    bool RemoveSense(const std::string& senseId);
    std::string CreateStimulusSource(const std::string& name, SenseType type = SenseType::Hearing);
    bool RemoveStimulusSource(const std::string& sourceId);
    bool AddSenseToConfig(const std::string& agentId, const std::string& senseId);
    bool SetSenseRange(const std::string& senseId, float range);
    bool SetSenseAngle(const std::string& senseId, float angle);
    bool SetReaction(const std::string& agentId, const std::string& stimulusType, PerceptionReaction reaction);
    bool SetUpdateInterval(const std::string& agentId, float interval);
    bool SimulatePerception(const std::string& agentId);
    const SenseDef* GetSense(const std::string& senseId) const;
    const StimulusSource* GetStimulusSource(const std::string& sourceId) const;
    const PerceptionConfig* GetPerceptionConfig(const std::string& agentId) const;
    std::vector<std::string> GetAllSenseIds() const;
    std::vector<std::string> GetAllStimulusIds() const;
    bool ValidateConfig(const std::string& agentId) const;
    bool ExportPerceptionConfig(const std::string& filePath) const;
    bool SavePerception(const std::string& filePath) const;
    bool LoadPerception(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, SenseDef> m_senses;
    std::unordered_map<std::string, StimulusSource> m_stimulusSources;
    std::unordered_map<std::string, PerceptionConfig> m_perceptionConfigs;
    int m_nextSenseIndex{0};
    int m_nextStimulusIndex{0};
};

} // namespace Atlas::Editor
