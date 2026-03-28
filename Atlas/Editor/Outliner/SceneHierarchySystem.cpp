// SceneHierarchySystem.cpp
// Atlas Editor — full scene hierarchy management.

#include "Outliner/SceneHierarchySystem.h"

#include <algorithm>

namespace atlas::editor::outliner {

bool SceneHierarchySystem::Initialize() { return true; }
void SceneHierarchySystem::Shutdown()   { m_nodes.clear(); }

bool SceneHierarchySystem::AddNode(const HierarchyNode& node)
{
    if (m_nodes.count(node.nodeId)) return false; // duplicate
    m_nodes[node.nodeId] = node;

    // Register this node as a child of its parent.
    if (!node.parentNodeId.empty())
    {
        HierarchyNode* parent = GetMutable(node.parentNodeId);
        if (parent)
            parent->childNodeIds.push_back(node.nodeId);
    }
    return true;
}

bool SceneHierarchySystem::RemoveNode(const std::string& nodeId)
{
    auto it = m_nodes.find(nodeId);
    if (it == m_nodes.end()) return false;

    // Detach from parent.
    if (!it->second.parentNodeId.empty())
    {
        HierarchyNode* parent = GetMutable(it->second.parentNodeId);
        if (parent)
        {
            auto& v = parent->childNodeIds;
            v.erase(std::remove(v.begin(), v.end(), nodeId), v.end());
        }
    }
    m_nodes.erase(it);
    return true;
}

bool SceneHierarchySystem::ReparentNode(const std::string& nodeId,
                                         const std::string& newParentId)
{
    HierarchyNode* node = GetMutable(nodeId);
    if (!node) return false;

    // Remove from old parent.
    if (!node->parentNodeId.empty())
    {
        HierarchyNode* oldParent = GetMutable(node->parentNodeId);
        if (oldParent)
        {
            auto& v = oldParent->childNodeIds;
            v.erase(std::remove(v.begin(), v.end(), nodeId), v.end());
        }
    }

    node->parentNodeId = newParentId;

    // Register under new parent.
    if (!newParentId.empty())
    {
        HierarchyNode* newParent = GetMutable(newParentId);
        if (newParent)
            newParent->childNodeIds.push_back(nodeId);
    }
    return true;
}

bool SceneHierarchySystem::SetTransform(const std::string& nodeId,
                                         float px, float py, float pz,
                                         float rx, float ry, float rz,
                                         float sx, float sy, float sz)
{
    HierarchyNode* node = GetMutable(nodeId);
    if (!node || node->isLocked) return false;

    node->posX = px; node->posY = py; node->posZ = pz;
    node->rotX = rx; node->rotY = ry; node->rotZ = rz;
    node->scaleX = sx; node->scaleY = sy; node->scaleZ = sz;

    if (m_transformCb) m_transformCb(nodeId, px, py, pz, rx, ry, rz, sx, sy, sz);
    return true;
}

bool SceneHierarchySystem::ResetTransform(const std::string& nodeId)
{
    return SetTransform(nodeId,
                        0.f, 0.f, 0.f,
                        0.f, 0.f, 0.f,
                        1.f, 1.f, 1.f);
}

bool SceneHierarchySystem::AddComponent(const std::string& nodeId,
                                         const ComponentSummaryEntry& entry)
{
    HierarchyNode* node = GetMutable(nodeId);
    if (!node) return false;
    node->components.push_back(entry);
    return true;
}

bool SceneHierarchySystem::SetComponentActive(const std::string& nodeId,
                                               const std::string& componentType,
                                               bool active)
{
    HierarchyNode* node = GetMutable(nodeId);
    if (!node) return false;
    for (auto& c : node->components)
    {
        if (c.componentType == componentType)
        {
            c.isActive = active;
            return true;
        }
    }
    return false;
}

std::string SceneHierarchySystem::CreateFolder(const std::string& label,
                                                const std::string& parentId)
{
    HierarchyNode folder;
    folder.nodeId       = "folder_" + std::to_string(m_folderCounter++);
    folder.displayLabel = label;
    folder.type         = ENodeType::Folder;
    folder.parentNodeId = parentId;
    AddNode(folder);
    return folder.nodeId;
}

bool SceneHierarchySystem::GroupIntoFolder(const std::vector<std::string>& nodeIds,
                                            const std::string& folderId)
{
    bool allOk = true;
    for (const auto& id : nodeIds)
        if (!ReparentNode(id, folderId)) allOk = false;
    return allOk;
}

bool SceneHierarchySystem::SetVisible(const std::string& nodeId, bool visible)
{
    HierarchyNode* node = GetMutable(nodeId);
    if (!node) return false;
    node->isVisible = visible;
    return true;
}

bool SceneHierarchySystem::SetLocked(const std::string& nodeId, bool locked)
{
    HierarchyNode* node = GetMutable(nodeId);
    if (!node) return false;
    node->isLocked = locked;
    return true;
}

bool SceneHierarchySystem::SetProperty(const std::string& nodeId,
                                        const std::string& propertyName,
                                        const std::string& value)
{
    if (!m_nodes.count(nodeId)) return false;
    if (m_propertyCb) m_propertyCb(nodeId, propertyName, value);
    return true;
}

std::optional<const HierarchyNode*>
SceneHierarchySystem::FindNode(const std::string& nodeId) const
{
    auto it = m_nodes.find(nodeId);
    if (it == m_nodes.end()) return std::nullopt;
    return &it->second;
}

std::vector<const HierarchyNode*> SceneHierarchySystem::ListRootNodes() const
{
    std::vector<const HierarchyNode*> result;
    for (const auto& [id, node] : m_nodes)
        if (node.parentNodeId.empty()) result.push_back(&node);
    return result;
}

std::vector<const HierarchyNode*>
SceneHierarchySystem::ListChildren(const std::string& parentId) const
{
    std::vector<const HierarchyNode*> result;
    for (const auto& [id, node] : m_nodes)
        if (node.parentNodeId == parentId) result.push_back(&node);
    return result;
}

std::vector<const HierarchyNode*>
SceneHierarchySystem::ListByType(ENodeType type) const
{
    std::vector<const HierarchyNode*> result;
    for (const auto& [id, node] : m_nodes)
        if (node.type == type) result.push_back(&node);
    return result;
}

std::vector<const HierarchyNode*> SceneHierarchySystem::FlatList() const
{
    std::vector<const HierarchyNode*> result;
    result.reserve(m_nodes.size());
    for (const auto& [id, node] : m_nodes)
        result.push_back(&node);
    return result;
}

HierarchyNode* SceneHierarchySystem::GetMutable(const std::string& nodeId)
{
    auto it = m_nodes.find(nodeId);
    return (it != m_nodes.end()) ? &it->second : nullptr;
}

} // namespace atlas::editor::outliner
