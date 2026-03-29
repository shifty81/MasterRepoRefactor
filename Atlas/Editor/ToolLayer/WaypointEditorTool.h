#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P4 Tool — Place, move and chain waypoints for AI navigation and scripted paths.
class WaypointEditorTool : public ITool {
public:
    struct Waypoint {
        std::string id;
        float x{0.0f};
        float y{0.0f};
        float z{0.0f};
        std::string nextId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "WaypointEditorTool"; }
    bool IsActive() const override { return m_active; }

    std::string AddWaypoint(float x, float y, float z);
    bool RemoveWaypoint(const std::string& id);
    bool ChainWaypoints(const std::string& fromId, const std::string& toId);
    const std::vector<Waypoint>& GetWaypoints() const { return m_waypoints; }
    int GetWaypointCount() const { return static_cast<int>(m_waypoints.size()); }

private:
    bool m_active{false};
    std::vector<Waypoint> m_waypoints;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
