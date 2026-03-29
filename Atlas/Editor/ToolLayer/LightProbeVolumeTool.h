#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P6 Tool — Place volumetric grids of light probes for indirect lighting capture.
class LightProbeVolumeTool : public ITool {
public:
    struct ProbeVolume {
        std::string volumeId;
        float minX{0.0f};
        float minY{0.0f};
        float minZ{0.0f};
        float maxX{10.0f};
        float maxY{10.0f};
        float maxZ{10.0f};
        int resolutionX{4};
        int resolutionY{4};
        int resolutionZ{4};
        bool baked{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "LightProbeVolumeTool"; }
    bool IsActive() const override { return m_active; }

    std::string AddVolume(float minX, float minY, float minZ,
                          float maxX, float maxY, float maxZ);
    bool RemoveVolume(const std::string& volumeId);
    bool SetResolution(const std::string& volumeId, int rx, int ry, int rz);
    bool BakeVolume(const std::string& volumeId);
    void BakeAll();
    int GetBakedCount() const;
    const std::vector<ProbeVolume>& GetVolumes() const { return m_volumes; }
    int GetVolumeCount() const { return static_cast<int>(m_volumes.size()); }
    int GetTotalProbeCount() const;

private:
    bool m_active{false};
    std::vector<ProbeVolume> m_volumes;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
