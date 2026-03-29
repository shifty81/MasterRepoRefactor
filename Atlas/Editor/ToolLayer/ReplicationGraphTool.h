#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P20 Tool — Replication graph node configuration, actor channel setup, and bandwidth budget management.
class ReplicationGraphTool : public ITool {
public:
    enum class RepNodeType { AlwaysRelevant, GridCell, DormancyNode, Spatialized, TeamsOnly, ConnectionBased, Custom };
    enum class ChannelPriority { Critical, High, Medium, Low, Background, Custom };
    enum class BandwidthBucket { Unlimited, High, Medium, Low, VeryLow, Custom };

    struct RepNodeConfig {
        std::string nodeId;
        std::string name;
        RepNodeType nodeType{RepNodeType::GridCell};
        float cellSize{10000.0f};
        float connectionBias{1.0f};
        bool spatialEnabled{true};
        std::vector<std::string> actorClasses;
    };

    struct ActorChannelDef {
        std::string channelId;
        std::string actorClass;
        ChannelPriority priority{ChannelPriority::Medium};
        BandwidthBucket bucket{BandwidthBucket::Medium};
        float relevancyRadius{5000.0f};
        bool dormancyEnabled{true};
        float dormancyTimeout{5.0f};
    };

    struct BandwidthBudgetDef {
        std::string budgetId;
        std::string name;
        float maxBytesPerSecond{65536.0f};
        float saturationThreshold{0.85f};
        BandwidthBucket bucket{BandwidthBucket::Medium};
        bool dynamicScaling{true};
        int priorityChannels{4};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "ReplicationGraphTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateRepNode(const RepNodeConfig& config);
    bool RemoveRepNode(const std::string& nodeId);
    bool SetRepNodeType(const std::string& nodeId, RepNodeType type);
    bool SetCellSize(const std::string& nodeId, float cellSize);
    bool AddActorClassToNode(const std::string& nodeId, const std::string& actorClass);
    bool RemoveActorClassFromNode(const std::string& nodeId, const std::string& actorClass);
    const RepNodeConfig* GetRepNode(const std::string& nodeId) const;
    std::vector<std::string> GetAllNodeIds() const;
    std::vector<std::string> GetNodesByType(RepNodeType type) const;

    std::string CreateActorChannel(const ActorChannelDef& def);
    bool RemoveActorChannel(const std::string& channelId);
    bool SetChannelPriority(const std::string& channelId, ChannelPriority priority);
    bool SetDormancyEnabled(const std::string& channelId, bool enabled);
    const ActorChannelDef* GetActorChannel(const std::string& channelId) const;

    std::string CreateBandwidthBudget(const BandwidthBudgetDef& def);
    bool RemoveBandwidthBudget(const std::string& budgetId);
    bool SetMaxBytesPerSecond(const std::string& budgetId, float max);

    bool ValidateGraph() const;
    bool SaveConfig(const std::string& filePath) const;
    bool LoadConfig(const std::string& filePath);
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, RepNodeConfig> m_nodes;
    std::unordered_map<std::string, ActorChannelDef> m_channels;
    std::unordered_map<std::string, BandwidthBudgetDef> m_budgets;
    int m_nextNodeIndex{0};
};

} // namespace Atlas::Editor
