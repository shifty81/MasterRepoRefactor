// InputContextManager.cpp
// Atlas Engine — input context management.

#include "InputContextManager.h"

namespace atlas::input {

bool InputContextManager::Initialize(InputManager& manager)
{
    m_manager = &manager;
    m_contextStack.clear();
    m_contextStack.push_back(EInputContext::Game);
    m_mouseMode = EMouseCaptureMode::Free;
    return true;
}

void InputContextManager::Shutdown()
{
    m_contextStack.clear();
    m_manager = nullptr;
}

// ---- context switching --------------------------------------------------

void InputContextManager::PushContext(EInputContext ctx, const std::string& reason)
{
    EInputContext prev = CurrentContext();
    m_contextStack.push_back(ctx);
    FireContextChanged(prev, ctx, reason);
    ApplyDefaultMousePolicy(ctx);
}

void InputContextManager::PopContext()
{
    if (m_contextStack.size() <= 1) return; // never remove the root
    EInputContext prev = CurrentContext();
    m_contextStack.pop_back();
    EInputContext next = CurrentContext();
    FireContextChanged(prev, next, "pop");
    ApplyDefaultMousePolicy(next);
}

void InputContextManager::SetContext(EInputContext ctx, const std::string& reason)
{
    EInputContext prev = CurrentContext();
    m_contextStack.clear();
    m_contextStack.push_back(ctx);
    FireContextChanged(prev, ctx, reason);
    ApplyDefaultMousePolicy(ctx);
}

void InputContextManager::FireContextChanged(EInputContext from, EInputContext to,
                                               const std::string& reason)
{
    m_history.push_back({ from, to, reason });
    if (m_contextCb) m_contextCb(from, to);
}

// ---- mouse capture ------------------------------------------------------

void InputContextManager::SetMouseCapture(EMouseCaptureMode mode)
{
    m_mouseMode = mode;
}

void InputContextManager::ApplyDefaultMousePolicy(EInputContext ctx)
{
    switch (ctx)
    {
        case EInputContext::Game:        SetMouseCapture(EMouseCaptureMode::Locked);   break;
        case EInputContext::UI:          SetMouseCapture(EMouseCaptureMode::Free);     break;
        case EInputContext::Editor:      SetMouseCapture(EMouseCaptureMode::Confined); break;
        case EInputContext::EditorModal: SetMouseCapture(EMouseCaptureMode::Free);     break;
        case EInputContext::Debug:       SetMouseCapture(EMouseCaptureMode::Free);     break;
        default:                         SetMouseCapture(EMouseCaptureMode::Free);     break;
    }
}

// ---- remappable keybinds ------------------------------------------------

void InputContextManager::LoadKeybindConfig(const KeybindConfig& cfg)
{
    m_keybinds        = cfg;
    m_defaultKeybinds = cfg;
    ApplyBindingsToManager();
}

KeybindConfig InputContextManager::GetKeybindConfig() const
{
    return m_keybinds;
}

bool InputContextManager::Remap(InputAction action,
                                  InputDevice device,
                                  uint32_t key)
{
    for (auto& b : m_keybinds.bindings)
    {
        if (b.action == action && b.rebindable)
        {
            b.primaryDevice = device;
            b.primaryKey    = key;
            if (m_manager)
                m_manager->BindAction(action, device, key, b.displayName);
            return true;
        }
    }
    return false;
}

bool InputContextManager::ResetToDefault(InputAction action)
{
    for (size_t i = 0; i < m_defaultKeybinds.bindings.size(); ++i)
    {
        if (m_defaultKeybinds.bindings[i].action == action)
        {
            const auto& def = m_defaultKeybinds.bindings[i];
            if (i < m_keybinds.bindings.size())
                m_keybinds.bindings[i] = def;
            if (m_manager)
                m_manager->BindAction(action, def.primaryDevice,
                                       def.primaryKey, def.displayName);
            return true;
        }
    }
    return false;
}

void InputContextManager::ResetAllToDefault()
{
    m_keybinds = m_defaultKeybinds;
    ApplyBindingsToManager();
}

void InputContextManager::ApplyBindingsToManager()
{
    if (!m_manager) return;
    for (const auto& b : m_keybinds.bindings)
        m_manager->BindAction(b.action, b.primaryDevice, b.primaryKey, b.displayName);
}

// ---- action routing -----------------------------------------------------

bool InputContextManager::IsGameplayAction(InputAction action)
{
    switch (action)
    {
        case InputAction::MoveForward:
        case InputAction::MoveBackward:
        case InputAction::MoveLeft:
        case InputAction::MoveRight:
        case InputAction::Jump:
        case InputAction::Crouch:
        case InputAction::Sprint:
        case InputAction::PrimaryAction:
        case InputAction::SecondaryAction:
        case InputAction::Reload:
        case InputAction::BoardShip:
            return true;
        default:
            return false;
    }
}

bool InputContextManager::ShouldDispatch(InputAction action) const
{
    EInputContext ctx = CurrentContext();
    if (ctx == EInputContext::Game)         return true;
    if (ctx == EInputContext::Debug)        return true;
    if (ctx == EInputContext::UI ||
        ctx == EInputContext::EditorModal)
        return !IsGameplayAction(action);
    if (ctx == EInputContext::Editor)
        return !IsGameplayAction(action); // editor actions pass, gameplay blocked
    return false;
}

bool InputContextManager::RoutePress(InputAction action)
{
    if (!m_manager || !ShouldDispatch(action)) return false;
    m_manager->InjectPress(action);
    return true;
}

bool InputContextManager::RouteRelease(InputAction action)
{
    if (!m_manager || !ShouldDispatch(action)) return false;
    m_manager->InjectRelease(action);
    return true;
}

} // namespace atlas::input
