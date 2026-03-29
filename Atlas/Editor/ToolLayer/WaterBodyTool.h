#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P22 Tool — Water body actor and wave simulation manager.
class WaterBodyTool : public ITool {
public:
    enum class WaterBodyType { Ocean, River, Lake, Pond, Transition, Custom };
    enum class WaveType { Gerstner, FFT, Simple, Capillary, Trochoidal, Custom };
    enum class WaterRenderMode { Forward, Deferred, SingleLayer, MultiLayer, Translucent, Custom };
    enum class BuoyancyMode { Disabled, Simple, PointSampled, Volumetric, Custom };

    struct WaterBodyDef {
        std::string waterBodyId;
        std::string name;
        WaterBodyType bodyType{WaterBodyType::Ocean};
        WaterRenderMode renderMode{WaterRenderMode::Forward};
        float depthLevel{1000.0f};
        float surfaceElevation{0.0f};
        float velocityX{0.0f};
        float velocityY{0.0f};
        bool enableWaves{true};
        bool castShadows{false};
    };

    struct WaveSettingsDef {
        std::string settingsId;
        std::string waterBodyId;
        WaveType waveType{WaveType::Gerstner};
        float waveHeight{100.0f};
        float waveLength{1500.0f};
        float waveSpeed{300.0f};
        float steepness{0.5f};
        float directionAngle{0.0f};
        int numWaves{4};
    };

    struct BuoyancyConfig {
        std::string configId;
        std::string waterBodyId;
        BuoyancyMode buoyancyMode{BuoyancyMode::Simple};
        int pontoonCount{4};
        float buoyancyCoefficient{1.0f};
        float dampingLinear{0.5f};
        float dampingAngular{0.5f};
        bool enablePhysicsForces{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "WaterBodyTool"; }
    bool IsActive() const override { return m_active; }

    std::string RegisterWaterBody(const WaterBodyDef& def);
    bool UnregisterWaterBody(const std::string& waterBodyId);
    const WaterBodyDef* GetWaterBody(const std::string& waterBodyId) const;
    std::vector<std::string> GetAllWaterBodyIds() const;

    bool SetWaterBodyType(const std::string& waterBodyId, WaterBodyType type);
    bool SetRenderMode(const std::string& waterBodyId, WaterRenderMode mode);
    bool ApplyWaveSettings(const WaveSettingsDef& settings);
    const WaveSettingsDef* GetWaveSettings(const std::string& waterBodyId) const;
    bool SetBuoyancyConfig(const BuoyancyConfig& config);
    const BuoyancyConfig* GetBuoyancyConfig(const std::string& waterBodyId) const;

    std::vector<std::string> GetBodiesByType(WaterBodyType type) const;
    std::vector<std::string> GetOceanBodies() const;
    std::vector<std::string> GetRiverBodies() const;

    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, WaterBodyDef> m_waterBodies;
    std::unordered_map<std::string, WaveSettingsDef> m_waveSettings;
    std::unordered_map<std::string, BuoyancyConfig> m_buoyancyConfigs;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
