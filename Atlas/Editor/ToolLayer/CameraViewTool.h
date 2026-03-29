#pragma once
#include "ITool.h"
#include <string>

namespace Atlas::Editor {

/// P0 Tool — Free-fly, orbit, and orthographic camera views.
class CameraViewTool : public ITool {
public:
    enum class ViewMode { FreeFly, Orbit, Orthographic };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "CameraViewTool"; }
    bool IsActive() const override { return m_active; }

    void SetViewMode(ViewMode mode);
    ViewMode GetViewMode() const { return m_viewMode; }
    void SetFOV(float fov);
    float GetFOV() const { return m_fov; }
    void FocusOnEntity(const std::string& entityId);

private:
    bool m_active{false};
    ViewMode m_viewMode{ViewMode::FreeFly};
    float m_fov{60.0f};
};

} // namespace Atlas::Editor
