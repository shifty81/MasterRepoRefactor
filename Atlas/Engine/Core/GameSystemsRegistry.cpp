// GameSystemsRegistry.cpp
// Atlas Engine — registry implementation.

#include "GameSystemsRegistry.h"
#include <algorithm>
#include <sstream>
#include <stdexcept>

namespace atlas
{

// ---------------------------------------------------------------------------
// Singleton
// ---------------------------------------------------------------------------

GameSystemsRegistry& GameSystemsRegistry::Get()
{
    static GameSystemsRegistry instance;
    return instance;
}

// ---------------------------------------------------------------------------
// Registration
// ---------------------------------------------------------------------------

bool GameSystemsRegistry::Register(const std::string& name, const std::string& category)
{
    if (FindMutable(name) != nullptr)
        return false;
    m_systems.push_back({ name, category, ESystemState::Pending, {} });
    return true;
}

// ---------------------------------------------------------------------------
// State transitions
// ---------------------------------------------------------------------------

bool GameSystemsRegistry::SetState(const std::string& name, ESystemState state,
                                    const std::string& errorMessage)
{
    SystemEntry* entry = FindMutable(name);
    if (!entry) return false;
    entry->state        = state;
    entry->errorMessage = errorMessage;
    return true;
}

bool GameSystemsRegistry::MarkReady(const std::string& name)
{
    return SetState(name, ESystemState::Ready);
}

bool GameSystemsRegistry::MarkFailed(const std::string& name, const std::string& reason)
{
    return SetState(name, ESystemState::Failed, reason);
}

// ---------------------------------------------------------------------------
// Queries
// ---------------------------------------------------------------------------

bool GameSystemsRegistry::AllReady() const
{
    for (const auto& s : m_systems)
        if (s.state != ESystemState::Ready) return false;
    return !m_systems.empty();
}

std::vector<const SystemEntry*> GameSystemsRegistry::GetFailed() const
{
    return GetByState(ESystemState::Failed);
}

std::vector<const SystemEntry*> GameSystemsRegistry::GetByState(ESystemState state) const
{
    std::vector<const SystemEntry*> result;
    for (const auto& s : m_systems)
        if (s.state == state) result.push_back(&s);
    return result;
}

const SystemEntry* GameSystemsRegistry::Find(const std::string& name) const
{
    return const_cast<GameSystemsRegistry*>(this)->FindMutable(name);
}

size_t GameSystemsRegistry::CountByState(ESystemState state) const
{
    size_t n = 0;
    for (const auto& s : m_systems)
        if (s.state == state) ++n;
    return n;
}

// ---------------------------------------------------------------------------
// Lifecycle
// ---------------------------------------------------------------------------

void GameSystemsRegistry::Reset()
{
    m_systems.clear();
}

std::string GameSystemsRegistry::HealthReport() const
{
    static const char* kStateNames[] = {
        "Pending", "Initialising", "Ready", "Failed", "ShuttingDown", "Shutdown"
    };
    std::ostringstream ss;
    ss << "=== GameSystemsRegistry Health Report ===\n";
    ss << "Total: " << m_systems.size() << "\n";
    for (const auto& s : m_systems)
    {
        const char* stateStr = kStateNames[static_cast<int>(s.state)];
        ss << "  [" << s.category << "] " << s.name << " — " << stateStr;
        if (!s.errorMessage.empty())
            ss << " (" << s.errorMessage << ")";
        ss << "\n";
    }
    return ss.str();
}

// ---------------------------------------------------------------------------
// Private helpers
// ---------------------------------------------------------------------------

SystemEntry* GameSystemsRegistry::FindMutable(const std::string& name)
{
    for (auto& s : m_systems)
        if (s.name == name) return &s;
    return nullptr;
}

} // namespace atlas
