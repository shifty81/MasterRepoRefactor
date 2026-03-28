using AtlasSuite.Core.Jobs;

namespace AtlasSuite.Core.Abstractions;

public interface IJobRunner
{
    event EventHandler<JobRecord>? JobCompleted;
    void Enqueue(JobDefinition job);
    IReadOnlyCollection<JobRecord> Snapshot();
}
