#pragma once
#include "ITool.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Atlas::Editor {

/// P28 Tool — Blueprint comment block authoring, grouping, color coding, and doc-gen.
class BlueprintCommentTool : public ITool {
public:
    enum class CommentType { Info, Warning, Todo, Section, Divider, Custom };
    enum class CommentColor { White, Yellow, Red, Green, Blue, Cyan, Magenta, Orange, Custom };
    enum class CommentStyle { Bubble, Box, Arrow, Banner, Custom };
    enum class CommentScope { Local, Graph, Class, Package, Custom };

    struct CommentBlockDef {
        std::string commentId;
        std::string commentText;
        CommentType commentType{CommentType::Info};
        CommentColor color{CommentColor::Yellow};
        CommentStyle style{CommentStyle::Box};
        CommentScope scope{CommentScope::Graph};
        std::string graphId;
        float posX{0.0f};
        float posY{0.0f};
        float width{200.0f};
        float height{60.0f};
        float fontSize{10.0f};
        bool enabled{true};
    };

    struct CommentGroupDef {
        std::string groupId;
        std::string groupName;
        std::string graphId;
        CommentColor groupColor{CommentColor::Blue};
        float posX{0.0f};
        float posY{0.0f};
        float width{400.0f};
        float height{300.0f};
        bool collapseContents{false};
        bool enabled{true};
    };

    struct DocAnnotationDef {
        std::string annotationId;
        std::string commentId;
        std::string docText;
        std::string author;
        std::string dateStr;
        bool isDeprecated{false};
        bool exported{false};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "BlueprintCommentTool"; }
    bool IsActive() const override { return m_active; }

    bool CreateComment(const CommentBlockDef& def);
    bool DeleteComment(const std::string& commentId);
    bool EnableComment(const std::string& commentId, bool enabled);
    bool SetCommentType(const std::string& commentId, CommentType type);
    bool SetCommentColor(const std::string& commentId, CommentColor color);
    bool MoveComment(const std::string& commentId, float x, float y);
    const CommentBlockDef* GetComment(const std::string& commentId) const;
    std::vector<std::string> GetAllCommentIds() const;
    std::vector<std::string> GetCommentsByGraph(const std::string& graphId) const;
    std::vector<std::string> GetCommentsByType(CommentType type) const;
    std::vector<std::string> GetCommentsByColor(CommentColor color) const;
    bool CreateGroup(const CommentGroupDef& def);
    bool DeleteGroup(const std::string& groupId);
    bool AddCommentToGroup(const std::string& groupId, const std::string& commentId);
    bool RemoveCommentFromGroup(const std::string& groupId, const std::string& commentId);
    const CommentGroupDef* GetGroup(const std::string& groupId) const;
    std::vector<std::string> GetGroupsByGraph(const std::string& graphId) const;
    bool AddDocAnnotation(const std::string& commentId, const DocAnnotationDef& def);
    bool RemoveDocAnnotation(const std::string& annotationId);
    bool ExportDocAnnotation(const std::string& annotationId);
    const DocAnnotationDef* GetDocAnnotation(const std::string& annotationId) const;
    std::vector<std::string> GetDocAnnotationsByComment(const std::string& commentId) const;
    std::vector<std::string> GetExportedAnnotations() const;
    void Reset();

private:
    bool m_active{false};
    std::unordered_map<std::string, CommentBlockDef> m_comments;
    std::unordered_map<std::string, CommentGroupDef> m_groups;
    std::unordered_map<std::string, DocAnnotationDef> m_docAnnotations;
};

} // namespace Atlas::Editor
