// AtlasBuildService.h
// Build orchestration service — queues, runs, and reports build tasks.

#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include <functional>

namespace Atlas::Services
{

enum class BuildStatus : uint8_t
{
    Idle, Queued, Running, Succeeded, Failed, Cancelled
};

enum class BuildTarget : uint8_t
{
    Editor, Client, Server, Tests, All
};

struct BuildRequest
{
    BuildTarget target        = BuildTarget::Editor;
    std::string configuration = "Debug";   ///< "Debug", "Release", "Shipping"
    std::string platform      = "x64";
    bool        clean         = false;
    bool        dryRun        = true;
};

struct BuildJob
{
    uint64_t    jobId         = 0;
    BuildRequest request;
    BuildStatus  status       = BuildStatus::Queued;
    std::string  startedAt;
    std::string  completedAt;
    std::string  logOutput;
    int32_t      exitCode     = 0;
};

using BuildProgressCallback = std::function<void(uint64_t jobId, float percent, const std::string& message)>;

class AtlasBuildService
{
public:
    AtlasBuildService()  = default;
    ~AtlasBuildService() = default;

    void initialise();
    void shutdown();

    uint64_t queueBuild(const BuildRequest& request);
    bool     cancelBuild(uint64_t jobId);
    BuildJob queryJob(uint64_t jobId) const;
    std::vector<BuildJob> listJobs() const;
    BuildStatus overallStatus() const;

    void setProgressCallback(BuildProgressCallback cb);

private:
    std::vector<BuildJob> jobs_;
    uint64_t nextJobId_ = 1;
    BuildProgressCallback progressCallback_;
};

} // namespace Atlas::Services
