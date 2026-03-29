#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P2 Tool — Balance resource distribution across zones and factions.
class ResourceBalancerTool : public ITool {
public:
    struct ResourceZone {
        std::string zoneId;
        std::string resourceType;
        float abundance{1.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ResourceBalancerTool"; }
    bool IsActive() const override { return m_active; }

    void AddZone(const std::string& zoneId, const std::string& resourceType,
                 float abundance);
    void SetAbundance(const std::string& zoneId, float abundance);
    void NormalizeAll();
    void ExportConfig(const std::string& outputPath);

    int GetZoneCount() const { return static_cast<int>(m_zones.size()); }

private:
    bool m_active{false};
    std::vector<ResourceZone> m_zones;
};

} // namespace Atlas::Editor
