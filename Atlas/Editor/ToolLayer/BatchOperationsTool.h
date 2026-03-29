#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P3 Tool — Apply mass transformations, rename, retag, and delete multiple assets.
class BatchOperationsTool : public ITool {
public:
    enum class Operation { Translate, Rotate, Scale, Rename, Retag, Delete };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "BatchOperationsTool"; }
    bool IsActive() const override { return m_active; }

    void AddToSelection(const std::string& entityId);
    void ClearSelection();
    void ApplyTranslate(float dx, float dy, float dz);
    void ApplyScale(float sx, float sy, float sz);
    void ApplyDelete();
    void ApplyRetag(const std::string& newTag);

    int GetSelectionSize() const { return static_cast<int>(m_selection.size()); }
    int GetLastOperationAffectedCount() const { return m_lastAffectedCount; }

private:
    bool m_active{false};
    std::vector<std::string> m_selection;
    int m_lastAffectedCount{0};
};

} // namespace Atlas::Editor
