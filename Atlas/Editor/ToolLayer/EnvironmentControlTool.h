#pragma once
#include "ITool.h"
#include <string>

namespace Atlas::Editor {

/// P1 Tool — Control skybox, lighting, weather, and ambient environment.
class EnvironmentControlTool : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "EnvironmentControlTool"; }
    bool IsActive() const override { return m_active; }

    void SetSkybox(const std::string& skyboxName);
    void SetAmbientLight(float r, float g, float b, float intensity);
    void SetTimeOfDay(float hours);
    float GetTimeOfDay() const { return m_timeOfDay; }

private:
    bool m_active{false};
    float m_timeOfDay{12.0f};
};

} // namespace Atlas::Editor
