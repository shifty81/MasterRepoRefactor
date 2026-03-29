#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P13 Tool — Visual effects graph editor with emitter nodes, particle links, and simulation.
class VFXGraphTool : public ITool {
public:
    enum class EmitterType { Point, Sphere, Box, Cone, Mesh, Trail };
    enum class SimulationSpace { World, Local, Custom };
    enum class ParticleDataType { Float, Vector2, Vector3, Color, Texture, Boolean };
    enum class NodeCategory { Emitter, Force, Modifier, Renderer, Output, Logic };

    struct EmitterNodeConfig {
        EmitterType emitterType{EmitterType::Point};
        float spawnRate{10.0f};
        float lifetime{2.0f};
        float startSpeed{1.0f};
        float startSize{0.1f};
        SimulationSpace simulationSpace{SimulationSpace::World};
        bool loop{true};
        bool prewarm{false};
    };

    struct ParticleLinkEdge {
        std::string edgeId;
        std::string sourceNodeId;
        std::string targetNodeId;
        ParticleDataType dataType{ParticleDataType::Float};
        std::string outputPort;
        std::string inputPort;
        bool enabled{true};
    };

    struct ForceModifier {
        std::string modifierId;
        std::string name;
        float forceX{0.0f};
        float forceY{-9.81f};
        float forceZ{0.0f};
        float turbulenceStrength{0.0f};
        float turbulenceScale{1.0f};
        bool enabled{true};
    };

    struct VFXGraphNode {
        std::string nodeId;
        std::string name;
        NodeCategory category{NodeCategory::Emitter};
        EmitterNodeConfig emitterConfig;
        ForceModifier forceModifier;
        float positionX{0.0f};
        float positionY{0.0f};
        float colorR{1.0f};
        float colorG{1.0f};
        float colorB{1.0f};
        float colorA{1.0f};
        std::string assetPath;
        std::string shaderPath;
        bool selected{false};
        bool enabled{true};
        std::string parentGraphId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "VFXGraphTool"; }
    bool IsActive() const override { return m_active; }

    // Node management
    std::string CreateNode(const std::string& name, NodeCategory category = NodeCategory::Emitter);
    bool RemoveNode(const std::string& nodeId);
    bool SetNodeCategory(const std::string& nodeId, NodeCategory category);
    bool SetEmitterType(const std::string& nodeId, EmitterType type);
    bool SetSpawnRate(const std::string& nodeId, float rate);
    bool SetLifetime(const std::string& nodeId, float lifetime);
    bool SetSimulationSpace(const std::string& nodeId, SimulationSpace space);
    bool SetNodePosition(const std::string& nodeId, float x, float y);
    bool SetNodeEnabled(const std::string& nodeId, bool enabled);
    bool SetNodeSelected(const std::string& nodeId, bool selected);
    bool SetNodeColor(const std::string& nodeId, float r, float g, float b, float a);
    bool SetNodeAsset(const std::string& nodeId, const std::string& assetPath);

    // Edge management
    std::string ConnectNodes(const std::string& sourceId, const std::string& targetId,
                              ParticleDataType dataType = ParticleDataType::Float);
    bool DisconnectEdge(const std::string& edgeId);
    bool SetEdgeEnabled(const std::string& edgeId, bool enabled);
    const ParticleLinkEdge* GetEdge(const std::string& edgeId) const;
    std::vector<std::string> GetEdgesFromNode(const std::string& nodeId) const;
    std::vector<std::string> GetEdgesToNode(const std::string& nodeId) const;

    // Force modifiers
    std::string AddForceModifier(const std::string& nodeId, const std::string& name);
    bool SetForce(const std::string& nodeId, float fx, float fy, float fz);
    bool SetTurbulence(const std::string& nodeId, float strength, float scale);

    // Simulation control
    void PlaySimulation();
    void PauseSimulation();
    void StopSimulation();
    bool IsSimulating() const { return m_simulating; }
    void StepSimulation(float deltaTime);

    // Queries
    int GetNodeCount() const { return static_cast<int>(m_nodes.size()); }
    int GetEdgeCount() const { return static_cast<int>(m_edges.size()); }
    const VFXGraphNode* GetNode(const std::string& nodeId) const;
    std::vector<std::string> GetNodeIds() const;
    std::vector<std::string> GetNodesByCategory(NodeCategory category) const;
    std::vector<std::string> GetSelectedNodeIds() const;

    // Graph operations
    bool ValidateGraph() const;
    bool CompileGraph(const std::string& outputPath);
    void SelectAll();
    void DeselectAll();
    void ClearAll();

private:
    bool m_active{false};
    bool m_simulating{false};
    std::unordered_map<std::string, VFXGraphNode> m_nodes;
    std::unordered_map<std::string, ParticleLinkEdge> m_edges;
    int m_nextNodeIndex{0};
    int m_nextEdgeIndex{0};
};

} // namespace Atlas::Editor
