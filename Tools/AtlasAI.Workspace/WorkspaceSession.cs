using System;
using System.Collections.Generic;

namespace AtlasAI.Workspace;

/// Represents the state of a single workspace session.
public class WorkspaceSession
{
    public string SessionId { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string WorkspacePath { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime LastAccessedAt { get; set; } = DateTime.UtcNow;
    public DateTime? ClosedAt { get; set; }
    public bool IsActive { get; set; } = true;
    public string ActiveFile { get; set; } = string.Empty;
    public List<string> OpenFiles { get; set; } = new();
    public List<string> RecentFiles { get; set; } = new();
    public Dictionary<string, string> Settings { get; set; } = new();
    public string Theme { get; set; } = "Dark";
    public bool IsModified { get; set; } = false;

    public TimeSpan Duration => IsActive
        ? DateTime.UtcNow - CreatedAt
        : (ClosedAt ?? DateTime.UtcNow) - CreatedAt;

    public void TouchAccess() => LastAccessedAt = DateTime.UtcNow;

    public void AddOpenFile(string filePath)
    {
        if (!OpenFiles.Contains(filePath))
            OpenFiles.Add(filePath);
        TouchAccess();
    }

    public bool CloseFile(string filePath)
    {
        var removed = OpenFiles.Remove(filePath);
        if (removed) TouchAccess();
        return removed;
    }
}
