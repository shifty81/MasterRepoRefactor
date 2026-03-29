#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P12 Tool — Real-time cloth simulation authoring with wind and collision response.
class ClothSimulationTool : public ITool {
public:
    enum class ClothType { Fabric, Leather, Silk, Canvas, Chain, Custom };
    enum class CollisionMode { None, SelfCollision, WorldCollision, Both };
    enum class SolverType { Verlet, XPBD, PBD };
    enum class TearMode { None, StressThreshold, UserPaint };

    struct ClothConstraints {
        float stretchStiffness{1.0f};
        float bendingStiffness{0.1f};
        float compressionStiffness{0.8f};
        float shearStiffness{0.5f};
        float dampingCoefficient{0.01f};
    };

    struct ClothPhysics {
        float mass{0.1f};
        float gravityScale{1.0f};
        float airResistance{0.02f};
        float friction{0.4f};
        float restitution{0.1f};
        bool enableCollision{true};
        bool selfCollision{false};
        float collisionMargin{0.01f};
    };

    struct ClothWindResponse {
        float windLift{0.3f};
        float windDrag{0.5f};
        bool turbulenceEnabled{true};
        float turbulenceScale{1.0f};
    };

    struct ClothLayer {
        std::string layerId;
        std::string name;
        ClothType type{ClothType::Fabric};
        CollisionMode collisionMode{CollisionMode::WorldCollision};
        SolverType solver{SolverType::XPBD};
        TearMode tearMode{TearMode::None};
        ClothConstraints constraints;
        ClothPhysics physics;
        ClothWindResponse windResponse;
        std::string meshId;
        std::string meshPath;
        float tearThreshold{1000.0f};
        int solverIterations{8};
        int substeps{2};
        bool enabled{true};
        bool pinned{false};
        std::string linkedEntityId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ClothSimulationTool"; }
    bool IsActive() const override { return m_active; }

    // Layer management
    std::string CreateLayer(const std::string& name,
                             ClothType type = ClothType::Fabric);
    bool RemoveLayer(const std::string& layerId);
    bool SetClothType(const std::string& layerId, ClothType type);
    bool SetCollisionMode(const std::string& layerId, CollisionMode mode);
    bool SetSolver(const std::string& layerId, SolverType solver);
    bool SetTearMode(const std::string& layerId, TearMode mode);
    bool SetSolverIterations(const std::string& layerId, int iterations);
    bool SetSubsteps(const std::string& layerId, int substeps);
    bool SetLayerEnabled(const std::string& layerId, bool enabled);
    bool SetPinned(const std::string& layerId, bool pinned);
    bool SetMesh(const std::string& layerId, const std::string& meshId,
                  const std::string& meshPath = "");
    bool LinkToEntity(const std::string& layerId, const std::string& entityId);
    int GetLayerCount() const { return static_cast<int>(m_layers.size()); }
    const ClothLayer* GetLayer(const std::string& layerId) const;
    std::vector<std::string> GetLayerIds() const;
    std::vector<std::string> GetEnabledLayerIds() const;

    // Constraint settings
    bool SetStretchStiffness(const std::string& layerId, float value);
    bool SetBendingStiffness(const std::string& layerId, float value);
    bool SetCompressionStiffness(const std::string& layerId, float value);
    bool SetShearStiffness(const std::string& layerId, float value);
    bool SetDamping(const std::string& layerId, float value);

    // Physics settings
    bool SetMass(const std::string& layerId, float mass);
    bool SetGravityScale(const std::string& layerId, float scale);
    bool SetAirResistance(const std::string& layerId, float resistance);
    bool SetFriction(const std::string& layerId, float friction);
    bool SetTearThreshold(const std::string& layerId, float threshold);

    // Wind response
    bool SetWindLift(const std::string& layerId, float lift);
    bool SetWindDrag(const std::string& layerId, float drag);
    bool SetTurbulence(const std::string& layerId, bool enabled, float scale = 1.0f);

    // Simulation control
    void PauseSimulation();
    void ResumeSimulation();
    bool IsSimulationPaused() const { return m_simPaused; }
    bool ResetLayer(const std::string& layerId);
    bool BakeLayer(const std::string& layerId);

    // Persistence
    bool SaveLayers(const std::string& filePath) const;
    bool LoadLayers(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    bool m_simPaused{false};
    std::unordered_map<std::string, ClothLayer> m_layers;
    int m_nextLayerIndex{0};
};

} // namespace Atlas::Editor
