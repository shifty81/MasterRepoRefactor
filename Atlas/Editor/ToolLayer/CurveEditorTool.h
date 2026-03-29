#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P13 Tool — Animation curve editing with keyframes, tangent handles, and spline interpolation.
class CurveEditorTool : public ITool {
public:
    enum class InterpolationType { Constant, Linear, Bezier, Hermite, CatmullRom };
    enum class TangentMode { Auto, Free, Linear, Flat, Broken, ClampedAuto };
    enum class CurveWrapMode { Once, Loop, PingPong, ClampForever };
    enum class CurveDataType { Float, Vector2, Vector3, Color, Quaternion };

    struct Keyframe {
        std::string keyId;
        float time{0.0f};
        float value{0.0f};
        float inTangentX{0.0f};
        float inTangentY{0.0f};
        float outTangentX{0.0f};
        float outTangentY{0.0f};
        InterpolationType interpolation{InterpolationType::Bezier};
        TangentMode tangentMode{TangentMode::Auto};
        bool selected{false};
    };

    struct CurveTrack {
        std::string trackId;
        std::string name;
        CurveDataType dataType{CurveDataType::Float};
        std::string targetProperty;
        std::string targetObjectId;
        float defaultValue{0.0f};
        float minValue{-1e9f};
        float maxValue{1e9f};
        bool clamped{false};
        bool visible{true};
        bool locked{false};
        float displayColorR{1.0f};
        float displayColorG{1.0f};
        float displayColorB{1.0f};
    };

    struct CurveCursorState {
        float currentTime{0.0f};
        float viewStartTime{0.0f};
        float viewEndTime{10.0f};
        float viewMinValue{-1.0f};
        float viewMaxValue{1.0f};
        float timeZoom{1.0f};
        float valueZoom{1.0f};
        bool snapToFrames{true};
        float framesPerSecond{30.0f};
    };

    struct AnimCurveRecord {
        std::string curveId;
        std::string name;
        CurveWrapMode preWrapMode{CurveWrapMode::Once};
        CurveWrapMode postWrapMode{CurveWrapMode::Once};
        std::vector<CurveTrack> tracks;
        std::unordered_map<std::string, std::vector<Keyframe>> keyframes; // trackId -> keyframes
        float duration{10.0f};
        bool enabled{true};
        std::string linkedAnimationId;
        std::string linkedEntityId;
        std::string linkedSceneId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "CurveEditorTool"; }
    bool IsActive() const override { return m_active; }

    // Curve management
    std::string CreateCurve(const std::string& name);
    bool RemoveCurve(const std::string& curveId);
    bool SetWrapMode(const std::string& curveId, CurveWrapMode pre, CurveWrapMode post);
    bool SetCurveDuration(const std::string& curveId, float duration);
    bool SetCurveEnabled(const std::string& curveId, bool enabled);
    bool LinkToAnimation(const std::string& curveId, const std::string& animId);
    bool LinkToEntity(const std::string& curveId, const std::string& entityId);

    // Track management
    std::string AddTrack(const std::string& curveId, const std::string& name,
                          CurveDataType dataType = CurveDataType::Float);
    bool RemoveTrack(const std::string& curveId, const std::string& trackId);
    bool SetTrackProperty(const std::string& curveId, const std::string& trackId,
                           const std::string& property);
    bool SetTrackTargetObject(const std::string& curveId, const std::string& trackId,
                               const std::string& objectId);
    bool SetTrackVisible(const std::string& curveId, const std::string& trackId, bool visible);
    bool SetTrackLocked(const std::string& curveId, const std::string& trackId, bool locked);
    bool SetTrackColor(const std::string& curveId, const std::string& trackId,
                        float r, float g, float b);
    bool SetValueClamp(const std::string& curveId, const std::string& trackId,
                        float minVal, float maxVal);

    // Keyframe management
    std::string AddKeyframe(const std::string& curveId, const std::string& trackId,
                             float time, float value,
                             InterpolationType interp = InterpolationType::Bezier);
    bool RemoveKeyframe(const std::string& curveId, const std::string& trackId,
                         const std::string& keyId);
    bool MoveKeyframe(const std::string& curveId, const std::string& trackId,
                       const std::string& keyId, float newTime, float newValue);
    bool SetKeyframeTangents(const std::string& curveId, const std::string& trackId,
                              const std::string& keyId,
                              float inX, float inY, float outX, float outY);
    bool SetKeyframeTangentMode(const std::string& curveId, const std::string& trackId,
                                 const std::string& keyId, TangentMode mode);
    bool SetKeyframeInterpolation(const std::string& curveId, const std::string& trackId,
                                   const std::string& keyId, InterpolationType interp);
    bool SelectKeyframe(const std::string& curveId, const std::string& trackId,
                         const std::string& keyId, bool selected);

    // Evaluation
    float EvaluateCurve(const std::string& curveId, const std::string& trackId, float time) const;
    std::vector<float> SampleCurve(const std::string& curveId, const std::string& trackId,
                                    float startTime, float endTime, int samples) const;

    // View state
    void SetCursorTime(float time);
    float GetCursorTime() const { return m_cursor.currentTime; }
    void SetViewRange(float startTime, float endTime, float minValue, float maxValue);
    void SetSnapToFrames(bool enabled, float fps = 30.0f);
    void ZoomToFit(const std::string& curveId);

    // Queries
    int GetCurveCount() const { return static_cast<int>(m_curves.size()); }
    const AnimCurveRecord* GetCurve(const std::string& curveId) const;
    std::vector<std::string> GetCurveIds() const;
    int GetTrackCount(const std::string& curveId) const;
    int GetKeyframeCount(const std::string& curveId, const std::string& trackId) const;
    std::vector<std::string> GetSelectedKeyframeIds(const std::string& curveId,
                                                      const std::string& trackId) const;

    // Persistence
    bool SaveCurves(const std::string& filePath) const;
    bool LoadCurves(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, AnimCurveRecord> m_curves;
    CurveCursorState m_cursor;
    int m_nextCurveIndex{0};
    int m_nextTrackIndex{0};
    int m_nextKeyIndex{0};
};

} // namespace Atlas::Editor
