#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P4 Tool — Scatter objects across surfaces using density masks and PCG seeds.
class ObjectScatterTool : public ITool {
public:
    struct ScatterParams {
        std::string prefabId;
        float density{1.0f};
        float minScale{0.8f};
        float maxScale{1.2f};
        float randomRotation{360.0f};
        int pcgSeed{0};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ObjectScatterTool"; }
    bool IsActive() const override { return m_active; }

    void SetScatterParams(const ScatterParams& params);
    const ScatterParams& GetScatterParams() const { return m_params; }
    int ScatterAt(float worldX, float worldZ, float radius);
    void ClearScatter();
    int GetScatteredCount() const { return static_cast<int>(m_scattered.size()); }

private:
    bool m_active{false};
    ScatterParams m_params;
    std::vector<std::string> m_scattered;
};

} // namespace Atlas::Editor
