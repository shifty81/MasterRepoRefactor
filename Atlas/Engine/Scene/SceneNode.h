// SceneNode.h
// Atlas Engine — scene graph node: identity, type, transform, flags, and
// parent/child hierarchy.

#pragma once
#include "Scene/SceneTypes.h"

#include <memory>
#include <string>
#include <vector>

namespace atlas::engine::scene {

// ---------------------------------------------------------------------------
// SceneNode
// ---------------------------------------------------------------------------

class SceneNode
{
public:
    explicit SceneNode(SceneNodeId id,
                       ESceneNodeType type,
                       std::string name);
    ~SceneNode() = default;

    // Non-copyable, movable
    SceneNode(const SceneNode&)            = delete;
    SceneNode& operator=(const SceneNode&) = delete;
    SceneNode(SceneNode&&)                 = default;
    SceneNode& operator=(SceneNode&&)      = default;

    // ---- identity --------------------------------------------------------
    SceneNodeId     GetId()   const { return m_id; }
    ESceneNodeType  GetType() const { return m_type; }
    const std::string& GetName() const { return m_name; }
    void               SetName(std::string name) { m_name = std::move(name); }

    // ---- transform -------------------------------------------------------
    const SceneTransform& GetTransform() const { return m_transform; }
    void                  SetTransform(const SceneTransform& t) { m_transform = t; }

    // ---- flags -----------------------------------------------------------
    SceneNodeFlags GetFlags() const { return m_flags; }
    void           SetFlags(SceneNodeFlags flags) { m_flags = flags; }
    void           AddFlags(SceneNodeFlags flags) { m_flags |= flags; }
    void           ClearFlags(SceneNodeFlags flags) { m_flags &= ~flags; }
    bool           HasFlags(SceneNodeFlags flags) const { return (m_flags & flags) == flags; }

    // ---- visibility convenience ------------------------------------------
    bool IsVisible() const;
    void SetVisible(bool visible);

    // ---- hierarchy -------------------------------------------------------
    SceneNode* GetParent() const { return m_parent; }

    const std::vector<std::unique_ptr<SceneNode>>& GetChildren() const { return m_children; }

    /// Takes ownership of child and sets its parent pointer.
    SceneNode* AddChild(std::unique_ptr<SceneNode> child);

    /// Removes and returns the child with the given id (nullptr if not found).
    std::unique_ptr<SceneNode> RemoveChild(SceneNodeId childId);

    /// Returns first child matching id (searches recursively).
    SceneNode* FindChild(SceneNodeId id);
    const SceneNode* FindChild(SceneNodeId id) const;

    size_t ChildCount() const { return m_children.size(); }

private:
    SceneNodeId    m_id;
    ESceneNodeType m_type;
    std::string    m_name;
    SceneTransform m_transform;
    SceneNodeFlags m_flags  = NodeFlags::Defaults;
    SceneNode*     m_parent = nullptr;

    std::vector<std::unique_ptr<SceneNode>> m_children;
};

} // namespace atlas::engine::scene
