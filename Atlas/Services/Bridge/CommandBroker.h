#pragma once

#include "common/Status.h"

#include <filesystem>
#include <string>
#include <vector>

namespace Atlas::Bridge {

struct ToolDefinition {
    std::string toolId;
    std::string exe;
    std::vector<std::string> allowedArgs;
    bool networkAccess{false};
};

struct CommandRequest {
    std::string toolId;
    std::vector<std::string> args;
    std::filesystem::path workingDirectory;
    bool dryRun{true};
};

struct CommandResult {
    Atlas::Common::Status status;
    int exitCode{0};
    std::string commandLine;
};

class CommandBroker {
public:
    bool LoadAllowlist(const std::filesystem::path& path);
    CommandResult Execute(const CommandRequest& request) const;

private:
    std::vector<ToolDefinition> tools_;
    const ToolDefinition* FindTool(const std::string& toolId) const;
    bool ArgsAllowed(const ToolDefinition& tool, const std::vector<std::string>& args) const;
};

} // namespace Atlas::Bridge
