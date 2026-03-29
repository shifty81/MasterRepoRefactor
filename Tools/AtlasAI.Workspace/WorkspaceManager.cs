using System;
using System.Collections.Generic;

namespace AtlasAI.Workspace;

/// Manages active workspace sessions and their lifecycle.
public class WorkspaceManager
{
    private readonly Dictionary<string, WorkspaceSession> _sessions = new();
    private int _nextId = 0;

    public WorkspaceSession CreateSession(string name, string workspacePath = "")
    {
        var sessionId = $"session_{_nextId++:D4}";
        var session = new WorkspaceSession
        {
            SessionId = sessionId,
            Name = name,
            WorkspacePath = workspacePath,
            CreatedAt = DateTime.UtcNow,
            LastAccessedAt = DateTime.UtcNow,
            IsActive = true,
        };
        _sessions[sessionId] = session;
        return session;
    }

    public WorkspaceSession? GetSession(string sessionId)
        => _sessions.TryGetValue(sessionId, out var s) ? s : null;

    public bool CloseSession(string sessionId)
    {
        if (!_sessions.TryGetValue(sessionId, out var session)) return false;
        session.IsActive = false;
        session.ClosedAt = DateTime.UtcNow;
        return true;
    }

    public bool RemoveSession(string sessionId)
        => _sessions.Remove(sessionId);

    public IReadOnlyList<string> ListSessionIds() => new List<string>(_sessions.Keys);

    public IReadOnlyList<WorkspaceSession> GetActiveSessions()
    {
        var result = new List<WorkspaceSession>();
        foreach (var s in _sessions.Values)
            if (s.IsActive) result.Add(s);
        return result;
    }

    public int SessionCount => _sessions.Count;
    public int ActiveSessionCount => GetActiveSessions().Count;

    public bool SetWorkspacePath(string sessionId, string path)
    {
        if (!_sessions.TryGetValue(sessionId, out var session)) return false;
        session.WorkspacePath = path;
        session.LastAccessedAt = DateTime.UtcNow;
        return true;
    }

    public void Clear()
    {
        _sessions.Clear();
        _nextId = 0;
    }
}
