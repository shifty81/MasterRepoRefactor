#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P17 Tool — StateTree graph authoring, state transition configuration, and condition management.
class StateTreeTool : public ITool {
public:
    enum class StateType { Root, Branch, Select, Parallel, Sequence, Leaf };
    enum class TransitionTrigger { OnEnter, OnExit, OnTick, Condition, Event, Timer, Always };
    enum class ConditionOp { And, Or, Not, Equals, Greater, Less, Contains, Changed };

    struct StateDef {
        std::string stateId;
        std::string name;
        StateType stateType{StateType::Leaf};
        std::vector<std::string> enterTasks;
        std::vector<std::string> exitTasks;
        std::vector<std::string> tickTasks;
        int priority{0};
    };

    struct TransitionDef {
        std::string transitionId;
        std::string name;
        std::string fromStateId;
        std::string toStateId;
        TransitionTrigger trigger{TransitionTrigger::Condition};
        std::vector<std::string> conditions;
        int priority{0};
        float delay{0.0f};
    };

    struct StateTreeDef {
        std::string treeId;
        std::string name;
        std::string rootStateId;
        std::vector<std::string> states;
        std::vector<std::string> transitions;
        std::string schema;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "StateTreeTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateTree(const std::string& name);
    bool RemoveTree(const std::string& treeId);
    std::string AddState(const std::string& treeId, const std::string& name, StateType type);
    bool RemoveState(const std::string& treeId, const std::string& stateId);
    std::string AddTransition(const std::string& treeId, const std::string& fromStateId, const std::string& toStateId);
    bool RemoveTransition(const std::string& treeId, const std::string& transitionId);
    bool SetStateType(const std::string& stateId, StateType type);
    bool SetTransitionTrigger(const std::string& transitionId, TransitionTrigger trigger);
    bool AddCondition(const std::string& transitionId, const std::string& condition);
    bool SetConditionOp(const std::string& transitionId, ConditionOp op);
    bool ActivateTree(const std::string& treeId);
    bool DeactivateTree(const std::string& treeId);
    bool TickTree(const std::string& treeId, float deltaTime);
    bool PreviewTree(const std::string& treeId);
    const StateTreeDef* GetTree(const std::string& treeId) const;
    const StateDef* GetState(const std::string& stateId) const;
    const TransitionDef* GetTransition(const std::string& transitionId) const;
    std::vector<std::string> GetAllTreeIds() const;
    std::vector<std::string> GetStatesByType(StateType type) const;
    std::vector<std::string> GetTransitionsByState(const std::string& stateId) const;
    bool ValidateTree(const std::string& treeId) const;
    bool ExportStateTree(const std::string& treeId, const std::string& filePath) const;
    bool SaveStateTree(const std::string& filePath) const;
    bool LoadStateTree(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, StateTreeDef> m_trees;
    std::unordered_map<std::string, StateDef> m_states;
    std::unordered_map<std::string, TransitionDef> m_transitions;
    int m_nextTreeIndex{0};
    int m_nextStateIndex{0};
};

} // namespace Atlas::Editor
