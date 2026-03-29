#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P22 Tool — Chaos geometry collection destruction manager.
class ChaosDestructionTool : public ITool {
public:
    enum class DestructionMode { Disabled, Simulated, Kinematic, Fracture, Crumble, Shatter, Custom };
    enum class FragmentPolicy { None, ByVolume, ByMass, ByDamage, Uniform, Hierarchical, Custom };
    enum class DamageThresholdType { Absolute, Relative, Impulse, Accumulated, Percentage, Custom };
    enum class DebrisLifetimeMode { Infinite, TimeBased, DistanceBased, OutOfView, Custom };

    struct GeometryCollectionDef {
        std::string collectionId;
        std::string name;
        std::string assetPath;
        DestructionMode destructionMode{DestructionMode::Simulated};
        FragmentPolicy fragmentPolicy{FragmentPolicy::ByVolume};
        float damageThreshold{100.0f};
        int maxFragments{64};
        bool enableClustering{true};
        std::string clusterId;
    };

    struct DestructionEventRecord {
        std::string eventId;
        std::string collectionId;
        std::string impactSourceId;
        float damageAmount{0.0f};
        float impactX{0.0f};
        float impactY{0.0f};
        float impactZ{0.0f};
        long long timestamp{0};
        bool didFracture{false};
    };

    struct FragmentConfigDef {
        std::string configId;
        std::string collectionId;
        FragmentPolicy policy{FragmentPolicy::ByVolume};
        float minFragmentVolume{10.0f};
        float maxFragmentVolume{1000.0f};
        float massScale{1.0f};
        int maxFragmentCount{32};
        bool enableDebris{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ChaosDestructionTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateGeometryCollection(const GeometryCollectionDef& def);
    bool DeleteGeometryCollection(const std::string& collectionId);
    const GeometryCollectionDef* GetGeometryCollection(const std::string& collectionId) const;
    std::vector<std::string> GetAllCollectionIds() const;

    bool SetDestructionMode(const std::string& collectionId, DestructionMode mode);
    bool SetFragmentPolicy(const std::string& collectionId, FragmentPolicy policy);
    bool SetDamageThreshold(const std::string& collectionId, float threshold);

    bool RecordDestructionEvent(const DestructionEventRecord& record);
    std::vector<DestructionEventRecord> GetDestructionEvents() const;
    std::vector<DestructionEventRecord> GetEventsByCollection(const std::string& collectionId) const;
    void FlushEventLog();

    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, GeometryCollectionDef> m_collections;
    std::unordered_map<std::string, FragmentConfigDef> m_fragmentConfigs;
    std::vector<DestructionEventRecord> m_eventLog;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
