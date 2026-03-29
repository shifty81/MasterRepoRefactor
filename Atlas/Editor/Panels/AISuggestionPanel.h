#pragma once
#include <string>

namespace Atlas::Editor {

/// Phase 17A — Dev AI Phase 3: AI suggestion (diff+confirm) panel.
/// Displays a unified diff of the AI-proposed change and
/// lets the developer approve or reject before patching.
class AISuggestionPanel {
public:
    void LoadSuggestion(const std::string& diffText);
    bool Approve();
    bool Reject();
    void Clear();

    bool HasPendingSuggestion() const { return !m_diffText.empty(); }
    const std::string& GetDiffText() const { return m_diffText; }

private:
    std::string m_diffText;
    bool m_approved{false};
};

} // namespace Atlas::Editor
