#pragma once

#include "ArbiterBridgeTypes.h"

namespace NovaForge::Arbiter
{
    class FArbiterBridgeService
    {
    public:
        FArbiterBridgeService();
        ~FArbiterBridgeService();

        bool Start(int Port = 8005);
        void Stop();
        bool IsRunning() const;

        FProjectInfo GetProjectInfo() const;
        FBuildResult RunBuild(const FBuildRequest& Request) const;
        bool OpenFileInEditor(const FOpenFileRequest& Request) const;
        FEditorSelectionSnapshot GetEditorSelection() const;
        FToolActionResult RunToolAction(const FToolActionRequest& Request) const;

    private:
        bool bRunning = false;
        int ActivePort = 8005;
    };
}
