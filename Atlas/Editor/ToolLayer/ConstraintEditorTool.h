#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P8 Tool — Physics constraint editor for joints, hinges, and rigid body connections.
class ConstraintEditorTool : public ITool {
public:
    enum class ConstraintType { Fixed, Hinge, Slider, BallSocket, Cone, Universal, Spring };
    enum class ConstraintSpace { Local, World };
    enum class DriveMode { None, Position, Velocity };

    struct ConstraintLimit {
        float lower{-45.0f};
        float upper{45.0f};
        float softness{0.1f};
        float restitution{0.0f};
        bool enabled{true};
    };

    struct ConstraintDrive {
        DriveMode mode{DriveMode::None};
        float target{0.0f};
        float stiffness{100.0f};
        float damping{10.0f};
        float maxForce{1000.0f};
    };

    struct ConstraintDefinition {
        std::string constraintId;
        std::string name;
        ConstraintType type{ConstraintType::Hinge};
        std::string entityAId;
        std::string entityBId;
        ConstraintSpace space{ConstraintSpace::Local};
        float anchorAX{0.0f};
        float anchorAY{0.0f};
        float anchorAZ{0.0f};
        float anchorBX{0.0f};
        float anchorBY{0.0f};
        float anchorBZ{0.0f};
        float axisX{0.0f};
        float axisY{1.0f};
        float axisZ{0.0f};
        bool enabled{true};
        bool breakable{false};
        float breakForce{1e10f};
        float breakTorque{1e10f};
        ConstraintLimit angularLimit;
        ConstraintLimit linearLimit;
        ConstraintDrive angularDrive;
        ConstraintDrive linearDrive;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ConstraintEditorTool"; }
    bool IsActive() const override { return m_active; }

    // Constraint management
    std::string CreateConstraint(const std::string& name, ConstraintType type,
                                  const std::string& entityAId,
                                  const std::string& entityBId);
    bool RemoveConstraint(const std::string& constraintId);
    bool SetConstraintType(const std::string& constraintId, ConstraintType type);
    bool SetConstraintEntities(const std::string& constraintId,
                                const std::string& entityAId,
                                const std::string& entityBId);
    bool SetConstraintEnabled(const std::string& constraintId, bool enabled);
    bool SetConstraintBreakable(const std::string& constraintId,
                                 float breakForce, float breakTorque);
    bool IsConstraintBroken(const std::string& constraintId) const;
    int GetConstraintCount() const { return static_cast<int>(m_constraints.size()); }
    const ConstraintDefinition* GetConstraint(const std::string& constraintId) const;
    std::vector<std::string> GetConstraintIds() const;

    // Anchor / axis
    bool SetAnchorA(const std::string& constraintId, float x, float y, float z);
    bool SetAnchorB(const std::string& constraintId, float x, float y, float z);
    bool SetAxis(const std::string& constraintId, float ax, float ay, float az);
    bool SetConstraintSpace(const std::string& constraintId, ConstraintSpace space);

    // Limits
    bool SetAngularLimit(const std::string& constraintId, const ConstraintLimit& limit);
    bool SetLinearLimit(const std::string& constraintId, const ConstraintLimit& limit);

    // Drives
    bool SetAngularDrive(const std::string& constraintId, const ConstraintDrive& drive);
    bool SetLinearDrive(const std::string& constraintId, const ConstraintDrive& drive);

    // Queries
    std::vector<std::string> GetConstraintsForEntity(const std::string& entityId) const;
    int GetEnabledConstraintCount() const;

    // Persistence
    bool SaveConstraints(const std::string& filePath) const;
    bool LoadConstraints(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::vector<ConstraintDefinition> m_constraints;
    int m_nextConstraintIndex{0};
};

} // namespace Atlas::Editor
