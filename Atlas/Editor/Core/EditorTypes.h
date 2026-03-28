#pragma once

#include <string>

enum class EEditorMode
{
    Game,
    Editor
};

enum class EEditorToolMode
{
    None,
    Select,
    Move,
    Rotate,
    Scale
};

struct EditorSessionState
{
    EEditorMode Mode = EEditorMode::Game;
    EEditorToolMode ToolMode = EEditorToolMode::Select;
    bool bGridSnapEnabled = true;
    bool bLocalTransformMode = false;
};
