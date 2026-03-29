#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P23 Tool — Curve linear color editing, keyframe management, and gradient baking.
class CurveLinearColorTool : public ITool {
public:
    enum class CurveInterpolation { Linear, Cubic, Constant, Ease, Step, Custom };
    enum class ColorChannel { Red, Green, Blue, Alpha, All, Custom };
    enum class GradientBakeMode { Linear, Perceptual, Gamma, Custom };
    enum class KeyframeSnapMode { None, Grid, Frame, BeatSync, Custom };

    struct ColorKeyframeDef {
        std::string keyframeId;
        float time{0.0f};
        float r{1.0f};
        float g{1.0f};
        float b{1.0f};
        float a{1.0f};
    };

    struct CurveLinearColorDef {
        std::string curveId;
        std::string curveName;
        CurveInterpolation interp{CurveInterpolation::Linear};
        std::vector<std::string> keyframeIds;
    };

    struct GradientBakeResult {
        std::string bakeId;
        std::string curveId;
        int resolution{256};
        bool success{false};
        std::string outputPath;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "CurveLinearColorTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateCurve(const CurveLinearColorDef& def);
    bool DeleteCurve(const std::string& curveId);
    const CurveLinearColorDef* GetCurve(const std::string& curveId) const;
    std::vector<std::string> GetAllCurveIds() const;
    bool AddKeyframe(const std::string& curveId, const ColorKeyframeDef& kf);
    bool RemoveKeyframe(const std::string& curveId, const std::string& keyframeId);
    const ColorKeyframeDef* GetKeyframe(const std::string& keyframeId) const;
    std::vector<std::string> GetKeyframesForCurve(const std::string& curveId) const;
    bool SetInterpolation(const std::string& curveId, CurveInterpolation interp);
    bool SetChannel(const std::string& curveId, ColorChannel channel);
    std::string BakeGradient(const std::string& curveId, int resolution, GradientBakeMode mode);
    const GradientBakeResult* GetBakeResult(const std::string& bakeId) const;
    std::vector<std::string> GetBakesByResolution(int resolution) const;
    bool ResetCurve(const std::string& curveId);
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, CurveLinearColorDef> m_curves;
    std::unordered_map<std::string, ColorKeyframeDef> m_keyframes;
    std::unordered_map<std::string, GradientBakeResult> m_bakes;
    int m_nextCurveIndex{0};
};

} // namespace Atlas::Editor
