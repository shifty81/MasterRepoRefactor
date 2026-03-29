#pragma once
#include "ITool.h"
#include <string>

namespace Atlas::Editor {

/// P3 Tool — Display scene hierarchy, physics body, memory, and draw-call stats.
class AssetStatsPanel : public ITool {
public:
    struct SceneStats {
        int totalEntities{0};
        int physicsBodyCount{0};
        int drawCallCount{0};
        float memoryMB{0.0f};
        int vertexCount{0};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AssetStatsPanel"; }
    bool IsActive() const override { return m_active; }

    void Refresh();
    const SceneStats& GetStats() const { return m_stats; }
    void SetAutoRefresh(bool enabled);
    bool IsAutoRefresh() const { return m_autoRefresh; }

private:
    bool m_active{false};
    bool m_autoRefresh{false};
    SceneStats m_stats;
};

} // namespace Atlas::Editor
