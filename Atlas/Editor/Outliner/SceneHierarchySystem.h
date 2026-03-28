// SceneHierarchySystem.h
// Atlas Editor — full scene hierarchy management with grouping, transform editing,
// and edit callbacks.

#pragma once
#include "Outliner/HierarchyNode.h"

#include <functional>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

namespace atlas::editor::outliner {

/// Callback fired when a node's transform is changed through the inspector.
using TransformEditCallback =
    std::function<void(const std::string& nodeId,
                       float px, float py, float pz,
                       float rx, float ry, float rz,
                       float sx, float sy, float sz)>;

/// Callback fired when a node property (non-transform) is changed.
using PropertyEditCallback =
    std::function<void(const std::string& nodeId,
                       const std::string& propertyName,
                       const std::string& newValue)>;

class SceneHierarchySystem
{
public:
    bool Initialize();
    void Shutdown();

    // ---- node lifecycle -----------------------------------------------
    bool AddNode(const HierarchyNode& node);
    bool RemoveNode(const std::string& nodeId);
    bool ReparentNode(const std::string& nodeId,
                      const std::string& newParentId);

    // ---- transform editing -------------------------------------------
    bool SetTransform(const std::string& nodeId,
                      float px, float py, float pz,
                      float rx, float ry, float rz,
                      float sx, float sy, float sz);

    bool ResetTransform(const std::string& nodeId);

    // ---- component management ----------------------------------------
    bool AddComponent(const std::string& nodeId,
                      const ComponentSummaryEntry& entry);
    bool SetComponentActive(const std::string& nodeId,
                            const std::string& componentType,
                            bool active);

    // ---- grouping / folders ------------------------------------------
    /// Create a folder node and return its ID.
    std::string CreateFolder(const std::string& label,
                             const std::string& parentId = "");
    /// Move multiple nodes into a folder.
    bool GroupIntoFolder(const std::vector<std::string>& nodeIds,
                         const std::string& folderId);

    // ---- visibility / lock -------------------------------------------
    bool SetVisible(const std::string& nodeId, bool visible);
    bool SetLocked(const std::string& nodeId, bool locked);

    // ---- property edit -----------------------------------------------
    bool SetProperty(const std::string& nodeId,
                     const std::string& propertyName,
                     const std::string& value);

    // ---- callbacks ---------------------------------------------------
    void SetTransformEditCallback(TransformEditCallback cb)
    { m_transformCb = std::move(cb); }
    void SetPropertyEditCallback(PropertyEditCallback cb)
    { m_propertyCb  = std::move(cb); }

    // ---- queries -----------------------------------------------------
    std::optional<const HierarchyNode*> FindNode(const std::string& nodeId) const;
    std::vector<const HierarchyNode*>   ListRootNodes()  const;
    std::vector<const HierarchyNode*>   ListChildren(const std::string& parentId) const;
    std::vector<const HierarchyNode*>   ListByType(ENodeType type) const;
    std::vector<const HierarchyNode*>   FlatList() const;

private:
    std::unordered_map<std::string, HierarchyNode> m_nodes;
    TransformEditCallback m_transformCb;
    PropertyEditCallback  m_propertyCb;
    uint32_t m_folderCounter = 0;

    HierarchyNode* GetMutable(const std::string& nodeId);
};

} // namespace atlas::editor::outliner
