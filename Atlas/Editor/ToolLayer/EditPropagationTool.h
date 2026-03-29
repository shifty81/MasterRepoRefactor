#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P3 Tool — Propagate property edits to all similar assets in the scene.
class EditPropagationTool : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "EditPropagationTool"; }
    bool IsActive() const override { return m_active; }

    void SetSourceEntity(const std::string& entityId);
    void PropagateProperty(const std::string& propertyName, bool dryRun = false);
    void PropagateAll(bool dryRun = false);
    int GetAffectedCount() const { return m_affectedCount; }
    int GetDryRunPreviewCount() const { return m_dryRunCount; }

private:
    bool m_active{false};
    std::string m_sourceEntity;
    int m_affectedCount{0};
    int m_dryRunCount{0};
};

} // namespace Atlas::Editor
