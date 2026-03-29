#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 36D — Registry for event body definitions used by the event-driven gameplay and trigger subsystem.
class EventBodyRegistry {
public:
    enum class EventBodyState { Idle, Listening, Triggered, Processing, Completed, Failed, Disabled, Custom };
    enum class EventBodyScope { Global, Local, Team, Channel, Instance, World, Custom };
    enum class TriggerType { OnEnter, OnExit, OnOverlap, OnTimer, OnSignal, OnCondition, OnInput, Custom };
    enum class EventPriority { Critical, High, Normal, Low, Deferred, Custom };
    enum class EventBodyFlags { None_, Persistent, Repeatable, Networked, Serializable, Ordered, Custom };

    struct TriggerConfig {
        std::string configId;
        TriggerType triggerType{TriggerType::OnSignal};
        EventPriority priority{EventPriority::Normal};
        float debounceMs{0.0f};
        int maxTriggers{0};
        float cooldownMs{0.0f};
        bool persistent{false};
    };

    struct EventPayload {
        std::string payloadId;
        std::string bodyId;
        std::string eventType;
        std::string data;
        std::string sender;
        std::vector<std::string> recipients;
        long long timestamp{0};
        int sequenceId{0};
    };

    struct EventBodyRecord {
        std::string bodyId;
        std::string name;
        EventBodyScope scope{EventBodyScope::Global};
        EventBodyFlags flags{EventBodyFlags::None_};
        TriggerConfig triggerConfig;
        std::vector<std::string> payloads;
        std::string channelId;
        std::string ownerId;
        EventBodyState bodyState{EventBodyState::Idle};
        int triggerCount{0};
        long long lastTriggeredAt{0};
    };

    // Body registration
    bool RegisterBody(const EventBodyRecord& record);
    bool UnregisterBody(const std::string& bodyId);

    // State and configuration
    bool SetBodyScope(const std::string& bodyId, EventBodyScope scope);
    bool SetBodyState(const std::string& bodyId, EventBodyState state);
    bool SetBodyFlags(const std::string& bodyId, EventBodyFlags flags);
    bool SetTriggerType(const std::string& bodyId, TriggerType type);
    bool SetTriggerPriority(const std::string& bodyId, EventPriority priority);
    bool SetDebounce(const std::string& bodyId, float debounceMs);
    bool SetCooldown(const std::string& bodyId, float cooldownMs);
    bool SetMaxTriggers(const std::string& bodyId, int maxTriggers);
    bool SetChannel(const std::string& bodyId, const std::string& channelId);
    bool SetOwner(const std::string& bodyId, const std::string& ownerId);

    // Payload management
    bool AddPayload(const std::string& bodyId, const EventPayload& payload);
    bool RemovePayload(const std::string& bodyId, const std::string& payloadId);

    // Queries
    const EventBodyRecord* GetBodyById(const std::string& bodyId) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByScope(EventBodyScope scope) const;
    std::vector<std::string> GetBodiesByState(EventBodyState state) const;
    std::vector<std::string> GetBodiesByChannel(const std::string& channelId) const;
    std::vector<std::string> GetBodiesByOwner(const std::string& ownerId) const;
    std::vector<std::string> GetListeningBodies() const;
    std::vector<std::string> GetTriggeredBodies() const;
    std::vector<std::string> GetDisabledBodies() const;
    std::vector<EventPayload> GetPayloadsByBody(const std::string& bodyId) const;
    std::vector<EventPayload> GetPayloadsByType(const std::string& eventType) const;

    // Lifecycle
    bool TriggerBody(const std::string& bodyId);
    bool ResetBody(const std::string& bodyId);
    bool DisableBody(const std::string& bodyId);

    // Persistence
    void Clear();
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);

private:
    std::unordered_map<std::string, EventBodyRecord> m_bodies;
    std::unordered_map<std::string, EventPayload> m_payloads;
};

} // namespace Atlas::Engine
