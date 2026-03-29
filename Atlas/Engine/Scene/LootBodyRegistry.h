#pragma once
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Engine {

/// Phase 42D — Registry for loot body components managing drop tables, loot rolls, and reward pools.
class LootBodyRegistry {
public:
    enum class LootRarity { Trash, Common, Uncommon, Rare, Epic, Legendary, Mythic, Custom };
    enum class DropCondition { Always, OnKill, OnChest, OnQuest, OnEvent, OnTimer, Custom };
    enum class RollMethod { Uniform, Weighted, Guaranteed, Exclusive, Cumulative, Custom };
    enum class LootPoolType { Item, Currency, Experience, Blueprint, Custom };

    struct LootEntryDef {
        std::string lootEntryId;
        std::string itemId;
        LootRarity rarity{LootRarity::Common};
        LootPoolType poolType{LootPoolType::Item};
        float dropWeight{1.0f};
        int minQuantity{1};
        int maxQuantity{1};
        float dropChance{1.0f};
        bool enabled{true};
    };

    struct LootTableDef {
        std::string lootTableId;
        std::string lootTableName;
        DropCondition dropCondition{DropCondition::Always};
        RollMethod rollMethod{RollMethod::Weighted};
        int maxRolls{1};
        int minRolls{1};
        float guaranteedChance{0.0f};
        bool enabled{true};
        std::vector<std::string> lootEntryIds;
    };

    struct LootBodyRecord {
        std::string lootBodyId;
        std::string ownerEntityId;
        std::string lootTableId;
        int level{1};
        float luckModifier{1.0f};
        bool exhausted{false};
        std::string displayName;
        std::vector<std::string> activePoolIds;
        std::vector<std::string> flags;
    };

    // Loot entry CRUD
    bool RegisterLootEntry(const LootEntryDef& entry);
    bool UnregisterLootEntry(const std::string& lootEntryId);
    bool UpdateLootEntryWeight(const std::string& lootEntryId, float weight);
    bool EnableLootEntry(const std::string& lootEntryId, bool enabled);
    const LootEntryDef* GetLootEntry(const std::string& lootEntryId) const;
    std::vector<std::string> GetAllLootEntryIds() const;
    std::vector<std::string> GetLootEntriesByRarity(LootRarity rarity) const;
    std::vector<std::string> GetLootEntriesByPool(LootPoolType poolType) const;
    std::vector<std::string> GetEnabledLootEntries() const;

    // Loot table CRUD
    bool RegisterLootTable(const LootTableDef& table);
    bool UnregisterLootTable(const std::string& lootTableId);
    bool EnableLootTable(const std::string& lootTableId, bool enabled);
    bool AddEntryToTable(const std::string& lootTableId, const std::string& lootEntryId);
    bool RemoveEntryFromTable(const std::string& lootTableId, const std::string& lootEntryId);
    bool SetDropCondition(const std::string& lootTableId, DropCondition condition);
    bool SetRollMethod(const std::string& lootTableId, RollMethod method);
    const LootTableDef* GetLootTable(const std::string& lootTableId) const;
    std::vector<std::string> GetAllLootTableIds() const;
    std::vector<std::string> GetLootTablesByCondition(DropCondition condition) const;
    std::vector<std::string> GetEnabledLootTables() const;

    // Loot body CRUD
    bool RegisterLootBody(const LootBodyRecord& record);
    bool UnregisterLootBody(const std::string& lootBodyId);
    bool ExhaustLootBody(const std::string& lootBodyId);
    bool ResetLootBody(const std::string& lootBodyId);
    bool SetLuckModifier(const std::string& lootBodyId, float modifier);
    const LootBodyRecord* GetLootBody(const std::string& lootBodyId) const;
    std::vector<std::string> GetAllLootBodyIds() const;
    std::vector<std::string> GetLootBodiesByOwner(const std::string& ownerEntityId) const;
    std::vector<std::string> GetExhaustedBodies() const;
    std::vector<std::string> GetActiveBodies() const;

    void Clear();
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);

private:
    std::unordered_map<std::string, LootEntryDef> m_lootEntries;
    std::unordered_map<std::string, LootTableDef> m_lootTables;
    std::unordered_map<std::string, LootBodyRecord> m_lootBodies;
};

} // namespace Atlas::Engine
