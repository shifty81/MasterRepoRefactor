#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P13 Tool — Scene layer compositing, blend modes, and render target management.
class SceneCompositorTool : public ITool {
public:
    enum class BlendMode { Normal, Additive, Multiply, Screen, Overlay, Darken, Lighten };
    enum class RenderTargetFormat { RGBA8, RGBA16F, RGBA32F, R11G11B10F, Depth24Stencil8 };
    enum class CompositeOrder { Background, Midground, Foreground, UI, Debug };
    enum class SamplerFilter { Point, Linear, Anisotropic };

    struct RenderTargetDesc {
        std::string targetId;
        std::string name;
        RenderTargetFormat format{RenderTargetFormat::RGBA16F};
        int width{1920};
        int height{1080};
        bool autoResize{true};
        float resolutionScale{1.0f};
        bool useMSAA{false};
        int msaaSamples{4};
    };

    struct LayerBlendSettings {
        BlendMode blendMode{BlendMode::Normal};
        float opacity{1.0f};
        float colorMultR{1.0f};
        float colorMultG{1.0f};
        float colorMultB{1.0f};
        bool premultipliedAlpha{false};
    };

    struct CompositePassSettings {
        std::string passId;
        std::string shaderPath;
        SamplerFilter filter{SamplerFilter::Linear};
        bool clearBeforeRender{false};
        float clearColorR{0.0f};
        float clearColorG{0.0f};
        float clearColorB{0.0f};
        float clearColorA{0.0f};
    };

    struct CompositeLayer {
        std::string layerId;
        std::string name;
        CompositeOrder order{CompositeOrder::Midground};
        BlendMode blendMode{BlendMode::Normal};
        RenderTargetDesc renderTarget;
        LayerBlendSettings blendSettings;
        CompositePassSettings passSettings;
        std::string sourceRenderTargetId;
        std::string outputRenderTargetId;
        float zDepth{0.0f};
        bool visible{true};
        bool locked{false};
        bool enabled{true};
        std::string linkedCameraId;
        std::string linkedEntityGroupId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SceneCompositorTool"; }
    bool IsActive() const override { return m_active; }

    // Layer management
    std::string CreateLayer(const std::string& name, CompositeOrder order = CompositeOrder::Midground);
    bool RemoveLayer(const std::string& layerId);
    bool SetBlendMode(const std::string& layerId, BlendMode mode);
    bool SetOpacity(const std::string& layerId, float opacity);
    bool SetLayerOrder(const std::string& layerId, CompositeOrder order);
    bool SetLayerVisible(const std::string& layerId, bool visible);
    bool SetLayerLocked(const std::string& layerId, bool locked);
    bool SetLayerEnabled(const std::string& layerId, bool enabled);
    bool SetZDepth(const std::string& layerId, float depth);
    bool LinkCamera(const std::string& layerId, const std::string& cameraId);
    bool LinkEntityGroup(const std::string& layerId, const std::string& groupId);
    bool SetRenderTarget(const std::string& layerId, const RenderTargetDesc& desc);
    bool SetSourceTarget(const std::string& layerId, const std::string& sourceTargetId);
    bool SetOutputTarget(const std::string& layerId, const std::string& outputTargetId);
    bool SetPassSettings(const std::string& layerId, const CompositePassSettings& pass);

    // Render target management
    std::string CreateRenderTarget(const std::string& name, RenderTargetFormat format,
                                    int width, int height);
    bool RemoveRenderTarget(const std::string& targetId);
    const RenderTargetDesc* GetRenderTarget(const std::string& targetId) const;
    std::vector<std::string> GetRenderTargetIds() const;

    // Queries
    int GetLayerCount() const { return static_cast<int>(m_layers.size()); }
    const CompositeLayer* GetLayer(const std::string& layerId) const;
    std::vector<std::string> GetLayerIds() const;
    std::vector<std::string> GetLayersByOrder(CompositeOrder order) const;
    std::vector<std::string> GetVisibleLayerIds() const;

    // Compositing
    void FlattenLayers();
    bool MergeLayers(const std::string& bottomLayerId, const std::string& topLayerId);
    bool ReorderLayer(const std::string& layerId, int newIndex);
    void ResetAllBlendModes();

    // Persistence
    bool SaveComposite(const std::string& filePath) const;
    bool LoadComposite(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, CompositeLayer> m_layers;
    std::unordered_map<std::string, RenderTargetDesc> m_renderTargets;
    int m_nextLayerIndex{0};
    int m_nextTargetIndex{0};
};

} // namespace Atlas::Editor
