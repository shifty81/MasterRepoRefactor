// DesignDocPanel.cpp
// Atlas Editor — design doc panel.

#include "Docs/DesignDocPanel.h"

#include <algorithm>

namespace atlas::editor::docs {

bool DesignDocPanel::Initialize() { return true; }
void DesignDocPanel::Shutdown()   { m_pages.clear(); }

void DesignDocPanel::RegisterPage(const DesignDocPage& page)
{
    for (auto& p : m_pages)
        if (p.pageId == page.pageId) { p = page; return; }
    m_pages.push_back(page);
}

bool DesignDocPanel::UnregisterPage(const std::string& pageId)
{
    auto it = std::find_if(m_pages.begin(), m_pages.end(),
                           [&](const DesignDocPage& p){ return p.pageId == pageId; });
    if (it == m_pages.end()) return false;
    m_pages.erase(it);
    return true;
}

bool DesignDocPanel::HasPage(const std::string& pageId) const
{
    return FindPage(pageId).has_value();
}

std::optional<DesignDocPage> DesignDocPanel::FindPage(const std::string& pageId) const
{
    for (const auto& p : m_pages)
        if (p.pageId == pageId) return p;
    return std::nullopt;
}

std::vector<DesignDocPage> DesignDocPanel::ListByCategory(const std::string& cat) const
{
    std::vector<DesignDocPage> result;
    for (const auto& p : m_pages)
        if (p.category == cat) result.push_back(p);
    return result;
}

std::vector<DesignDocPage> DesignDocPanel::Search(const std::string& query) const
{
    std::vector<DesignDocPage> result;
    for (const auto& p : m_pages)
    {
        if (p.title.find(query) != std::string::npos ||
            p.summary.find(query) != std::string::npos ||
            p.category.find(query) != std::string::npos)
            result.push_back(p);
    }
    return result;
}

void DesignDocPanel::OpenPage(const std::string& pageId)
{
    DesignDocPage* p = GetMutable(pageId);
    if (p) p->isOpen = true;
}

void DesignDocPanel::ClosePage(const std::string& pageId)
{
    DesignDocPage* p = GetMutable(pageId);
    if (p) p->isOpen = false;
}

bool DesignDocPanel::IsOpen(const std::string& pageId) const
{
    for (const auto& p : m_pages)
        if (p.pageId == pageId) return p.isOpen;
    return false;
}

std::vector<std::string> DesignDocPanel::GetOpenPageIds() const
{
    std::vector<std::string> ids;
    for (const auto& p : m_pages)
        if (p.isOpen) ids.push_back(p.pageId);
    return ids;
}

bool DesignDocPanel::AddLink(const std::string& pageId, const DocLink& link)
{
    DesignDocPage* p = GetMutable(pageId);
    if (!p) return false;
    p->links.push_back(link);
    p->isDirty = true;
    return true;
}

bool DesignDocPanel::RemoveLink(const std::string& pageId,
                                  const std::string& linkLabel)
{
    DesignDocPage* p = GetMutable(pageId);
    if (!p) return false;
    auto it = std::find_if(p->links.begin(), p->links.end(),
                           [&](const DocLink& l){ return l.label == linkLabel; });
    if (it == p->links.end()) return false;
    p->links.erase(it);
    p->isDirty = true;
    return true;
}

std::vector<DocLink> DesignDocPanel::GetLinksForPage(const std::string& pageId) const
{
    for (const auto& p : m_pages)
        if (p.pageId == pageId) return p.links;
    return {};
}

void DesignDocPanel::NavigateTo(const DocLink& link)
{
    if (m_navCb) m_navCb(link);
}

void DesignDocPanel::MarkDirty(const std::string& pageId)
{
    DesignDocPage* p = GetMutable(pageId);
    if (p) p->isDirty = true;
}

void DesignDocPanel::MarkClean(const std::string& pageId)
{
    DesignDocPage* p = GetMutable(pageId);
    if (p) p->isDirty = false;
}

DesignDocPage* DesignDocPanel::GetMutable(const std::string& pageId)
{
    for (auto& p : m_pages)
        if (p.pageId == pageId) return &p;
    return nullptr;
}

} // namespace atlas::editor::docs
