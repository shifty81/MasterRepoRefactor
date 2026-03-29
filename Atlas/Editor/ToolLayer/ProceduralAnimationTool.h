#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P9 Tool — Procedural animation rule authoring for runtime character motion.
class ProceduralAnimationTool : public ITool {
public:
    enum class RuleType { IK, LookAt, FootPlant, SwingTwist, Spring, Jiggle, Secondary };
    enum class SolverAlgorithm { FABRIK, CCD, TwoBone, Jacobian };
    enum class ActivationMode { Always, OnEvent, OnState, Blend };
    enum class TargetSpace { World, Local, BoneRelative };

    struct IKTarget {
        std::string targetId;
        std::string name;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        TargetSpace space{TargetSpace::World};
        std::string attachEntityId;
        std::string attachSocket;
        float weight{1.0f};
    };

    struct ProceduralRule {
        std::string ruleId;
        std::string name;
        RuleType type{RuleType::IK};
        SolverAlgorithm solver{SolverAlgorithm::FABRIK};
        ActivationMode activationMode{ActivationMode::Always};
        std::string rootBoneName;
        std::string tipBoneName;
        std::string targetId;
        float weight{1.0f};
        float blendSpeed{5.0f};
        int maxIterations{10};
        float tolerance{0.001f};
        bool enabled{true};
        bool stretchEnabled{false};
        float stretchLimit{1.2f};
        std::string activationEvent;
        std::string activationState;
    };

    struct AnimationLayer {
        std::string layerId;
        std::string name;
        float weight{1.0f};
        bool additive{false};
        std::vector<std::string> ruleIds;
        std::vector<std::string> boneFilter;
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ProceduralAnimationTool"; }
    bool IsActive() const override { return m_active; }

    // Rule management
    std::string CreateRule(const std::string& name, RuleType type,
                            const std::string& rootBone = "",
                            const std::string& tipBone = "");
    bool RemoveRule(const std::string& ruleId);
    bool SetRuleType(const std::string& ruleId, RuleType type);
    bool SetRuleSolver(const std::string& ruleId, SolverAlgorithm solver);
    bool SetRuleWeight(const std::string& ruleId, float weight);
    bool SetRuleEnabled(const std::string& ruleId, bool enabled);
    bool SetRuleTarget(const std::string& ruleId, const std::string& targetId);
    bool SetRuleActivationMode(const std::string& ruleId, ActivationMode mode);
    bool SetRuleStretch(const std::string& ruleId, bool enabled, float limit = 1.2f);
    bool SetRuleIterations(const std::string& ruleId, int maxIterations);
    int GetRuleCount() const { return static_cast<int>(m_rules.size()); }
    const ProceduralRule* GetRule(const std::string& ruleId) const;
    std::vector<std::string> GetRuleIds() const;
    std::vector<std::string> GetRuleIdsByType(RuleType type) const;

    // IK target management
    std::string CreateIKTarget(const std::string& name,
                                float px = 0.0f, float py = 0.0f, float pz = 0.0f);
    bool RemoveIKTarget(const std::string& targetId);
    bool SetTargetPosition(const std::string& targetId, float px, float py, float pz);
    bool SetTargetWeight(const std::string& targetId, float weight);
    bool SetTargetAttachment(const std::string& targetId, const std::string& entityId,
                              const std::string& socket);
    int GetIKTargetCount() const { return static_cast<int>(m_targets.size()); }
    const IKTarget* GetIKTarget(const std::string& targetId) const;

    // Layer management
    std::string CreateLayer(const std::string& name, bool additive = false);
    bool RemoveLayer(const std::string& layerId);
    bool AddRuleToLayer(const std::string& layerId, const std::string& ruleId);
    bool RemoveRuleFromLayer(const std::string& layerId, const std::string& ruleId);
    bool SetLayerWeight(const std::string& layerId, float weight);
    bool SetLayerEnabled(const std::string& layerId, bool enabled);
    bool AddBoneFilter(const std::string& layerId, const std::string& boneName);
    int GetLayerCount() const { return static_cast<int>(m_layers.size()); }
    const AnimationLayer* GetLayer(const std::string& layerId) const;

    // Persistence
    bool SaveRules(const std::string& filePath) const;
    bool LoadRules(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::vector<ProceduralRule> m_rules;
    std::vector<IKTarget> m_targets;
    std::vector<AnimationLayer> m_layers;
    int m_nextRuleIndex{0};
    int m_nextTargetIndex{0};
    int m_nextLayerIndex{0};
};

} // namespace Atlas::Editor
