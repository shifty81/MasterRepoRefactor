// ScriptingVM.h
// Atlas Engine — scripting virtual machine: binding registry, script context
// lifecycle, event dispatch, and execution hooks.

#pragma once
#include "Scripting/ScriptingTypes.h"

#include <optional>
#include <unordered_map>
#include <vector>

namespace atlas::scripting {

// ---------------------------------------------------------------------------
// Execution result
// ---------------------------------------------------------------------------

struct ScriptExecResult
{
    bool         success = false;
    ScriptReturn returnValue;
    std::string  errorMessage;
};

// ---------------------------------------------------------------------------
// ScriptingVM
// ---------------------------------------------------------------------------

class ScriptingVM
{
public:
    ScriptingVM()  = default;
    ~ScriptingVM() = default;

    bool Initialize();
    void Shutdown();

    // ---- native binding registry ----------------------------------------
    bool RegisterBinding (const ScriptBinding& binding);
    bool UnregisterBinding(const std::string& name);
    bool HasBinding(const std::string& name) const;
    std::optional<ScriptBinding> FindBinding(const std::string& name) const;
    std::vector<ScriptBinding>   ListBindings(const std::string& module = "") const;

    // ---- script context management --------------------------------------
    uint64_t     CreateContext  (uint64_t entityId, const std::string& scriptName);
    bool         DestroyContext (uint64_t contextId);
    bool         HasContext     (uint64_t contextId) const;
    ScriptContext* GetContext   (uint64_t contextId);
    const ScriptContext* GetContext(uint64_t contextId) const;
    std::vector<ScriptContext> ListContexts() const;

    // ---- execution -------------------------------------------------------
    ScriptExecResult Call(const std::string& bindingName,
                           const ScriptArgs& args = {});
    ScriptExecResult CallInContext(uint64_t contextId,
                                    const std::string& bindingName,
                                    const ScriptArgs& args = {});

    // ---- event dispatch --------------------------------------------------
    void  SubscribeEvent   (const std::string& eventName,
                             ScriptEventCallback callback);
    void  UnsubscribeEvent (const std::string& eventName);
    void  FireEvent        (const ScriptEvent& event);
    void  FireEvent        (const std::string& eventName,
                             uint64_t entityId = 0,
                             const ScriptArgs& args = {});

    // ---- tick / update ---------------------------------------------------
    void Tick(float deltaSeconds);

    // ---- diagnostics -----------------------------------------------------
    size_t BindingCount()  const { return m_bindings.size(); }
    size_t ContextCount()  const { return m_contexts.size(); }

private:
    std::vector<ScriptBinding>                           m_bindings;
    std::vector<ScriptContext>                           m_contexts;
    std::unordered_map<std::string, ScriptEventCallback> m_eventHandlers;
    uint64_t                                             m_nextContextId = 1;

    ScriptContext* GetMutableContext(uint64_t contextId);
};

} // namespace atlas::scripting
