#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 26D — Registry for physics body definitions used by the simulation subsystem.
/// Manages rigidbody metadata, collider shapes, physics materials, and constraint
/// manifests for deterministic physics scene setup and serialisation.
class PhysicsBodyRegistry {
public:
    enum class BodyState { Inactive, Active, Sleeping, Destroyed };
    enum class BodyType { Static, Kinematic, Dynamic };
    enum class ColliderShape { Box, Sphere, Capsule, Cylinder, Mesh, ConvexHull };
    enum class PhysicsLayer {
        Default, Character, Vehicle, Projectile,
        Terrain, Trigger, Debris, Water, Custom
    };

    struct PhysicsMaterialDef {
        std::string materialId;
        std::string name;
        float staticFriction{0.6f};
        float dynamicFriction{0.4f};
        float restitution{0.1f};
        float density{1000.0f};
        bool isTrigger{false};
    };

    struct ColliderDef {
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
        std::string physicsMaterialId;
        bool isTrigger{false};
        bool enabled{true};
    };

    struct BodyRecord {
        std::string bodyId;
        std::string name;
        BodyType type{BodyType::Dynamic};
        BodyState state{BodyState::Inactive};
        PhysicsLayer layer{PhysicsLayer::Default};
        float mass{1.0f};
        float linearDrag{0.0f};
        float angularDrag{0.05f};
        float gravityScale{1.0f};
        bool useGravity{true};
        bool freezePosX{false};
        bool freezePosY{false};
        bool freezePosZ{false};
        bool freezeRotX{false};
        bool freezeRotY{false};
        bool freezeRotZ{false};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        std::vector<ColliderDef> colliders;
        std::string linkedEntityId;
        std::string sceneId;
        int priority{0};
        bool alwaysActive{false};
    };

    struct ConstraintManifest {
        std::string constraintId;
        std::string name;
        std::string bodyAId;
        std::string bodyBId;
        std::string constraintType;
        float limitMin{-90.0f};
        float limitMax{90.0f};
        float springStiffness{100.0f};
        float springDamping{10.0f};
        bool breakable{false};
        float breakForce{10000.0f};
        bool enabled{true};
    };

    // Body registration
    bool RegisterBody(const BodyRecord& record);
    bool UnregisterBody(const std::string& bodyId);
    bool UpdateBody(const std::string& bodyId, const BodyRecord& record);
    bool SetBodyState(const std::string& bodyId, BodyState state);
    bool SetBodyType(const std::string& bodyId, BodyType type);
    bool SetBodyLayer(const std::string& bodyId, PhysicsLayer layer);
    bool SetBodyMass(const std::string& bodyId, float mass);
    bool SetBodyGravity(const std::string& bodyId, float scale, bool useGravity = true);
    bool SetBodyScene(const std::string& bodyId, const std::string& sceneId);
    bool SetAlwaysActive(const std::string& bodyId, bool alwaysActive);
    bool LinkToEntity(const std::string& bodyId, const std::string& entityId);
    int GetRegisteredCount() const { return static_cast<int>(m_bodies.size()); }
    bool IsRegistered(const std::string& bodyId) const;
    const BodyRecord* GetBody(const std::string& bodyId) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByScene(const std::string& sceneId) const;
    std::vector<std::string> GetBodiesByType(BodyType type) const;
    std::vector<std::string> GetBodiesByLayer(PhysicsLayer layer) const;
    std::vector<std::string> GetActiveBodies() const;
    std::vector<std::string> GetAlwaysActiveBodies() const;

    // Collider management
    bool AddCollider(const std::string& bodyId, const ColliderDef& collider);
    bool RemoveCollider(const std::string& bodyId, const std::string& colliderId);
    bool SetColliderEnabled(const std::string& bodyId,
                              const std::string& colliderId, bool enabled);
    int GetColliderCount(const std::string& bodyId) const;

    // Physics materials
    bool RegisterMaterial(const PhysicsMaterialDef& material);
    bool UnregisterMaterial(const std::string& materialId);
    bool SetFriction(const std::string& materialId,
                      float staticFric, float dynamicFric);
    bool SetRestitution(const std::string& materialId, float restitution);
    int GetMaterialCount() const { return static_cast<int>(m_materials.size()); }
    const PhysicsMaterialDef* GetMaterial(const std::string& materialId) const;
    std::vector<std::string> GetMaterialIds() const;

    // Constraints
    bool RegisterConstraint(const ConstraintManifest& constraint);
    bool UnregisterConstraint(const std::string& constraintId);
    bool SetConstraintEnabled(const std::string& constraintId, bool enabled);
    int GetConstraintCount() const { return static_cast<int>(m_constraints.size()); }
    const ConstraintManifest* GetConstraint(const std::string& constraintId) const;
    std::vector<std::string> GetConstraintsForBody(const std::string& bodyId) const;

    // Activation
    bool ActivateBody(const std::string& bodyId);
    bool DeactivateBody(const std::string& bodyId);
    bool SleepBody(const std::string& bodyId);
    int GetActiveCount() const;
    int GetSleepingCount() const;
    void ActivateAllInScene(const std::string& sceneId);
    void DeactivateAllInScene(const std::string& sceneId);

    // Callbacks
    using StateChangedCallback = std::function<void(const std::string&, BodyState)>;
    void SetOnStateChangedCallback(StateChangedCallback cb);

    // Persistence
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);
    void Clear();

private:
    std::unordered_map<std::string, BodyRecord> m_bodies;
    std::unordered_map<std::string, PhysicsMaterialDef> m_materials;
    std::unordered_map<std::string, ConstraintManifest> m_constraints;
    StateChangedCallback m_onStateChanged;
};

} // namespace Atlas::Engine
