#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P9 Tool — Visual scripting debugger panel for inspecting blueprint graphs at runtime.
class BlueprintDebuggerTool : public ITool {
public:
    enum class DebuggerState { Idle, Running, Paused, Stepping };
    enum class BreakpointType { NodeEntry, NodeExit, VariableWatch, Conditional };
    enum class NodeExecutionState { Pending, Active, Completed, Error };
    enum class WireHighlight { Normal, Active, Inactive, Error };

    struct Breakpoint {
        std::string breakpointId;
        std::string graphId;
        std::string nodeId;
        BreakpointType type{BreakpointType::NodeEntry};
        bool enabled{true};
        std::string condition;       // optional expression
        int hitCount{0};
        int ignoreCount{0};
    };

    struct WatchVariable {
        std::string watchId;
        std::string graphId;
        std::string variableName;
        std::string currentValue;
        std::string previousValue;
        bool changed{false};
    };

    struct NodeState {
        std::string nodeId;
        NodeExecutionState state{NodeExecutionState::Pending};
        int executionCount{0};
        float lastExecutionTimeMs{0.0f};
        std::string lastError;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "BlueprintDebuggerTool"; }
    bool IsActive() const override { return m_active; }

    // Debugger control
    void AttachGraph(const std::string& graphId);
    void DetachGraph(const std::string& graphId);
    bool IsAttached(const std::string& graphId) const;
    int GetAttachedGraphCount() const { return static_cast<int>(m_attachedGraphs.size()); }
    DebuggerState GetDebuggerState() const { return m_debuggerState; }

    void Run();
    void Pause();
    void StepOver();
    void StepInto();
    void StepOut();
    void Continue();
    void Stop();

    // Breakpoints
    std::string AddBreakpoint(const std::string& graphId, const std::string& nodeId,
                               BreakpointType type = BreakpointType::NodeEntry);
    bool RemoveBreakpoint(const std::string& breakpointId);
    bool EnableBreakpoint(const std::string& breakpointId, bool enabled);
    bool SetBreakpointCondition(const std::string& breakpointId,
                                 const std::string& condition);
    bool SetBreakpointIgnoreCount(const std::string& breakpointId, int ignoreCount);
    int GetBreakpointCount() const { return static_cast<int>(m_breakpoints.size()); }
    const Breakpoint* GetBreakpoint(const std::string& breakpointId) const;
    std::vector<std::string> GetBreakpointIdsForGraph(const std::string& graphId) const;
    void ClearBreakpoints();

    // Watch variables
    std::string AddWatchVariable(const std::string& graphId,
                                  const std::string& variableName);
    bool RemoveWatchVariable(const std::string& watchId);
    bool UpdateWatchValue(const std::string& watchId, const std::string& value);
    int GetWatchCount() const { return static_cast<int>(m_watches.size()); }
    const WatchVariable* GetWatchVariable(const std::string& watchId) const;
    std::vector<std::string> GetChangedWatchIds() const;

    // Node states
    void UpdateNodeState(const std::string& nodeId, NodeExecutionState state,
                          float execTimeMs = 0.0f);
    const NodeState* GetNodeState(const std::string& nodeId) const;
    std::vector<std::string> GetErrorNodeIds() const;
    int GetTotalExecutionCount() const;

    // Wire highlighting
    void SetWireHighlight(const std::string& wireId, WireHighlight highlight);
    WireHighlight GetWireHighlight(const std::string& wireId) const;
    void ClearWireHighlights();

    void ClearAll();

private:
    bool m_active{false};
    DebuggerState m_debuggerState{DebuggerState::Idle};
    std::vector<std::string> m_attachedGraphs;
    std::unordered_map<std::string, Breakpoint> m_breakpoints;
    std::unordered_map<std::string, WatchVariable> m_watches;
    std::unordered_map<std::string, NodeState> m_nodeStates;
    std::unordered_map<std::string, WireHighlight> m_wireHighlights;
    int m_nextBreakpointIndex{0};
    int m_nextWatchIndex{0};
};

} // namespace Atlas::Editor
