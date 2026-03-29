#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P5 Tool — Define axis-aligned trigger volumes for physics events and scripted triggers.
class TriggerVolumeTool : public ITool {
public:
    enum class TriggerShape { Box, Sphere, Capsule };

    struct TriggerVolume {
        std::string id;
        TriggerShape shape{TriggerShape::Box};
        float x{0.0f};
        float y{0.0f};
        float z{0.0f};
        float sizeX{5.0f};
        float sizeY{5.0f};
        float sizeZ{5.0f};
        std::string onEnterEvent;
        std::string onExitEvent;
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "TriggerVolumeTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateVolume(float x, float y, float z,
                             TriggerShape shape = TriggerShape::Box);
    bool RemoveVolume(const std::string& id);
    bool SetVolumeSize(const std::string& id, float sx, float sy, float sz);
    bool BindEvent(const std::string& id, const std::string& onEnter,
                   const std::string& onExit);
    bool SetEnabled(const std::string& id, bool enabled);
    const std::vector<TriggerVolume>& GetVolumes() const { return m_volumes; }
    int GetVolumeCount() const { return static_cast<int>(m_volumes.size()); }

private:
    bool m_active{false};
    std::vector<TriggerVolume> m_volumes;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
