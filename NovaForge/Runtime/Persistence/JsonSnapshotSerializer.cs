using System.Text.Json;

namespace Runtime.NovaForge.Persistence;

public sealed class JsonSnapshotSerializer
{
    private static readonly JsonSerializerOptions Options = new()
    {
        WriteIndented = true
    };

    public string Serialize(object snapshot)
    {
        return JsonSerializer.Serialize(snapshot, Options);
    }

    public T? Deserialize<T>(string json)
    {
        return JsonSerializer.Deserialize<T>(json, Options);
    }
}
