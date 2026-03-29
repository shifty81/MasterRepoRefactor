#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P26 Tool — Scene capture setup, render target management, and capture pipeline config.
class SceneCaptureTool : public ITool {
public:
    enum class CaptureType { Color, Depth, Normal, Emissive, Cubemap, Array, Custom };
    enum class CaptureResolution { R256, R512, R1024, R2048, R4096, Custom };
    enum class UpdateMode { RealTime, OnDemand, OnSceneChange, Manual, Custom };
    enum class CaptureBlendMode { Opaque, Translucent, Additive, Custom };

    struct SceneCaptureDef {
        std::string captureId;
        std::string captureName;
        CaptureType captureType{CaptureType::Color};
        CaptureResolution resolution{CaptureResolution::R1024};
        UpdateMode updateMode{UpdateMode::OnDemand};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float fovDegrees{90.0f};
        float nearClip{0.1f};
        float farClip{10000.0f};
        bool captureEveryFrame{false};
        bool enabled{true};
    };

    struct RenderTargetDef {
        std::string renderTargetId;
        std::string captureId;
        CaptureResolution width{CaptureResolution::R1024};
        CaptureResolution height{CaptureResolution::R1024};
        std::string formatHint;
        bool useMips{false};
        bool sRGB{true};
        CaptureBlendMode blendMode{CaptureBlendMode::Opaque};
    };

    struct CaptureFilterDef {
        std::string filterId;
        std::string captureId;
        std::string actorTag;
        bool inclusive{true};
        int layerMask{0xFFFFFFFF};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SceneCaptureTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateCapture(const SceneCaptureDef& def);
    bool DeleteCapture(const std::string& captureId);
    bool EnableCapture(const std::string& captureId, bool enabled);
    bool TriggerCapture(const std::string& captureId);
    bool SetUpdateMode(const std::string& captureId, UpdateMode mode);
    const SceneCaptureDef* GetCapture(const std::string& captureId) const;
    std::vector<std::string> GetAllCaptureIds() const;
    std::vector<std::string> GetCapturesByType(CaptureType type) const;
    std::vector<std::string> GetEnabledCaptures() const;
    bool CreateRenderTarget(const RenderTargetDef& def);
    bool DeleteRenderTarget(const std::string& renderTargetId);
    const RenderTargetDef* GetRenderTarget(const std::string& renderTargetId) const;
    std::vector<std::string> GetRenderTargetsByCapture(const std::string& captureId) const;
    bool AddCaptureFilter(const std::string& captureId, const CaptureFilterDef& filter);
    bool RemoveCaptureFilter(const std::string& captureId, const std::string& filterId);
    const CaptureFilterDef* GetCaptureFilter(const std::string& filterId) const;
    std::vector<std::string> GetFiltersByCapture(const std::string& captureId) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, SceneCaptureDef> m_captures;
    std::unordered_map<std::string, RenderTargetDef> m_renderTargets;
    std::unordered_map<std::string, std::vector<CaptureFilterDef>> m_filters;
};

} // namespace Atlas::Editor
