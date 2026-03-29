#pragma once
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Engine {

/// Phase 43D — Registry for trap body components managing trigger zones, trap states, and effect chains.
class TrapBodyRegistry {
public:
    enum class TrapType { Spike, Fire, Poison, Electric, Ice, Explosive, Void, Custom };
    enum class TriggerCondition { OnEnter, OnStay, OnExit, OnInteract, OnTimer, OnDamage, Custom };
    enum class TrapState { Idle, Armed, Triggered, Cooldown, Depleted, Disabled, Custom };
    enum class ArmingMethod { Automatic, Manual, Proximity, Remote, Timed, Custom };

    struct TrapEffectDef {
        std::string effectId;
        std::string effectName;
        TrapType trapType{TrapType::Spike};
        float damageAmount{10.0f};
        float effectRadius{2.0f};
        float effectDuration{0.5f};
        std::string particleEffectId;
        std::string soundCueId;
        bool enabled{true};
    };

    struct TrapTriggerZoneDef {
        std::string triggerZoneId;
        std::string trapBodyId;
        TriggerCondition condition{TriggerCondition::OnEnter};
        float zoneRadius{1.5f};
        float zoneHeight{2.0f};
        bool playerOnly{false};
        bool npcTrigger{true};
        bool repeatTrigger{false};
        bool enabled{true};
    };

    struct TrapBodyRecord {
        std::string trapBodyId;
        std::string ownerEntityId;
        std::string zoneId;
        TrapState state{TrapState::Idle};
        ArmingMethod armingMethod{ArmingMethod::Automatic};
        TrapType trapType{TrapType::Spike};
        float armingDelayMs{0.0f};
        float cooldownMs{5000.0f};
        int maxTriggers{-1};
        int triggerCount{0};
        float luckModifier{1.0f};
        bool enabled{true};
        std::vector<std::string> effectChainIds;
    };

    // Trap effect CRUD
    bool RegisterTrapEffect(const TrapEffectDef& effect);
    bool UnregisterTrapEffect(const std::string& effectId);
    bool EnableTrapEffect(const std::string& effectId, bool enabled);
    const TrapEffectDef* GetTrapEffect(const std::string& effectId) const;
    std::vector<std::string> GetAllEffectIds() const;
    std::vector<std::string> GetEffectsByType(TrapType type) const;
    std::vector<std::string> GetEnabledEffects() const;

    // Trigger zone CRUD
    bool RegisterTriggerZone(const TrapTriggerZoneDef& zone);
    bool UnregisterTriggerZone(const std::string& triggerZoneId);
    bool EnableTriggerZone(const std::string& triggerZoneId, bool enabled);
    bool SetTriggerCondition(const std::string& triggerZoneId, TriggerCondition condition);
    const TrapTriggerZoneDef* GetTriggerZone(const std::string& triggerZoneId) const;
    std::vector<std::string> GetAllZoneIds() const;
    std::vector<std::string> GetZonesByCondition(TriggerCondition condition) const;
    std::vector<std::string> GetZonesByTrap(const std::string& trapBodyId) const;

    // Trap body CRUD
    bool RegisterTrapBody(const TrapBodyRecord& record);
    bool UnregisterTrapBody(const std::string& trapBodyId);
    bool ArmTrap(const std::string& trapBodyId);
    bool DisarmTrap(const std::string& trapBodyId);
    bool TriggerTrap(const std::string& trapBodyId);
    bool ResetTrap(const std::string& trapBodyId);
    bool DisableTrap(const std::string& trapBodyId);
    bool SetTrapState(const std::string& trapBodyId, TrapState state);
    bool AddEffectToChain(const std::string& trapBodyId, const std::string& effectId);
    bool RemoveEffectFromChain(const std::string& trapBodyId, const std::string& effectId);
    const TrapBodyRecord* GetTrapBody(const std::string& trapBodyId) const;
    std::vector<std::string> GetAllTrapBodyIds() const;
    std::vector<std::string> GetTrapBodiesByOwner(const std::string& ownerEntityId) const;
    std::vector<std::string> GetTrapBodiesByState(TrapState state) const;
    std::vector<std::string> GetTrapBodiesByType(TrapType type) const;
    std::vector<std::string> GetArmedTraps() const;
    std::vector<std::string> GetDepletedTraps() const;

    void Clear();
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);

private:
    std::unordered_map<std::string, TrapEffectDef> m_trapEffects;
    std::unordered_map<std::string, TrapTriggerZoneDef> m_triggerZones;
    std::unordered_map<std::string, TrapBodyRecord> m_trapBodies;
};

} // namespace Atlas::Engine
