#include "ArbiterBridgeService.h"

namespace NovaForge::Arbiter
{
    FArbiterBridgeService::FArbiterBridgeService() = default;
    FArbiterBridgeService::~FArbiterBridgeService() = default;

    bool FArbiterBridgeService::Start(int Port)
    {
        ActivePort = Port;
        bRunning = true;
        return true;
    }

    void FArbiterBridgeService::Stop()
    {
        bRunning = false;
    }

    bool FArbiterBridgeService::IsRunning() const
    {
        return bRunning;
    }

    FProjectInfo FArbiterBridgeService::GetProjectInfo() const
    {
        return FProjectInfo{
            "novaforge",
            "NovaForge",
            "0.1.0",
            { "editor", "client", "server", "tests" },
            {
                "project.info",
                "build.run",
                "files.open",
                "analysis.lint",
                "editor.selection.query",
                "editor.tools.list",
                "editor.tools.run",
                "assets.generate.request",
                "logs.stream"
            }
        };
    }

    FBuildResult FArbiterBridgeService::RunBuild(const FBuildRequest& Request) const
    {
        FBuildResult Result;
        Result.Code = EBridgeResultCode::Ok;
        Result.Success = false;
        Result.TargetId = Request.TargetId;
        Result.Summary = "Build execution is not wired yet. Hook this to your build runner.";
        Result.LogPath = "Saved/Logs/arbiter_bridge_build.log";
        return Result;
    }

    bool FArbiterBridgeService::OpenFileInEditor(const FOpenFileRequest& Request) const
    {
        (void)Request;
        return false;
    }

    FEditorSelectionSnapshot FArbiterBridgeService::GetEditorSelection() const
    {
        return FEditorSelectionSnapshot{
            "None",
            "",
            "",
            ""
        };
    }

    FToolActionResult FArbiterBridgeService::RunToolAction(const FToolActionRequest& Request) const
    {
        FToolActionResult Result;
        Result.Code = EBridgeResultCode::Unsupported;
        Result.Success = false;
        Result.ActionId = Request.ActionId;
        Result.Message = "Tool action is not implemented yet.";
        Result.JsonResult = "{}";
        return Result;
    }
}
