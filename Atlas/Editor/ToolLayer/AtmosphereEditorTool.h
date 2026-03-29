#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P7 Tool — Configure sky, atmosphere, fog, and weather visual parameters.
class AtmosphereEditorTool : public ITool {
public:
    struct AtmosphereSettings {
        float sunAzimuth{180.0f};
        float sunElevation{45.0f};
        float sunIntensity{1.0f};
        float fogDensity{0.01f};
        float fogHeightFalloff{0.2f};
        float rayleighScattering{1.0f};
        float mieScattering{0.1f};
        float ozoneDensity{1.0f};
        std::string skyboxAsset;
        bool volumetricClouds{true};
        float cloudCoverage{0.4f};
        float cloudHeight{2000.0f};
    };

    struct WeatherPreset {
        std::string presetId;
        std::string name;
        AtmosphereSettings settings;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AtmosphereEditorTool"; }
    bool IsActive() const override { return m_active; }

    void SetSunPosition(float azimuth, float elevation);
    void SetFogDensity(float density, float heightFalloff = 0.2f);
    void SetRayleighScattering(float value);
    void SetMieScattering(float value);
    void SetCloudParameters(float coverage, float height);
    void SetVolumetricClouds(bool enabled);
    AtmosphereSettings GetCurrentSettings() const { return m_current; }

    std::string SavePreset(const std::string& name);
    bool LoadPreset(const std::string& presetId);
    bool RemovePreset(const std::string& presetId);
    int GetPresetCount() const { return static_cast<int>(m_presets.size()); }
    std::vector<std::string> GetPresetIds() const;
    void BlendToPreset(const std::string& presetId, float duration);
    bool IsBlending() const { return m_blending; }

private:
    bool m_active{false};
    bool m_blending{false};
    AtmosphereSettings m_current;
    std::vector<WeatherPreset> m_presets;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
