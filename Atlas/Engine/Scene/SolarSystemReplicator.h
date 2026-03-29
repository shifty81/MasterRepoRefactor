#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 29C — Solar system replication manager for distributed sync and conflict resolution
class SolarSystemReplicator {
public:
    enum class ReplicaMode { Primary, Secondary, Shadow, Offline };
    enum class SyncState { InSync, Drifted, Conflicted, Syncing, Unknown };
    enum class ReplicaRole { Leader, Follower, Observer };

    struct ReplicaDescriptor {
        std::string replicaId;
        std::string systemId;
        ReplicaMode mode{ReplicaMode::Secondary};
        ReplicaRole role{ReplicaRole::Follower};
        SyncState syncState{SyncState::Unknown};
        std::string endpoint;
        long long lastSyncTimestamp{0};
    };

    struct SyncCheckpoint {
        std::string checkpointId;
        std::string replicaId;
        long long timestamp{0};
        std::string stateHash;
        std::string snapshotPath;
        bool valid{true};
    };

    struct ReplicationPolicy {
        std::string policyId;
        int minReplicas{2};
        int maxReplicas{5};
        long long syncIntervalMs{5000};
        bool autoResolveConflicts{false};
        bool allowOfflineReplicas{true};
        int conflictRetentionDays{7};
    };

    struct ConflictRecord {
        std::string conflictId;
        std::string replicaIdA;
        std::string replicaIdB;
        long long detectedAt{0};
        std::string conflictType;
        bool resolved{false};
        std::string resolution;
    };

    std::string RegisterReplica(const std::string& systemId, ReplicaMode mode, const std::string& endpoint);
    bool UnregisterReplica(const std::string& replicaId);
    bool StartReplication(const std::string& replicaId);
    bool StopReplication(const std::string& replicaId);
    bool SyncNow(const std::string& replicaId);
    bool ForceLeader(const std::string& replicaId);
    bool SetPolicy(const ReplicationPolicy& policy);
    SyncState GetSyncState(const std::string& replicaId) const;

    std::vector<std::string> GetConflicts(const std::string& replicaId) const;
    bool ResolveConflict(const std::string& conflictId, const std::string& resolution);
    std::vector<std::string> GetReplicas(const std::string& systemId) const;
    std::string GetLeader(const std::string& systemId) const;

    std::string Checkpoint(const std::string& replicaId);
    bool RestoreFromCheckpoint(const std::string& replicaId, const std::string& checkpointId);
    const SyncCheckpoint* GetCheckpoint(const std::string& checkpointId) const;
    std::vector<std::string> GetCheckpointIds(const std::string& replicaId) const;

    int GetReplicaCount() const;
    const ReplicaDescriptor* GetReplica(const std::string& replicaId) const;
    std::vector<std::string> GetAllReplicaIds() const;

    struct ReplicationStats {
        int totalReplicas{0};
        int activeReplicas{0};
        int conflictCount{0};
        long long lastSyncTimestamp{0};
        double avgSyncLatencyMs{0.0};
    };
    ReplicationStats GetReplicationStats() const;
    bool SetReplicaRole(const std::string& replicaId, ReplicaRole role);
    bool SetReplicaMode(const std::string& replicaId, ReplicaMode mode);

    bool SaveReplicatorState(const std::string& filePath) const;
    bool LoadReplicatorState(const std::string& filePath);
    void Clear();

private:
    std::unordered_map<std::string, ReplicaDescriptor> m_replicas;
    std::unordered_map<std::string, SyncCheckpoint> m_checkpoints;
    std::unordered_map<std::string, ConflictRecord> m_conflicts;
    ReplicationPolicy m_policy;
    int m_nextReplicaIndex{0};
    int m_nextCheckpointIndex{0};
    int m_nextConflictIndex{0};
};

} // namespace Atlas::Engine
