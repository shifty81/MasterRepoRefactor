#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P27 Tool — Lens flare asset authoring, flare element stacking, and screen-space config.
class LensFlareEditorTool : public ITool {
public:
    enum class FlareElementType { Glow, Ring, Streak, Bokeh, Starburst, Shimmer, Custom };
    enum class OcclusionMode { None, Trace, Volume, Custom };
    enum class BlendFunction { Additive, Screen, Multiply, Overlay, Custom };
    enum class FlareTrigger { Always, OnBright, OnSunAngle, OnCamera, Custom };

    struct FlareAssetDef {
        std::string flareId;
        std::string flareName;
        FlareTrigger trigger{FlareTrigger::Always};
        float intensityScale{1.0f};
        float sizeScale{1.0f};
        float distortionStrength{0.0f};
        bool enabled{true};
        bool autoRotate{false};
    };

    struct FlareElementDef {
        std::string elementId;
        std::string flareId;
        FlareElementType elementType{FlareElementType::Glow};
        BlendFunction blendFunction{BlendFunction::Additive};
        float offsetAlongAxis{0.0f};
        float scaleX{1.0f};
        float scaleY{1.0f};
        float rotation{0.0f};
        float r{1.0f};
        float g{1.0f};
        float b{1.0f};
        float a{1.0f};
        float intensity{1.0f};
        bool enabled{true};
    };

    struct FlareOcclusionDef {
        std::string occlusionId;
        std::string flareId;
        OcclusionMode mode{OcclusionMode::Trace};
        float fadeInTime{0.1f};
        float fadeOutTime{0.2f};
        float checkRadius{5.0f};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "LensFlareEditorTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateFlare(const FlareAssetDef& def);
    bool DeleteFlare(const std::string& flareId);
    bool EnableFlare(const std::string& flareId, bool enabled);
    const FlareAssetDef* GetFlare(const std::string& flareId) const;
    std::vector<std::string> GetAllFlareIds() const;
    std::vector<std::string> GetFlaresByTrigger(FlareTrigger trigger) const;
    std::vector<std::string> GetEnabledFlares() const;
    bool AddElement(const std::string& flareId, const FlareElementDef& element);
    bool RemoveElement(const std::string& flareId, const std::string& elementId);
    bool SetElementBlend(const std::string& elementId, BlendFunction blend);
    const FlareElementDef* GetElement(const std::string& elementId) const;
    std::vector<std::string> GetElementsByFlare(const std::string& flareId) const;
    std::vector<std::string> GetElementsByType(FlareElementType type) const;
    bool SetOcclusion(const std::string& flareId, const FlareOcclusionDef& occlusion);
    bool RemoveOcclusion(const std::string& flareId);
    const FlareOcclusionDef* GetOcclusion(const std::string& flareId) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, FlareAssetDef> m_flares;
    std::unordered_map<std::string, std::vector<FlareElementDef>> m_elements;
    std::unordered_map<std::string, FlareOcclusionDef> m_occlusions;
};

} // namespace Atlas::Editor
