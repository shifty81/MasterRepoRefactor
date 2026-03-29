#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 34D — Registry for network body definitions used by the replication and session subsystem.
class NetworkBodyRegistry {
public:
    enum class NetworkBodyState { Offline, Connecting, Connected, Synchronizing, Ready, Error, Disconnecting };
    enum class NetworkBodyRole { None_, Authority, AutonomousProxy, SimulatedProxy, Replay, Custom };
    enum class ReplicationMode { None_, RepGraph, Actor, Component, Subobject, Custom };
    enum class NetworkChannel { Reliable, Unreliable, Voice, DataStream, FileTransfer, Custom };
    enum class SyncFrequency { Never, Low, Medium, High, VeryHigh, Custom };

    struct ReplicationConfig {
        std::string configId;
        ReplicationMode mode{ReplicationMode::RepGraph};
        NetworkChannel channel{NetworkChannel::Reliable};
        SyncFrequency syncFrequency{SyncFrequency::Medium};
        float relevancyRadius{10000.0f};
        bool dormancy{false};
        float priorityMultiplier{1.0f};
    };

    struct NetworkPropertyDef {
        std::string propId;
        std::string name;
        std::string propType;
        ReplicationMode replicationMode{ReplicationMode::Actor};
        SyncFrequency syncFrequency{SyncFrequency::Medium};
        std::string condition;
        bool isOwnerOnly{false};
    };

    struct NetworkBodyRecord {
        std::string bodyId;
        std::string name;
        NetworkBodyRole role{NetworkBodyRole::SimulatedProxy};
        ReplicationConfig replicationConfig;
        std::vector<std::string> properties;
        std::string ownerActorId;
        std::string netId;
        NetworkBodyState bodyState{NetworkBodyState::Offline};
        float latencyMs{0.0f};
    };

    // Body registration
    bool RegisterBody(const NetworkBodyRecord& record);
    bool UnregisterBody(const std::string& bodyId);

    // Role and state
    bool SetBodyRole(const std::string& bodyId, NetworkBodyRole role);
    bool SetBodyState(const std::string& bodyId, NetworkBodyState state);

    // Replication configuration
    bool SetReplicationMode(const std::string& bodyId, ReplicationMode mode);
    bool SetSyncFrequency(const std::string& bodyId, SyncFrequency frequency);
    bool SetRelevancyRadius(const std::string& bodyId, float radius);

    // Property management
    bool AddNetworkProperty(const std::string& bodyId, const NetworkPropertyDef& prop);
    bool RemoveNetworkProperty(const std::string& bodyId, const std::string& propId);
    bool SetPropertyCondition(const std::string& propId, const std::string& condition);
    bool SetOwnerOnly(const std::string& propId, bool ownerOnly);

    // Ownership and identity
    bool SetOwnerActor(const std::string& bodyId, const std::string& ownerActorId);
    bool SetNetId(const std::string& bodyId, const std::string& netId);
    bool SetLatency(const std::string& bodyId, float latencyMs);

    // Queries
    const NetworkBodyRecord* GetBodyById(const std::string& bodyId) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByRole(NetworkBodyRole role) const;
    std::vector<std::string> GetBodiesByState(NetworkBodyState state) const;
    std::vector<std::string> GetConnectedBodies() const;
    std::vector<std::string> GetAuthorityBodies() const;
    std::vector<std::string> GetProxies() const;
    std::vector<std::string> GetBodiesInRadius(float x, float y, float z, float radius) const;

    // Persistence
    void Clear();
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);

private:
    std::unordered_map<std::string, NetworkBodyRecord> m_bodies;
    std::unordered_map<std::string, NetworkPropertyDef> m_properties;
};

} // namespace Atlas::Engine
