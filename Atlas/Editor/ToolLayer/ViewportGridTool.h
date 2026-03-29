#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>
#include <array>

namespace Atlas::Editor {

/// P14 Tool — Viewport grid with snapping, alignment modes, and layered grid configs
class ViewportGridTool : public ITool {
public:
    enum class GridType { Cartesian, Isometric, Hex, Polar, Custom };
    enum class GridAlignment { World, Camera, Screen };
    enum class SnapAxis { None, X, Y, Z, XY, XZ, YZ, All };

    struct GridConfig {
        std::string configId;
        GridType type{GridType::Cartesian};
        GridAlignment alignment{GridAlignment::World};
        float spacingX{1.0f};
        float spacingY{1.0f};
        float spacingZ{1.0f};
        bool visible{true};
        std::array<float, 4> color{0.5f, 0.5f, 0.5f, 0.5f};
        int subdivisions{4};
    };

    struct SnapSettings {
        bool enabled{false};
        SnapAxis axis{SnapAxis::All};
        float snapIncrement{1.0f};
        float rotationSnapDeg{15.0f};
        float scaleSnapIncrement{0.1f};
        bool snapToVertices{false};
        bool snapToEdges{false};
        bool snapToSurfaces{false};
    };

    struct GridLayerSettings {
        std::string layerId;
        std::string name;
        GridConfig config;
        SnapSettings snap;
        int zOrder{0};
        bool locked{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ViewportGridTool"; }
    bool IsActive() const override { return m_active; }

    void SetGridType(GridType type);
    void SetGridSpacing(float x, float y, float z = 1.0f);
    void SetGridAlignment(GridAlignment alignment);
    void SetGridSubdivisions(int subdivisions);
    void SetGridColor(float r, float g, float b, float a = 1.0f);
    void ShowGrid();
    void HideGrid();
    bool IsGridVisible() const;

    void EnableSnapping(bool enable);
    void SetSnapAxis(SnapAxis axis);
    void SetSnapIncrement(float increment);
    void SetRotationSnap(float degrees);
    void SetScaleSnap(float increment);
    void SetSnapToVertices(bool enable);
    void SetSnapToEdges(bool enable);

    std::array<float, 3> GetNearestGridPoint(float x, float y, float z) const;
    std::array<float, 3> SnapPosition(float x, float y, float z) const;
    float SnapRotation(float degrees) const;

    std::string AddGridLayer(const std::string& name);
    bool RemoveGridLayer(const std::string& layerId);
    bool SetLayerActive(const std::string& layerId, bool active);
    bool SetLayerLocked(const std::string& layerId, bool locked);
    bool SetLayerZOrder(const std::string& layerId, int zOrder);
    const GridLayerSettings* GetLayer(const std::string& layerId) const;
    std::vector<std::string> GetLayerIds() const;

    const GridConfig& GetCurrentConfig() const;
    const SnapSettings& GetSnapSettings() const;

    bool SaveGridConfig(const std::string& filePath) const;
    bool LoadGridConfig(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    GridConfig m_currentConfig;
    SnapSettings m_snapSettings;
    std::unordered_map<std::string, GridLayerSettings> m_layers;
    int m_nextLayerIndex{0};
};

} // namespace Atlas::Editor
