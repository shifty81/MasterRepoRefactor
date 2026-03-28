// ScriptingVM.cpp
// Atlas Engine — scripting virtual machine.

#include "Scripting/ScriptingVM.h"

#include <algorithm>

namespace atlas::scripting {

bool ScriptingVM::Initialize() { m_nextContextId = 1; return true; }
void ScriptingVM::Shutdown()
{
    m_bindings.clear();
    m_contexts.clear();
    m_eventHandlers.clear();
}

// ---- binding registry -------------------------------------------------------

bool ScriptingVM::RegisterBinding(const ScriptBinding& binding)
{
    for (auto& b : m_bindings)
        if (b.name == binding.name && b.module == binding.module)
        { b = binding; return true; }
    m_bindings.push_back(binding);
    return true;
}

bool ScriptingVM::UnregisterBinding(const std::string& name)
{
    auto it = std::find_if(m_bindings.begin(), m_bindings.end(),
                           [&](const ScriptBinding& b){ return b.name == name; });
    if (it == m_bindings.end()) return false;
    m_bindings.erase(it);
    return true;
}

bool ScriptingVM::HasBinding(const std::string& name) const
{
    return FindBinding(name).has_value();
}

std::optional<ScriptBinding> ScriptingVM::FindBinding(const std::string& name) const
{
    for (const auto& b : m_bindings)
        if (b.name == name) return b;
    return std::nullopt;
}

std::vector<ScriptBinding> ScriptingVM::ListBindings(const std::string& module) const
{
    if (module.empty()) return m_bindings;
    std::vector<ScriptBinding> result;
    for (const auto& b : m_bindings)
        if (b.module == module) result.push_back(b);
    return result;
}

// ---- context management -----------------------------------------------------

uint64_t ScriptingVM::CreateContext(uint64_t entityId, const std::string& scriptName)
{
    ScriptContext ctx;
    ctx.contextId  = m_nextContextId++;
    ctx.entityId   = entityId;
    ctx.scriptName = scriptName;
    ctx.state      = EScriptState::Idle;
    m_contexts.push_back(ctx);
    return ctx.contextId;
}

bool ScriptingVM::DestroyContext(uint64_t contextId)
{
    auto it = std::find_if(m_contexts.begin(), m_contexts.end(),
                           [contextId](const ScriptContext& c){ return c.contextId == contextId; });
    if (it == m_contexts.end()) return false;
    m_contexts.erase(it);
    return true;
}

bool ScriptingVM::HasContext(uint64_t contextId) const
{
    for (const auto& c : m_contexts)
        if (c.contextId == contextId) return true;
    return false;
}

ScriptContext* ScriptingVM::GetContext(uint64_t contextId)
{
    return GetMutableContext(contextId);
}

const ScriptContext* ScriptingVM::GetContext(uint64_t contextId) const
{
    for (const auto& c : m_contexts)
        if (c.contextId == contextId) return &c;
    return nullptr;
}

std::vector<ScriptContext> ScriptingVM::ListContexts() const
{
    return m_contexts;
}

// ---- execution --------------------------------------------------------------

ScriptExecResult ScriptingVM::Call(const std::string& bindingName,
                                     const ScriptArgs& args)
{
    ScriptExecResult result;
    auto binding = FindBinding(bindingName);
    if (!binding)
    {
        result.success      = false;
        result.errorMessage = "Binding not found: " + bindingName;
        return result;
    }

    if (args.size() < binding->minArgs)
    {
        result.success      = false;
        result.errorMessage = "Too few arguments for: " + bindingName;
        return result;
    }

    try
    {
        result.returnValue = binding->fn(args);
        result.success     = true;
    }
    catch (const std::exception& ex)
    {
        result.success      = false;
        result.errorMessage = ex.what();
    }
    return result;
}

ScriptExecResult ScriptingVM::CallInContext(uint64_t contextId,
                                              const std::string& bindingName,
                                              const ScriptArgs& args)
{
    ScriptContext* ctx = GetMutableContext(contextId);
    if (!ctx)
    {
        ScriptExecResult r;
        r.success      = false;
        r.errorMessage = "Context not found";
        return r;
    }

    ctx->state = EScriptState::Running;
    auto result = Call(bindingName, args);
    ctx->state = result.success ? EScriptState::Idle : EScriptState::Error;
    if (!result.success)
        ctx->errorMessage = result.errorMessage;
    return result;
}

// ---- event dispatch ---------------------------------------------------------

void ScriptingVM::SubscribeEvent(const std::string& eventName,
                                   ScriptEventCallback callback)
{
    m_eventHandlers[eventName] = std::move(callback);
}

void ScriptingVM::UnsubscribeEvent(const std::string& eventName)
{
    m_eventHandlers.erase(eventName);
}

void ScriptingVM::FireEvent(const ScriptEvent& event)
{
    auto it = m_eventHandlers.find(event.eventName);
    if (it != m_eventHandlers.end())
        it->second(event);
}

void ScriptingVM::FireEvent(const std::string& eventName,
                              uint64_t entityId,
                              const ScriptArgs& args)
{
    FireEvent({ eventName, entityId, args });
}

// ---- tick -------------------------------------------------------------------

void ScriptingVM::Tick(float /*deltaSeconds*/)
{
    // Placeholder: in a real VM, resume coroutines, expire timeouts, etc.
}

ScriptContext* ScriptingVM::GetMutableContext(uint64_t contextId)
{
    for (auto& c : m_contexts)
        if (c.contextId == contextId) return &c;
    return nullptr;
}

} // namespace atlas::scripting
