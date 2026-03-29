#pragma once
#include "ITool.h"
#include <string>

namespace Atlas::Editor {

/// P1 Tool — Inverse kinematics for characters and turrets.
class IKRigTool : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "IKRigTool"; }
    bool IsActive() const override { return m_active; }

    void SetRigTarget(const std::string& boneName, float x, float y, float z);
    void SetMaxIterations(int iterations);
    int GetMaxIterations() const { return m_maxIterations; }
    void SolveIK();

private:
    bool m_active{false};
    int m_maxIterations{10};
};

} // namespace Atlas::Editor
