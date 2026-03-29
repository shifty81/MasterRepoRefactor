#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 34C — Dispatcher for solar system events and asynchronous operation management.
class SolarSystemDispatcher {
public:
    enum class DispatchState { Idle, Queued, Running, Paused, Completed, Failed, Cancelled };
    enum class DispatchPriority { Critical, High, Normal, Low, Background, Deferred };
    enum class EventType { CelestialAdded, CelestialRemoved, StateChanged, FactionEvent, HazardAlert, AnomalyDetected, Custom };

    struct DispatchFilter {
        std::string filterId;
        std::string name;
        std::vector<std::string> allowedTypes;
        std::vector<std::string> blockedTypes;
        DispatchPriority minPriority{DispatchPriority::Background};
        DispatchPriority maxPriority{DispatchPriority::Critical};
        std::vector<std::string> systemFilter;
    };

    struct DispatchJob {
        std::string jobId;
        std::string systemId;
        EventType eventType{EventType::Custom};
        std::string payload;
        DispatchPriority priority{DispatchPriority::Normal};
        DispatchState state{DispatchState::Idle};
        int maxRetries{3};
        int retryCount{0};
        long long scheduledMs{0};
    };

    struct DispatchResult {
        std::string resultId;
        std::string jobId;
        std::string systemId;
        bool success{false};
        double elapsedMs{0.0};
        std::vector<std::string> errors;
        DispatchState dispatchState{DispatchState::Idle};
    };

    // Handler registration
    bool RegisterHandler(const std::string& handlerId, EventType eventType, const std::function<void(const DispatchJob&)>& handler);
    bool UnregisterHandler(const std::string& handlerId);

    // Job management
    std::string CreateJob(const std::string& systemId, EventType eventType, const std::string& payload, DispatchPriority priority);
    bool CancelJob(const std::string& jobId);
    bool PauseJob(const std::string& jobId);
    bool ResumeJob(const std::string& jobId);
    const DispatchJob* GetJob(const std::string& jobId) const;
    std::vector<std::string> GetAllJobIds() const;

    // Job configuration
    bool SetPriority(const std::string& jobId, DispatchPriority priority);
    bool SetMaxRetries(const std::string& jobId, int maxRetries);

    // Filter management
    bool AddFilter(const DispatchFilter& filter);
    bool RemoveFilter(const std::string& filterId);
    const DispatchFilter* GetFilter(const std::string& filterId) const;

    // Dispatch operations
    DispatchResult Dispatch(const std::string& jobId);
    bool DispatchAsync(const std::string& jobId, const std::string& callbackId);
    std::vector<DispatchResult> DispatchBatch(const std::vector<std::string>& jobIds);
    void FlushQueue();
    void DrainQueue();

    // Result access
    const DispatchResult* GetResult(const std::string& resultId) const;
    std::vector<std::string> GetAllResults() const;
    std::vector<std::string> GetJobsByState(DispatchState state) const;
    std::vector<std::string> GetJobsByPriority(DispatchPriority priority) const;
    int GetQueueDepth() const;

    // Validation and introspection
    bool ValidateJob(const std::string& jobId) const;
    std::vector<std::string> ListHandlers() const;

    // Maintenance
    void ClearResults();
    void Reset();

private:
    std::unordered_map<std::string, DispatchJob> m_jobs;
    std::unordered_map<std::string, DispatchResult> m_results;
    std::unordered_map<std::string, DispatchFilter> m_filters;
    std::unordered_map<std::string, std::function<void(const DispatchJob&)>> m_handlers;
    int m_nextJobIndex{0};
    int m_nextResultIndex{0};
};

} // namespace Atlas::Engine
