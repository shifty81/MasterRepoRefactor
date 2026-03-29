#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 38C — Orchestrator for coordinating multi-system workflows, task sequencing, and dependency resolution.
class SolarSystemOrchestrator {
public:
    enum class OrchestratorState { Idle, Planning, Executing, Paused, Completing, Aborting, Error };
    enum class TaskPriority { Critical, High, Normal, Low, Background, Custom };
    enum class DependencyMode { Sequential, Parallel, ConditionalAnd, ConditionalOr, Custom };
    enum class WorkflowEventType { TaskStarted, TaskCompleted, TaskFailed, WorkflowStarted, WorkflowCompleted, WorkflowAborted, Custom };

    struct OrchestratorTask {
        std::string taskId;
        std::string workflowId;
        std::string taskName;
        TaskPriority priority{TaskPriority::Normal};
        DependencyMode depMode{DependencyMode::Sequential};
        std::vector<std::string> dependencyIds;
        std::string targetSystemId;
        std::string payload;
        int retryCount{0};
        int maxRetries{3};
        double timeoutMs{30000.0};
        bool completed{false};
        bool failed{false};
    };

    struct WorkflowDef {
        std::string workflowId;
        std::string workflowName;
        OrchestratorState state{OrchestratorState::Idle};
        std::vector<std::string> taskIds;
        int completedTasks{0};
        int totalTasks{0};
        double elapsedMs{0.0};
        bool autoRetry{false};
    };

    struct WorkflowAuditEntry {
        std::string entryId;
        std::string workflowId;
        std::string taskId;
        WorkflowEventType eventType{WorkflowEventType::TaskStarted};
        std::string message;
        long long timestamp{0};
        bool success{false};
    };

    // Workflow management
    bool RegisterWorkflow(const WorkflowDef& def);
    bool UnregisterWorkflow(const std::string& workflowId);
    bool SetWorkflowState(const std::string& workflowId, OrchestratorState state);
    OrchestratorState GetWorkflowState(const std::string& workflowId) const;
    const WorkflowDef* GetWorkflow(const std::string& workflowId) const;
    std::vector<std::string> GetAllWorkflowIds() const;
    std::vector<std::string> GetActiveWorkflows() const;
    std::vector<std::string> GetCompletedWorkflows() const;
    std::vector<std::string> GetFailedWorkflows() const;

    // Task management
    bool AddTask(const std::string& workflowId, const OrchestratorTask& task);
    bool RemoveTask(const std::string& workflowId, const std::string& taskId);
    const OrchestratorTask* GetTask(const std::string& taskId) const;
    std::vector<std::string> GetTasksByWorkflow(const std::string& workflowId) const;
    std::vector<std::string> GetPendingTasks(const std::string& workflowId) const;
    std::vector<std::string> GetCompletedTasks(const std::string& workflowId) const;
    bool CompleteTask(const std::string& taskId, bool success);
    bool RetryTask(const std::string& taskId);
    bool SetTaskPriority(const std::string& taskId, TaskPriority priority);

    // Orchestration
    bool StartWorkflow(const std::string& workflowId);
    bool PauseWorkflow(const std::string& workflowId);
    bool ResumeWorkflow(const std::string& workflowId);
    bool AbortWorkflow(const std::string& workflowId);

    // Audit
    void LogEvent(const WorkflowAuditEntry& entry);
    const WorkflowAuditEntry* GetAuditEntry(const std::string& entryId) const;
    std::vector<std::string> GetAuditByWorkflow(const std::string& workflowId) const;
    void FlushAuditLog();

    void Reset();

private:
    std::unordered_map<std::string, WorkflowDef> m_workflows;
    std::unordered_map<std::string, OrchestratorTask> m_tasks;
    std::unordered_map<std::string, WorkflowAuditEntry> m_auditLog;
    int m_nextAuditIndex{0};
};

} // namespace Atlas::Engine
