#include "Renderer.h"
#include <iostream>

bool Renderer::Initialize()
{
    std::cout << "[Renderer] Initialize\n";
    return true;
}

void Renderer::Render(const World&)
{
    std::cout << "[Renderer] Render\n";
}

void Renderer::Shutdown()
{
    std::cout << "[Renderer] Shutdown\n";
}
