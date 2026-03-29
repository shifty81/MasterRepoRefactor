#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P21 Tool — AI agent runtime debugging, blackboard inspection, and task visualization.
class AIDebuggerTool : public ITool {
public:
    enum class AIDebugMode { Inactive, Snapshot, Live, Stepped, Paused, FilteredLive, Custom };
    enum class BlackboardDisplayMode { Flat, Grouped, Delta, History, TypeFiltered, Custom };
    enum class TaskVisualMode { Tree, List, Timeline, Graph, Overlay, Custom };

    struct AgentWatchEntry {
        std::string watchId;
        std::string agentId;
        std::string agentName;
        std::string behaviorTreeId;
        std::string currentTaskId;
        std::string agentState;
        float tickRate{0.1f};
        bool breakOnTaskChange{false};
        bool logAllTicks{false};
    };

    struct BlackboardEntry {
        std::string entryId;
        std::string agentId;
        std::string keyName;
        std::string keyType;
        std::string value;
        bool isDirty{false};
        bool watchForChange{false};
        BlackboardDisplayMode displayMode{BlackboardDisplayMode::Flat};
    };

    struct TaskVisualizationEntry {
        std::string vizId;
        std::string agentId;
        std::string taskId;
        std::string taskName;
        std::string taskStatus;
        TaskVisualMode visualMode{TaskVisualMode::Tree};
        float executionTime{0.0f};
        bool isActive{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "AIDebuggerTool"; }
    bool IsActive() const override { return m_active; }

    std::string AddAgentWatch(const AgentWatchEntry& entry);
    bool RemoveAgentWatch(const std::string& watchId);
    const AgentWatchEntry* GetAgentWatch(const std::string& watchId) const;
    std::vector<std::string> GetAllAgentWatchIds() const;

    std::string AddBlackboardEntry(const BlackboardEntry& entry);
    bool RemoveBlackboardEntry(const std::string& entryId);
    const BlackboardEntry* GetBlackboardEntry(const std::string& entryId) const;
    std::vector<std::string> GetBlackboardEntriesByAgent(const std::string& agentId) const;

    std::string AddTaskVisualization(const TaskVisualizationEntry& entry);
    bool RemoveTaskVisualization(const std::string& vizId);
    const TaskVisualizationEntry* GetTaskVisualization(const std::string& vizId) const;
    std::vector<std::string> GetActiveTaskVisualizations() const;

    bool SetDebugMode(AIDebugMode mode);
    AIDebugMode GetDebugMode() const { return m_mode; }
    bool SetBlackboardDisplayMode(const std::string& entryId, BlackboardDisplayMode mode);
    bool SetTaskVisualMode(const std::string& vizId, TaskVisualMode mode);
    bool SetBreakOnTaskChange(const std::string& watchId, bool enabled);
    bool SetLogAllTicks(const std::string& watchId, bool enabled);
    bool FilterByAgent(const std::string& agentId);
    bool ClearAgentFilter();
    std::vector<std::string> GetWatchesByAgent(const std::string& agentId) const;
    int GetTotalWatchCount() const;
    bool ExportDebugSnapshot(const std::string& filePath) const;
    void Reset();

private:
    bool m_active{false};
    AIDebugMode m_mode{AIDebugMode::Inactive};
    std::unordered_map<std::string, AgentWatchEntry> m_agentWatches;
    std::unordered_map<std::string, BlackboardEntry> m_blackboardEntries;
    std::unordered_map<std::string, TaskVisualizationEntry> m_taskVisualizations;
    std::string m_agentFilter;
    int m_nextWatchIndex{0};
};

} // namespace Atlas::Editor
