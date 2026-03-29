#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P8 Tool — Rope and cable physics simulation authoring tool.
class RopeSimulationTool : public ITool {
public:
    enum class RopeType { Rope, Cable, Chain, Elastic, Rigid };
    enum class AnchorType { World, Entity, Dynamic };
    enum class SolverMode { Verlet, PBD, XPBD };

    struct RopeSegment {
        std::string segmentId;
        int index{0};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float mass{0.1f};
        bool isPinned{false};
    };

    struct RopeAnchor {
        std::string anchorId;
        AnchorType type{AnchorType::World};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        std::string entityId;
        std::string socketName;
    };

    struct RopeDefinition {
        std::string ropeId;
        std::string name;
        RopeType type{RopeType::Rope};
        int segmentCount{20};
        float length{10.0f};
        float radius{0.05f};
        float stiffness{0.8f};
        float damping{0.1f};
        float gravity{-9.81f};
        float mass{0.1f};
        SolverMode solver{SolverMode::PBD};
        std::string materialAsset;
        std::string startAnchorId;
        std::string endAnchorId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "RopeSimulationTool"; }
    bool IsActive() const override { return m_active; }

    // Rope management
    std::string CreateRope(const std::string& name, RopeType type = RopeType::Rope,
                            int segmentCount = 20, float length = 10.0f);
    bool RemoveRope(const std::string& ropeId);
    bool SetRopeLength(const std::string& ropeId, float length);
    bool SetRopeStiffness(const std::string& ropeId, float stiffness);
    bool SetRopeDamping(const std::string& ropeId, float damping);
    bool SetRopeMass(const std::string& ropeId, float mass);
    bool SetRopeSolver(const std::string& ropeId, SolverMode solver);
    bool SetRopeMaterial(const std::string& ropeId, const std::string& materialAsset);
    int GetRopeCount() const { return static_cast<int>(m_ropes.size()); }
    const RopeDefinition* GetRope(const std::string& ropeId) const;

    // Anchor management
    std::string AddAnchor(AnchorType type, float px, float py, float pz,
                          const std::string& entityId = "");
    bool RemoveAnchor(const std::string& anchorId);
    bool AttachStart(const std::string& ropeId, const std::string& anchorId);
    bool AttachEnd(const std::string& ropeId, const std::string& anchorId);
    bool DetachStart(const std::string& ropeId);
    bool DetachEnd(const std::string& ropeId);
    int GetAnchorCount() const { return static_cast<int>(m_anchors.size()); }

    // Simulation
    bool SimulateRope(const std::string& ropeId, float deltaTime, int iterations = 10);
    bool SimulateAll(float deltaTime, int iterations = 10);
    bool ResetRope(const std::string& ropeId);
    bool PinSegment(const std::string& ropeId, int segmentIndex, bool pin = true);
    std::vector<RopeSegment> GetSegments(const std::string& ropeId) const;

    // Persistence
    bool SaveRope(const std::string& ropeId, const std::string& filePath) const;
    std::string LoadRope(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::vector<RopeDefinition> m_ropes;
    std::vector<RopeAnchor> m_anchors;
    int m_nextRopeIndex{0};
    int m_nextAnchorIndex{0};
};

} // namespace Atlas::Editor
