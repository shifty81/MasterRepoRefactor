#pragma once
#include "ITool.h"
#include <string>
#include <vector>

namespace Atlas::Editor {

/// P3 Tool — Snapshot and rollback PCG generation state.
class PCGSnapshotManager : public ITool {
public:
    struct Snapshot {
        std::string id;
        std::string label;
        int revision{0};
    };

    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "PCGSnapshotManager"; }
    bool IsActive() const override { return m_active; }

    void CaptureSnapshot(const std::string& label);
    bool RestoreSnapshot(const std::string& snapshotId);
    void DeleteSnapshot(const std::string& snapshotId);
    const std::vector<Snapshot>& GetSnapshots() const { return m_snapshots; }
    int GetSnapshotCount() const { return static_cast<int>(m_snapshots.size()); }

private:
    bool m_active{false};
    int m_revisionCounter{0};
    std::vector<Snapshot> m_snapshots;
};

} // namespace Atlas::Editor
