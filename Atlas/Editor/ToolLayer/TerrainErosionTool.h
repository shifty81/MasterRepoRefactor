#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P11 Tool — Procedural terrain erosion authoring for realistic landscape formation.
class TerrainErosionTool : public ITool {
public:
    enum class ErosionType { Hydraulic, Thermal, Wind, Fluvial, Glacial };
    enum class ErosionQuality { Preview, Medium, High, Ultra };
    enum class SedimentMode { Deposit, Erode, Transport };

    struct HydraulicParams {
        float rainAmount{0.01f};
        float evaporationRate{0.05f};
        float sedimentCapacity{4.0f};
        float depositionRate{0.3f};
        float erosionRate{0.3f};
        float inertia{0.05f};
        float gravity{4.0f};
        int iterationsPerStep{50000};
    };

    struct ThermalParams {
        float talusAngle{45.0f};
        float erosionRate{0.5f};
        int iterations{1000};
    };

    struct WindParams {
        float windSpeed{5.0f};
        float windDirectionX{1.0f};
        float windDirectionZ{0.0f};
        float saltationStrength{0.3f};
        float depositionRate{0.2f};
        int iterations{2000};
    };

    struct ErosionLayer {
        std::string layerId;
        std::string name;
        ErosionType type{ErosionType::Hydraulic};
        ErosionQuality quality{ErosionQuality::Medium};
        SedimentMode sedimentMode{SedimentMode::Transport};
        HydraulicParams hydraulic;
        ThermalParams thermal;
        WindParams wind;
        float brushRadius{50.0f};
        float brushStrength{1.0f};
        float maskStrength{1.0f};
        bool enabled{true};
        bool useHeightMask{false};
        float minHeightMask{0.0f};
        float maxHeightMask{1.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "TerrainErosionTool"; }
    bool IsActive() const override { return m_active; }

    // Layer management
    std::string CreateLayer(const std::string& name, ErosionType type = ErosionType::Hydraulic);
    bool RemoveLayer(const std::string& layerId);
    bool SetErosionType(const std::string& layerId, ErosionType type);
    bool SetErosionQuality(const std::string& layerId, ErosionQuality quality);
    bool SetSedimentMode(const std::string& layerId, SedimentMode mode);
    bool SetBrushRadius(const std::string& layerId, float radius);
    bool SetBrushStrength(const std::string& layerId, float strength);
    bool SetLayerEnabled(const std::string& layerId, bool enabled);
    bool SetHeightMask(const std::string& layerId, bool use, float minH, float maxH);
    int GetLayerCount() const { return static_cast<int>(m_layers.size()); }
    const ErosionLayer* GetLayer(const std::string& layerId) const;
    std::vector<std::string> GetLayerIds() const;

    // Hydraulic params
    bool SetRainAmount(const std::string& layerId, float amount);
    bool SetEvaporationRate(const std::string& layerId, float rate);
    bool SetSedimentCapacity(const std::string& layerId, float capacity);
    bool SetDepositionRate(const std::string& layerId, float rate);
    bool SetHydraulicErosionRate(const std::string& layerId, float rate);
    bool SetInertia(const std::string& layerId, float inertia);
    bool SetIterationsPerStep(const std::string& layerId, int count);

    // Thermal params
    bool SetTalusAngle(const std::string& layerId, float degrees);
    bool SetThermalErosionRate(const std::string& layerId, float rate);
    bool SetThermalIterations(const std::string& layerId, int count);

    // Wind params
    bool SetWindSpeed(const std::string& layerId, float speed);
    bool SetWindDirection(const std::string& layerId, float dx, float dz);
    bool SetSaltationStrength(const std::string& layerId, float strength);
    bool SetWindDepositionRate(const std::string& layerId, float rate);

    // Simulation
    bool BakeLayer(const std::string& layerId);
    bool BakeAll();
    void CancelBake();
    bool IsBaking() const { return m_baking; }

    // Persistence
    bool SaveLayers(const std::string& filePath) const;
    bool LoadLayers(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    bool m_baking{false};
    std::unordered_map<std::string, ErosionLayer> m_layers;
    int m_nextLayerIndex{0};
};

} // namespace Atlas::Editor
