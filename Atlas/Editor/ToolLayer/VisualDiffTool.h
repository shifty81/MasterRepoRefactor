#pragma once
#include "ITool.h"
#include <string>

namespace Atlas::Editor {

/// P3 Tool — Compare current scene/asset state against a baseline snapshot.
class VisualDiffTool : public ITool {
public:
    enum class DiffMode { Scene, Asset, Transform, Material };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "VisualDiffTool"; }
    bool IsActive() const override { return m_active; }

    void SetBaseline(const std::string& snapshotId);
    void SetDiffMode(DiffMode mode);
    void Refresh();
    int GetChangedEntityCount() const { return m_changedCount; }
    DiffMode GetDiffMode() const { return m_diffMode; }

private:
    bool m_active{false};
    DiffMode m_diffMode{DiffMode::Scene};
    int m_changedCount{0};
};

} // namespace Atlas::Editor
