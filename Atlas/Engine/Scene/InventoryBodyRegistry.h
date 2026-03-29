#pragma once
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Engine {

/// Phase 41D — Registry for inventory body components managing items, stacks, and container slots.
class InventoryBodyRegistry {
public:
    enum class ItemRarity { Common, Uncommon, Rare, Epic, Legendary, Unique, Custom };
    enum class ItemCategory { Weapon, Armor, Consumable, Material, Quest, Misc, Currency, Custom };
    enum class SlotType { Head, Chest, Legs, Hands, Feet, Weapon, OffHand, Ring, Neck, Bag, Custom };
    enum class InventoryState { Active, Locked, Overweight, Empty, Full, Custom };
    enum class StackPolicy { NoStack, Stack, StackCapped, Custom };

    struct ItemDef {
        std::string itemId;
        std::string itemName;
        ItemRarity rarity{ItemRarity::Common};
        ItemCategory category{ItemCategory::Misc};
        StackPolicy stackPolicy{StackPolicy::NoStack};
        int maxStack{1};
        float weight{1.0f};
        int value{0};
        std::string iconAssetId;
        bool tradeable{true};
        bool destroyable{true};
    };

    struct InventorySlotDef {
        std::string slotId;
        std::string containerId;
        SlotType slotType{SlotType::Bag};
        std::string itemId;
        int quantity{0};
        int slotIndex{0};
        bool locked{false};
    };

    struct InventoryBodyRecord {
        std::string containerId;
        std::string ownerEntityId;
        InventoryState state{InventoryState::Active};
        int maxSlots{20};
        float maxWeight{100.0f};
        float currentWeight{0.0f};
        std::string displayName;
        std::vector<std::string> slotIds;
        std::vector<std::string> flags;
    };

    // Item CRUD
    bool RegisterItem(const ItemDef& item);
    bool UnregisterItem(const std::string& itemId);
    bool UpdateItemRarity(const std::string& itemId, ItemRarity rarity);
    bool UpdateItemValue(const std::string& itemId, int value);
    const ItemDef* GetItem(const std::string& itemId) const;
    std::vector<std::string> GetAllItemIds() const;
    std::vector<std::string> GetItemsByRarity(ItemRarity rarity) const;
    std::vector<std::string> GetItemsByCategory(ItemCategory category) const;
    std::vector<std::string> GetTradeableItems() const;
    std::vector<std::string> GetStackableItems() const;

    // Container CRUD
    bool RegisterContainer(const InventoryBodyRecord& record);
    bool UnregisterContainer(const std::string& containerId);
    bool SetContainerState(const std::string& containerId, InventoryState state);
    bool LockContainer(const std::string& containerId);
    bool UnlockContainer(const std::string& containerId);
    const InventoryBodyRecord* GetContainer(const std::string& containerId) const;
    std::vector<std::string> GetAllContainerIds() const;
    std::vector<std::string> GetContainersByOwner(const std::string& ownerEntityId) const;
    std::vector<std::string> GetContainersByState(InventoryState state) const;
    std::vector<std::string> GetFullContainers() const;
    std::vector<std::string> GetEmptyContainers() const;

    // Slot CRUD
    bool AddSlot(const std::string& containerId, const InventorySlotDef& slot);
    bool RemoveSlot(const std::string& containerId, const std::string& slotId);
    bool SetSlotItem(const std::string& slotId, const std::string& itemId, int quantity);
    bool ClearSlot(const std::string& slotId);
    bool LockSlot(const std::string& slotId, bool locked);
    bool MoveItem(const std::string& srcSlotId, const std::string& dstSlotId);
    const InventorySlotDef* GetSlot(const std::string& slotId) const;
    std::vector<std::string> GetSlotsByContainer(const std::string& containerId) const;
    std::vector<std::string> GetSlotsByType(SlotType slotType) const;
    std::vector<std::string> GetOccupiedSlots(const std::string& containerId) const;
    std::vector<std::string> GetFreeSlots(const std::string& containerId) const;
    std::vector<std::string> GetLockedSlots(const std::string& containerId) const;

    void Clear();
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);

private:
    std::unordered_map<std::string, ItemDef> m_items;
    std::unordered_map<std::string, InventoryBodyRecord> m_containers;
    std::unordered_map<std::string, InventorySlotDef> m_slots;
};

} // namespace Atlas::Engine
