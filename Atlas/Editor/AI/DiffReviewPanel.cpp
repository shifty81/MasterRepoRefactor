// DiffReviewPanel.cpp
// Atlas Editor / AtlasAI — AI suggestion diff review panel.

#include "AI/DiffReviewPanel.h"

#include <algorithm>

namespace atlas::editor::ai {

bool DiffReviewPanel::Initialize() { return true; }
void DiffReviewPanel::Shutdown()
{
    m_suggestions.clear();
    m_rollbackHistory.clear();
}

void DiffReviewPanel::SubmitSuggestion(const AISuggestion& suggestion)
{
    for (auto& s : m_suggestions)
        if (s.suggestionId == suggestion.suggestionId) { s = suggestion; return; }
    m_suggestions.push_back(suggestion);
}

bool DiffReviewPanel::AcceptSuggestion(const std::string& id)
{
    AISuggestion* s = GetMutable(id);
    if (!s || s->status != ESuggestionStatus::Pending) return false;

    // Store pre-accept state for rollback.
    for (const auto& fi : s->fileImpacts)
    {
        RollbackEntry entry;
        entry.suggestionId   = id;
        entry.filePath       = fi.filePath;
        entry.originalContent = fi.hunks.empty() ? "" : fi.hunks[0].before;
        m_rollbackHistory.push_back(entry);
    }

    s->status = ESuggestionStatus::Accepted;
    if (m_acceptCb) m_acceptCb(id, s->fileImpacts);
    return true;
}

bool DiffReviewPanel::RejectSuggestion(const std::string& id)
{
    AISuggestion* s = GetMutable(id);
    if (!s || s->status != ESuggestionStatus::Pending) return false;
    s->status = ESuggestionStatus::Rejected;
    return true;
}

bool DiffReviewPanel::RollbackSuggestion(const std::string& id)
{
    AISuggestion* s = GetMutable(id);
    if (!s || s->status != ESuggestionStatus::Accepted) return false;

    // Remove rollback entries for this suggestion.
    m_rollbackHistory.erase(
        std::remove_if(m_rollbackHistory.begin(), m_rollbackHistory.end(),
                       [&](const RollbackEntry& e){ return e.suggestionId == id; }),
        m_rollbackHistory.end());

    s->status = ESuggestionStatus::RolledBack;
    if (m_rollbackCb) m_rollbackCb(id);
    return true;
}

void DiffReviewPanel::SetSelected(const std::string& id)
{
    m_selectedId = id;
}

void DiffReviewPanel::ClearSelected()
{
    m_selectedId.clear();
}

std::optional<AISuggestion> DiffReviewPanel::GetSelected() const
{
    return FindSuggestion(m_selectedId);
}

std::vector<AISuggestion> DiffReviewPanel::GetPending() const
{
    std::vector<AISuggestion> result;
    for (const auto& s : m_suggestions)
        if (s.status == ESuggestionStatus::Pending) result.push_back(s);
    return result;
}

std::vector<AISuggestion> DiffReviewPanel::GetAccepted() const
{
    std::vector<AISuggestion> result;
    for (const auto& s : m_suggestions)
        if (s.status == ESuggestionStatus::Accepted) result.push_back(s);
    return result;
}

std::vector<AISuggestion> DiffReviewPanel::GetRejected() const
{
    std::vector<AISuggestion> result;
    for (const auto& s : m_suggestions)
        if (s.status == ESuggestionStatus::Rejected) result.push_back(s);
    return result;
}

std::optional<AISuggestion> DiffReviewPanel::FindSuggestion(const std::string& id) const
{
    for (const auto& s : m_suggestions)
        if (s.suggestionId == id) return s;
    return std::nullopt;
}

void DiffReviewPanel::SetContextObject(const std::string& objectId)
{
    m_contextObject = objectId;
}

std::vector<AISuggestion> DiffReviewPanel::GetSuggestionsForContext(
    const std::string& objectId) const
{
    std::vector<AISuggestion> result;
    for (const auto& s : m_suggestions)
        if (s.contextObjectId == objectId) result.push_back(s);
    return result;
}

std::vector<ArchRuleWarning> DiffReviewPanel::GetAllWarnings() const
{
    std::vector<ArchRuleWarning> result;
    for (const auto& s : m_suggestions)
        if (s.status == ESuggestionStatus::Pending)
            for (const auto& w : s.archWarnings)
                result.push_back(w);
    return result;
}

size_t DiffReviewPanel::PendingCount() const
{
    size_t c = 0;
    for (const auto& s : m_suggestions)
        if (s.status == ESuggestionStatus::Pending) ++c;
    return c;
}

size_t DiffReviewPanel::AcceptedCount() const
{
    size_t c = 0;
    for (const auto& s : m_suggestions)
        if (s.status == ESuggestionStatus::Accepted) ++c;
    return c;
}

AISuggestion* DiffReviewPanel::GetMutable(const std::string& id)
{
    for (auto& s : m_suggestions)
        if (s.suggestionId == id) return &s;
    return nullptr;
}

} // namespace atlas::editor::ai
