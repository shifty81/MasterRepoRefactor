#pragma once
#include <string>
#include <vector>
#include <functional>

namespace Atlas::Engine {

/// Phase 22C — Decoupled event bus for solar system lifecycle events.
/// Allows multiple systems (AI, UI, PCG, persistence) to react to
/// solar system state changes without tight coupling.
class SolarSystemEventBus {
public:
    enum class EventType {
        SystemRegistered,
        SystemUnregistered,
        SystemLoaded,
        SystemUnloaded,
        CelestialAdded,
        CelestialRemoved,
        SystemLinked,
        SystemUnlinked,
        SystemSerialised,
        SystemDeserialised,
    };

    struct SolarSystemEvent {
        EventType type;
        std::string systemId;
        std::string secondaryId;   // celestialId, linkedSystemId, etc.
        std::string payload;       // optional JSON payload
    };

    using EventHandler = std::function<void(const SolarSystemEvent&)>;

    // Subscription
    int Subscribe(EventType type, EventHandler handler);
    bool Unsubscribe(int handlerId);
    void UnsubscribeAll();
    int GetHandlerCount(EventType type) const;
    int GetTotalHandlerCount() const;

    // Publishing
    void Publish(const SolarSystemEvent& event);
    void PublishSystemRegistered(const std::string& systemId);
    void PublishSystemLoaded(const std::string& systemId);
    void PublishSystemUnloaded(const std::string& systemId);
    void PublishCelestialAdded(const std::string& systemId,
                               const std::string& celestialId);
    void PublishSystemLinked(const std::string& systemId,
                             const std::string& linkedId);

    // History / replay
    int GetPublishedCount() const { return m_publishedCount; }
    void ResetCount() { m_publishedCount = 0; }
    const std::vector<SolarSystemEvent>& GetRecentEvents(int maxCount = 50) const;
    void ClearHistory();

    // Singleton access
    static SolarSystemEventBus& Instance();

private:
    int m_publishedCount{0};
    std::vector<SolarSystemEvent> m_history;
    int m_nextHandlerId{1};
};

} // namespace Atlas::Engine
