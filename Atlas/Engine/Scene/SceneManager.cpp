// SceneManager.cpp
// Atlas Engine — scene manager implementation.

#include "Scene/SceneManager.h"

namespace atlas::engine::scene {

// ---- singleton -------------------------------------------------------------

SceneManager& SceneManager::GetInstance()
{
    static SceneManager instance;
    return instance;
}

// ---- lifecycle -------------------------------------------------------------

bool SceneManager::Initialize()
{
    m_sceneLoaded     = false;
    m_activeSceneName.clear();
    m_activeGraph.reset();
    return true;
}

void SceneManager::Shutdown()
{
    UnloadScene();
}

// ---- scene load/unload -----------------------------------------------------

bool SceneManager::LoadScene(const std::string& sceneName)
{
    UnloadScene();

    m_activeGraph = std::make_unique<SceneGraph>();
    if (!m_activeGraph->Initialize())
    {
        m_activeGraph.reset();
        return false;
    }

    m_activeSceneName = sceneName;
    m_sceneLoaded     = true;
    return true;
}

void SceneManager::UnloadScene()
{
    if (m_activeGraph)
    {
        m_activeGraph->Shutdown();
        m_activeGraph.reset();
    }
    m_activeSceneName.clear();
    m_sceneLoaded = false;
}

// ---- graph access ----------------------------------------------------------

SceneGraph* SceneManager::GetActiveGraph()
{
    return m_activeGraph.get();
}

const SceneGraph* SceneManager::GetActiveGraph() const
{
    return m_activeGraph.get();
}

// ---- per-frame update ------------------------------------------------------

void SceneManager::Tick(float deltaSeconds)
{
    if (m_sceneLoaded && m_activeGraph)
        m_activeGraph->Tick(deltaSeconds);
}

} // namespace atlas::engine::scene
