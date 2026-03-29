#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P1 Tool — Place, edit, and preview scene lights.
class LightingControlTool : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "LightingControlTool"; }
    bool IsActive() const override { return m_active; }

    void AddLight(const std::string& type, float x, float y, float z);
    void RemoveLight(const std::string& lightId);
    void SetLightIntensity(const std::string& lightId, float intensity);
    void ToggleShadows(const std::string& lightId, bool enabled);
    int GetLightCount() const { return static_cast<int>(m_lightIds.size()); }

private:
    bool m_active{false};
    std::vector<std::string> m_lightIds;
};

} // namespace Atlas::Editor
