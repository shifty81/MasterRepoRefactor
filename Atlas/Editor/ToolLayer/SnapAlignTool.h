#pragma once
#include "ITool.h"
#include <string>

namespace Atlas::Editor {

/// P0 Tool — Grid, surface, and asset alignment.
class SnapAlignTool : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SnapAlignTool"; }
    bool IsActive() const override { return m_active; }

    void SetGridSize(float size);
    float GetGridSize() const { return m_gridSize; }
    void SetSnapToSurface(bool enabled);
    bool IsSnapToSurface() const { return m_snapToSurface; }
    void SnapEntity(const std::string& entityId);

private:
    bool m_active{false};
    float m_gridSize{1.0f};
    bool m_snapToSurface{false};
};

} // namespace Atlas::Editor
