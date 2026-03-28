// FeatureChecklistPanel.cpp
// Atlas Editor — feature checklist panel.

#include "Docs/FeatureChecklistPanel.h"

#include <algorithm>

namespace atlas::editor::docs {

bool FeatureChecklistPanel::Initialize() { return true; }
void FeatureChecklistPanel::Shutdown()   { m_items.clear(); }

void FeatureChecklistPanel::RegisterItem(const FeatureItem& item)
{
    for (auto& i : m_items)
        if (i.itemId == item.itemId) { i = item; return; }
    m_items.push_back(item);
}

bool FeatureChecklistPanel::UnregisterItem(const std::string& itemId)
{
    auto it = std::find_if(m_items.begin(), m_items.end(),
                           [&](const FeatureItem& i){ return i.itemId == itemId; });
    if (it == m_items.end()) return false;
    m_items.erase(it);
    return true;
}

bool FeatureChecklistPanel::HasItem(const std::string& itemId) const
{
    return FindItem(itemId).has_value();
}

bool FeatureChecklistPanel::SetStatus(const std::string& itemId,
                                        EFeatureStatus status)
{
    FeatureItem* item = GetMutable(itemId);
    if (!item) return false;
    item->status = status;
    if (m_statusCb) m_statusCb(itemId, status);
    return true;
}

bool FeatureChecklistPanel::SetPriority(const std::string& itemId,
                                          EFeaturePriority priority)
{
    FeatureItem* item = GetMutable(itemId);
    if (!item) return false;
    item->priority = priority;
    return true;
}

bool FeatureChecklistPanel::SetOwner(const std::string& itemId,
                                       const std::string& owner)
{
    FeatureItem* item = GetMutable(itemId);
    if (!item) return false;
    item->ownerTag = owner;
    return true;
}

std::optional<FeatureItem> FeatureChecklistPanel::FindItem(
    const std::string& itemId) const
{
    for (const auto& i : m_items)
        if (i.itemId == itemId) return i;
    return std::nullopt;
}

std::vector<FeatureItem> FeatureChecklistPanel::ListByStatus(
    EFeatureStatus status) const
{
    std::vector<FeatureItem> result;
    for (const auto& i : m_items)
        if (i.status == status) result.push_back(i);
    return result;
}

std::vector<FeatureItem> FeatureChecklistPanel::ListByPriority(
    EFeaturePriority prio) const
{
    std::vector<FeatureItem> result;
    for (const auto& i : m_items)
        if (i.priority == prio) result.push_back(i);
    return result;
}

std::vector<FeatureItem> FeatureChecklistPanel::ListByMilestone(
    const std::string& tag) const
{
    std::vector<FeatureItem> result;
    for (const auto& i : m_items)
        if (i.milestoneTag == tag) result.push_back(i);
    return result;
}

std::vector<FeatureItem> FeatureChecklistPanel::ListBlocking() const
{
    std::vector<FeatureItem> result;
    for (const auto& i : m_items)
        if (i.isBlocking && i.status != EFeatureStatus::Complete)
            result.push_back(i);
    return result;
}

std::vector<FeatureItem> FeatureChecklistPanel::Filter(
    const FeatureChecklistFilter& f) const
{
    std::vector<FeatureItem> result;
    for (const auto& i : m_items)
    {
        if (f.filterByStatus && i.status != f.statusFilter) continue;
        if (f.filterByPrio   && i.priority != f.prioFilter) continue;
        if (!f.milestoneFilter.empty() && i.milestoneTag != f.milestoneFilter) continue;
        result.push_back(i);
    }
    return result;
}

size_t FeatureChecklistPanel::CompleteCount() const
{
    size_t c = 0;
    for (const auto& i : m_items)
        if (i.status == EFeatureStatus::Complete) ++c;
    return c;
}

size_t FeatureChecklistPanel::BlockedCount() const
{
    size_t c = 0;
    for (const auto& i : m_items)
        if (i.status == EFeatureStatus::Blocked) ++c;
    return c;
}

float FeatureChecklistPanel::CompletionPct() const
{
    if (m_items.empty()) return 0.f;
    return static_cast<float>(CompleteCount()) /
           static_cast<float>(m_items.size()) * 100.f;
}

FeatureItem* FeatureChecklistPanel::GetMutable(const std::string& itemId)
{
    for (auto& i : m_items)
        if (i.itemId == itemId) return &i;
    return nullptr;
}

} // namespace atlas::editor::docs
