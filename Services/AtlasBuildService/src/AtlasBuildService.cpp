// AtlasBuildService.cpp
#include "AtlasBuildService.h"

namespace Atlas::Services
{

void AtlasBuildService::initialise() {}
void AtlasBuildService::shutdown()   {}

uint64_t AtlasBuildService::queueBuild(const BuildRequest& req)
{
    BuildJob job;
    job.jobId   = nextJobId_++;
    job.request = req;
    job.status  = req.dryRun ? BuildStatus::Succeeded : BuildStatus::Queued;
    job.logOutput = req.dryRun ? "[dry-run] Build simulated successfully." : "";
    jobs_.push_back(job);
    if (progressCallback_ && req.dryRun)
        progressCallback_(job.jobId, 100.0f, "Dry-run complete");
    return job.jobId;
}

bool AtlasBuildService::cancelBuild(uint64_t jobId)
{
    for (auto& j : jobs_)
    {
        if (j.jobId == jobId && j.status == BuildStatus::Queued)
        {
            j.status = BuildStatus::Cancelled;
            return true;
        }
    }
    return false;
}

BuildJob AtlasBuildService::queryJob(uint64_t jobId) const
{
    for (const auto& j : jobs_)
        if (j.jobId == jobId) return j;
    return {};
}

std::vector<BuildJob> AtlasBuildService::listJobs() const { return jobs_; }

BuildStatus AtlasBuildService::overallStatus() const
{
    for (const auto& j : jobs_)
        if (j.status == BuildStatus::Running || j.status == BuildStatus::Queued)
            return BuildStatus::Running;
    return BuildStatus::Idle;
}

void AtlasBuildService::setProgressCallback(BuildProgressCallback cb)
{
    progressCallback_ = std::move(cb);
}

} // namespace Atlas::Services
