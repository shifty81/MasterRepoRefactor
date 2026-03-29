#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P12 Tool — Procedural camera shake authoring for gameplay and cinematic events.
class CameraShakeTool : public ITool {
public:
    enum class ShakeProfile { Impact, Explosion, Footstep, Earthquake, Heartbeat, Custom };
    enum class ShakeAxis { X, Y, Z, XY, XZ, YZ, XYZ };
    enum class Waveform { Sine, Perlin, Square, Sawtooth, Random };
    enum class FalloffCurve { Linear, Quadratic, Exponential, EaseInOut };

    struct ShakeChannel {
        std::string channelId;
        ShakeAxis axis{ShakeAxis::XY};
        Waveform waveform{Waveform::Perlin};
        float amplitude{0.1f};
        float frequency{10.0f};
        float phase{0.0f};
        float noise{0.0f};
        bool enabled{true};
    };

    struct ShakeEnvelope {
        float attackTime{0.05f};
        float sustainTime{0.2f};
        float releaseTime{0.3f};
        FalloffCurve falloffCurve{FalloffCurve::EaseInOut};
        float peakAmplitudeScale{1.0f};
    };

    struct ShakePreset {
        std::string presetId;
        std::string name;
        ShakeProfile profile{ShakeProfile::Impact};
        ShakeEnvelope envelope;
        std::vector<ShakeChannel> channels;
        float globalAmplitudeScale{1.0f};
        float globalFrequencyScale{1.0f};
        float maxDistance{50.0f};
        float innerRadius{5.0f};
        bool loop{false};
        float loopInterval{0.0f};
        bool affectPosition{true};
        bool affectRotation{true};
        bool affectFOV{false};
        float fovAmplitude{0.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "CameraShakeTool"; }
    bool IsActive() const override { return m_active; }

    // Preset management
    std::string CreatePreset(const std::string& name,
                              ShakeProfile profile = ShakeProfile::Impact);
    bool RemovePreset(const std::string& presetId);
    bool DuplicatePreset(const std::string& srcId, const std::string& newName);
    bool SetProfile(const std::string& presetId, ShakeProfile profile);
    bool SetGlobalAmplitudeScale(const std::string& presetId, float scale);
    bool SetGlobalFrequencyScale(const std::string& presetId, float scale);
    bool SetMaxDistance(const std::string& presetId, float dist);
    bool SetInnerRadius(const std::string& presetId, float radius);
    bool SetLoop(const std::string& presetId, bool loop, float interval = 0.0f);
    bool SetAffectsPosition(const std::string& presetId, bool affect);
    bool SetAffectsRotation(const std::string& presetId, bool affect);
    bool SetAffectsFOV(const std::string& presetId, bool affect, float amplitude = 0.0f);
    int GetPresetCount() const { return static_cast<int>(m_presets.size()); }
    const ShakePreset* GetPreset(const std::string& presetId) const;
    std::vector<std::string> GetPresetIds() const;

    // Envelope settings
    bool SetAttackTime(const std::string& presetId, float seconds);
    bool SetSustainTime(const std::string& presetId, float seconds);
    bool SetReleaseTime(const std::string& presetId, float seconds);
    bool SetFalloffCurve(const std::string& presetId, FalloffCurve curve);
    bool SetPeakAmplitudeScale(const std::string& presetId, float scale);

    // Channel management
    std::string AddChannel(const std::string& presetId,
                            ShakeAxis axis = ShakeAxis::XY,
                            Waveform waveform = Waveform::Perlin);
    bool RemoveChannel(const std::string& presetId,
                        const std::string& channelId);
    bool SetChannelAmplitude(const std::string& presetId,
                               const std::string& channelId, float amplitude);
    bool SetChannelFrequency(const std::string& presetId,
                              const std::string& channelId, float frequency);
    bool SetChannelPhase(const std::string& presetId,
                          const std::string& channelId, float phase);
    bool SetChannelNoise(const std::string& presetId,
                          const std::string& channelId, float noise);
    bool SetChannelEnabled(const std::string& presetId,
                            const std::string& channelId, bool enabled);
    int GetChannelCount(const std::string& presetId) const;

    // Preview
    bool PreviewPreset(const std::string& presetId);
    bool StopPreview();
    bool IsPreviewPlaying() const { return m_previewPlaying; }

    // Persistence
    bool SavePresets(const std::string& filePath) const;
    bool LoadPresets(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    bool m_previewPlaying{false};
    std::unordered_map<std::string, ShakePreset> m_presets;
    int m_nextPresetIndex{0};
    int m_nextChannelIndex{0};
};

} // namespace Atlas::Editor
