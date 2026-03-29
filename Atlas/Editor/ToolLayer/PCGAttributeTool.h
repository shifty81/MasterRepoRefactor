#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P22 Tool — PCG attribute set and custom attribute management.
class PCGAttributeTool : public ITool {
public:
    enum class AttributeType { Boolean, Integer, Float, Vector, String, Transform, Object, Custom };
    enum class AttributeScope { Node, Graph, Component, Actor, World, Custom };
    enum class AttributeInheritance { None, Parent, Root, Hierarchical, Override, Custom };
    enum class AttributeBlendMode { Replace, Add, Multiply, Lerp, Min, Max, Custom };

    struct PCGAttributeDef {
        std::string attributeId;
        std::string attributeName;
        AttributeType attributeType{AttributeType::Float};
        AttributeScope scope{AttributeScope::Node};
        AttributeInheritance inheritance{AttributeInheritance::None};
        std::string defaultValue;
        bool readOnly{false};
        bool serializable{true};
    };

    struct AttributeSetDef {
        std::string setId;
        std::string name;
        std::string ownerNodeId;
        std::vector<std::string> attributeIds;
        bool allowDuplicates{false};
        bool locked{false};
    };

    struct AttributeOverrideDef {
        std::string overrideId;
        std::string targetAttributeId;
        std::string overrideValue;
        AttributeBlendMode blendMode{AttributeBlendMode::Replace};
        float blendWeight{1.0f};
        bool enabled{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "PCGAttributeTool"; }
    bool IsActive() const override { return m_active; }

    std::string RegisterAttribute(const PCGAttributeDef& def);
    bool UnregisterAttribute(const std::string& attributeId);
    const PCGAttributeDef* GetAttribute(const std::string& attributeId) const;
    std::vector<std::string> GetAllAttributeIds() const;

    std::string CreateAttributeSet(const AttributeSetDef& def);
    bool DeleteAttributeSet(const std::string& setId);
    const AttributeSetDef* GetAttributeSet(const std::string& setId) const;
    std::vector<std::string> GetAllSetIds() const;

    bool AddAttributeToSet(const std::string& setId, const std::string& attributeId);
    bool RemoveAttributeFromSet(const std::string& setId, const std::string& attributeId);

    bool AddOverride(const AttributeOverrideDef& override_);
    bool RemoveOverride(const std::string& overrideId);
    std::vector<AttributeOverrideDef> GetOverridesByAttribute(const std::string& attributeId) const;

    std::vector<std::string> GetAttributesByType(AttributeType type) const;
    std::vector<std::string> GetAttributesByScope(AttributeScope scope) const;

    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, PCGAttributeDef> m_attributes;
    std::unordered_map<std::string, AttributeSetDef> m_attributeSets;
    std::unordered_map<std::string, AttributeOverrideDef> m_overrides;
    int m_nextIndex{0};
};

} // namespace Atlas::Editor
