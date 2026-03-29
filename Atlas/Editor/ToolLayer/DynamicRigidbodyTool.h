#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P11 Tool — Dynamic rigidbody authoring and physics constraint editor.
class DynamicRigidbodyTool : public ITool {
public:
    enum class BodyType { Static, Kinematic, Dynamic };
    enum class ColliderShape { Box, Sphere, Capsule, Cylinder, Mesh, ConvexHull, Compound };
    enum class ConstraintType { Fixed, Hinge, Slider, BallSocket, Cone, Spring, Distance };
    enum class InterpolationMode { None, Interpolate, Extrapolate };

    struct PhysicsMaterial {
        std::string materialId;
        std::string name;
        float staticFriction{0.6f};
        float dynamicFriction{0.4f};
        float restitution{0.1f};
        float density{1000.0f};
    };

    struct ColliderConfig {
        std::string colliderId;
        ColliderShape shape{ColliderShape::Box};
        float extentX{0.5f};
        float extentY{0.5f};
        float extentZ{0.5f};
        float radius{0.5f};
        float height{2.0f};
        float offsetX{0.0f};
        float offsetY{0.0f};
        float offsetZ{0.0f};
        bool isTrigger{false};
        std::string physicsMaterialId;
    };

    struct ConstraintConfig {
        std::string constraintId;
        std::string name;
        ConstraintType type{ConstraintType::Fixed};
        std::string bodyAId;
        std::string bodyBId;
        float anchorAX{0.0f};
        float anchorAY{0.0f};
        float anchorAZ{0.0f};
        float anchorBX{0.0f};
        float anchorBY{0.0f};
        float anchorBZ{0.0f};
        float limitMin{-90.0f};
        float limitMax{90.0f};
        float springStiffness{100.0f};
        float springDamping{10.0f};
        bool breakable{false};
        float breakForce{10000.0f};
        bool enabled{true};
    };

    struct RigidbodyRecord {
        std::string bodyId;
        std::string name;
        BodyType bodyType{BodyType::Dynamic};
        InterpolationMode interpolation{InterpolationMode::Interpolate};
        float mass{1.0f};
        float linearDrag{0.0f};
        float angularDrag{0.05f};
        float gravityScale{1.0f};
        bool useGravity{true};
        bool isKinematic{false};
        bool freezePositionX{false};
        bool freezePositionY{false};
        bool freezePositionZ{false};
        bool freezeRotationX{false};
        bool freezeRotationY{false};
        bool freezeRotationZ{false};
        std::vector<ColliderConfig> colliders;
        int layer{0};
        std::string linkedEntityId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "DynamicRigidbodyTool"; }
    bool IsActive() const override { return m_active; }

    // Body management
    std::string CreateBody(const std::string& name, BodyType type = BodyType::Dynamic);
    bool RemoveBody(const std::string& bodyId);
    bool SetBodyType(const std::string& bodyId, BodyType type);
    bool SetMass(const std::string& bodyId, float mass);
    bool SetLinearDrag(const std::string& bodyId, float drag);
    bool SetAngularDrag(const std::string& bodyId, float drag);
    bool SetGravityScale(const std::string& bodyId, float scale);
    bool SetUseGravity(const std::string& bodyId, bool useGravity);
    bool SetInterpolation(const std::string& bodyId, InterpolationMode mode);
    bool SetFreezePosition(const std::string& bodyId, bool x, bool y, bool z);
    bool SetFreezeRotation(const std::string& bodyId, bool x, bool y, bool z);
    bool LinkToEntity(const std::string& bodyId, const std::string& entityId);
    int GetBodyCount() const { return static_cast<int>(m_bodies.size()); }
    const RigidbodyRecord* GetBody(const std::string& bodyId) const;
    std::vector<std::string> GetBodyIds() const;
    std::vector<std::string> GetBodiesByType(BodyType type) const;

    // Collider management
    std::string AddCollider(const std::string& bodyId, ColliderShape shape);
    bool RemoveCollider(const std::string& bodyId, const std::string& colliderId);
    bool SetColliderShape(const std::string& bodyId, const std::string& colliderId,
                           ColliderShape shape);
    bool SetColliderExtents(const std::string& bodyId, const std::string& colliderId,
                             float ex, float ey, float ez);
    bool SetColliderOffset(const std::string& bodyId, const std::string& colliderId,
                            float ox, float oy, float oz);
    bool SetColliderTrigger(const std::string& bodyId, const std::string& colliderId,
                             bool isTrigger);
    bool SetColliderMaterial(const std::string& bodyId, const std::string& colliderId,
                              const std::string& matId);
    int GetColliderCount(const std::string& bodyId) const;

    // Physics materials
    std::string CreatePhysicsMaterial(const std::string& name,
                                        float staticFriction = 0.6f,
                                        float dynamicFriction = 0.4f,
                                        float restitution = 0.1f);
    bool RemovePhysicsMaterial(const std::string& materialId);
    bool SetFriction(const std::string& materialId,
                      float staticFric, float dynamicFric);
    bool SetRestitution(const std::string& materialId, float restitution);
    int GetPhysicsMaterialCount() const { return static_cast<int>(m_materials.size()); }
    const PhysicsMaterial* GetPhysicsMaterial(const std::string& materialId) const;

    // Constraints
    std::string AddConstraint(const std::string& name, ConstraintType type,
                                const std::string& bodyAId,
                                const std::string& bodyBId);
    bool RemoveConstraint(const std::string& constraintId);
    bool SetConstraintLimits(const std::string& constraintId, float min, float max);
    bool SetConstraintSpring(const std::string& constraintId,
                               float stiffness, float damping);
    bool SetConstraintBreakable(const std::string& constraintId,
                                  bool breakable, float breakForce = 10000.0f);
    bool SetConstraintEnabled(const std::string& constraintId, bool enabled);
    int GetConstraintCount() const { return static_cast<int>(m_constraints.size()); }
    const ConstraintConfig* GetConstraint(const std::string& constraintId) const;

    // Persistence
    bool SaveBodies(const std::string& filePath) const;
    bool LoadBodies(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, RigidbodyRecord> m_bodies;
    std::unordered_map<std::string, PhysicsMaterial> m_materials;
    std::unordered_map<std::string, ConstraintConfig> m_constraints;
    int m_nextBodyIndex{0};
    int m_nextColliderIndex{0};
    int m_nextMaterialIndex{0};
    int m_nextConstraintIndex{0};
};

} // namespace Atlas::Editor
