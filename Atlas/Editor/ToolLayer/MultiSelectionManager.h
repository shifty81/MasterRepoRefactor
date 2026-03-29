#pragma once
#include "ITool.h"
#include <vector>
#include <string>

namespace Atlas::Editor {

/// P0 Tool — Select and group multiple scene assets.
class MultiSelectionManager : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MultiSelectionManager"; }
    bool IsActive() const override { return m_active; }

    void SelectEntity(const std::string& entityId);
    void DeselectEntity(const std::string& entityId);
    void ClearSelection();
    void GroupSelected(const std::string& groupName);
    const std::vector<std::string>& GetSelected() const { return m_selected; }
    int GetSelectedCount() const { return static_cast<int>(m_selected.size()); }

private:
    bool m_active{false};
    std::vector<std::string> m_selected;
};

} // namespace Atlas::Editor
