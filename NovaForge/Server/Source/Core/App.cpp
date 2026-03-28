#include "Core/App.h"
#include "Core/EngineKernel.h"
#include <iostream>

bool App::Initialize()
{
    Kernel = std::make_unique<EngineKernel>();
    if (!Kernel->Initialize())
    {
        return false;
    }

    bRunning = true;
    return true;
}

void App::Run()
{
    constexpr int TickCount = 5;
    constexpr float DeltaTime = 1.0f / 60.0f;

    std::cout << "=== MasterRepo Phase 2 Runtime Boot ===\n";
    for (int TickIndex = 0; TickIndex < TickCount && bRunning; ++TickIndex)
    {
        std::cout << "[App] Tick " << TickIndex << "\n";
        Kernel->Tick(DeltaTime);
    }
}

void App::Shutdown()
{
    if (Kernel)
    {
        Kernel->Shutdown();
        Kernel.reset();
    }

    bRunning = false;
    std::cout << "=== MasterRepo Phase 2 Runtime Shutdown ===\n";
}
