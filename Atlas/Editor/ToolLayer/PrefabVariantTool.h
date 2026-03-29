#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P6 Tool — Create, manage, and override prefab variants with per-instance deltas.
class PrefabVariantTool : public ITool {
public:
    struct VariantOverride {
        std::string property;
        std::string value;
    };

    struct PrefabVariant {
        std::string variantId;
        std::string basePrefabId;
        std::string variantName;
        std::vector<VariantOverride> overrides;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "PrefabVariantTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateVariant(const std::string& basePrefabId,
                              const std::string& variantName);
    bool RemoveVariant(const std::string& variantId);
    bool AddOverride(const std::string& variantId,
                     const std::string& property, const std::string& value);
    bool RemoveOverride(const std::string& variantId, const std::string& property);
    bool ClearOverrides(const std::string& variantId);
    const PrefabVariant* GetVariant(const std::string& variantId) const;
    std::vector<std::string> GetVariantsForPrefab(const std::string& basePrefabId) const;
    int GetVariantCount() const { return static_cast<int>(m_variants.size()); }
    void RegisterBasePrefab(const std::string& prefabId);
    int GetBasePrefabCount() const { return static_cast<int>(m_basePrefabs.size()); }

private:
    bool m_active{false};
    std::vector<PrefabVariant> m_variants;
    std::vector<std::string> m_basePrefabs;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
