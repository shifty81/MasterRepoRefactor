#pragma once

class ArbiterBridgeService
{
public:
    bool Start(int port = 8005);
    void Stop();
};
