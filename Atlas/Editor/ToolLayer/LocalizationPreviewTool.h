#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P25 Tool — In-editor localization string preview, language switching, and string table diff.
class LocalizationPreviewTool : public ITool {
public:
    enum class PreviewLanguage { English, French, German, Spanish, Japanese, Chinese, Korean, Custom };
    enum class StringTableState { Draft, Review, Approved, Deprecated, Missing, Custom };
    enum class DiffMode { Added, Removed, Changed, All, Custom };
    enum class PreviewRenderMode { Inline, Overlay, Popup, Custom };

    struct LocalizedStringPreview {
        std::string previewId;
        std::string stringKey;
        PreviewLanguage language{PreviewLanguage::English};
        std::string displayText;
        StringTableState state{StringTableState::Draft};
        bool rtl{false};
        bool hasPlaceholders{false};
    };

    struct StringTableDiffEntry {
        std::string diffId;
        std::string stringKey;
        DiffMode diffMode{DiffMode::Changed};
        std::string oldValue;
        std::string newValue;
        PreviewLanguage language{PreviewLanguage::English};
    };

    struct PreviewOverrideConfig {
        std::string overrideId;
        PreviewLanguage language{PreviewLanguage::English};
        PreviewRenderMode renderMode{PreviewRenderMode::Inline};
        float fontScale{1.0f};
        bool showKeys{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "LocalizationPreviewTool"; }
    bool IsActive() const override { return m_active; }

    bool AddStringPreview(const LocalizedStringPreview& preview);
    bool RemoveStringPreview(const std::string& previewId);
    const LocalizedStringPreview* GetStringPreview(const std::string& previewId) const;
    std::vector<std::string> GetAllPreviewIds() const;
    std::vector<std::string> GetPreviewsByLanguage(PreviewLanguage language) const;
    std::vector<std::string> GetPreviewsByState(StringTableState state) const;
    bool AddDiffEntry(const StringTableDiffEntry& entry);
    bool RemoveDiffEntry(const std::string& diffId);
    const StringTableDiffEntry* GetDiffEntry(const std::string& diffId) const;
    std::vector<std::string> GetAllDiffIds() const;
    std::vector<std::string> GetDiffsByMode(DiffMode mode) const;
    bool SetOverrideConfig(const PreviewOverrideConfig& config);
    const PreviewOverrideConfig* GetOverrideConfig(const std::string& overrideId) const;
    std::vector<std::string> GetAllOverrideIds() const;
    bool SwitchLanguage(PreviewLanguage language);
    PreviewLanguage GetActiveLanguage() const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, LocalizedStringPreview> m_previews;
    std::unordered_map<std::string, StringTableDiffEntry> m_diffEntries;
    std::unordered_map<std::string, PreviewOverrideConfig> m_overrideConfigs;
    PreviewLanguage m_activeLanguage{PreviewLanguage::English};
};

} // namespace Atlas::Editor
