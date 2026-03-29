#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P14 Tool — Localization editor with locale management, translation tracking, and glossary
class LocalizationEditorTool : public ITool {
public:
    enum class LocaleStatus { Pending, Translated, Reviewed, Approved };
    enum class TextCategory { UI, Subtitle, Dialogue, Lore, Quest };

    struct LocaleEntry {
        std::string entryId;
        std::string key;
        std::string sourceText;
        TextCategory category{TextCategory::UI};
        bool pluralizable{false};
        std::string context;
    };

    struct TranslationRecord {
        std::string recordId;
        std::string entryId;
        std::string locale;
        std::string translatedText;
        LocaleStatus status{LocaleStatus::Pending};
        std::string translatorId;
        std::string reviewerId;
    };

    struct GlossaryTerm {
        std::string termId;
        std::string term;
        std::string definition;
        std::unordered_map<std::string, std::string> translations;
        bool doNotTranslate{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "LocalizationEditorTool"; }
    bool IsActive() const override { return m_active; }

    std::string AddLocale(const std::string& localeCode);
    bool RemoveLocale(const std::string& localeCode);
    bool SetLocaleActive(const std::string& localeCode, bool active);

    std::string AddEntry(const std::string& key, const std::string& sourceText, TextCategory category = TextCategory::UI);
    bool RemoveEntry(const std::string& entryId);
    bool SetEntryContext(const std::string& entryId, const std::string& context);

    bool SetTranslation(const std::string& entryId, const std::string& locale, const std::string& text);
    bool SetTranslationStatus(const std::string& recordId, LocaleStatus status);
    bool SetTranslator(const std::string& recordId, const std::string& translatorId);
    bool ApproveTranslation(const std::string& recordId);

    std::string AddGlossaryTerm(const std::string& term, const std::string& definition);
    bool RemoveGlossaryTerm(const std::string& termId);
    bool SetGlossaryTranslation(const std::string& termId, const std::string& locale, const std::string& translation);

    int GetEntryCount() const;
    const LocaleEntry* GetEntry(const std::string& entryId) const;
    std::vector<std::string> GetEntryIds() const;
    std::vector<std::string> GetEntriesByCategory(TextCategory category) const;
    std::vector<std::string> GetMissingTranslations(const std::string& locale) const;
    std::vector<std::string> GetLocales() const;
    int GetTranslationProgress(const std::string& locale) const;

    bool ImportTranslations(const std::string& filePath, const std::string& locale);
    bool ExportTranslations(const std::string& locale, const std::string& filePath) const;
    bool ExportAllTranslations(const std::string& directory) const;

    bool SaveLocalizationData(const std::string& filePath) const;
    bool LoadLocalizationData(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, LocaleEntry> m_entries;
    std::unordered_map<std::string, TranslationRecord> m_translations;
    std::unordered_map<std::string, GlossaryTerm> m_glossary;
    std::vector<std::string> m_locales;
    int m_nextEntryIndex{0};
    int m_nextRecordIndex{0};
    int m_nextTermIndex{0};
};

} // namespace Atlas::Editor
