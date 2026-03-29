#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P21 Tool — Pixel streaming session configuration, encoder settings, and client connection management.
class PixelStreamingTool : public ITool {
public:
    enum class StreamingSessionState { Idle, Initializing, Running, Paused, Stopping, Error, Custom };
    enum class EncoderPreset { UltraFast, SuperFast, Fast, Medium, Slow, VerySlow, Custom };
    enum class ClientConnectionState { Disconnected, Connecting, Connected, Authenticating, Streaming, Error, Custom };

    struct StreamingSessionConfig {
        std::string sessionId;
        std::string name;
        int targetBitrateMbps{20};
        int targetFPS{60};
        int resolutionWidth{1920};
        int resolutionHeight{1080};
        EncoderPreset encoderPreset{EncoderPreset::Fast};
        bool adaptiveBitrate{true};
        std::string signallingServerUrl;
    };

    struct EncoderSettingsDef {
        std::string encoderId;
        std::string sessionId;
        EncoderPreset preset{EncoderPreset::Fast};
        int keyframeIntervalS{2};
        int bFrameCount{0};
        float rateControlFactor{1.0f};
        bool enableHardwareAccel{true};
        std::string codecName;
    };

    struct ClientConnectionRecord {
        std::string connectionId;
        std::string sessionId;
        std::string clientAddress;
        ClientConnectionState state{ClientConnectionState::Disconnected};
        float latencyMs{0.0f};
        long long connectedAt{0};
        int receivedFrames{0};
        bool authenticated{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "PixelStreamingTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateSession(const StreamingSessionConfig& config);
    bool DeleteSession(const std::string& sessionId);
    bool StartSession(const std::string& sessionId);
    bool StopSession(const std::string& sessionId);
    bool PauseSession(const std::string& sessionId);
    const StreamingSessionConfig* GetSession(const std::string& sessionId) const;
    std::vector<std::string> GetAllSessionIds() const;
    std::vector<std::string> GetRunningSessionIds() const;

    std::string ConfigureEncoder(const EncoderSettingsDef& settings);
    bool RemoveEncoderConfig(const std::string& encoderId);
    bool SetEncoderPreset(const std::string& encoderId, EncoderPreset preset);
    bool SetBitrate(const std::string& sessionId, int bitrateMbps);
    bool SetTargetFPS(const std::string& sessionId, int fps);
    bool SetResolution(const std::string& sessionId, int width, int height);
    bool SetAdaptiveBitrate(const std::string& sessionId, bool enabled);
    const EncoderSettingsDef* GetEncoderConfig(const std::string& encoderId) const;

    std::string RegisterClient(const ClientConnectionRecord& record);
    bool DisconnectClient(const std::string& connectionId);
    bool AuthenticateClient(const std::string& connectionId);
    const ClientConnectionRecord* GetClient(const std::string& connectionId) const;
    std::vector<std::string> GetClientsBySession(const std::string& sessionId) const;
    std::vector<std::string> GetConnectedClients() const;
    int GetTotalClientCount() const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, StreamingSessionConfig> m_sessions;
    std::unordered_map<std::string, EncoderSettingsDef> m_encoderConfigs;
    std::unordered_map<std::string, ClientConnectionRecord> m_clients;
    int m_nextSessionIndex{0};
};

} // namespace Atlas::Editor
