#include "bridge/CommandBroker.h"

#include "common/TextUtil.h"

#include <sstream>

namespace Atlas::Bridge {

bool CommandBroker::LoadAllowlist(const std::filesystem::path& path) {
    const std::string json = Atlas::Common::ReadTextFile(path);
    if (json.empty()) {
        return false;
    }

    tools_.clear();
    const auto lines = Atlas::Common::SplitLines(json);
    ToolDefinition current;
    bool inObject = false;
    for (auto rawLine : lines) {
        const auto line = Atlas::Common::Trim(rawLine);
        if (line.find('{') != std::string::npos) {
            current = {};
            inObject = true;
        }
        if (!inObject) continue;

        if (line.find("\"toolId\"") != std::string::npos) current.toolId = Atlas::Common::ExtractString(line, "toolId");
        if (line.find("\"exe\"") != std::string::npos) current.exe = Atlas::Common::ExtractString(line, "exe");
        if (line.find("\"networkAccess\"") != std::string::npos) current.networkAccess = Atlas::Common::ExtractBool(line, "networkAccess", false);
        if (line.find("\"allowedArgs\"") != std::string::npos) current.allowedArgs = Atlas::Common::ExtractStringArray(line, "allowedArgs");

        if (line.find('}') != std::string::npos && !current.toolId.empty()) {
            tools_.push_back(current);
            inObject = false;
        }
    }
    return !tools_.empty();
}

const ToolDefinition* CommandBroker::FindTool(const std::string& toolId) const {
    for (const auto& tool : tools_) {
        if (tool.toolId == toolId) {
            return &tool;
        }
    }
    return nullptr;
}

bool CommandBroker::ArgsAllowed(const ToolDefinition& tool, const std::vector<std::string>& args) const {
    for (const auto& arg : args) {
        bool matched = false;
        for (const auto& allowed : tool.allowedArgs) {
            if (arg == allowed || arg.rfind(allowed, 0) == 0) {
                matched = true;
                break;
            }
        }
        if (!matched) {
            return false;
        }
    }
    return true;
}

CommandResult CommandBroker::Execute(const CommandRequest& request) const {
    const ToolDefinition* tool = FindTool(request.toolId);
    if (!tool) {
        return {Atlas::Common::Status::Error("tool is not allowlisted"), -1, {}};
    }
    if (!ArgsAllowed(*tool, request.args)) {
        return {Atlas::Common::Status::Error("arguments not allowlisted"), -2, {}};
    }

    std::ostringstream cmd;
    cmd << tool->exe;
    for (const auto& arg : request.args) {
        cmd << ' ' << arg;
    }

    if (request.dryRun) {
        return {Atlas::Common::Status::Ok("dry run only"), 0, cmd.str()};
    }

    // Intentionally not executing arbitrary processes here.
    // Wire this to a platform-specific broker runner after integrating the policy layer.
    return {Atlas::Common::Status::Error("live process execution is intentionally disabled in scaffold"), -3, cmd.str()};
}

} // namespace Atlas::Bridge
