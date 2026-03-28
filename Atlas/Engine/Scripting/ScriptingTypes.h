// ScriptingTypes.h
// Atlas Engine — scripting bridge types: value, function binding, event dispatch.

#pragma once
#include <cstdint>
#include <functional>
#include <string>
#include <variant>
#include <vector>

namespace atlas::scripting {

// ---------------------------------------------------------------------------
// Script value (dynamic type for API boundary)
// ---------------------------------------------------------------------------

using ScriptValue = std::variant<
    std::monostate,   ///< nil / null
    bool,
    int64_t,
    double,
    std::string
>;

inline bool IsNil(const ScriptValue& v) { return std::holds_alternative<std::monostate>(v); }
inline bool AsBool(const ScriptValue& v, bool def = false)
{ return std::holds_alternative<bool>(v) ? std::get<bool>(v) : def; }
inline int64_t AsInt(const ScriptValue& v, int64_t def = 0)
{ return std::holds_alternative<int64_t>(v) ? std::get<int64_t>(v) : def; }
inline double AsFloat(const ScriptValue& v, double def = 0.0)
{ return std::holds_alternative<double>(v) ? std::get<double>(v) : def; }
inline std::string AsString(const ScriptValue& v, const std::string& def = "")
{ return std::holds_alternative<std::string>(v) ? std::get<std::string>(v) : def; }

// ---------------------------------------------------------------------------
// Script function binding
// ---------------------------------------------------------------------------

using ScriptArgs   = std::vector<ScriptValue>;
using ScriptReturn = ScriptValue;
using NativeFunction = std::function<ScriptReturn(const ScriptArgs&)>;

struct ScriptBinding
{
    std::string    name;
    std::string    module;       ///< namespace/module this belongs to
    std::string    docString;
    NativeFunction fn;
    uint8_t        minArgs = 0;
    uint8_t        maxArgs = 255;
};

// ---------------------------------------------------------------------------
// Script event
// ---------------------------------------------------------------------------

struct ScriptEvent
{
    std::string   eventName;
    uint64_t      entityId  = 0;  ///< source entity (0 = global)
    ScriptArgs    args;
};

using ScriptEventCallback = std::function<void(const ScriptEvent&)>;

// ---------------------------------------------------------------------------
// Script execution context per entity / module
// ---------------------------------------------------------------------------

enum class EScriptState : uint8_t
{
    Idle,
    Running,
    Suspended,
    Error,
    Finished,
};

struct ScriptContext
{
    uint64_t       contextId   = 0;
    uint64_t       entityId    = 0;   ///< owning entity (0 = global)
    std::string    scriptName;
    EScriptState   state       = EScriptState::Idle;
    std::string    errorMessage;
    ScriptArgs     locals;            ///< simple local variable store
};

} // namespace atlas::scripting
