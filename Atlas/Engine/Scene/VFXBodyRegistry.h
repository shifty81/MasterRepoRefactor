#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 28D — Registry for VFX emitter body definitions used by the visual effects subsystem.
/// Manages emitter metadata, simulation settings, render configurations, and LOD levels
/// for runtime and authoring time VFX scene composition.
class VFXBodyRegistry {
public:
    enum class VFXBodyState { Inactive, Active, Playing, Paused, Stopped };
    enum class EmitterShape { Point, Sphere, Box, Cone, Mesh, Trail };
    enum class SimulationSpace { World, Local, Custom };
    enum class BlendMode { Additive, AlphaBlend, Multiply, Screen, Premultiplied };
    enum class VFXLayer { World, UI, Overlay, Debug, Cinematic };

    struct EmitterBounds {
        EmitterShape shape{EmitterShape::Sphere};
        float extentX{1.0f};
        float extentY{1.0f};
        float extentZ{1.0f};
        float radius{1.0f};
        bool useMeshBounds{false};
    };

    struct SimulationSettings {
        SimulationSpace space{SimulationSpace::World};
        int maxParticles{1000};
        bool fixedTimeStep{false};
        float timeStep{0.016f};
        float gravityScale{1.0f};
        bool collisionEnabled{false};
        bool useGPUSimulation{false};
        float warmupDuration{0.0f};
    };

    struct RenderSettings {
        BlendMode blendMode{BlendMode::Additive};
        std::string materialPath;
        std::string shaderOverridePath;
        bool castShadows{false};
        bool receiveShadows{false};
        bool depthWrite{false};
        bool depthTest{true};
        float sortingOffset{0.0f};
        int renderQueue{3000};
    };

    struct LODSettings {
        bool enabled{true};
        float lod0Distance{10.0f};
        float lod1Distance{30.0f};
        float lod2Distance{80.0f};
        float cullDistance{150.0f};
        float spawnRateLOD1{0.5f};
        float spawnRateLOD2{0.2f};
    };

    struct VFXBodyRecord {
        std::string bodyId;
        std::string name;
        EmitterShape emitterShape{EmitterShape::Point};
        VFXBodyState state{VFXBodyState::Inactive};
        VFXLayer layer{VFXLayer::World};
        BlendMode blendMode{BlendMode::Additive};
        EmitterBounds bounds;
        SimulationSettings simulation;
        RenderSettings renderSettings;
        LODSettings lodSettings;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float spawnRate{10.0f};
        float lifetime{2.0f};
        float startSpeed{1.0f};
        float startSize{0.1f};
        float startColorR{1.0f};
        float startColorG{1.0f};
        float startColorB{1.0f};
        float startColorA{1.0f};
        bool loop{false};
        bool playOnActivate{false};
        bool prewarm{false};
        std::string effectAssetId;
        std::string linkedEntityId;
        std::string sceneId;
        int priority{0};
        int lodLevel{0};
        bool alwaysPlay{false};
    };

    // Body registration
    bool RegisterBody(const VFXBodyRecord& record);
    bool UnregisterBody(const std::string& bodyId);
    bool UpdateBody(const std::string& bodyId, const VFXBodyRecord& record);
    bool SetBodyState(const std::string& bodyId, VFXBodyState state);
    bool SetBodyLayer(const std::string& bodyId, VFXLayer layer);
    bool SetBodyBlendMode(const std::string& bodyId, BlendMode mode);
    bool SetBodyPosition(const std::string& bodyId, float x, float y, float z);
    bool SetSpawnRate(const std::string& bodyId, float rate);
    bool SetLifetime(const std::string& bodyId, float lifetime);
    bool SetStartSpeed(const std::string& bodyId, float speed);
    bool SetStartSize(const std::string& bodyId, float size);
    bool SetStartColor(const std::string& bodyId, float r, float g, float b, float a);
    bool SetLoop(const std::string& bodyId, bool loop);
    bool SetPlayOnActivate(const std::string& bodyId, bool playOnActivate);
    bool SetPrewarm(const std::string& bodyId, bool prewarm);
    bool SetEffectAsset(const std::string& bodyId, const std::string& assetId);
    bool SetPriority(const std::string& bodyId, int priority);
    bool SetAlwaysPlay(const std::string& bodyId, bool alwaysPlay);
    bool SetScene(const std::string& bodyId, const std::string& sceneId);
    bool LinkToEntity(const std::string& bodyId, const std::string& entityId);
    bool SetLODLevel(const std::string& bodyId, int lodLevel);

    // Simulation settings
    bool SetSimulationSpace(const std::string& bodyId, SimulationSpace space);
    bool SetMaxParticles(const std::string& bodyId, int count);
    bool SetGravityScale(const std::string& bodyId, float scale);
    bool SetCollisionEnabled(const std::string& bodyId, bool enabled);
    bool SetGPUSimulation(const std::string& bodyId, bool enabled);

    // Render settings
    bool SetMaterialPath(const std::string& bodyId, const std::string& path);
    bool SetCastShadows(const std::string& bodyId, bool enabled);
    bool SetDepthWrite(const std::string& bodyId, bool enabled);
    bool SetRenderQueue(const std::string& bodyId, int queue);

    // LOD settings
    bool SetLODEnabled(const std::string& bodyId, bool enabled);
    bool SetLODDistances(const std::string& bodyId,
                          float lod0, float lod1, float lod2, float cull);
    bool SetCullDistance(const std::string& bodyId, float distance);

    // Queries
    int GetRegisteredCount() const { return static_cast<int>(m_bodies.size()); }
    bool IsRegistered(const std::string& bodyId) const;
    const VFXBodyRecord* GetBody(const std::string& bodyId) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByScene(const std::string& sceneId) const;
    std::vector<std::string> GetBodiesByLayer(VFXLayer layer) const;
    std::vector<std::string> GetBodiesByShape(EmitterShape shape) const;
    std::vector<std::string> GetActiveBodies() const;
    std::vector<std::string> GetAlwaysPlayBodies() const;
    std::vector<std::string> GetLoopingBodies() const;

    // Activation
    bool ActivateBody(const std::string& bodyId);
    bool DeactivateBody(const std::string& bodyId);
    bool PlayBody(const std::string& bodyId);
    bool PauseBody(const std::string& bodyId);
    bool StopBody(const std::string& bodyId);
    int GetActiveCount() const;
    int GetPlayingCount() const;
    void ActivateAllInScene(const std::string& sceneId);
    void DeactivateAllInScene(const std::string& sceneId);
    void ActivateAlwaysPlay();
    void PlayOnActivateAll();

    // Callbacks
    using StateChangedCallback = std::function<void(const std::string&, VFXBodyState)>;
    void SetOnStateChangedCallback(StateChangedCallback cb);

    // Persistence
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);
    void Clear();

private:
    std::unordered_map<std::string, VFXBodyRecord> m_bodies;
    StateChangedCallback m_onStateChanged;
};

} // namespace Atlas::Engine
