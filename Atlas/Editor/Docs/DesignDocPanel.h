// DesignDocPanel.h
// Atlas Editor — design doc panel: links documentation pages to live
// systems, data records, and editor objects.

#pragma once
#include <functional>
#include <optional>
#include <string>
#include <vector>

namespace atlas::editor::docs {

// ---------------------------------------------------------------------------
// Link from doc section to a code/data/system target
// ---------------------------------------------------------------------------

enum class EDocLinkType : uint8_t
{
    CppHeader,    ///< link to a .h file
    DataRecord,   ///< link to a data registry entry
    EditorObject, ///< link to a scene / hierarchy object
    Feature,      ///< link to a feature checklist item
    ExternalURL,
};

struct DocLink
{
    EDocLinkType type       = EDocLinkType::CppHeader;
    std::string  label;
    std::string  target;    ///< file path, record id, URL, etc.
    std::string  sectionAnchor; ///< optional anchor within target
};

// ---------------------------------------------------------------------------
// A single design doc page
// ---------------------------------------------------------------------------

struct DesignDocPage
{
    std::string          pageId;
    std::string          title;
    std::string          category;   ///< Gameplay, Systems, Art, UI, etc.
    std::string          markdownPath;  ///< relative path to the .md file
    std::string          summary;       ///< one-liner pulled from file
    std::vector<DocLink> links;
    bool                 isOpen     = false;
    bool                 isDirty    = false;  ///< unsaved edits
};

// ---------------------------------------------------------------------------
// DesignDocPanel
// ---------------------------------------------------------------------------

class DesignDocPanel
{
public:
    bool Initialize();
    void Shutdown();

    // ---- page registry ------------------------------------------------
    void RegisterPage     (const DesignDocPage& page);
    bool UnregisterPage   (const std::string& pageId);
    bool HasPage          (const std::string& pageId) const;
    std::optional<DesignDocPage> FindPage(const std::string& pageId) const;

    // ---- list / search ------------------------------------------------
    std::vector<DesignDocPage> ListAll()                     const { return m_pages; }
    std::vector<DesignDocPage> ListByCategory(const std::string& cat) const;
    std::vector<DesignDocPage> Search(const std::string& query)       const;

    // ---- open / close (panel tabs) ------------------------------------
    void OpenPage (const std::string& pageId);
    void ClosePage(const std::string& pageId);
    bool IsOpen   (const std::string& pageId) const;
    std::vector<std::string> GetOpenPageIds() const;

    // ---- links management --------------------------------------------
    bool AddLink   (const std::string& pageId, const DocLink& link);
    bool RemoveLink(const std::string& pageId, const std::string& linkLabel);
    std::vector<DocLink> GetLinksForPage(const std::string& pageId) const;

    // ---- navigate-to callback ----------------------------------------
    using NavigateCallback = std::function<void(const DocLink&)>;
    void SetNavigateCallback(NavigateCallback cb) { m_navCb = std::move(cb); }
    void NavigateTo(const DocLink& link);

    // ---- dirty tracking ----------------------------------------------
    void MarkDirty(const std::string& pageId);
    void MarkClean(const std::string& pageId);

    size_t PageCount() const { return m_pages.size(); }

private:
    std::vector<DesignDocPage> m_pages;
    NavigateCallback           m_navCb;

    DesignDocPage* GetMutable(const std::string& pageId);
};

} // namespace atlas::editor::docs
