#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P11 Tool — Runtime prefab spawning rules and pool management editor.
class PrefabSpawnerTool : public ITool {
public:
    enum class SpawnTrigger { OnStart, OnEvent, OnTimer, OnProximity, Manual };
    enum class SpawnShape { Point, Sphere, Box, Ring, Surface };
    enum class DespawnCondition { Never, LifetimeExpired, OutOfRange, OnEvent };
    enum class PoolStrategy { FixedSize, GrowOnDemand, Shrink };

    struct SpawnOffset {
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float rotY{0.0f};
        float scaleMin{1.0f};
        float scaleMax{1.0f};
        bool randomRotY{true};
        bool alignToSurface{false};
    };

    struct SpawnPool {
        std::string poolId;
        std::string name;
        std::string prefabId;
        PoolStrategy strategy{PoolStrategy::FixedSize};
        int initialSize{10};
        int maxSize{50};
        int currentActive{0};
        bool preWarm{true};
    };

    struct SpawnerRule {
        std::string ruleId;
        std::string name;
        std::string poolId;
        SpawnTrigger trigger{SpawnTrigger::OnTimer};
        SpawnShape shape{SpawnShape::Sphere};
        DespawnCondition despawnCondition{DespawnCondition::LifetimeExpired};
        SpawnOffset spawnOffset;
        float spawnRadius{5.0f};
        float spawnBoxHalfX{5.0f};
        float spawnBoxHalfY{1.0f};
        float spawnBoxHalfZ{5.0f};
        float timerInterval{5.0f};
        float timerVariance{1.0f};
        float proximityRadius{20.0f};
        float despawnLifetime{30.0f};
        float despawnRange{100.0f};
        int maxSpawnedCount{10};
        int spawnCountPerTrigger{1};
        bool enabled{true};
        std::string triggerEventName;
        std::string despawnEventName;
        std::string linkedEntityId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "PrefabSpawnerTool"; }
    bool IsActive() const override { return m_active; }

    // Pool management
    std::string CreatePool(const std::string& name, const std::string& prefabId,
                            int initialSize = 10, int maxSize = 50);
    bool RemovePool(const std::string& poolId);
    bool SetPoolPrefab(const std::string& poolId, const std::string& prefabId);
    bool SetPoolStrategy(const std::string& poolId, PoolStrategy strategy);
    bool SetPoolSize(const std::string& poolId, int initialSize, int maxSize);
    bool SetPoolPreWarm(const std::string& poolId, bool preWarm);
    int GetPoolCount() const { return static_cast<int>(m_pools.size()); }
    const SpawnPool* GetPool(const std::string& poolId) const;
    std::vector<std::string> GetPoolIds() const;

    // Spawner rule management
    std::string CreateRule(const std::string& name, const std::string& poolId,
                            SpawnTrigger trigger = SpawnTrigger::OnTimer);
    bool RemoveRule(const std::string& ruleId);
    bool SetTrigger(const std::string& ruleId, SpawnTrigger trigger);
    bool SetSpawnShape(const std::string& ruleId, SpawnShape shape);
    bool SetDespawnCondition(const std::string& ruleId, DespawnCondition condition);
    bool SetSpawnRadius(const std::string& ruleId, float radius);
    bool SetSpawnBox(const std::string& ruleId, float hx, float hy, float hz);
    bool SetTimerInterval(const std::string& ruleId, float interval, float variance = 0.0f);
    bool SetProximityRadius(const std::string& ruleId, float radius);
    bool SetDespawnLifetime(const std::string& ruleId, float lifetime);
    bool SetDespawnRange(const std::string& ruleId, float range);
    bool SetMaxSpawnedCount(const std::string& ruleId, int max);
    bool SetSpawnCountPerTrigger(const std::string& ruleId, int count);
    bool SetRuleEnabled(const std::string& ruleId, bool enabled);
    bool SetSpawnOffset(const std::string& ruleId, float px, float py, float pz,
                         float rotY, float scaleMin, float scaleMax);
    bool LinkToEntity(const std::string& ruleId, const std::string& entityId);
    bool SetTriggerEvent(const std::string& ruleId, const std::string& eventName);
    int GetRuleCount() const { return static_cast<int>(m_rules.size()); }
    const SpawnerRule* GetRule(const std::string& ruleId) const;
    std::vector<std::string> GetRuleIds() const;
    std::vector<std::string> GetEnabledRuleIds() const;

    // Runtime simulation
    bool TriggerSpawn(const std::string& ruleId);
    bool DespawnAll(const std::string& ruleId);
    int GetActiveCount(const std::string& ruleId) const;

    // Persistence
    bool SaveSpawners(const std::string& filePath) const;
    bool LoadSpawners(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, SpawnPool> m_pools;
    std::unordered_map<std::string, SpawnerRule> m_rules;
    int m_nextPoolIndex{0};
    int m_nextRuleIndex{0};
};

} // namespace Atlas::Editor
