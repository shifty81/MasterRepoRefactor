#pragma once

#include <string>
#include <vector>
#include <optional>

namespace NovaForge::Arbiter
{
    enum class EBridgeResultCode
    {
        Ok = 0,
        InvalidRequest,
        Unauthorized,
        Unsupported,
        InternalError,
        Timeout
    };

    struct FProjectInfo
    {
        std::string ProjectId;
        std::string DisplayName;
        std::string Version;
        std::vector<std::string> BuildTargets;
        std::vector<std::string> Capabilities;
    };

    struct FBuildRequest
    {
        std::string TargetId;
        bool Clean = false;
        bool Verbose = false;
    };

    struct FBuildResult
    {
        EBridgeResultCode Code = EBridgeResultCode::Ok;
        bool Success = false;
        std::string TargetId;
        std::string Summary;
        std::string LogPath;
    };

    struct FOpenFileRequest
    {
        std::string RelativePath;
        std::optional<int> Line;
        std::optional<int> Column;
    };

    struct FEditorSelectionSnapshot
    {
        std::string ActiveScene;
        std::string SelectedObjectId;
        std::string SelectedObjectName;
        std::string SelectedObjectType;
    };

    struct FToolActionRequest
    {
        std::string ActionId;
        std::string JsonPayload;
        bool DryRun = true;
    };

    struct FToolActionResult
    {
        EBridgeResultCode Code = EBridgeResultCode::Ok;
        bool Success = false;
        std::string ActionId;
        std::string Message;
        std::string JsonResult;
    };
}
