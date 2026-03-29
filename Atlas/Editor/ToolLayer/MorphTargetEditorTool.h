#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P24 Tool — Morph target authoring, blend weight management, and corrective shape sculpting.
class MorphTargetEditorTool : public ITool {
public:
    enum class MorphBlendMode { Additive, Override, Weighted, Clamped, Custom };
    enum class MorphTargetScope { Character, Vehicle, Prop, Environment, Custom };
    enum class CorrectiveMode { None, Automatic, Manual, Delta, Custom };
    enum class MorphPreviewMode { Rest, Animated, Blended, Isolated, Custom };

    struct MorphTargetDef {
        std::string morphId;
        std::string morphName;
        MorphTargetScope scope{MorphTargetScope::Character};
        float defaultWeight{0.0f};
        float minWeight{0.0f};
        float maxWeight{1.0f};
    };

    struct CorrectiveShapeDef {
        std::string correctiveId;
        std::string morphId;
        CorrectiveMode mode{CorrectiveMode::Automatic};
        std::string triggerExpr;
        float threshold{0.5f};
    };

    struct MorphBlendPreset {
        std::string presetId;
        std::string presetName;
        MorphBlendMode blendMode{MorphBlendMode::Additive};
        std::vector<std::string> morphIds;
        std::vector<float> weights;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MorphTargetEditorTool"; }
    bool IsActive() const override { return m_active; }

    bool RegisterMorph(const MorphTargetDef& def);
    bool UnregisterMorph(const std::string& morphId);
    const MorphTargetDef* GetMorph(const std::string& morphId) const;
    std::vector<std::string> GetAllMorphIds() const;
    std::vector<std::string> GetMorphsByScope(MorphTargetScope scope) const;
    bool SetBlendWeight(const std::string& morphId, float weight);
    float GetBlendWeight(const std::string& morphId) const;
    bool AddCorrective(const std::string& morphId, const CorrectiveShapeDef& corrective);
    bool RemoveCorrective(const std::string& morphId, const std::string& correctiveId);
    const CorrectiveShapeDef* GetCorrective(const std::string& correctiveId) const;
    std::vector<std::string> GetCorrectivesByMorph(const std::string& morphId) const;
    std::string CreatePreset(const MorphBlendPreset& preset);
    bool DeletePreset(const std::string& presetId);
    const MorphBlendPreset* GetPreset(const std::string& presetId) const;
    std::vector<std::string> GetAllPresetIds() const;
    bool ApplyPreset(const std::string& presetId);
    void ResetWeights();
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, MorphTargetDef> m_morphs;
    std::unordered_map<std::string, CorrectiveShapeDef> m_correctives;
    std::unordered_map<std::string, MorphBlendPreset> m_presets;
    std::unordered_map<std::string, float> m_blendWeights;
};

} // namespace Atlas::Editor
