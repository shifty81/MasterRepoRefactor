#pragma once

#include "Input/EditorInputTypes.h"
#include <string>
#include <vector>

class EditorInputRouter
{
public:
    bool Initialize();
    EditorInputFrame BuildFrame(const std::vector<std::string>& Keys, float YawDelta, float PitchDelta) const;
};
