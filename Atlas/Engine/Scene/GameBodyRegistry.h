#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 35D — Registry for game body definitions used by the gameplay and session subsystem.
class GameBodyRegistry {
public:
    enum class GameBodyState { Inactive, Initializing, Active, Paused, Terminating, Terminated, Error };
    enum class GameBodyRole { None_, Player, NPC, Vehicle, Projectile, Interactable, Environment, Custom };
    enum class GameEventType { Spawn, Despawn, Interact, Damage, Death, Respawn, StateChange, Custom };
    enum class GameBodyFlags { None_, Persistent, Replicated, Physics, Collidable, Interactable, Networked, Custom };
    enum class SpawnPolicy { Immediate, Deferred, Pooled, Streamed, Custom };

    struct SpawnConfig {
        std::string configId;
        SpawnPolicy policy{SpawnPolicy::Immediate};
        float spawnRadius{500.0f};
        int maxInstances{100};
        float respawnDelay{5.0f};
        int poolSize{10};
        bool persistent{false};
    };

    struct GameEventRecord {
        std::string eventId;
        std::string bodyId;
        GameEventType eventType{GameEventType::Spawn};
        long long timestamp{0};
        std::string actorId;
        std::string payload;
    };

    struct GameBodyRecord {
        std::string bodyId;
        std::string name;
        GameBodyRole role{GameBodyRole::NPC};
        GameBodyFlags flags{GameBodyFlags::None_};
        SpawnConfig spawnConfig;
        std::vector<std::string> events;
        std::string teamId;
        std::string ownerId;
        GameBodyState bodyState{GameBodyState::Inactive};
        float health{100.0f};
        float maxHealth{100.0f};
    };

    // Body registration
    bool RegisterBody(const GameBodyRecord& record);
    bool UnregisterBody(const std::string& bodyId);

    // Role, state, and flags
    bool SetBodyRole(const std::string& bodyId, GameBodyRole role);
    bool SetBodyState(const std::string& bodyId, GameBodyState state);
    bool SetBodyFlags(const std::string& bodyId, GameBodyFlags flags);

    // Spawn configuration
    bool SetSpawnPolicy(const std::string& bodyId, SpawnPolicy policy);
    bool SetMaxInstances(const std::string& bodyId, int maxInstances);
    bool SetRespawnDelay(const std::string& bodyId, float delay);

    // Ownership
    bool SetTeam(const std::string& bodyId, const std::string& teamId);
    bool SetOwner(const std::string& bodyId, const std::string& ownerId);
    bool SetHealth(const std::string& bodyId, float health);

    // Event management
    bool AddEvent(const std::string& bodyId, const GameEventRecord& event);
    bool RemoveEvent(const std::string& bodyId, const std::string& eventId);

    // Queries
    const GameBodyRecord* GetBodyById(const std::string& bodyId) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByRole(GameBodyRole role) const;
    std::vector<std::string> GetBodiesByState(GameBodyState state) const;
    std::vector<std::string> GetBodiesByTeam(const std::string& teamId) const;
    std::vector<std::string> GetBodiesByOwner(const std::string& ownerId) const;
    std::vector<std::string> GetActiveBody() const;
    std::vector<std::string> GetInactiveBodies() const;
    std::vector<std::string> GetHealthyBodies() const;
    std::vector<std::string> GetDeadBodies() const;
    std::vector<GameEventRecord> GetEventsByBody(const std::string& bodyId) const;
    std::vector<GameEventRecord> GetEventsByType(GameEventType eventType) const;

    // Lifecycle
    bool RespawnBody(const std::string& bodyId);
    bool DespawnBody(const std::string& bodyId);

    // Persistence
    void Clear();
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);

private:
    std::unordered_map<std::string, GameBodyRecord> m_bodies;
    std::unordered_map<std::string, GameEventRecord> m_events;
};

} // namespace Atlas::Engine
