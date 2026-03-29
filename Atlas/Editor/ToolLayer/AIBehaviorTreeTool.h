#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P11 Tool — AI behavior tree authoring and visual editing tool.
class AIBehaviorTreeTool : public ITool {
public:
    enum class NodeType {
        Root, Sequence, Selector, Parallel, Decorator,
        Condition, Action, SubTree, BlackboardQuery
    };
    enum class DecoratorType { Invert, Repeat, RetryUntilFail, Cooldown, Timeout, AlwaysSucceed };
    enum class ParallelPolicy { RequireOne, RequireAll };
    enum class BlackboardOp { Equals, NotEquals, Greater, Less, IsSet, IsNotSet };
    enum class NodeStatus { Success, Failure, Running, Idle };

    struct BlackboardEntry {
        std::string key;
        std::string valueType;   // "bool", "int", "float", "string", "vector3"
        std::string defaultValue;
    };

    struct NodePort {
        std::string portId;
        std::string name;
        bool isOutput{false};
        std::string connectedNodeId;
        std::string connectedPortId;
    };

    struct BehaviorNode {
        std::string nodeId;
        std::string name;
        NodeType type{NodeType::Action};
        DecoratorType decoratorType{DecoratorType::Invert};
        ParallelPolicy parallelPolicy{ParallelPolicy::RequireOne};
        BlackboardOp bbOp{BlackboardOp::IsSet};
        std::string actionId;
        std::string conditionId;
        std::string subTreeId;
        std::string bbKey;
        std::string bbValue;
        std::string parentNodeId;
        std::vector<std::string> childNodeIds;
        std::vector<NodePort> ports;
        float posX{0.0f};
        float posY{0.0f};
        float weight{1.0f};
        int repeatCount{-1};
        float cooldownSeconds{1.0f};
        float timeoutSeconds{5.0f};
        NodeStatus lastStatus{NodeStatus::Idle};
        bool enabled{true};
        std::string comment;
    };

    struct BehaviorTree {
        std::string treeId;
        std::string name;
        std::string rootNodeId;
        std::vector<std::string> nodeIds;
        std::vector<BlackboardEntry> blackboard;
        bool debugMode{false};
        std::string linkedAgentId;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AIBehaviorTreeTool"; }
    bool IsActive() const override { return m_active; }

    // Tree management
    std::string CreateTree(const std::string& name);
    bool RemoveTree(const std::string& treeId);
    bool DuplicateTree(const std::string& srcTreeId, const std::string& newName);
    bool SetDebugMode(const std::string& treeId, bool debug);
    bool LinkToAgent(const std::string& treeId, const std::string& agentId);
    int GetTreeCount() const { return static_cast<int>(m_trees.size()); }
    const BehaviorTree* GetTree(const std::string& treeId) const;
    std::vector<std::string> GetTreeIds() const;

    // Node management
    std::string AddNode(const std::string& treeId, NodeType type,
                         const std::string& name = "");
    bool RemoveNode(const std::string& treeId, const std::string& nodeId);
    bool SetNodeType(const std::string& treeId, const std::string& nodeId,
                      NodeType type);
    bool SetDecoratorType(const std::string& treeId, const std::string& nodeId,
                           DecoratorType decoratorType);
    bool SetParallelPolicy(const std::string& treeId, const std::string& nodeId,
                            ParallelPolicy policy);
    bool SetNodeAction(const std::string& treeId, const std::string& nodeId,
                        const std::string& actionId);
    bool SetNodeCondition(const std::string& treeId, const std::string& nodeId,
                           const std::string& conditionId);
    bool SetNodeBlackboardQuery(const std::string& treeId, const std::string& nodeId,
                                  const std::string& key, BlackboardOp op,
                                  const std::string& value = "");
    bool SetNodeSubTree(const std::string& treeId, const std::string& nodeId,
                         const std::string& subTreeId);
    bool SetNodePosition(const std::string& treeId, const std::string& nodeId,
                          float px, float py);
    bool SetNodeEnabled(const std::string& treeId, const std::string& nodeId,
                         bool enabled);
    bool SetNodeComment(const std::string& treeId, const std::string& nodeId,
                         const std::string& comment);
    bool SetRepeatCount(const std::string& treeId, const std::string& nodeId,
                         int count);
    bool SetCooldown(const std::string& treeId, const std::string& nodeId,
                      float seconds);
    bool SetTimeout(const std::string& treeId, const std::string& nodeId,
                     float seconds);
    int GetNodeCount(const std::string& treeId) const;
    const BehaviorNode* GetNode(const std::string& treeId,
                                  const std::string& nodeId) const;

    // Parent-child wiring
    bool SetParent(const std::string& treeId, const std::string& nodeId,
                    const std::string& parentId);
    bool AddChild(const std::string& treeId, const std::string& parentId,
                   const std::string& childId);
    bool RemoveChild(const std::string& treeId, const std::string& parentId,
                      const std::string& childId);
    bool SetRootNode(const std::string& treeId, const std::string& nodeId);

    // Blackboard
    bool AddBlackboardEntry(const std::string& treeId, const std::string& key,
                              const std::string& valueType,
                              const std::string& defaultValue = "");
    bool RemoveBlackboardEntry(const std::string& treeId, const std::string& key);
    int GetBlackboardEntryCount(const std::string& treeId) const;

    // Debug
    bool SetNodeStatus(const std::string& treeId, const std::string& nodeId,
                        NodeStatus status);

    // Persistence
    bool SaveTree(const std::string& treeId, const std::string& filePath) const;
    bool LoadTree(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, BehaviorTree> m_trees;
    std::unordered_map<std::string, BehaviorNode> m_nodes;
    int m_nextTreeIndex{0};
    int m_nextNodeIndex{0};
};

} // namespace Atlas::Editor
