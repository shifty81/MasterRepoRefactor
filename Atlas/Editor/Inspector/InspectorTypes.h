#pragma once

#include <string>
#include <vector>

struct InspectorField
{
    std::string Name;
    std::string Value;
};

struct InspectorState
{
    std::string SelectedId;
    std::string SelectedType;
    std::vector<InspectorField> Fields;
};
