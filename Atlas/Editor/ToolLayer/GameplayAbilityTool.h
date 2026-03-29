#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P18 Tool — Gameplay Ability System ability authoring, attribute set configuration, and effect management.
class GameplayAbilityTool : public ITool {
public:
    enum class AbilityActivationPolicy { OnInputAction, OnSpawn, OnEvent, Manual, Passive, OnGranted };
    enum class AbilityEndPolicy { WhenInputEnded, WhenCompleted, ByTag, Manual, OnDeath, OnStateChange };
    enum class EffectApplicationType { Instant, Duration, Infinite, Periodic };

    struct AbilityTagDef {
        std::string tagId;
        std::string name;
        std::string category;
        std::vector<std::string> inherits;
    };

    struct GameplayAttributeDef {
        std::string attrId;
        std::string name;
        float baseValue{0.0f};
        float minValue{0.0f};
        float maxValue{100.0f};
        bool replication{true};
    };

    struct GameplayAbilityDef {
        std::string abilityId;
        std::string name;
        AbilityActivationPolicy activationPolicy{AbilityActivationPolicy::OnInputAction};
        AbilityEndPolicy endPolicy{AbilityEndPolicy::WhenCompleted};
        std::vector<std::string> tags;
        std::vector<std::string> costs;
        float cooldown{0.0f};
        std::string inputAction;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "GameplayAbilityTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateAbility(const std::string& name);
    bool RemoveAbility(const std::string& abilityId);
    bool GrantAbility(const std::string& abilityId, const std::string& targetId);
    bool RevokeAbility(const std::string& abilityId, const std::string& targetId);
    bool ActivateAbility(const std::string& abilityId);
    bool CancelAbility(const std::string& abilityId);
    std::string CreateAttribute(const std::string& name, float baseValue, float minValue, float maxValue);
    bool RemoveAttribute(const std::string& attrId);
    bool SetAttributeValue(const std::string& attrId, float value);
    bool SetAttributeRange(const std::string& attrId, float minValue, float maxValue);
    bool AddAbilityCost(const std::string& abilityId, const std::string& attrId, float cost);
    bool RemoveAbilityCost(const std::string& abilityId, const std::string& attrId);
    bool SetCooldown(const std::string& abilityId, float cooldown);
    bool SetActivationPolicy(const std::string& abilityId, AbilityActivationPolicy policy);
    bool SetEndPolicy(const std::string& abilityId, AbilityEndPolicy policy);
    bool PreviewAbility(const std::string& abilityId);
    const GameplayAbilityDef* GetAbility(const std::string& abilityId) const;
    const GameplayAttributeDef* GetAttribute(const std::string& attrId) const;
    std::vector<std::string> GetAllAbilityIds() const;
    std::vector<std::string> GetAllAttributeIds() const;
    std::vector<std::string> GetAbilitiesByTag(const std::string& tag) const;
    bool ValidateAbility(const std::string& abilityId) const;
    bool ExportAbilitySet(const std::string& filePath) const;
    bool SaveAbilitySet(const std::string& filePath) const;
    bool LoadAbilitySet(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, GameplayAbilityDef> m_abilities;
    std::unordered_map<std::string, GameplayAttributeDef> m_attributes;
    std::unordered_map<std::string, AbilityTagDef> m_tags;
    int m_nextAbilityIndex{0};
    int m_nextAttributeIndex{0};
};

} // namespace Atlas::Editor
