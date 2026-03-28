// SceneManager.h
// Atlas Engine — scene manager: singleton-ish façade for loading, unloading,
// and querying the active scene graph.

#pragma once
#include "Scene/SceneGraph.h"

#include <memory>
#include <string>

namespace atlas::engine::scene {

// ---------------------------------------------------------------------------
// SceneManager
// ---------------------------------------------------------------------------

class SceneManager
{
public:
    // ---- singleton access ------------------------------------------------
    static SceneManager& GetInstance();

    // Non-copyable, non-movable singleton
    SceneManager(const SceneManager&)            = delete;
    SceneManager& operator=(const SceneManager&) = delete;
    SceneManager(SceneManager&&)                 = delete;
    SceneManager& operator=(SceneManager&&)      = delete;

    // ---- lifecycle -------------------------------------------------------
    bool Initialize();
    void Shutdown();

    // ---- scene load/unload -----------------------------------------------

    /// Creates (or replaces) the active scene graph and marks it as loaded.
    bool LoadScene(const std::string& sceneName);

    /// Destroys the active scene graph.
    void UnloadScene();

    bool IsSceneLoaded() const { return m_sceneLoaded; }
    const std::string& GetActiveSceneName() const { return m_activeSceneName; }

    // ---- graph access ----------------------------------------------------
    SceneGraph*       GetActiveGraph();
    const SceneGraph* GetActiveGraph() const;

    // ---- per-frame update ------------------------------------------------
    void Tick(float deltaSeconds);

private:
    SceneManager()  = default;
    ~SceneManager() = default;

    std::unique_ptr<SceneGraph> m_activeGraph;
    std::string                 m_activeSceneName;
    bool                        m_sceneLoaded = false;
};

} // namespace atlas::engine::scene
