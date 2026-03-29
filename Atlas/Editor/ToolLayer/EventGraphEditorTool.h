#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P15 Tool — Visual event graph editor for node-based event flow and condition authoring.
class EventGraphEditorTool : public ITool {
public:
    enum class NodeType { Event, Condition, Action, Delay, Branch, Loop, Sequence, Custom };
    enum class ConnectionType { Flow, Data, Reference };
    enum class GraphStatus { Empty, Valid, HasErrors, Running };

    struct GraphNode {
        std::string nodeId;
        std::string name;
        NodeType nodeType{NodeType::Event};
        float posX{0.0f};
        float posY{0.0f};
        std::vector<std::string> inputPins;
        std::vector<std::string> outputPins;
    };

    struct GraphEdge {
        std::string edgeId;
        std::string fromNodeId;
        std::string fromPin;
        std::string toNodeId;
        std::string toPin;
        ConnectionType connectionType{ConnectionType::Flow};
    };

    struct EventGraph {
        std::string graphId;
        std::string name;
        std::vector<std::string> nodes;
        std::vector<std::string> edges;
        GraphStatus status{GraphStatus::Empty};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "EventGraphEditorTool"; }
    bool IsActive() const override { return m_active; }

    // Graph management
    std::string CreateGraph(const std::string& name);
    bool RemoveGraph(const std::string& graphId);

    // Node management
    std::string AddNode(const std::string& graphId, NodeType type, float posX, float posY);
    bool RemoveNode(const std::string& graphId, const std::string& nodeId);
    bool MoveNode(const std::string& nodeId, float posX, float posY);

    // Edge management
    std::string AddEdge(const std::string& graphId, const std::string& fromNodeId,
                        const std::string& fromPin, const std::string& toNodeId,
                        const std::string& toPin, ConnectionType connType = ConnectionType::Flow);
    bool RemoveEdge(const std::string& graphId, const std::string& edgeId);

    // Graph operations
    bool ValidateGraph(const std::string& graphId);
    bool CompileGraph(const std::string& graphId);
    bool RunGraph(const std::string& graphId);

    // Queries
    const EventGraph* GetGraph(const std::string& graphId) const;
    std::vector<std::string> GetAllGraphIds() const;
    const GraphNode* GetNodeById(const std::string& nodeId) const;
    std::vector<std::string> GetEdgesForNode(const std::string& nodeId) const;
    GraphStatus GetGraphStatus(const std::string& graphId) const;

    // Persistence
    bool SaveGraph(const std::string& graphId, const std::string& filePath) const;
    bool LoadGraph(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, EventGraph> m_graphs;
    std::unordered_map<std::string, GraphNode> m_nodes;
    std::unordered_map<std::string, GraphEdge> m_edges;
    int m_nextGraphIndex{0};
    int m_nextNodeIndex{0};
    int m_nextEdgeIndex{0};
};

} // namespace Atlas::Editor
