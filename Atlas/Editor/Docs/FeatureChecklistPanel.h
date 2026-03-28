// FeatureChecklistPanel.h
// Atlas Editor — feature checklist panel: live tracking of feature completion
// with linking to systems, owners, and priority tags.

#pragma once
#include <functional>
#include <optional>
#include <string>
#include <vector>

namespace atlas::editor::docs {

enum class EFeatureStatus : uint8_t
{
    NotStarted,
    InProgress,
    Complete,
    Blocked,
    Deferred,
};

enum class EFeaturePriority : uint8_t
{
    Critical,
    High,
    Medium,
    Low,
    Ice,          ///< on ice / future
};

struct FeatureItem
{
    std::string      itemId;
    std::string      title;
    std::string      description;
    EFeatureStatus   status       = EFeatureStatus::NotStarted;
    EFeaturePriority priority     = EFeaturePriority::Medium;
    std::string      ownerTag;        ///< team/person responsible
    std::string      linkedSystemId;  ///< C++ system or subsystem ID
    std::string      linkedPageId;    ///< design doc page
    std::string      milestoneTag;
    bool             isBlocking   = false;
};

struct FeatureChecklistFilter
{
    EFeatureStatus   statusFilter   = EFeatureStatus::NotStarted;
    bool             filterByStatus = false;
    EFeaturePriority prioFilter     = EFeaturePriority::High;
    bool             filterByPrio   = false;
    std::string      milestoneFilter;
};

class FeatureChecklistPanel
{
public:
    bool Initialize();
    void Shutdown();

    // ---- item management -----------------------------------------------
    void RegisterItem  (const FeatureItem& item);
    bool UnregisterItem(const std::string& itemId);
    bool HasItem       (const std::string& itemId) const;

    // ---- status updates ------------------------------------------------
    bool SetStatus  (const std::string& itemId, EFeatureStatus status);
    bool SetPriority(const std::string& itemId, EFeaturePriority priority);
    bool SetOwner   (const std::string& itemId, const std::string& owner);

    // ---- queries -------------------------------------------------------
    std::optional<FeatureItem>     FindItem      (const std::string& itemId) const;
    std::vector<FeatureItem>       ListAll()       const { return m_items; }
    std::vector<FeatureItem>       ListByStatus   (EFeatureStatus status)   const;
    std::vector<FeatureItem>       ListByPriority (EFeaturePriority prio)   const;
    std::vector<FeatureItem>       ListByMilestone(const std::string& tag)  const;
    std::vector<FeatureItem>       ListBlocking()  const;
    std::vector<FeatureItem>       Filter(const FeatureChecklistFilter& f)  const;

    // ---- progress stats -----------------------------------------------
    size_t TotalCount()    const { return m_items.size(); }
    size_t CompleteCount() const;
    size_t BlockedCount()  const;
    float  CompletionPct() const;

    // ---- change callback -----------------------------------------------
    using StatusChangedCallback = std::function<void(const std::string& itemId,
                                                       EFeatureStatus newStatus)>;
    void SetStatusChangedCallback(StatusChangedCallback cb)
    { m_statusCb = std::move(cb); }

    size_t ItemCount() const { return m_items.size(); }

private:
    std::vector<FeatureItem>   m_items;
    StatusChangedCallback      m_statusCb;

    FeatureItem* GetMutable(const std::string& itemId);
};

} // namespace atlas::editor::docs
