using System.Collections.Generic;
using System.Linq;

namespace Runtime.NovaForge.Persistence;

public sealed class PersistenceRegistry
{
    private readonly List<IPersistenceContributor> _contributors = new();

    public void Register(IPersistenceContributor contributor)
    {
        _contributors.Add(contributor);
    }

    public IReadOnlyList<IPersistenceContributor> GetContributors()
    {
        return _contributors;
    }

    public IPersistenceContributor? Find(string contributorId)
    {
        return _contributors.FirstOrDefault(x => x.ContributorId == contributorId);
    }
}
