#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>

namespace Atlas::Engine {

/// Phase 37D — Registry for script body components with language-specific execution management.
class ScriptBodyRegistry {
public:
    enum class ScriptBodyState { Idle, Running, Paused, Completed, Failed, Disabled, Custom };
    enum class ScriptBodyScope { Global, Local, Team, Scene, Actor, Component, Custom };
    enum class ScriptLanguage { Lua, Python, Blueprint, JavaScript, AngelScript, Custom };
    enum class ScriptExecutionMode { Immediate, Deferred, Scheduled, EventDriven, Custom };
    enum class ScriptBodyFlags { None = 0, Persistent, Reentrant, DebugTrace, ProfileMode, AutoReload };

    struct ScriptConfig {
        std::string configId;
        std::string scriptPath;
        ScriptLanguage language{ScriptLanguage::Lua};
        ScriptExecutionMode executionMode{ScriptExecutionMode::Immediate};
        int timeoutMs{5000};
        int maxRetries{0};
        bool sandboxed{true};
    };

    struct ScriptBinding {
        std::string bindingId;
        std::string scriptBodyId;
        std::string targetId;
        std::string event;
        std::string handlerName;
        bool active{true};
    };

    struct ScriptBodyRecord {
        std::string bodyId;
        std::string name;
        ScriptBodyScope scope{ScriptBodyScope::Global};
        ScriptBodyState state{ScriptBodyState::Idle};
        ScriptLanguage language{ScriptLanguage::Lua};
        int triggerCount{0};
        std::string lastErrorMessage;
        std::vector<std::string> bindingIds;
        std::vector<std::string> configIds;
    };

    // Body registration
    bool RegisterBody(const ScriptBodyRecord& record);
    bool UnregisterBody(const std::string& bodyId);

    // State and configuration
    bool SetBodyScope(const std::string& bodyId, ScriptBodyScope scope);
    bool SetBodyState(const std::string& bodyId, ScriptBodyState state);
    bool SetScriptLanguage(const std::string& bodyId, ScriptLanguage language);

    // Execution control
    bool ExecuteBody(const std::string& bodyId);
    bool PauseBody(const std::string& bodyId);
    bool ResumeBody(const std::string& bodyId);

    // Queries
    const ScriptBodyRecord* GetBodyById(const std::string& bodyId) const;
    std::vector<std::string> GetAllBodyIds() const;
    std::vector<std::string> GetBodiesByScope(ScriptBodyScope scope) const;
    std::vector<std::string> GetBodiesByLanguage(ScriptLanguage language) const;
    std::vector<std::string> GetRunningBodies() const;
    std::vector<std::string> GetFailedBodies() const;

    // Script config management
    bool AddScriptConfig(const std::string& bodyId, const ScriptConfig& config);
    bool RemoveScriptConfig(const std::string& bodyId, const std::string& configId);
    std::vector<ScriptConfig> GetConfigsByBody(const std::string& bodyId) const;

    // Binding management
    bool AddBinding(const std::string& bodyId, const ScriptBinding& binding);
    bool RemoveBinding(const std::string& bodyId, const std::string& bindingId);
    std::vector<ScriptBinding> GetBindingsByBody(const std::string& bodyId) const;

    // Persistence
    void Clear();
    bool SaveRegistry(const std::string& filePath) const;
    bool LoadRegistry(const std::string& filePath);

private:
    std::unordered_map<std::string, ScriptBodyRecord> m_bodies;
    std::unordered_map<std::string, ScriptConfig> m_configs;
    std::unordered_map<std::string, ScriptBinding> m_bindings;
};

} // namespace Atlas::Engine
