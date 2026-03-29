#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P10 Tool — Character appearance and equipment customization tool.
class CharacterCustomizerTool : public ITool {
public:
    enum class SlotCategory { Head, Torso, Legs, Feet, Hands, Back, Accessory, Weapon };
    enum class MorphTarget { Body, Face, Height, Weight, Musculature, Custom };
    enum class ColorChannel { Primary, Secondary, Tertiary, Emissive, Subsurface };

    struct ColorSwatch {
        std::string swatchId;
        std::string name;
        float r{1.0f};
        float g{1.0f};
        float b{1.0f};
        float a{1.0f};
        float roughness{0.5f};
        float metallic{0.0f};
    };

    struct EquipSlot {
        std::string slotId;
        std::string name;
        SlotCategory category{SlotCategory::Torso};
        std::string equippedMeshId;
        std::string equippedMaterialId;
        bool visible{true};
        bool locked{false};
    };

    struct MorphWeight {
        std::string morphId;
        MorphTarget target{MorphTarget::Body};
        float weight{0.0f};
        float minValue{-1.0f};
        float maxValue{1.0f};
    };

    struct CharacterPreset {
        std::string presetId;
        std::string name;
        std::string baseMeshId;
        std::vector<EquipSlot> slots;
        std::vector<MorphWeight> morphs;
        std::unordered_map<std::string, ColorSwatch> colorChannels;
        std::string thumbnailPath;
        bool isBasePreset{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "CharacterCustomizerTool"; }
    bool IsActive() const override { return m_active; }

    // Preset management
    std::string CreatePreset(const std::string& name, const std::string& baseMeshId);
    bool RemovePreset(const std::string& presetId);
    bool DuplicatePreset(const std::string& srcPresetId, const std::string& newName);
    bool SetBaseMesh(const std::string& presetId, const std::string& meshId);
    bool SetThumbnail(const std::string& presetId, const std::string& path);
    int GetPresetCount() const { return static_cast<int>(m_presets.size()); }
    const CharacterPreset* GetPreset(const std::string& presetId) const;
    std::vector<std::string> GetPresetIds() const;

    // Slot management
    std::string AddSlot(const std::string& presetId, const std::string& name,
                         SlotCategory category);
    bool RemoveSlot(const std::string& presetId, const std::string& slotId);
    bool EquipMesh(const std::string& presetId, const std::string& slotId,
                    const std::string& meshId);
    bool EquipMaterial(const std::string& presetId, const std::string& slotId,
                        const std::string& materialId);
    bool SetSlotVisible(const std::string& presetId, const std::string& slotId,
                         bool visible);
    bool SetSlotLocked(const std::string& presetId, const std::string& slotId,
                        bool locked);
    int GetSlotCount(const std::string& presetId) const;

    // Morph management
    std::string AddMorph(const std::string& presetId, MorphTarget target,
                          float weight = 0.0f);
    bool SetMorphWeight(const std::string& presetId, const std::string& morphId,
                         float weight);
    bool SetMorphRange(const std::string& presetId, const std::string& morphId,
                        float minVal, float maxVal);
    int GetMorphCount(const std::string& presetId) const;

    // Color
    bool SetColorChannel(const std::string& presetId, ColorChannel channel,
                          float r, float g, float b, float a = 1.0f,
                          float roughness = 0.5f, float metallic = 0.0f);
    const ColorSwatch* GetColorChannel(const std::string& presetId,
                                        ColorChannel channel) const;

    // Persistence
    bool SavePreset(const std::string& presetId, const std::string& filePath) const;
    bool LoadPreset(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, CharacterPreset> m_presets;
    int m_nextPresetIndex{0};
    int m_nextSlotIndex{0};
    int m_nextMorphIndex{0};
};

} // namespace Atlas::Editor
