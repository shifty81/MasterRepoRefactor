#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P10 Tool — Cinematic lighting authoring for scenes and cutscenes.
class CinematicLightingTool : public ITool {
public:
    enum class LightType { Directional, Point, Spot, Rect, Sky, IES };
    enum class ShadowQuality { Off, Low, Medium, High, Ultra, RayTraced };
    enum class LightingUnit { Lux, Candela, Lumen, EV100 };

    struct LightColor {
        float r{1.0f};
        float g{1.0f};
        float b{1.0f};
        float temperature{6500.0f};
        bool useTemperature{false};
    };

    struct ShadowSettings {
        ShadowQuality quality{ShadowQuality::Medium};
        float nearPlane{0.1f};
        float bias{0.005f};
        float normalBias{0.02f};
        int resolution{1024};
        float softness{0.0f};
        bool contactShadows{false};
    };

    struct LightRig {
        std::string lightId;
        std::string name;
        LightType type{LightType::Point};
        LightColor color;
        LightingUnit unit{LightingUnit::Lumen};
        float intensity{1000.0f};
        float range{10.0f};
        float innerAngle{30.0f};
        float outerAngle{45.0f};
        float posX{0.0f};
        float posY{2.0f};
        float posZ{0.0f};
        float rotX{0.0f};
        float rotY{0.0f};
        float rotZ{0.0f};
        float rectWidth{1.0f};
        float rectHeight{1.0f};
        ShadowSettings shadows;
        bool enabled{true};
        bool castShadows{true};
        bool affectsVolumetrics{false};
        std::string iesProfilePath;
        std::string linkedEntityId;
    };

    struct LightingScenario {
        std::string scenarioId;
        std::string name;
        std::vector<std::string> lightIds;
        float timeOfDay{12.0f};
        float atmosphericDensity{1.0f};
        bool isActive{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "CinematicLightingTool"; }
    bool IsActive() const override { return m_active; }

    // Light management
    std::string AddLight(const std::string& name, LightType type);
    bool RemoveLight(const std::string& lightId);
    bool SetLightType(const std::string& lightId, LightType type);
    bool SetLightIntensity(const std::string& lightId, float intensity, LightingUnit unit);
    bool SetLightColor(const std::string& lightId, float r, float g, float b);
    bool SetLightTemperature(const std::string& lightId, float kelvin, bool use = true);
    bool SetLightPosition(const std::string& lightId, float px, float py, float pz);
    bool SetLightRotation(const std::string& lightId, float rx, float ry, float rz);
    bool SetLightRange(const std::string& lightId, float range);
    bool SetSpotAngles(const std::string& lightId, float inner, float outer);
    bool SetRectSize(const std::string& lightId, float width, float height);
    bool SetLightEnabled(const std::string& lightId, bool enabled);
    bool SetCastShadows(const std::string& lightId, bool cast);
    bool SetShadowQuality(const std::string& lightId, ShadowQuality quality);
    bool SetShadowSoftness(const std::string& lightId, float softness);
    bool SetContactShadows(const std::string& lightId, bool enabled);
    bool SetAffectsVolumetrics(const std::string& lightId, bool enabled);
    bool SetIESProfile(const std::string& lightId, const std::string& profilePath);
    bool LinkToEntity(const std::string& lightId, const std::string& entityId);
    int GetLightCount() const { return static_cast<int>(m_lights.size()); }
    const LightRig* GetLight(const std::string& lightId) const;
    std::vector<std::string> GetLightIds() const;
    std::vector<std::string> GetEnabledLightIds() const;

    // Scenario management
    std::string CreateScenario(const std::string& name);
    bool RemoveScenario(const std::string& scenarioId);
    bool AddLightToScenario(const std::string& scenarioId, const std::string& lightId);
    bool RemoveLightFromScenario(const std::string& scenarioId,
                                  const std::string& lightId);
    bool SetScenarioActive(const std::string& scenarioId, bool active);
    bool SetTimeOfDay(const std::string& scenarioId, float hour);
    int GetScenarioCount() const { return static_cast<int>(m_scenarios.size()); }
    const LightingScenario* GetScenario(const std::string& scenarioId) const;
    std::vector<std::string> GetScenarioIds() const;

    // Persistence
    bool SaveLighting(const std::string& filePath) const;
    bool LoadLighting(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, LightRig> m_lights;
    std::unordered_map<std::string, LightingScenario> m_scenarios;
    int m_nextLightIndex{0};
    int m_nextScenarioIndex{0};
};

} // namespace Atlas::Editor
