#include "Input/EditorInputRouter.h"

bool EditorInputRouter::Initialize()
{
    return true;
}

EditorInputFrame EditorInputRouter::BuildFrame(const std::vector<std::string>& Keys, float YawDelta, float PitchDelta) const
{
    auto has = [&](const char* k)
    {
        for (const auto& key : Keys)
        {
            if (key == k) return true;
        }
        return false;
    };

    EditorInputFrame Frame;
    Frame.ToggleEditorMode = has("F12");
    Frame.SelectPressed = has("LMB");
    Frame.MoveToolPressed = has("W_KEY");
    Frame.RotateToolPressed = has("E_KEY");
    Frame.ScaleToolPressed = has("R_KEY");
    Frame.ToggleSnap = has("G");
    Frame.ToggleLocalWorld = has("L");
    Frame.CameraForward = has("W");
    Frame.CameraBackward = has("S");
    Frame.CameraLeft = has("A");
    Frame.CameraRight = has("D");
    Frame.CameraUp = has("Q");
    Frame.CameraDown = has("Z");
    Frame.LookYawDelta = YawDelta;
    Frame.LookPitchDelta = PitchDelta;
    return Frame;
}
