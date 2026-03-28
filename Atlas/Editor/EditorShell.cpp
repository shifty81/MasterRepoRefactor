#include "EditorShell.h"
#include <iostream>

bool EditorShell::Initialize()
{
    std::cout << "[EditorShell] Initialize\n";
    return true;
}

void EditorShell::Tick(float)
{
    std::cout << "[EditorShell] Tick\n";
}

void EditorShell::Shutdown()
{
    std::cout << "[EditorShell] Shutdown\n";
}
