#pragma once
#include "ITool.h"
#include <string>

namespace Atlas::Editor {

/// P0 Tool — Edit scene assets while simulation is running.
class LiveEditMode : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "LiveEditMode"; }
    bool IsActive() const override { return m_active; }

    void PauseSimulation();
    void ResumeSimulation();
    bool IsSimulationPaused() const { return m_simPaused; }
    void CommitLiveEdit(const std::string& entityId);

private:
    bool m_active{false};
    bool m_simPaused{false};
};

} // namespace Atlas::Editor
