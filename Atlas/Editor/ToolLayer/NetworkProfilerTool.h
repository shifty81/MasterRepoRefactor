#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P23 Tool — Network profiler for bandwidth, latency, and packet loss visualization in multiplayer sessions.
class NetworkProfilerTool : public ITool {
public:
    enum class ProfilerSessionState { Idle, Recording, Paused, Completed, Analyzing, Error, Custom };
    enum class NetworkMetricType { Bandwidth, Latency, PacketLoss, RTT, Jitter, Custom };
    enum class CaptureFilter { AllTraffic, GameplayOnly, RPCOnly, ReplicationOnly, Custom };
    enum class AnalysisMode { RealTime, PostProcess, Comparison, Custom };

    struct NetworkSampleDef {
        std::string sampleId;
        std::string sessionId;
        NetworkMetricType metricType{NetworkMetricType::Bandwidth};
        double value{0.0};
        long long timestamp{0};
    };

    struct ProfilerSessionConfig {
        std::string sessionId;
        std::string sessionName;
        ProfilerSessionState state{ProfilerSessionState::Idle};
        CaptureFilter filter{CaptureFilter::AllTraffic};
        int maxSamples{10000};
        float sampleIntervalMs{16.0f};
    };

    struct NetworkAnomalyRecord {
        std::string anomalyId;
        std::string sessionId;
        NetworkMetricType metricType{NetworkMetricType::Latency};
        double threshold{0.0};
        double actualValue{0.0};
        bool acknowledged{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "NetworkProfilerTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateSession(const ProfilerSessionConfig& config);
    bool DeleteSession(const std::string& sessionId);
    const ProfilerSessionConfig* GetSession(const std::string& sessionId) const;
    std::vector<std::string> GetAllSessionIds() const;
    bool StartRecording(const std::string& sessionId);
    bool PauseRecording(const std::string& sessionId);
    bool StopRecording(const std::string& sessionId);
    bool AddSample(const std::string& sessionId, const NetworkSampleDef& sample);
    const NetworkSampleDef* GetSample(const std::string& sampleId) const;
    std::vector<std::string> GetSamplesBySession(const std::string& sessionId) const;
    std::vector<std::string> GetSamplesByMetric(NetworkMetricType metricType) const;
    std::vector<std::string> DetectAnomalies(const std::string& sessionId) const;
    const NetworkAnomalyRecord* GetAnomaly(const std::string& anomalyId) const;
    std::vector<std::string> GetAnomaliesBySession(const std::string& sessionId) const;
    bool AcknowledgeAnomaly(const std::string& anomalyId);
    bool ExportSession(const std::string& sessionId, const std::string& outputPath) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, ProfilerSessionConfig> m_sessions;
    std::unordered_map<std::string, NetworkSampleDef> m_samples;
    std::unordered_map<std::string, NetworkAnomalyRecord> m_anomalies;
    int m_nextSessionIndex{0};
};

} // namespace Atlas::Editor
