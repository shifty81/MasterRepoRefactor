#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P8 Tool — Node-based shader graph editor for creating and editing material shaders.
class ShaderGraphEditorTool : public ITool {
public:
    enum class NodeType { Input, Output, Math, Texture, Color, Lerp, Fresnel, Custom };
    enum class PortType { Float, Float2, Float3, Float4, Bool, Sampler };
    enum class ShaderDomain { Surface, PostProcess, Unlit, Volumetric };

    struct Port {
        std::string portId;
        std::string name;
        PortType type{PortType::Float};
        bool isInput{true};
        std::string connectedPortId;
    };

    struct ShaderNode {
        std::string nodeId;
        std::string name;
        NodeType nodeType{NodeType::Math};
        float posX{0.0f};
        float posY{0.0f};
        std::vector<Port> ports;
        std::string customCode;
    };

    struct NodeConnection {
        std::string connectionId;
        std::string fromNodeId;
        std::string fromPortId;
        std::string toNodeId;
        std::string toPortId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ShaderGraphEditorTool"; }
    bool IsActive() const override { return m_active; }

    // Graph management
    std::string CreateGraph(const std::string& name, ShaderDomain domain = ShaderDomain::Surface);
    bool SetActiveGraph(const std::string& graphId);
    bool DeleteGraph(const std::string& graphId);
    int GetGraphCount() const { return static_cast<int>(m_graphs.size()); }

    // Node operations
    std::string AddNode(const std::string& name, NodeType type, float posX = 0.0f, float posY = 0.0f);
    bool RemoveNode(const std::string& nodeId);
    bool MoveNode(const std::string& nodeId, float posX, float posY);
    bool SetNodeCustomCode(const std::string& nodeId, const std::string& code);
    int GetNodeCount() const { return static_cast<int>(m_nodes.size()); }
    const ShaderNode* GetNode(const std::string& nodeId) const;

    // Port operations
    std::string AddPort(const std::string& nodeId, const std::string& name,
                        PortType type, bool isInput);
    bool RemovePort(const std::string& nodeId, const std::string& portId);

    // Connection operations
    std::string ConnectNodes(const std::string& fromNodeId, const std::string& fromPortId,
                              const std::string& toNodeId, const std::string& toPortId);
    bool DisconnectNodes(const std::string& connectionId);
    bool HasConnection(const std::string& fromNodeId, const std::string& toNodeId) const;
    int GetConnectionCount() const { return static_cast<int>(m_connections.size()); }
    const NodeConnection* GetConnection(const std::string& connectionId) const;

    // Compilation
    bool CompileGraph(const std::string& graphId);
    bool IsCompiled(const std::string& graphId) const;
    std::string GetCompiledSource(const std::string& graphId) const;
    std::string GetLastCompileError() const { return m_lastCompileError; }

    // Persistence
    bool SaveGraph(const std::string& graphId, const std::string& filePath) const;
    std::string LoadGraph(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::vector<std::pair<std::string, std::string>> m_graphs; // id, name
    std::unordered_map<std::string, ShaderNode> m_nodes;
    std::vector<NodeConnection> m_connections;
    std::string m_activeGraphId;
    std::string m_lastCompileError;
    int m_nextGraphIndex{0};
    int m_nextNodeIndex{0};
    int m_nextConnIndex{0};
};

} // namespace Atlas::Editor
