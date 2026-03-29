#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P2 Tool — Star system map editing: add/remove/move celestials.
class MapEditorTool : public ITool {
public:
    struct MapNode {
        std::string id;
        std::string type;
        float orbitRadius{0.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MapEditorTool"; }
    bool IsActive() const override { return m_active; }

    void AddNode(const std::string& id, const std::string& type, float orbitRadius);
    void RemoveNode(const std::string& id);
    void MoveNode(const std::string& id, float newOrbitRadius);
    void SetActiveSystem(const std::string& systemId);

    const std::string& GetActiveSystem() const { return m_activeSystem; }
    int GetNodeCount() const { return static_cast<int>(m_nodes.size()); }

private:
    bool m_active{false};
    std::string m_activeSystem;
    std::vector<MapNode> m_nodes;
};

} // namespace Atlas::Editor
