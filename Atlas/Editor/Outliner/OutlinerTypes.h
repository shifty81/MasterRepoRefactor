#pragma once

#include <string>
#include <vector>

struct OutlinerNode
{
    std::string Id;
    std::string Label;
    std::string ParentId;
    std::string Type;
};

struct SceneOutlinerState
{
    std::vector<OutlinerNode> Nodes;
};
