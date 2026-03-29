#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 43C — Compositor for scene layer compositing, post-process stack ordering, and render pass management.
class SolarSystemCompositor {
public:
    enum class CompositeMode { Opaque, Translucent, Additive, Modulate, AlphaBlend, Custom };
    enum class RenderPassType { Depth, Color, Lighting, Shadow, Reflection, PostProcess, Custom };
    enum class LayerBlendOp { Over, Under, Add, Multiply, Screen, Mask, Custom };
    enum class CompositorState { Idle, Building, Compositing, Done, Error, Custom };

    struct CompositeLayerDef {
        std::string layerId;
        std::string layerName;
        std::string systemId;
        CompositeMode mode{CompositeMode::Opaque};
        LayerBlendOp blendOp{LayerBlendOp::Over};
        float opacity{1.0f};
        int sortOrder{0};
        bool castShadows{true};
        bool receiveShadows{true};
        bool enabled{true};
    };

    struct RenderPassDef {
        std::string passId;
        std::string passName;
        RenderPassType passType{RenderPassType::Color};
        std::string targetLayerId;
        int executionOrder{0};
        float scale{1.0f};
        bool isEnabled{true};
        bool asyncExecution{false};
    };

    struct PostProcessStackDef {
        std::string stackId;
        std::string stackName;
        std::string systemId;
        std::vector<std::string> effectIds;
        int priority{0};
        bool blendable{true};
        float blendWeight{1.0f};
        bool enabled{true};
    };

    // Composite layer management
    bool AddLayer(const CompositeLayerDef& layer);
    bool RemoveLayer(const std::string& layerId);
    bool EnableLayer(const std::string& layerId, bool enabled);
    bool SetLayerMode(const std::string& layerId, CompositeMode mode);
    bool SetLayerOrder(const std::string& layerId, int order);
    const CompositeLayerDef* GetLayer(const std::string& layerId) const;
    std::vector<std::string> GetAllLayerIds() const;
    std::vector<std::string> GetLayersByMode(CompositeMode mode) const;
    std::vector<std::string> GetLayersBySystem(const std::string& systemId) const;
    std::vector<std::string> GetEnabledLayers() const;
    std::vector<std::string> GetLayersSortedByOrder() const;

    // Render pass management
    bool AddRenderPass(const RenderPassDef& pass);
    bool RemoveRenderPass(const std::string& passId);
    bool EnableRenderPass(const std::string& passId, bool enabled);
    bool SetPassOrder(const std::string& passId, int order);
    const RenderPassDef* GetRenderPass(const std::string& passId) const;
    std::vector<std::string> GetAllPassIds() const;
    std::vector<std::string> GetPassesByType(RenderPassType type) const;
    std::vector<std::string> GetPassesByLayer(const std::string& layerId) const;
    std::vector<std::string> GetAsyncPasses() const;

    // Post-process stack management
    bool AddPostProcessStack(const PostProcessStackDef& stack);
    bool RemovePostProcessStack(const std::string& stackId);
    bool EnablePostProcessStack(const std::string& stackId, bool enabled);
    bool AddEffectToStack(const std::string& stackId, const std::string& effectId);
    bool RemoveEffectFromStack(const std::string& stackId, const std::string& effectId);
    const PostProcessStackDef* GetPostProcessStack(const std::string& stackId) const;
    std::vector<std::string> GetAllStackIds() const;
    std::vector<std::string> GetStacksBySystem(const std::string& systemId) const;
    std::vector<std::string> GetEnabledStacks() const;

    // Compositor state
    bool Composite(const std::string& systemId);
    void SetState(CompositorState state);
    CompositorState GetState() const { return m_state; }
    bool IsCompositing() const;

    void Reset();

private:
    std::unordered_map<std::string, CompositeLayerDef> m_layers;
    std::unordered_map<std::string, RenderPassDef> m_passes;
    std::unordered_map<std::string, PostProcessStackDef> m_stacks;
    CompositorState m_state{CompositorState::Idle};
};

} // namespace Atlas::Engine
