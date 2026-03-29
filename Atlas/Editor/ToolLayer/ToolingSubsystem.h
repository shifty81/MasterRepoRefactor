#pragma once

class ToolingSubsystem
{
public:
    bool Initialize();
    void Tick(float DeltaTime);
    void Shutdown();

private:
    bool bOverlayEnabled = true;
};
