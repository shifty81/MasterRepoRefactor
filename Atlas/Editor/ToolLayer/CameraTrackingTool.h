#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P25 Tool — Camera tracking target management, follow curves, and tracking constraint authoring.
class CameraTrackingTool : public ITool {
public:
    enum class TrackingMode { LookAt, Follow, Orbit, Rail, Dolly, Custom };
    enum class TrackingConstraint { Position, Rotation, Scale, LookAt, Path, Custom };
    enum class CameraRailType { Linear, Bezier, Spline, Loop, Custom };
    enum class TrackingBlendMode { Immediate, Smooth, Spring, Lerp, Custom };

    struct TrackingTargetDef {
        std::string targetId;
        std::string targetName;
        std::string actorId;
        TrackingMode mode{TrackingMode::Follow};
        TrackingBlendMode blendMode{TrackingBlendMode::Smooth};
        float blendSpeed{5.0f};
        bool active{true};
    };

    struct CameraRailDef {
        std::string railId;
        std::string railName;
        CameraRailType railType{CameraRailType::Linear};
        std::vector<std::string> controlPointIds;
        float totalLength{0.0f};
        bool looping{false};
    };

    struct TrackingConstraintDef {
        std::string constraintId;
        std::string targetId;
        TrackingConstraint constraint{TrackingConstraint::Position};
        float weight{1.0f};
        float offset{0.0f};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "CameraTrackingTool"; }
    bool IsActive() const override { return m_active; }

    bool RegisterTarget(const TrackingTargetDef& target);
    bool UnregisterTarget(const std::string& targetId);
    const TrackingTargetDef* GetTarget(const std::string& targetId) const;
    std::vector<std::string> GetAllTargetIds() const;
    std::vector<std::string> GetTargetsByMode(TrackingMode mode) const;
    bool CreateRail(const CameraRailDef& rail);
    bool DeleteRail(const std::string& railId);
    const CameraRailDef* GetRail(const std::string& railId) const;
    std::vector<std::string> GetAllRailIds() const;
    bool AddConstraint(const TrackingConstraintDef& constraint);
    bool RemoveConstraint(const std::string& constraintId);
    const TrackingConstraintDef* GetConstraint(const std::string& constraintId) const;
    std::vector<std::string> GetConstraintsByTarget(const std::string& targetId) const;
    bool SetActiveTarget(const std::string& targetId);
    std::string GetActiveTarget() const;
    bool BlendToTarget(const std::string& targetId, float duration);
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, TrackingTargetDef> m_targets;
    std::unordered_map<std::string, CameraRailDef> m_rails;
    std::unordered_map<std::string, TrackingConstraintDef> m_constraints;
    std::string m_activeTargetId;
};

} // namespace Atlas::Editor
