#pragma once
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Engine {

/// Phase 39D — Registry for quest body components managing quest state, objectives, and reward distribution.
class QuestBodyRegistry {
public:
    enum class QuestBodyState { Inactive, Active, InProgress, Completed, Failed, Abandoned, Locked, Custom };
    enum class QuestBodyScope { MainStory, SideQuest, DailyQuest, WeeklyQuest, HiddenQuest, FactionQuest, Custom };
    enum class ObjectiveTriggerType { OnEnter, OnInteract, OnKill, OnCollect, OnTimer, OnCondition, OnSignal, Custom };
    enum class RewardType { Experience, Currency, Item, Reputation, Unlock, Cosmetic, Custom };
    enum class QuestBodyFlags { None=0, Repeatable=1, Trackable=2, AutoAccept=4, AutoComplete=8, Hidden=16 };

    struct QuestObjectiveDef {
        std::string objectiveId;
        std::string questId;
        std::string description;
        ObjectiveTriggerType triggerType{ObjectiveTriggerType::OnCondition};
        std::string triggerExpr;
        int targetCount{1};
        int currentCount{0};
        bool completed{false};
        bool optional{false};
        std::vector<std::string> dependencyIds;
    };

    struct QuestRewardDef {
        std::string rewardId;
        std::string questId;
        RewardType rewardType{RewardType::Experience};
        std::string rewardAssetId;
        int quantity{1};
        bool distributed{false};
        std::string conditionExpr;
    };

    struct QuestBodyRecord {
        std::string questId;
        std::string name;
        QuestBodyScope scope{QuestBodyScope::SideQuest};
        QuestBodyState state{QuestBodyState::Inactive};
        std::string description;
        std::string giverNpcId;
        std::string startConditionExpr;
        std::string failConditionExpr;
        int playCount{0};
        std::vector<std::string> objectiveIds;
        std::vector<std::string> rewardIds;
        std::vector<int> flags;
    };

    // Quest CRUD
    bool RegisterQuest(const QuestBodyRecord& record);
    bool UnregisterQuest(const std::string& questId);
    bool SetQuestScope(const std::string& questId, QuestBodyScope scope);
    bool SetQuestState(const std::string& questId, QuestBodyState state);
    bool ActivateQuest(const std::string& questId);
    bool CompleteQuest(const std::string& questId);
    bool FailQuest(const std::string& questId);
    bool AbandonQuest(const std::string& questId);
    bool LockQuest(const std::string& questId);
    const QuestBodyRecord* GetQuestById(const std::string& questId) const;
    std::vector<std::string> GetAllQuestIds() const;
    std::vector<std::string> GetQuestsByScope(QuestBodyScope scope) const;
    std::vector<std::string> GetActiveQuests() const;
    std::vector<std::string> GetCompletedQuests() const;
    std::vector<std::string> GetFailedQuests() const;

    // Objective CRUD
    bool AddObjective(const std::string& questId, const QuestObjectiveDef& objective);
    bool RemoveObjective(const std::string& questId, const std::string& objectiveId);
    bool CompleteObjective(const std::string& objectiveId);
    bool IncrementObjective(const std::string& objectiveId, int delta);
    const QuestObjectiveDef* GetObjective(const std::string& objectiveId) const;
    std::vector<std::string> GetObjectivesByQuest(const std::string& questId) const;
    std::vector<std::string> GetCompletedObjectives(const std::string& questId) const;

    // Reward CRUD
    bool AddReward(const std::string& questId, const QuestRewardDef& reward);
    bool RemoveReward(const std::string& questId, const std::string& rewardId);
    bool DistributeReward(const std::string& rewardId);
    const QuestRewardDef* GetReward(const std::string& rewardId) const;
    std::vector<std::string> GetRewardsByQuest(const std::string& questId) const;
    std::vector<std::string> GetPendingRewards(const std::string& questId) const;

    void Clear();
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);

private:
    std::unordered_map<std::string, QuestBodyRecord> m_quests;
    std::unordered_map<std::string, QuestObjectiveDef> m_objectives;
    std::unordered_map<std::string, QuestRewardDef> m_rewards;
};

} // namespace Atlas::Engine
