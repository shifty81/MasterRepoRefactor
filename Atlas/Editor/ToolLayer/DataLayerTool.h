#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P19 Tool — Data layer authoring, actor assignment, and runtime state management.
class DataLayerTool : public ITool {
public:
    enum class DataLayerState { Unloaded, Loaded, Activated, Deactivated, Error };
    enum class DataLayerType { Editor, Runtime, Both };
    enum class RuntimeDataLayerInit { Activated, Deactivated };

    struct DataLayerDef {
        std::string layerId;
        std::string name;
        DataLayerType layerType{DataLayerType::Runtime};
        RuntimeDataLayerInit runtimeInit{RuntimeDataLayerInit::Deactivated};
        std::string parentId;
        std::vector<float> color;
        std::vector<float> debugColor;
        bool visible{true};
        bool locked{false};
    };

    struct DataLayerAssignment {
        std::string assignmentId;
        std::string actorId;
        std::string layerId;
        bool inherited{false};
    };

    struct DataLayerLoadRequest {
        std::string requestId;
        std::string layerId;
        DataLayerState targetState{DataLayerState::Loaded};
        int priority{0};
        std::vector<std::string> conditions;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "DataLayerTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateDataLayer(const std::string& name, DataLayerType type);
    bool RemoveDataLayer(const std::string& layerId);
    bool SetLayerType(const std::string& layerId, DataLayerType type);
    bool SetRuntimeInit(const std::string& layerId, RuntimeDataLayerInit init);
    bool SetParent(const std::string& layerId, const std::string& parentId);
    bool SetLayerColor(const std::string& layerId, float r, float g, float b);
    bool SetLayerVisible(const std::string& layerId, bool visible);
    bool SetLayerLocked(const std::string& layerId, bool locked);
    bool AssignActor(const std::string& actorId, const std::string& layerId);
    bool UnassignActor(const std::string& actorId, const std::string& layerId);
    bool SetLayerState(const std::string& layerId, DataLayerState state);
    bool RequestLoad(const std::string& layerId);
    bool RequestUnload(const std::string& layerId);
    bool RequestActivate(const std::string& layerId);
    bool RequestDeactivate(const std::string& layerId);
    const DataLayerDef* GetLayer(const std::string& layerId) const;
    std::vector<std::string> GetAllLayerIds() const;
    std::vector<std::string> GetLayersByType(DataLayerType type) const;
    std::vector<std::string> GetLayersByState(DataLayerState state) const;
    std::vector<std::string> GetActorsByLayer(const std::string& layerId) const;
    std::vector<std::string> GetLayersByActor(const std::string& actorId) const;
    std::vector<std::string> GetChildLayers(const std::string& parentId) const;
    bool ValidateLayer(const std::string& layerId) const;
    bool ExportLayers(const std::string& filePath) const;
    bool SaveLayers(const std::string& filePath) const;
    bool LoadLayers(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, DataLayerDef> m_layers;
    std::unordered_map<std::string, DataLayerAssignment> m_assignments;
    std::unordered_map<std::string, DataLayerState> m_states;
    int m_nextLayerIndex{0};
    int m_nextAssignmentIndex{0};
};

} // namespace Atlas::Editor
