#pragma once
#include "ITool.h"

namespace Atlas::Editor {

/// P1 Tool — Pause, step, and scrub physics simulation.
class SimulationStepController : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SimulationStepController"; }
    bool IsActive() const override { return m_active; }

    void Pause();
    void Resume();
    void StepForward(int frames = 1);
    void StepBackward(int frames = 1);
    void SetTimeScale(float scale);
    float GetTimeScale() const { return m_timeScale; }
    bool IsPaused() const { return m_paused; }

private:
    bool m_active{false};
    bool m_paused{false};
    float m_timeScale{1.0f};
};

} // namespace Atlas::Editor
