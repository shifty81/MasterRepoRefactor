#pragma once
#include <string>

namespace Atlas::Editor {

/// Base interface for all Atlas editor tools.
/// All 32 ITool implementations must inherit from this class.
class ITool {
public:
    virtual ~ITool() = default;

    virtual void Activate() = 0;
    virtual void Deactivate() = 0;
    virtual void Update(float deltaTime) = 0;
    virtual void OnMouseDown(int button, float x, float y) = 0;
    virtual void OnMouseUp(int button, float x, float y) = 0;
    virtual void OnKeyDown(int keyCode) = 0;
    virtual std::string GetToolName() const = 0;
    virtual bool IsActive() const = 0;
};

} // namespace Atlas::Editor
