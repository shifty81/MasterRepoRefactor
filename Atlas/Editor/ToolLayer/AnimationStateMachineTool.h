#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P7 Tool — Visual editor for character and object animation state machines.
class AnimationStateMachineTool : public ITool {
public:
    enum class TransitionCondition { Bool, Float, Int, Trigger };

    struct Transition {
        std::string transitionId;
        std::string fromStateId;
        std::string toStateId;
        TransitionCondition condition{TransitionCondition::Bool};
        std::string parameterName;
        float threshold{0.0f};
        float exitTime{1.0f};
        float transitionDuration{0.1f};
        bool hasExitTime{false};
    };

    struct State {
        std::string stateId;
        std::string name;
        std::string clipAsset;
        float speed{1.0f};
        bool loop{true};
        bool isAnyState{false};
        bool isEntryState{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AnimationStateMachineTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateStateMachine(const std::string& name);
    bool SetActiveMachine(const std::string& machineId);
    std::string AddState(const std::string& name, const std::string& clipAsset = "");
    bool RemoveState(const std::string& stateId);
    bool SetStateClip(const std::string& stateId, const std::string& clipAsset);
    bool SetStateSpeed(const std::string& stateId, float speed);
    bool SetEntryState(const std::string& stateId);
    std::string AddTransition(const std::string& fromId, const std::string& toId);
    bool RemoveTransition(const std::string& transitionId);
    bool SetTransitionCondition(const std::string& transitionId,
                                 TransitionCondition cond,
                                 const std::string& paramName,
                                 float threshold = 0.0f);
    bool SetTransitionDuration(const std::string& transitionId, float duration);
    int GetStateCount() const { return static_cast<int>(m_states.size()); }
    int GetTransitionCount() const { return static_cast<int>(m_transitions.size()); }
    int GetMachineCount() const { return static_cast<int>(m_machines.size()); }
    const State* GetState(const std::string& stateId) const;
    const Transition* GetTransition(const std::string& transitionId) const;
    void ClearAll();

private:
    bool m_active{false};
    std::vector<State> m_states;
    std::vector<Transition> m_transitions;
    std::vector<std::pair<std::string, std::string>> m_machines; // id, name
    std::string m_activeMachineId;
    std::string m_entryStateId;
    int m_nextStateIndex{0};
    int m_nextTransitionIndex{0};
    int m_nextMachineIndex{0};
};

} // namespace Atlas::Editor
