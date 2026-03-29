#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P2 Tool — Spawn AI/PCG assets into the scene.
class NPCSpawnerTool : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "NPCSpawnerTool"; }
    bool IsActive() const override { return m_active; }

    void SetSpawnTemplate(const std::string& templateName);
    void SetSpawnCount(int count);
    void SetSpawnRadius(float radius);
    void SpawnAt(float x, float y, float z);
    void DespawnAll();

    const std::string& GetSpawnTemplate() const { return m_spawnTemplate; }
    int GetSpawnCount() const { return m_spawnCount; }
    int GetSpawnedEntityCount() const { return static_cast<int>(m_spawnedIds.size()); }

private:
    bool m_active{false};
    std::string m_spawnTemplate;
    int m_spawnCount{1};
    float m_spawnRadius{10.0f};
    std::vector<std::string> m_spawnedIds;
};

} // namespace Atlas::Editor
