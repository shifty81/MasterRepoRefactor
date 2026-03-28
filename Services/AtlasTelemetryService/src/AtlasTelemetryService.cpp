// AtlasTelemetryService.cpp
#include "AtlasTelemetryService.h"
#include <algorithm>

namespace Atlas::Services
{

void AtlasTelemetryService::initialise() {}
void AtlasTelemetryService::shutdown()   { clearListeners(); }

void AtlasTelemetryService::log(LogLevel level, const std::string& source,
                                 const std::string& message)
{
    LogEntry e;
    e.entryId      = nextEntryId_++;
    e.level        = level;
    e.source       = source;
    e.message      = message;
    e.timestampUtc = "stub-timestamp";
    logs_.push_back(e);

    if (level >= LogLevel::Error)
    {
        ++health_.errorCount;
        health_.lastError = message;
        health_.servicesHealthy = false;
    }
    else if (level == LogLevel::Warning)
    {
        ++health_.warningCount;
    }

    for (const auto& l : logListeners_)
        l(e);
}

void AtlasTelemetryService::emit(const TelemetryEvent& event)
{
    events_.push_back(event);
    for (const auto& l : eventListeners_)
        l(event);
}

std::vector<LogEntry> AtlasTelemetryService::getRecentLogs(uint32_t maxCount) const
{
    if (logs_.size() <= maxCount) return logs_;
    return std::vector<LogEntry>(logs_.end() - maxCount, logs_.end());
}

std::vector<TelemetryEvent> AtlasTelemetryService::getRecentEvents(uint32_t maxCount) const
{
    if (events_.size() <= maxCount) return events_;
    return std::vector<TelemetryEvent>(events_.end() - maxCount, events_.end());
}

HealthSummary AtlasTelemetryService::getHealthSummary() const { return health_; }

void AtlasTelemetryService::addLogListener(LogListener l)    { logListeners_.push_back(std::move(l)); }
void AtlasTelemetryService::addEventListener(EventListener l) { eventListeners_.push_back(std::move(l)); }
void AtlasTelemetryService::clearListeners()
{
    logListeners_.clear();
    eventListeners_.clear();
}

} // namespace Atlas::Services
