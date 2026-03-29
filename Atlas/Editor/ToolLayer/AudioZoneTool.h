#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P4 Tool — Define audio trigger zones with volume, reverb and asset assignment.
class AudioZoneTool : public ITool {
public:
    struct AudioZone {
        std::string id;
        std::string audioAsset;
        float centerX{0.0f};
        float centerZ{0.0f};
        float radius{10.0f};
        float volume{1.0f};
        bool loop{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AudioZoneTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateZone(float centerX, float centerZ, float radius,
                           const std::string& audioAsset);
    bool RemoveZone(const std::string& id);
    bool SetZoneVolume(const std::string& id, float volume);
    const std::vector<AudioZone>& GetZones() const { return m_zones; }
    int GetZoneCount() const { return static_cast<int>(m_zones.size()); }

private:
    bool m_active{false};
    std::vector<AudioZone> m_zones;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
