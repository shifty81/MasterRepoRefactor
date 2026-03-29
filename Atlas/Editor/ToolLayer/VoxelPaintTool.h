#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P24 Tool — Voxel volume painting, density sculpting, and material layer stamping.
class VoxelPaintTool : public ITool {
public:
    enum class VoxelPaintMode { Add, Remove, Smooth, Flatten, Paint, Stamp, Custom };
    enum class VoxelBrushShape { Sphere, Box, Cylinder, Custom };
    enum class VoxelMaterialLayer { Base, Detail, Trim, Decal, Emissive, Custom };
    enum class VoxelSculptAxis { X, Y, Z, Normal, Free, Custom };

    struct VoxelBrushDef {
        std::string brushId;
        std::string brushName;
        VoxelBrushShape shape{VoxelBrushShape::Sphere};
        VoxelPaintMode mode{VoxelPaintMode::Add};
        float radius{50.0f};
        float strength{1.0f};
        float falloff{0.5f};
    };

    struct VoxelStrokeRecord {
        std::string strokeId;
        std::string brushId;
        VoxelSculptAxis axis{VoxelSculptAxis::Normal};
        int samplesCount{0};
        bool committed{false};
        float totalVolumeDelta{0.0f};
    };

    struct VoxelLayerConfig {
        std::string layerId;
        std::string brushId;
        VoxelMaterialLayer layer{VoxelMaterialLayer::Base};
        std::string materialAssetId;
        float opacity{1.0f};
        bool visible{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "VoxelPaintTool"; }
    bool IsActive() const override { return m_active; }

    bool RegisterBrush(const VoxelBrushDef& def);
    bool UnregisterBrush(const std::string& brushId);
    const VoxelBrushDef* GetBrush(const std::string& brushId) const;
    std::vector<std::string> GetAllBrushIds() const;
    std::vector<std::string> GetBrushesByMode(VoxelPaintMode mode) const;
    bool SetBrushShape(const std::string& brushId, VoxelBrushShape shape);
    bool SetPaintMode(const std::string& brushId, VoxelPaintMode mode);
    std::string BeginStroke(const std::string& brushId, VoxelSculptAxis axis);
    bool CommitStroke(const std::string& strokeId);
    bool CancelStroke(const std::string& strokeId);
    const VoxelStrokeRecord* GetStroke(const std::string& strokeId) const;
    std::vector<std::string> GetAllStrokeIds() const;
    std::vector<std::string> GetPendingStrokes() const;
    std::vector<std::string> GetCommittedStrokes() const;
    bool AddLayerConfig(const VoxelLayerConfig& config);
    bool RemoveLayerConfig(const std::string& layerId);
    const VoxelLayerConfig* GetLayerConfig(const std::string& layerId) const;
    std::vector<std::string> GetLayersByBrush(const std::string& brushId) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, VoxelBrushDef> m_brushes;
    std::unordered_map<std::string, VoxelStrokeRecord> m_strokes;
    std::unordered_map<std::string, VoxelLayerConfig> m_layerConfigs;
};

} // namespace Atlas::Editor
