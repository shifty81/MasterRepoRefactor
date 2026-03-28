// SceneGraph.h
// Atlas Engine — scene graph: owns root nodes, allocates node IDs, provides
// creation/destruction/lookup, and drives per-frame tick.

#pragma once
#include "Scene/SceneNode.h"

#include <memory>
#include <string>
#include <vector>

namespace atlas::engine::scene {

// ---------------------------------------------------------------------------
// SceneGraph
// ---------------------------------------------------------------------------

class SceneGraph
{
public:
    SceneGraph()  = default;
    ~SceneGraph() = default;

    SceneGraph(const SceneGraph&)            = delete;
    SceneGraph& operator=(const SceneGraph&) = delete;
    SceneGraph(SceneGraph&&)                 = default;
    SceneGraph& operator=(SceneGraph&&)      = default;

    // ---- lifecycle -------------------------------------------------------
    bool Initialize();
    void Shutdown();

    // ---- node factory ----------------------------------------------------

    /// Creates a root-level node owned by the graph and returns a raw pointer.
    SceneNode* CreateNode(ESceneNodeType type, std::string name);

    /// Creates a child node under the given parent.
    SceneNode* CreateChildNode(SceneNodeId parentId,
                                ESceneNodeType type,
                                std::string name);

    /// Destroys any node (root or child) by id. Returns false if not found.
    bool DestroyNode(SceneNodeId id);

    // ---- lookup ----------------------------------------------------------
    SceneNode*       FindNode(SceneNodeId id);
    const SceneNode* FindNode(SceneNodeId id) const;

    /// Returns first node whose name matches (case-sensitive, first hit).
    SceneNode*       FindNodeByName(const std::string& name);
    const SceneNode* FindNodeByName(const std::string& name) const;

    // ---- root access -----------------------------------------------------
    const std::vector<std::unique_ptr<SceneNode>>& GetRoots() const { return m_roots; }
    size_t RootCount() const { return m_roots.size(); }

    // ---- per-frame update ------------------------------------------------
    void Tick(float deltaSeconds);

    // ---- stats -----------------------------------------------------------
    size_t TotalNodeCount() const;

private:
    std::vector<std::unique_ptr<SceneNode>> m_roots;
    SceneNodeId m_nextId = 1;

    SceneNodeId AllocId() { return m_nextId++; }

    // Recursive helpers
    static SceneNode*       FindInSubtree(SceneNode* root, SceneNodeId id);
    static SceneNode*       FindByNameInSubtree(SceneNode* root, const std::string& name);
    static const SceneNode* FindByNameInSubtree(const SceneNode* root, const std::string& name);
    static size_t           CountSubtree(const SceneNode* root);
    static bool             DestroyInSubtree(SceneNode* root, SceneNodeId id);
};

} // namespace atlas::engine::scene
