#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P10 Tool — Material layer compositor for blending multi-layer surface materials.
class MaterialLayerTool : public ITool {
public:
    enum class BlendOperation { Normal, Multiply, Screen, Overlay, Add, Subtract };
    enum class MaskType { None, Texture, Vertex, Height, Slope, Curvature, Procedural };
    enum class ShadingModel { PBR, Unlit, Subsurface, Hair, Eye, Custom };

    struct TextureSlot {
        std::string slotId;
        std::string slotName;
        std::string texturePath;
        float tilingX{1.0f};
        float tilingY{1.0f};
        float offsetX{0.0f};
        float offsetY{0.0f};
        bool enabled{true};
    };

    struct MaterialLayer {
        std::string layerId;
        std::string name;
        ShadingModel shadingModel{ShadingModel::PBR};
        BlendOperation blendOp{BlendOperation::Normal};
        MaskType maskType{MaskType::None};
        float opacity{1.0f};
        float roughness{0.5f};
        float metallic{0.0f};
        float emissiveIntensity{0.0f};
        float subsurfaceRadius{0.0f};
        bool visible{true};
        std::vector<TextureSlot> textureSlots;
    };

    struct MaterialStack {
        std::string stackId;
        std::string name;
        std::vector<std::string> layerOrder;
        bool useVertexColors{false};
        bool castShadows{true};
        bool receiveShadows{true};
        bool twoSided{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MaterialLayerTool"; }
    bool IsActive() const override { return m_active; }

    // Stack management
    std::string CreateStack(const std::string& name);
    bool RemoveStack(const std::string& stackId);
    bool SetUseVertexColors(const std::string& stackId, bool enabled);
    bool SetCastShadows(const std::string& stackId, bool enabled);
    bool SetReceiveShadows(const std::string& stackId, bool enabled);
    bool SetTwoSided(const std::string& stackId, bool enabled);
    int GetStackCount() const { return static_cast<int>(m_stacks.size()); }
    const MaterialStack* GetStack(const std::string& stackId) const;
    std::vector<std::string> GetStackIds() const;

    // Layer management
    std::string AddLayer(const std::string& stackId, const std::string& name,
                          ShadingModel model = ShadingModel::PBR);
    bool RemoveLayer(const std::string& stackId, const std::string& layerId);
    bool MoveLayerUp(const std::string& stackId, const std::string& layerId);
    bool MoveLayerDown(const std::string& stackId, const std::string& layerId);
    bool SetLayerBlendOp(const std::string& stackId, const std::string& layerId,
                          BlendOperation op);
    bool SetLayerMaskType(const std::string& stackId, const std::string& layerId,
                           MaskType maskType);
    bool SetLayerOpacity(const std::string& stackId, const std::string& layerId,
                          float opacity);
    bool SetLayerRoughness(const std::string& stackId, const std::string& layerId,
                            float roughness);
    bool SetLayerMetallic(const std::string& stackId, const std::string& layerId,
                           float metallic);
    bool SetLayerEmissive(const std::string& stackId, const std::string& layerId,
                           float intensity);
    bool SetLayerVisible(const std::string& stackId, const std::string& layerId,
                          bool visible);
    int GetLayerCount(const std::string& stackId) const;
    const MaterialLayer* GetLayer(const std::string& stackId,
                                   const std::string& layerId) const;

    // Texture slots
    std::string AddTextureSlot(const std::string& stackId, const std::string& layerId,
                                 const std::string& slotName,
                                 const std::string& texturePath = "");
    bool SetTextureSlotPath(const std::string& stackId, const std::string& layerId,
                             const std::string& slotId,
                             const std::string& texturePath);
    bool SetTextureSlotTiling(const std::string& stackId, const std::string& layerId,
                               const std::string& slotId, float tx, float ty);
    int GetTextureSlotCount(const std::string& stackId, const std::string& layerId) const;

    // Persistence
    bool SaveStacks(const std::string& filePath) const;
    bool LoadStacks(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, MaterialStack> m_stacks;
    std::unordered_map<std::string, MaterialLayer> m_layers;
    int m_nextStackIndex{0};
    int m_nextLayerIndex{0};
    int m_nextSlotIndex{0};
};

} // namespace Atlas::Editor
