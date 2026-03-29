#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P15 Tool — Network replication policy authoring, entity ownership, and authority management.
class NetworkReplicationTool : public ITool {
public:
    enum class ReplicaPolicy { None, OwnerOnly, Broadcast, RelevantActors, Custom };
    enum class AuthorityMode { Server, Client, Shared, Autonomous };
    enum class ReplicationFrequency { Realtime, PerTick, OnChange, Throttled };

    struct ReplicationRule {
        std::string ruleId;
        std::string propertyPath;
        ReplicaPolicy policy{ReplicaPolicy::Broadcast};
        ReplicationFrequency frequency{ReplicationFrequency::OnChange};
        int priority{0};
    };

    struct EntityNetConfig {
        std::string entityId;
        AuthorityMode authorityMode{AuthorityMode::Server};
        std::vector<std::string> rules;
        float relevanceRadius{1000.0f};
        bool dormantByDefault{false};
    };

    struct NetDiagnostics {
        float rttMs{0.0f};
        float packetLoss{0.0f};
        float bandwidth{0.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "NetworkReplicationTool"; }
    bool IsActive() const override { return m_active; }

    // Config management
    std::string CreateEntityConfig(const std::string& entityId, AuthorityMode mode = AuthorityMode::Server);
    bool RemoveEntityConfig(const std::string& entityId);
    bool AddRule(const std::string& entityId, const ReplicationRule& rule);
    bool RemoveRule(const std::string& entityId, const std::string& ruleId);
    bool SetAuthorityMode(const std::string& entityId, AuthorityMode mode);
    bool SetRelevanceRadius(const std::string& entityId, float radius);
    bool SetDormant(const std::string& entityId, bool dormant);

    // Simulation and validation
    NetDiagnostics SimulateReplication(const std::string& entityId) const;
    bool ValidateConfig(const std::string& entityId) const;
    bool ExportReplicationManifest(const std::string& filePath) const;

    // Queries
    const EntityNetConfig* GetEntityConfig(const std::string& entityId) const;
    std::vector<std::string> GetAllEntityIds() const;
    int GetRuleCount(const std::string& entityId) const;

    // Persistence
    bool SaveNetConfig(const std::string& filePath) const;
    bool LoadNetConfig(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, EntityNetConfig> m_configs;
    std::unordered_map<std::string, ReplicationRule> m_rules;
    int m_nextRuleIndex{0};
};

} // namespace Atlas::Editor
