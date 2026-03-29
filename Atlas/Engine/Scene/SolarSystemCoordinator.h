#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 39C — Coordinator for cross-system resource allocation, priority scheduling, and inter-system communication.
class SolarSystemCoordinator {
public:
    enum class CoordinatorMode { Passive, Active, Arbitrating, Synchronizing, Recovering, Shutdown, Custom };
    enum class ResourceType { CPU, GPU, Memory, IO, Network, Physics, AI, Custom };
    enum class AllocationPolicy { FirstFit, BestFit, WorstFit, RoundRobin, PriorityBased, Custom };
    enum class SyncEventType { ResourceGranted, ResourceRevoked, SystemJoined, SystemLeft, PriorityChanged, ConflictResolved, Custom };

    struct ResourceSlotDef {
        std::string slotId;
        std::string systemId;
        ResourceType resType{ResourceType::CPU};
        AllocationPolicy policy{AllocationPolicy::PriorityBased};
        double allocatedUnits{0.0};
        double maxUnits{100.0};
        int priority{0};
        bool reserved{false};
    };

    struct SystemParticipant {
        std::string participantId;
        std::string systemName;
        CoordinatorMode mode{CoordinatorMode::Passive};
        std::vector<std::string> slotIds;
        int activePriority{0};
        double cpuWeight{1.0};
        double memoryWeight{1.0};
        bool online{false};
    };

    struct SyncRecord {
        std::string recordId;
        std::string participantId;
        SyncEventType eventType{SyncEventType::SystemJoined};
        std::string detail;
        long long timestamp{0};
        bool acknowledged{false};
    };

    // Participant management
    bool RegisterParticipant(const SystemParticipant& participant);
    bool UnregisterParticipant(const std::string& participantId);
    bool SetParticipantMode(const std::string& participantId, CoordinatorMode mode);
    bool SetParticipantPriority(const std::string& participantId, int priority);
    bool SetOnline(const std::string& participantId, bool online);
    const SystemParticipant* GetParticipant(const std::string& participantId) const;
    std::vector<std::string> GetAllParticipantIds() const;
    std::vector<std::string> GetOnlineParticipants() const;
    std::vector<std::string> GetOfflineParticipants() const;

    // Resource slot management
    bool AllocateSlot(const ResourceSlotDef& slot);
    bool DeallocateSlot(const std::string& slotId);
    bool ReserveSlot(const std::string& slotId);
    bool ReleaseSlot(const std::string& slotId);
    bool SetAllocationPolicy(const std::string& slotId, AllocationPolicy policy);
    const ResourceSlotDef* GetSlot(const std::string& slotId) const;
    std::vector<std::string> GetAllSlotIds() const;
    std::vector<std::string> GetSlotsBySystem(const std::string& systemId) const;
    std::vector<std::string> GetSlotsByResourceType(ResourceType resType) const;
    std::vector<std::string> GetReservedSlots() const;

    // Synchronization
    void RecordSyncEvent(const SyncRecord& record);
    bool AcknowledgeSyncEvent(const std::string& recordId);
    const SyncRecord* GetSyncRecord(const std::string& recordId) const;
    std::vector<std::string> GetSyncByParticipant(const std::string& participantId) const;
    std::vector<std::string> GetUnacknowledgedEvents() const;
    void FlushSyncLog();

    void Reset();

private:
    std::unordered_map<std::string, SystemParticipant> m_participants;
    std::unordered_map<std::string, ResourceSlotDef> m_slots;
    std::unordered_map<std::string, SyncRecord> m_syncLog;
    CoordinatorMode m_globalMode{CoordinatorMode::Passive};
};

} // namespace Atlas::Engine
