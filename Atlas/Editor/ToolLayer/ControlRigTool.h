#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P17 Tool — Control rig graph authoring, control configuration, and IK/FK constraint management.
class ControlRigTool : public ITool {
public:
    enum class ControlType { Transform, Rotation, Translation, Scale, Float, Bool, Integer, Vector, EulerRotation };
    enum class RigConstraint { Point, Orient, AimAt, Parent, Scale, SixDOF, Spline, IK, FK };
    enum class RigSolverMode { Forward, Inverse, Hybrid, Expression };

    struct RigControl {
        std::string controlId;
        std::string name;
        ControlType controlType{ControlType::Transform};
        std::vector<float> offsetTransform;
        std::vector<float> initialValue;
        std::string shape;
        std::vector<float> color;
        float gizmoSize{1.0f};
    };

    struct RigConstraintDef {
        std::string constraintId;
        std::string name;
        RigConstraint rigConstraint{RigConstraint::Parent};
        std::string driverControlId;
        std::string drivenBoneId;
        float weight{1.0f};
        bool maintainOffset{true};
    };

    struct ControlRigDef {
        std::string rigId;
        std::string name;
        std::string skeletonPath;
        std::vector<std::string> controls;
        std::vector<std::string> constraints;
        RigSolverMode solverMode{RigSolverMode::Inverse};
        bool autoSolve{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ControlRigTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateRig(const std::string& name, const std::string& skeletonPath);
    bool RemoveRig(const std::string& rigId);
    std::string AddControl(const std::string& rigId, const std::string& name, ControlType type);
    bool RemoveControl(const std::string& rigId, const std::string& controlId);
    std::string AddConstraint(const std::string& rigId, RigConstraint constraint, const std::string& driverControlId, const std::string& drivenBoneId);
    bool RemoveConstraint(const std::string& rigId, const std::string& constraintId);
    bool SetControlType(const std::string& controlId, ControlType type);
    bool SetConstraintWeight(const std::string& constraintId, float weight);
    bool SetSolverMode(const std::string& rigId, RigSolverMode mode);
    bool SolveRig(const std::string& rigId);
    bool ResetRig(const std::string& rigId);
    bool PreviewRig(const std::string& rigId);
    const ControlRigDef* GetRig(const std::string& rigId) const;
    const RigControl* GetControl(const std::string& controlId) const;
    const RigConstraintDef* GetConstraint(const std::string& constraintId) const;
    std::vector<std::string> GetAllRigIds() const;
    std::vector<std::string> GetControlsByRig(const std::string& rigId) const;
    std::vector<std::string> GetConstraintsByRig(const std::string& rigId) const;
    bool ValidateRig(const std::string& rigId) const;
    bool ExportRig(const std::string& rigId, const std::string& filePath) const;
    bool SaveControlRig(const std::string& filePath) const;
    bool LoadControlRig(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, ControlRigDef> m_rigs;
    std::unordered_map<std::string, RigControl> m_controls;
    std::unordered_map<std::string, RigConstraintDef> m_constraints;
    int m_nextRigIndex{0};
    int m_nextControlIndex{0};
};

} // namespace Atlas::Editor
