#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P10 Tool — Authoring tool for configuring render pipeline passes and features.
class RenderPipelineTool : public ITool {
public:
    enum class PipelineType { Forward, Deferred, ForwardPlus, RayTraced };
    enum class PassType {
        GBuffer, Lighting, Shadow, Reflection, PostProcess,
        Transparency, UI, Debug, Custom
    };
    enum class AntiAliasingMode { None, FXAA, TAA, MSAA, DLSS, FSR };

    struct RenderFeature {
        std::string featureId;
        std::string name;
        bool enabled{true};
        float quality{1.0f};
        int priority{0};
    };

    struct RenderPass {
        std::string passId;
        std::string name;
        PassType type{PassType::GBuffer};
        bool enabled{true};
        int order{0};
        std::vector<RenderFeature> features;
        float resolutionScale{1.0f};
        std::string outputTarget;
    };

    struct PipelineConfig {
        std::string configId;
        std::string name;
        PipelineType type{PipelineType::Deferred};
        AntiAliasingMode aaMode{AntiAliasingMode::TAA};
        bool hdrEnabled{true};
        bool shadowsEnabled{true};
        bool reflectionsEnabled{true};
        bool ambientOcclusion{true};
        int shadowCascades{4};
        float shadowDistance{150.0f};
        std::vector<RenderPass> passes;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "RenderPipelineTool"; }
    bool IsActive() const override { return m_active; }

    // Pipeline management
    std::string CreatePipeline(const std::string& name, PipelineType type = PipelineType::Deferred);
    bool RemovePipeline(const std::string& configId);
    bool SetPipelineType(const std::string& configId, PipelineType type);
    bool SetAntiAliasing(const std::string& configId, AntiAliasingMode mode);
    bool SetHDREnabled(const std::string& configId, bool enabled);
    bool SetShadowsEnabled(const std::string& configId, bool enabled);
    bool SetShadowCascades(const std::string& configId, int cascades);
    bool SetShadowDistance(const std::string& configId, float distance);
    bool SetAmbientOcclusion(const std::string& configId, bool enabled);
    bool SetReflectionsEnabled(const std::string& configId, bool enabled);
    int GetPipelineCount() const { return static_cast<int>(m_configs.size()); }
    const PipelineConfig* GetPipeline(const std::string& configId) const;
    std::vector<std::string> GetPipelineIds() const;

    // Pass management
    std::string AddPass(const std::string& configId, const std::string& name, PassType type);
    bool RemovePass(const std::string& configId, const std::string& passId);
    bool SetPassEnabled(const std::string& configId, const std::string& passId, bool enabled);
    bool SetPassOrder(const std::string& configId, const std::string& passId, int order);
    bool SetPassResolutionScale(const std::string& configId, const std::string& passId, float scale);
    int GetPassCount(const std::string& configId) const;

    // Feature management
    std::string AddFeature(const std::string& configId, const std::string& passId,
                            const std::string& name, float quality = 1.0f);
    bool RemoveFeature(const std::string& configId, const std::string& passId,
                        const std::string& featureId);
    bool SetFeatureEnabled(const std::string& configId, const std::string& passId,
                            const std::string& featureId, bool enabled);
    bool SetFeatureQuality(const std::string& configId, const std::string& passId,
                            const std::string& featureId, float quality);
    int GetFeatureCount(const std::string& configId, const std::string& passId) const;

    // Persistence
    bool SaveConfig(const std::string& filePath) const;
    bool LoadConfig(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, PipelineConfig> m_configs;
    int m_nextConfigIndex{0};
    int m_nextPassIndex{0};
    int m_nextFeatureIndex{0};
};

} // namespace Atlas::Editor
