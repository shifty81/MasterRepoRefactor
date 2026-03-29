#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P22 Tool — Hair groom simulation and asset manager.
class HairGroomTool : public ITool {
public:
    enum class GroomSimMode { Disabled, CPU, GPU, NvHair, Alembic, Custom };
    enum class StrandRenderMode { Cards, Meshes, Strands, LODStrands, InstancedMesh, Custom };
    enum class WindResponseType { None, Simple, Turbulent, Directional, Vortex, Custom };
    enum class CollisionType { None, Capsule, Sphere, Box, Convex, Custom };

    struct GroomAssetDef {
        std::string groomId;
        std::string name;
        std::string assetPath;
        GroomSimMode simMode{GroomSimMode::Disabled};
        StrandRenderMode renderMode{StrandRenderMode::Strands};
        int strandCount{10000};
        float strandLength{10.0f};
        float strandWidth{0.02f};
        bool castShadows{true};
    };

    struct GroomSimConfig {
        std::string configId;
        std::string groomId;
        GroomSimMode simMode{GroomSimMode::Disabled};
        int simulationSubsteps{4};
        float damping{0.1f};
        float stiffness{0.5f};
        float gravityScale{1.0f};
        bool enableSelfCollision{false};
        bool enableExternalCollision{true};
    };

    struct GroomLODDef {
        std::string lodId;
        std::string groomId;
        int lodLevel{0};
        float screenSize{1.0f};
        float strandRatio{1.0f};
        StrandRenderMode renderMode{StrandRenderMode::Strands};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "HairGroomTool"; }
    bool IsActive() const override { return m_active; }

    std::string RegisterGroomAsset(const GroomAssetDef& def);
    bool UnregisterGroomAsset(const std::string& groomId);
    const GroomAssetDef* GetGroomAsset(const std::string& groomId) const;
    std::vector<std::string> GetAllGroomIds() const;

    bool SetSimMode(const std::string& groomId, GroomSimMode mode);
    bool SetStrandRenderMode(const std::string& groomId, StrandRenderMode mode);
    bool ApplySimConfig(const GroomSimConfig& config);
    const GroomSimConfig* GetSimConfig(const std::string& groomId) const;

    bool AddLOD(const GroomLODDef& lod);
    bool RemoveLOD(const std::string& lodId);
    std::vector<GroomLODDef> GetLODsForGroom(const std::string& groomId) const;

    bool SetWindResponse(const std::string& groomId, WindResponseType responseType);
    bool SetCollisionType(const std::string& groomId, CollisionType collisionType);

    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, GroomAssetDef> m_groomAssets;
    std::unordered_map<std::string, GroomSimConfig> m_simConfigs;
    std::unordered_map<std::string, std::vector<GroomLODDef>> m_lods;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
