#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P5 Tool — Place and configure reflection/lighting environment probes.
class EnvironmentProbesTool : public ITool {
public:
    enum class ProbeType { Reflection, Irradiance, Mixed };

    struct Probe {
        std::string id;
        ProbeType type{ProbeType::Reflection};
        float x{0.0f};
        float y{0.0f};
        float z{0.0f};
        float radius{10.0f};
        int resolution{128};
        bool realtime{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "EnvironmentProbesTool"; }
    bool IsActive() const override { return m_active; }

    std::string AddProbe(float x, float y, float z, ProbeType type = ProbeType::Reflection);
    bool RemoveProbe(const std::string& id);
    bool SetProbeRadius(const std::string& id, float radius);
    bool BakeProbe(const std::string& id);
    void BakeAll();
    const std::vector<Probe>& GetProbes() const { return m_probes; }
    int GetProbeCount() const { return static_cast<int>(m_probes.size()); }

private:
    bool m_active{false};
    std::vector<Probe> m_probes;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
