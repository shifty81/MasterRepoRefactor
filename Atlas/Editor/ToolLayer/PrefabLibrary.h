#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P0 Tool — Drag-and-drop reusable prefab modules.
class PrefabLibrary : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "PrefabLibrary"; }
    bool IsActive() const override { return m_active; }

    void RegisterPrefab(const std::string& name, const std::string& assetPath);
    bool SpawnPrefab(const std::string& name, float x, float y, float z);
    const std::vector<std::string>& GetPrefabNames() const { return m_prefabNames; }
    int GetPrefabCount() const { return static_cast<int>(m_prefabNames.size()); }

private:
    bool m_active{false};
    std::vector<std::string> m_prefabNames;
};

} // namespace Atlas::Editor
