#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P25 Tool — Rigid body joint authoring, constraint limits, and joint visualization.
class RigidBodyJointTool : public ITool {
public:
    enum class JointType { Fixed, Hinge, Slider, BallSocket, Cone, Custom };
    enum class ConstraintAxis { X, Y, Z, All, None, Custom };
    enum class JointLimitMode { Hard, Soft, Spring, Locked, Free, Custom };
    enum class JointVisualization { None, Axes, Limits, Forces, All, Custom };

    struct JointDef {
        std::string jointId;
        std::string jointName;
        JointType type{JointType::Hinge};
        std::string bodyAId;
        std::string bodyBId;
        float limitLow{0.0f};
        float limitHigh{0.0f};
        JointLimitMode limitMode{JointLimitMode::Hard};
    };

    struct JointConstraintData {
        std::string constraintId;
        std::string jointId;
        ConstraintAxis axis{ConstraintAxis::X};
        float stiffness{1.0f};
        float damping{0.1f};
        float breakForce{1000.0f};
        bool enabled{true};
    };

    struct JointVisualizationConfig {
        std::string visConfigId;
        std::string jointId;
        JointVisualization mode{JointVisualization::Axes};
        float scale{1.0f};
        bool showLabels{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "RigidBodyJointTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateJoint(const JointDef& joint);
    bool DeleteJoint(const std::string& jointId);
    const JointDef* GetJoint(const std::string& jointId) const;
    std::vector<std::string> GetAllJointIds() const;
    std::vector<std::string> GetJointsByType(JointType type) const;
    bool AddConstraint(const std::string& jointId, const JointConstraintData& constraint);
    bool RemoveConstraint(const std::string& jointId, const std::string& constraintId);
    const JointConstraintData* GetConstraint(const std::string& constraintId) const;
    std::vector<std::string> GetConstraintsByJoint(const std::string& jointId) const;
    bool SetVisualization(const JointVisualizationConfig& config);
    const JointVisualizationConfig* GetVisualization(const std::string& visConfigId) const;
    std::vector<std::string> GetVisualizationsByJoint(const std::string& jointId) const;
    bool BreakJoint(const std::string& jointId);
    bool ResetJoint(const std::string& jointId);
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, JointDef> m_joints;
    std::unordered_map<std::string, JointConstraintData> m_constraints;
    std::unordered_map<std::string, JointVisualizationConfig> m_visualizations;
};

} // namespace Atlas::Editor
