#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P16 Tool — Volumetric cloud layer authoring, density painting, and atmospheric coverage management.
class VolumetricCloudTool : public ITool {
public:
    enum class CloudLayer { Cirrus, Cumulus, Stratus, Cumulonimbus, Nimbostratus, Custom };
    enum class CloudCoverage { Clear, Scattered, Broken, Overcast, Dynamic };
    enum class WeatherIntensity { Calm, Mild, Moderate, Severe, Extreme };

    struct CloudLayerDef {
        std::string layerId;
        std::string name;
        CloudLayer cloudLayer{CloudLayer::Cumulus};
        float altitude{3000.0f};
        float thickness{500.0f};
        float density{0.5f};
        CloudCoverage coverage{CloudCoverage::Scattered};
        float scatterCoeff{0.1f};
        float extinctionCoeff{0.05f};
    };

    struct CloudWeatherState {
        std::string stateId;
        WeatherIntensity intensity{WeatherIntensity::Calm};
        float windSpeed{10.0f};
        float windDirection{0.0f};
        float precipitation{0.0f};
        float visibility{10000.0f};
    };

    struct CloudAnimSettings {
        std::string animId;
        float speedX{0.0f};
        float speedY{0.0f};
        float evolveSpeed{0.01f};
        float cycleTime{300.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "VolumetricCloudTool"; }
    bool IsActive() const override { return m_active; }

    std::string AddLayer(const std::string& name, CloudLayer type = CloudLayer::Cumulus);
    bool RemoveLayer(const std::string& layerId);
    bool SetLayerDensity(const std::string& layerId, float density);
    bool SetLayerAltitude(const std::string& layerId, float altitude);
    bool SetLayerCoverage(const std::string& layerId, CloudCoverage coverage);
    bool SetWeatherState(const CloudWeatherState& state);
    bool ApplyWeatherState(const std::string& stateId);
    bool BlendWeatherStates(const std::string& fromId, const std::string& toId, float alpha);
    bool SetAnimSettings(const std::string& layerId, const CloudAnimSettings& settings);
    bool PreviewClouds();
    const CloudLayerDef* GetLayerById(const std::string& layerId) const;
    std::vector<std::string> GetAllLayers() const;
    int GetLayerCount() const { return static_cast<int>(m_layers.size()); }
    const CloudWeatherState* GetWeatherState(const std::string& stateId) const;
    bool SimulateWeather(float durationSeconds);
    bool ExportCloudConfig(const std::string& filePath) const;
    bool SaveCloudConfig(const std::string& filePath) const;
    bool LoadCloudConfig(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, CloudLayerDef> m_layers;
    std::unordered_map<std::string, CloudWeatherState> m_weatherStates;
    std::unordered_map<std::string, CloudAnimSettings> m_animSettings;
    int m_nextLayerIndex{0};
};

} // namespace Atlas::Editor
