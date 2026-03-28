// ADLPanel.cpp
// Atlas Editor — Architecture Decision Log panel.

#include "Docs/ADLPanel.h"

#include <algorithm>

namespace atlas::editor::docs {

bool ADLPanel::Initialize() { return true; }
void ADLPanel::Shutdown()   { m_entries.clear(); }

void ADLPanel::AddEntry(const ADLEntry& entry)
{
    for (auto& e : m_entries)
        if (e.entryId == entry.entryId) { e = entry; return; }
    m_entries.push_back(entry);
}

bool ADLPanel::RemoveEntry(const std::string& entryId)
{
    auto it = std::find_if(m_entries.begin(), m_entries.end(),
                           [&](const ADLEntry& e){ return e.entryId == entryId; });
    if (it == m_entries.end()) return false;
    m_entries.erase(it);
    return true;
}

bool ADLPanel::HasEntry(const std::string& entryId) const
{
    return FindEntry(entryId).has_value();
}

bool ADLPanel::UpdateEntry(const ADLEntry& entry)
{
    ADLEntry* e = GetMutable(entry.entryId);
    if (!e) return false;
    *e = entry;
    return true;
}

bool ADLPanel::SetStatus(const std::string& entryId, EADLStatus status)
{
    ADLEntry* e = GetMutable(entryId);
    if (!e) return false;
    e->status = status;
    return true;
}

bool ADLPanel::Supersede(const std::string& entryId,
                           const std::string& supersededById)
{
    ADLEntry* e = GetMutable(entryId);
    if (!e) return false;
    e->status          = EADLStatus::Superseded;
    e->supersededById  = supersededById;
    return true;
}

std::optional<ADLEntry> ADLPanel::FindEntry(const std::string& entryId) const
{
    for (const auto& e : m_entries)
        if (e.entryId == entryId) return e;
    return std::nullopt;
}

std::vector<ADLEntry> ADLPanel::ListAll() const
{
    return m_entries;
}

std::vector<ADLEntry> ADLPanel::ListByStatus(EADLStatus status) const
{
    std::vector<ADLEntry> result;
    for (const auto& e : m_entries)
        if (e.status == status) result.push_back(e);
    return result;
}

std::vector<ADLEntry> ADLPanel::Search(const std::string& query) const
{
    std::vector<ADLEntry> result;
    for (const auto& e : m_entries)
    {
        if (e.title.find(query)    != std::string::npos ||
            e.decision.find(query) != std::string::npos ||
            e.context.find(query)  != std::string::npos)
            result.push_back(e);
    }
    return result;
}

std::vector<ADLEntry> ADLPanel::LinkedTo(const std::string& target) const
{
    std::vector<ADLEntry> result;
    for (const auto& e : m_entries)
        for (const auto& lk : e.contextLinks)
            if (lk.target == target) { result.push_back(e); break; }
    return result;
}

bool ADLPanel::AddContextLink(const std::string& entryId,
                                const ADLContextLink& link)
{
    ADLEntry* e = GetMutable(entryId);
    if (!e) return false;
    e->contextLinks.push_back(link);
    return true;
}

bool ADLPanel::RemoveContextLink(const std::string& entryId,
                                   const std::string& target)
{
    ADLEntry* e = GetMutable(entryId);
    if (!e) return false;
    auto it = std::find_if(e->contextLinks.begin(), e->contextLinks.end(),
                           [&](const ADLContextLink& l){ return l.target == target; });
    if (it == e->contextLinks.end()) return false;
    e->contextLinks.erase(it);
    return true;
}

void ADLPanel::NavigateTo(const ADLContextLink& link)
{
    if (m_navCb) m_navCb(link);
}

size_t ADLPanel::AcceptedCount() const
{
    size_t c = 0;
    for (const auto& e : m_entries)
        if (e.status == EADLStatus::Accepted) ++c;
    return c;
}

ADLEntry* ADLPanel::GetMutable(const std::string& entryId)
{
    for (auto& e : m_entries)
        if (e.entryId == entryId) return &e;
    return nullptr;
}

} // namespace atlas::editor::docs
