#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P16 Tool — Haptic feedback pattern authoring, controller rumble design, and force feedback sequencing.
class HapticFeedbackTool : public ITool {
public:
    enum class HapticDevice { DualSense, XboxController, ViveController, OculusTouch, SteelSeriesGG, Custom };
    enum class MotorType { LargeMotor, SmallMotor, TriggerL, TriggerR, AdaptiveL, AdaptiveR };
    enum class HapticEffect { Click, Buzz, Pulse, Ramp, Waveform, Custom };

    struct HapticPulse {
        std::string pulseId;
        MotorType motorType{MotorType::LargeMotor};
        float intensity{1.0f};
        float duration{0.1f};
        float frequency{60.0f};
        float envelope{0.0f};
    };

    struct HapticPattern {
        std::string patternId;
        std::string name;
        HapticDevice device{HapticDevice::DualSense};
        std::vector<std::string> pulses;
        bool looping{false};
        int loopCount{1};
    };

    struct HapticTriggerSettings {
        std::string triggerId;
        HapticEffect effect{HapticEffect::Click};
        float startPosition{0.0f};
        float endPosition{1.0f};
        float force{1.0f};
        float stiffness{0.5f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "HapticFeedbackTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreatePattern(const std::string& name, HapticDevice device = HapticDevice::DualSense);
    bool RemovePattern(const std::string& patternId);
    std::string AddPulse(const std::string& patternId, MotorType motor, float intensity, float duration);
    bool RemovePulse(const std::string& patternId, const std::string& pulseId);
    bool SetTriggerSettings(const HapticTriggerSettings& settings);
    bool PreviewPattern(const std::string& patternId);
    bool PreviewTrigger(const std::string& triggerId);
    bool ExportPattern(const std::string& patternId, const std::string& filePath) const;
    const HapticPattern* GetPattern(const std::string& patternId) const;
    std::vector<std::string> GetAllPatternIds() const;
    int GetPulseCount(const std::string& patternId) const;
    bool SetDevice(const std::string& patternId, HapticDevice device);
    bool SetMotorIntensity(const std::string& patternId, MotorType motor, float intensity);
    std::vector<std::string> GetSupportedDevices() const;
    bool ValidatePattern(const std::string& patternId) const;
    bool SavePatterns(const std::string& filePath) const;
    bool LoadPatterns(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, HapticPattern> m_patterns;
    std::unordered_map<std::string, HapticPulse> m_pulses;
    std::unordered_map<std::string, HapticTriggerSettings> m_triggerSettings;
    int m_nextPatternIndex{0};
    int m_nextPulseIndex{0};
};

} // namespace Atlas::Editor
