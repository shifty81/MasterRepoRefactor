#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P11 Tool — Authoring tool for real-time grass and ground-cover simulation.
class GrassSimulationTool : public ITool {
public:
    enum class GrassType { Grass, Bush, Reed, Flower, Moss, Fern };
    enum class WindModel { None, Uniform, Perlin, Turbulent };
    enum class CullingMode { None, Frustum, Occlusion, DistanceFade };
    enum class DensityMode { Uniform, Painted, Procedural, HeightBased };

    struct GrassBladeSettings {
        float widthMin{0.02f};
        float widthMax{0.05f};
        float heightMin{0.3f};
        float heightMax{0.8f};
        float tilt{0.0f};
        float bend{0.2f};
        float randomRotation{1.0f};
        bool castShadows{false};
    };

    struct WindSettings {
        WindModel model{WindModel::Perlin};
        float speed{1.5f};
        float strength{0.3f};
        float turbulence{0.1f};
        float directionX{1.0f};
        float directionZ{0.0f};
        float gustFrequency{0.5f};
    };

    struct GrassLayer {
        std::string layerId;
        std::string name;
        GrassType type{GrassType::Grass};
        DensityMode densityMode{DensityMode::Procedural};
        CullingMode cullingMode{CullingMode::DistanceFade};
        float density{1.0f};
        float maxRenderDistance{100.0f};
        float fadeStartDistance{80.0f};
        GrassBladeSettings bladeSettings;
        WindSettings wind;
        std::string texturePath;
        std::string materialId;
        bool enabled{true};
        bool receiveShadows{true};
        float slopeThreshold{45.0f};
        float minHeight{-9999.0f};
        float maxHeight{9999.0f};
        int maxInstanceCount{100000};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "GrassSimulationTool"; }
    bool IsActive() const override { return m_active; }

    // Layer management
    std::string CreateLayer(const std::string& name, GrassType type = GrassType::Grass);
    bool RemoveLayer(const std::string& layerId);
    bool SetGrassType(const std::string& layerId, GrassType type);
    bool SetDensityMode(const std::string& layerId, DensityMode mode);
    bool SetCullingMode(const std::string& layerId, CullingMode mode);
    bool SetDensity(const std::string& layerId, float density);
    bool SetMaxRenderDistance(const std::string& layerId, float dist);
    bool SetFadeStartDistance(const std::string& layerId, float dist);
    bool SetSlopeThreshold(const std::string& layerId, float degrees);
    bool SetHeightRange(const std::string& layerId, float minH, float maxH);
    bool SetMaxInstanceCount(const std::string& layerId, int count);
    bool SetLayerEnabled(const std::string& layerId, bool enabled);
    bool SetTexture(const std::string& layerId, const std::string& texPath);
    bool SetMaterial(const std::string& layerId, const std::string& matId);
    int GetLayerCount() const { return static_cast<int>(m_layers.size()); }
    const GrassLayer* GetLayer(const std::string& layerId) const;
    std::vector<std::string> GetLayerIds() const;
    std::vector<std::string> GetEnabledLayerIds() const;

    // Blade settings
    bool SetBladeWidth(const std::string& layerId, float minW, float maxW);
    bool SetBladeHeight(const std::string& layerId, float minH, float maxH);
    bool SetBladeTilt(const std::string& layerId, float tilt);
    bool SetBladeBend(const std::string& layerId, float bend);
    bool SetBladeRandomRotation(const std::string& layerId, float amount);

    // Wind settings
    bool SetWindModel(const std::string& layerId, WindModel model);
    bool SetWindSpeed(const std::string& layerId, float speed);
    bool SetWindStrength(const std::string& layerId, float strength);
    bool SetWindTurbulence(const std::string& layerId, float turbulence);
    bool SetWindDirection(const std::string& layerId, float dx, float dz);
    bool SetGustFrequency(const std::string& layerId, float freq);

    // Simulation control
    void PauseSimulation();
    void ResumeSimulation();
    bool IsSimulationPaused() const { return m_simPaused; }
    int GetTotalInstanceCount() const;

    // Persistence
    bool SaveLayers(const std::string& filePath) const;
    bool LoadLayers(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    bool m_simPaused{false};
    std::unordered_map<std::string, GrassLayer> m_layers;
    int m_nextLayerIndex{0};
};

} // namespace Atlas::Editor
