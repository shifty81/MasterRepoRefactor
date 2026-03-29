#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P24 Tool — Animation curve editing, tangent management, and curve comparison overlays.
class AnimationCurveEditorTool : public ITool {
public:
    enum class CurveTangentMode { Auto, User, Break, Clamped, Linear, Constant, Custom };
    enum class CurveSelectionMode { Single, Multi, Range, All, Custom };
    enum class CurveCompareMode { None, Overlay, Diff, Mirror, Custom };
    enum class CurveExtrapolation { Cycle, Oscillate, Linear, Constant, Custom };

    struct AnimCurveKeyframe {
        std::string keyId;
        float time{0.0f};
        float value{0.0f};
        float arriveTangent{0.0f};
        float leaveTangent{0.0f};
        CurveTangentMode tangentMode{CurveTangentMode::Auto};
    };

    struct AnimCurveDef {
        std::string curveId;
        std::string curveName;
        std::string animationId;
        CurveExtrapolation extrapolation{CurveExtrapolation::Constant};
        std::vector<std::string> keyframeIds;
    };

    struct CurveCompareEntry {
        std::string compareId;
        std::string curveAId;
        std::string curveBId;
        CurveCompareMode mode{CurveCompareMode::Overlay};
        float timeOffset{0.0f};
        float scaleOffset{1.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AnimationCurveEditorTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateCurve(const AnimCurveDef& def);
    bool DeleteCurve(const std::string& curveId);
    const AnimCurveDef* GetCurve(const std::string& curveId) const;
    std::vector<std::string> GetAllCurveIds() const;
    std::vector<std::string> GetCurvesByAnimation(const std::string& animationId) const;
    bool AddKeyframe(const std::string& curveId, const AnimCurveKeyframe& keyframe);
    bool RemoveKeyframe(const std::string& curveId, const std::string& keyId);
    const AnimCurveKeyframe* GetKeyframe(const std::string& keyId) const;
    std::vector<std::string> GetKeyframesByCurve(const std::string& curveId) const;
    bool SetTangentMode(const std::string& keyId, CurveTangentMode mode);
    bool SetExtrapolation(const std::string& curveId, CurveExtrapolation extrapolation);
    std::string AddComparison(const CurveCompareEntry& entry);
    bool RemoveComparison(const std::string& compareId);
    const CurveCompareEntry* GetComparison(const std::string& compareId) const;
    std::vector<std::string> GetAllComparisonIds() const;
    std::vector<std::string> GetComparisonsByCurve(const std::string& curveId) const;
    bool FlattenTangents(const std::string& curveId);
    bool AutoFitCurve(const std::string& curveId);
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, AnimCurveDef> m_curves;
    std::unordered_map<std::string, AnimCurveKeyframe> m_keyframes;
    std::unordered_map<std::string, CurveCompareEntry> m_comparisons;
};

} // namespace Atlas::Editor
