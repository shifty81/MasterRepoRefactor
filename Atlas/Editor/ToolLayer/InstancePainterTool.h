#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P10 Tool — Instance painting for large-scale placement of mesh instances.
class InstancePainterTool : public ITool {
public:
    enum class PaintMode { Paint, Erase, Scatter, Align, Scale };
    enum class DistributionMode { Uniform, Poisson, Clustered, Random };
    enum class SurfaceSnapMode { None, Normal, WorldUp, Custom };

    struct InstanceVariation {
        float scaleMin{0.8f};
        float scaleMax{1.2f};
        float rotationRangeY{360.0f};
        float rotationRangeX{0.0f};
        float rotationRangeZ{0.0f};
        bool randomRotationY{true};
        float offsetY{0.0f};
    };

    struct InstanceRecord {
        std::string instanceId;
        std::string meshId;
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float rotX{0.0f};
        float rotY{0.0f};
        float rotZ{0.0f};
        float scaleX{1.0f};
        float scaleY{1.0f};
        float scaleZ{1.0f};
        bool visible{true};
    };

    struct PaintLayer {
        std::string layerId;
        std::string name;
        std::string meshId;
        PaintMode paintMode{PaintMode::Paint};
        DistributionMode distribution{DistributionMode::Poisson};
        SurfaceSnapMode snapMode{SurfaceSnapMode::Normal};
        InstanceVariation variation;
        float brushRadius{5.0f};
        float brushDensity{0.5f};
        float brushStrength{1.0f};
        int maxInstances{10000};
        bool slopeFilter{false};
        float maxSlopeDegrees{45.0f};
        bool heightFilter{false};
        float minHeight{-9999.0f};
        float maxHeight{9999.0f};
        std::vector<InstanceRecord> instances;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "InstancePainterTool"; }
    bool IsActive() const override { return m_active; }

    // Layer management
    std::string CreateLayer(const std::string& name, const std::string& meshId);
    bool RemoveLayer(const std::string& layerId);
    bool SetLayerMesh(const std::string& layerId, const std::string& meshId);
    bool SetPaintMode(const std::string& layerId, PaintMode mode);
    bool SetDistributionMode(const std::string& layerId, DistributionMode mode);
    bool SetSurfaceSnapMode(const std::string& layerId, SurfaceSnapMode mode);
    bool SetBrushRadius(const std::string& layerId, float radius);
    bool SetBrushDensity(const std::string& layerId, float density);
    bool SetBrushStrength(const std::string& layerId, float strength);
    bool SetMaxInstances(const std::string& layerId, int maxCount);
    bool SetSlopeFilter(const std::string& layerId, bool enabled, float maxDeg = 45.0f);
    bool SetHeightFilter(const std::string& layerId, bool enabled,
                          float minH = -9999.0f, float maxH = 9999.0f);
    int GetLayerCount() const { return static_cast<int>(m_layers.size()); }
    const PaintLayer* GetLayer(const std::string& layerId) const;
    std::vector<std::string> GetLayerIds() const;

    // Variation
    bool SetVariation(const std::string& layerId, float scaleMin, float scaleMax,
                       float rotRangeY = 360.0f, bool randomRotY = true);

    // Instance operations
    std::string PaintInstance(const std::string& layerId,
                               float px, float py, float pz,
                               float rotY = 0.0f, float scale = 1.0f);
    bool EraseInstance(const std::string& layerId, const std::string& instanceId);
    int GetInstanceCount(const std::string& layerId) const;
    int GetTotalInstanceCount() const;
    void ClearLayer(const std::string& layerId);

    // Persistence
    bool SaveLayers(const std::string& filePath) const;
    bool LoadLayers(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, PaintLayer> m_layers;
    int m_nextLayerIndex{0};
    int m_nextInstanceIndex{0};
};

} // namespace Atlas::Editor
