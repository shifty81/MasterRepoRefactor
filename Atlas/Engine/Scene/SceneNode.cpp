// SceneNode.cpp
// Atlas Engine — scene graph node implementation.

#include "Scene/SceneNode.h"

#include <algorithm>

namespace atlas::engine::scene {

SceneNode::SceneNode(SceneNodeId id, ESceneNodeType type, std::string name)
    : m_id(id), m_type(type), m_name(std::move(name))
{}

// ---- visibility ----------------------------------------------------------

bool SceneNode::IsVisible() const
{
    return HasFlags(NodeFlags::Visible) && !HasFlags(NodeFlags::Hidden);
}

void SceneNode::SetVisible(bool visible)
{
    if (visible)
    {
        AddFlags(NodeFlags::Visible);
        ClearFlags(NodeFlags::Hidden);
    }
    else
    {
        AddFlags(NodeFlags::Hidden);
        ClearFlags(NodeFlags::Visible);
    }
}

// ---- hierarchy -----------------------------------------------------------

SceneNode* SceneNode::AddChild(std::unique_ptr<SceneNode> child)
{
    if (!child) return nullptr;
    child->m_parent = this;
    m_children.push_back(std::move(child));
    return m_children.back().get();
}

std::unique_ptr<SceneNode> SceneNode::RemoveChild(SceneNodeId childId)
{
    auto it = std::find_if(m_children.begin(), m_children.end(),
        [childId](const std::unique_ptr<SceneNode>& n){ return n->GetId() == childId; });

    if (it == m_children.end()) return nullptr;

    (*it)->m_parent = nullptr;
    auto removed = std::move(*it);
    m_children.erase(it);
    return removed;
}

SceneNode* SceneNode::FindChild(SceneNodeId id)
{
    for (auto& child : m_children)
    {
        if (child->m_id == id) return child.get();
        if (SceneNode* found = child->FindChild(id)) return found;
    }
    return nullptr;
}

const SceneNode* SceneNode::FindChild(SceneNodeId id) const
{
    for (const auto& child : m_children)
    {
        if (child->m_id == id) return child.get();
        if (const SceneNode* found = child->FindChild(id)) return found;
    }
    return nullptr;
}

} // namespace atlas::engine::scene
