#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 28C/31C — Profiler for solar system simulation performance metrics, tick budgets, and bottleneck detection.
/// Phase 28C introduced the record registry API (RegisterRecord, TakeSnapshot, RunAnalysis, GetBottleneckMetrics).
/// Phase 31C extended the profiler with SamplingMode, MetricSeries, and detailed configuration support.
class SolarSystemProfiler {
public:
    enum class ProfilerState { Idle, Profiling, Paused, Complete, Error };
    enum class MetricCategory { Simulation, Physics, AI, Rendering, Streaming, Audio, Network };
    enum class SamplingMode { Continuous, Sampled, OnDemand, Triggered };
    enum class SampleResolution { Low, Medium, High, Ultra, Adaptive };

    struct ProfileMetric {
        std::string metricId;
        MetricCategory category{MetricCategory::Simulation};
        std::string name;
        float value{0.0f};
        float budgetMs{16.67f};
        SampleResolution resolution{SampleResolution::Medium};
    };

    struct SystemLoadSnapshot {
        std::string snapshotId;
        double timestamp{0.0};
        std::vector<ProfileMetric> metrics;
        float cpuLoad{0.0f};
        float gpuLoad{0.0f};
        float memoryMb{0.0f};
    };

    struct ProfileSession {
        std::string sessionId;
        std::string systemId;
        double startTime{0.0};
        double endTime{0.0};
        SamplingMode mode{SamplingMode::Continuous};
        std::vector<std::string> snapshotIds;
    };

    struct ProfileRecord {
        std::string recordId;
        std::string systemId;
        std::string systemName;
        ProfilerState state{ProfilerState::Idle};
        ProfileSession session;
        std::vector<std::string> metrics;
        int totalSamples{0};
        bool analysisComplete{false};
    };

    struct ProfileSample {
        std::string sampleId;
        MetricCategory category{MetricCategory::Simulation};
        std::string label;
        float durationMs{0.0f};
        float memoryKb{0.0f};
        int frameIndex{0};
        double timestamp{0.0};
    };

    struct MetricSeries {
        std::string seriesId;
        MetricCategory category{MetricCategory::Simulation};
        std::string label;
        std::vector<std::string> samples;
        int maxSamples{1000};
        float rollingAvg{0.0f};
    };

    struct ProfilerConfig {
        std::string configId;
        SamplingMode samplingMode{SamplingMode::Continuous};
        float sampleRate{60.0f};
        float budgetMs{16.67f};
        std::vector<MetricCategory> categories;
        bool captureStackTrace{false};
    };

    // Phase 28C — record registry methods
    bool RegisterRecord(const ProfileRecord& record);
    bool RemoveRecord(const std::string& recordId);
    const ProfileRecord* FindRecord(const std::string& recordId) const;
    std::vector<std::string> ListRecordIds() const;
    bool HasRecord(const std::string& recordId) const;
    int Count() const { return static_cast<int>(m_records.size()); }
    void Clear();

    // Snapshot / analysis
    SystemLoadSnapshot TakeSnapshot(const std::string& systemId);
    bool RunAnalysis(const std::string& recordId);
    std::vector<ProfileMetric> GetBottleneckMetrics(float thresholdMs = 8.0f) const;

    // Profiler lifecycle
    bool StartProfiling();
    bool StopProfiling();
    bool PauseProfiling();
    bool ResumeProfiling();

    // Recording
    bool RecordSample(const ProfileSample& sample);
    bool RecordSeries(const MetricSeries& series);

    // Queries
    const ProfileSample* GetSample(const std::string& sampleId) const;
    const MetricSeries* GetSeries(const std::string& seriesId) const;
    std::vector<std::string> GetAllSampleIds() const;
    std::vector<std::string> GetSeriesByCategory(MetricCategory category) const;
    ProfilerState GetProfilerState() const { return m_state; }

    // Configuration
    bool SetConfig(const ProfilerConfig& config);
    const ProfilerConfig& GetConfig() const { return m_config; }

    // Analysis
    float GetAverageForCategory(MetricCategory category) const;
    float GetPeakForCategory(MetricCategory category) const;
    std::vector<std::string> DetectBottlenecks(float thresholdMs = 8.0f) const;

    // Persistence
    bool ExportProfile(const std::string& filePath) const;
    bool LoadProfile(const std::string& filePath);
    void ClearSamples();
    void Reset();

private:
    ProfilerState m_state{ProfilerState::Idle};
    ProfilerConfig m_config;
    std::unordered_map<std::string, ProfileSample> m_samples;
    std::unordered_map<std::string, MetricSeries> m_series;
    std::unordered_map<std::string, ProfileRecord> m_records;
};

} // namespace Atlas::Engine
