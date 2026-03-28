// SceneGraph.cpp
// Atlas Engine — scene graph implementation.

#include "Scene/SceneGraph.h"

#include <algorithm>
#include <numeric>

namespace atlas::engine::scene {

// ---- lifecycle -------------------------------------------------------------

bool SceneGraph::Initialize()
{
    m_roots.clear();
    m_nextId = 1;
    return true;
}

void SceneGraph::Shutdown()
{
    m_roots.clear();
    m_nextId = 1;
}

// ---- node factory ----------------------------------------------------------

SceneNode* SceneGraph::CreateNode(ESceneNodeType type, std::string name)
{
    auto node = std::make_unique<SceneNode>(AllocId(), type, std::move(name));
    m_roots.push_back(std::move(node));
    return m_roots.back().get();
}

SceneNode* SceneGraph::CreateChildNode(SceneNodeId parentId,
                                        ESceneNodeType type,
                                        std::string name)
{
    SceneNode* parent = FindNode(parentId);
    if (!parent) return nullptr;

    auto child = std::make_unique<SceneNode>(AllocId(), type, std::move(name));
    return parent->AddChild(std::move(child));
}

bool SceneGraph::DestroyNode(SceneNodeId id)
{
    // Check root nodes first
    auto it = std::find_if(m_roots.begin(), m_roots.end(),
        [id](const std::unique_ptr<SceneNode>& n){ return n->GetId() == id; });

    if (it != m_roots.end())
    {
        m_roots.erase(it);
        return true;
    }

    // Search children of each root
    for (auto& root : m_roots)
    {
        if (DestroyInSubtree(root.get(), id))
            return true;
    }
    return false;
}

// ---- lookup ----------------------------------------------------------------

SceneNode* SceneGraph::FindNode(SceneNodeId id)
{
    for (auto& root : m_roots)
    {
        if (root->GetId() == id) return root.get();
        if (SceneNode* found = FindInSubtree(root.get(), id)) return found;
    }
    return nullptr;
}

const SceneNode* SceneGraph::FindNode(SceneNodeId id) const
{
    for (const auto& root : m_roots)
    {
        if (root->GetId() == id) return root.get();
        if (const SceneNode* found = root->FindChild(id)) return found;
    }
    return nullptr;
}

SceneNode* SceneGraph::FindNodeByName(const std::string& name)
{
    for (auto& root : m_roots)
    {
        if (root->GetName() == name) return root.get();
        if (SceneNode* found = FindByNameInSubtree(root.get(), name)) return found;
    }
    return nullptr;
}

const SceneNode* SceneGraph::FindNodeByName(const std::string& name) const
{
    for (const auto& root : m_roots)
    {
        if (root->GetName() == name) return root.get();
        if (const SceneNode* found = FindByNameInSubtree(root.get(), name)) return found;
    }
    return nullptr;
}

// ---- per-frame update ------------------------------------------------------

void SceneGraph::Tick(float /*deltaSeconds*/)
{
    // Placeholder: traverse dirty transforms, evaluate animations, etc.
}

// ---- stats -----------------------------------------------------------------

size_t SceneGraph::TotalNodeCount() const
{
    size_t count = 0;
    for (const auto& root : m_roots)
        count += CountSubtree(root.get());
    return count;
}

// ---- private helpers -------------------------------------------------------

SceneNode* SceneGraph::FindInSubtree(SceneNode* root, SceneNodeId id)
{
    for (const auto& child : root->GetChildren())
    {
        if (child->GetId() == id) return child.get();
        if (SceneNode* found = FindInSubtree(child.get(), id)) return found;
    }
    return nullptr;
}

SceneNode* SceneGraph::FindByNameInSubtree(SceneNode* root, const std::string& name)
{
    for (const auto& child : root->GetChildren())
    {
        if (child->GetName() == name) return child.get();
        if (SceneNode* found = FindByNameInSubtree(child.get(), name)) return found;
    }
    return nullptr;
}

const SceneNode* SceneGraph::FindByNameInSubtree(const SceneNode* root, const std::string& name)
{
    for (const auto& child : root->GetChildren())
    {
        if (child->GetName() == name) return child.get();
        if (const SceneNode* found = FindByNameInSubtree(child.get(), name)) return found;
    }
    return nullptr;
}

size_t SceneGraph::CountSubtree(const SceneNode* root)
{
    size_t count = 1; // count self
    for (const auto& child : root->GetChildren())
        count += CountSubtree(child.get());
    return count;
}

bool SceneGraph::DestroyInSubtree(SceneNode* root, SceneNodeId id)
{
    auto removed = root->RemoveChild(id);
    if (removed) return true;

    for (const auto& child : root->GetChildren())
    {
        if (DestroyInSubtree(child.get(), id))
            return true;
    }
    return false;
}

} // namespace atlas::engine::scene
