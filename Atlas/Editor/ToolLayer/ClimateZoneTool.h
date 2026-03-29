#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P5 Tool — Define climate and weather zones that drive ambient VFX and gameplay.
class ClimateZoneTool : public ITool {
public:
    struct ClimateZone {
        std::string id;
        std::string climate;
        float centerX{0.0f};
        float centerZ{0.0f};
        float radius{50.0f};
        float temperature{20.0f};
        float precipitation{0.5f};
        std::string weatherPreset;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ClimateZoneTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateZone(const std::string& climate,
                           float centerX, float centerZ, float radius);
    bool RemoveZone(const std::string& id);
    bool SetTemperature(const std::string& id, float temp);
    bool SetWeatherPreset(const std::string& id, const std::string& preset);
    const std::vector<ClimateZone>& GetZones() const { return m_zones; }
    int GetZoneCount() const { return static_cast<int>(m_zones.size()); }
    void RegisterClimatePreset(const std::string& climate, const std::string& desc);
    int GetPresetCount() const { return static_cast<int>(m_presets.size()); }

private:
    bool m_active{false};
    std::vector<ClimateZone> m_zones;
    std::unordered_map<std::string, std::string> m_presets;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
