// AtlasTelemetryService.h
// Telemetry service — log streaming, diagnostics, profiling, and event broadcast.

#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include <functional>

namespace Atlas::Services
{

enum class LogLevel : uint8_t { Trace, Debug, Info, Warning, Error, Critical };

struct LogEntry
{
    uint64_t    entryId     = 0;
    LogLevel    level       = LogLevel::Info;
    std::string source;
    std::string message;
    std::string timestampUtc;
};

struct TelemetryEvent
{
    std::string eventType;   ///< e.g. "BuildStarted", "AssetImported"
    std::string source;
    std::string payload;     ///< JSON payload stub
    std::string timestampUtc;
};

struct HealthSummary
{
    bool     servicesHealthy = true;
    uint32_t errorCount      = 0;
    uint32_t warningCount    = 0;
    std::string lastError;
};

using LogListener   = std::function<void(const LogEntry&)>;
using EventListener = std::function<void(const TelemetryEvent&)>;

class AtlasTelemetryService
{
public:
    AtlasTelemetryService()  = default;
    ~AtlasTelemetryService() = default;

    void initialise();
    void shutdown();

    void log(LogLevel level, const std::string& source, const std::string& message);
    void emit(const TelemetryEvent& event);

    std::vector<LogEntry>       getRecentLogs(uint32_t maxCount = 100) const;
    std::vector<TelemetryEvent> getRecentEvents(uint32_t maxCount = 50) const;
    HealthSummary               getHealthSummary() const;

    void addLogListener(LogListener listener);
    void addEventListener(EventListener listener);
    void clearListeners();

private:
    std::vector<LogEntry>       logs_;
    std::vector<TelemetryEvent> events_;
    std::vector<LogListener>    logListeners_;
    std::vector<EventListener>  eventListeners_;
    uint64_t nextEntryId_ = 1;
    HealthSummary health_;
};

} // namespace Atlas::Services
