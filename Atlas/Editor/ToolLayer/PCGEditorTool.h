#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P19 Tool — Procedural Content Generation graph authoring, node configuration, and point data management.
class PCGEditorTool : public ITool {
public:
    enum class PCGNodeCategory { Sampler, Filter, Transform, Attribute, Debug, Subgraph, Blueprint, Custom };
    enum class PCGExecutionMode { Normal, Debug, Isolated, Inherited };
    enum class PCGGridType { Landscape, Spline, Volume, Surface, Point, Custom };

    struct PCGNodeDef {
        std::string nodeId;
        std::string name;
        PCGNodeCategory category{PCGNodeCategory::Sampler};
        std::vector<std::string> pins;
        std::vector<std::string> properties;
        bool enabled{true};
        bool debugMode{false};
    };

    struct PCGGraphProperty {
        std::string propId;
        std::string name;
        std::string propType;
        std::string value;
        bool exposed{false};
        bool overridable{false};
    };

    struct PCGGridConfig {
        std::string gridId;
        std::string name;
        PCGGridType gridType{PCGGridType::Point};
        std::vector<float> dimensions;
        float cellSize{100.0f};
        float resolution{1.0f};
        float boundExpand{0.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "PCGEditorTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateGraph(const std::string& name);
    bool RemoveGraph(const std::string& graphId);
    std::string AddNode(const std::string& graphId, const std::string& name, PCGNodeCategory category);
    bool RemoveNode(const std::string& graphId, const std::string& nodeId);
    bool ConnectPins(const std::string& srcNodeId, const std::string& srcPin, const std::string& dstNodeId, const std::string& dstPin);
    bool DisconnectPins(const std::string& srcNodeId, const std::string& srcPin, const std::string& dstNodeId, const std::string& dstPin);
    std::string AddProperty(const std::string& graphId, const std::string& name, const std::string& propType);
    bool RemoveProperty(const std::string& graphId, const std::string& propId);
    bool SetPropertyValue(const std::string& propId, const std::string& value);
    bool SetExecutionMode(const std::string& graphId, PCGExecutionMode mode);
    bool SetGridType(const std::string& graphId, PCGGridType gridType);
    bool SetGridResolution(const std::string& graphId, float resolution);
    bool EnableDebugMode(const std::string& nodeId);
    bool DisableDebugMode(const std::string& nodeId);
    bool PreviewGraph(const std::string& graphId);
    bool ExecuteGraph(const std::string& graphId);
    bool ExecuteGraphAsync(const std::string& graphId, const std::string& callbackId);
    bool CancelExecution(const std::string& graphId);
    const PCGNodeDef* GetNode(const std::string& nodeId) const;
    const PCGGraphProperty* GetProperty(const std::string& propId) const;
    std::vector<std::string> GetAllGraphIds() const;
    std::vector<std::string> GetNodesByCategory(PCGNodeCategory category) const;
    bool ValidateGraph(const std::string& graphId) const;
    bool ExportGraph(const std::string& graphId, const std::string& filePath) const;
    bool SaveGraph(const std::string& graphId, const std::string& filePath) const;
    bool LoadGraph(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, PCGNodeDef> m_nodes;
    std::unordered_map<std::string, PCGGraphProperty> m_properties;
    std::unordered_map<std::string, PCGGridConfig> m_grids;
    int m_nextGraphIndex{0};
    int m_nextNodeIndex{0};
    int m_nextPropIndex{0};
};

} // namespace Atlas::Editor
