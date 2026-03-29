#pragma once
#include "ITool.h"
#include <string>

namespace Atlas::Editor {

/// P1 Tool — Edit materials and live-compile GLSL shaders.
class MaterialShaderTool : public ITool {
public:
    void Activate() override;
    void Deactivate() override;
    void Update(float deltaTime) override;
    void OnMouseDown(int button, float x, float y) override;
    void OnMouseUp(int button, float x, float y) override;
    void OnKeyDown(int keyCode) override;
    std::string GetToolName() const override { return "MaterialShaderTool"; }
    bool IsActive() const override { return m_active; }

    void LoadMaterial(const std::string& materialPath);
    void SetShaderSource(const std::string& glslSource);
    bool CompileShader();
    bool ApplyToEntity(const std::string& entityId);
    bool HasCompileError() const { return m_hasCompileError; }

private:
    bool m_active{false};
    bool m_hasCompileError{false};
    std::string m_currentMaterial;
};

} // namespace Atlas::Editor
