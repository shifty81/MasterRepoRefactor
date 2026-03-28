// ADLPanel.h
// Atlas Editor — Architecture Decision Log panel: record/browse/link ADL
// entries to affected systems, data types, and editor objects.

#pragma once
#include <functional>
#include <optional>
#include <string>
#include <vector>

namespace atlas::editor::docs {

enum class EADLStatus : uint8_t
{
    Proposed,
    Accepted,
    Deprecated,
    Superseded,
};

struct ADLContextLink
{
    std::string type;    ///< "System", "DataRecord", "File", etc.
    std::string target;  ///< system ID, file path, data record ID
};

struct ADLEntry
{
    std::string              entryId;
    std::string              title;
    std::string              context;        ///< problem statement
    std::string              decision;       ///< chosen approach
    std::string              consequences;   ///< trade-offs
    EADLStatus               status         = EADLStatus::Proposed;
    std::string              date;           ///< ISO-8601 date string
    std::string              author;
    std::vector<ADLContextLink> contextLinks;  ///< linked systems/data
    std::string              supersededById;   ///< if Superseded
};

class ADLPanel
{
public:
    bool Initialize();
    void Shutdown();

    // ---- entry management ---------------------------------------------
    void AddEntry   (const ADLEntry& entry);
    bool RemoveEntry(const std::string& entryId);
    bool HasEntry   (const std::string& entryId) const;
    bool UpdateEntry(const ADLEntry& entry);

    // ---- status -------------------------------------------------------
    bool SetStatus(const std::string& entryId, EADLStatus status);
    bool Supersede(const std::string& entryId,
                    const std::string& supersededById);

    // ---- queries -------------------------------------------------------
    std::optional<ADLEntry>    FindEntry  (const std::string& entryId) const;
    std::vector<ADLEntry>      ListAll    ()                           const;
    std::vector<ADLEntry>      ListByStatus(EADLStatus status)         const;
    std::vector<ADLEntry>      Search     (const std::string& query)   const;
    std::vector<ADLEntry>      LinkedTo   (const std::string& target)  const;

    // ---- context links ------------------------------------------------
    bool AddContextLink   (const std::string& entryId,
                            const ADLContextLink& link);
    bool RemoveContextLink(const std::string& entryId,
                            const std::string& target);

    // ---- navigate callback --------------------------------------------
    using NavigateCallback = std::function<void(const ADLContextLink&)>;
    void SetNavigateCallback(NavigateCallback cb) { m_navCb = std::move(cb); }
    void NavigateTo(const ADLContextLink& link);

    size_t EntryCount()   const { return m_entries.size(); }
    size_t AcceptedCount() const;

private:
    std::vector<ADLEntry> m_entries;
    NavigateCallback      m_navCb;

    ADLEntry* GetMutable(const std::string& entryId);
};

} // namespace atlas::editor::docs
