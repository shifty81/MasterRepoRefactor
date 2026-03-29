#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P27 Tool — Terrain material blend layer authoring, weight-map painting, and splat map baking.
class TerrainMaterialBlendTool : public ITool {
public:
    enum class BlendLayerType { Base, Detail, Overlay, Decal, Macro, Custom };
    enum class WeightPaintMode { Absolute, Additive, Smooth, Erase, Fill, Custom };
    enum class SplatChannel { R, G, B, A, Custom };
    enum class BlendInterpolation { Linear, Cubic, Nearest, Custom };

    struct BlendLayerDef {
        std::string layerId;
        std::string layerName;
        BlendLayerType layerType{BlendLayerType::Base};
        std::string materialAssetId;
        SplatChannel splatChannel{SplatChannel::R};
        float tilingX{1.0f};
        float tilingY{1.0f};
        float blendSharpness{0.5f};
        int sortOrder{0};
        bool enabled{true};
    };

    struct WeightPaintOpDef {
        std::string opId;
        std::string layerId;
        std::string terrainId;
        WeightPaintMode mode{WeightPaintMode::Absolute};
        float brushRadius{50.0f};
        float brushStrength{0.5f};
        float falloff{0.5f};
        BlendInterpolation interpolation{BlendInterpolation::Linear};
        bool useTextureMask{false};
    };

    struct SplatMapBakeDef {
        std::string bakeId;
        std::string terrainId;
        int textureWidth{1024};
        int textureHeight{1024};
        std::string outputPath;
        bool includeAlpha{true};
        bool normalizeWeights{true};
        bool completed{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "TerrainMaterialBlendTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateLayer(const BlendLayerDef& def);
    bool DeleteLayer(const std::string& layerId);
    bool EnableLayer(const std::string& layerId, bool enabled);
    bool SetLayerOrder(const std::string& layerId, int order);
    const BlendLayerDef* GetLayer(const std::string& layerId) const;
    std::vector<std::string> GetAllLayerIds() const;
    std::vector<std::string> GetLayersByType(BlendLayerType type) const;
    std::vector<std::string> GetLayersBySplatChannel(SplatChannel channel) const;
    std::vector<std::string> GetEnabledLayers() const;
    bool AddWeightPaintOp(const WeightPaintOpDef& op);
    bool RemoveWeightPaintOp(const std::string& opId);
    bool ApplyWeightPaintOp(const std::string& opId);
    const WeightPaintOpDef* GetWeightPaintOp(const std::string& opId) const;
    std::vector<std::string> GetWeightPaintOpsByLayer(const std::string& layerId) const;
    bool CreateSplatMapBake(const SplatMapBakeDef& def);
    bool ExecuteSplatMapBake(const std::string& bakeId);
    bool DeleteSplatMapBake(const std::string& bakeId);
    const SplatMapBakeDef* GetSplatMapBake(const std::string& bakeId) const;
    std::vector<std::string> GetSplatMapBakesByTerrain(const std::string& terrainId) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, BlendLayerDef> m_layers;
    std::unordered_map<std::string, WeightPaintOpDef> m_paintOps;
    std::unordered_map<std::string, SplatMapBakeDef> m_splatBakes;
};

} // namespace Atlas::Editor
