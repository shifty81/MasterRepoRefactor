#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P18 Tool — Smart object definition authoring, slot configuration, and behavior tag management.
class SmartObjectTool : public ITool {
public:
    enum class SmartObjectState { Available, Occupied, Disabled, Destroyed, Cooldown, Reserved };
    enum class SlotType { SingleActor, MultiActor, PlayerOnly, AIOnly, Interaction, Observation };
    enum class ClaimHandle { None, Actor, AI, Player, System, Persistent };

    struct SmartObjectSlot {
        std::string slotId;
        std::string name;
        SlotType slotType{SlotType::SingleActor};
        std::vector<float> offset;
        std::vector<float> rotation;
        int maxConcurrent{1};
        float cooldown{0.0f};
        ClaimHandle claimHandle{ClaimHandle::None};
    };

    struct SmartObjectDef {
        std::string objectId;
        std::string name;
        std::vector<std::string> slots;
        std::vector<std::string> behaviorTags;
        std::vector<float> worldLocation;
        std::vector<float> worldRotation;
        float radius{200.0f};
        bool autoEnable{true};
    };

    struct SmartObjectConfig {
        std::string configId;
        std::string objectId;
        bool enableFilter{false};
        bool disableOnOccupy{false};
        float respawnTime{0.0f};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "SmartObjectTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateSmartObject(const std::string& name);
    bool RemoveSmartObject(const std::string& objectId);
    std::string AddSlot(const std::string& objectId, const std::string& name, SlotType type);
    bool RemoveSlot(const std::string& objectId, const std::string& slotId);
    bool SetSlotType(const std::string& slotId, SlotType type);
    bool SetSlotClaim(const std::string& slotId, ClaimHandle handle);
    bool SetObjectState(const std::string& objectId, SmartObjectState state);
    bool SetBehaviorTags(const std::string& objectId, const std::vector<std::string>& tags);
    bool SetObjectRadius(const std::string& objectId, float radius);
    bool ClaimSlot(const std::string& slotId, ClaimHandle handle);
    bool ReleaseSlot(const std::string& slotId);
    bool EnableObject(const std::string& objectId);
    bool DisableObject(const std::string& objectId);
    const SmartObjectDef* GetSmartObject(const std::string& objectId) const;
    const SmartObjectSlot* GetSlot(const std::string& slotId) const;
    std::vector<std::string> GetAllObjectIds() const;
    std::vector<std::string> GetSlotsByObject(const std::string& objectId) const;
    std::vector<std::string> GetObjectsByState(SmartObjectState state) const;
    std::vector<std::string> GetAvailableObjects() const;
    std::vector<std::string> GetObjectsInRadius(float cx, float cy, float cz, float radius) const;
    bool ValidateSmartObject(const std::string& objectId) const;
    bool ExportSmartObjects(const std::string& filePath) const;
    bool SaveSmartObjects(const std::string& filePath) const;
    bool LoadSmartObjects(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, SmartObjectDef> m_objects;
    std::unordered_map<std::string, SmartObjectSlot> m_slots;
    std::unordered_map<std::string, SmartObjectState> m_states;
    int m_nextObjectIndex{0};
    int m_nextSlotIndex{0};
};

} // namespace Atlas::Editor
