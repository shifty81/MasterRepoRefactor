#pragma once

class World;

class Renderer
{
public:
    bool Initialize();
    void Render(const World& WorldRef);
    void Shutdown();
};
