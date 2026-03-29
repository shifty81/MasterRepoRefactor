#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P6 Tool — Paint foliage instances (grass, bushes, trees) onto terrain surfaces.
class FoliagePainterTool : public ITool {
public:
    struct FoliageLayer {
        std::string layerId;
        std::string meshAsset;
        float density{1.0f};
        float minScale{0.8f};
        float maxScale{1.2f};
        float alignToNormal{1.0f};
        int pcgSeed{0};
    };

    struct FoliageBrush {
        float radius{5.0f};
        float strength{1.0f};
        bool erasing{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "FoliagePainterTool"; }
    bool IsActive() const override { return m_active; }

    std::string AddLayer(const std::string& meshAsset, float density = 1.0f);
    bool RemoveLayer(const std::string& layerId);
    bool SetLayerDensity(const std::string& layerId, float density);
    bool SetLayerScaleRange(const std::string& layerId, float minS, float maxS);
    void SetBrushRadius(float radius);
    void SetBrushStrength(float strength);
    void SetEraseMode(bool erasing);
    int PaintArea(float x, float z, float radius, const std::string& layerId);
    int EraseArea(float x, float z, float radius);
    int GetLayerCount() const { return static_cast<int>(m_layers.size()); }
    int GetTotalInstances() const { return m_totalInstances; }
    void ClearAll();
    const FoliageBrush& GetBrush() const { return m_brush; }

private:
    bool m_active{false};
    std::vector<FoliageLayer> m_layers;
    FoliageBrush m_brush;
    int m_nextIndex{0};
    int m_totalInstances{0};
};

} // namespace Atlas::Editor
