#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 32D — Registry for VFX body definitions used by the particle and visual effects subsystem.
class FXBodyRegistry {
public:
    enum class FXBodyState { Inactive, Active, Playing, Paused, Stopped, Recycled, Culled };
    enum class FXBodyType { Particle, Ribbon, Mesh, Trail, Beam, Volume, Sprite, Decal };
    enum class FXMobility { Static, Stationary, Movable };
    enum class LODReductionMode { None, ScaleDown, Cull, Simplify, BudgetBased };
    enum class SimulationTarget { CPU, GPU, GPUCompute, Hybrid };

    struct FXColorGradient {
        std::vector<std::string> stops;
        std::string interpMode;
    };

    struct FXEmitSettings {
        float spawnRate{100.0f};
        int burstCount{0};
        float lifetime{2.0f};
        float startSize{10.0f};
        float endSize{0.0f};
        float startSpeed{100.0f};
        float endSpeed{50.0f};
        float inheritVelocity{0.0f};
    };

    struct FXSimSettings {
        SimulationTarget target{SimulationTarget::GPU};
        int maxParticles{1000};
        bool localSpace{false};
        int seed{0};
        float warmupTime{0.0f};
        float fixedTimestep{0.0f};
    };

    struct FXBodyRecord {
        std::string bodyId;
        std::string name;
        FXBodyType fxType{FXBodyType::Particle};
        FXMobility mobility{FXMobility::Movable};
        FXEmitSettings emitSettings;
        FXSimSettings simSettings;
        FXColorGradient colorGradient;
        LODReductionMode lodReductionMode{LODReductionMode::None};
        float range{5000.0f};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float rotX{0.0f};
        float rotY{0.0f};
        float rotZ{0.0f};
        bool enabled{true};
        bool looping{true};
        bool autoDestroy{false};
        bool visible{true};
        FXBodyState state{FXBodyState::Inactive};
    };

    // Body registration
    bool RegisterBody(const FXBodyRecord& record);
    bool UnregisterBody(const std::string& bodyId);

    // State and transform
    bool SetBodyState(const std::string& bodyId, FXBodyState state);
    bool SetBodyPosition(const std::string& bodyId, float x, float y, float z);
    bool SetBodyRotation(const std::string& bodyId, float x, float y, float z);

    // FX configuration
    bool SetFXType(const std::string& bodyId, FXBodyType type);
    bool SetFXMobility(const std::string& bodyId, FXMobility mobility);
    bool SetEmitSettings(const std::string& bodyId, const FXEmitSettings& settings);
    bool SetSimSettings(const std::string& bodyId, const FXSimSettings& settings);
    bool SetColorGradient(const std::string& bodyId, const FXColorGradient& gradient);
    bool SetLODReduction(const std::string& bodyId, LODReductionMode mode);
    bool SetRange(const std::string& bodyId, float range);
    bool SetBodyEnabled(const std::string& bodyId, bool enabled);
    bool SetBodyVisible(const std::string& bodyId, bool visible);
    bool SetLooping(const std::string& bodyId, bool looping);
    bool SetAutoDestroy(const std::string& bodyId, bool autoDestroy);

    // Queries
    const FXBodyRecord* GetBodyById(const std::string& bodyId) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByType(FXBodyType type) const;
    std::vector<std::string> GetBodiesByMobility(FXMobility mobility) const;
    std::vector<std::string> GetBodiesByState(FXBodyState state) const;
    std::vector<std::string> GetActiveBodies() const;
    std::vector<std::string> GetPlayingBodies() const;
    std::vector<std::string> GetBodiesInRange(float cx, float cy, float cz, float radius) const;

    // Persistence
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);
    void Clear();

private:
    std::unordered_map<std::string, FXBodyRecord> m_bodies;
};

} // namespace Atlas::Engine
