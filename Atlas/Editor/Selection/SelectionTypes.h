#pragma once

#include <string>

enum class ESelectionTargetType
{
    None,
    Entity,
    Structure,
    Module,
    VoxelChunk
};

struct SelectionHandle
{
    ESelectionTargetType Type = ESelectionTargetType::None;
    std::string Id;
    bool IsValid() const { return Type != ESelectionTargetType::None && !Id.empty(); }
};
