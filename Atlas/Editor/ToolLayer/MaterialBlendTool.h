#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P8 Tool — Multi-layer material blending tool for terrain and surfaces.
class MaterialBlendTool : public ITool {
public:
    enum class BlendMode { Lerp, Multiply, Additive, Screen, Overlay, Mask };
    enum class BlendMaskType { Noise, Slope, Height, Manual, Texture };

    struct BlendLayer {
        std::string layerId;
        std::string name;
        std::string materialAsset;
        float weight{1.0f};
        int order{0};
        BlendMode blendMode{BlendMode::Lerp};
        BlendMaskType maskType{BlendMaskType::Manual};
        bool visible{true};
        bool locked{false};
    };

    struct BlendMask {
        std::string maskId;
        std::string layerId;
        BlendMaskType type{BlendMaskType::Manual};
        float minValue{0.0f};
        float maxValue{1.0f};
        float softness{0.1f};
        std::string textureAsset;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MaterialBlendTool"; }
    bool IsActive() const override { return m_active; }

    // Layer management
    std::string AddLayer(const std::string& name, const std::string& materialAsset,
                         BlendMode mode = BlendMode::Lerp);
    bool RemoveLayer(const std::string& layerId);
    bool MoveLayer(const std::string& layerId, int newOrder);
    bool SetLayerWeight(const std::string& layerId, float weight);
    bool SetLayerVisible(const std::string& layerId, bool visible);
    bool SetLayerLocked(const std::string& layerId, bool locked);
    bool SetLayerMaterial(const std::string& layerId, const std::string& materialAsset);
    int GetLayerCount() const { return static_cast<int>(m_layers.size()); }
    const BlendLayer* GetLayer(const std::string& layerId) const;
    std::vector<std::string> GetLayerIds() const;
    std::vector<std::string> GetLayerIdsByOrder() const;

    // Mask management
    std::string AddMask(const std::string& layerId, BlendMaskType type);
    bool RemoveMask(const std::string& maskId);
    bool SetMaskRange(const std::string& maskId, float minValue, float maxValue);
    bool SetMaskSoftness(const std::string& maskId, float softness);
    bool SetMaskTexture(const std::string& maskId, const std::string& textureAsset);
    int GetMaskCount() const { return static_cast<int>(m_masks.size()); }
    const BlendMask* GetMask(const std::string& maskId) const;

    // Painting
    bool PaintLayer(const std::string& layerId, float wx, float wz,
                    float radius, float strength);
    bool EraseLayer(const std::string& layerId, float wx, float wz, float radius);
    bool FillLayer(const std::string& layerId, float weight = 1.0f);

    // Baking
    bool BakeBlendMap(const std::string& outputPath, int resolution = 1024) const;

    // Persistence
    bool SaveBlendConfig(const std::string& filePath) const;
    bool LoadBlendConfig(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::vector<BlendLayer> m_layers;
    std::vector<BlendMask> m_masks;
    int m_nextLayerIndex{0};
    int m_nextMaskIndex{0};
};

} // namespace Atlas::Editor
