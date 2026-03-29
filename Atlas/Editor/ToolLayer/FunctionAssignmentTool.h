#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P2 Tool — Assign trigger functions and callbacks to scene entities.
class FunctionAssignmentTool : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "FunctionAssignmentTool"; }
    bool IsActive() const override { return m_active; }

    void AssignFunction(const std::string& entityId, const std::string& trigger,
                        const std::string& functionName);
    void RemoveFunction(const std::string& entityId, const std::string& trigger);
    const std::vector<std::string>& GetAssignedEntities() const { return m_assignedEntities; }
    int GetAssignmentCount() const { return static_cast<int>(m_assignedEntities.size()); }

private:
    bool m_active{false};
    std::vector<std::string> m_assignedEntities;
};

} // namespace Atlas::Editor
