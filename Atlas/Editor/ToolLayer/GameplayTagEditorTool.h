#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P14 Tool — Gameplay tag hierarchy editor with rule binding and scope management
class GameplayTagEditorTool : public ITool {
public:
    enum class TagScope { Global, Module, Level, Entity };
    enum class TagInheritMode { None, Single, Multi };

    struct TagHierarchyNode {
        std::string nodeId;
        std::string tag;
        std::string parentId;
        TagScope scope{TagScope::Global};
        TagInheritMode inheritMode{TagInheritMode::None};
        std::vector<std::string> childIds;
    };

    struct TagRule {
        std::string ruleId;
        std::string name;
        std::string sourceTag;
        std::string targetTag;
        bool exclusive{false};
        bool required{false};
    };

    struct TagBinding {
        std::string bindingId;
        std::string entityId;
        std::string tag;
        TagScope scope{TagScope::Global};
        bool active{true};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "GameplayTagEditorTool"; }
    bool IsActive() const override { return m_active; }

    std::string CreateTag(const std::string& name, TagScope scope = TagScope::Global);
    bool RemoveTag(const std::string& id);
    bool SetParentTag(const std::string& id, const std::string& parentId);
    bool SetTagScope(const std::string& id, TagScope scope);
    bool SetTagInheritMode(const std::string& id, TagInheritMode mode);

    std::string AddTagRule(const std::string& name, const std::string& sourceTag, const std::string& targetTag);
    bool RemoveTagRule(const std::string& ruleId);
    bool SetRuleExclusive(const std::string& ruleId, bool exclusive);

    std::string BindTag(const std::string& entityId, const std::string& tag, TagScope scope = TagScope::Global);
    bool UnbindTag(const std::string& bindingId);
    bool SetBindingActive(const std::string& bindingId, bool active);

    int GetTagCount() const;
    const TagHierarchyNode* GetTag(const std::string& id) const;
    std::vector<std::string> GetTagIds() const;
    std::vector<std::string> GetTagsByScope(TagScope scope) const;
    std::vector<std::string> GetTagTree(const std::string& rootId) const;
    std::vector<std::string> GetChildTags(const std::string& parentId) const;
    int GetRuleCount() const;
    const TagRule* GetRule(const std::string& ruleId) const;
    std::vector<std::string> GetRuleIds() const;
    int GetBindingCount() const;
    std::vector<std::string> GetBindingsForEntity(const std::string& entityId) const;

    bool SaveTagDatabase(const std::string& filePath) const;
    bool LoadTagDatabase(const std::string& filePath);
    void ClearAll();

private:
    bool m_active{false};
    std::unordered_map<std::string, TagHierarchyNode> m_tags;
    std::unordered_map<std::string, TagRule> m_rules;
    std::unordered_map<std::string, TagBinding> m_bindings;
    int m_nextTagIndex{0};
    int m_nextRuleIndex{0};
    int m_nextBindingIndex{0};
};

} // namespace Atlas::Editor
