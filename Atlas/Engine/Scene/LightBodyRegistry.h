#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 31D — Registry for light body definitions used by the lighting subsystem.
class LightBodyRegistry {
public:
    enum class LightBodyState { Inactive, Active, Baking, Baked, Streaming, Dynamic, Culled };
    enum class LightType { Directional, Point, Spot, Area, SkyLight, EmissiveMesh, VolumetricFog, IES };
    enum class LightMobility { Static, Stationary, Movable };
    enum class ShadowResolution { Off, Low, Medium, High, Ultra, Cinematic };
    enum class AttenuationShape { Sphere, Box, Cylinder, Cone, Custom };

    struct LightColorDef {
        float r{1.0f};
        float g{1.0f};
        float b{1.0f};
        float temperature{6500.0f};
        float intensity{1.0f};
        bool useTemperature{false};
    };

    struct ShadowSettings {
        ShadowResolution resolution{ShadowResolution::Medium};
        float bias{0.01f};
        float nearPlane{0.1f};
        bool contactShadow{false};
        int cascades{4};
        bool softShadow{true};
    };

    struct AtmosphericSettings {
        bool castVolumetric{false};
        float scatterIntensity{1.0f};
        float fogDensity{0.0f};
        bool cloudShadow{false};
    };

    struct LightBodyRecord {
        std::string bodyId;
        std::string name;
        LightType lightType{LightType::Point};
        LightMobility mobility{LightMobility::Stationary};
        LightColorDef colorDef;
        ShadowSettings shadowSettings;
        AtmosphericSettings atmosphericSettings;
        AttenuationShape attenuationShape{AttenuationShape::Sphere};
        float range{1000.0f};
        float innerAngle{0.0f};
        float outerAngle{45.0f};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float rotX{0.0f};
        float rotY{0.0f};
        float rotZ{0.0f};
        bool enabled{true};
        bool castShadow{true};
        bool affectsWorld{true};
        bool visible{true};
        LightBodyState state{LightBodyState::Inactive};
    };

    // Body registration
    bool RegisterBody(const LightBodyRecord& record);
    bool UnregisterBody(const std::string& bodyId);

    // State and transform
    bool SetBodyState(const std::string& bodyId, LightBodyState state);
    bool SetBodyPosition(const std::string& bodyId, float x, float y, float z);
    bool SetBodyRotation(const std::string& bodyId, float x, float y, float z);

    // Light configuration
    bool SetLightType(const std::string& bodyId, LightType type);
    bool SetLightMobility(const std::string& bodyId, LightMobility mobility);
    bool SetLightColor(const std::string& bodyId, const LightColorDef& color);
    bool SetLightIntensity(const std::string& bodyId, float intensity);
    bool SetShadowSettings(const std::string& bodyId, const ShadowSettings& settings);
    bool SetAtmosphericSettings(const std::string& bodyId, const AtmosphericSettings& settings);
    bool SetAttenuationShape(const std::string& bodyId, AttenuationShape shape);
    bool SetRange(const std::string& bodyId, float range);
    bool SetInnerAngle(const std::string& bodyId, float angle);
    bool SetOuterAngle(const std::string& bodyId, float angle);
    bool SetBodyEnabled(const std::string& bodyId, bool enabled);
    bool SetBodyVisible(const std::string& bodyId, bool visible);

    // Queries
    const LightBodyRecord* GetBodyById(const std::string& bodyId) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByType(LightType type) const;
    std::vector<std::string> GetBodiesByMobility(LightMobility mobility) const;
    std::vector<std::string> GetBodiesByState(LightBodyState state) const;
    std::vector<std::string> GetActiveBodies() const;
    std::vector<std::string> GetShadowCastingBodies() const;
    std::vector<std::string> GetBodiesInRange(float cx, float cy, float cz, float radius) const;

    // Callbacks
    using StateChangedCallback = std::function<void(const std::string&, LightBodyState)>;
    void SetOnStateChangedCallback(StateChangedCallback cb);

    // Persistence
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);
    void Clear();

private:
    std::unordered_map<std::string, LightBodyRecord> m_bodies;
    StateChangedCallback m_onStateChanged;
};

} // namespace Atlas::Engine
