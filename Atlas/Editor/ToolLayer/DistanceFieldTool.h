#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P27 Tool — Distance field mesh authoring, SDF visualization, and soft-shadow config.
class DistanceFieldTool : public ITool {
public:
    enum class FieldResolution { Low, Medium, High, Ultra, Custom };
    enum class FieldShape { Sphere, Box, Capsule, Cone, Torus, Mesh, Custom };
    enum class ShadowType { Hard, Soft, RayTraced, None, Custom };
    enum class FieldBlendMode { Union, Intersection, Subtraction, SmoothUnion, Custom };

    struct DistanceFieldDef {
        std::string fieldId;
        std::string fieldName;
        FieldShape shape{FieldShape::Sphere};
        FieldResolution resolution{FieldResolution::Medium};
        float posX{0.0f};
        float posY{0.0f};
        float posZ{0.0f};
        float scaleX{1.0f};
        float scaleY{1.0f};
        float scaleZ{1.0f};
        float blendRadius{0.0f};
        bool selfShadow{true};
        bool enabled{true};
    };

    struct ShadowConfigDef {
        std::string shadowConfigId;
        std::string fieldId;
        ShadowType shadowType{ShadowType::Soft};
        float penumbraAngle{3.0f};
        float shadowBias{0.01f};
        float maxDistance{5000.0f};
        float softnessFactor{1.0f};
        bool castShadow{true};
    };

    struct FieldBlendOpDef {
        std::string blendOpId;
        std::string fieldAId;
        std::string fieldBId;
        FieldBlendMode blendMode{FieldBlendMode::Union};
        float smoothK{0.1f};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "DistanceFieldTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateField(const DistanceFieldDef& def);
    bool DeleteField(const std::string& fieldId);
    bool EnableField(const std::string& fieldId, bool enabled);
    bool SetResolution(const std::string& fieldId, FieldResolution resolution);
    const DistanceFieldDef* GetField(const std::string& fieldId) const;
    std::vector<std::string> GetAllFieldIds() const;
    std::vector<std::string> GetFieldsByShape(FieldShape shape) const;
    std::vector<std::string> GetEnabledFields() const;
    bool AddShadowConfig(const std::string& fieldId, const ShadowConfigDef& config);
    bool RemoveShadowConfig(const std::string& fieldId, const std::string& shadowConfigId);
    bool SetShadowType(const std::string& shadowConfigId, ShadowType type);
    const ShadowConfigDef* GetShadowConfig(const std::string& shadowConfigId) const;
    std::vector<std::string> GetShadowConfigsByField(const std::string& fieldId) const;
    bool CreateBlendOp(const FieldBlendOpDef& blendOp);
    bool DeleteBlendOp(const std::string& blendOpId);
    const FieldBlendOpDef* GetBlendOp(const std::string& blendOpId) const;
    std::vector<std::string> GetAllBlendOpIds() const;
    std::vector<std::string> GetBlendOpsByMode(FieldBlendMode mode) const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, DistanceFieldDef> m_fields;
    std::unordered_map<std::string, ShadowConfigDef> m_shadowConfigs;
    std::unordered_map<std::string, FieldBlendOpDef> m_blendOps;
};

} // namespace Atlas::Editor
