#pragma once
#include <string>
#include <vector>
#include <functional>

namespace Atlas::Engine {

/// Phase 23C — Scheduler for timed and recurring solar system events.
/// Manages time-based triggers such as scheduled faction spawns, dynamic
/// event windows, orbit phase updates, and cross-system synchronisation pulses.
class SolarSystemScheduler {
public:
    enum class TriggerType { Once, Repeating, OrbitalPhase, CrossSystem };
    enum class EventPriority { Low, Normal, High, Critical };
    enum class SchedulerState { Stopped, Running, Paused };

    struct ScheduledEvent {
        std::string eventId;
        std::string systemId;
        std::string eventTag;
        TriggerType triggerType{TriggerType::Once};
        EventPriority priority{EventPriority::Normal};
        double triggerTimeSeconds{0.0};
        double intervalSeconds{0.0};     // > 0 for Repeating
        double orbitalPhaseRad{0.0};     // for OrbitalPhase
        std::string linkedSystemId;      // for CrossSystem
        bool enabled{true};
        bool fired{false};
        int fireCount{0};
        std::string payload;             // optional JSON payload
    };

    using EventCallback = std::function<void(const ScheduledEvent&)>;

    // Scheduler lifecycle
    void Start();
    void Pause();
    void Resume();
    void Stop();
    SchedulerState GetState() const { return m_state; }
    bool IsRunning() const { return m_state == SchedulerState::Running; }

    // Tick — advance simulation time, fire due events
    int Tick(double deltaSeconds);
    double GetCurrentTime() const { return m_currentTime; }
    void ResetTime();
    void SetTime(double timeSeconds);

    // Event registration
    std::string ScheduleOnce(const std::string& systemId, const std::string& tag,
                              double triggerTimeSeconds,
                              EventPriority priority = EventPriority::Normal,
                              const std::string& payload = "");
    std::string ScheduleRepeating(const std::string& systemId, const std::string& tag,
                                   double firstTriggerSeconds, double intervalSeconds,
                                   EventPriority priority = EventPriority::Normal);
    std::string ScheduleOrbitalPhase(const std::string& systemId, const std::string& tag,
                                      double orbitalPhaseRad,
                                      EventPriority priority = EventPriority::Normal);
    std::string ScheduleCrossSystem(const std::string& systemId,
                                     const std::string& linkedSystemId,
                                     const std::string& tag,
                                     double triggerTimeSeconds);
    bool CancelEvent(const std::string& eventId);
    bool EnableEvent(const std::string& eventId, bool enabled);
    bool IsScheduled(const std::string& eventId) const;

    // Queries
    int GetEventCount() const { return static_cast<int>(m_events.size()); }
    int GetPendingCount() const;
    int GetFiredCount() const;
    int GetEnabledCount() const;
    std::vector<std::string> GetEventIdsForSystem(const std::string& systemId) const;
    std::vector<std::string> GetEventsByPriority(EventPriority priority) const;
    std::vector<std::string> GetEventsByTag(const std::string& tag) const;
    const ScheduledEvent* GetEvent(const std::string& eventId) const;
    std::vector<std::string> GetAllEventIds() const;
    std::vector<std::string> GetUpcomingEvents(double withinSeconds) const;

    // Callbacks
    void SetOnEventFiredCallback(EventCallback cb);
    void SetOnEventCancelledCallback(EventCallback cb);

    // Bulk operations
    int CancelAllForSystem(const std::string& systemId);
    int EnableAllForSystem(const std::string& systemId, bool enabled);

    // Persistence
    void Clear();

private:
    SchedulerState m_state{SchedulerState::Stopped};
    double m_currentTime{0.0};
    std::vector<ScheduledEvent> m_events;
    EventCallback m_onFired;
    EventCallback m_onCancelled;
    int m_nextEventIndex{0};
};

} // namespace Atlas::Engine
