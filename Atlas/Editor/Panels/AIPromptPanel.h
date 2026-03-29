#pragma once
#include <string>
#include <functional>

namespace Atlas::Editor {

/// Phase 17A — Dev AI Phase 3: AI prompt entry panel.
/// Provides a text input field for developer AI prompts,
/// dispatches to the AtlasAI bridge via EditorCommandBus.
class AIPromptPanel {
public:
    void SetPrompt(const std::string& text);
    void Submit();
    void Clear();
    void SetOnSubmitCallback(std::function<void(const std::string&)> cb);

    const std::string& GetCurrentPrompt() const { return m_prompt; }

private:
    std::string m_prompt;
    std::function<void(const std::string&)> m_onSubmit;
};

} // namespace Atlas::Editor
