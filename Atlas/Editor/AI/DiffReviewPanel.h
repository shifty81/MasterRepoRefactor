// DiffReviewPanel.h
// Atlas Editor / AtlasAI — AI suggestion diff review panel: accept/reject/rollback,
// file impact preview, and architecture-rule warnings.

#pragma once
#include <functional>
#include <optional>
#include <string>
#include <vector>

namespace atlas::editor::ai {

// ---------------------------------------------------------------------------
// Diff hunk (one block of changed lines)
// ---------------------------------------------------------------------------

struct DiffHunk
{
    int32_t     startLine   = 0;
    int32_t     lineCount   = 0;
    std::string before;    ///< original text
    std::string after;     ///< proposed text
};

// ---------------------------------------------------------------------------
// File impact entry — one file affected by a suggestion
// ---------------------------------------------------------------------------

struct FileImpactEntry
{
    std::string filePath;
    int32_t     linesAdded   = 0;
    int32_t     linesRemoved = 0;
    bool        isNewFile    = false;
    bool        isDeleted    = false;
    std::vector<DiffHunk> hunks;
};

// ---------------------------------------------------------------------------
// Architecture rule warning
// ---------------------------------------------------------------------------

enum class EArchRuleLevel : uint8_t { Info, Warning, Violation };

struct ArchRuleWarning
{
    std::string       ruleId;
    std::string       description;
    EArchRuleLevel    level       = EArchRuleLevel::Warning;
    std::string       affectedFile;
    int32_t           affectedLine = -1;
};

// ---------------------------------------------------------------------------
// One AI suggestion (pending for review)
// ---------------------------------------------------------------------------

enum class ESuggestionStatus : uint8_t
{
    Pending,
    Accepted,
    Rejected,
    RolledBack,
};

struct AISuggestion
{
    std::string                  suggestionId;
    std::string                  title;
    std::string                  description;
    std::vector<FileImpactEntry> fileImpacts;
    std::vector<ArchRuleWarning> archWarnings;
    ESuggestionStatus            status       = ESuggestionStatus::Pending;
    std::string                  contextObjectId;  ///< linked editor object/file
    std::string                  aiReasoning;
};

// ---------------------------------------------------------------------------
// Rollback snapshot (pre-accept state)
// ---------------------------------------------------------------------------

struct RollbackEntry
{
    std::string        suggestionId;
    std::string        filePath;
    std::string        originalContent;
};

// ---------------------------------------------------------------------------
// DiffReviewPanel
// ---------------------------------------------------------------------------

class DiffReviewPanel
{
public:
    DiffReviewPanel()  = default;
    ~DiffReviewPanel() = default;

    bool Initialize();
    void Shutdown();

    // ---- suggestion management --------------------------------------
    void  SubmitSuggestion(const AISuggestion& suggestion);
    bool  AcceptSuggestion(const std::string& suggestionId);
    bool  RejectSuggestion(const std::string& suggestionId);
    bool  RollbackSuggestion(const std::string& suggestionId);

    // ---- selection --------------------------------------------------
    void  SetSelected(const std::string& suggestionId);
    void  ClearSelected();
    std::optional<AISuggestion> GetSelected() const;

    // ---- queries ----------------------------------------------------
    std::vector<AISuggestion> GetPending()   const;
    std::vector<AISuggestion> GetAccepted()  const;
    std::vector<AISuggestion> GetRejected()  const;
    std::optional<AISuggestion> FindSuggestion(const std::string& id) const;

    // ---- rollback history -------------------------------------------
    const std::vector<RollbackEntry>& GetRollbackHistory() const
    { return m_rollbackHistory; }

    // ---- context linkage --------------------------------------------
    void  SetContextObject(const std::string& objectId);
    std::vector<AISuggestion> GetSuggestionsForContext(
        const std::string& objectId) const;

    // ---- arch rule warnings -----------------------------------------
    std::vector<ArchRuleWarning> GetAllWarnings() const;

    // ---- callbacks --------------------------------------------------
    using AcceptCallback   = std::function<void(const std::string& suggestionId,
                                                  const std::vector<FileImpactEntry>&)>;
    using RollbackCallback = std::function<void(const std::string& suggestionId)>;

    void SetAcceptCallback  (AcceptCallback   cb) { m_acceptCb   = std::move(cb); }
    void SetRollbackCallback(RollbackCallback cb) { m_rollbackCb = std::move(cb); }

    size_t PendingCount()  const;
    size_t AcceptedCount() const;

private:
    std::vector<AISuggestion>   m_suggestions;
    std::vector<RollbackEntry>  m_rollbackHistory;
    std::string                 m_selectedId;
    std::string                 m_contextObject;
    AcceptCallback              m_acceptCb;
    RollbackCallback            m_rollbackCb;

    AISuggestion* GetMutable(const std::string& id);
};

} // namespace atlas::editor::ai
