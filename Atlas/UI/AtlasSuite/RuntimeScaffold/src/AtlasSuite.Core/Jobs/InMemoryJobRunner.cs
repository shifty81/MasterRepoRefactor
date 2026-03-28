using AtlasSuite.Core.Abstractions;

namespace AtlasSuite.Core.Jobs;

public sealed class InMemoryJobRunner : IJobRunner
{
    private readonly List<JobRecord> _records = [];

    public event EventHandler<JobRecord>? JobCompleted;

    public void Enqueue(JobDefinition job)
    {
        ArgumentNullException.ThrowIfNull(job);
        _ = ExecuteAsync(job);
    }

    public IReadOnlyCollection<JobRecord> Snapshot() => _records.ToArray();

    private async Task ExecuteAsync(JobDefinition job)
    {
        var started = new JobRecord(job.Id, job.Label, DateTimeOffset.UtcNow, null, "Running");
        _records.Add(started);

        try
        {
            await job.Work(CancellationToken.None).ConfigureAwait(false);
            var completed = started with { FinishedUtc = DateTimeOffset.UtcNow, Status = "Completed" };
            _records.Remove(started);
            _records.Add(completed);
            JobCompleted?.Invoke(this, completed);
        }
        catch (Exception ex)
        {
            var failed = started with { FinishedUtc = DateTimeOffset.UtcNow, Status = "Failed", Error = ex.Message };
            _records.Remove(started);
            _records.Add(failed);
            JobCompleted?.Invoke(this, failed);
        }
    }
}
