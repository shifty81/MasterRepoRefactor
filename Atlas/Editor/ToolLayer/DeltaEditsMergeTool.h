#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P3 Tool — Merge and resolve conflicting DeltaEdits across sessions.
class DeltaEditsMergeTool : public ITool {
public:
    enum class ConflictResolution { KeepLocal, KeepRemote, Merge };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "DeltaEditsMergeTool"; }
    bool IsActive() const override { return m_active; }

    void LoadLocalEdits(const std::string& filePath);
    void LoadRemoteEdits(const std::string& filePath);
    void ResolveConflict(const std::string& conflictId, ConflictResolution resolution);
    bool Commit();

    int GetConflictCount() const { return m_conflictCount; }
    bool HasUnresolvedConflicts() const { return m_conflictCount > 0; }

private:
    bool m_active{false};
    int m_conflictCount{0};
};

} // namespace Atlas::Editor
