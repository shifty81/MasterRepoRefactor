#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P21 Tool — Ability system runtime debugging, attribute inspection, and cooldown visualization.
class AbilitySystemDebuggerTool : public ITool {
public:
    enum class AbilityDebugMode { Inactive, Snapshot, Live, Replay, Paused, FilteredLive, Custom };
    enum class AttributeDisplayMode { Raw, Normalized, Delta, History, Overlay, Custom };
    enum class CooldownVisualization { Bar, Radial, Numeric, Timeline, HeatMap, Custom };

    struct AbilityWatchEntry {
        std::string watchId;
        std::string abilityId;
        std::string abilityName;
        std::string ownerId;
        std::string activationState;
        float cooldownRemaining{0.0f};
        int stackCount{1};
        bool breakOnActivation{false};
        bool breakOnCooldown{false};
    };

    struct AttributeWatchEntry {
        std::string watchId;
        std::string ownerId;
        std::string attributeName;
        float baseValue{0.0f};
        float currentValue{0.0f};
        float minValue{0.0f};
        float maxValue{100.0f};
        bool highlightWhenChanged{true};
        bool logHistory{false};
    };

    struct CooldownTrackEntry {
        std::string trackId;
        std::string abilityId;
        std::string ownerId;
        float totalCooldown{0.0f};
        float remaining{0.0f};
        CooldownVisualization visMode{CooldownVisualization::Bar};
        bool showLabel{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AbilitySystemDebuggerTool"; }
    bool IsActive() const override { return m_active; }

    std::string AddAbilityWatch(const AbilityWatchEntry& entry);
    bool RemoveAbilityWatch(const std::string& watchId);
    const AbilityWatchEntry* GetAbilityWatch(const std::string& watchId) const;
    std::vector<std::string> GetAllAbilityWatchIds() const;

    std::string AddAttributeWatch(const AttributeWatchEntry& entry);
    bool RemoveAttributeWatch(const std::string& watchId);
    const AttributeWatchEntry* GetAttributeWatch(const std::string& watchId) const;
    std::vector<std::string> GetAttributeWatchesByOwner(const std::string& ownerId) const;

    std::string AddCooldownTrack(const CooldownTrackEntry& entry);
    bool RemoveCooldownTrack(const std::string& trackId);
    const CooldownTrackEntry* GetCooldownTrack(const std::string& trackId) const;
    std::vector<std::string> GetActiveCooldownTracks() const;

    bool SetDebugMode(AbilityDebugMode mode);
    AbilityDebugMode GetDebugMode() const { return m_mode; }
    bool SetAttributeDisplayMode(const std::string& watchId, AttributeDisplayMode mode);
    bool SetCooldownVisualization(const std::string& trackId, CooldownVisualization vis);
    bool SetBreakOnActivation(const std::string& watchId, bool enabled);
    bool SetBreakOnCooldown(const std::string& watchId, bool enabled);
    bool SetHighlightOnChange(const std::string& watchId, bool enabled);
    bool FilterByOwner(const std::string& ownerId);
    bool ClearOwnerFilter();
    std::vector<std::string> GetWatchesByOwner(const std::string& ownerId) const;
    int GetTotalWatchCount() const;
    bool ExportDebugSnapshot(const std::string& filePath) const;
    void Reset();

private:
    bool m_active{false};
    AbilityDebugMode m_mode{AbilityDebugMode::Inactive};
    std::unordered_map<std::string, AbilityWatchEntry> m_abilityWatches;
    std::unordered_map<std::string, AttributeWatchEntry> m_attributeWatches;
    std::unordered_map<std::string, CooldownTrackEntry> m_cooldownTracks;
    std::string m_ownerFilter;
    int m_nextWatchIndex{0};
};

} // namespace Atlas::Editor
