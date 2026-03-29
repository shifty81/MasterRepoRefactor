#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 28C — Solar system profiler for runtime performance analysis, resource
/// tracking, and simulation quality metrics across multi-system space scenes.
class SolarSystemProfiler {
public:
    enum class ProfilerState { Idle, Profiling, Paused, Completed };
    enum class MetricCategory { Rendering, Simulation, Streaming, AI, Network };
    enum class SampleResolution { Low, Medium, High, Ultra };

    struct ProfileMetric {
        std::string metricId;
        std::string name;
        MetricCategory category{MetricCategory::Rendering};
        float value{0.0f};
        float minValue{0.0f};
        float maxValue{0.0f};
        float avgValue{0.0f};
        std::string unit;
        bool enabled{true};
    };

    struct SystemLoadSnapshot {
        std::string snapshotId;
        std::string systemId;
        float cpuUsagePercent{0.0f};
        float gpuUsagePercent{0.0f};
        float memoryUsageMB{0.0f};
        float drawCallCount{0.0f};
        int activeCelestials{0};
        float simulationStepMs{0.0f};
        std::string timestamp;
    };

    struct ProfileSession {
        std::string sessionId;
        std::string systemId;
        std::string systemName;
        float durationSeconds{0.0f};
        SampleResolution resolution{SampleResolution::Medium};
        bool captureGPU{true};
        bool captureCPU{true};
        bool captureMemory{true};
        bool captureNetwork{false};
        std::string outputPath;
    };

    struct ProfileRecord {
        std::string recordId;
        std::string systemId;
        std::string systemName;
        ProfilerState state{ProfilerState::Idle};
        ProfileSession session;
        std::vector<ProfileMetric> metrics;
        std::vector<SystemLoadSnapshot> snapshots;
        float avgFrameTimeMs{0.0f};
        float peakFrameTimeMs{0.0f};
        float avgCelestialCount{0.0f};
        int totalSamples{0};
        bool analysisComplete{false};
        std::string createdAt;
        std::string completedAt;
        std::string notes;
    };

    // Record management
    void RegisterRecord(const ProfileRecord& entry);
    const ProfileRecord* FindRecord(const std::string& id) const;
    std::vector<std::string> ListRecordIds() const;
    bool HasRecord(const std::string& id) const;
    void RemoveRecord(const std::string& id);
    size_t Count() const;
    void Clear();

    // Profiling control
    bool StartProfiling(const std::string& recordId);
    bool PauseProfiling(const std::string& recordId);
    bool ResumeProfiling(const std::string& recordId);
    bool StopProfiling(const std::string& recordId);
    bool IsProfileing(const std::string& recordId) const;
    float GetProgress(const std::string& recordId) const;

    // Metric management
    bool AddMetric(const std::string& recordId, const ProfileMetric& metric);
    bool RemoveMetric(const std::string& recordId, const std::string& metricId);
    const ProfileMetric* GetMetric(const std::string& recordId,
                                    const std::string& metricId) const;
    std::vector<ProfileMetric> GetMetricsByCategory(const std::string& recordId,
                                                      MetricCategory category) const;

    // Snapshot management
    bool TakeSnapshot(const std::string& recordId);
    bool AddSnapshot(const std::string& recordId, const SystemLoadSnapshot& snapshot);
    int GetSnapshotCount(const std::string& recordId) const;
    std::vector<SystemLoadSnapshot> GetSnapshots(const std::string& recordId) const;

    // Analysis
    bool RunAnalysis(const std::string& recordId);
    float GetAverageFrameTime(const std::string& recordId) const;
    float GetPeakMemoryUsage(const std::string& recordId) const;
    std::vector<std::string> GetBottleneckMetrics(const std::string& recordId) const;
    std::vector<std::string> FindByState(ProfilerState state) const;
    std::vector<std::string> FindBySystem(const std::string& systemId) const;
    std::vector<std::string> GetCompletedRecordIds() const;

    // Statistics
    int GetProfilingCount() const;
    float GetTotalProfiledTime() const;

    // Callbacks
    using ProfileCompleteCallback = std::function<void(const std::string&)>;
    void SetOnProfileCompleteCallback(ProfileCompleteCallback cb);

    // Persistence
    bool SaveProfile(const std::string& recordId, const std::string& filePath) const;
    bool LoadProfile(const std::string& filePath);

private:
    std::unordered_map<std::string, ProfileRecord> m_records;
    ProfileCompleteCallback m_onProfileComplete;
};

} // namespace Atlas::Engine
