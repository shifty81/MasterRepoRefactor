#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P15 Tool — Material instance authoring, parameter overrides, and variant management.
class MaterialInstanceTool : public ITool {
public:
    enum class ParameterType { Scalar, Vector, Texture, Color, Boolean, Integer };
    enum class MaterialDomain { Surface, Deferred, Unlit, Postprocess, UI, Custom };
    enum class BlendMode { Opaque, Translucent, Masked, Additive, Modulate };

    struct ParameterOverride {
        std::string paramId;
        std::string paramName;
        ParameterType paramType{ParameterType::Scalar};
        float scalarValue{0.0f};
        float vectorValueX{0.0f};
        float vectorValueY{0.0f};
        float vectorValueZ{0.0f};
        float vectorValueW{0.0f};
        std::string textureRef;
    };

    struct MaterialInstanceDef {
        std::string instanceId;
        std::string name;
        std::string baseMaterialPath;
        MaterialDomain domain{MaterialDomain::Surface};
        BlendMode blendMode{BlendMode::Opaque};
        std::vector<std::string> overrides;
    };

    struct MaterialVariant {
        std::string variantId;
        std::string name;
        std::vector<std::string> overrides;
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MaterialInstanceTool"; }
    bool IsActive() const override { return m_active; }

    // Instance management
    std::string CreateInstance(const std::string& name, const std::string& baseMaterialPath);
    bool RemoveInstance(const std::string& instanceId);
    bool AddOverride(const std::string& instanceId, const ParameterOverride& param);
    bool RemoveOverride(const std::string& instanceId, const std::string& paramId);

    // Variant management
    std::string CreateVariant(const std::string& instanceId, const std::string& variantName);
    bool RemoveVariant(const std::string& variantId);

    // Parameter setters
    bool SetScalarParam(const std::string& instanceId, const std::string& paramName, float value);
    bool SetVectorParam(const std::string& instanceId, const std::string& paramName,
                        float x, float y, float z, float w);
    bool SetTextureParam(const std::string& instanceId, const std::string& paramName,
                         const std::string& textureRef);

    // Apply and preview
    bool ApplyVariant(const std::string& instanceId, const std::string& variantId);
    bool ValidateInstance(const std::string& instanceId) const;
    bool PreviewInstance(const std::string& instanceId) const;

    // Queries
    const MaterialInstanceDef* GetInstance(const std::string& instanceId) const;
    std::vector<std::string> GetAllInstanceIds() const;
    std::vector<std::string> GetInstanceVariants(const std::string& instanceId) const;

    // Persistence
    bool SaveInstances(const std::string& filePath) const;
    bool LoadInstances(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, MaterialInstanceDef> m_instances;
    std::unordered_map<std::string, ParameterOverride> m_overrides;
    std::unordered_map<std::string, MaterialVariant> m_variants;
    int m_nextInstanceIndex{0};
    int m_nextVariantIndex{0};
};

} // namespace Atlas::Editor
