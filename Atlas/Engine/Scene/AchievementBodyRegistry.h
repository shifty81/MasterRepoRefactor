#pragma once
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Engine {

/// Phase 40D — Registry for achievement body components managing unlock conditions, progress, and reward tiers.
class AchievementBodyRegistry {
public:
    enum class AchievementState { Locked, InProgress, Unlocked, Claimed, Hidden, Deprecated, Custom };
    enum class AchievementScope { Story, Combat, Exploration, Crafting, Social, Collection, Meta, Custom };
    enum class TriggerConditionType { OnKill, OnCollect, OnReach, OnCraft, OnSocial, OnComplete, OnTimer, Custom };
    enum class RewardTierType { Bronze, Silver, Gold, Platinum, Diamond, Custom };
    enum class AchievementFlags { None=0, Hidden=1, Repeatable=2, Progressive=4, Global=8, Secret=16 };

    struct AchievementProgressDef {
        std::string progressId;
        std::string achievementId;
        TriggerConditionType conditionType{TriggerConditionType::OnComplete};
        std::string conditionExpr;
        int targetValue{1};
        int currentValue{0};
        bool satisfied{false};
    };

    struct AchievementRewardDef {
        std::string rewardId;
        std::string achievementId;
        RewardTierType tier{RewardTierType::Bronze};
        std::string rewardAssetId;
        int xpValue{0};
        bool claimed{false};
        std::string claimConditionExpr;
    };

    struct AchievementBodyRecord {
        std::string achievementId;
        std::string name;
        AchievementScope scope{AchievementScope::Story};
        AchievementState state{AchievementState::Locked};
        std::string description;
        std::string iconAssetId;
        int displayOrder{0};
        int playCount{0};
        std::vector<std::string> progressIds;
        std::vector<std::string> rewardIds;
        std::vector<int> flags;
    };

    // Achievement CRUD
    bool RegisterAchievement(const AchievementBodyRecord& record);
    bool UnregisterAchievement(const std::string& achievementId);
    bool SetAchievementScope(const std::string& achievementId, AchievementScope scope);
    bool SetAchievementState(const std::string& achievementId, AchievementState state);
    bool UnlockAchievement(const std::string& achievementId);
    bool ClaimAchievement(const std::string& achievementId);
    bool HideAchievement(const std::string& achievementId);
    const AchievementBodyRecord* GetAchievementById(const std::string& achievementId) const;
    std::vector<std::string> GetAllAchievementIds() const;
    std::vector<std::string> GetAchievementsByScope(AchievementScope scope) const;
    std::vector<std::string> GetLockedAchievements() const;
    std::vector<std::string> GetUnlockedAchievements() const;
    std::vector<std::string> GetClaimedAchievements() const;
    std::vector<std::string> GetInProgressAchievements() const;

    // Progress CRUD
    bool AddProgress(const std::string& achievementId, const AchievementProgressDef& progress);
    bool RemoveProgress(const std::string& achievementId, const std::string& progressId);
    bool UpdateProgressValue(const std::string& progressId, int delta);
    bool SatisfyProgress(const std::string& progressId);
    const AchievementProgressDef* GetProgress(const std::string& progressId) const;
    std::vector<std::string> GetProgressByAchievement(const std::string& achievementId) const;
    std::vector<std::string> GetSatisfiedProgress(const std::string& achievementId) const;

    // Reward CRUD
    bool AddReward(const std::string& achievementId, const AchievementRewardDef& reward);
    bool RemoveReward(const std::string& achievementId, const std::string& rewardId);
    bool ClaimReward(const std::string& rewardId);
    const AchievementRewardDef* GetReward(const std::string& rewardId) const;
    std::vector<std::string> GetRewardsByAchievement(const std::string& achievementId) const;
    std::vector<std::string> GetUnclaimedRewards(const std::string& achievementId) const;
    std::vector<std::string> GetRewardsByTier(RewardTierType tier) const;

    void Clear();
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);

private:
    std::unordered_map<std::string, AchievementBodyRecord> m_achievements;
    std::unordered_map<std::string, AchievementProgressDef> m_progress;
    std::unordered_map<std::string, AchievementRewardDef> m_rewards;
};

} // namespace Atlas::Engine
